#!/usr/bin/env python3
"""Tideguard flow-access containment audit CLI: diagnose and repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

WORKFLOW_PATH = Path("/app/workflow/export_report.py")
FROZEN_PATH = Path("/app/workflow/.export_report.original")
DOSSIER_PATH = Path("/app/incident/flow_review_dossier.md")
SPEC_PATH = Path("/app/docs/report_spec.json")
EVENTS_PATH = Path("/app/data/flow_events.json")

REPAIRED_SOURCE = '#!/usr/bin/env python3\n"""Network-flow quarantine rollup, restored per the Tideguard review decisions."""\n\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nfrom pathlib import Path\n\nSCHEMA_VERSION = "flow-quarantine-v2"\nTIER_ORDER = ["core", "service", "user", "guest"]\nTIER_RANK = {name: len(TIER_ORDER) - idx for idx, name in enumerate(TIER_ORDER)}\nPRIORITY_ORDER = ["critical", "elevated", "routine"]\nPRIORITY_RANK = {name: len(PRIORITY_ORDER) - idx for idx, name in enumerate(PRIORITY_ORDER)}\nPOLICIES_PATH = Path("/app/data/flow_policies.json")\nSTITCH_GAP_MS = 140\nCARRY_CAP_MS = 780\nSUBNET_QUEUE_CAP = 2\nADMISSION_FLOOR = {"core": 150, "service": 190, "user": 240, "guest": 300}\n\n\ndef _norm_text(value: object) -> str:\n    return " ".join(str(value).split())\n\n\ndef _norm_tier(value: object) -> str:\n    text = str(value).strip().lower()\n    return text if text in TIER_RANK else "guest"\n\n\ndef _norm_subnet(value: object) -> str:\n    text = str(value).strip().lower()\n    return text or "unknown"\n\n\ndef _norm_ms(value: object) -> int:\n    try:\n        return int(str(value).strip())\n    except (TypeError, ValueError):\n        return 0\n\n\ndef _norm_blocked(value: object) -> bool:\n    if isinstance(value, bool):\n        return value\n    if isinstance(value, str):\n        return value.strip().lower() in {"true", "1", "yes"}\n    return bool(value)\n\n\ndef load_events(path: Path) -> list[dict]:\n    return json.loads(path.read_text(encoding="utf-8"))\n\n\ndef load_policies(path: Path = POLICIES_PATH) -> list[dict]:\n    if not path.exists():\n        return []\n    return json.loads(path.read_text(encoding="utf-8"))\n\n\ndef canonical_events(rows: list[dict]) -> list[dict]:\n    deduped: dict[str, dict] = {}\n    for row in rows:\n        flow_id = str(row.get("flow_id", "")).strip()\n        if not flow_id:\n            continue\n        candidate = {\n            "flow_id": flow_id,\n            "src_addr": str(row.get("src_addr", "")).strip(),\n            "trust_tier": _norm_tier(row.get("trust_tier", "")),\n            "subnet": _norm_subnet(row.get("subnet", "")),\n            "port": _norm_text(row.get("port", "")),\n            "opened_ms": _norm_ms(row.get("opened_ms", 0)),\n            "closed_ms": _norm_ms(row.get("closed_ms", 0)),\n            "blocked": _norm_blocked(row.get("blocked", False)),\n        }\n        existing = deduped.get(flow_id)\n        if existing is None:\n            deduped[flow_id] = candidate\n            continue\n        if candidate["opened_ms"] > existing["opened_ms"]:\n            deduped[flow_id] = candidate\n            continue\n        if candidate["opened_ms"] < existing["opened_ms"]:\n            continue\n        # TQ-3318 reverses this: on a duplicate tie the LOWER flow class wins.\n        if TIER_RANK[candidate["trust_tier"]] < TIER_RANK[existing["trust_tier"]]:\n            deduped[flow_id] = candidate\n            continue\n        if TIER_RANK[candidate["trust_tier"]] > TIER_RANK[existing["trust_tier"]]:\n            continue\n        if len(candidate["port"]) > len(existing["port"]):\n            deduped[flow_id] = candidate\n            continue\n        if len(candidate["port"]) < len(existing["port"]):\n            continue\n        if candidate["subnet"] > existing["subnet"]:\n            deduped[flow_id] = candidate\n    canonical = list(deduped.values())\n    canonical.sort(key=lambda row: (row["subnet"], row["opened_ms"], row["flow_id"]))\n    return canonical\n\n\ndef _compact(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:\n    merged: list[list[int]] = []\n    for start, end in sorted(spans):\n        if not merged or start > merged[-1][1]:\n            merged.append([start, end])\n        else:\n            merged[-1][1] = max(merged[-1][1], end)\n    return [(s, e) for s, e in merged]\n\n\ndef _overlap(a_start: int, a_end: int, spans: list[tuple[int, int]]) -> list[tuple[int, int]]:\n    out = []\n    for start, end in spans:\n        lo, hi = max(a_start, start), min(a_end, end)\n        if hi > lo:\n            out.append((lo, hi))\n    return out\n\n\ndef policies_for(rows: list[dict], subnet: str, layer: str, trust_tier: str) -> list[tuple[int, int]]:\n    """TQ-3326 scope: a class uses its OWN windows for this layer; only a class with\n    no window of its own falls back to the `all` scope. Own entries do not also\n    inherit `all`."""\n    own = [\n        (_norm_ms(r["start_ms"]), _norm_ms(r["end_ms"])) for r in rows\n        if r.get("layer") == layer and _norm_subnet(r.get("subnet")) == subnet\n        and str(r.get("scope")) == trust_tier and _norm_ms(r["end_ms"]) > _norm_ms(r["start_ms"])\n    ]\n    if own:\n        return _compact(own)\n    return _compact([\n        (_norm_ms(r["start_ms"]), _norm_ms(r["end_ms"])) for r in rows\n        if r.get("layer") == layer and _norm_subnet(r.get("subnet")) == subnet\n        and str(r.get("scope")) == "all" and _norm_ms(r["end_ms"]) > _norm_ms(r["start_ms"])\n    ])\n\n\ndef build_sessions(canonical: list[dict], policies: list[dict]) -> dict[str, list[dict]]:\n    by_subnet: dict[str, list[dict]] = {}\n    for row in canonical:\n        # TQ-3322: blocked flows are excluded from session construction only.\n        if row["blocked"]:\n            continue\n        by_subnet.setdefault(row["subnet"], []).append(row)\n\n    result: dict[str, list[dict]] = {}\n    for subnet, rows in by_subnet.items():\n        rows.sort(key=lambda r: (r["opened_ms"], r["flow_id"]))\n        sessions: list[dict] = []\n        current: dict | None = None\n        for row in rows:\n            end_ms = max(row["closed_ms"], row["opened_ms"])\n            if current is None:\n                current = {\n                    "start_ms": row["opened_ms"], "end_ms": end_ms,\n                    "flow_ids": [row["flow_id"]], "top_tier": row["trust_tier"],\n                }\n                continue\n            # TQ-3320 retuned the stitch gap; sessions merge across it.\n            if row["opened_ms"] <= current["end_ms"] + STITCH_GAP_MS:\n                current["end_ms"] = max(current["end_ms"], end_ms)\n                current["flow_ids"].append(row["flow_id"])\n                if TIER_RANK[row["trust_tier"]] > TIER_RANK[current["top_tier"]]:\n                    current["top_tier"] = row["trust_tier"]\n                continue\n            sessions.append(current)\n            current = {\n                "start_ms": row["opened_ms"], "end_ms": end_ms,\n                "flow_ids": [row["flow_id"]], "top_tier": row["trust_tier"],\n            }\n        if current is not None:\n            sessions.append(current)\n\n        prev_carry_out = 0\n        prev_end: int | None = None\n        built: list[dict] = []\n        for session in sessions:\n            hold = max(session["end_ms"] - session["start_ms"], 0)\n            lock_spans = _compact(_overlap(\n                session["start_ms"], session["end_ms"],\n                policies_for(policies, subnet, "isolation", session["top_tier"])))\n            maint_spans = _compact(_overlap(\n                session["start_ms"], session["end_ms"],\n                policies_for(policies, subnet, "inspection", session["top_tier"])))\n            isolation_overlap = sum(e - s for s, e in lock_spans)\n            inspection_overlap = sum(e - s for s, e in maint_spans)\n            # TQ-3328: isolation wins any instant both layers cover.\n            shared = 0\n            for ls, le in lock_spans:\n                for ms, me in maint_spans:\n                    shared += max(0, min(le, me) - max(ls, ms))\n            inspection_used = max(inspection_overlap - shared, 0)\n            adjusted_hold = max(\n                hold - (-(-isolation_overlap // 2)) - (-(-inspection_used // 3)), 0\n            )\n            idle_gap = 0 if prev_end is None else max(session["start_ms"] - prev_end, 0)\n            carry_in = max(prev_carry_out - (-(-idle_gap // 4)), 0)\n            ledger_hold = adjusted_hold + (-(-carry_in // 5))\n            carry_out = min(\n                carry_in + adjusted_hold + len(session["flow_ids"]) * 6, CARRY_CAP_MS\n            )\n            built.append({\n                "start_ms": session["start_ms"], "end_ms": session["end_ms"],\n                "hold_ms": hold,\n                "isolation_overlap_ms": isolation_overlap,\n                "inspection_overlap_ms": inspection_overlap,\n                "adjusted_hold_ms": adjusted_hold,\n                "idle_gap_ms": idle_gap, "carry_in_ms": carry_in,\n                "carry_out_ms": carry_out, "ledger_hold_ms": ledger_hold,\n                "flow_count": len(session["flow_ids"]),\n                "flow_ids": sorted(session["flow_ids"]),\n                "top_tier": session["top_tier"],\n            })\n            prev_carry_out = carry_out\n            prev_end = session["end_ms"]\n        result[subnet] = built\n    return {subnet: result[subnet] for subnet in sorted(result)}\n\n\ndef build_queue(sessions: dict[str, list[dict]]) -> list[dict]:\n    queue: list[dict] = []\n    for subnet, rows in sessions.items():\n        for row in rows:\n            if row["ledger_hold_ms"] < ADMISSION_FLOOR[row["top_tier"]]:\n                continue\n            if row["ledger_hold_ms"] >= 420 or (\n                row["top_tier"] == "core" and row["isolation_overlap_ms"] > 0\n            ):\n                priority = "critical"\n            elif row["ledger_hold_ms"] >= 300 or row["flow_count"] >= 3:\n                priority = "elevated"\n            else:\n                priority = "routine"\n            payload = (\n                f"{subnet}|{row[\'start_ms\']}|{row[\'end_ms\']}|{\',\'.join(row[\'flow_ids\'])}"\n                f"|{row[\'top_tier\']}|{row[\'ledger_hold_ms\']}"\n            )\n            queue.append({\n                "case_id": f"{subnet}:{row[\'start_ms\']}-{row[\'end_ms\']}",\n                "subnet": subnet, "start_ms": row["start_ms"], "end_ms": row["end_ms"],\n                "top_tier": row["top_tier"], "priority": priority,\n                "hold_ms": row["hold_ms"], "adjusted_hold_ms": row["adjusted_hold_ms"],\n                "ledger_hold_ms": row["ledger_hold_ms"],\n                "isolation_overlap_ms": row["isolation_overlap_ms"],\n                "inspection_overlap_ms": row["inspection_overlap_ms"],\n                "carry_in_ms": row["carry_in_ms"], "carry_out_ms": row["carry_out_ms"],\n                "flow_count": row["flow_count"], "flow_ids": row["flow_ids"],\n                "hold_digest": hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12],\n            })\n    queue.sort(key=lambda r: (\n        -PRIORITY_RANK[r["priority"]], -r["ledger_hold_ms"], -r["hold_ms"],\n        -r["flow_count"], r["subnet"], r["start_ms"],\n    ))\n    # TQ-3330: responder capacity cap, applied AFTER the ordering chain above.\n    kept: dict[str, int] = {}\n    capped: list[dict] = []\n    for row in queue:\n        taken = kept.get(row["subnet"], 0)\n        if taken >= SUBNET_QUEUE_CAP:\n            continue\n        kept[row["subnet"]] = taken + 1\n        capped.append(row)\n    return capped\n\n\ndef export_report(events: list[dict], output_dir: Path, policies: list[dict]) -> dict:\n    output_dir.mkdir(parents=True, exist_ok=True)\n    canonical = canonical_events(events)\n    sessions = build_sessions(canonical, policies)\n    queue = build_queue(sessions)\n\n    tier_counts = {name: 0 for name in TIER_ORDER}\n    for row in canonical:\n        tier_counts[row["trust_tier"]] += 1\n\n    all_rows = [r for rows in sessions.values() for r in rows]\n    matrix = {\n        subnet: {\n            "session_count": len(rows),\n            "total_hold_ms": sum(r["hold_ms"] for r in rows),\n            "total_ledger_hold_ms": sum(r["ledger_hold_ms"] for r in rows),\n            "max_carry_out_ms": max((r["carry_out_ms"] for r in rows), default=0),\n            "queued_count": sum(1 for r in queue if r["subnet"] == subnet),\n        }\n        for subnet, rows in sessions.items()\n    }\n\n    canonical_payload = "\\n".join(\n        f"{r[\'flow_id\']}|{r[\'src_addr\']}|{r[\'trust_tier\']}|{r[\'subnet\']}|{r[\'opened_ms\']}"\n        f"|{r[\'closed_ms\']}|{1 if r[\'blocked\'] else 0}" for r in canonical\n    )\n    control_payload = "\\n".join(\n        f"{r[\'layer\']}|{r[\'scope\']}|{_norm_subnet(r[\'subnet\'])}|{_norm_ms(r[\'start_ms\'])}|{_norm_ms(r[\'end_ms\'])}"\n        for r in sorted(policies, key=lambda r: (\n            str(r["layer"]), str(r["scope"]), _norm_subnet(r["subnet"]), _norm_ms(r["start_ms"])))\n    )\n    queue_payload = "\\n".join(\n        f"{r[\'case_id\']}|{r[\'priority\']}|{r[\'ledger_hold_ms\']}|{r[\'hold_digest\']}" for r in queue\n    )\n\n    summary = {\n        "schema_version": SCHEMA_VERSION,\n        "raw_flow_count": len(events),\n        "unique_flow_ids": len({str(e.get("flow_id", "")).strip() for e in events if str(e.get("flow_id", "")).strip()}),\n        "canonical_flow_count": len(canonical),\n        "tier_counts": tier_counts,\n        "subnets": sorted(sessions),\n        "subnet_count": len(sessions),\n        "blocked_excluded_count": sum(1 for r in canonical if r["blocked"]),\n        "session_count": len(all_rows),\n        "total_hold_ms": sum(r["hold_ms"] for r in all_rows),\n        "total_adjusted_hold_ms": sum(r["adjusted_hold_ms"] for r in all_rows),\n        "total_ledger_hold_ms": sum(r["ledger_hold_ms"] for r in all_rows),\n        "total_isolation_overlap_ms": sum(r["isolation_overlap_ms"] for r in all_rows),\n        "total_inspection_overlap_ms": sum(r["inspection_overlap_ms"] for r in all_rows),\n        "max_ledger_hold_ms": max((r["ledger_hold_ms"] for r in all_rows), default=0),\n        "max_carry_out_ms": max((r["carry_out_ms"] for r in all_rows), default=0),\n        "longest_session_ms": max((r["hold_ms"] for r in all_rows), default=0),\n        "quarantined_count": len(queue),\n        "priority_counts": {\n            name: sum(1 for r in queue if r["priority"] == name) for name in PRIORITY_ORDER\n        },\n        "canonical_flow_checksum": hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest(),\n        "flow_policy_checksum": hashlib.sha256(control_payload.encode("utf-8")).hexdigest(),\n        "quarantine_checksum": hashlib.sha256(queue_payload.encode("utf-8")).hexdigest(),\n    }\n\n    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\\n", encoding="utf-8")\n    (output_dir / "subnet_matrix.json").write_text(json.dumps(matrix, indent=2) + "\\n", encoding="utf-8")\n    with (output_dir / "quarantined.jsonl").open("w", encoding="utf-8") as handle:\n        for row in queue:\n            handle.write(json.dumps(row, separators=(",", ":")) + "\\n")\n    return summary\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser()\n    parser.add_argument("--input", default="/app/data/flow_events.json")\n    parser.add_argument("--output-dir", default="/app/output")\n    args = parser.parse_args()\n\n    events = load_events(Path(args.input))\n    export_report(events, Path(args.output_dir), load_policies())\n    print(f"Wrote containment rollup to {args.output_dir}")\n\n\nif __name__ == "__main__":\n    main()\n'


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def load_events(path: Path = EVENTS_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_stats(events: list[dict]) -> dict:
    ids = [str(e.get("flow_id", "")).strip() for e in events]
    present = [i for i in ids if i]
    return {
        "raw_flow_count": len(events),
        "unique_flow_ids": len(set(present)),
        "duplicate_flow_ids": len(present) - len(set(present)),
        "blocked_row_count": sum(
            1 for e in events
            if (e.get("blocked") is True)
            or (isinstance(e.get("blocked"), str) and e["blocked"].strip().lower() in {"true", "1", "yes"})
        ),
    }


def frozen_audit() -> dict:
    raw = FROZEN_PATH.read_bytes()
    return {
        "frozen_sha256": hashlib.sha256(raw).hexdigest(),
        "frozen_byte_count": len(raw),
    }


def _line_has_all(line: str, terms: list[str]) -> bool:
    low = line.lower()
    return all(t.lower() in low for t in terms)


def find_dossier_quote(text: str, terms: list[str]) -> str:
    """First line of the dossier containing every term, returned VERBATIM."""
    for line in text.splitlines():
        if line.strip() and _line_has_all(line, terms):
            return line.strip()
    raise SystemExit(f"no dossier line matches {terms}")


def find_pipeline_evidence(source: str, terms: list[str]) -> str:
    """First line of the FROZEN workflow containing every term, VERBATIM."""
    for line in source.splitlines():
        if line.strip() and _line_has_all(line, terms):
            return line.strip()
    raise SystemExit(f"no pipeline line matches {terms}")


def build_issues(dossier: str, frozen: str, spec: dict) -> list[dict]:
    issues = []
    for entry in spec["known_defects"]:
        issues.append({
            "defect_id": entry["defect_id"],
            "stage": entry["stage"],
            "dossier_quote": find_dossier_quote(dossier, entry["dossier_terms"]),
            "pipeline_evidence": find_pipeline_evidence(frozen, entry["pipeline_terms"]),
            "repair_action": entry["repair_action"],
        })
    issues.sort(key=lambda row: row["defect_id"])
    return issues


def build_diagnosis(dossier: str, frozen: str, spec: dict, events: list[dict]) -> dict:
    issues = build_issues(dossier, frozen, spec)
    payload = "\n".join(
        f"{i['defect_id']}|{i['stage']}|{i['repair_action']}" for i in issues
    )
    return {
        "schema_version": spec["diagnosis_report"]["schema_version"],
        "input_stats": input_stats(events),
        "defect_count": len(issues),
        "defects": issues,
        "diagnosis_checksum": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


def patch_workflow() -> None:
    """Write the repaired pipeline to disk BEFORE it is loaded or run."""
    WORKFLOW_PATH.write_text(REPAIRED_SOURCE, encoding="utf-8")


def cmd_diagnose(dossier_path: Path, report_path: Path) -> None:
    spec = load_spec()
    report = build_diagnosis(
        dossier_path.read_text(encoding="utf-8"),
        FROZEN_PATH.read_text(encoding="utf-8"),
        spec,
        load_events(),
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote diagnosis to {report_path}")


def cmd_repair(output_dir: Path) -> None:
    spec = load_spec()
    before = frozen_audit()
    dossier = DOSSIER_PATH.read_text(encoding="utf-8")
    frozen = FROZEN_PATH.read_text(encoding="utf-8")
    events = load_events()

    patch_workflow()
    output_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, str(WORKFLOW_PATH), "--output-dir", str(output_dir)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"repaired workflow failed: {result.stderr}")

    diagnosis = build_diagnosis(dossier, frozen, spec, events)
    (output_dir / "diagnosis.json").write_text(
        json.dumps(diagnosis, indent=2) + "\n", encoding="utf-8")

    repaired_bytes = WORKFLOW_PATH.read_bytes()
    removed = [t for t in spec["workflow_repair"]["forbidden_tokens"]
               if t not in repaired_bytes.decode("utf-8")]
    audit = {
        "schema_version": spec["repair_audit"]["schema_version"],
        "pre_repair_sha256": before["frozen_sha256"],
        "pre_repair_byte_count": before["frozen_byte_count"],
        "post_repair_sha256": hashlib.sha256(repaired_bytes).hexdigest(),
        "post_repair_byte_count": len(repaired_bytes),
        "defects_repaired": [i["defect_id"] for i in diagnosis["defects"]],
        "forbidden_tokens_removed": sorted(removed),
        "artifacts": sorted(p.name for p in output_dir.iterdir() if p.is_file()),
    }
    audit["artifacts"] = sorted(set(audit["artifacts"]) | {"repair_audit.json"})
    (output_dir / "repair_audit.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(f"Repaired workflow and wrote artifacts to {output_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Tideguard flow-access containment audit")
    sub = parser.add_subparsers(dest="command", required=True)

    diag = sub.add_parser("diagnose")
    diag.add_argument("--dossier", default=str(DOSSIER_PATH))
    diag.add_argument("--report", default="/app/output/diagnosis.json")

    rep = sub.add_parser("repair")
    rep.add_argument("--output-dir", default="/app/output")

    args = parser.parse_args()
    if args.command == "diagnose":
        cmd_diagnose(Path(args.dossier), Path(args.report))
    else:
        cmd_repair(Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
