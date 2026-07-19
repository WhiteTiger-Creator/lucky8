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
    per_bundle: dict[str, dict] = {}
    critical_response_ids: list[str] = []
    max_urgency = 0
    ledger_rows: list[str] = []
    for b in bundles:
        assets = set(b["assets"])
        shared_prev = len(assets & prev_assets)
        carry_in = max(prev_carry_out - (shared_prev * 7) // 3, 0)
        pressure = b["severity"] * len(assets)
        # Carry credit into urgency is rounded UP (ceil) per SR-2219. ceil(x/5)=-(-x//5).
        urgency = pressure + (-(-carry_in // 5))
        carry_out = min(carry_in + pressure - (len(assets) // 2), CARRY_CAP)
        if urgency >= URGENCY_THRESHOLD:
            critical_response_ids.append(b["id"])
        max_urgency = max(max_urgency, urgency)
        ledger_rows.append(f"{b['id']}|{urgency}|{1 if urgency >= URGENCY_THRESHOLD else 0}|{carry_out}")
        per_bundle[b["id"]] = {
            "urgency": urgency,
            "urgency_carry_out": carry_out,
            "critical_response": 1 if urgency >= URGENCY_THRESHOLD else 0,
        }
        prev_carry_out = carry_out
        prev_assets = assets
    critical_response_ids = sorted(critical_response_ids)
    critical_response_count = len(critical_response_ids)
    urgency_ledger_checksum = hashlib.sha256("\n".join(ledger_rows).encode("utf-8")).hexdigest()

    # Remediation response-wave layer. Each contained bundle carries the conflict
    # load it inherits from the bundles that were NOT contained but contend for
    # its assets. The conflict half of the response_load is HALVED AND ROUNDED UP (ceil)
    # per SR-2231, while the asset relief that follows it is floored; ceil(x/2) is
    # written -(-x // 2). Both terms clamp the response load at zero. The response-wave
    # floor sits directly on the response_load distribution, so a one-unit slip in a
    # conflict count, a ceil read as a floor, or a wrong contained set moves
    # bundles across the boundary and changes the wave membership, the tier
    # counts, the response order and the wave checksum together.
    RESPONSE_WAVE_FLOOR = 16
    RESPONSE_TIERS = ("immediate", "urgent", "routine")
    CLASS_RANK = {n: len(RESPONSE_TIERS) - i for i, n in enumerate(RESPONSE_TIERS)}
    uncontained_bundles = [b for b in bundles if b["id"] not in contained_set]
    total_exposure_overlap = 0
    wave_candidates = []
    for b in bundles:
        if b["id"] not in contained_set:
            continue
        assets = set(b["assets"])
        exposure_overlap = sum(len(assets & set(o["assets"])) for o in uncontained_bundles)
        exposing_bundle_count = sum(1 for o in uncontained_bundles if assets & set(o["assets"]))
        total_exposure_overlap += exposure_overlap
        response_load = max(b["severity"] * 3 + (-(-exposure_overlap // 2)) - (len(assets) // 2), 0)
        wave_candidates.append(
            {
                "id": b["id"],
                "severity": b["severity"],
                "n_assets": len(assets),
                "exposure_overlap": exposure_overlap,
                "exposing_bundle_count": exposing_bundle_count,
                "response_load": response_load,
            }
        )
    admitted = [r for r in wave_candidates if r["response_load"] >= RESPONSE_WAVE_FLOOR]
    # Class per SR-2233, clauses in order; the first match fixes the class.
    for r in admitted:
        if r["response_load"] >= 27:
            r["response_tier"] = "immediate"
        elif r["response_load"] >= 21 or r["exposure_overlap"] >= 4:
            r["response_tier"] = "urgent"
        else:
            r["response_tier"] = "routine"
    response_tier_counts = {n: 0 for n in RESPONSE_TIERS}
    for r in admitted:
        response_tier_counts[r["response_tier"]] += 1
    ordered_wave = sorted(
        admitted,
        key=lambda r: (
            -CLASS_RANK[r["response_tier"]],
            -r["response_load"],
            -r["severity"],
            -r["exposing_bundle_count"],
            r["id"],
        ),
    )
    response_order = [r["id"] for r in ordered_wave]
    response_wave_ids = sorted(r["id"] for r in admitted)
    response_wave_count = len(admitted)
    total_response_load = sum(r["response_load"] for r in admitted)
    max_response_load = max((r["response_load"] for r in admitted), default=0)
    response_wave_checksum = hashlib.sha256(
        "\n".join(
            f"{r['id']}|{r['response_tier']}|{r['response_load']}|{r['exposure_overlap']}"
            for r in ordered_wave
        ).encode("utf-8")
    ).hexdigest()

    # Per-asset exposure view, governed by SR-2239. This is the asset-centric
    # counterpart of the bundle ledger: for each asset in the estate it records how
    # many proposed bundles contend for it, which contained bundle actually locks it
    # (if any), and the contention pressure that contention represents.
    asset_claims: dict[int, list[dict]] = {}
    for b in bundles:
        for a in b["assets"]:
            asset_claims.setdefault(int(a), []).append(b)
    asset_records = []
    for asset_id in range(asset_count):
        claims = asset_claims.get(asset_id, [])
        claim_ids = sorted(b["id"] for b in claims)
        locker = next((b["id"] for b in claims if b["id"] in contained_set), "none")
        asset_records.append(
            {
                "asset_id": asset_id,
                "claiming_bundle_count": len(claims),
                "claiming_bundle_ids": claim_ids,
                "locked_by": locker,
                "is_locked": 0 if locker == "none" else 1,
                "max_claim_severity": max((b["severity"] for b in claims), default=0),
                "total_claim_pressure": sum(b["severity"] for b in claims),
                "contention": max(len(claims) - 1, 0),
            }
        )
    asset_records.sort(
        key=lambda r: (-r["contention"], -r["total_claim_pressure"], -r["is_locked"], r["asset_id"])
    )
    asset_exposure_checksum = hashlib.sha256(
        "\n".join(
            f"{r['asset_id']}|{r['claiming_bundle_count']}|{r['locked_by']}|"
            f"{r['is_locked']}|{r['max_claim_severity']}|{r['total_claim_pressure']}|{r['contention']}"
            for r in asset_records
        ).encode("utf-8")
    ).hexdigest()

    # Per-bundle remediation ledger, emitted as compact JSON lines. One row per
    # canonical bundle carrying every derived per-bundle value, ordered per SR-2237:
    # contained bundles first, then response_load descending, then urgency descending,
    # then severity descending, then id ascending.
    wave_by_id = {r["id"]: r for r in wave_candidates}
    admitted_ids = {r["id"] for r in admitted}
    ledger_records = []
    for b in bundles:
        bid = b["id"]
        assets = set(b["assets"])
        tier = "critical" if b["severity"] >= 7 else "major" if b["severity"] >= 4 else "minor"
        wave = wave_by_id.get(bid)
        ledger_records.append(
            {
                "bundle_id": bid,
                "severity": b["severity"],
                "severity_tier": tier,
                "n_assets": len(assets),
                "asset_pressure": b["severity"] * len(assets),
                "contained": 1 if bid in contained_set else 0,
                "urgency": per_bundle[bid]["urgency"],
                "urgency_carry_out": per_bundle[bid]["urgency_carry_out"],
                "critical_response": per_bundle[bid]["critical_response"],
                "exposure_overlap": wave["exposure_overlap"] if wave else 0,
                "exposing_bundle_count": wave["exposing_bundle_count"] if wave else 0,
                "response_load": wave["response_load"] if wave else 0,
                "in_response_wave": 1 if bid in admitted_ids else 0,
                "response_tier": wave.get("response_tier", "none") if wave else "none",
            }
        )
    ledger_records.sort(
        key=lambda r: (-r["contained"], -r["response_load"], -r["urgency"], -r["severity"], r["bundle_id"])
    )

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
        f"{total_exposure_overlap}|{response_wave_count}|{total_response_load}|"
        f"{max_response_load}|"
        f"{response_tier_counts['immediate']},{response_tier_counts['urgent']},{response_tier_counts['routine']}|"
        f"{','.join(response_order)}|"
        f"{','.join(contained_bundle_ids)}"
    )
    plan_checksum = hashlib.sha256(plan_payload.encode("utf-8")).hexdigest()

    return {
        "_ledger_records": ledger_records,
        "_asset_records": asset_records,
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
        "asset_exposure_checksum": asset_exposure_checksum,
        "total_exposure_overlap": total_exposure_overlap,
        "response_wave_ids": response_wave_ids,
        "response_wave_count": response_wave_count,
        "total_response_load": total_response_load,
        "max_response_load": max_response_load,
        "response_tier_counts": response_tier_counts,
        "response_order": response_order,
        "response_wave_checksum": response_wave_checksum,
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
    records = result.pop("_ledger_records")
    assets = result.pop("_asset_records")
    (out / "plan.json").write_text(json.dumps(result, indent=2) + "\n")
    with (out / "remediation_ledger.jsonl").open("w", encoding="utf-8") as handle:
        for row in records:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    with (out / "asset_exposure.jsonl").open("w", encoding="utf-8") as handle:
        for row in assets:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
