# Tideguard containment rollup — implementation guide

This guide describes the two commands, the artifacts they must leave behind, and the
evidence rules. It does **not** decide any computed value. Every rule that produces a
number or picks a winner lives in `/app/incident/flow_review_dossier.md`, and where the
board revisited a point the latest dated decision is the one that binds.
`/app/docs/report_spec.json` is the authoritative schema: exact key sets, digest payloads
and checksum serialization. Read it in full — a missing key fails the artifact.

## Commands

    python3 /app/flow_audit.py diagnose --dossier PATH --report PATH
    python3 /app/flow_audit.py repair --output-dir PATH

`diagnose` is **stateless**. It writes a complete report on every explicit call, whatever
state the workflow is in and whether or not a repair has already run. It never depends on
a previous invocation having happened.

`repair` restores `/app/workflow/export_report.py`, runs it, and leaves five artifacts in
the output directory: `summary.json`, `subnet_matrix.json`, `quarantined.jsonl`,
`diagnosis.json` and `repair_audit.json`.

## Evidence rules

Each of the six defects in `report_spec.json` under `known_defects` is reported with:

* `dossier_quote` — a line from the dossier reproduced **verbatim**, character for
  character, with only surrounding whitespace stripped. Not a paraphrase, not a summary,
  not a re-wrapped line.
* `pipeline_evidence` — likewise a verbatim stripped line, taken from the **frozen**
  snapshot `/app/workflow/.export_report.original`, not from the live workflow.
* `repair_action` — the action recorded for that defect in the spec.

Defects are emitted sorted by `defect_id` ascending.

## Repair audit

`repair_audit.json` carries all eight keys of `repair_audit.required_keys` — a file with only
the hash and token fields is incomplete:

* `schema_version` — the literal string fixed by the spec.
* `pre_repair_sha256` and `pre_repair_byte_count` — read from the **frozen** snapshot, so they
  are identical whether or not a repair already ran. The frozen file is read-only and must
  never be modified.
* `post_repair_sha256` and `post_repair_byte_count` — describe the restored workflow on disk
  after the repair.
* `defects_repaired` — the array of repaired defect id strings, sorted ascending. It is a list
  of ids, not a count.
* `forbidden_tokens_removed` — which of the spec's `forbidden_tokens` are absent from the
  restored source, sorted.
* `artifacts` — the sorted array of artifact file names written by the repair.

Their exact types are given in the spec's `repair_audit.required_keys_annotated`.

## Order of operations

The repaired workflow must be written to disk **before** it is loaded or executed, so a
single `repair` invocation produces artifacts from the restored code rather than from the
build that was on disk when the command started. A repair that runs the old module and
patches afterwards will disagree with a rerun.

## Processing stages

The rollup proceeds in this order. What each stage *does* is governed by the dossier.

1. **Canonicalization** — normalize flow class, subnet, port, timestamps and the blocked
   flag; drop rows with no flow id.
2. **Deduplication** — collapse repeated `flow_id` rows. This happens before any count,
   aggregate or checksum is computed.
3. **Session construction** — group canonical rows by subnet and merge them into occupancy
   sessions across the stitch gap.
4. **Control-window attenuation** — resolve each layer's windows for the session's class,
   measure the overlap, and reduce the hold.
5. **Occupancy ledger** — carry propagates between consecutive sessions in a subnet and
   decays across the idle gap.
6. **Containment admission, priority and ordering** — admit by the per-class floor, assign
   a priority tier, order the queue, then apply the responder capacity cap.
7. **Aggregation and checksums** — per-subnet matrix, summary totals, digests.

## Generalization

The repaired rollup is graded on behaviour. It must accept an alternate flow stream via
`--input`, produce identical output on reruns, and derive every value from the operational
inputs and the governing decisions. Nothing is read or imported from external grading resources. No particular identifiers, helper names or code structure are required.
