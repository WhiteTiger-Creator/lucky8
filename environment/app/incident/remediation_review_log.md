# Sentinel-1 Remediation Planning Review Log
Sentinel-1 incident-response board — containment review archive for the intrusion remediation programme. These entries govern how compromised assets are quarantined and how residual exposure is scored.
Sentinel-1 incident-response board — governance archive for the remediation-planning model (2026-Q1 through 2026-Q2).

## Executive Summary
The remediation planner has produced unsafe containment plans since the February rollout. How the plan is *meant* to be computed — bundle canonicalization and its validity bounds, the containment objective, the tie-broken selected set, the residual packing, and the plan-derived aggregates — was settled incrementally by the incident-response board, and those decisions live in the review entries below, not in any single summary. The February draft proposals were revisited during the 2026-05 review cycle and several were reversed; where a draft proposal and a later decision disagree, the later decision governs, and where a decision was itself revised by a still-later one, the latest dated decision is binding — trace each rule to its final entry. `/app/docs/plan_spec.md` is the output contract only: it fixes the input shape, the exact `plan.json` key set, and the checksum serialization, not how the values are derived.

## February Draft Proposals (2026-02 — partly reversed)
The initial rollout circulated planning-behavior proposals through SR tickets in the 1900 range. Several did not survive review; they are archived in place below and marked superseded — do not implement them as written.

### Review entry 0001 — intake lane
> **Board proposal (2026-02-04 - SR-1902)** Rhea: bundle severities are valid in the range 1..5; bundles outside that range are dropped. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Shift lead logged a routine intake observation for the containment queue. Dashboard tiles lagged during a rule refresh; attributed to cache staleness, not the planner.

### Review entry 0002 — triage lane
> **Board proposal (2026-02-07 - SR-1905)** Rhea: when a bundle id repeats, keep the FIRST occurrence encountered and discard the rest. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Review entry 0003 — scoping lane
> **Board proposal (2026-02-10 - SR-1908)** Tomas: the contained severity is the SUM of every canonical bundle's severity — the total proposed severity is what the plan reports as contained. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Review entry 0004 — scoping lane
> **Board proposal (2026-02-13 - SR-1911)** Tomas: the contained severity is computed greedily — repeatedly take the highest-severity bundle still asset-compatible with the ones already chosen; that greedy total is the reported contained severity. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Historical CSV exports remain archived and non-authoritative for the JSON plan acceptance.

### Review entry 0005 — selection lane
> **Board proposal (2026-02-16 - SR-1914)** Dana: when the objective admits more than one optimal set, report ANY one of them — the selected set is not required to be canonical. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Thread archived; see the SR decision entries for anything affecting planner behavior.

## Governance Review Archive (2025-Q4 through 2026-Q2)
Routine entries are context only. SR-ticketed proposal and decision quotes embedded in the entries are the authoritative record for planner behavior.

### Review entry 0021 — intake lane
> **Board decision (2026-04-09 - SR-2104)** Priya: bundle severities are valid in the range 1..7; assets are kept in input order without deduplication. *(Revised — see the 2026-05 review.)*
Shift lead logged a routine intake observation; rotation swap approved, no parameter change.

