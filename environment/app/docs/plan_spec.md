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
* `bundle_checksum` — the SHA-256 hex digest of the canonical bundles serialized
  as follows: for each bundle in `id` order, the line `id|severity|a0,a1,...`
  (assets ascending, comma-joined); lines joined by a single `\n`, no trailing
  newline; hash the UTF-8 encoding.
* `plan_checksum` — the SHA-256 hex digest of the UTF-8 encoding of
  `asset_count|total_proposed_severity|max_single_bundle_severity|max_contained_severity|contained_asset_count|residual_contained_severity|id0,id1,...`
  where the trailing segment is `contained_bundle_ids` comma-joined in ascending
  order.

The program reads its input from `--input` (default `/app/data/remediation.json`)
and writes to `--output-dir` (default `/app/output`).
