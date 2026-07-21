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
    assert AUDIT.exists(), "the audit CLI was not created at /app/flow_audit.py"


def test_repair_writes_all_five_artifacts(repaired):
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
    report = tmp_path / "again.json"
    subprocess.run(
        [sys.executable, str(AUDIT), "diagnose", "--dossier", str(DOSSIER), "--report", str(report)],
        capture_output=True, text=True, check=True)
    body = json.loads(report.read_text())
    assert body["defect_count"] == len(SPEC["known_defects"])


# ------------------------------------------------------------ diagnosis -----
def test_diagnosis_schema(repaired):
    body = json.loads((repaired / "diagnosis.json").read_text())
    assert set(body) == set(SPEC["diagnosis_report"]["required_keys"])
    assert body["schema_version"] == SPEC["diagnosis_report"]["schema_version"]
    assert set(body["input_stats"]) == set(SPEC["diagnosis_report"]["input_stats_keys"])
    for defect in body["defects"]:
        assert set(defect) == set(SPEC["diagnosis_report"]["defect_keys"])


def test_diagnosis_input_stats_match_the_raw_stream(repaired):
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
    body = json.loads((repaired / "diagnosis.json").read_text())
    payload = "\n".join(
        f"{d['defect_id']}|{d['stage']}|{d['repair_action']}" for d in body["defects"])
    assert body["diagnosis_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


# ----------------------------------------------------------- repair audit ---
def test_repair_audit_schema(repaired):
    audit = json.loads((repaired / "repair_audit.json").read_text())
    assert set(audit) == set(SPEC["repair_audit"]["required_keys"])
    assert audit["schema_version"] == SPEC["repair_audit"]["schema_version"]


def test_pre_repair_hash_is_read_from_the_frozen_snapshot(repaired):
    audit = json.loads((repaired / "repair_audit.json").read_text())
    raw = FROZEN.read_bytes()
    assert audit["pre_repair_sha256"] == hashlib.sha256(raw).hexdigest()
    assert audit["pre_repair_byte_count"] == len(raw)


def test_frozen_snapshot_is_unchanged(repaired):
    assert FROZEN.read_text() == EXPECTED["frozen_source"]


def test_post_repair_hash_matches_the_restored_workflow(repaired):
    audit = json.loads((repaired / "repair_audit.json").read_text())
    raw = WORKFLOW.read_bytes()
    assert audit["post_repair_sha256"] == hashlib.sha256(raw).hexdigest()
    assert audit["post_repair_byte_count"] == len(raw)
    assert audit["post_repair_sha256"] != audit["pre_repair_sha256"]


def test_forbidden_tokens_are_gone_from_the_restored_workflow(repaired):
    source = WORKFLOW.read_text()
    audit = json.loads((repaired / "repair_audit.json").read_text())
    for token in SPEC["workflow_repair"]["forbidden_tokens"]:
        assert token not in source, f"defective construct still present: {token}"
    assert sorted(audit["forbidden_tokens_removed"]) == sorted(
        SPEC["workflow_repair"]["forbidden_tokens"])


def test_audit_lists_every_defect_and_artifact(repaired):
    audit = json.loads((repaired / "repair_audit.json").read_text())
    assert sorted(audit["defects_repaired"]) == sorted(
        d["defect_id"] for d in SPEC["known_defects"])
    assert set(audit["artifacts"]) >= {
        "summary.json", "subnet_matrix.json", "quarantined.jsonl",
        "diagnosis.json", "repair_audit.json"}


def test_source_does_not_reference_verifier_trees():
    source = AUDIT.read_text() + WORKFLOW.read_text()
    for token in ("/tests", "/solution", "expected_outputs.json"):
        assert token not in source


# --------------------------------------------------------------- outputs ----
def test_summary_matches_fixture(repaired):
    assert json.loads((repaired / "summary.json").read_text()) == EXPECTED["primary"]["summary"]


def test_subnet_matrix_matches_fixture(repaired):
    assert json.loads((repaired / "subnet_matrix.json").read_text()) == EXPECTED["primary"]["matrix"]


def test_quarantined_queue_matches_fixture(repaired):
    assert _jsonl(repaired / "quarantined.jsonl") == EXPECTED["primary"]["queue"]


def test_summary_schema(repaired):
    summary = json.loads((repaired / "summary.json").read_text())
    assert set(summary) == set(SPEC["outputs"]["summary_json"]["required_keys"])
    assert list(summary["tier_counts"]) == CLASS_ORDER
    assert list(summary["priority_counts"]) == PRIORITY_ORDER
    assert summary["subnets"] == sorted(summary["subnets"])
    for key in ("canonical_flow_checksum", "flow_policy_checksum", "quarantine_checksum"):
        assert len(summary[key]) == 64


def test_subnet_matrix_shape(repaired):
    matrix = json.loads((repaired / "subnet_matrix.json").read_text())
    assert isinstance(matrix, dict) and matrix
    wanted = set(SPEC["outputs"]["subnet_matrix_json"]["required_keys"])
    for row in matrix.values():
        assert set(row) == wanted


def test_queue_row_shape_and_vocabulary(repaired):
    rows = _jsonl(repaired / "quarantined.jsonl")
    wanted = set(SPEC["outputs"]["quarantined_jsonl"]["required_keys"])
    for row in rows:
        assert set(row) == wanted
        assert row["top_tier"] in CLASS_ORDER
        assert row["priority"] in PRIORITY_ORDER
        assert row["flow_ids"] == sorted(row["flow_ids"])
        assert row["case_id"] == f"{row['subnet']}:{row['start_ms']}-{row['end_ms']}"


def test_quarantined_jsonl_is_compact(repaired):
    for line in (repaired / "quarantined.jsonl").read_text().splitlines():
        if line.strip():
            assert ", " not in line and '": ' not in line


# ------------------------------------------------------------- behaviour ----
def test_tier_counts_cover_every_canonical_row_including_blocked(repaired):
    summary = json.loads((repaired / "summary.json").read_text())
    assert sum(summary["tier_counts"].values()) == summary["canonical_flow_count"]
    assert summary["blocked_excluded_count"] > 0, "the stream must contain blocked flows"


def test_duplicate_flows_are_collapsed_before_aggregates(repaired):
    summary = json.loads((repaired / "summary.json").read_text())
    rows = json.loads(EVENTS.read_text())
    assert summary["raw_flow_count"] == len(rows)
    assert summary["canonical_flow_count"] < summary["raw_flow_count"]
    assert summary["canonical_flow_count"] == summary["unique_flow_ids"]


def test_unknown_trust_tier_falls_back_to_visitor(repaired):
    """TQ-3316: an unrecognized class becomes visitor, the LOWEST class."""
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
    for row in _jsonl(repaired / "quarantined.jsonl"):
        payload = (f"{row['subnet']}|{row['start_ms']}|{row['end_ms']}"
                   f"|{','.join(row['flow_ids'])}|{row['top_tier']}|{row['ledger_hold_ms']}")
        assert row["hold_digest"] == hashlib.sha256(payload.encode()).hexdigest()[:12]


def test_quarantine_checksum_consistent(repaired):
    summary = json.loads((repaired / "summary.json").read_text())
    rows = _jsonl(repaired / "quarantined.jsonl")
    payload = "\n".join(
        f"{r['case_id']}|{r['priority']}|{r['ledger_hold_ms']}|{r['hold_digest']}" for r in rows)
    assert summary["quarantine_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


def test_flow_policy_checksum_consistent(repaired):
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
    first = _repair(tmp_path / "a")
    second = _repair(tmp_path / "b")
    for name in ("summary.json", "subnet_matrix.json", "quarantined.jsonl"):
        assert (first / name).read_text() == (second / name).read_text()


def test_generalizes_to_alternate_stream(tmp_path):
    out = _repair(tmp_path / "alt", input_path=ALT_EVENTS)
    assert json.loads((out / "summary.json").read_text()) == EXPECTED["alternate"]["summary"]
    assert json.loads((out / "subnet_matrix.json").read_text()) == EXPECTED["alternate"]["matrix"]
    assert _jsonl(out / "quarantined.jsonl") == EXPECTED["alternate"]["queue"]


def test_custom_output_dir_is_honoured(tmp_path):
    out = tmp_path / "elsewhere"
    subprocess.run([sys.executable, str(AUDIT), "repair", "--output-dir", str(out)],
                   capture_output=True, text=True, check=True)
    assert (out / "summary.json").exists()
    assert (out / "repair_audit.json").exists()
