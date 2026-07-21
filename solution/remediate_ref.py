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
POLICY_PATH = Path("/app/data/remediation_policies.json")
POLICY_FIELDS = (
    "wave_floor", "immediate_min", "urgent_min", "urgent_overlap_min",
    "urgency_threshold", "carry_cap",
)
DEFAULT_POLICY = {
    "wave_floor": 16, "immediate_min": 27, "urgent_min": 21,
    "urgent_overlap_min": 4, "urgency_threshold": 30, "carry_cap": 90,
}


def severity_band(severity: int) -> str:
    """SR-2248: bands are 1-3 low, 4-6 mid, 7-9 high, on the CANONICAL severity."""
    if severity <= 3:
        return "low"
    if severity <= 6:
        return "mid"
    return "high"


CONTAINMENT_WINDOWS_PATH = Path("/app/data/containment_windows.json")
CONTAINMENT_LAYERS = ("blackout", "maintenance")


def load_containment_windows(path: Path = CONTAINMENT_WINDOWS_PATH) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def windows_for_band(rows: list[dict], layer: str, band: str) -> list[tuple[int, int]]:
    """SR-2250 scope resolution: a band uses its OWN windows for this layer; only a
    band with no window of its own in this layer borrows the `all` scope. A band that
    has its own entry does NOT additionally inherit `all`."""
    own = [
        (int(r["lo"]), int(r["hi"]), int(r["charge"])) for r in rows
        if r.get("layer") == layer and r.get("band") == band and int(r["hi"]) > int(r["lo"])
    ]
    if own:
        return sorted(own)
    return sorted(
        (int(r["lo"]), int(r["hi"]), int(r["charge"])) for r in rows
        if r.get("layer") == layer and r.get("band") == "all" and int(r["hi"]) > int(r["lo"])
    )


def covered_assets(assets: set[int], spans: list[tuple[int, int, int]]) -> dict[int, int]:
    """Charge per covered asset. An asset inside several spans of the same layer is
    charged the MAXIMUM of their charges, not their sum (SR-2250)."""
    charged: dict[int, int] = {}
    for asset in assets:
        best = None
        for lo, hi, charge in spans:
            if lo <= asset < hi and (best is None or charge > best):
                best = charge
        if best is not None:
            charged[asset] = best
    return charged


def containment_window_checksum(rows: list[dict]) -> str:
    """Windows serialized layer-major, then band, then lo, then hi."""
    ordered = sorted(
        rows, key=lambda r: (str(r.get("layer")), str(r.get("band")), int(r["lo"]), int(r["hi"]), int(r["charge"]))
    )
    lines = [f"{r['layer']}|{r['band']}|{r['lo']}|{r['hi']}|{r['charge']}" for r in ordered]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def load_policies(path: Path = POLICY_PATH) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_policy(raw: object) -> dict:
    """Start from the shipped baseline and overlay any field the object supplies."""
    resolved = dict(DEFAULT_POLICY)
    if isinstance(raw, dict):
        for key in POLICY_FIELDS:
            if key in raw:
                resolved[key] = int(raw[key])
    return resolved


def policy_for_band(band: str, policy_data: dict) -> dict:
    """Resolve a band's policy: baseline, then file default, then that band's override.

    A sparse override supplies only the fields it names; every unlisted field is
    inherited, so an override is never a complete policy on its own.
    """
    base = _normalize_policy(policy_data.get("default", {}))
    overrides = policy_data.get("band_overrides", {})
    if not isinstance(overrides, dict):
        return base
    raw = overrides.get(band)
    if not isinstance(raw, dict):
        return base
    merged = dict(base)
    for key in POLICY_FIELDS:
        if key in raw:
            merged[key] = int(raw[key])
    return merged


