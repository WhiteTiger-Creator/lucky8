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
        # SR-2243: for a repeated id the LOWER severity is kept.
        if bid not in by_id or sev < by_id[bid]["severity"]:
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
                           "max_urgency", "urgency_ledger_checksum", "asset_exposure_checksum",
                           "total_exposure_overlap", "policy_checksum", "response_wave_ids",
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
        pol = _pol(b["severity"])
        carry_out = min(carry_in + pressure - (len(assets) // 2), pol["carry_cap"])
        if urgency >= pol["urgency_threshold"]:
            crit.append(b["id"])
        max_u = max(max_u, urgency)
        rows.append(f"{b['id']}|{urgency}|{1 if urgency >= pol['urgency_threshold'] else 0}|{carry_out}")
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
        # SR-2241: shared assets are attributed to one owner only.
        exposure_overlap = 0
        for o in uncontained:
            shared = assets & set(o["assets"])
            if not shared:
                continue
            claimants = [c for c in bundles
                         if c["id"] in contained and set(o["assets"]) & set(c["assets"])]
            owner = sorted(claimants, key=lambda c: (-c["severity"], c["id"]))[0]
            if owner["id"] == b["id"]:
                exposure_overlap += len(shared)
        exposing_bundle_count = sum(1 for o in uncontained if assets & set(o["assets"]))
        response_load = max(
            b["severity"] * 3 + (-(-exposure_overlap // 2)) - (len(assets) // 2), 0
        )
        rows.append({"id": b["id"], "severity": b["severity"],
                     "exposure_overlap": exposure_overlap,
                     "exposing_bundle_count": exposing_bundle_count, "response_load": response_load})
    admitted = [r for r in rows if r["response_load"] >= _pol(r["severity"])["wave_floor"]]
    for r in admitted:
        rp = _pol(r["severity"])
        if r["response_load"] >= rp["immediate_min"]:
            r["response_tier"] = "immediate"
        elif r["response_load"] >= rp["urgent_min"] or r["exposure_overlap"] >= rp["urgent_overlap_min"]:
            r["response_tier"] = "urgent"
        else:
            r["response_tier"] = "routine"
    ordered = sorted(admitted, key=lambda r: (-CLASS_RANK[r["response_tier"]], -r["response_load"],
                                              -r["severity"], -r["exposing_bundle_count"], r["id"]))
    # SR-2245: capacity cap applied AFTER the ordering chain, two per tier.
    kept = {}
    capped = []
    for r in ordered:
        taken = kept.get(r["response_tier"], 0)
        if taken < 2:
            capped.append(r)
            kept[r["response_tier"]] = taken + 1
    return capped


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
    bundles_all = _canonical(json.loads(DATA.read_text())["bundles"])
    contained_set = set(result["contained_bundle_ids"])
    unc = [x for x in bundles_all if x["id"] not in contained_set]
    expected_exposure = 0
    for o in unc:
        claimants = [c for c in bundles_all
                     if c["id"] in contained_set and set(o["assets"]) & set(c["assets"])]
        if not claimants:
            continue
        owner = sorted(claimants, key=lambda c: (-c["severity"], c["id"]))[0]
        expected_exposure += len(set(owner["assets"]) & set(o["assets"]))
    assert result["total_exposure_overlap"] == expected_exposure


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
        if max(b["severity"] * 3 + (ca // 2) - (len(assets) // 2), 0) >= _pol(b["severity"])["wave_floor"]:
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


ASSET_FIELDS = ("asset_id","claiming_bundle_count","claiming_bundle_ids","locked_by",
                "is_locked","max_claim_severity","total_claim_severity","contention")


def _run_assets(tmp: Path, input_path: Path = DATA) -> list[dict]:
    out = tmp / "out"
    subprocess.run([sys.executable, str(APP), "--input", str(input_path), "--output-dir", str(out)],
                   check=True, capture_output=True, text=True)
    path = out / "asset_exposure.jsonl"
    assert path.exists(), "asset_exposure.jsonl was not written"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_assets_match_fixture(tmp_path):
    """asset_exposure.jsonl matches the reference fixture row for row."""
    expected = [json.loads(line) for line in (FIX / "expected_assets.jsonl").read_text().splitlines() if line.strip()]
    assert _run_assets(tmp_path) == expected


def test_assets_generalize_to_alternate_input(tmp_path):
    """The asset view reproduces the reference rows for a held-out input."""
    expected = [json.loads(line) for line in (FIX / "alt_expected_assets.jsonl").read_text().splitlines() if line.strip()]
    assert _run_assets(tmp_path, FIX / "alt_remediation.json") == expected


def test_assets_cover_the_whole_estate(tmp_path, result):
    """Every asset id 0..asset_count-1 is reported, including unclaimed ones."""
    rows = _run_assets(tmp_path)
    assert sorted(r["asset_id"] for r in rows) == list(range(result["asset_count"]))
    assert all(tuple(r) == ASSET_FIELDS for r in rows)
    for r in rows:
        assert r["is_locked"] in (0, 1) and not isinstance(r["is_locked"], bool)
        assert r["contention"] == max(r["claiming_bundle_count"] - 1, 0)
        if r["claiming_bundle_count"] == 0:
            assert r["locked_by"] == "none" and r["total_claim_severity"] == 0


def test_asset_locker_is_unique_and_contained(tmp_path, result):
    """locked_by names a contained bundle, and containment disjointness makes it unique."""
    rows = _run_assets(tmp_path)
    contained = set(result["contained_bundle_ids"])
    for r in rows:
        if r["locked_by"] != "none":
            assert r["locked_by"] in contained
            assert r["locked_by"] in r["claiming_bundle_ids"]
            assert sum(1 for b in r["claiming_bundle_ids"] if b in contained) == 1


def test_asset_row_order_follows_sr_2239(tmp_path):
    """Asset rows follow the log's ordering chain, not ascending asset id."""
    rows = _run_assets(tmp_path)
    keyed = [(-r["contention"], -r["total_claim_severity"], -r["is_locked"], r["asset_id"]) for r in rows]
    assert keyed == sorted(keyed)
    assert [r["asset_id"] for r in rows] != sorted(r["asset_id"] for r in rows)


def test_asset_exposure_checksum_consistent(tmp_path, result):
    """asset_exposure_checksum hashes the emitted asset rows in order."""
    rows = _run_assets(tmp_path)
    payload = "\n".join(
        f"{r['asset_id']}|{r['claiming_bundle_count']}|{r['locked_by']}|{r['is_locked']}|"
        f"{r['max_claim_severity']}|{r['total_claim_severity']}|{r['contention']}" for r in rows)
    assert result["asset_exposure_checksum"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_total_claim_severity_is_not_a_sum_of_asset_pressure(tmp_path):
    """SR-2239: total_claim_severity sums raw severities, never asset_pressure.

    asset_pressure is severity * n_assets, so summing it gives a different number for
    any asset claimed by a multi-asset bundle. The shipped estate is required to make
    the two readings disagree, so this misreading cannot pass unnoticed.
    """
    rows = _run_assets(tmp_path)
    bundles = {b["id"]: b for b in _canonical(json.loads(DATA.read_text())["bundles"])}
    disagreed = 0
    for r in rows:
        claims = [bundles[b] for b in r["claiming_bundle_ids"]]
        correct = sum(b["severity"] for b in claims)
        wrong = sum(b["severity"] * len(b["assets"]) for b in claims)
        assert r["total_claim_severity"] == correct
        assert r["max_claim_severity"] == max((b["severity"] for b in claims), default=0)
        if correct != wrong:
            disagreed += 1
    assert disagreed, "estate must contain an asset where the two readings differ"


def test_sr_2241_owner_counts_only_its_own_intersection(result):
    """SR-2241: the owner adds |owner_assets & uncontained_assets|, nothing more.

    Three readings of the attribution rule are possible and two of them coincide
    numerically, so a bare total does not discriminate between them. This pins the
    governing one and asserts the alternatives are genuinely different, which is
    what makes the assertion meaningful rather than tautological.
    """
    bundles = _canonical(json.loads(DATA.read_text())["bundles"])
    contained = set(result["contained_bundle_ids"])
    con = [b for b in bundles if b["id"] in contained]
    unc = [b for b in bundles if b["id"] not in contained]

    def owner_of(o):
        claimants = [c for c in con if set(o["assets"]) & set(c["assets"])]
        return sorted(claimants, key=lambda c: (-c["severity"], c["id"]))[0] if claimants else None

    governing = 0          # owner counts only its own intersection
    owner_absorbs_all = 0  # owner absorbs the whole contended set
    every_claimant = 0     # no ownership filter at all
    for o in unc:
        owner = owner_of(o)
        shared_any = set()
        for c in con:
            shared_any |= set(o["assets"]) & set(c["assets"])
            every_claimant += len(set(o["assets"]) & set(c["assets"]))
        if owner is not None:
            governing += len(set(owner["assets"]) & set(o["assets"]))
            owner_absorbs_all += len(shared_any)

    assert result["total_exposure_overlap"] == governing
    assert governing != owner_absorbs_all, "readings coincide -- test cannot discriminate"
    assert governing != every_claimant, "readings coincide -- test cannot discriminate"


POLICY_PATH = Path("/app/data/remediation_policies.json")
POLICY_FIELDS = (
    "wave_floor", "immediate_min", "urgent_min", "urgent_overlap_min",
    "urgency_threshold", "carry_cap",
)
BASELINE_POLICY = {
    "wave_floor": 16, "immediate_min": 27, "urgent_min": 21,
    "urgent_overlap_min": 4, "urgency_threshold": 30, "carry_cap": 90,
}


def _resolve_band(band, data):
    base = dict(BASELINE_POLICY)
    for k in POLICY_FIELDS:
        if k in data.get("default", {}):
            base[k] = int(data["default"][k])
    raw = data.get("band_overrides", {}).get(band)
    if not isinstance(raw, dict):
        return base
    merged = dict(base)
    for k in POLICY_FIELDS:
        if k in raw:
            merged[k] = int(raw[k])
    return merged


def test_policy_source_path_affects_output(tmp_path: Path):
    """SR-2248: thresholds come from the policy file, not hardcoded constants."""
    original = POLICY_PATH.read_text(encoding="utf-8")
    try:
        base = _run(tmp_path / "base")
        bumped = json.loads(original)
        bumped["default"]["wave_floor"] = 999
        POLICY_PATH.write_text(json.dumps(bumped), encoding="utf-8")
        changed = _run(tmp_path / "changed")
        assert changed["response_wave_count"] < base["response_wave_count"]
        assert changed["policy_checksum"] != base["policy_checksum"]
    finally:
        POLICY_PATH.write_text(original, encoding="utf-8")


def test_sparse_band_override_inherits_remaining_fields():
    """A band override names some fields; every unlisted field is inherited."""
    data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    sparse = [b for b, v in data["band_overrides"].items() if len(v) < len(POLICY_FIELDS)]
    assert sparse, "no sparse override -- the inheritance rule is dormant"
    for band in sparse:
        resolved = _resolve_band(band, data)
        assert set(resolved) == set(POLICY_FIELDS)
        for key in POLICY_FIELDS:
            if key not in data["band_overrides"][band]:
                expected = int(data["default"].get(key, BASELINE_POLICY[key]))
                assert resolved[key] == expected, f"{band}.{key} did not inherit"


def test_policy_default_may_omit_fields_and_falls_back_to_baseline():
    """The file default is itself partial; omitted fields keep the shipped baseline."""
    data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    omitted = [k for k in POLICY_FIELDS if k not in data.get("default", {})]
    assert omitted, "file default names every field -- the baseline tier is dormant"
    for key in omitted:
        assert _resolve_band("no-such-band", data)[key] == BASELINE_POLICY[key]


def test_policy_checksum_consistent(result):
    """policy_checksum serializes RESOLVED values, default then low, mid, high."""
    data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    base = _resolve_band("no-such-band", data)
    lines = ["default|" + "|".join(str(base[k]) for k in POLICY_FIELDS)]
    for band in ("low", "mid", "high"):
        resolved = _resolve_band(band, data)
        lines.append(f"{band}|" + "|".join(str(resolved[k]) for k in POLICY_FIELDS))
    expected = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    assert result["policy_checksum"] == expected


def test_band_uses_canonical_severity_not_raw(result):
    """SR-2248 bands on the severity that survives SR-2243, not the raw proposal."""
    raw = json.loads(DATA.read_text())["bundles"]
    canonical = {b["id"]: b["severity"] for b in _canonical(raw)}
    by_id = {}
    for row in raw:
        by_id.setdefault(row["id"], []).append(int(row["severity"]))
    contested = [i for i, v in by_id.items() if len(v) > 1 and max(v) != min(v)]
    assert contested, "no contested duplicate id -- the banding distinction is dormant"
    for bundle_id in contested:
        assert canonical[bundle_id] == min(by_id[bundle_id]), (
            "canonical severity should be the LOWER one per SR-2243"
        )


def _band(severity):
    """SR-2248 banding on the canonical severity."""
    return "low" if severity <= 3 else "mid" if severity <= 6 else "high"


def _pol(severity):
    return _resolve_band(_band(severity), json.loads(POLICY_PATH.read_text(encoding="utf-8")))



ROGUE_KEY_MARKER = "sentinel-remediation-operator"
SUDOERS_ESCALATION = Path("/etc/sudoers.d/sentinel-quarantine")
QUARANTINE_CRED = Path("/app/secrets/quarantine.cred")


def test_rogue_operator_key_revoked():
    """The intrusion's key is gone; legitimate keys, if any, are left in place."""
    keys = Path("/root/.ssh/authorized_keys")
    if keys.exists():
        text = keys.read_text(encoding="utf-8")
        assert ROGUE_KEY_MARKER not in text, "rogue operator key still authorized"
        assert oct(keys.stat().st_mode)[-3:] == "600", "authorized_keys must stay 0600"


def test_sudoers_escalation_removed():
    """The passwordless escalation is removed outright, not weakened or commented."""
    assert not SUDOERS_ESCALATION.exists(), "passwordless sudoers escalation still present"
    for path in Path("/etc/sudoers.d").glob("*"):
        body = path.read_text(encoding="utf-8", errors="ignore")
        assert "svc-quarantine" not in body, f"escalation reintroduced in {path}"


def test_quarantine_credential_locked_down():
    """The credential is still in use: it must be kept, but restricted to root 0600."""
    assert QUARANTINE_CRED.exists(), "operations still needs the credential in place"
    stat = QUARANTINE_CRED.stat()
    assert oct(stat.st_mode)[-3:] == "600", "credential must be mode 0600"
    assert stat.st_uid == 0 and stat.st_gid == 0, "credential must be owned by root:root"
