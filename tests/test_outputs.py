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
        urgency = pressure + carry_in // 5
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
