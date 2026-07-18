# Sentinel-1 remediation-planning model

This is the authoritative definition of the Sentinel-1 remediation-planning
model and of the output contract. During incident response a set of candidate
remediation **bundles** is proposed; each bundle has a severity weight and locks
a set of shared assets. Two bundles conflict when they lock a common asset and
cannot both be applied. The task is to select the set of pairwise
**asset-disjoint** bundles that maximizes the total contained severity.

## Input

The input (`/app/data/remediation.json`) has the shape:

```json
{ "asset_count": M, "bundles": [ {"id": "...", "severity": w, "assets": [a, ...]}, ... ] }
```

Assets are integers `0 .. M-1`. Each bundle has a string `id`, an integer
`severity`, and a list of the asset ids it locks.

## Canonicalization

Before planning, normalize the bundle list:

* Drop any bundle whose `severity` is outside the valid range `1 .. 9` inclusive.
* Drop any bundle with an empty asset list.
* Within a bundle, deduplicate and sort the asset ids.
* If the same `id` appears more than once, keep the single occurrence with the
  **maximum** severity.

The canonical bundle list is ordered by `id` ascending.

## Contained severity (the objective)

`max_contained_severity` is the **maximum total severity of a set of pairwise
asset-disjoint bundles**. Two bundles may both be selected only if they lock no
common asset. Choose the set of bundles — pairwise asset-disjoint — that
maximizes the summed severity; the empty set scores 0.

**`max_contained_severity` is NOT the sum of all bundle severities** — bundles
compete for assets, so a bundle sharing an asset with a selected bundle cannot
also be counted, and the summed-over-everything value badly over-counts. **It is
also NOT a greedy highest-severity-first selection** — repeatedly taking the
highest-severity still-compatible bundle is not optimal for this packing and in
general yields a strictly smaller total than the exact maximum. Compute the
exact maximum-weight asset-disjoint packing.

## The selected set and its tie-break

The objective value `max_contained_severity` may be achievable by more than one
pairwise asset-disjoint bundle set (ties are common). The **contained set** is
selected deterministically: among **all** pairwise asset-disjoint bundle sets
whose summed severity equals `max_contained_severity`, choose the one whose
bundle ids, sorted ascending, form the **lexicographically smallest tuple**,
compared element by element as strings (so `("rb-01",)` precedes
`("rb-02",)`, and at equal first elements a shorter/earlier second element
wins). Note this is a tie-break over **whole optimal sets**, not a greedy
smallest-id-first construction: you must consider every set that attains the
maximum and then take the lexicographically least. `contained_bundle_ids` lists
that set's ids in ascending order; the empty set (value 0) is the baseline when
no bundle can be selected.

The **residual packing** re-runs the identical maximum-weight asset-disjoint
objective over only the canonical bundles that are **not** in the contained set,
and `residual_contained_severity` is that packing's value (0 if none remain).

## Output

Write `plan.json` to the output directory (`/app/output` by default) with
exactly these keys:

* `asset_count` — copied from the input.
* `bundle_count` — the number of canonical bundles.
* `total_proposed_severity` — the sum of all canonical bundle severities (a
  summary of what was proposed; not the contained severity).
* `max_single_bundle_severity` — the largest single canonical bundle severity
  (0 if none).
* `max_contained_severity` — the exact packing objective defined above.
* `contained_bundle_ids` — the tie-broken contained set's bundle ids, ascending.
* `contained_bundle_count` — the number of ids in `contained_bundle_ids`.
* `contained_asset_count` — the number of distinct assets locked by the
  contained set.
* `uncontained_severity` — `total_proposed_severity - max_contained_severity`.
* `residual_contained_severity` — the residual packing value defined above.
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