### Review entry 0022 — selection lane
> **Board decision (2026-04-12 - SR-2108)** Priya: among optimal sets, prefer the one built by taking eligible bundles in ascending id order (a greedy smallest-id-first construction). *(Revised — see the 2026-05 review.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Review entry 0023 — residual lane
> **Board decision (2026-04-16 - SR-2112)** Dana: the residual severity is the best packing over the bundles whose assets are entirely disjoint from the selected set's assets. *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Review entry 0024 — scoring lane
> **Board decision (2026-04-18 - SR-2116)** Priya: severity tiers — a bundle is `critical` when its severity is 8 or 9, `major` when 5 to 7, and `minor` when 4 or below. *(Revised — see the 2026-05 review.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Review entry 0025 — scoring lane
> **Board decision (2026-04-20 - SR-2118)** Priya: a bundle's asset pressure is `severity + asset_count`; `total_asset_pressure` sums it over canonical bundles and `max_asset_pressure` is the largest. *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Review entry 0026 — scoring lane
> **Board decision (2026-04-22 - SR-2120)** Dana: `containment_score` = sum over the contained set of `severity * 3 + asset_count`, with no divisor. *(Revised — see the 2026-05 review.)*
Thread archived; see the SR decision entries for anything affecting planner behavior.

### Review entry 0027 — scoring lane
> **Board decision (2026-04-24 - SR-2122)** Dana: `coverage_permille` reports coverage as a percent — `contained_asset_count * 100 // asset_count` (0 when asset_count is 0). *(Revised — see the 2026-05 review.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Review entry 0028 — scoring lane
> **Board decision (2026-04-28 - SR-2124)** Dana: `residual_pressure` is the sum of asset pressure over ALL canonical bundles (contained and not). *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Review entry 0031 — canonicalization lane
> **Board decision (2026-05-03 - SR-2201)** Ilya: bundle canonicalization — drop any bundle whose severity is outside the inclusive range 1..9, and drop any bundle with an empty asset list. Within a bundle, deduplicate the asset ids and sort them ascending. When the same bundle id appears more than once, keep the single occurrence with the MAXIMUM severity. The canonical bundle list is ordered by bundle id ascending. This supersedes SR-1902, SR-1905 and SR-2104.

### Review entry 0032 — objective lane
> **Board decision (2026-05-05 - SR-2203)** Ilya: the contained severity `max_contained_severity` is the exact maximum total severity of a set of pairwise ASSET-DISJOINT bundles — the maximum-weight asset-disjoint packing. It is NOT the sum of all bundle severities (bundles contend for assets) and NOT a greedy highest-severity-first selection (greedy is not optimal). The empty set scores 0. This supersedes SR-1908 and SR-1911.

### Review entry 0033 — selection lane
> **Board decision (2026-05-08 - SR-2205)** Marta: the contained set is selected deterministically. Among ALL pairwise asset-disjoint bundle sets whose summed severity equals `max_contained_severity`, choose the one whose bundle ids, sorted ascending, form the lexicographically smallest tuple (compared element by element as strings). This is a tie-break over whole optimal sets, not a greedy smallest-id construction: consider every set that attains the maximum, then take the lexicographically least. `contained_bundle_ids` lists that set's ids ascending. This supersedes SR-1914 and SR-2108.

### Review entry 0034 — residual lane
> **Board decision (2026-05-10 - SR-2207)** Marta: the residual packing re-runs the identical maximum-weight asset-disjoint objective over only the canonical bundles that are NOT in the contained set (identified by bundle id); `residual_contained_severity` is that packing's value (0 if none remain). The bundles that lost the tie-break contend among themselves, so this is a genuine second packing — it is NOT restricted to bundles asset-disjoint from the selected set. This supersedes SR-2112.

### Review entry 0035 — scoring lane
> **Board decision (2026-05-12 - SR-2209)** Ilya: severity tiers — a bundle is `critical` when its severity is 7 or greater, `major` when 4 to 6 inclusive, and `minor` when 3 or below. `proposed_tier_counts` counts the canonical bundles in each tier; `contained_tier_counts` counts only the bundles in the contained set in each tier. This supersedes SR-2116.

### Review entry 0036 — scoring lane
> **Board decision (2026-05-13 - SR-2211)** Ilya: a bundle's asset pressure is the PRODUCT `severity * asset_count` (asset_count being the number of distinct locked assets after canonicalization). `total_asset_pressure` sums asset pressure over all canonical bundles; `max_asset_pressure` is the largest single value (0 if none). This supersedes SR-2118.

### Review entry 0037 — scoring lane
> **Board decision (2026-05-14 - SR-2213)** Marta: `containment_score` = sum over the bundles in the contained set of `(severity * 5 + asset_count * 2) // 3` — the weighted term is floored with integer division per bundle before summing. This supersedes SR-2120.

### Review entry 0038 — scoring lane
> **Board decision (2026-05-15 - SR-2215)** Marta: `coverage_permille` = `contained_asset_count * 1000 // asset_count` (per-mille, not percent), and 0 when asset_count is 0. This supersedes SR-2122.

### Review entry 0039 — scoring lane
> **Board decision (2026-05-16 - SR-2217)** Marta: `residual_pressure` is the sum of asset pressure over only the canonical bundles that are NOT in the contained set — the same complement used by the residual packing. This supersedes SR-2124.

### Review entry 0026b — response-ledger lane
> **Board proposal (2026-02-19 - SR-1930)** Tomas: response-urgency ledger — process canonical bundles in id order; carry_in = max(previous carry_out - (shared_prev_assets * 5) // 2, 0) where shared_prev_assets is the asset overlap with the previous canonical bundle; urgency = asset_pressure + carry_in // 4; carry_out = min(carry_in + asset_pressure, 80); a bundle joins the critical response set when urgency >= 25. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Review entry 0029b — response-ledger lane
> **Board decision (2026-04-30 - SR-2126)** Priya: response-urgency ledger interim — carry_in = max(previous carry_out - (shared_prev_assets * 7) // 2, 0); urgency = asset_pressure + carry_in // 4; carry_out = min(carry_in + asset_pressure - asset_count // 2, 100); critical when urgency >= 28. *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Review entry 0040 — response-ledger lane
> **Board decision (2026-05-18 - SR-2219)** Marta: response-urgency ledger (final) — process canonical bundles in id order; carry starts at 0. For each bundle: shared_prev is the count of assets shared with the immediately-preceding canonical bundle (0 for the first); `carry_in = max(previous_carry_out - (shared_prev * 7) // 3, 0)`; `urgency = asset_pressure + ceil(carry_in / 5)` — the carry credit is divided by 5 and **rounded UP** (ceiling), not floored (asset_pressure = severity * n_assets per SR-2211, where n_assets is the number of assets THIS bundle locks, i.e. len(bundle.assets)); `carry_out = min(carry_in + asset_pressure - (n_assets // 2), 90)` — here **n_assets is the count of assets this bundle locks (len of its own asset list), NOT the global input asset_count**; a bundle is admitted to the critical response set when `urgency >= 30`. `critical_response_ids` are the admitted bundle ids sorted ascending; `critical_response_count` is their number; `max_urgency` is the maximum urgency over all canonical bundles. The `* 7`/`// 3` decay, the `// 5` carry credit, the 90 cap and the 30 threshold are final and revise SR-2126; this supersedes SR-1930.

### Review entry 0710 — containment bench
> **Board draft (2026-03-05 - SR-1934)** Rao: response load — a contained bundle's response load is `severity * 3` and nothing else; every contained bundle joins the response wave, with no response_load floor and no class. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*

### Review entry 0712 — containment bench
> **Board interim (2026-04-18 - SR-2130)** Priya: response load interim — response load adds the exposure overlap a contained bundle inherits, halved with integer floor division, and subtracts nothing: `response_load = severity * 3 + exposure_overlap // 2`. Bundles join the response wave at `response_load >= 12` and carry one of TWO classes. *(Revised — see the 2026-05 review.)*

### Review entry 0714 — containment bench
> **Board decision (2026-05-19 - SR-2231)** Nadia: response load (final). Only bundles in the contained set join the response wave. A contained bundle's `exposure_overlap` is the total number of shared asset slots it has with the bundles that were NOT contained, counted with multiplicity across those bundles (a bundle sharing two assets with each of two uncontained bundles contributes four), and `exposing_bundle_count` is how many uncontained bundles it shares at least one asset with. `total_exposure_overlap` sums `exposure_overlap` over the contained bundles. Effort is `max(severity * 3 + ceil(exposure_overlap / 2) - (n_assets // 2), 0)`: the conflict half is HALVED AND ROUNDED UP, revising the floored form in SR-2130, while the asset relief `n_assets // 2` is floored. In integer arithmetic ceil(x/2) is -(-x // 2). Here `n_assets` is the count of assets that bundle itself locks, not the global asset_count. This supersedes SR-1934 and SR-2130.

### Review entry 0716 — containment bench
> **Board decision (2026-05-20 - SR-2233)** Nadia: response-wave admission and class (final). A contained bundle joins the response wave when `response_load >= 16`. Scheduled bundles carry exactly one of THREE classes, evaluated in clause order with the first match fixing the class: `immediate` when `response_load >= 27`; otherwise `urgent` when `response_load >= 21`, or `exposure_overlap >= 4`; otherwise `routine`. `response_wave_ids` are the response-wave bundles' ids sorted ascending. This supersedes the two-class scheme in SR-2130.

### Review entry 0718 — containment bench
> **Board decision (2026-05-20 - SR-2235)** Nadia: response-wave reporting (final). `response_tier_counts` always enumerates ALL THREE response-tier names in the order `immediate`, `urgent`, `routine`, emitting 0 for a class with no response-wave bundles. `response_order` lists the response-wave bundle ids ordered strictly in this sequence: class rank `immediate` > `urgent` > `routine`; then `response_load` descending; then `severity` descending; then `exposing_bundle_count` descending; then bundle id ascending — this is an ordering, not ascending id order, which is what `response_wave_ids` carries. `total_response_load` sums `response_load` over the response-wave bundles and `max_response_load` is the largest (0 when none join the response wave). `response_wave_checksum` is the SHA-256 hex digest of one line per response-wave bundle in `response_order` order, each `id|response_tier|response_load|exposure_overlap`, lines joined by a single newline with no trailing newline, hashed over the UTF-8 encoding.

### Review entry 0041 — audit lane
Shift lead logged a routine audit observation; quarterly recertification touched this lane, no planner-relevant configuration changed.

### Review entry 0042 — audit lane
> **Board decision (2026-05-22 - SR-2240)** Priya: remediation dashboards retain ninety days of plan history; older plans are served from the artifact archive on demand. Dashboard retention is an operational setting and carries no weight in plan output.

### Review entry 0043 — audit lane
> **Board decision (2026-05-26 - SR-2243)** Marta: artifact bundles must record plan signatures at export and again at archive ingest; a mismatch quarantines the bundle for manual review. Evidence handling only; plan contents are unaffected.
