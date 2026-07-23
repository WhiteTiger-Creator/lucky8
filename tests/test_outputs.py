"""Verifier tests for the Tideguard flow-access containment audit task."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

AUDIT = Path("/app/flow_audit.py")
WORKFLOW = Path("/app/workflow/export_report.py")
FROZEN = Path("/app/workflow/.export_report.original")
DOSSIER = Path("/app/incident/flow_review_dossier.md")
SPEC_PATH = Path("/app/docs/report_spec.json")
EVENTS = Path("/app/data/flow_events.json")
CONTROLS = Path("/app/data/flow_policies.json")
FIX = Path("/tests/fixtures")
ALT_EVENTS = FIX / "alt_flow_events.json"

SPEC = json.loads(SPEC_PATH.read_text())
EXPECTED = json.loads((FIX / "expected_outputs.json").read_text())

CLASS_ORDER = ["core", "service", "user", "guest"]
PRIORITY_ORDER = ["critical", "elevated", "routine"]
CLASS_RANK = {n: len(CLASS_ORDER) - i for i, n in enumerate(CLASS_ORDER)}


def _jsonl(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _repair(tmp: Path, input_path: Path | None = None) -> Path:
    out = tmp / "out"
    out.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(AUDIT), "repair", "--output-dir", str(out)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    if input_path is not None:
        res = subprocess.run(
            [sys.executable, str(WORKFLOW), "--input", str(input_path), "--output-dir", str(out)],
            capture_output=True, text=True)
        assert res.returncode == 0, res.stderr
    return out


@pytest.fixture(scope="session")
def repaired(tmp_path_factory) -> Path:
    return _repair(tmp_path_factory.mktemp("primary"))


@pytest.fixture(scope="session", autouse=True)
def _hide_expected_fixture():
    """Keep the expected-output fixture off disk while candidate code runs."""
    stash = FIX / "expected_outputs.json.hidden"
    moved = False
    try:
        if (FIX / "expected_outputs.json").exists():
            (FIX / "expected_outputs.json").rename(stash)
            moved = True
    except OSError:
        moved = False
    try:
        yield
    finally:
        if moved:
            stash.rename(FIX / "expected_outputs.json")


# ----------------------------------------------------------------- CLI ------
def test_cli_exists():
    """The audit CLI is created at its operational path /app/flow_audit.py."""
    assert AUDIT.exists(), "the audit CLI was not created at /app/flow_audit.py"


def test_repair_writes_all_five_artifacts(repaired):
    """A repair run leaves exactly the five contracted artifacts and nothing else: the three containment records plus the diagnosis and the repair audit."""
    names = sorted(p.name for p in repaired.iterdir() if p.is_file())
    assert names == sorted(["quarantined.jsonl", "diagnosis.json", "repair_audit.json",
                            "summary.json", "subnet_matrix.json"])


def test_diagnose_is_stateless(tmp_path):
    """An explicit diagnose call writes a full report with no prior repair."""
    report = tmp_path / "d.json"
    res = subprocess.run(
        [sys.executable, str(AUDIT), "diagnose", "--dossier", str(DOSSIER), "--report", str(report)],
        capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    body = json.loads(report.read_text())
    assert body["defect_count"] == len(SPEC["known_defects"])
    assert [d["defect_id"] for d in body["defects"]] == sorted(
        d["defect_id"] for d in SPEC["known_defects"])


def test_diagnose_after_repair_still_reports_every_defect(repaired, tmp_path):
    """diagnose is stateless: run again after a repair has already completed, it still reports every known containment defect rather than an empty or already-fixed report."""
    report = tmp_path / "again.json"
    subprocess.run(
        [sys.executable, str(AUDIT), "diagnose", "--dossier", str(DOSSIER), "--report", str(report)],
        capture_output=True, text=True, check=True)
    body = json.loads(report.read_text())
    assert body["defect_count"] == len(SPEC["known_defects"])


# ------------------------------------------------------------ diagnosis -----
def test_diagnosis_schema(repaired):
    """diagnosis.json carries exactly the contracted key set, the contracted schema_version literal, and the full input_stats key set."""
    body = json.loads((repaired / "diagnosis.json").read_text())
    assert set(body) == set(SPEC["diagnosis_report"]["required_keys"])
    assert body["schema_version"] == SPEC["diagnosis_report"]["schema_version"]
    assert set(body["input_stats"]) == set(SPEC["diagnosis_report"]["input_stats_keys"])
    for defect in body["defects"]:
        assert set(defect) == set(SPEC["diagnosis_report"]["defect_keys"])


def test_diagnosis_input_stats_match_the_raw_stream(repaired):
    """input_stats describe the RAW telemetry stream - raw row count, distinct flow ids and the excess-duplicate count all follow the input file, not the deduplicated set."""
    body = json.loads((repaired / "diagnosis.json").read_text())
    rows = json.loads(EVENTS.read_text())
    ids = [str(r.get("flow_id", "")).strip() for r in rows]
    present = [i for i in ids if i]
    stats = body["input_stats"]
    assert stats["raw_flow_count"] == len(rows)
    assert stats["unique_flow_ids"] == len(set(present))
    assert stats["duplicate_flow_ids"] == len(present) - len(set(present))
    assert stats["duplicate_flow_ids"] > 0, "the stream must contain duplicates"


def test_dossier_quotes_are_verbatim_dossier_lines(repaired):
    """Evidence must be copied character for character, not paraphrased."""
    body = json.loads((repaired / "diagnosis.json").read_text())
    lines = {line.strip() for line in DOSSIER.read_text().splitlines() if line.strip()}
    for defect in body["defects"]:
        assert defect["dossier_quote"] in lines, (
            f"{defect['defect_id']}: dossier_quote is not a verbatim dossier line")


def test_pipeline_evidence_comes_from_the_frozen_snapshot(repaired):
    """Each defect's pipeline_evidence is a verbatim line from the FROZEN snapshot rather than the live workflow, so the evidence is unchanged by a repair having already run."""
    body = json.loads((repaired / "diagnosis.json").read_text())
    lines = {line.strip() for line in FROZEN.read_text().splitlines() if line.strip()}
    for defect in body["defects"]:
        assert defect["pipeline_evidence"] in lines, (
            f"{defect['defect_id']}: pipeline_evidence is not a verbatim frozen-snapshot line")


