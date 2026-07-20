# Sentinel-1 incident containment — output contract

## Required output keys at a glance

Read this section first; the detail for each item follows below.

`plan.json` carries exactly these 32 keys: asset_count, bundle_count,
total_proposed_severity, max_single_bundle_severity, max_contained_severity,
contained_bundle_ids, contained_bundle_count, contained_asset_count,
uncontained_severity, residual_contained_severity, proposed_tier_counts,
contained_tier_counts, total_asset_pressure, max_asset_pressure, containment_score,
coverage_permille, residual_pressure, critical_response_ids, critical_response_count,
max_urgency, urgency_ledger_checksum, asset_exposure_checksum, total_exposure_overlap,
policy_checksum, total_blackout_overlap, total_maintenance_overlap,
containment_window_checksum,
response_wave_ids, response_wave_count, total_response_load, max_response_load,
response_tier_counts, response_order, response_wave_checksum, bundle_checksum,
plan_checksum.

Three files are written to the output directory: `plan.json`,
`remediation_ledger.jsonl` (one row per canonical bundle) and `asset_exposure.jsonl`
(one row per asset id in the estate).

`total_exposure_overlap` counts each contended asset once across the whole plan, not once per
claimant — the attribution rule is in the review log. The response-wave fields describe the wave
after the capacity cap is applied, not before it.

Three flags share similar names and must not be conflated. `contained` means the
bundle is in the containment set. `critical_response` means its urgency reached the
critical threshold, which is independent of containment. `in_response_wave` means it
is a contained bundle that also cleared the wave admission floor. The `c` field in the
urgency-ledger checksum payload is the critical-response flag, not containment.


The Sentinel-1 containment planner turns proposed remediation bundles for compromised
assets into an incident containment plan: the threat severity that can be contained in
one quarantine pass, the bundle set that achieves it, the exposure left uncontained, the
response-urgency ledger, and the responder tiers assigned for the containment pass.

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

Two ordering facts are stated here only so that they are not missed; the keys, directions and tie-breaks themselves stay in the review log. First, the rows of `asset_exposure.jsonl` are NOT in `asset_id` order: they follow a multi-key sort whose governing entry is in the log, and getting that order wrong changes `asset_exposure_checksum` even when every field value is right. Second, duplicate bundle ids are resolved by a severity precedence rule that the log REVERSED from the obvious reading, so the rule you want is the latest dated decision on duplicate-id handling, not the first one you find.

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
* `total_exposure_overlap` — the summed exposure overlap over the contained set (per log).
* `response_wave_ids` — a JSON **array** of the response-wave bundles' ids, sorted
  ascending (which bundles join the response wave is governed by the review log).
* `response_wave_count` — the number of ids in `response_wave_ids`.
* `total_response_load` — the summed response_load over the response-wave bundles (per log).
* `max_response_load` — the largest single response load in the wave, `0` when none are
  in the wave (per log).
* `response_tier_counts` — a JSON **object** whose keys are exactly the three class
  names `immediate`, `urgent`, `routine`, in that order, mapping to the number of
  response-wave bundles in each class. All three keys are always present, emitting `0`
  for a class with no response-wave bundles. These three lowercase strings are the only
  accepted class labels; which class a bundle earns is governed by the review log.
* `response_order` — a JSON **array** of the response-wave bundle ids in the log's
  response order. This is an ordering, **not** sorted ascending; contrast
  `response_wave_ids`, which is the sorted one.
* `response_wave_checksum` — the SHA-256 hex digest of one line per response-wave bundle in
  `response_order` order, each `id|response_tier|response_load|exposure_overlap`, lines
  joined by a single newline with no trailing newline, hashed over the UTF-8
  encoding (each value per the log).
* `bundle_checksum` — the SHA-256 hex digest of the canonical bundles serialized
  as follows: for each bundle in `id` order, the line `id|severity|a0,a1,...`
  (assets ascending, comma-joined); lines joined by a single `\n`, no trailing
  newline; hash the UTF-8 encoding.
### `remediation_ledger.jsonl`

A second artifact written beside `plan.json` in the same output directory: one compact
JSON line per **canonical bundle** (not only the response-wave ones), each carrying
exactly these fourteen keys in this order — `bundle_id`, `severity`, `severity_tier`,
`n_assets`, `asset_pressure`, `contained`, `urgency`, `urgency_carry_out`,
`critical_response`, `exposure_overlap`, `exposing_bundle_count`, `response_load`,
`in_response_wave`, `response_tier`.

`contained`, `critical_response` and `in_response_wave` are integer `0`/`1` flags, not
booleans. `response_tier` is one of `immediate`, `urgent`, `routine`, or the literal
string `none` for a bundle that did not join the wave. The zero-reporting rule keys off
`contained`, not off `in_response_wave`: an **uncontained** bundle reports `0` for
`exposure_overlap`, `exposing_bundle_count` and `response_load`, while a **contained**
bundle that fell below the wave admission floor keeps its computed values for all
three and reports `in_response_wave` as `0`. See the review log for the governing rule. Rows are
serialized with compact separators (no spaces after `,` or `:`) and one row per line. The
row ordering is governed by the review log, not by bundle id.

### `asset_exposure.jsonl`

One compact JSON line per asset id from `0` to `asset_count - 1` inclusive, each with
exactly these eight keys in order — `asset_id`, `claiming_bundle_count`,
`claiming_bundle_ids`, `locked_by`, `is_locked`, `max_claim_severity`,
`total_claim_severity`, `contention`. `total_claim_severity` is the sum of the claiming bundles' raw
`severity` values — it is not a sum of `asset_pressure` and involves no multiplication by asset
count. `max_claim_severity` is the largest of those raw severities.
`claiming_bundle_ids` is a sorted array of
strings, `locked_by` is a bundle id or the literal string `none`, and `is_locked` is an
integer `0`/`1` flag. Assets no bundle claims are still reported. Row ordering and every
derived value are governed by the review log.

* `asset_exposure_checksum` — the SHA-256 hex digest of one line per asset row in the
  emitted order, each `asset_id|claiming_bundle_count|locked_by|is_locked|max_claim_severity|total_claim_severity|contention`,
  joined by a single newline with no trailing newline, hashed over UTF-8.

* `plan_checksum` — the SHA-256 hex digest of the UTF-8 encoding of
  `asset_count|total_proposed_severity|max_single_bundle_severity|max_contained_severity|contained_asset_count|residual_contained_severity|total_asset_pressure|max_asset_pressure|containment_score|coverage_permille|residual_pressure|PC|CC|CRC|MU|CRI|TEO|RWC|TRL|MRL|RTC|RO|id0,id1,...`
  where `PC` is `proposed_tier_counts` as `critical,major,minor`, `CC` is
  `contained_tier_counts` as `critical,major,minor`, `CRC` is
  `critical_response_count`, `MU` is `max_urgency`, `CRI` is
  `critical_response_ids` comma-joined ascending, `TEO` is
  `total_exposure_overlap`, `RWC` is `response_wave_count`, `TRL` is
  `total_response_load`, `MRL` is `max_response_load`, `RTC` is
  `response_tier_counts` as `immediate,urgent,routine`, `RO` is `response_order`
  comma-joined in response order (not ascending), and the trailing segment is
  `contained_bundle_ids` comma-joined in ascending order.

  The six segments `TEO|RWC|TRL|MRL|RTC|RO` sit between `CRI` and the trailing
  `contained_bundle_ids`; the payload does not end at `CRI`.

The program reads its input from `--input` (default `/app/data/remediation.json`)
and writes to `--output-dir` (default `/app/output`).