def policy_checksum(policy_data: dict) -> str:
    """Resolved default, then each band in the fixed order low, mid, high."""
    lines = ["default|" + "|".join(
        str(_normalize_policy(policy_data.get("default", {}))[k]) for k in POLICY_FIELDS)]
    for band in ("low", "mid", "high"):
        resolved = policy_for_band(band, policy_data)
        lines.append(f"{band}|" + "|".join(str(resolved[k]) for k in POLICY_FIELDS))
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def canonical_bundles(bundle_rows: list[dict]) -> list[dict]:
    """Normalize bundles: drop severities outside 1..9 or empty asset lists;
    for a repeated bundle id keep the one with the LOWER severity per SR-2243; assets are
    deduplicated and sorted. Result is sorted by bundle id."""
    by_id: dict[str, dict] = {}
    for row in bundle_rows:
        bid = str(row["id"])
        sev = int(row["severity"])
        assets = sorted({int(a) for a in row["assets"]})
        if sev < SEVERITY_MIN or sev > SEVERITY_MAX or not assets:
            continue
        cur = by_id.get(bid)
        # SR-2243 reverses this: for a repeated id the LOWER severity is kept.
        if cur is None or sev < cur["severity"]:
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
    # suffix[i] = sum of severities of items[i:], an upper bound on the value still
    # reachable from index i (it ignores asset conflicts, so it never underestimates).
    suffix = [0] * (len(items) + 1)
    for i in range(len(items) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + items[i][0]
    best_total = 0
    best_ids: tuple[str, ...] = ()

    def rec(index: int, used: frozenset[int], total: int, chosen: list[str]) -> None:
        nonlocal best_total, best_ids
        # Prune only branches that provably cannot reach the current best value.
        # A branch with total + suffix[index] == best_total is kept, because it may
        # still tie the best value with a lexicographically smaller id set.
        if total + suffix[index] < best_total:
            return
        if index >= len(items):
            key = tuple(sorted(chosen))
            if total > best_total or (total == best_total and key < best_ids):
                best_total = total
                best_ids = key
            return
        # Explore the take-branch first so a high value is found early and prunes more.
        severity, assets, bid = items[index]
        if not (assets & used):
            rec(index + 1, used | assets, total + severity, chosen + [bid])
        rec(index + 1, used, total, chosen)

    rec(0, frozenset(), 0, [])
    return best_total, list(best_ids)


def plan_remediation(asset_count: int, bundle_rows: list[dict],
                     policy_data: dict | None = None,
                     containment_rows: list[dict] | None = None) -> dict:
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
    # SR-2248: the urgency threshold and carry cap are resolved PER BUNDLE from
    # its severity band's policy, not taken from a single global constant.
    policy_data = policy_data or {}
    containment_rows = containment_rows or []
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
        pol = policy_for_band(severity_band(b["severity"]), policy_data)
        carry_out = min(carry_in + pressure - (len(assets) // 2), pol["carry_cap"])
        if urgency >= pol["urgency_threshold"]:
            critical_response_ids.append(b["id"])
        max_urgency = max(max_urgency, urgency)
        ledger_rows.append(f"{b['id']}|{urgency}|{1 if urgency >= pol["urgency_threshold"] else 0}|{carry_out}")
        per_bundle[b["id"]] = {
            "urgency": urgency,
            "urgency_carry_out": carry_out,
            "critical_response": 1 if urgency >= pol["urgency_threshold"] else 0,
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
    TIER_WAVE_CAP = 2
    RESPONSE_TIERS = ("immediate", "urgent", "routine")
    CLASS_RANK = {n: len(RESPONSE_TIERS) - i for i, n in enumerate(RESPONSE_TIERS)}
    uncontained_bundles = [b for b in bundles if b["id"] not in contained_set]
    total_exposure_overlap = 0
    total_blackout_overlap = 0
    total_maintenance_overlap = 0
    wave_candidates = []
    for b in bundles:
        if b["id"] not in contained_set:
            continue
        assets = set(b["assets"])
        # SR-2241: an uncontained bundle's shared assets are attributed to ONE
        # contained bundle -- the highest-severity claimant, ties by smallest id.
        exposure_overlap = 0
        for o in uncontained_bundles:
            shared = assets & set(o["assets"])
            if not shared:
                continue
            claimants = [
                c for c in bundles
                if c["id"] in contained_set and set(o["assets"]) & set(c["assets"])
            ]
            owner = sorted(claimants, key=lambda c: (-c["severity"], c["id"]))[0]
            if owner["id"] == b["id"]:
                exposure_overlap += len(shared)
        exposing_bundle_count = sum(1 for o in uncontained_bundles if assets & set(o["assets"]))
        total_exposure_overlap += exposure_overlap
        raw_load = max(b["severity"] * 3 + (-(-exposure_overlap // 2)) - (len(assets) // 2), 0)
        # SR-2250: containment-window attenuation. Each layer's spans are resolved
        # for this bundle's severity band (own scope, else the `all` scope), and the
        # bundle's OWN assets falling inside them are counted. SR-2252: blackout
        # takes precedence where both layers cover the same asset, so an asset in
        # both is charged to blackout only. The blackout half is ROUNDED UP and the
        # maintenance half is FLOORED.
        band = severity_band(b["severity"])
        blackout_hit = covered_assets(
            assets, windows_for_band(containment_rows, "blackout", band)
        )
        maintenance_hit = covered_assets(
            assets, windows_for_band(containment_rows, "maintenance", band)
        )
        maintenance_hit = {a: c for a, c in maintenance_hit.items() if a not in blackout_hit}
        blackout_overlap = sum(blackout_hit.values())
        maintenance_overlap = sum(maintenance_hit.values())
        total_blackout_overlap += blackout_overlap
        total_maintenance_overlap += maintenance_overlap
        response_load = max(
            raw_load - (-(-blackout_overlap // 2)) - (maintenance_overlap // 3), 0
        )
        wave_candidates.append(
            {
                "id": b["id"],
                "severity": b["severity"],
                "n_assets": len(assets),
                "exposure_overlap": exposure_overlap,
                "exposing_bundle_count": exposing_bundle_count,
                "response_load": response_load,
                "raw_load": raw_load,
                "blackout_overlap": blackout_overlap,
                "maintenance_overlap": maintenance_overlap,
            }
        )
    admitted = [
        r for r in wave_candidates
        if r["response_load"] >= policy_for_band(severity_band(r["severity"]), policy_data)["wave_floor"]
    ]
    # Class per SR-2233, clauses in order; the first match fixes the class.
    for r in admitted:
        rp = policy_for_band(severity_band(r["severity"]), policy_data)
        if r["response_load"] >= rp["immediate_min"]:
            r["response_tier"] = "immediate"
        elif r["response_load"] >= rp["urgent_min"] or r["exposure_overlap"] >= rp["urgent_overlap_min"]:
            r["response_tier"] = "urgent"
        else:
            r["response_tier"] = "routine"
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
    # SR-2245: responder capacity cap, applied AFTER the ordering chain above.
    kept_per_tier: dict[str, int] = {}
    capped_wave = []
    for r in ordered_wave:
        taken = kept_per_tier.get(r["response_tier"], 0)
        if taken < TIER_WAVE_CAP:
            capped_wave.append(r)
            kept_per_tier[r["response_tier"]] = taken + 1
    ordered_wave = capped_wave
    admitted = [r for r in admitted if r["id"] in {x["id"] for x in ordered_wave}]
    # Tier counts are taken AFTER the cap, so they describe the wave as dispatched.
    response_tier_counts = {n: 0 for n in RESPONSE_TIERS}
    for r in admitted:
        response_tier_counts[r["response_tier"]] += 1
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
                "total_claim_severity": sum(b["severity"] for b in claims),
                "contention": max(len(claims) - 1, 0),
            }
        )
    asset_records.sort(
        key=lambda r: (-r["contention"], -r["total_claim_severity"], -r["is_locked"], r["asset_id"])
    )
    asset_exposure_checksum = hashlib.sha256(
        "\n".join(
            f"{r['asset_id']}|{r['claiming_bundle_count']}|{r['locked_by']}|"
            f"{r['is_locked']}|{r['max_claim_severity']}|{r['total_claim_severity']}|{r['contention']}"
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
                "response_tier": (
                    wave.get("response_tier", "none")
                    if wave and bid in admitted_ids
                    else "none"
                ),
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
        "total_blackout_overlap": total_blackout_overlap,
        "total_maintenance_overlap": total_maintenance_overlap,
        "containment_window_checksum": containment_window_checksum(containment_rows),
        "policy_checksum": policy_checksum(policy_data),
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
    result = plan_remediation(
        data["asset_count"], data["bundles"], load_policies(), load_containment_windows()
    )
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
