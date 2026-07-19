"""Verifier for the Sentinel-1 remediation-planning task.

The agent's /app/remediate.py is run against the shipped bundle set and against a
held-out alternate set. Outputs are checked against exact fixtures and against
structural invariants (canonical checksum, the asset-disjoint packing objective,
and the fact that neither the total-severity sum nor a greedy selection is the
answer).
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

APP = Path("/app/remediate.py")
DATA = Path("/app/data/remediation.json")
TEST_DIR = Path(os.environ.get("TEST_DIR", "/tests"))
FIX = TEST_DIR / "fixtures"
EXPECTED = json.loads((FIX / "expected_plan.json").read_text())


def _run(tmp: Path, input_path: Path = DATA) -> dict:
    out = tmp / "out"
    subprocess.run(
        [sys.executable, str(APP), "--input", str(input_path), "--output-dir", str(out)],
        check=True, capture_output=True, text=True,
    )
    return json.loads((out / "plan.json").read_text())


def _canonical(bundle_rows):
    by_id = {}
    for row in bundle_rows:
        bid = str(row["id"])
        sev = int(row["severity"])
        assets = sorted({int(a) for a in row["assets"]})
        if sev < 1 or sev > 9 or not assets:
            continue
        if bid not in by_id or sev > by_id[bid]["severity"]:
            by_id[bid] = {"id": bid, "severity": sev, "assets": assets}
    return [by_id[bid] for bid in sorted(by_id)]


def _sum_all(bundle_rows):
    return sum(b["severity"] for b in _canonical(bundle_rows))


def _greedy(bundle_rows):
    used, total = set(), 0
    for b in sorted(_canonical(bundle_rows), key=lambda b: -b["severity"]):
        assets = set(b["assets"])
        if not (assets & used):
            used |= assets
            total += b["severity"]
    return total


@pytest.fixture(scope="module")
def result(tmp_path_factory) -> dict:
    """Run the agent's planner once on the shipped bundle set."""
    assert APP.exists(), "remediate.py is missing"
    return _run(tmp_path_factory.mktemp("primary"))


def test_result_has_required_keys(result):
    """plan.json carries exactly the contracted key set."""
    assert set(result) == {"asset_count", "bundle_count", "total_proposed_severity",
                           "max_single_bundle_severity", "max_contained_severity",
                           "contained_bundle_ids", "contained_bundle_count",
                           "contained_asset_count", "uncontained_severity",
                           "residual_contained_severity", "proposed_tier_counts",
                           "contained_tier_counts", "total_asset_pressure",
                           "max_asset_pressure", "containment_score",
                           "coverage_permille", "residual_pressure",
                           "critical_response_ids", "critical_response_count",
                           "max_urgency", "urgency_ledger_checksum",
                           "total_exposure_overlap", "response_wave_ids",
                           "response_wave_count", "total_response_load",
                           "max_response_load", "response_tier_counts",
                           "response_order", "response_wave_checksum",
                           "bundle_checksum", "plan_checksum"}


def test_matches_fixture(result):
    """The full plan matches the reference fixture exactly."""
    assert result == EXPECTED


def test_generalizes_to_alternate_input(tmp_path):
    """The planner reproduces the reference output for a held-out bundle set."""
    alt_expected = json.loads((FIX / "alt_expected.json").read_text())
    got = _run(tmp_path, input_path=FIX / "alt_remediation.json")
    assert got == alt_expected


