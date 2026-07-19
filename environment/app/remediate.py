#!/usr/bin/env python3
"""Sentinel-1 remediation-planning computation.

Skeleton only. The input format, canonicalization rules, the asset-disjoint
packing objective (max_contained_severity, which is NOT the total-severity sum
and NOT a greedy selection), and the exact plan.json (and the per-bundle remediation_ledger.jsonl) keys and checksum
serialization are all specified in /app/docs/plan_spec.md. Fill in
`plan_remediation` to compute the plan and record the observables.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def plan_remediation(asset_count: int, bundles: list[dict]) -> dict:
    """Plan the Sentinel-1 remediation and return the result observables.

    See /app/docs/plan_spec.md for canonicalization, the max_contained_severity
    asset-disjoint packing objective (which is NOT the total-severity sum and NOT
    a greedy highest-severity-first selection), the result keys, and the checksum
    serialization.
    """
    raise NotImplementedError(
        "Implement the Sentinel-1 remediation plan defined in /app/docs/plan_spec.md"
    )


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
