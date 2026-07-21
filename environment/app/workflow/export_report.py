#!/usr/bin/env python3
"""Badge-access containment rollup deployed during the Tideguard incident.

This build is producing an unreliable containment queue. It is the artifact the
response team asked to have investigated and restored.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "flow-quarantine-v2"
CLASS_ORDER = ["core", "service", "user", "guest"]


def load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def export_report(events: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    tier_counts = {name: 0 for name in CLASS_ORDER}
    subnets: set[str] = set()
    for event in events:
        trust_tier = str(event.get("trust_tier", ""))
        if trust_tier in tier_counts:
            tier_counts[trust_tier] += 1
        subnets.add(str(event.get("subnet", "")))

    quarantined = []
    for event in events:
        if event.get("trust_tier") == "core":
            quarantined.append(
                {
                    "flow_id": event["flow_id"],
                    "entered_ms": event["granted_at"] if "granted_at" in event else 0,
                    "trust_tier": event["trust_tier"],
                    "subnet": event["subnet"],
                    "port": event["port"],
                }
            )

    quarantined.sort(key=lambda row: row["entered_ms"])

    summary = {
        "schema_version": SCHEMA_VERSION,
        "raw_flow_count": len(events),
        "unique_flow_ids": len({str(event["flow_id"]) for event in events}),
        "total_flows": len(events),
        "tier_counts": tier_counts,
        "subnets": sorted(subnets),
        "quarantined_count": len(quarantined),
        "blocked_excluded_count": 0,
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output_dir / "subnet_matrix.json").write_text(json.dumps({}, indent=2) + "\n")
    with (output_dir / "quarantined.jsonl").open("w", encoding="utf-8") as handle:
        for row in quarantined:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/flow_events.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()

    events = load_events(Path(args.input))
    export_report(events, Path(args.output_dir))
    print(f"Wrote containment rollup to {args.output_dir}")


if __name__ == "__main__":
    main()