def test_bundle_checksum_consistent(result):
    """bundle_checksum is the SHA-256 of the canonical-bundle serialization."""
    data = json.loads(DATA.read_text())
    bundles = _canonical(data["bundles"])
    payload = "\n".join(
        f"{b['id']}|{b['severity']}|{','.join(str(a) for a in b['assets'])}" for b in bundles
    )
    assert result["bundle_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


def test_plan_checksum_consistent(result):
    """plan_checksum is the SHA-256 of the contracted plan payload."""
    pc = result["proposed_tier_counts"]
    cc = result["contained_tier_counts"]
    sc = result["response_tier_counts"]
    payload = (
        f"{result['asset_count']}|{result['total_proposed_severity']}|"
        f"{result['max_single_bundle_severity']}|{result['max_contained_severity']}|"
        f"{result['contained_asset_count']}|{result['residual_contained_severity']}|"
        f"{result['total_asset_pressure']}|{result['max_asset_pressure']}|"
        f"{result['containment_score']}|{result['coverage_permille']}|"
        f"{result['residual_pressure']}|"
        f"{pc['critical']},{pc['major']},{pc['minor']}|"
        f"{cc['critical']},{cc['major']},{cc['minor']}|"
        f"{result['critical_response_count']}|{result['max_urgency']}|"
        f"{','.join(result['critical_response_ids'])}|"
        f"{result['total_exposure_overlap']}|{result['response_wave_count']}|"
        f"{result['total_response_load']}|{result['max_response_load']}|"
        f"{sc['immediate']},{sc['urgent']},{sc['routine']}|"
        f"{','.join(result['response_order'])}|"
        f"{','.join(result['contained_bundle_ids'])}"
    )
    assert result["plan_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


def test_response_urgency_ledger_consistent(result):
    """The response-urgency ledger reproduces the log-governed carry/threshold rule."""
    data = json.loads(DATA.read_text())
    bundles = _canonical(data["bundles"])
    prev_out, prev = 0, set()
    crit, max_u, rows = [], 0, []
    for b in bundles:
        assets = set(b["assets"])
        shared = len(assets & prev)
        carry_in = max(prev_out - (shared * 7) // 3, 0)
        pressure = b["severity"] * len(assets)
        urgency = pressure + (-(-carry_in // 5))
        carry_out = min(carry_in + pressure - (len(assets) // 2), 90)
        if urgency >= 30:
            crit.append(b["id"])
        max_u = max(max_u, urgency)
        rows.append(f"{b['id']}|{urgency}|{1 if urgency >= 30 else 0}|{carry_out}")
        prev_out, prev = carry_out, assets
    assert result["critical_response_ids"] == sorted(crit)
    assert result["critical_response_count"] == len(crit)
    assert result["max_urgency"] == max_u
    assert result["urgency_ledger_checksum"] == hashlib.sha256("\n".join(rows).encode()).hexdigest()


def test_scoring_layer_consistent(result):
    """Tier counts and pressure aggregates follow the log-governed formulas."""
    data = json.loads(DATA.read_text())
    bundles = _canonical(data["bundles"])
    contained = set(result["contained_bundle_ids"])
    def tier(s):
        return "critical" if s >= 7 else "major" if s >= 4 else "minor"
    exp_prop = {"critical": 0, "major": 0, "minor": 0}
    exp_cont = {"critical": 0, "major": 0, "minor": 0}
    pressures, score, residual = [], 0, 0
    for b in bundles:
        exp_prop[tier(b["severity"])] += 1
        p = b["severity"] * len(b["assets"])
        pressures.append(p)
        if b["id"] in contained:
            exp_cont[tier(b["severity"])] += 1
            score += (b["severity"] * 5 + len(b["assets"]) * 2) // 3
        else:
            residual += p
    assert result["proposed_tier_counts"] == exp_prop
    assert result["contained_tier_counts"] == exp_cont
    assert result["total_asset_pressure"] == sum(pressures)
    assert result["max_asset_pressure"] == (max(pressures) if pressures else 0)
    assert result["containment_score"] == score
    assert result["residual_pressure"] == residual
    ac = result["asset_count"]
    assert result["coverage_permille"] == (result["contained_asset_count"] * 1000 // ac if ac else 0)


def test_contained_set_is_valid_optimal_and_disjoint(result):
    """contained_bundle_ids is a pairwise asset-disjoint set summing to the objective."""
    data = json.loads(DATA.read_text())
    by_id = {b["id"]: b for b in _canonical(data["bundles"])}
    chosen = result["contained_bundle_ids"]
    assert chosen == sorted(chosen), "contained_bundle_ids must be ascending"
    assert result["contained_bundle_count"] == len(chosen)
    used, total, assets_all = set(), 0, set()
    for bid in chosen:
        assets = set(by_id[bid]["assets"])
        assert not (assets & used), "contained set is not asset-disjoint"
        used |= assets
        total += by_id[bid]["severity"]
        assets_all |= assets
    assert total == result["max_contained_severity"], "contained set severity != objective"
    assert result["contained_asset_count"] == len(assets_all)
    assert result["uncontained_severity"] == result["total_proposed_severity"] - result["max_contained_severity"]


def test_residual_is_below_contained(result):
    """The residual packing (over unselected bundles) is a valid, smaller packing."""
    assert 0 <= result["residual_contained_severity"] <= result["max_contained_severity"]


def test_canonicalization_drops_invalid(result):
    """bundle_count reflects canonicalization (invalid/empty/dup bundles removed)."""
    data = json.loads(DATA.read_text())
    assert result["bundle_count"] == len(_canonical(data["bundles"]))
    assert result["bundle_count"] < len(data["bundles"])


def test_contained_is_packing_not_total_sum(result):
    """max_contained_severity is the packing, strictly below the total-severity sum here."""
    data = json.loads(DATA.read_text())
    assert result["max_contained_severity"] <= _sum_all(data["bundles"])
    assert result["max_contained_severity"] != result["total_proposed_severity"], \
        "max_contained_severity equals the total sum (wrong objective)"


def test_contained_beats_greedy(result):
    """The exact packing is at least, and here strictly above, a greedy selection."""
    data = json.loads(DATA.read_text())
    greedy = _greedy(data["bundles"])
    assert result["max_contained_severity"] >= greedy
    assert result["max_contained_severity"] != greedy, \
        "max_contained_severity equals the greedy selection (not the exact optimum)"


def test_source_does_not_reference_verifier_trees():
    """The planner source does not read or import verifier artifacts."""
    src = APP.read_text()
    for token in ("/tests", "/solution", "expected_plan.json", "alt_expected.json"):
        assert token not in src


RESPONSE_TIERS = ("immediate", "urgent", "routine")
CLASS_RANK = {n: len(RESPONSE_TIERS) - i for i, n in enumerate(RESPONSE_TIERS)}


def _response_wave_layer(bundles: list[dict], contained_ids: list[str]) -> list[dict]:
    """Recompute the response-wave layer per SR-2231/2233/2235, independently."""
    contained = set(contained_ids)
    uncontained = [b for b in bundles if b["id"] not in contained]
    rows = []
    for b in bundles:
        if b["id"] not in contained:
            continue
        assets = set(b["assets"])
        exposure_overlap = sum(len(assets & set(o["assets"])) for o in uncontained)
        exposing_bundle_count = sum(1 for o in uncontained if assets & set(o["assets"]))
        response_load = max(
            b["severity"] * 3 + (-(-exposure_overlap // 2)) - (len(assets) // 2), 0
        )
        rows.append({"id": b["id"], "severity": b["severity"],
                     "exposure_overlap": exposure_overlap,
                     "exposing_bundle_count": exposing_bundle_count, "response_load": response_load})
    admitted = [r for r in rows if r["response_load"] >= 16]
    for r in admitted:
        if r["response_load"] >= 27:
            r["response_tier"] = "immediate"
        elif r["response_load"] >= 21 or r["exposure_overlap"] >= 4:
            r["response_tier"] = "urgent"
        else:
            r["response_tier"] = "routine"
    return sorted(admitted, key=lambda r: (-CLASS_RANK[r["response_tier"]], -r["response_load"],
                                           -r["severity"], -r["exposing_bundle_count"], r["id"]))


def test_response_wave_layer_matches_independent_computation(result):
    """The response-wave layer reproduces the log-governed response_load, admission and ordering."""
    bundles = _canonical(json.loads(DATA.read_text())["bundles"])
    ordered = _response_wave_layer(bundles, result["contained_bundle_ids"])
    assert result["response_order"] == [r["id"] for r in ordered]
    assert result["response_wave_ids"] == sorted(r["id"] for r in ordered)
    assert result["response_wave_count"] == len(ordered)
    assert result["total_response_load"] == sum(r["response_load"] for r in ordered)
    assert result["max_response_load"] == max((r["response_load"] for r in ordered), default=0)
    expected_counts = {n: 0 for n in RESPONSE_TIERS}
    for r in ordered:
        expected_counts[r["response_tier"]] += 1
    assert list(result["response_tier_counts"]) == list(RESPONSE_TIERS)
    assert result["response_tier_counts"] == expected_counts


def test_response_wave_checksum_and_conflict_load_consistent(result):
    """response_wave_checksum hashes the ordered response-wave rows; exposure overlap covers the contained set."""
    bundles = _canonical(json.loads(DATA.read_text())["bundles"])
    ordered = _response_wave_layer(bundles, result["contained_bundle_ids"])
    payload = "\n".join(
        f"{r['id']}|{r['response_tier']}|{r['response_load']}|{r['exposure_overlap']}"
        for r in ordered
    )
    assert result["response_wave_checksum"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    contained = set(result["contained_bundle_ids"])
    uncontained = [b for b in bundles if b["id"] not in contained]
    assert result["total_exposure_overlap"] == sum(
        len(set(b["assets"]) & set(o["assets"]))
        for b in bundles if b["id"] in contained
        for o in uncontained
    )


def test_response_load_exposure_half_is_ceilinged(result):
    """The conflict half of response_load rounds UP; a floored halving admits a different set."""
    bundles = _canonical(json.loads(DATA.read_text())["bundles"])
    contained = set(result["contained_bundle_ids"])
    uncontained = [b for b in bundles if b["id"] not in contained]
    floored = []
    for b in bundles:
        if b["id"] not in contained:
            continue
        assets = set(b["assets"])
        ca = sum(len(assets & set(o["assets"])) for o in uncontained)
        if max(b["severity"] * 3 + (ca // 2) - (len(assets) // 2), 0) >= 16:
            floored.append(b["id"])
    assert sorted(floored) != result["response_wave_ids"]


LEDGER_FIELDS = ("bundle_id","severity","severity_tier","n_assets","asset_pressure","contained",
                 "urgency","urgency_carry_out","critical_response","exposure_overlap",
                 "exposing_bundle_count","response_load","in_response_wave","response_tier")


def _run_ledger(tmp: Path, input_path: Path = DATA) -> list[dict]:
    out = tmp / "out"
    subprocess.run([sys.executable, str(APP), "--input", str(input_path), "--output-dir", str(out)],
                   check=True, capture_output=True, text=True)
    path = out / "remediation_ledger.jsonl"
    assert path.exists(), "remediation_ledger.jsonl was not written"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_ledger_matches_fixture(tmp_path):
    """remediation_ledger.jsonl matches the reference fixture row for row."""
    expected = [json.loads(line) for line in (FIX / "expected_ledger.jsonl").read_text().splitlines() if line.strip()]
    assert _run_ledger(tmp_path) == expected


def test_ledger_generalizes_to_alternate_input(tmp_path):
    """The ledger reproduces the reference rows for a held-out input."""
    expected = [json.loads(line) for line in (FIX / "alt_expected_ledger.jsonl").read_text().splitlines() if line.strip()]
    assert _run_ledger(tmp_path, FIX / "alt_remediation.json") == expected


def test_ledger_covers_every_canonical_bundle(tmp_path, result):
    """One row per canonical bundle -- uncontained and non-wave bundles included."""
    rows = _run_ledger(tmp_path)
    assert len(rows) == result["bundle_count"]
    assert sorted(r["bundle_id"] for r in rows) == sorted(
        b["id"] for b in _canonical(json.loads(DATA.read_text())["bundles"]))
    assert {r["bundle_id"] for r in rows} >= set(result["contained_bundle_ids"])


def test_ledger_row_shape_and_flag_types(tmp_path):
    """Every row carries the fourteen contracted keys, with integer 0/1 flags."""
    for row in _run_ledger(tmp_path):
        assert tuple(row) == LEDGER_FIELDS
        for flag in ("contained", "critical_response", "in_response_wave"):
            assert row[flag] in (0, 1) and isinstance(row[flag], int) and not isinstance(row[flag], bool)
        assert row["response_tier"] in ("immediate", "urgent", "routine", "none")
        if row["in_response_wave"] == 0 and row["contained"] == 0:
            assert row["exposure_overlap"] == 0
            assert row["exposing_bundle_count"] == 0
            assert row["response_load"] == 0


def test_ledger_row_order_follows_sr_2237(tmp_path):
    """Rows follow the log's ordering chain, not bundle-id order."""
    rows = _run_ledger(tmp_path)
    keyed = [(-r["contained"], -r["response_load"], -r["urgency"], -r["severity"], r["bundle_id"])
             for r in rows]
    assert keyed == sorted(keyed)
    assert [r["bundle_id"] for r in rows] != sorted(r["bundle_id"] for r in rows)


def test_ledger_jsonl_is_compact(tmp_path):
    """Ledger rows use compact separators, one row per line."""
    out = tmp_path / "c"
    subprocess.run([sys.executable, str(APP), "--input", str(DATA), "--output-dir", str(out)],
                   check=True, capture_output=True, text=True)
    for line in (out / "remediation_ledger.jsonl").read_text().splitlines():
        if line.strip():
            assert ", " not in line and '": ' not in line


def test_contained_below_floor_keeps_its_computed_load(tmp_path):
    """SR-2237: the zero-reporting rule keys off `contained`, not `in_response_wave`.

    A contained bundle that fell below the wave admission floor keeps the response_load
    that kept it out; only uncontained bundles report zero.
    """
    rows = _run_ledger(tmp_path)
    uncontained = [r for r in rows if r["contained"] == 0]
    assert uncontained, "fixture must exercise at least one uncontained bundle"
    for r in uncontained:
        assert (r["exposure_overlap"], r["exposing_bundle_count"], r["response_load"]) == (0, 0, 0)
    below = [r for r in rows if r["contained"] == 1 and r["in_response_wave"] == 0]
    assert below, "fixture must exercise a contained bundle below the wave floor"
    for r in below:
        assert r["response_load"] > 0
        assert r["response_tier"] == "none"
