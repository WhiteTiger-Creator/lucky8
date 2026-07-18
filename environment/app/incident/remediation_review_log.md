# Sentinel-1 Remediation Planning Review Log
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

### Review entry 0031 — canonicalization lane
> **Board decision (2026-05-03 - SR-2201)** Ilya: bundle canonicalization — drop any bundle whose severity is outside the inclusive range 1..9, and drop any bundle with an empty asset list. Within a bundle, deduplicate the asset ids and sort them ascending. When the same bundle id appears more than once, keep the single occurrence with the MAXIMUM severity. The canonical bundle list is ordered by bundle id ascending. This supersedes SR-1902, SR-1905 and SR-2104.

### Review entry 0032 — objective lane
> **Board decision (2026-05-05 - SR-2203)** Ilya: the contained severity `max_contained_severity` is the exact maximum total severity of a set of pairwise ASSET-DISJOINT bundles — the maximum-weight asset-disjoint packing. It is NOT the sum of all bundle severities (bundles contend for assets) and NOT a greedy highest-severity-first selection (greedy is not optimal). The empty set scores 0. This supersedes SR-1908 and SR-1911.

### Review entry 0033 — selection lane
> **Board decision (2026-05-08 - SR-2205)** Marta: the contained set is selected deterministically. Among ALL pairwise asset-disjoint bundle sets whose summed severity equals `max_contained_severity`, choose the one whose bundle ids, sorted ascending, form the lexicographically smallest tuple (compared element by element as strings). This is a tie-break over whole optimal sets, not a greedy smallest-id construction: consider every set that attains the maximum, then take the lexicographically least. `contained_bundle_ids` lists that set's ids ascending. This supersedes SR-1914 and SR-2108.

### Review entry 0034 — residual lane
> **Board decision (2026-05-10 - SR-2207)** Marta: the residual packing re-runs the identical maximum-weight asset-disjoint objective over only the canonical bundles that are NOT in the contained set (identified by bundle id); `residual_contained_severity` is that packing's value (0 if none remain). The bundles that lost the tie-break contend among themselves, so this is a genuine second packing — it is NOT restricted to bundles asset-disjoint from the selected set. This supersedes SR-2112.

### Review entry 0041 — audit lane
Shift lead logged a routine audit observation; quarterly recertification touched this lane, no planner-relevant configuration changed.

### Review entry 0042 — audit lane
> **Board decision (2026-05-22 - SR-2240)** Priya: remediation dashboards retain ninety days of plan history; older plans are served from the artifact archive on demand. Dashboard retention is an operational setting and carries no weight in plan output.

### Review entry 0043 — audit lane
> **Board decision (2026-05-26 - SR-2243)** Marta: artifact bundles must record plan signatures at export and again at archive ingest; a mismatch quarantines the bundle for manual review. Evidence handling only; plan contents are unaffected.
