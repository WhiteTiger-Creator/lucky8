"""Broken Mailguard signal workflow used for repair task."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "identity-triage-v2"


def load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def export_report(events: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    severity_counts = {name: 0 for name in ("critical", "high", "medium", "low")}
    mailboxs: set[str] = set()
    for event in events:
        severity = str(event.get("severity", ""))
        if severity in severity_counts:
            severity_counts[severity] += 1
        mailboxs.add(str(event.get("mailbox", "")))

    signals = []
    for event in events:
        severity = event.get("severity")
        if severity == "critical":
            signals.append(
                {
                    "message_id": event["message_id"],
                    "occurred_ms": event["occurred_at"] if "occurred_at" in event else 0,  # noqa: SIM401
                    "severity": event["severity"],
                    "mailbox": event["mailbox"],
                    "detector": event["detector"],
                }
            )

    signals.sort(key=lambda row: row["occurred_ms"])

    summary = {
        "schema_version": SCHEMA_VERSION,
        "raw_message_count": len(events),
        "unique_message_ids": len({str(event["message_id"]) for event in events}),
        "total_messages": len(events),
        "severity_counts": severity_counts,
        "mailboxs": sorted(mailboxs),
        "escalated_count": len(signals),
        "dismissed_excluded_count": 0,
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output_dir / "mailbox_matrix.json").write_text(json.dumps({}, indent=2) + "\n")
    with (output_dir / "escalated.jsonl").open("w", encoding="utf-8") as handle:
        for row in signals:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/events.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()

    events = load_events(Path(args.input))
    export_report(events, Path(args.output_dir))
    print(f"Wrote report to {args.output_dir}")


if __name__ == "__main__":
    main()
