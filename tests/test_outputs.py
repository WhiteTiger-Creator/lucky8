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
    payload = (
        f"{result['asset_count']}|{result['total_proposed_severity']}|"
        f"{result['max_single_bundle_severity']}|{result['max_contained_severity']}"
    )
    assert result["plan_checksum"] == hashlib.sha256(payload.encode()).hexdigest()


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
