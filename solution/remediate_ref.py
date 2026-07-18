#!/usr/bin/env python3
"""Reference implementation of the Sentinel-1 remediation-planning model.

Given a set of proposed remediation bundles that each lock a set of shared
assets, select the maximum-total-severity set of bundles that are pairwise
asset-disjoint, report the contained severity, the tie-broken selected set and
several plan-derived aggregates, plus integrity checksums. See
/app/docs/plan_spec.md for the authoritative contract. The contained severity is
NOT the sum of all bundle severities (bundles compete for assets) and NOT a
greedy highest-severity-first selection (greedy is not optimal) — it is the
exact maximum-weight asset-disjoint packing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SEVERITY_MIN = 1
SEVERITY_MAX = 9


def canonical_bundles(bundle_rows: list[dict]) -> list[dict]:
    """Normalize bundles: drop severities outside 1..9 or empty asset lists;
    for a repeated bundle id keep the one with the maximum severity; assets are
    deduplicated and sorted. Result is sorted by bundle id."""
    by_id: dict[str, dict] = {}
    for row in bundle_rows:
        bid = str(row["id"])
        sev = int(row["severity"])
        assets = sorted({int(a) for a in row["assets"]})
        if sev < SEVERITY_MIN or sev > SEVERITY_MAX or not assets:
            continue
        cur = by_id.get(bid)
        if cur is None or sev > cur["severity"]:
            by_id[bid] = {"id": bid, "severity": sev, "assets": assets}
    return [by_id[bid] for bid in sorted(by_id)]


def _best_packing(bundles: list[dict]) -> tuple[int, list[str]]:
    """Exact maximum-weight asset-disjoint packing.

    Returns (best_total, best_ids) where best_ids is the tie-break-selected set:
    among all pairwise asset-disjoint bundle sets whose summed severity equals
    the maximum, the one whose ids sorted ascending form the lexicographically
    smallest tuple (compared element by element as strings). Ids are returned
    sorted ascending. The empty packing (total 0, no ids) is the baseline.
    """
    items = [(b["severity"], frozenset(b["assets"]), b["id"]) for b in bundles]
    items.sort(key=lambda it: -it[0])
    best_total = 0
    best_ids: tuple[str, ...] = ()

    def rec(index: int, used: frozenset[int], total: int, chosen: list[str]) -> None:
        nonlocal best_total, best_ids
        if index >= len(items):
            key = tuple(sorted(chosen))
            if total > best_total or (total == best_total and key < best_ids):
                best_total = total
                best_ids = key
            return
        rec(index + 1, used, total, chosen)
        severity, assets, bid = items[index]
        if not (assets & used):
            rec(index + 1, used | assets, total + severity, chosen + [bid])

    rec(0, frozenset(), 0, [])
    return best_total, list(best_ids)


def plan_remediation(asset_count: int, bundle_rows: list[dict]) -> dict:
    bundles = canonical_bundles(bundle_rows)

    total_proposed_severity = sum(b["severity"] for b in bundles)
    max_single_bundle_severity = max((b["severity"] for b in bundles), default=0)

    max_contained_severity, contained_bundle_ids = _best_packing(bundles)

    contained_set = set(contained_bundle_ids)
    contained_assets = sorted(
        {a for b in bundles if b["id"] in contained_set for a in b["assets"]}
    )
    contained_asset_count = len(contained_assets)
    contained_bundle_count = len(contained_bundle_ids)
    uncontained_severity = total_proposed_severity - max_contained_severity

    residual_bundles = [b for b in bundles if b["id"] not in contained_set]
    residual_contained_severity, _ = _best_packing(residual_bundles)

    # Severity-tier and pressure scoring layer. Tier cutoffs, the asset-pressure
    # product, the containment-score weights/divisor and the coverage scale are
    # all governed by the review log; each aggregate is a floored integer.
    tiers = ("critical", "major", "minor")
    proposed_tier_counts = {t: 0 for t in tiers}
    contained_tier_counts = {t: 0 for t in tiers}
    asset_pressures = []
    containment_score = 0
    residual_pressure = 0
    for b in bundles:
        tier = "critical" if b["severity"] >= 7 else "major" if b["severity"] >= 4 else "minor"
        proposed_tier_counts[tier] += 1
        pressure = b["severity"] * len(b["assets"])
        asset_pressures.append(pressure)
        if b["id"] in contained_set:
            contained_tier_counts[tier] += 1
            containment_score += (b["severity"] * 5 + len(b["assets"]) * 2) // 3
        else:
            residual_pressure += pressure
    total_asset_pressure = sum(asset_pressures)
    max_asset_pressure = max(asset_pressures, default=0)
    coverage_permille = (contained_asset_count * 1000) // asset_count if asset_count else 0

    # Sequential response-urgency ledger over canonical bundles in id order.
    # Carry propagates between consecutive bundles and decays by a shared-asset
    # penalty; a bundle is admitted to the critical response set when its urgency
    # reaches the threshold. This is boundary-sensitive and order-dependent: a
    # small slip in any floored term shifts a bundle's urgency across the
    # threshold and changes the set, the count and the ledger checksum. The
    # decay/credit divisors, the threshold and the carry cap are governed by the
    # review log.
    URGENCY_THRESHOLD = 30
    CARRY_CAP = 90
    prev_carry_out = 0
    prev_assets: set[int] = set()
    critical_response_ids: list[str] = []
    max_urgency = 0
    ledger_rows: list[str] = []
    for b in bundles:
        assets = set(b["assets"])
        shared_prev = len(assets & prev_assets)
        carry_in = max(prev_carry_out - (shared_prev * 7) // 3, 0)
        pressure = b["severity"] * len(assets)
        urgency = pressure + carry_in // 5
        carry_out = min(carry_in + pressure - (len(assets) // 2), CARRY_CAP)
        if urgency >= URGENCY_THRESHOLD:
            critical_response_ids.append(b["id"])
        max_urgency = max(max_urgency, urgency)
        ledger_rows.append(f"{b['id']}|{urgency}|{1 if urgency >= URGENCY_THRESHOLD else 0}|{carry_out}")
        prev_carry_out = carry_out
        prev_assets = assets
    critical_response_ids = sorted(critical_response_ids)
    critical_response_count = len(critical_response_ids)
    urgency_ledger_checksum = hashlib.sha256("\n".join(ledger_rows).encode("utf-8")).hexdigest()

    bundle_payload = "\n".join(
        f"{b['id']}|{b['severity']}|{','.join(str(a) for a in b['assets'])}" for b in bundles
    )
    bundle_checksum = hashlib.sha256(bundle_payload.encode("utf-8")).hexdigest()

    plan_payload = (
        f"{asset_count}|{total_proposed_severity}|{max_single_bundle_severity}|"
        f"{max_contained_severity}|{contained_asset_count}|{residual_contained_severity}|"
        f"{total_asset_pressure}|{max_asset_pressure}|{containment_score}|"
        f"{coverage_permille}|{residual_pressure}|"
        f"{proposed_tier_counts['critical']},{proposed_tier_counts['major']},{proposed_tier_counts['minor']}|"
        f"{contained_tier_counts['critical']},{contained_tier_counts['major']},{contained_tier_counts['minor']}|"
        f"{critical_response_count}|{max_urgency}|{','.join(critical_response_ids)}|"
        f"{','.join(contained_bundle_ids)}"
    )
    plan_checksum = hashlib.sha256(plan_payload.encode("utf-8")).hexdigest()

    return {
        "asset_count": asset_count,
        "bundle_count": len(bundles),
        "total_proposed_severity": total_proposed_severity,
        "max_single_bundle_severity": max_single_bundle_severity,
        "max_contained_severity": max_contained_severity,
        "contained_bundle_ids": contained_bundle_ids,
        "contained_bundle_count": contained_bundle_count,
        "contained_asset_count": contained_asset_count,
        "uncontained_severity": uncontained_severity,
        "residual_contained_severity": residual_contained_severity,
        "proposed_tier_counts": proposed_tier_counts,
        "contained_tier_counts": contained_tier_counts,
        "total_asset_pressure": total_asset_pressure,
        "max_asset_pressure": max_asset_pressure,
        "containment_score": containment_score,
        "coverage_permille": coverage_permille,
        "residual_pressure": residual_pressure,
        "critical_response_ids": critical_response_ids,
        "critical_response_count": critical_response_count,
        "max_urgency": max_urgency,
        "urgency_ledger_checksum": urgency_ledger_checksum,
        "bundle_checksum": bundle_checksum,
        "plan_checksum": plan_checksum,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/remediation.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text())
    result = plan_remediation(data["asset_count"], data["bundles"])
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "plan.json").write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
