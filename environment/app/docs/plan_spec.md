# Sentinel-1 remediation-planning — output contract

This document is the **output contract only**: it fixes the input shape, the
exact `plan.json` key set, and the byte-level checksum serialization. It does
**not** define how the values are derived. Bundle canonicalization and its
validity bounds, the containment objective, the tie-broken selected set, and the
residual packing are settled in `/app/incident/remediation_review_log.md`;
reconcile the governing (latest) decision for each rule there.

## Input

The input (`/app/data/remediation.json`) has the shape:

```json
{ "asset_count": M, "bundles": [ {"id": "...", "severity": w, "assets": [a, ...]}, ... ] }
```

Assets are integers `0 .. M-1`. Each bundle has a string `id`, an integer
`severity`, and a list of the asset ids it locks. How the bundle list is
canonicalized (validity bounds, duplicate-id handling, asset dedup/sort, and
ordering) is governed by the review log, not by this contract.

## Output

Write `plan.json` to the output directory (`/app/output` by default) with
exactly these keys. What each derived value **means** is fixed by the review
log; this contract fixes only the key set and the serializations below.

* `asset_count` — copied from the input.
* `bundle_count` — the number of canonical bundles.
* `total_proposed_severity` — the sum of all canonical bundle severities.
* `max_single_bundle_severity` — the largest single canonical bundle severity
  (0 if none).
* `max_contained_severity` — the containment objective (see the review log).
* `contained_bundle_ids` — the tie-broken contained set's bundle ids, ascending
  (selection and tie-break rule per the review log).
* `contained_bundle_count` — the number of ids in `contained_bundle_ids`.
* `contained_asset_count` — the number of distinct assets locked by the
  contained set.
* `uncontained_severity` — `total_proposed_severity - max_contained_severity`.
* `residual_contained_severity` — the residual packing value (see the review log).
* `proposed_tier_counts` — a JSON object `{"critical": n, "major": n, "minor": n}`
  counting canonical bundles per severity tier (tier cutoffs per the review log).
* `contained_tier_counts` — the same object shape over the contained set only.
* `total_asset_pressure` — sum of per-bundle asset pressure over canonical bundles
  (asset-pressure definition per the review log).
* `max_asset_pressure` — the largest single per-bundle asset pressure (0 if none).
* `containment_score` — the floored weighted score over the contained set (per log).
* `coverage_permille` — the coverage measure over `asset_count` (per log).
* `residual_pressure` — the asset-pressure sum over the log-defined complement.
* `critical_response_ids` — the ids (ascending) admitted to the critical response
  set by the sequential response-urgency ledger (definition per the review log).
* `critical_response_count` — the number of ids in `critical_response_ids`.
* `max_urgency` — the maximum per-bundle urgency over all canonical bundles.
* `urgency_ledger_checksum` — the SHA-256 hex digest of the ledger rows serialized
  as follows: for each canonical bundle in `id` order, the line
  `id|urgency|c|carry_out` where `c` is `1` if the bundle is in the critical
  response set else `0`; lines joined by a single `\n`, no trailing newline; hash
  the UTF-8 encoding. (The urgency, critical flag and carry_out are defined by the
  review log's response-urgency ledger decision.)
* `total_conflict_load` — the summed conflict load over the contained set (per log).
* `scheduled_bundle_ids` — a JSON **array** of the scheduled bundles' ids, sorted
  ascending (which bundles are scheduled is governed by the review log).
* `scheduled_bundle_count` — the number of ids in `scheduled_bundle_ids`.
* `total_scheduled_effort` — the summed effort over the scheduled bundles (per log).
* `max_scheduled_effort` — the largest single scheduled effort, `0` when none are
  scheduled (per log).
* `schedule_class_counts` — a JSON **object** whose keys are exactly the three class
  names `immediate`, `planned`, `deferred`, in that order, mapping to the number of
  scheduled bundles in each class. All three keys are always present, emitting `0`
  for a class with no scheduled bundles. These three lowercase strings are the only
  accepted class labels; which class a bundle earns is governed by the review log.
* `schedule_order` — a JSON **array** of the scheduled bundle ids in the log's
  scheduling order. This is an ordering, **not** sorted ascending; contrast
  `scheduled_bundle_ids`, which is the sorted one.
* `schedule_checksum` — the SHA-256 hex digest of one line per scheduled bundle in
  `schedule_order` order, each `id|schedule_class|effort|conflict_assets`, lines
  joined by a single newline with no trailing newline, hashed over the UTF-8
  encoding (each value per the log).
* `bundle_checksum` — the SHA-256 hex digest of the canonical bundles serialized
  as follows: for each bundle in `id` order, the line `id|severity|a0,a1,...`
  (assets ascending, comma-joined); lines joined by a single `\n`, no trailing
  newline; hash the UTF-8 encoding.
* `plan_checksum` — the SHA-256 hex digest of the UTF-8 encoding of
  `asset_count|total_proposed_severity|max_single_bundle_severity|max_contained_severity|contained_asset_count|residual_contained_severity|total_asset_pressure|max_asset_pressure|containment_score|coverage_permille|residual_pressure|PC|CC|CRC|MU|CRI|id0,id1,...`
  where `PC` is `proposed_tier_counts` as `critical,major,minor`, `CC` is
  `contained_tier_counts` as `critical,major,minor`, `CRC` is
  `critical_response_count`, `MU` is `max_urgency`, `CRI` is
  `critical_response_ids` comma-joined ascending, and the trailing segment is
  `contained_bundle_ids` comma-joined in ascending order.

The program reads its input from `--input` (default `/app/data/remediation.json`)
and writes to `--output-dir` (default `/app/output`).
