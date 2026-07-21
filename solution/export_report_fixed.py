#!/usr/bin/env python3
"""Network-flow quarantine rollup, restored per the Tideguard review decisions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCHEMA_VERSION = "flow-quarantine-v2"
TIER_ORDER = ["core", "service", "user", "guest"]
TIER_RANK = {name: len(TIER_ORDER) - idx for idx, name in enumerate(TIER_ORDER)}
PRIORITY_ORDER = ["critical", "elevated", "routine"]
PRIORITY_RANK = {name: len(PRIORITY_ORDER) - idx for idx, name in enumerate(PRIORITY_ORDER)}
POLICIES_PATH = Path("/app/data/flow_policies.json")
STITCH_GAP_MS = 140
CARRY_CAP_MS = 780
SUBNET_QUEUE_CAP = 2
ADMISSION_FLOOR = {"core": 150, "service": 190, "user": 240, "guest": 300}


def _norm_text(value: object) -> str:
    return " ".join(str(value).split())


def _norm_tier(value: object) -> str:
    text = str(value).strip().lower()
    return text if text in TIER_RANK else "guest"


def _norm_subnet(value: object) -> str:
    text = str(value).strip().lower()
    return text or "unknown"


def _norm_ms(value: object) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def _norm_blocked(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def load_events(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_policies(path: Path = POLICIES_PATH) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_events(rows: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for row in rows:
        flow_id = str(row.get("flow_id", "")).strip()
        if not flow_id:
            continue
        candidate = {
            "flow_id": flow_id,
            "src_addr": str(row.get("src_addr", "")).strip(),
            "trust_tier": _norm_tier(row.get("trust_tier", "")),
            "subnet": _norm_subnet(row.get("subnet", "")),
            "port": _norm_text(row.get("port", "")),
            "opened_ms": _norm_ms(row.get("opened_ms", 0)),
            "closed_ms": _norm_ms(row.get("closed_ms", 0)),
            "blocked": _norm_blocked(row.get("blocked", False)),
        }
        existing = deduped.get(flow_id)
        if existing is None:
            deduped[flow_id] = candidate
            continue
        if candidate["opened_ms"] > existing["opened_ms"]:
            deduped[flow_id] = candidate
            continue
        if candidate["opened_ms"] < existing["opened_ms"]:
            continue
        # TQ-3318 reverses this: on a duplicate tie the LOWER flow class wins.
        if TIER_RANK[candidate["trust_tier"]] < TIER_RANK[existing["trust_tier"]]:
            deduped[flow_id] = candidate
            continue
        if TIER_RANK[candidate["trust_tier"]] > TIER_RANK[existing["trust_tier"]]:
            continue
        if len(candidate["port"]) > len(existing["port"]):
            deduped[flow_id] = candidate
            continue
        if len(candidate["port"]) < len(existing["port"]):
            continue
        if candidate["subnet"] > existing["subnet"]:
            deduped[flow_id] = candidate
    canonical = list(deduped.values())
    canonical.sort(key=lambda row: (row["subnet"], row["opened_ms"], row["flow_id"]))
    return canonical


def _compact(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[list[int]] = []
    for start, end in sorted(spans):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return [(s, e) for s, e in merged]


def _overlap(a_start: int, a_end: int, spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out = []
    for start, end in spans:
        lo, hi = max(a_start, start), min(a_end, end)
        if hi > lo:
            out.append((lo, hi))
    return out


def policies_for(rows: list[dict], subnet: str, layer: str, trust_tier: str) -> list[tuple[int, int]]:
    """TQ-3326 scope: a class uses its OWN windows for this layer; only a class with
    no window of its own falls back to the `all` scope. Own entries do not also
    inherit `all`."""
    own = [
        (_norm_ms(r["start_ms"]), _norm_ms(r["end_ms"])) for r in rows
        if r.get("layer") == layer and _norm_subnet(r.get("subnet")) == subnet
        and str(r.get("scope")) == trust_tier and _norm_ms(r["end_ms"]) > _norm_ms(r["start_ms"])
    ]
    if own:
        return _compact(own)
    return _compact([
        (_norm_ms(r["start_ms"]), _norm_ms(r["end_ms"])) for r in rows
        if r.get("layer") == layer and _norm_subnet(r.get("subnet")) == subnet
        and str(r.get("scope")) == "all" and _norm_ms(r["end_ms"]) > _norm_ms(r["start_ms"])
    ])


def build_sessions(canonical: list[dict], policies: list[dict]) -> dict[str, list[dict]]:
    by_subnet: dict[str, list[dict]] = {}
    for row in canonical:
        # TQ-3322: blocked flows are excluded from session construction only.
        if row["blocked"]:
            continue
        by_subnet.setdefault(row["subnet"], []).append(row)

    result: dict[str, list[dict]] = {}
    for subnet, rows in by_subnet.items():
        rows.sort(key=lambda r: (r["opened_ms"], r["flow_id"]))
        sessions: list[dict] = []
        current: dict | None = None
        for row in rows:
            end_ms = max(row["closed_ms"], row["opened_ms"])
            if current is None:
                current = {
                    "start_ms": row["opened_ms"], "end_ms": end_ms,
                    "flow_ids": [row["flow_id"]], "top_tier": row["trust_tier"],
                }
                continue
            # TQ-3320 retuned the stitch gap; sessions merge across it.
            if row["opened_ms"] <= current["end_ms"] + STITCH_GAP_MS:
                current["end_ms"] = max(current["end_ms"], end_ms)
                current["flow_ids"].append(row["flow_id"])
                if TIER_RANK[row["trust_tier"]] > TIER_RANK[current["top_tier"]]:
                    current["top_tier"] = row["trust_tier"]
                continue
            sessions.append(current)
            current = {
                "start_ms": row["opened_ms"], "end_ms": end_ms,
                "flow_ids": [row["flow_id"]], "top_tier": row["trust_tier"],
            }
        if current is not None:
            sessions.append(current)

        prev_carry_out = 0
        prev_end: int | None = None
        built: list[dict] = []
        for session in sessions:
            hold = max(session["end_ms"] - session["start_ms"], 0)
            lock_spans = _compact(_overlap(
                session["start_ms"], session["end_ms"],
                policies_for(policies, subnet, "isolation", session["top_tier"])))
            maint_spans = _compact(_overlap(
                session["start_ms"], session["end_ms"],
                policies_for(policies, subnet, "inspection", session["top_tier"])))
            isolation_overlap = sum(e - s for s, e in lock_spans)
            inspection_overlap = sum(e - s for s, e in maint_spans)
            # TQ-3328: isolation wins any instant both layers cover.
            shared = 0
            for ls, le in lock_spans:
                for ms, me in maint_spans:
                    shared += max(0, min(le, me) - max(ls, ms))
            inspection_used = max(inspection_overlap - shared, 0)
            adjusted_hold = max(
                hold - (-(-isolation_overlap // 2)) - (inspection_used // 3), 0
            )
            idle_gap = 0 if prev_end is None else max(session["start_ms"] - prev_end, 0)
            carry_in = max(prev_carry_out - (-(-idle_gap // 4)), 0)
            ledger_hold = adjusted_hold + (carry_in // 5)
            carry_out = min(
                carry_in + adjusted_hold + len(session["flow_ids"]) * 6, CARRY_CAP_MS
            )
            built.append({
                "start_ms": session["start_ms"], "end_ms": session["end_ms"],
                "hold_ms": hold,
                "isolation_overlap_ms": isolation_overlap,
                "inspection_overlap_ms": inspection_overlap,
                "adjusted_hold_ms": adjusted_hold,
                "idle_gap_ms": idle_gap, "carry_in_ms": carry_in,
                "carry_out_ms": carry_out, "ledger_hold_ms": ledger_hold,
                "flow_count": len(session["flow_ids"]),
                "flow_ids": sorted(session["flow_ids"]),
                "top_tier": session["top_tier"],
            })
            prev_carry_out = carry_out
            prev_end = session["end_ms"]
        result[subnet] = built
    return {subnet: result[subnet] for subnet in sorted(result)}


def build_queue(sessions: dict[str, list[dict]]) -> list[dict]:
    queue: list[dict] = []
    for subnet, rows in sessions.items():
        for row in rows:
            if row["ledger_hold_ms"] < ADMISSION_FLOOR[row["top_tier"]]:
                continue
            if row["ledger_hold_ms"] >= 420 or (
                row["top_tier"] == "core" and row["isolation_overlap_ms"] > 0
            ):
                priority = "critical"
            elif row["ledger_hold_ms"] >= 300 or row["flow_count"] >= 3:
                priority = "elevated"
            else:
                priority = "routine"
            payload = (
                f"{subnet}|{row['start_ms']}|{row['end_ms']}|{','.join(row['flow_ids'])}"
                f"|{row['top_tier']}|{row['ledger_hold_ms']}"
            )
            queue.append({
                "case_id": f"{subnet}:{row['start_ms']}-{row['end_ms']}",
                "subnet": subnet, "start_ms": row["start_ms"], "end_ms": row["end_ms"],
                "top_tier": row["top_tier"], "priority": priority,
                "hold_ms": row["hold_ms"], "adjusted_hold_ms": row["adjusted_hold_ms"],
                "ledger_hold_ms": row["ledger_hold_ms"],
                "isolation_overlap_ms": row["isolation_overlap_ms"],
                "inspection_overlap_ms": row["inspection_overlap_ms"],
                "carry_in_ms": row["carry_in_ms"], "carry_out_ms": row["carry_out_ms"],
                "flow_count": row["flow_count"], "flow_ids": row["flow_ids"],
                "hold_digest": hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12],
            })
    queue.sort(key=lambda r: (
        -PRIORITY_RANK[r["priority"]], -r["ledger_hold_ms"], -r["hold_ms"],
        -r["flow_count"], r["subnet"], r["start_ms"],
    ))
    # TQ-3330: responder capacity cap, applied AFTER the ordering chain above.
    kept: dict[str, int] = {}
    capped: list[dict] = []
    for row in queue:
        taken = kept.get(row["subnet"], 0)
        if taken >= SUBNET_QUEUE_CAP:
            continue
        kept[row["subnet"]] = taken + 1
        capped.append(row)
    return capped


def export_report(events: list[dict], output_dir: Path, policies: list[dict]) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    canonical = canonical_events(events)
    sessions = build_sessions(canonical, policies)
    queue = build_queue(sessions)

    tier_counts = {name: 0 for name in TIER_ORDER}
    for row in canonical:
        tier_counts[row["trust_tier"]] += 1

    all_rows = [r for rows in sessions.values() for r in rows]
    matrix = {
        subnet: {
            "session_count": len(rows),
            "total_hold_ms": sum(r["hold_ms"] for r in rows),
            "total_ledger_hold_ms": sum(r["ledger_hold_ms"] for r in rows),
            "max_carry_out_ms": max((r["carry_out_ms"] for r in rows), default=0),
            "queued_count": sum(1 for r in queue if r["subnet"] == subnet),
        }
        for subnet, rows in sessions.items()
    }

    canonical_payload = "\n".join(
        f"{r['flow_id']}|{r['src_addr']}|{r['trust_tier']}|{r['subnet']}|{r['opened_ms']}"
        f"|{r['closed_ms']}|{1 if r['blocked'] else 0}" for r in canonical
    )
    control_payload = "\n".join(
        f"{r['layer']}|{r['scope']}|{_norm_subnet(r['subnet'])}|{_norm_ms(r['start_ms'])}|{_norm_ms(r['end_ms'])}"
        for r in sorted(policies, key=lambda r: (
            str(r["layer"]), str(r["scope"]), _norm_subnet(r["subnet"]), _norm_ms(r["start_ms"])))
    )
    queue_payload = "\n".join(
        f"{r['case_id']}|{r['priority']}|{r['ledger_hold_ms']}|{r['hold_digest']}" for r in queue
    )

    summary = {
        "schema_version": SCHEMA_VERSION,
        "raw_flow_count": len(events),
        "unique_flow_ids": len({str(e.get("flow_id", "")).strip() for e in events if str(e.get("flow_id", "")).strip()}),
        "canonical_flow_count": len(canonical),
        "tier_counts": tier_counts,
        "subnets": sorted(sessions),
        "subnet_count": len(sessions),
        "blocked_excluded_count": sum(1 for r in canonical if r["blocked"]),
        "session_count": len(all_rows),
        "total_hold_ms": sum(r["hold_ms"] for r in all_rows),
        "total_adjusted_hold_ms": sum(r["adjusted_hold_ms"] for r in all_rows),
        "total_ledger_hold_ms": sum(r["ledger_hold_ms"] for r in all_rows),
        "total_isolation_overlap_ms": sum(r["isolation_overlap_ms"] for r in all_rows),
        "total_inspection_overlap_ms": sum(r["inspection_overlap_ms"] for r in all_rows),
        "max_ledger_hold_ms": max((r["ledger_hold_ms"] for r in all_rows), default=0),
        "max_carry_out_ms": max((r["carry_out_ms"] for r in all_rows), default=0),
        "longest_session_ms": max((r["hold_ms"] for r in all_rows), default=0),
        "quarantined_count": len(queue),
        "priority_counts": {
            name: sum(1 for r in queue if r["priority"] == name) for name in PRIORITY_ORDER
        },
        "canonical_flow_checksum": hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest(),
        "flow_policy_checksum": hashlib.sha256(control_payload.encode("utf-8")).hexdigest(),
        "quarantine_checksum": hashlib.sha256(queue_payload.encode("utf-8")).hexdigest(),
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "subnet_matrix.json").write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "quarantined.jsonl").open("w", encoding="utf-8") as handle:
        for row in queue:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/flow_events.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()

    events = load_events(Path(args.input))
    export_report(events, Path(args.output_dir), load_policies())
    print(f"Wrote containment rollup to {args.output_dir}")


if __name__ == "__main__":
    main()