def test_each_defect_cites_the_expected_evidence(repaired):
    """The quote for a defect must actually contain that defect's search terms."""
    body = json.loads((repaired / "diagnosis.json").read_text())
    by_id = {d["defect_id"]: d for d in body["defects"]}
    for entry in SPEC["known_defects"]:
        got = by_id[entry["defect_id"]]
        low = got["dossier_quote"].lower()
        for term in entry["dossier_terms"]:
            assert term.lower() in low, f"{entry['defect_id']}: quote misses {term!r}"
        assert got["stage"] == entry["stage"]
        assert got["repair_action"] == entry["repair_action"]


def test_diagnosis_checksum_consistent(repaired):
    """The diagnosis checksum is the SHA-256 of the contracted per-defect payload, so it is reproducible from the report's own contents."""
    body = json.loads((repaired / "diagnosis.json").read_text())
    payload = "\n".join(
        f"{d['defect_id']}|{d['stage']}|{d['repair_action']}" for d in body["defects"])
    assert body["diagnosis_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


# ----------------------------------------------------------- repair audit ---
def test_repair_audit_schema(repaired):
    """repair_audit.json carries exactly the eight contracted keys and the contracted schema_version literal - the hash and token fields alone are an incomplete audit."""
    audit = json.loads((repaired / "repair_audit.json").read_text())
    assert set(audit) == set(SPEC["repair_audit"]["required_keys"])
    assert audit["schema_version"] == SPEC["repair_audit"]["schema_version"]


def test_pre_repair_hash_is_read_from_the_frozen_snapshot(repaired):
    """The pre-repair hash and byte count are read from the FROZEN snapshot, so they are identical whether or not a repair already ran."""
    audit = json.loads((repaired / "repair_audit.json").read_text())
    raw = FROZEN.read_bytes()
    assert audit["pre_repair_sha256"] == hashlib.sha256(raw).hexdigest()
    assert audit["pre_repair_byte_count"] == len(raw)


def test_frozen_snapshot_is_unchanged(repaired):
    """The frozen pre-incident snapshot is read-only forensic evidence and remains byte-identical after the repair."""
    assert FROZEN.read_text() == EXPECTED["frozen_source"]


def test_post_repair_hash_matches_the_restored_workflow(repaired):
    """The post-repair hash and byte count describe the restored workflow actually on disk, so they differ from the frozen pre-repair pair."""
    audit = json.loads((repaired / "repair_audit.json").read_text())
    raw = WORKFLOW.read_bytes()
    assert audit["post_repair_sha256"] == hashlib.sha256(raw).hexdigest()
    assert audit["post_repair_byte_count"] == len(raw)
    assert audit["post_repair_sha256"] != audit["pre_repair_sha256"]


def test_forbidden_tokens_are_gone_from_the_restored_workflow(repaired):
    """Every forbidden construct named by the spec is absent from the restored source, and the audit reports exactly those tokens as removed."""
    source = WORKFLOW.read_text()
    audit = json.loads((repaired / "repair_audit.json").read_text())
    for token in SPEC["workflow_repair"]["forbidden_tokens"]:
        assert token not in source, f"defective construct still present: {token}"
    assert sorted(audit["forbidden_tokens_removed"]) == sorted(
        SPEC["workflow_repair"]["forbidden_tokens"])


def test_audit_lists_every_defect_and_artifact(repaired):
    """defects_repaired lists every known defect id as a sorted array of id strings (not a count), and artifacts names the files the repair wrote."""
    audit = json.loads((repaired / "repair_audit.json").read_text())
    assert sorted(audit["defects_repaired"]) == sorted(
        d["defect_id"] for d in SPEC["known_defects"])
    assert set(audit["artifacts"]) >= {
        "summary.json", "subnet_matrix.json", "quarantined.jsonl",
        "diagnosis.json", "repair_audit.json"}


def test_source_does_not_reference_verifier_trees():
    """Neither the audit CLI nor the restored workflow references the verifier tree, so the solution cannot read expected outputs."""
    source = AUDIT.read_text() + WORKFLOW.read_text()
    for token in ("/tests", "/solution", "expected_outputs.json"):
        assert token not in source


# --------------------------------------------------------------- outputs ----
def test_summary_matches_fixture(repaired):
    """summary.json from the primary telemetry stream matches its expected values exactly."""
    assert json.loads((repaired / "summary.json").read_text()) == EXPECTED["primary"]["summary"]


def test_subnet_matrix_matches_fixture(repaired):
    """subnet_matrix.json from the primary telemetry stream matches its expected values exactly."""
    assert json.loads((repaired / "subnet_matrix.json").read_text()) == EXPECTED["primary"]["matrix"]


def test_quarantined_queue_matches_fixture(repaired):
    """quarantined.jsonl from the primary telemetry stream matches its expected rows exactly."""
    assert _jsonl(repaired / "quarantined.jsonl") == EXPECTED["primary"]["queue"]


def test_summary_schema(repaired):
    """summary.json carries the contracted key set, with tier_counts and priority_counts enumerating their vocabularies in the contracted order."""
    summary = json.loads((repaired / "summary.json").read_text())
    assert set(summary) == set(SPEC["outputs"]["summary_json"]["required_keys"])
    assert list(summary["tier_counts"]) == CLASS_ORDER
    assert list(summary["priority_counts"]) == PRIORITY_ORDER
    assert summary["subnets"] == sorted(summary["subnets"])
    for key in ("canonical_flow_checksum", "flow_policy_checksum", "quarantine_checksum"):
        assert len(summary[key]) == 64


def test_subnet_matrix_shape(repaired):
    """subnet_matrix.json is an object keyed by subnet, each value carrying exactly the contracted per-subnet key set."""
    matrix = json.loads((repaired / "subnet_matrix.json").read_text())
    assert isinstance(matrix, dict) and matrix
    wanted = set(SPEC["outputs"]["subnet_matrix_json"]["required_keys"])
    for row in matrix.values():
        assert set(row) == wanted


def test_queue_row_shape_and_vocabulary(repaired):
    """Every queue row carries the complete contracted field set, and its trust tier and priority use only the contracted vocabularies."""
    rows = _jsonl(repaired / "quarantined.jsonl")
    wanted = set(SPEC["outputs"]["quarantined_jsonl"]["required_keys"])
    for row in rows:
        assert set(row) == wanted
        assert row["top_tier"] in CLASS_ORDER
        assert row["priority"] in PRIORITY_ORDER
        assert row["flow_ids"] == sorted(row["flow_ids"])
        assert row["case_id"] == f"{row['subnet']}:{row['start_ms']}-{row['end_ms']}"


def test_quarantined_jsonl_is_compact(repaired):
    """quarantined.jsonl uses compact JSON separators, with no space after a comma or colon."""
    for line in (repaired / "quarantined.jsonl").read_text().splitlines():
        if line.strip():
            assert ", " not in line and '": ' not in line


# ------------------------------------------------------------- behaviour ----
def test_tier_counts_cover_every_canonical_row_including_blocked(repaired):
    """tier_counts covers every canonical row including blocked flows, which open no session but are still counted."""
    summary = json.loads((repaired / "summary.json").read_text())
    assert sum(summary["tier_counts"].values()) == summary["canonical_flow_count"]
    assert summary["blocked_excluded_count"] > 0, "the stream must contain blocked flows"


def test_duplicate_flows_are_collapsed_before_aggregates(repaired):
    """Duplicate flow ids collapse before any aggregate, so the canonical count falls below the raw count while raw_flow_count still reflects the input."""
    summary = json.loads((repaired / "summary.json").read_text())
    rows = json.loads(EVENTS.read_text())
    assert summary["raw_flow_count"] == len(rows)
    assert summary["canonical_flow_count"] < summary["raw_flow_count"]
    assert summary["canonical_flow_count"] == summary["unique_flow_ids"]


def test_unknown_trust_tier_falls_back_to_guest(repaired):
    """TQ-3316: an unrecognized trust tier normalizes to guest, the LOWEST class."""
    rows = json.loads(EVENTS.read_text())
    unknown = [r for r in rows
               if str(r.get("trust_tier", "")).strip().lower() not in CLASS_RANK]
    assert unknown, "the stream must contain an unrecognized flow class"
    summary = json.loads((repaired / "summary.json").read_text())
    assert summary["tier_counts"]["guest"] >= len(unknown)


def test_blocked_flows_open_no_session(repaired):
    """TQ-3322: blocked rows are excluded from sessions but still counted."""
    rows = json.loads(EVENTS.read_text())
    blocked_ids = {
        str(r["flow_id"]).strip() for r in rows
        if r.get("blocked") is True
        or (isinstance(r.get("blocked"), str) and r["blocked"].strip().lower() in {"true", "1", "yes"})
    }
    assert blocked_ids
    for row in _jsonl(repaired / "quarantined.jsonl"):
        assert not (set(row["flow_ids"]) & blocked_ids)


def test_isolation_and_inspection_overlaps_are_reported_unadjusted(repaired):
    """TQ-3328 changes the subtraction only; both overlaps are reported raw."""
    summary = json.loads((repaired / "summary.json").read_text())
    assert summary["total_isolation_overlap_ms"] > 0
    assert summary["total_inspection_overlap_ms"] > 0
    assert summary["total_adjusted_hold_ms"] < summary["total_hold_ms"]


def test_carry_out_never_exceeds_the_retuned_cap(repaired):
    """TQ-3324 retuned the carry-out cap; the superseded 2000 ms bound is not it."""
    summary = json.loads((repaired / "summary.json").read_text())
    assert summary["max_carry_out_ms"] <= 780
    assert summary["max_carry_out_ms"] > 0


def test_queue_follows_the_pac_3334_ordering_chain(repaired):
    """The queue follows the full governed tie-break chain - priority rank, then ledger hold, hold, flow count, subnet and start - rather than entry order."""
    rows = _jsonl(repaired / "quarantined.jsonl")
    rank = {n: len(PRIORITY_ORDER) - i for i, n in enumerate(PRIORITY_ORDER)}
    keys = [(-rank[r["priority"]], -r["ledger_hold_ms"], -r["hold_ms"],
             -r["flow_count"], r["subnet"], r["start_ms"]) for r in rows]
    assert keys == sorted(keys), "queue is not in the governing order"
    assert [r["start_ms"] for r in rows] != sorted(r["start_ms"] for r in rows) or len(rows) < 3


def test_subnet_capacity_cap_applied_after_ordering(repaired):
    """TQ-3330: at most two rows per subnet, retained by the GLOBAL order."""
    rows = _jsonl(repaired / "quarantined.jsonl")
    per_subnet: dict[str, int] = {}
    for row in rows:
        per_subnet[row["subnet"]] = per_subnet.get(row["subnet"], 0) + 1
    assert per_subnet and max(per_subnet.values()) <= 2
    assert any(v == 2 for v in per_subnet.values()), "the cap never binds"


def test_admission_floor_is_per_class(repaired):
    """TQ-3332: every admitted session clears its own class floor."""
    floors = {"core": 150, "service": 190, "user": 240, "guest": 300}
    for row in _jsonl(repaired / "quarantined.jsonl"):
        assert row["ledger_hold_ms"] >= floors[row["top_tier"]]


def test_hold_digest_consistent(repaired):
    """Each queue row's hold digest is reproducible from that row's own contracted payload."""
    for row in _jsonl(repaired / "quarantined.jsonl"):
        payload = (f"{row['subnet']}|{row['start_ms']}|{row['end_ms']}"
                   f"|{','.join(row['flow_ids'])}|{row['top_tier']}|{row['ledger_hold_ms']}"
                   f"|{row['containment_index']}")
        assert row["hold_digest"] == hashlib.sha256(payload.encode()).hexdigest()[:12]


def test_quarantine_checksum_consistent(repaired):
    """The quarantine checksum is reproducible from the emitted queue rows in queue order."""
    summary = json.loads((repaired / "summary.json").read_text())
    rows = _jsonl(repaired / "quarantined.jsonl")
    payload = "\n".join(
        f"{r['case_id']}|{r['priority']}|{r['ledger_hold_ms']}|{r['hold_digest']}" for r in rows)
    assert summary["quarantine_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


def test_flow_policy_checksum_consistent(repaired):
    """The flow-policy checksum is reproducible from the control windows in the contracted ordering."""
    summary = json.loads((repaired / "summary.json").read_text())
    controls = json.loads(CONTROLS.read_text())
    ordered = sorted(controls, key=lambda r: (
        str(r["layer"]), str(r["scope"]), str(r["subnet"]).strip().lower(), int(r["start_ms"])))
    payload = "\n".join(
        f"{r['layer']}|{r['scope']}|{str(r['subnet']).strip().lower()}|{int(r['start_ms'])}|{int(r['end_ms'])}"
        for r in ordered)
    assert summary["flow_policy_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


# --------------------------------------------------------- generalization ---
def test_repair_is_idempotent(tmp_path):
    """Two independent repair runs produce byte-identical containment records."""
    first = _repair(tmp_path / "a")
    second = _repair(tmp_path / "b")
    for name in ("summary.json", "subnet_matrix.json", "quarantined.jsonl"):
        assert (first / name).read_text() == (second / name).read_text()


def test_generalizes_to_alternate_stream(tmp_path):
    """The restored control produces correct output on an alternate telemetry capture it has never seen, so values cannot be hardcoded."""
    out = _repair(tmp_path / "alt", input_path=ALT_EVENTS)
    assert json.loads((out / "summary.json").read_text()) == EXPECTED["alternate"]["summary"]
    assert json.loads((out / "subnet_matrix.json").read_text()) == EXPECTED["alternate"]["matrix"]
    assert _jsonl(out / "quarantined.jsonl") == EXPECTED["alternate"]["queue"]


def test_custom_output_dir_is_honoured(tmp_path):
    """--output-dir redirects every repair output to the requested directory."""
    out = tmp_path / "elsewhere"
    subprocess.run([sys.executable, str(AUDIT), "repair", "--output-dir", str(out)],
                   capture_output=True, text=True, check=True)
    assert (out / "summary.json").exists()
    assert (out / "repair_audit.json").exists()


# --- Host containment: the tampered automation's persistence and escalation paths ---

ROOT_AUTH_KEYS = Path("/root/.ssh/authorized_keys")
SUDOERS_DROPIN = Path("/etc/sudoers.d/tideguard-flow")
COLLECTOR_KEY = Path("/app/secrets/flow_collector.key")
SENTINEL_KEY_MARKER = "netops-oncall@bastion"


def test_sentinel_ssh_key_survives_containment():
    """Containment revokes the rogue key WITHOUT destroying legitimate access.

    root's authorized_keys also holds the netops on-call bastion key. Truncating the
    file or rewriting it wholesale removes the rogue entry but locks responders out,
    so the sentinel must still be present and the file still mode 0600.
    """
    assert ROOT_AUTH_KEYS.exists(), "authorized_keys was deleted; on-call access lost"
    text = ROOT_AUTH_KEYS.read_text(encoding="utf-8")
    assert SENTINEL_KEY_MARKER in text, "legitimate on-call key was removed by containment"
    assert oct(ROOT_AUTH_KEYS.stat().st_mode)[-3:] == "600"


def test_rogue_ssh_key_revoked():
    """The flow-quarantine automation's SSH persistence key is removed from root's authorized_keys."""
    if ROOT_AUTH_KEYS.exists():
        assert "flow-quarantine-automation" not in ROOT_AUTH_KEYS.read_text()


def test_sudoers_escalation_removed():
    """The passwordless sudoers drop-in for svc-tideguard is deleted entirely."""
    assert not SUDOERS_DROPIN.exists()


def test_collector_credential_locked_down():
    """The flow-collector credential is retained but restricted to root-only 0600."""
    import pwd

    assert COLLECTOR_KEY.exists(), "the collector still needs the credential in place"
    info = COLLECTOR_KEY.stat()
    assert (info.st_mode & 0o777) == 0o600
    assert info.st_uid == pwd.getpwnam("root").pw_uid
    assert info.st_gid == pwd.getpwnam("root").pw_gid


def test_probe_pressure_scores_are_nonnegative_integers(repaired):
    """Every queued row carries integer, non-negative isolation and inspection pressure scores.

    This is a shape guard only; the isolation/inspection opposite-rounding rule of
    TQ-3342/TQ-3344 is enforced exactly by the fixture-equality tests, since a swapped
    rounding direction changes the pressure scores and breaks those comparisons.
    """
    rows = _jsonl(repaired / "quarantined.jsonl")
    assert rows, "queue is empty; probe scores cannot be exercised"
    for row in rows:
        assert isinstance(row["isolation_pressure_score"], int)
        assert isinstance(row["inspection_pressure_score"], int)
        assert row["isolation_pressure_score"] >= 0
        assert row["inspection_pressure_score"] >= 0


def test_containment_index_is_the_sum_of_both_probe_families(repaired):
    """TQ-3346: containment_index = isolation + inspection pressure + floored adjusted hold.

    The index is reproducible from fields already on the row, so an implementation that
    computes it from a different combination is detected without re-deriving the probes.
    """
    for row in _jsonl(repaired / "quarantined.jsonl"):
        expected = (row["isolation_pressure_score"] + row["inspection_pressure_score"]
                    + (row["adjusted_hold_ms"] // 40))
        assert row["containment_index"] == expected


def test_containment_index_participates_in_priority(repaired):
    """TQ-3346: a session with containment_index >= 12 is at least elevated.

    The index is a promotion path independent of ledger_hold_ms and flow_count, so an
    implementation that ignores it leaves such sessions at routine.
    """
    for row in _jsonl(repaired / "quarantined.jsonl"):
        if row["containment_index"] >= 12:
            assert row["priority"] in ("critical", "elevated"), row["case_id"]
