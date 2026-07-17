#!/usr/bin/env python3
"""Reference implementation of the Sentinel-1 remediation-planning model.

Given a set of proposed remediation bundles that each lock a set of shared
assets, select the maximum-total-severity set of bundles that are pairwise
asset-disjoint, and report the contained severity along with integrity
checksums. See /app/docs/plan_spec.md for the authoritative contract. The
contained severity is NOT the sum of all bundle severities (bundles compete for
assets) and NOT a greedy highest-severity-first selection (greedy is not
optimal) — it is the exact maximum-weight asset-disjoint packing.
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


def _max_contained(bundles: list[dict]) -> int:
    """Maximum total severity of a set of pairwise asset-disjoint bundles."""
    items = [(b["severity"], frozenset(b["assets"])) for b in bundles]
    items.sort(key=lambda it: -it[0])
    best = 0

    def rec(index: int, used: frozenset[int], total: int) -> None:
        nonlocal best
        if total > best:
            best = total
        if index >= len(items):
            return
        rec(index + 1, used, total)
        severity, assets = items[index]
        if not (assets & used):
            rec(index + 1, used | assets, total + severity)

    rec(0, frozenset(), 0)
    return best


def plan_remediation(asset_count: int, bundle_rows: list[dict]) -> dict:
    bundles = canonical_bundles(bundle_rows)

    total_proposed_severity = sum(b["severity"] for b in bundles)
    max_single_bundle_severity = max((b["severity"] for b in bundles), default=0)
    max_contained_severity = _max_contained(bundles)

    bundle_payload = "\n".join(
        f"{b['id']}|{b['severity']}|{','.join(str(a) for a in b['assets'])}" for b in bundles
    )
    bundle_checksum = hashlib.sha256(bundle_payload.encode("utf-8")).hexdigest()

    plan_payload = (
        f"{asset_count}|{total_proposed_severity}|"
        f"{max_single_bundle_severity}|{max_contained_severity}"
    )
    plan_checksum = hashlib.sha256(plan_payload.encode("utf-8")).hexdigest()

    return {
        "asset_count": asset_count,
        "bundle_count": len(bundles),
        "total_proposed_severity": total_proposed_severity,
        "max_single_bundle_severity": max_single_bundle_severity,
        "max_contained_severity": max_contained_severity,
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
