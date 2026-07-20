# Sentinel-1 Remediation Planning Review Log
Sentinel-1 incident-response board — containment review archive for the intrusion remediation programme. These entries govern how compromised assets are quarantined and how residual exposure is scored.
Sentinel-1 incident-response board — governance archive for the remediation-planning model (2026-Q1 through 2026-Q2).

## Executive Summary
The remediation planner has produced unsafe containment plans since the February rollout. How the plan is *meant* to be computed — bundle canonicalization and its validity bounds, the containment objective, the tie-broken selected set, the residual packing, and the plan-derived aggregates — was settled incrementally by the incident-response board, and those decisions live in the review entries below, not in any single summary. The February draft proposals were revisited during the 2026-05 review cycle and several were reversed; where a draft proposal and a later decision disagree, the later decision governs, and where a decision was itself revised by a still-later one, the latest dated decision is binding — trace each rule to its final entry. `/app/docs/plan_spec.md` is the output contract only: it fixes the input shape, the exact `plan.json` key set, and the checksum serialization, not how the values are derived.

## February Draft Proposals (2026-02 — partly reversed)
The initial rollout circulated planning-behavior proposals through SR tickets in the 1900 range. Several did not survive review; they are archived in place below and marked superseded — do not implement them as written.

### Remediation review 001 - edge-gateway
Responders confirmed the host was isolated before the sweep began and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2403; responder rota entry 2.

### Remediation review 002 - payments-core
Triage recorded the bundle as proposed by the on-call responder and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2406; responder rota entry 3.

### Remediation review 003 - identity-store
The asset owner acknowledged the containment notice inside the agreed window and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2409; responder rota entry 4.

### Remediation review 004 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2412; responder rota entry 5.

### Remediation review 005 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2415; responder rota entry 6.

### Review entry 0001 — intake lane
> **Board proposal (2026-02-04 - SR-1902)** Rhea: bundle severities are valid in the range 1..5; bundles outside that range are dropped. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Shift lead logged a routine intake observation for the containment queue. Dashboard tiles lagged during a rule refresh; attributed to cache staleness, not the planner.

### Remediation review 005b - board decision
> **Board decision (2026-05-21 - SR-2237)** Nadia: per-bundle remediation ledger (final). Every canonical bundle is reported, including bundles that were never contained and bundles that did not join the response wave — the ledger is the audit record for the whole proposal set, not for the wave. Row order is: contained bundles before uncontained ones; then `response_load` descending; then `urgency` descending; then `severity` descending; then `bundle_id` ascending. Two distinct cases must not be conflated. A bundle that was never contained is not assessed for the wave at all: it reports `response_tier` as the literal string `none` and zero for `exposure_overlap`, `exposing_bundle_count` and `response_load`, because those quantities are only defined for contained bundles. A CONTAINED bundle that was assessed but fell below the wave admission floor is different: it KEEPS its computed `exposure_overlap`, `exposing_bundle_count` and `response_load` — those were genuinely derived for it — and reports `in_response_wave` as 0 with `response_tier` as `none`. In short, the zero-reporting rule keys off `contained`, not off `in_response_wave`; a contained bundle below the floor still reports the load that kept it out. The three flags `contained`, `critical_response` and `in_response_wave` are emitted as integers 0 or 1, never as JSON booleans.

### Remediation review 005c - board decision
> **Board decision (2026-05-22 - SR-2239)** Marta: per-asset exposure view (final). Every asset id in the estate is reported, from 0 to asset_count-1 inclusive, including assets no proposed bundle claims. A bundle CLAIMS an asset when the asset appears in that bundle's asset list, whether or not the bundle was contained. Each field is derived as follows and no field is derived from another bundle's asset_pressure: `claiming_bundle_ids` — the ids of all claiming bundles, sorted ascending; `claiming_bundle_count` — the number of claiming bundles, i.e. the length of that list; `max_claim_severity` — the LARGEST `severity` value among the claiming bundles, and 0 when there are none; `total_claim_severity` — the SUM of the `severity` values of the claiming bundles, and 0 when there are none. Note carefully that `total_claim_severity` sums raw severities only. It does NOT sum the claiming bundles' `asset_pressure` (which is `severity * n_assets` per the scoring layer) and it does not multiply by anything: a bundle of severity 4 contributes exactly 4 to this total no matter how many assets it locks. `contention` — `claiming_bundle_count - 1`, floored at 0, representing how many proposals had to be turned away for that asset. `locked_by` — the id of the contained bundle that locks the asset, or the literal string `none`; because the containment set is asset-disjoint at most one contained bundle can claim any asset, so this is unambiguous. `is_locked` — 0 when `locked_by` is `none`, otherwise 1. An unclaimed asset reports an empty `claiming_bundle_ids`, `none` for `locked_by`, and 0 for every numeric field. Row order is: contention descending; then total_claim_severity descending; then is_locked descending; then asset_id ascending.

### Remediation review 005d - board decision
> **Board decision (2026-05-23 - SR-2241)** Nadia: exposure attribution (final). An uncontained bundle that contends for assets belonging to more than one contained bundle is attributed to exactly ONE of them, not to each. For each uncontained bundle, take the contained bundles it shares any asset with (its claimants) and pick the OWNER: highest severity, ties broken by lexicographically smallest bundle id. The owner then adds to its `exposure_overlap` the number of assets IT ITSELF shares with that uncontained bundle -- that is, the size of the intersection of the owner's own asset set with the uncontained bundle's asset set. Every other claimant adds zero for that uncontained bundle. The owner does NOT absorb assets that the uncontained bundle shares only with some other claimant; those assets are counted by nobody. Worked example: uncontained U holds assets {a, b}; contained A (severity 5) holds {a}; contained B (severity 3) holds {b}. A is the owner because its severity is higher, and A adds |{a} INTERSECT {a, b}| = 1 -- not 2. B adds 0, and asset b is counted by nobody. `total_exposure_overlap` is the sum of the per-bundle `exposure_overlap` values produced this way, so a reader who lets every claimant count its own intersection, or who lets the owner absorb the whole contended set, will overstate it.

### Remediation review 005e - board decision
> **Board decision (2026-05-23 - SR-2243)** Marta: duplicate-bundle severity precedence is REVERSED. Repeated bundle ids arrive from an automated proposer that raises severity on re-submission before a responder has confirmed it, so keeping the maximum was inflating the plan. Where a bundle id appears more than once in the input, the row with the LOWER severity is kept. The validity bounds and the asset deduplication recorded earlier are unchanged; only the severity comparison reverses.

### Remediation review 005f - board decision
> **Board decision (2026-05-24 - SR-2245)** Nadia: responder capacity cap. The wave is capped at TWO bundles per response tier. The cap is applied as a final pass over the fully ordered wave, not during admission and not per tier before ordering: admit, classify and order every bundle as before per SR-2233 and SR-2235, then walk the ordered wave from the top keeping the first two bundles of each tier and discarding the rest. Which bundles survive therefore depends on the global ordering chain. `response_tier_counts`, `response_wave_ids`, `response_wave_count`, `total_response_load`, `max_response_load` and `response_wave_checksum` all describe the wave AFTER the cap. A bundle discarded by the cap is not in the wave: in the per-bundle ledger it reports `in_response_wave` as 0 and `response_tier` as the literal string `none`, exactly like a contained bundle that never cleared the admission floor. The tier it would have carried is not reported anywhere.

> **Board decision (2026-05-27 - SR-2248)** Priya: per-band remediation policy (final). The wave and urgency thresholds are no longer single global constants. They are resolved PER BUNDLE from `/app/data/remediation_policies.json` at that fixed absolute path, keyed by the bundle's SEVERITY BAND: severity 1-3 is `low`, 4-6 is `mid`, 7-9 is `high`, banded on the CANONICAL severity -- the one that survives the duplicate-id rule of SR-2243, not the raw proposed severity. Resolution is three tiers, each overlaying the one before: the shipped baseline `wave_floor=16, immediate_min=27, urgent_min=21, urgent_overlap_min=4, urgency_threshold=30, carry_cap=90`; then the file's `default` object, which may name only SOME fields -- every field it omits keeps its baseline value; then that band's entry in `band_overrides`, likewise sparse, inheriting every field it does not name. An override is never a complete policy on its own, and a band with no entry resolves to the file default. The six resolved fields replace the former constants exactly: `wave_floor` is the response-wave admission floor, `immediate_min` / `urgent_min` / `urgent_overlap_min` are the clause bounds of SR-2233, and `urgency_threshold` / `carry_cap` are the critical-response bar and carry ceiling of the SR-2219 ledger. Those entries still govern everything else about their stages; only the threshold VALUES move here. Because the band comes from each bundle's own severity, two bundles in the same wave can be admitted against different floors. `policy_checksum` is sha256 over the resolved default line followed by one line per band in the fixed order `low`, `mid`, `high` -- every band, including one with no override -- each `band|` then the six resolved values in the field order listed above joined by `|`, lines joined by newline. Note the resolved values, not the raw override values.

> **Board decision (2026-05-28 - SR-2250)** Marta: containment-window attenuation (final). Responders cannot tear down assets that sit inside an active containment window, so a bundle's response load is attenuated before wave admission. Windows are read from `/app/data/containment_windows.json` at that fixed absolute path; each carries a `layer` (`blackout` or `maintenance`), a `band`, a half-open asset range `[lo, hi)` and a per-asset `charge`. SCOPE: for each layer, a bundle uses the windows recorded for its OWN severity band -- banded per SR-2248 on the canonical severity. Only a band with NO window of its own in that layer falls back to the `all`-scoped windows; a band that has its own entry does NOT additionally inherit `all`. CHARGE: count only the bundle's OWN assets that fall inside a window, and where several windows of the same layer cover one asset, charge the MAXIMUM of their charges, not their sum. The layer's overlap is the sum of those per-asset charges. ATTENUATION: `response_load = max(raw_load - ceil(blackout_overlap / 2) - (maintenance_overlap // 3), 0)` -- the blackout half is ROUNDED UP and the maintenance half is FLOORED, and `raw_load` is the effort value of SR-2231. `total_blackout_overlap` and `total_maintenance_overlap` sum the per-bundle overlaps over the contained bundles. `containment_window_checksum` is sha256 over the windows serialized `layer|band|lo|hi|charge`, ordered by layer, then band, then lo, then hi, then charge, joined by newline. ROUNDING: blackout_overlap // 2 = CEIL. ROUNDING: maintenance_overlap // 3 = FLOOR.

> **Board decision (2026-05-28 - SR-2252)** Marta: containment-layer precedence (final). The two layers may cover the same asset, and until now such an asset was charged twice. BLACKOUT takes precedence: an asset charged under blackout is NOT charged again under maintenance. Resolve each layer's per-asset charges as SR-2250 specifies, then drop from the maintenance set every asset that appears in the blackout set, and sum what remains. The precedence changes the maintenance side only: `blackout_overlap` is unaffected, and an asset covered by maintenance alone is charged normally. Worked example: a bundle holds assets {a, b}; blackout charges a at 5; maintenance charges a at 3 and b at 4. Then `blackout_overlap` is 5 and `maintenance_overlap` is 4 -- not 7 -- because a is already charged under blackout.

### Remediation review 006 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2418; responder rota entry 7.

### Remediation review 007 - search-index
Containment tooling reported the group reachable at the start of the window and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2421; responder rota entry 8.

### Remediation review 008 - metrics-sink
A responder walked the runbook for this group with the platform on-call and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2424; responder rota entry 9.

### Remediation review 009 - queue-broker
The wave was staged behind a dependency freeze released that morning and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2427; responder rota entry 10.

### Remediation review 010 - config-store
Detection replayed the original signature against this group before containment and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2430; responder rota entry 11.

### Remediation review 011 - cdn-origin
The group was pulled forward after an adjacent group completed early and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2433; responder rota entry 12.

### Remediation review 012 - auth-proxy
An owner handover moved this group to a second responder mid-window and no further lateral movement was observed on the segment afterwards Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2436; responder rota entry 13.

### Remediation review 013 - log-shipper
Responders confirmed the host was isolated before the sweep began though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2439; responder rota entry 14.

### Remediation review 014 - key-vault
Triage recorded the bundle as proposed by the on-call responder though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2442; responder rota entry 15.

### Remediation review 015 - report-render
The asset owner acknowledged the containment notice inside the agreed window though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2445; responder rota entry 16.

### Remediation review 016 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2448; responder rota entry 17.

### Remediation review 017 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2451; responder rota entry 18.

### Remediation review 018 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2454; responder rota entry 19.

### Remediation review 019 - session-store
Containment tooling reported the group reachable at the start of the window though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2457; responder rota entry 20.

### Remediation review 020 - policy-engine
A responder walked the runbook for this group with the platform on-call though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2460; responder rota entry 21.

### Remediation review 021 - artifact-repo
The wave was staged behind a dependency freeze released that morning though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2463; responder rota entry 22.

### Remediation review 022 - telemetry-hub
Detection replayed the original signature against this group before containment though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2466; responder rota entry 23.

### Remediation review 023 - ledger-api
The group was pulled forward after an adjacent group completed early though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2469; responder rota entry 24.

### Remediation review 024 - edge-cache
An owner handover moved this group to a second responder mid-window though a duplicate proposal from a second responder was withdrawn at handover Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2472; responder rota entry 25.

### Remediation review 025 - edge-gateway
Responders confirmed the host was isolated before the sweep began after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2475; responder rota entry 26.

### Remediation review 026 - payments-core
Triage recorded the bundle as proposed by the on-call responder after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2478; responder rota entry 27.

### Review entry 0002 — triage lane
> **Board proposal (2026-02-07 - SR-1905)** Rhea: when a bundle id repeats, keep the FIRST occurrence encountered and discard the rest. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Remediation review 027 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2481; responder rota entry 28.

### Remediation review 028 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2484; responder rota entry 29.

### Remediation review 029 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2487; responder rota entry 30.

### Remediation review 030 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2490; responder rota entry 31.

### Remediation review 031 - search-index
Containment tooling reported the group reachable at the start of the window after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2493; responder rota entry 32.

### Remediation review 032 - metrics-sink
A responder walked the runbook for this group with the platform on-call after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2496; responder rota entry 33.

### Remediation review 033 - queue-broker
The wave was staged behind a dependency freeze released that morning after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2499; responder rota entry 34.

### Remediation review 034 - config-store
Detection replayed the original signature against this group before containment after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2502; responder rota entry 35.

### Remediation review 035 - cdn-origin
The group was pulled forward after an adjacent group completed early after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2505; responder rota entry 36.

### Remediation review 036 - auth-proxy
An owner handover moved this group to a second responder mid-window after a brief reconnection attempt that never reached the control plane Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2508; responder rota entry 37.

### Remediation review 037 - log-shipper
Responders confirmed the host was isolated before the sweep began with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2511; responder rota entry 1.

### Remediation review 038 - key-vault
Triage recorded the bundle as proposed by the on-call responder with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2514; responder rota entry 2.

### Remediation review 039 - report-render
The asset owner acknowledged the containment notice inside the agreed window with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2517; responder rota entry 3.

### Remediation review 040 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2520; responder rota entry 4.

### Remediation review 041 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2523; responder rota entry 5.

### Remediation review 042 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2526; responder rota entry 6.

### Remediation review 043 - session-store
Containment tooling reported the group reachable at the start of the window with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2529; responder rota entry 7.

### Remediation review 044 - policy-engine
A responder walked the runbook for this group with the platform on-call with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2532; responder rota entry 8.

### Remediation review 045 - artifact-repo
The wave was staged behind a dependency freeze released that morning with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2535; responder rota entry 9.

### Remediation review 046 - telemetry-hub
Detection replayed the original signature against this group before containment with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2538; responder rota entry 10.

### Remediation review 047 - ledger-api
The group was pulled forward after an adjacent group completed early with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2541; responder rota entry 11.

### Review entry 0003 — scoping lane
> **Board proposal (2026-02-10 - SR-1908)** Tomas: the contained severity is the SUM of every canonical bundle's severity — the total proposed severity is what the plan reports as contained. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Remediation review 048 - edge-cache
An owner handover moved this group to a second responder mid-window with two listed assets already rebuilt and therefore dropped from scope Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2544; responder rota entry 12.

### Remediation review 049 - edge-gateway
Responders confirmed the host was isolated before the sweep began while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2547; responder rota entry 13.

### Remediation review 050 - payments-core
Triage recorded the bundle as proposed by the on-call responder while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2550; responder rota entry 14.

### Remediation review 051 - identity-store
The asset owner acknowledged the containment notice inside the agreed window while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2553; responder rota entry 15.

### Remediation review 052 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2556; responder rota entry 16.

### Remediation review 053 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2559; responder rota entry 17.

### Remediation review 054 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2562; responder rota entry 18.

### Remediation review 055 - search-index
Containment tooling reported the group reachable at the start of the window while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2565; responder rota entry 19.

### Remediation review 056 - metrics-sink
A responder walked the runbook for this group with the platform on-call while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2568; responder rota entry 20.

### Remediation review 057 - queue-broker
The wave was staged behind a dependency freeze released that morning while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2571; responder rota entry 21.

### Remediation review 058 - config-store
Detection replayed the original signature against this group before containment while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2574; responder rota entry 22.

### Remediation review 059 - cdn-origin
The group was pulled forward after an adjacent group completed early while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2577; responder rota entry 23.

### Remediation review 060 - auth-proxy
An owner handover moved this group to a second responder mid-window while a credential rotation held the containment lock for part of the window Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2580; responder rota entry 24.

### Remediation review 061 - log-shipper
Responders confirmed the host was isolated before the sweep began once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2583; responder rota entry 25.

### Remediation review 062 - key-vault
Triage recorded the bundle as proposed by the on-call responder once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2586; responder rota entry 26.

### Remediation review 063 - report-render
The asset owner acknowledged the containment notice inside the agreed window once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2589; responder rota entry 27.

### Remediation review 064 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2592; responder rota entry 28.

### Remediation review 065 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2595; responder rota entry 29.

### Remediation review 066 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2598; responder rota entry 30.

### Remediation review 067 - session-store
Containment tooling reported the group reachable at the start of the window once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2601; responder rota entry 31.

### Remediation review 068 - policy-engine
A responder walked the runbook for this group with the platform on-call once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2604; responder rota entry 32.

### Review entry 0004 — scoping lane
> **Board proposal (2026-02-13 - SR-1911)** Tomas: the contained severity is computed greedily — repeatedly take the highest-severity bundle still asset-compatible with the ones already chosen; that greedy total is the reported contained severity. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Historical CSV exports remain archived and non-authoritative for the JSON plan acceptance.

### Remediation review 069 - artifact-repo
The wave was staged behind a dependency freeze released that morning once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2607; responder rota entry 33.

### Remediation review 070 - telemetry-hub
Detection replayed the original signature against this group before containment once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2610; responder rota entry 34.

### Remediation review 071 - ledger-api
The group was pulled forward after an adjacent group completed early once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2613; responder rota entry 35.

### Remediation review 072 - edge-cache
An owner handover moved this group to a second responder mid-window once an intake mis-tag against a sibling group had been corrected Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2616; responder rota entry 36.

### Remediation review 073 - edge-gateway
Responders confirmed the host was isolated before the sweep began despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2619; responder rota entry 37.

### Remediation review 074 - payments-core
Triage recorded the bundle as proposed by the on-call responder despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2622; responder rota entry 1.

### Remediation review 075 - identity-store
The asset owner acknowledged the containment notice inside the agreed window despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2625; responder rota entry 2.

### Remediation review 076 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2628; responder rota entry 3.

### Remediation review 077 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2631; responder rota entry 4.

### Remediation review 078 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2634; responder rota entry 5.

### Remediation review 079 - search-index
Containment tooling reported the group reachable at the start of the window despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2637; responder rota entry 6.

### Remediation review 080 - metrics-sink
A responder walked the runbook for this group with the platform on-call despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2640; responder rota entry 7.

### Remediation review 081 - queue-broker
The wave was staged behind a dependency freeze released that morning despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2643; responder rota entry 8.

### Remediation review 082 - config-store
Detection replayed the original signature against this group before containment despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2646; responder rota entry 9.

### Remediation review 083 - cdn-origin
The group was pulled forward after an adjacent group completed early despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2649; responder rota entry 10.

### Remediation review 084 - auth-proxy
An owner handover moved this group to a second responder mid-window despite a transient API error in the sweep tooling that retried unattended Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2652; responder rota entry 11.

### Remediation review 085 - log-shipper
Responders confirmed the host was isolated before the sweep began after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2655; responder rota entry 12.

### Remediation review 086 - key-vault
Triage recorded the bundle as proposed by the on-call responder after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2658; responder rota entry 13.

### Remediation review 087 - report-render
The asset owner acknowledged the containment notice inside the agreed window after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2661; responder rota entry 14.

### Remediation review 088 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2664; responder rota entry 15.

### Remediation review 089 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2667; responder rota entry 16.

### Review entry 0005 — selection lane
> **Board proposal (2026-02-16 - SR-1914)** Dana: when the objective admits more than one optimal set, report ANY one of them — the selected set is not required to be canonical. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Thread archived; see the SR decision entries for anything affecting planner behavior.

## Governance Review Archive (2025-Q4 through 2026-Q2)
Routine entries are context only. SR-ticketed proposal and decision quotes embedded in the entries are the authoritative record for planner behavior.

### Remediation review 090 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2670; responder rota entry 17.

### Remediation review 091 - session-store
Containment tooling reported the group reachable at the start of the window after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2673; responder rota entry 18.

### Remediation review 092 - policy-engine
A responder walked the runbook for this group with the platform on-call after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2676; responder rota entry 19.

### Remediation review 093 - artifact-repo
The wave was staged behind a dependency freeze released that morning after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2679; responder rota entry 20.

### Remediation review 094 - telemetry-hub
Detection replayed the original signature against this group before containment after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2682; responder rota entry 21.

### Remediation review 095 - ledger-api
The group was pulled forward after an adjacent group completed early after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2685; responder rota entry 22.

### Remediation review 096 - edge-cache
An owner handover moved this group to a second responder mid-window after forensics retained a disk image under a separate retention policy Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2688; responder rota entry 23.

### Remediation review 097 - edge-gateway
Responders confirmed the host was isolated before the sweep began with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2691; responder rota entry 24.

### Remediation review 098 - payments-core
Triage recorded the bundle as proposed by the on-call responder with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2694; responder rota entry 25.

### Remediation review 099 - identity-store
The asset owner acknowledged the containment notice inside the agreed window with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2697; responder rota entry 26.

### Remediation review 100 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2700; responder rota entry 27.

### Remediation review 101 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2703; responder rota entry 28.

### Remediation review 102 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2706; responder rota entry 29.

### Remediation review 103 - search-index
Containment tooling reported the group reachable at the start of the window with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2709; responder rota entry 30.

### Remediation review 104 - metrics-sink
A responder walked the runbook for this group with the platform on-call with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2712; responder rota entry 31.

### Remediation review 105 - queue-broker
The wave was staged behind a dependency freeze released that morning with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2715; responder rota entry 32.

### Remediation review 106 - config-store
Detection replayed the original signature against this group before containment with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2718; responder rota entry 33.

### Remediation review 107 - cdn-origin
The group was pulled forward after an adjacent group completed early with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2721; responder rota entry 34.

### Remediation review 108 - auth-proxy
An owner handover moved this group to a second responder mid-window with one asset unreachable until its switch port was re-enabled Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2724; responder rota entry 35.

### Remediation review 109 - log-shipper
Responders confirmed the host was isolated before the sweep began following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2727; responder rota entry 36.

### Remediation review 110 - key-vault
Triage recorded the bundle as proposed by the on-call responder following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2730; responder rota entry 37.

### Review entry 0021 — intake lane
> **Board decision (2026-04-09 - SR-2104)** Priya: bundle severities are valid in the range 1..7; assets are kept in input order without deduplication. *(Revised — see the 2026-05 review.)*
Shift lead logged a routine intake observation; rotation swap approved, no parameter change.

### Remediation review 111 - report-render
The asset owner acknowledged the containment notice inside the agreed window following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2733; responder rota entry 1.

### Remediation review 112 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2736; responder rota entry 2.

### Remediation review 113 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2739; responder rota entry 3.

### Remediation review 114 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2742; responder rota entry 4.

### Remediation review 115 - session-store
Containment tooling reported the group reachable at the start of the window following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2745; responder rota entry 5.

### Remediation review 116 - policy-engine
A responder walked the runbook for this group with the platform on-call following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2748; responder rota entry 6.

### Remediation review 117 - artifact-repo
The wave was staged behind a dependency freeze released that morning following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2751; responder rota entry 7.

### Remediation review 118 - telemetry-hub
Detection replayed the original signature against this group before containment following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2754; responder rota entry 8.

### Remediation review 119 - ledger-api
The group was pulled forward after an adjacent group completed early following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2757; responder rota entry 9.

### Remediation review 120 - edge-cache
An owner handover moved this group to a second responder mid-window following a short pause while the change freeze exception was confirmed Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2760; responder rota entry 10.

### Remediation review 121 - edge-gateway
Responders confirmed the host was isolated before the sweep began after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2763; responder rota entry 11.

### Remediation review 122 - payments-core
Triage recorded the bundle as proposed by the on-call responder after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2766; responder rota entry 12.

### Remediation review 123 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2769; responder rota entry 13.

### Remediation review 124 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2772; responder rota entry 14.

### Remediation review 125 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2775; responder rota entry 15.

### Remediation review 126 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2778; responder rota entry 16.

### Remediation review 127 - search-index
Containment tooling reported the group reachable at the start of the window after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2781; responder rota entry 17.

### Remediation review 128 - metrics-sink
A responder walked the runbook for this group with the platform on-call after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2784; responder rota entry 18.

### Remediation review 129 - queue-broker
The wave was staged behind a dependency freeze released that morning after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2787; responder rota entry 19.

### Remediation review 130 - config-store
Detection replayed the original signature against this group before containment after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2790; responder rota entry 20.

### Remediation review 131 - cdn-origin
The group was pulled forward after an adjacent group completed early after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2793; responder rota entry 21.

### Review entry 0022 — selection lane
> **Board decision (2026-04-12 - SR-2108)** Priya: among optimal sets, prefer the one built by taking eligible bundles in ascending id order (a greedy smallest-id-first construction). *(Revised — see the 2026-05 review.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Remediation review 132 - auth-proxy
An owner handover moved this group to a second responder mid-window after the inventory source disagreement over hostname casing was settled Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2796; responder rota entry 22.

### Remediation review 133 - log-shipper
Responders confirmed the host was isolated before the sweep began with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2799; responder rota entry 23.

### Remediation review 134 - key-vault
Triage recorded the bundle as proposed by the on-call responder with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2802; responder rota entry 24.

### Remediation review 135 - report-render
The asset owner acknowledged the containment notice inside the agreed window with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2805; responder rota entry 25.

### Remediation review 136 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2808; responder rota entry 26.

### Remediation review 137 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2811; responder rota entry 27.

### Remediation review 138 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2814; responder rota entry 28.

### Remediation review 139 - session-store
Containment tooling reported the group reachable at the start of the window with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
No plan semantics changed in this entry. Wave reference 2817; responder rota entry 29.

### Remediation review 140 - policy-engine
A responder walked the runbook for this group with the platform on-call with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Parameters remain as approved by the board. Wave reference 2820; responder rota entry 30.

### Remediation review 141 - artifact-repo
The wave was staged behind a dependency freeze released that morning with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Logged for the incident record; no planning impact. Wave reference 2823; responder rota entry 31.

### Remediation review 142 - telemetry-hub
Detection replayed the original signature against this group before containment with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Closed with no action required. Wave reference 2826; responder rota entry 32.

### Remediation review 143 - ledger-api
The group was pulled forward after an adjacent group completed early with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Referred to the tooling backlog. Wave reference 2829; responder rota entry 33.

### Remediation review 144 - edge-cache
An owner handover moved this group to a second responder mid-window with the blast-radius estimate revised down once telemetry was reviewed Post-sweep verification cleared the group on the first pass.
Filed for the quarterly review. Wave reference 2832; responder rota entry 34.

### Remediation review 145 - edge-gateway
Responders confirmed the host was isolated before the sweep began and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2835; responder rota entry 35.

### Remediation review 146 - payments-core
Triage recorded the bundle as proposed by the on-call responder and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2838; responder rota entry 36.

### Remediation review 147 - identity-store
The asset owner acknowledged the containment notice inside the agreed window and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2841; responder rota entry 37.

### Remediation review 148 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2844; responder rota entry 1.

### Remediation review 149 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2847; responder rota entry 2.

### Remediation review 150 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2850; responder rota entry 3.

### Remediation review 151 - search-index
Containment tooling reported the group reachable at the start of the window and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2853; responder rota entry 4.

### Remediation review 152 - metrics-sink
A responder walked the runbook for this group with the platform on-call and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2856; responder rota entry 5.

### Review entry 0023 — residual lane
> **Board decision (2026-04-16 - SR-2112)** Dana: the residual severity is the best packing over the bundles whose assets are entirely disjoint from the selected set's assets. *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Remediation review 153 - queue-broker
The wave was staged behind a dependency freeze released that morning and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2859; responder rota entry 6.

### Remediation review 154 - config-store
Detection replayed the original signature against this group before containment and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2862; responder rota entry 7.

### Remediation review 155 - cdn-origin
The group was pulled forward after an adjacent group completed early and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2865; responder rota entry 8.

### Remediation review 156 - auth-proxy
An owner handover moved this group to a second responder mid-window and no further lateral movement was observed on the segment afterwards The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2868; responder rota entry 9.

### Remediation review 157 - log-shipper
Responders confirmed the host was isolated before the sweep began though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2871; responder rota entry 10.

### Remediation review 158 - key-vault
Triage recorded the bundle as proposed by the on-call responder though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2874; responder rota entry 11.

### Remediation review 159 - report-render
The asset owner acknowledged the containment notice inside the agreed window though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2877; responder rota entry 12.

### Remediation review 160 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2880; responder rota entry 13.

### Remediation review 161 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2883; responder rota entry 14.

### Remediation review 162 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2886; responder rota entry 15.

### Remediation review 163 - session-store
Containment tooling reported the group reachable at the start of the window though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2889; responder rota entry 16.

### Remediation review 164 - policy-engine
A responder walked the runbook for this group with the platform on-call though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2892; responder rota entry 17.

### Remediation review 165 - artifact-repo
The wave was staged behind a dependency freeze released that morning though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2895; responder rota entry 18.

### Remediation review 166 - telemetry-hub
Detection replayed the original signature against this group before containment though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2898; responder rota entry 19.

### Remediation review 167 - ledger-api
The group was pulled forward after an adjacent group completed early though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2901; responder rota entry 20.

### Remediation review 168 - edge-cache
An owner handover moved this group to a second responder mid-window though a duplicate proposal from a second responder was withdrawn at handover The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2904; responder rota entry 21.

### Remediation review 169 - edge-gateway
Responders confirmed the host was isolated before the sweep began after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2907; responder rota entry 22.

### Remediation review 170 - payments-core
Triage recorded the bundle as proposed by the on-call responder after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2910; responder rota entry 23.

### Remediation review 171 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2913; responder rota entry 24.

### Remediation review 172 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2916; responder rota entry 25.

### Remediation review 173 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2919; responder rota entry 26.

### Review entry 0024 — scoring lane
> **Board decision (2026-04-18 - SR-2116)** Priya: severity tiers — a bundle is `critical` when its severity is 8 or 9, `major` when 5 to 7, and `minor` when 4 or below. *(Revised — see the 2026-05 review.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Remediation review 174 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2922; responder rota entry 27.

### Remediation review 175 - search-index
Containment tooling reported the group reachable at the start of the window after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2925; responder rota entry 28.

### Remediation review 176 - metrics-sink
A responder walked the runbook for this group with the platform on-call after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2928; responder rota entry 29.

### Remediation review 177 - queue-broker
The wave was staged behind a dependency freeze released that morning after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2931; responder rota entry 30.

### Remediation review 178 - config-store
Detection replayed the original signature against this group before containment after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2934; responder rota entry 31.

### Remediation review 179 - cdn-origin
The group was pulled forward after an adjacent group completed early after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2937; responder rota entry 32.

### Remediation review 180 - auth-proxy
An owner handover moved this group to a second responder mid-window after a brief reconnection attempt that never reached the control plane The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2940; responder rota entry 33.

### Remediation review 181 - log-shipper
Responders confirmed the host was isolated before the sweep began with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2943; responder rota entry 34.

### Remediation review 182 - key-vault
Triage recorded the bundle as proposed by the on-call responder with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2946; responder rota entry 35.

### Remediation review 183 - report-render
The asset owner acknowledged the containment notice inside the agreed window with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2949; responder rota entry 36.

### Remediation review 184 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2952; responder rota entry 37.

### Remediation review 185 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2955; responder rota entry 1.

### Remediation review 186 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2958; responder rota entry 2.

### Remediation review 187 - session-store
Containment tooling reported the group reachable at the start of the window with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2961; responder rota entry 3.

### Remediation review 188 - policy-engine
A responder walked the runbook for this group with the platform on-call with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2964; responder rota entry 4.

### Remediation review 189 - artifact-repo
The wave was staged behind a dependency freeze released that morning with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2967; responder rota entry 5.

### Remediation review 190 - telemetry-hub
Detection replayed the original signature against this group before containment with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2970; responder rota entry 6.

### Remediation review 191 - ledger-api
The group was pulled forward after an adjacent group completed early with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2973; responder rota entry 7.

### Remediation review 192 - edge-cache
An owner handover moved this group to a second responder mid-window with two listed assets already rebuilt and therefore dropped from scope The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2976; responder rota entry 8.

### Remediation review 193 - edge-gateway
Responders confirmed the host was isolated before the sweep began while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2979; responder rota entry 9.

### Remediation review 194 - payments-core
Triage recorded the bundle as proposed by the on-call responder while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 2982; responder rota entry 10.

### Review entry 0025 — scoring lane
> **Board decision (2026-04-20 - SR-2118)** Priya: a bundle's asset pressure is `severity + asset_count`; `total_asset_pressure` sums it over canonical bundles and `max_asset_pressure` is the largest. *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Remediation review 195 - identity-store
The asset owner acknowledged the containment notice inside the agreed window while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 2985; responder rota entry 11.

### Remediation review 196 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 2988; responder rota entry 12.

### Remediation review 197 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 2991; responder rota entry 13.

### Remediation review 198 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 2994; responder rota entry 14.

### Remediation review 199 - search-index
Containment tooling reported the group reachable at the start of the window while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 2997; responder rota entry 15.

### Remediation review 200 - metrics-sink
A responder walked the runbook for this group with the platform on-call while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3000; responder rota entry 16.

### Remediation review 201 - queue-broker
The wave was staged behind a dependency freeze released that morning while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3003; responder rota entry 17.

### Remediation review 202 - config-store
Detection replayed the original signature against this group before containment while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3006; responder rota entry 18.

### Remediation review 203 - cdn-origin
The group was pulled forward after an adjacent group completed early while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3009; responder rota entry 19.

### Remediation review 204 - auth-proxy
An owner handover moved this group to a second responder mid-window while a credential rotation held the containment lock for part of the window The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3012; responder rota entry 20.

### Remediation review 205 - log-shipper
Responders confirmed the host was isolated before the sweep began once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3015; responder rota entry 21.

### Remediation review 206 - key-vault
Triage recorded the bundle as proposed by the on-call responder once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3018; responder rota entry 22.

### Remediation review 207 - report-render
The asset owner acknowledged the containment notice inside the agreed window once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3021; responder rota entry 23.

### Remediation review 208 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3024; responder rota entry 24.

### Remediation review 209 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3027; responder rota entry 25.

### Remediation review 210 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3030; responder rota entry 26.

### Remediation review 211 - session-store
Containment tooling reported the group reachable at the start of the window once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3033; responder rota entry 27.

### Remediation review 212 - policy-engine
A responder walked the runbook for this group with the platform on-call once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3036; responder rota entry 28.

### Remediation review 213 - artifact-repo
The wave was staged behind a dependency freeze released that morning once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3039; responder rota entry 29.

### Remediation review 214 - telemetry-hub
Detection replayed the original signature against this group before containment once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3042; responder rota entry 30.

### Remediation review 215 - ledger-api
The group was pulled forward after an adjacent group completed early once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3045; responder rota entry 31.

### Review entry 0026 — scoring lane
> **Board decision (2026-04-22 - SR-2120)** Dana: `containment_score` = sum over the contained set of `severity * 3 + asset_count`, with no divisor. *(Revised — see the 2026-05 review.)*
Thread archived; see the SR decision entries for anything affecting planner behavior.

### Remediation review 216 - edge-cache
An owner handover moved this group to a second responder mid-window once an intake mis-tag against a sibling group had been corrected The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3048; responder rota entry 32.

### Remediation review 217 - edge-gateway
Responders confirmed the host was isolated before the sweep began despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3051; responder rota entry 33.

### Remediation review 218 - payments-core
Triage recorded the bundle as proposed by the on-call responder despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3054; responder rota entry 34.

### Remediation review 219 - identity-store
The asset owner acknowledged the containment notice inside the agreed window despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3057; responder rota entry 35.

### Remediation review 220 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3060; responder rota entry 36.

### Remediation review 221 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3063; responder rota entry 37.

### Remediation review 222 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3066; responder rota entry 1.

### Remediation review 223 - search-index
Containment tooling reported the group reachable at the start of the window despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3069; responder rota entry 2.

### Remediation review 224 - metrics-sink
A responder walked the runbook for this group with the platform on-call despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3072; responder rota entry 3.

### Remediation review 225 - queue-broker
The wave was staged behind a dependency freeze released that morning despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3075; responder rota entry 4.

### Remediation review 226 - config-store
Detection replayed the original signature against this group before containment despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3078; responder rota entry 5.

### Remediation review 227 - cdn-origin
The group was pulled forward after an adjacent group completed early despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3081; responder rota entry 6.

### Remediation review 228 - auth-proxy
An owner handover moved this group to a second responder mid-window despite a transient API error in the sweep tooling that retried unattended The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3084; responder rota entry 7.

### Remediation review 229 - log-shipper
Responders confirmed the host was isolated before the sweep began after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3087; responder rota entry 8.

### Remediation review 230 - key-vault
Triage recorded the bundle as proposed by the on-call responder after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3090; responder rota entry 9.

### Remediation review 231 - report-render
The asset owner acknowledged the containment notice inside the agreed window after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3093; responder rota entry 10.

### Remediation review 232 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3096; responder rota entry 11.

### Remediation review 233 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3099; responder rota entry 12.

### Remediation review 234 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3102; responder rota entry 13.

### Remediation review 235 - session-store
Containment tooling reported the group reachable at the start of the window after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3105; responder rota entry 14.

### Remediation review 236 - policy-engine
A responder walked the runbook for this group with the platform on-call after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3108; responder rota entry 15.

### Review entry 0027 — scoring lane
> **Board decision (2026-04-24 - SR-2122)** Dana: `coverage_permille` reports coverage as a percent — `contained_asset_count * 100 // asset_count` (0 when asset_count is 0). *(Revised — see the 2026-05 review.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Remediation review 237 - artifact-repo
The wave was staged behind a dependency freeze released that morning after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3111; responder rota entry 16.

### Remediation review 238 - telemetry-hub
Detection replayed the original signature against this group before containment after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3114; responder rota entry 17.

### Remediation review 239 - ledger-api
The group was pulled forward after an adjacent group completed early after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3117; responder rota entry 18.

### Remediation review 240 - edge-cache
An owner handover moved this group to a second responder mid-window after forensics retained a disk image under a separate retention policy The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3120; responder rota entry 19.

### Remediation review 241 - edge-gateway
Responders confirmed the host was isolated before the sweep began with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3123; responder rota entry 20.

### Remediation review 242 - payments-core
Triage recorded the bundle as proposed by the on-call responder with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3126; responder rota entry 21.

### Remediation review 243 - identity-store
The asset owner acknowledged the containment notice inside the agreed window with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3129; responder rota entry 22.

### Remediation review 244 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3132; responder rota entry 23.

### Remediation review 245 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3135; responder rota entry 24.

### Remediation review 246 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3138; responder rota entry 25.

### Remediation review 247 - search-index
Containment tooling reported the group reachable at the start of the window with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3141; responder rota entry 26.

### Remediation review 248 - metrics-sink
A responder walked the runbook for this group with the platform on-call with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3144; responder rota entry 27.

### Remediation review 249 - queue-broker
The wave was staged behind a dependency freeze released that morning with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3147; responder rota entry 28.

### Remediation review 250 - config-store
Detection replayed the original signature against this group before containment with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3150; responder rota entry 29.

### Remediation review 251 - cdn-origin
The group was pulled forward after an adjacent group completed early with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3153; responder rota entry 30.

### Remediation review 252 - auth-proxy
An owner handover moved this group to a second responder mid-window with one asset unreachable until its switch port was re-enabled The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3156; responder rota entry 31.

### Remediation review 253 - log-shipper
Responders confirmed the host was isolated before the sweep began following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3159; responder rota entry 32.

### Remediation review 254 - key-vault
Triage recorded the bundle as proposed by the on-call responder following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3162; responder rota entry 33.

### Remediation review 255 - report-render
The asset owner acknowledged the containment notice inside the agreed window following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3165; responder rota entry 34.

### Remediation review 256 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3168; responder rota entry 35.

### Remediation review 257 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3171; responder rota entry 36.

### Review entry 0028 — scoring lane
> **Board decision (2026-04-28 - SR-2124)** Dana: `residual_pressure` is the sum of asset pressure over ALL canonical bundles (contained and not). *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Remediation review 258 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3174; responder rota entry 37.

### Remediation review 259 - session-store
Containment tooling reported the group reachable at the start of the window following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3177; responder rota entry 1.

### Remediation review 260 - policy-engine
A responder walked the runbook for this group with the platform on-call following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3180; responder rota entry 2.

### Remediation review 261 - artifact-repo
The wave was staged behind a dependency freeze released that morning following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3183; responder rota entry 3.

### Remediation review 262 - telemetry-hub
Detection replayed the original signature against this group before containment following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3186; responder rota entry 4.

### Remediation review 263 - ledger-api
The group was pulled forward after an adjacent group completed early following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3189; responder rota entry 5.

### Remediation review 264 - edge-cache
An owner handover moved this group to a second responder mid-window following a short pause while the change freeze exception was confirmed The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3192; responder rota entry 6.

### Remediation review 265 - edge-gateway
Responders confirmed the host was isolated before the sweep began after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3195; responder rota entry 7.

### Remediation review 266 - payments-core
Triage recorded the bundle as proposed by the on-call responder after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3198; responder rota entry 8.

### Remediation review 267 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3201; responder rota entry 9.

### Remediation review 268 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3204; responder rota entry 10.

### Remediation review 269 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3207; responder rota entry 11.

### Remediation review 270 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3210; responder rota entry 12.

### Remediation review 271 - search-index
Containment tooling reported the group reachable at the start of the window after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3213; responder rota entry 13.

### Remediation review 272 - metrics-sink
A responder walked the runbook for this group with the platform on-call after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3216; responder rota entry 14.

### Remediation review 273 - queue-broker
The wave was staged behind a dependency freeze released that morning after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3219; responder rota entry 15.

### Remediation review 274 - config-store
Detection replayed the original signature against this group before containment after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3222; responder rota entry 16.

### Remediation review 275 - cdn-origin
The group was pulled forward after an adjacent group completed early after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3225; responder rota entry 17.

### Remediation review 276 - auth-proxy
An owner handover moved this group to a second responder mid-window after the inventory source disagreement over hostname casing was settled The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3228; responder rota entry 18.

### Remediation review 277 - log-shipper
Responders confirmed the host was isolated before the sweep began with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3231; responder rota entry 19.

### Remediation review 278 - key-vault
Triage recorded the bundle as proposed by the on-call responder with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3234; responder rota entry 20.

### Review entry 0031 — canonicalization lane
> **Board decision (2026-05-03 - SR-2201)** Ilya: bundle canonicalization — drop any bundle whose severity is outside the inclusive range 1..9, and drop any bundle with an empty asset list. Within a bundle, deduplicate the asset ids and sort them ascending. When the same bundle id appears more than once, keep the single occurrence with the MAXIMUM severity. The canonical bundle list is ordered by bundle id ascending. This supersedes SR-1902, SR-1905 and SR-2104.

### Remediation review 279 - report-render
The asset owner acknowledged the containment notice inside the agreed window with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3237; responder rota entry 21.

### Remediation review 280 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3240; responder rota entry 22.

### Remediation review 281 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3243; responder rota entry 23.

### Remediation review 282 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3246; responder rota entry 24.

### Remediation review 283 - session-store
Containment tooling reported the group reachable at the start of the window with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
No plan semantics changed in this entry. Wave reference 3249; responder rota entry 25.

### Remediation review 284 - policy-engine
A responder walked the runbook for this group with the platform on-call with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Parameters remain as approved by the board. Wave reference 3252; responder rota entry 26.

### Remediation review 285 - artifact-repo
The wave was staged behind a dependency freeze released that morning with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Logged for the incident record; no planning impact. Wave reference 3255; responder rota entry 27.

### Remediation review 286 - telemetry-hub
Detection replayed the original signature against this group before containment with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Closed with no action required. Wave reference 3258; responder rota entry 28.

### Remediation review 287 - ledger-api
The group was pulled forward after an adjacent group completed early with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Referred to the tooling backlog. Wave reference 3261; responder rota entry 29.

### Remediation review 288 - edge-cache
An owner handover moved this group to a second responder mid-window with the blast-radius estimate revised down once telemetry was reviewed The remainder was queued for the following maintenance window.
Filed for the quarterly review. Wave reference 3264; responder rota entry 30.

### Remediation review 289 - edge-gateway
Responders confirmed the host was isolated before the sweep began and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3267; responder rota entry 31.

### Remediation review 290 - payments-core
Triage recorded the bundle as proposed by the on-call responder and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3270; responder rota entry 32.

### Remediation review 291 - identity-store
The asset owner acknowledged the containment notice inside the agreed window and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3273; responder rota entry 33.

### Remediation review 292 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3276; responder rota entry 34.

### Remediation review 293 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3279; responder rota entry 35.

### Remediation review 294 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3282; responder rota entry 36.

### Remediation review 295 - search-index
Containment tooling reported the group reachable at the start of the window and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3285; responder rota entry 37.

### Remediation review 296 - metrics-sink
A responder walked the runbook for this group with the platform on-call and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3288; responder rota entry 1.

### Remediation review 297 - queue-broker
The wave was staged behind a dependency freeze released that morning and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3291; responder rota entry 2.

### Remediation review 298 - config-store
Detection replayed the original signature against this group before containment and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3294; responder rota entry 3.

### Remediation review 299 - cdn-origin
The group was pulled forward after an adjacent group completed early and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3297; responder rota entry 4.

### Review entry 0032 — objective lane
> **Board decision (2026-05-05 - SR-2203)** Ilya: the contained severity `max_contained_severity` is the exact maximum total severity of a set of pairwise ASSET-DISJOINT bundles — the maximum-weight asset-disjoint packing. It is NOT the sum of all bundle severities (bundles contend for assets) and NOT a greedy highest-severity-first selection (greedy is not optimal). The empty set scores 0. This supersedes SR-1908 and SR-1911.

### Remediation review 300 - auth-proxy
An owner handover moved this group to a second responder mid-window and no further lateral movement was observed on the segment afterwards Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3300; responder rota entry 5.

### Remediation review 301 - log-shipper
Responders confirmed the host was isolated before the sweep began though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3303; responder rota entry 6.

### Remediation review 302 - key-vault
Triage recorded the bundle as proposed by the on-call responder though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3306; responder rota entry 7.

### Remediation review 303 - report-render
The asset owner acknowledged the containment notice inside the agreed window though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3309; responder rota entry 8.

### Remediation review 304 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3312; responder rota entry 9.

### Remediation review 305 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3315; responder rota entry 10.

### Remediation review 306 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3318; responder rota entry 11.

### Remediation review 307 - session-store
Containment tooling reported the group reachable at the start of the window though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3321; responder rota entry 12.

### Remediation review 308 - policy-engine
A responder walked the runbook for this group with the platform on-call though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3324; responder rota entry 13.

### Remediation review 309 - artifact-repo
The wave was staged behind a dependency freeze released that morning though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3327; responder rota entry 14.

### Remediation review 310 - telemetry-hub
Detection replayed the original signature against this group before containment though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3330; responder rota entry 15.

### Remediation review 311 - ledger-api
The group was pulled forward after an adjacent group completed early though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3333; responder rota entry 16.

### Remediation review 312 - edge-cache
An owner handover moved this group to a second responder mid-window though a duplicate proposal from a second responder was withdrawn at handover Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3336; responder rota entry 17.

### Remediation review 313 - edge-gateway
Responders confirmed the host was isolated before the sweep began after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3339; responder rota entry 18.

### Remediation review 314 - payments-core
Triage recorded the bundle as proposed by the on-call responder after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3342; responder rota entry 19.

### Remediation review 315 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3345; responder rota entry 20.

### Remediation review 316 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3348; responder rota entry 21.

### Remediation review 317 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3351; responder rota entry 22.

### Remediation review 318 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3354; responder rota entry 23.

### Remediation review 319 - search-index
Containment tooling reported the group reachable at the start of the window after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3357; responder rota entry 24.

### Remediation review 320 - metrics-sink
A responder walked the runbook for this group with the platform on-call after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3360; responder rota entry 25.

### Review entry 0033 — selection lane
> **Board decision (2026-05-08 - SR-2205)** Marta: the contained set is selected deterministically. Among ALL pairwise asset-disjoint bundle sets whose summed severity equals `max_contained_severity`, choose the one whose bundle ids, sorted ascending, form the lexicographically smallest tuple (compared element by element as strings). This is a tie-break over whole optimal sets, not a greedy smallest-id construction: consider every set that attains the maximum, then take the lexicographically least. `contained_bundle_ids` lists that set's ids ascending. This supersedes SR-1914 and SR-2108.

### Remediation review 321 - queue-broker
The wave was staged behind a dependency freeze released that morning after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3363; responder rota entry 26.

### Remediation review 322 - config-store
Detection replayed the original signature against this group before containment after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3366; responder rota entry 27.

### Remediation review 323 - cdn-origin
The group was pulled forward after an adjacent group completed early after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3369; responder rota entry 28.

### Remediation review 324 - auth-proxy
An owner handover moved this group to a second responder mid-window after a brief reconnection attempt that never reached the control plane Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3372; responder rota entry 29.

### Remediation review 325 - log-shipper
Responders confirmed the host was isolated before the sweep began with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3375; responder rota entry 30.

### Remediation review 326 - key-vault
Triage recorded the bundle as proposed by the on-call responder with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3378; responder rota entry 31.

### Remediation review 327 - report-render
The asset owner acknowledged the containment notice inside the agreed window with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3381; responder rota entry 32.

### Remediation review 328 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3384; responder rota entry 33.

### Remediation review 329 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3387; responder rota entry 34.

### Remediation review 330 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3390; responder rota entry 35.

### Remediation review 331 - session-store
Containment tooling reported the group reachable at the start of the window with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3393; responder rota entry 36.

### Remediation review 332 - policy-engine
A responder walked the runbook for this group with the platform on-call with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3396; responder rota entry 37.

### Remediation review 333 - artifact-repo
The wave was staged behind a dependency freeze released that morning with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3399; responder rota entry 1.

### Remediation review 334 - telemetry-hub
Detection replayed the original signature against this group before containment with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3402; responder rota entry 2.

### Remediation review 335 - ledger-api
The group was pulled forward after an adjacent group completed early with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3405; responder rota entry 3.

### Remediation review 336 - edge-cache
An owner handover moved this group to a second responder mid-window with two listed assets already rebuilt and therefore dropped from scope Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3408; responder rota entry 4.

### Remediation review 337 - edge-gateway
Responders confirmed the host was isolated before the sweep began while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3411; responder rota entry 5.

### Remediation review 338 - payments-core
Triage recorded the bundle as proposed by the on-call responder while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3414; responder rota entry 6.

### Remediation review 339 - identity-store
The asset owner acknowledged the containment notice inside the agreed window while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3417; responder rota entry 7.

### Remediation review 340 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3420; responder rota entry 8.

### Remediation review 341 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3423; responder rota entry 9.

### Review entry 0034 — residual lane
> **Board decision (2026-05-10 - SR-2207)** Marta: the residual packing re-runs the identical maximum-weight asset-disjoint objective over only the canonical bundles that are NOT in the contained set (identified by bundle id); `residual_contained_severity` is that packing's value (0 if none remain). The bundles that lost the tie-break contend among themselves, so this is a genuine second packing — it is NOT restricted to bundles asset-disjoint from the selected set. This supersedes SR-2112.

### Remediation review 342 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3426; responder rota entry 10.

### Remediation review 343 - search-index
Containment tooling reported the group reachable at the start of the window while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3429; responder rota entry 11.

### Remediation review 344 - metrics-sink
A responder walked the runbook for this group with the platform on-call while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3432; responder rota entry 12.

### Remediation review 345 - queue-broker
The wave was staged behind a dependency freeze released that morning while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3435; responder rota entry 13.

### Remediation review 346 - config-store
Detection replayed the original signature against this group before containment while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3438; responder rota entry 14.

### Remediation review 347 - cdn-origin
The group was pulled forward after an adjacent group completed early while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3441; responder rota entry 15.

### Remediation review 348 - auth-proxy
An owner handover moved this group to a second responder mid-window while a credential rotation held the containment lock for part of the window Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3444; responder rota entry 16.

### Remediation review 349 - log-shipper
Responders confirmed the host was isolated before the sweep began once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3447; responder rota entry 17.

### Remediation review 350 - key-vault
Triage recorded the bundle as proposed by the on-call responder once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3450; responder rota entry 18.

### Remediation review 351 - report-render
The asset owner acknowledged the containment notice inside the agreed window once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3453; responder rota entry 19.

### Remediation review 352 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3456; responder rota entry 20.

### Remediation review 353 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3459; responder rota entry 21.

### Remediation review 354 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3462; responder rota entry 22.

### Remediation review 355 - session-store
Containment tooling reported the group reachable at the start of the window once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3465; responder rota entry 23.

### Remediation review 356 - policy-engine
A responder walked the runbook for this group with the platform on-call once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3468; responder rota entry 24.

### Remediation review 357 - artifact-repo
The wave was staged behind a dependency freeze released that morning once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3471; responder rota entry 25.

### Remediation review 358 - telemetry-hub
Detection replayed the original signature against this group before containment once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3474; responder rota entry 26.

### Remediation review 359 - ledger-api
The group was pulled forward after an adjacent group completed early once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3477; responder rota entry 27.

### Remediation review 360 - edge-cache
An owner handover moved this group to a second responder mid-window once an intake mis-tag against a sibling group had been corrected Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3480; responder rota entry 28.

### Remediation review 361 - edge-gateway
Responders confirmed the host was isolated before the sweep began despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3483; responder rota entry 29.

### Remediation review 362 - payments-core
Triage recorded the bundle as proposed by the on-call responder despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3486; responder rota entry 30.

### Review entry 0035 — scoring lane
> **Board decision (2026-05-12 - SR-2209)** Ilya: severity tiers — a bundle is `critical` when its severity is 7 or greater, `major` when 4 to 6 inclusive, and `minor` when 3 or below. `proposed_tier_counts` counts the canonical bundles in each tier; `contained_tier_counts` counts only the bundles in the contained set in each tier. This supersedes SR-2116.

### Remediation review 363 - identity-store
The asset owner acknowledged the containment notice inside the agreed window despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3489; responder rota entry 31.

### Remediation review 364 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3492; responder rota entry 32.

### Remediation review 365 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3495; responder rota entry 33.

### Remediation review 366 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3498; responder rota entry 34.

### Remediation review 367 - search-index
Containment tooling reported the group reachable at the start of the window despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3501; responder rota entry 35.

### Remediation review 368 - metrics-sink
A responder walked the runbook for this group with the platform on-call despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3504; responder rota entry 36.

### Remediation review 369 - queue-broker
The wave was staged behind a dependency freeze released that morning despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3507; responder rota entry 37.

### Remediation review 370 - config-store
Detection replayed the original signature against this group before containment despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3510; responder rota entry 1.

### Remediation review 371 - cdn-origin
The group was pulled forward after an adjacent group completed early despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3513; responder rota entry 2.

### Remediation review 372 - auth-proxy
An owner handover moved this group to a second responder mid-window despite a transient API error in the sweep tooling that retried unattended Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3516; responder rota entry 3.

### Remediation review 373 - log-shipper
Responders confirmed the host was isolated before the sweep began after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3519; responder rota entry 4.

### Remediation review 374 - key-vault
Triage recorded the bundle as proposed by the on-call responder after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3522; responder rota entry 5.

### Remediation review 375 - report-render
The asset owner acknowledged the containment notice inside the agreed window after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3525; responder rota entry 6.

### Remediation review 376 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3528; responder rota entry 7.

### Remediation review 377 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3531; responder rota entry 8.

### Remediation review 378 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3534; responder rota entry 9.

### Remediation review 379 - session-store
Containment tooling reported the group reachable at the start of the window after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3537; responder rota entry 10.

### Remediation review 380 - policy-engine
A responder walked the runbook for this group with the platform on-call after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3540; responder rota entry 11.

### Remediation review 381 - artifact-repo
The wave was staged behind a dependency freeze released that morning after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3543; responder rota entry 12.

### Remediation review 382 - telemetry-hub
Detection replayed the original signature against this group before containment after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3546; responder rota entry 13.

### Remediation review 383 - ledger-api
The group was pulled forward after an adjacent group completed early after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3549; responder rota entry 14.

### Review entry 0036 — scoring lane
> **Board decision (2026-05-13 - SR-2211)** Ilya: a bundle's asset pressure is the PRODUCT `severity * asset_count` (asset_count being the number of distinct locked assets after canonicalization). `total_asset_pressure` sums asset pressure over all canonical bundles; `max_asset_pressure` is the largest single value (0 if none). This supersedes SR-2118.

### Remediation review 384 - edge-cache
An owner handover moved this group to a second responder mid-window after forensics retained a disk image under a separate retention policy Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3552; responder rota entry 15.

### Remediation review 385 - edge-gateway
Responders confirmed the host was isolated before the sweep began with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3555; responder rota entry 16.

### Remediation review 386 - payments-core
Triage recorded the bundle as proposed by the on-call responder with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3558; responder rota entry 17.

### Remediation review 387 - identity-store
The asset owner acknowledged the containment notice inside the agreed window with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3561; responder rota entry 18.

### Remediation review 388 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3564; responder rota entry 19.

### Remediation review 389 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3567; responder rota entry 20.

### Remediation review 390 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3570; responder rota entry 21.

### Remediation review 391 - search-index
Containment tooling reported the group reachable at the start of the window with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3573; responder rota entry 22.

### Remediation review 392 - metrics-sink
A responder walked the runbook for this group with the platform on-call with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3576; responder rota entry 23.

### Remediation review 393 - queue-broker
The wave was staged behind a dependency freeze released that morning with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3579; responder rota entry 24.

### Remediation review 394 - config-store
Detection replayed the original signature against this group before containment with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3582; responder rota entry 25.

### Remediation review 395 - cdn-origin
The group was pulled forward after an adjacent group completed early with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3585; responder rota entry 26.

### Remediation review 396 - auth-proxy
An owner handover moved this group to a second responder mid-window with one asset unreachable until its switch port was re-enabled Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3588; responder rota entry 27.

### Remediation review 397 - log-shipper
Responders confirmed the host was isolated before the sweep began following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3591; responder rota entry 28.

### Remediation review 398 - key-vault
Triage recorded the bundle as proposed by the on-call responder following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3594; responder rota entry 29.

### Remediation review 399 - report-render
The asset owner acknowledged the containment notice inside the agreed window following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3597; responder rota entry 30.

### Remediation review 400 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3600; responder rota entry 31.

### Remediation review 401 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3603; responder rota entry 32.

### Remediation review 402 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3606; responder rota entry 33.

### Remediation review 403 - session-store
Containment tooling reported the group reachable at the start of the window following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3609; responder rota entry 34.

### Remediation review 404 - policy-engine
A responder walked the runbook for this group with the platform on-call following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3612; responder rota entry 35.

### Review entry 0037 — scoring lane
> **Board decision (2026-05-14 - SR-2213)** Marta: `containment_score` = sum over the bundles in the contained set of `(severity * 5 + asset_count * 2) // 3` — the weighted term is floored with integer division per bundle before summing. This supersedes SR-2120.

### Remediation review 405 - artifact-repo
The wave was staged behind a dependency freeze released that morning following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3615; responder rota entry 36.

### Remediation review 406 - telemetry-hub
Detection replayed the original signature against this group before containment following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3618; responder rota entry 37.

### Remediation review 407 - ledger-api
The group was pulled forward after an adjacent group completed early following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3621; responder rota entry 1.

### Remediation review 408 - edge-cache
An owner handover moved this group to a second responder mid-window following a short pause while the change freeze exception was confirmed Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3624; responder rota entry 2.

### Remediation review 409 - edge-gateway
Responders confirmed the host was isolated before the sweep began after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3627; responder rota entry 3.

### Remediation review 410 - payments-core
Triage recorded the bundle as proposed by the on-call responder after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3630; responder rota entry 4.

### Remediation review 411 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3633; responder rota entry 5.

### Remediation review 412 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3636; responder rota entry 6.

### Remediation review 413 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3639; responder rota entry 7.

### Remediation review 414 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3642; responder rota entry 8.

### Remediation review 415 - search-index
Containment tooling reported the group reachable at the start of the window after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3645; responder rota entry 9.

### Remediation review 416 - metrics-sink
A responder walked the runbook for this group with the platform on-call after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3648; responder rota entry 10.

### Remediation review 417 - queue-broker
The wave was staged behind a dependency freeze released that morning after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3651; responder rota entry 11.

### Remediation review 418 - config-store
Detection replayed the original signature against this group before containment after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3654; responder rota entry 12.

### Remediation review 419 - cdn-origin
The group was pulled forward after an adjacent group completed early after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3657; responder rota entry 13.

### Remediation review 420 - auth-proxy
An owner handover moved this group to a second responder mid-window after the inventory source disagreement over hostname casing was settled Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3660; responder rota entry 14.

### Remediation review 421 - log-shipper
Responders confirmed the host was isolated before the sweep began with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3663; responder rota entry 15.

### Remediation review 422 - key-vault
Triage recorded the bundle as proposed by the on-call responder with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3666; responder rota entry 16.

### Remediation review 423 - report-render
The asset owner acknowledged the containment notice inside the agreed window with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3669; responder rota entry 17.

### Remediation review 424 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3672; responder rota entry 18.

### Remediation review 425 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3675; responder rota entry 19.

### Review entry 0038 — scoring lane
> **Board decision (2026-05-15 - SR-2215)** Marta: `coverage_permille` = `contained_asset_count * 1000 // asset_count` (per-mille, not percent), and 0 when asset_count is 0. This supersedes SR-2122.

### Remediation review 426 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3678; responder rota entry 20.

### Remediation review 427 - session-store
Containment tooling reported the group reachable at the start of the window with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
No plan semantics changed in this entry. Wave reference 3681; responder rota entry 21.

### Remediation review 428 - policy-engine
A responder walked the runbook for this group with the platform on-call with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Parameters remain as approved by the board. Wave reference 3684; responder rota entry 22.

### Remediation review 429 - artifact-repo
The wave was staged behind a dependency freeze released that morning with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Logged for the incident record; no planning impact. Wave reference 3687; responder rota entry 23.

### Remediation review 430 - telemetry-hub
Detection replayed the original signature against this group before containment with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Closed with no action required. Wave reference 3690; responder rota entry 24.

### Remediation review 431 - ledger-api
The group was pulled forward after an adjacent group completed early with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Referred to the tooling backlog. Wave reference 3693; responder rota entry 25.

### Remediation review 432 - edge-cache
An owner handover moved this group to a second responder mid-window with the blast-radius estimate revised down once telemetry was reviewed Change advisory approved the action out-of-band given the active intrusion.
Filed for the quarterly review. Wave reference 3696; responder rota entry 26.

### Remediation review 433 - edge-gateway
Responders confirmed the host was isolated before the sweep began and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3699; responder rota entry 27.

### Remediation review 434 - payments-core
Triage recorded the bundle as proposed by the on-call responder and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3702; responder rota entry 28.

### Remediation review 435 - identity-store
The asset owner acknowledged the containment notice inside the agreed window and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3705; responder rota entry 29.

### Remediation review 436 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3708; responder rota entry 30.

### Remediation review 437 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3711; responder rota entry 31.

### Remediation review 438 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3714; responder rota entry 32.

### Remediation review 439 - search-index
Containment tooling reported the group reachable at the start of the window and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3717; responder rota entry 33.

### Remediation review 440 - metrics-sink
A responder walked the runbook for this group with the platform on-call and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3720; responder rota entry 34.

### Remediation review 441 - queue-broker
The wave was staged behind a dependency freeze released that morning and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3723; responder rota entry 35.

### Remediation review 442 - config-store
Detection replayed the original signature against this group before containment and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3726; responder rota entry 36.

### Remediation review 443 - cdn-origin
The group was pulled forward after an adjacent group completed early and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3729; responder rota entry 37.

### Remediation review 444 - auth-proxy
An owner handover moved this group to a second responder mid-window and no further lateral movement was observed on the segment afterwards An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3732; responder rota entry 1.

### Remediation review 445 - log-shipper
Responders confirmed the host was isolated before the sweep began though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3735; responder rota entry 2.

### Remediation review 446 - key-vault
Triage recorded the bundle as proposed by the on-call responder though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3738; responder rota entry 3.

### Review entry 0039 — scoring lane
> **Board decision (2026-05-16 - SR-2217)** Marta: `residual_pressure` is the sum of asset pressure over only the canonical bundles that are NOT in the contained set — the same complement used by the residual packing. This supersedes SR-2124.

### Remediation review 447 - report-render
The asset owner acknowledged the containment notice inside the agreed window though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3741; responder rota entry 4.

### Remediation review 448 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3744; responder rota entry 5.

### Remediation review 449 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3747; responder rota entry 6.

### Remediation review 450 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3750; responder rota entry 7.

### Remediation review 451 - session-store
Containment tooling reported the group reachable at the start of the window though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3753; responder rota entry 8.

### Remediation review 452 - policy-engine
A responder walked the runbook for this group with the platform on-call though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3756; responder rota entry 9.

### Remediation review 453 - artifact-repo
The wave was staged behind a dependency freeze released that morning though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3759; responder rota entry 10.

### Remediation review 454 - telemetry-hub
Detection replayed the original signature against this group before containment though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3762; responder rota entry 11.

### Remediation review 455 - ledger-api
The group was pulled forward after an adjacent group completed early though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3765; responder rota entry 12.

### Remediation review 456 - edge-cache
An owner handover moved this group to a second responder mid-window though a duplicate proposal from a second responder was withdrawn at handover An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3768; responder rota entry 13.

### Remediation review 457 - edge-gateway
Responders confirmed the host was isolated before the sweep began after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3771; responder rota entry 14.

### Remediation review 458 - payments-core
Triage recorded the bundle as proposed by the on-call responder after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3774; responder rota entry 15.

### Remediation review 459 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3777; responder rota entry 16.

### Remediation review 460 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3780; responder rota entry 17.

### Remediation review 461 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3783; responder rota entry 18.

### Remediation review 462 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3786; responder rota entry 19.

### Remediation review 463 - search-index
Containment tooling reported the group reachable at the start of the window after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3789; responder rota entry 20.

### Remediation review 464 - metrics-sink
A responder walked the runbook for this group with the platform on-call after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3792; responder rota entry 21.

### Remediation review 465 - queue-broker
The wave was staged behind a dependency freeze released that morning after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3795; responder rota entry 22.

### Remediation review 466 - config-store
Detection replayed the original signature against this group before containment after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3798; responder rota entry 23.

### Remediation review 467 - cdn-origin
The group was pulled forward after an adjacent group completed early after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3801; responder rota entry 24.

### Review entry 0026b — response-ledger lane
> **Board proposal (2026-02-19 - SR-1930)** Tomas: response-urgency ledger — process canonical bundles in id order; carry_in = max(previous carry_out - (shared_prev_assets * 5) // 2, 0) where shared_prev_assets is the asset overlap with the previous canonical bundle; urgency = asset_pressure + carry_in // 4; carry_out = min(carry_in + asset_pressure, 80); a bundle joins the critical response set when urgency >= 25. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*
Analysts should reconcile behavior questions against the SR decision entries rather than chat excerpts.

### Remediation review 468 - auth-proxy
An owner handover moved this group to a second responder mid-window after a brief reconnection attempt that never reached the control plane An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3804; responder rota entry 25.

### Remediation review 469 - log-shipper
Responders confirmed the host was isolated before the sweep began with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3807; responder rota entry 26.

### Remediation review 470 - key-vault
Triage recorded the bundle as proposed by the on-call responder with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3810; responder rota entry 27.

### Remediation review 471 - report-render
The asset owner acknowledged the containment notice inside the agreed window with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3813; responder rota entry 28.

### Remediation review 472 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3816; responder rota entry 29.

### Remediation review 473 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3819; responder rota entry 30.

### Remediation review 474 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3822; responder rota entry 31.

### Remediation review 475 - session-store
Containment tooling reported the group reachable at the start of the window with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3825; responder rota entry 32.

### Remediation review 476 - policy-engine
A responder walked the runbook for this group with the platform on-call with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3828; responder rota entry 33.

### Remediation review 477 - artifact-repo
The wave was staged behind a dependency freeze released that morning with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3831; responder rota entry 34.

### Remediation review 478 - telemetry-hub
Detection replayed the original signature against this group before containment with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3834; responder rota entry 35.

### Remediation review 479 - ledger-api
The group was pulled forward after an adjacent group completed early with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3837; responder rota entry 36.

### Remediation review 480 - edge-cache
An owner handover moved this group to a second responder mid-window with two listed assets already rebuilt and therefore dropped from scope An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3840; responder rota entry 37.

### Remediation review 481 - edge-gateway
Responders confirmed the host was isolated before the sweep began while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3843; responder rota entry 1.

### Remediation review 482 - payments-core
Triage recorded the bundle as proposed by the on-call responder while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3846; responder rota entry 2.

### Remediation review 483 - identity-store
The asset owner acknowledged the containment notice inside the agreed window while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3849; responder rota entry 3.

### Remediation review 484 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3852; responder rota entry 4.

### Remediation review 485 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3855; responder rota entry 5.

### Remediation review 486 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3858; responder rota entry 6.

### Remediation review 487 - search-index
Containment tooling reported the group reachable at the start of the window while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3861; responder rota entry 7.

### Remediation review 488 - metrics-sink
A responder walked the runbook for this group with the platform on-call while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3864; responder rota entry 8.

### Review entry 0029b — response-ledger lane
> **Board decision (2026-04-30 - SR-2126)** Priya: response-urgency ledger interim — carry_in = max(previous carry_out - (shared_prev_assets * 7) // 2, 0); urgency = asset_pressure + carry_in // 4; carry_out = min(carry_in + asset_pressure - asset_count // 2, 100); critical when urgency >= 28. *(Revised — see the 2026-05 review.)*
No planner semantics changed in this entry; parameters remain as approved by the board.

### Remediation review 489 - queue-broker
The wave was staged behind a dependency freeze released that morning while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3867; responder rota entry 9.

### Remediation review 490 - config-store
Detection replayed the original signature against this group before containment while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3870; responder rota entry 10.

### Remediation review 491 - cdn-origin
The group was pulled forward after an adjacent group completed early while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3873; responder rota entry 11.

### Remediation review 492 - auth-proxy
An owner handover moved this group to a second responder mid-window while a credential rotation held the containment lock for part of the window An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3876; responder rota entry 12.

### Remediation review 493 - log-shipper
Responders confirmed the host was isolated before the sweep began once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3879; responder rota entry 13.

### Remediation review 494 - key-vault
Triage recorded the bundle as proposed by the on-call responder once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3882; responder rota entry 14.

### Remediation review 495 - report-render
The asset owner acknowledged the containment notice inside the agreed window once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3885; responder rota entry 15.

### Remediation review 496 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3888; responder rota entry 16.

### Remediation review 497 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3891; responder rota entry 17.

### Remediation review 498 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3894; responder rota entry 18.

### Remediation review 499 - session-store
Containment tooling reported the group reachable at the start of the window once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3897; responder rota entry 19.

### Remediation review 500 - policy-engine
A responder walked the runbook for this group with the platform on-call once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3900; responder rota entry 20.

### Remediation review 501 - artifact-repo
The wave was staged behind a dependency freeze released that morning once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3903; responder rota entry 21.

### Remediation review 502 - telemetry-hub
Detection replayed the original signature against this group before containment once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3906; responder rota entry 22.

### Remediation review 503 - ledger-api
The group was pulled forward after an adjacent group completed early once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3909; responder rota entry 23.

### Remediation review 504 - edge-cache
An owner handover moved this group to a second responder mid-window once an intake mis-tag against a sibling group had been corrected An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3912; responder rota entry 24.

### Remediation review 505 - edge-gateway
Responders confirmed the host was isolated before the sweep began despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3915; responder rota entry 25.

### Remediation review 506 - payments-core
Triage recorded the bundle as proposed by the on-call responder despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3918; responder rota entry 26.

### Remediation review 507 - identity-store
The asset owner acknowledged the containment notice inside the agreed window despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3921; responder rota entry 27.

### Remediation review 508 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3924; responder rota entry 28.

### Remediation review 509 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3927; responder rota entry 29.

### Review entry 0040 — response-ledger lane
> **Board decision (2026-05-18 - SR-2219)** Marta: response-urgency ledger (final) — process canonical bundles in id order; carry starts at 0. For each bundle: shared_prev is the count of assets shared with the immediately-preceding canonical bundle (0 for the first); `carry_in = max(previous_carry_out - (shared_prev * 7) // 3, 0)`; `urgency = asset_pressure + ceil(carry_in / 5)` — the carry credit is divided by 5 and **rounded UP** (ceiling), not floored (asset_pressure = severity * n_assets per SR-2211, where n_assets is the number of assets THIS bundle locks, i.e. len(bundle.assets)); `carry_out = min(carry_in + asset_pressure - (n_assets // 2), 90)` — here **n_assets is the count of assets this bundle locks (len of its own asset list), NOT the global input asset_count**; a bundle is admitted to the critical response set when `urgency >= 30`. `critical_response_ids` are the admitted bundle ids sorted ascending; `critical_response_count` is their number; `max_urgency` is the maximum urgency over all canonical bundles. The `* 7`/`// 3` decay, the `// 5` carry credit, the 90 cap and the 30 threshold are final and revise SR-2126; this supersedes SR-1930. ROUNDING: carry_in // 5 = CEIL.

### Remediation review 510 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3930; responder rota entry 30.

### Remediation review 511 - search-index
Containment tooling reported the group reachable at the start of the window despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3933; responder rota entry 31.

### Remediation review 512 - metrics-sink
A responder walked the runbook for this group with the platform on-call despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3936; responder rota entry 32.

### Remediation review 513 - queue-broker
The wave was staged behind a dependency freeze released that morning despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3939; responder rota entry 33.

### Remediation review 514 - config-store
Detection replayed the original signature against this group before containment despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3942; responder rota entry 34.

### Remediation review 515 - cdn-origin
The group was pulled forward after an adjacent group completed early despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3945; responder rota entry 35.

### Remediation review 516 - auth-proxy
An owner handover moved this group to a second responder mid-window despite a transient API error in the sweep tooling that retried unattended An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3948; responder rota entry 36.

### Remediation review 517 - log-shipper
Responders confirmed the host was isolated before the sweep began after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3951; responder rota entry 37.

### Remediation review 518 - key-vault
Triage recorded the bundle as proposed by the on-call responder after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3954; responder rota entry 1.

### Remediation review 519 - report-render
The asset owner acknowledged the containment notice inside the agreed window after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3957; responder rota entry 2.

### Remediation review 520 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3960; responder rota entry 3.

### Remediation review 521 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3963; responder rota entry 4.

### Remediation review 522 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3966; responder rota entry 5.

### Remediation review 523 - session-store
Containment tooling reported the group reachable at the start of the window after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3969; responder rota entry 6.

### Remediation review 524 - policy-engine
A responder walked the runbook for this group with the platform on-call after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3972; responder rota entry 7.

### Remediation review 525 - artifact-repo
The wave was staged behind a dependency freeze released that morning after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3975; responder rota entry 8.

### Remediation review 526 - telemetry-hub
Detection replayed the original signature against this group before containment after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3978; responder rota entry 9.

### Remediation review 527 - ledger-api
The group was pulled forward after an adjacent group completed early after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3981; responder rota entry 10.

### Remediation review 528 - edge-cache
An owner handover moved this group to a second responder mid-window after forensics retained a disk image under a separate retention policy An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 3984; responder rota entry 11.

### Remediation review 529 - edge-gateway
Responders confirmed the host was isolated before the sweep began with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 3987; responder rota entry 12.

### Remediation review 530 - payments-core
Triage recorded the bundle as proposed by the on-call responder with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 3990; responder rota entry 13.

### Review entry 0710 — containment bench
> **Board draft (2026-03-05 - SR-1934)** Rao: response load — a contained bundle's response load is `severity * 3` and nothing else; every contained bundle joins the response wave, with no response_load floor and no class. *(Superseded — reversed in the 2026-05 review; see the matching decision.)*

### Remediation review 531 - identity-store
The asset owner acknowledged the containment notice inside the agreed window with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 3993; responder rota entry 14.

### Remediation review 532 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 3996; responder rota entry 15.

### Remediation review 533 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 3999; responder rota entry 16.

### Remediation review 534 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4002; responder rota entry 17.

### Remediation review 535 - search-index
Containment tooling reported the group reachable at the start of the window with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4005; responder rota entry 18.

### Remediation review 536 - metrics-sink
A responder walked the runbook for this group with the platform on-call with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4008; responder rota entry 19.

### Remediation review 537 - queue-broker
The wave was staged behind a dependency freeze released that morning with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4011; responder rota entry 20.

### Remediation review 538 - config-store
Detection replayed the original signature against this group before containment with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4014; responder rota entry 21.

### Remediation review 539 - cdn-origin
The group was pulled forward after an adjacent group completed early with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4017; responder rota entry 22.

### Remediation review 540 - auth-proxy
An owner handover moved this group to a second responder mid-window with one asset unreachable until its switch port was re-enabled An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4020; responder rota entry 23.

### Remediation review 541 - log-shipper
Responders confirmed the host was isolated before the sweep began following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4023; responder rota entry 24.

### Remediation review 542 - key-vault
Triage recorded the bundle as proposed by the on-call responder following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4026; responder rota entry 25.

### Remediation review 543 - report-render
The asset owner acknowledged the containment notice inside the agreed window following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4029; responder rota entry 26.

### Remediation review 544 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4032; responder rota entry 27.

### Remediation review 545 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4035; responder rota entry 28.

### Remediation review 546 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4038; responder rota entry 29.

### Remediation review 547 - session-store
Containment tooling reported the group reachable at the start of the window following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4041; responder rota entry 30.

### Remediation review 548 - policy-engine
A responder walked the runbook for this group with the platform on-call following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4044; responder rota entry 31.

### Remediation review 549 - artifact-repo
The wave was staged behind a dependency freeze released that morning following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4047; responder rota entry 32.

### Remediation review 550 - telemetry-hub
Detection replayed the original signature against this group before containment following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4050; responder rota entry 33.

### Remediation review 551 - ledger-api
The group was pulled forward after an adjacent group completed early following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4053; responder rota entry 34.

### Review entry 0712 — containment bench
> **Board interim (2026-04-18 - SR-2130)** Priya: response load interim — response load adds the exposure overlap a contained bundle inherits, halved with integer floor division, and subtracts nothing: `response_load = severity * 3 + exposure_overlap // 2`. Bundles join the response wave at `response_load >= 12` and carry one of TWO classes. *(Revised — see the 2026-05 review.)*

### Remediation review 552 - edge-cache
An owner handover moved this group to a second responder mid-window following a short pause while the change freeze exception was confirmed An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4056; responder rota entry 35.

### Remediation review 553 - edge-gateway
Responders confirmed the host was isolated before the sweep began after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4059; responder rota entry 36.

### Remediation review 554 - payments-core
Triage recorded the bundle as proposed by the on-call responder after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4062; responder rota entry 37.

### Remediation review 555 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4065; responder rota entry 1.

### Remediation review 556 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4068; responder rota entry 2.

### Remediation review 557 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4071; responder rota entry 3.

### Remediation review 558 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4074; responder rota entry 4.

### Remediation review 559 - search-index
Containment tooling reported the group reachable at the start of the window after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4077; responder rota entry 5.

### Remediation review 560 - metrics-sink
A responder walked the runbook for this group with the platform on-call after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4080; responder rota entry 6.

### Remediation review 561 - queue-broker
The wave was staged behind a dependency freeze released that morning after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4083; responder rota entry 7.

### Remediation review 562 - config-store
Detection replayed the original signature against this group before containment after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4086; responder rota entry 8.

### Remediation review 563 - cdn-origin
The group was pulled forward after an adjacent group completed early after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4089; responder rota entry 9.

### Remediation review 564 - auth-proxy
An owner handover moved this group to a second responder mid-window after the inventory source disagreement over hostname casing was settled An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4092; responder rota entry 10.

### Remediation review 565 - log-shipper
Responders confirmed the host was isolated before the sweep began with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4095; responder rota entry 11.

### Remediation review 566 - key-vault
Triage recorded the bundle as proposed by the on-call responder with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4098; responder rota entry 12.

### Remediation review 567 - report-render
The asset owner acknowledged the containment notice inside the agreed window with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4101; responder rota entry 13.

### Remediation review 568 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4104; responder rota entry 14.

### Remediation review 569 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4107; responder rota entry 15.

### Remediation review 570 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4110; responder rota entry 16.

### Remediation review 571 - session-store
Containment tooling reported the group reachable at the start of the window with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
No plan semantics changed in this entry. Wave reference 4113; responder rota entry 17.

### Remediation review 572 - policy-engine
A responder walked the runbook for this group with the platform on-call with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Parameters remain as approved by the board. Wave reference 4116; responder rota entry 18.

### Review entry 0714 — containment bench
> **Board decision (2026-05-19 - SR-2231)** Nadia: response load (final). Only bundles in the contained set join the response wave. A contained bundle's `exposure_overlap` is the total number of shared asset slots it has with the bundles that were NOT contained, counted across those bundles *(Revised on this point by SR-2241 (2026-05-23), which attributes each uncontained bundle to a single owning claimant; the unattributed multiplicity count described here no longer governs. The rest of this entry -- `exposing_bundle_count`, the effort formula and the wave floor -- is unchanged and still governs.)*, and `exposing_bundle_count` is how many uncontained bundles it shares at least one asset with. `total_exposure_overlap` sums `exposure_overlap` over the contained bundles. Effort is `max(severity * 3 + ceil(exposure_overlap / 2) - (n_assets // 2), 0)`: the conflict half is HALVED AND ROUNDED UP, revising the floored form in SR-2130, while the asset relief `n_assets // 2` is floored. In integer arithmetic ceil(x/2) is -(-x // 2). Here `n_assets` is the count of assets that bundle itself locks, not the global asset_count. This supersedes SR-1934 and SR-2130. ROUNDING: exposure_overlap // 2 = CEIL.

### Remediation review 573 - artifact-repo
The wave was staged behind a dependency freeze released that morning with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Logged for the incident record; no planning impact. Wave reference 4119; responder rota entry 19.

### Remediation review 574 - telemetry-hub
Detection replayed the original signature against this group before containment with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Closed with no action required. Wave reference 4122; responder rota entry 20.

### Remediation review 575 - ledger-api
The group was pulled forward after an adjacent group completed early with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Referred to the tooling backlog. Wave reference 4125; responder rota entry 21.

### Remediation review 576 - edge-cache
An owner handover moved this group to a second responder mid-window with the blast-radius estimate revised down once telemetry was reviewed An audit sample was pulled for the quarterly review and returned no findings.
Filed for the quarterly review. Wave reference 4128; responder rota entry 22.

### Remediation review 577 - edge-gateway
Responders confirmed the host was isolated before the sweep began and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4131; responder rota entry 23.

### Remediation review 578 - payments-core
Triage recorded the bundle as proposed by the on-call responder and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4134; responder rota entry 24.

### Remediation review 579 - identity-store
The asset owner acknowledged the containment notice inside the agreed window and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4137; responder rota entry 25.

### Remediation review 580 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4140; responder rota entry 26.

### Remediation review 581 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4143; responder rota entry 27.

### Remediation review 582 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4146; responder rota entry 28.

### Remediation review 583 - search-index
Containment tooling reported the group reachable at the start of the window and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4149; responder rota entry 29.

### Remediation review 584 - metrics-sink
A responder walked the runbook for this group with the platform on-call and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4152; responder rota entry 30.

### Remediation review 585 - queue-broker
The wave was staged behind a dependency freeze released that morning and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4155; responder rota entry 31.

### Remediation review 586 - config-store
Detection replayed the original signature against this group before containment and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4158; responder rota entry 32.

### Remediation review 587 - cdn-origin
The group was pulled forward after an adjacent group completed early and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4161; responder rota entry 33.

### Remediation review 588 - auth-proxy
An owner handover moved this group to a second responder mid-window and no further lateral movement was observed on the segment afterwards Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4164; responder rota entry 34.

### Remediation review 589 - log-shipper
Responders confirmed the host was isolated before the sweep began though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4167; responder rota entry 35.

### Remediation review 590 - key-vault
Triage recorded the bundle as proposed by the on-call responder though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4170; responder rota entry 36.

### Remediation review 591 - report-render
The asset owner acknowledged the containment notice inside the agreed window though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4173; responder rota entry 37.

### Remediation review 592 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4176; responder rota entry 1.

### Remediation review 593 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4179; responder rota entry 2.

### Review entry 0716 — containment bench
> **Board decision (2026-05-20 - SR-2233)** Nadia: response-wave admission and class (final). A contained bundle joins the response wave when `response_load >= 16`. Scheduled bundles carry exactly one of THREE classes, evaluated in clause order with the first match fixing the class: `immediate` when `response_load >= 27`; otherwise `urgent` when `response_load >= 21`, or `exposure_overlap >= 4`; otherwise `routine`. `response_wave_ids` are the response-wave bundles' ids sorted ascending. This supersedes the two-class scheme in SR-2130.

### Remediation review 594 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4182; responder rota entry 3.

### Remediation review 595 - session-store
Containment tooling reported the group reachable at the start of the window though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4185; responder rota entry 4.

### Remediation review 596 - policy-engine
A responder walked the runbook for this group with the platform on-call though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4188; responder rota entry 5.

### Remediation review 597 - artifact-repo
The wave was staged behind a dependency freeze released that morning though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4191; responder rota entry 6.

### Remediation review 598 - telemetry-hub
Detection replayed the original signature against this group before containment though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4194; responder rota entry 7.

### Remediation review 599 - ledger-api
The group was pulled forward after an adjacent group completed early though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4197; responder rota entry 8.

### Remediation review 600 - edge-cache
An owner handover moved this group to a second responder mid-window though a duplicate proposal from a second responder was withdrawn at handover Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4200; responder rota entry 9.

### Remediation review 601 - edge-gateway
Responders confirmed the host was isolated before the sweep began after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4203; responder rota entry 10.

### Remediation review 602 - payments-core
Triage recorded the bundle as proposed by the on-call responder after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4206; responder rota entry 11.

### Remediation review 603 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4209; responder rota entry 12.

### Remediation review 604 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4212; responder rota entry 13.

### Remediation review 605 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4215; responder rota entry 14.

### Remediation review 606 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4218; responder rota entry 15.

### Remediation review 607 - search-index
Containment tooling reported the group reachable at the start of the window after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4221; responder rota entry 16.

### Remediation review 608 - metrics-sink
A responder walked the runbook for this group with the platform on-call after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4224; responder rota entry 17.

### Remediation review 609 - queue-broker
The wave was staged behind a dependency freeze released that morning after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4227; responder rota entry 18.

### Remediation review 610 - config-store
Detection replayed the original signature against this group before containment after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4230; responder rota entry 19.

### Remediation review 611 - cdn-origin
The group was pulled forward after an adjacent group completed early after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4233; responder rota entry 20.

### Remediation review 612 - auth-proxy
An owner handover moved this group to a second responder mid-window after a brief reconnection attempt that never reached the control plane Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4236; responder rota entry 21.

### Remediation review 613 - log-shipper
Responders confirmed the host was isolated before the sweep began with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4239; responder rota entry 22.

### Remediation review 614 - key-vault
Triage recorded the bundle as proposed by the on-call responder with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4242; responder rota entry 23.

### Review entry 0718 — containment bench
> **Board decision (2026-05-20 - SR-2235)** Nadia: response-wave reporting (final). `response_tier_counts` always enumerates ALL THREE response-tier names in the order `immediate`, `urgent`, `routine`, emitting 0 for a class with no response-wave bundles. `response_order` lists the response-wave bundle ids ordered strictly in this sequence: class rank `immediate` > `urgent` > `routine`; then `response_load` descending; then `severity` descending; then `exposing_bundle_count` descending; then bundle id ascending — this is an ordering, not ascending id order, which is what `response_wave_ids` carries. `total_response_load` sums `response_load` over the response-wave bundles and `max_response_load` is the largest (0 when none join the response wave). `response_wave_checksum` is the SHA-256 hex digest of one line per response-wave bundle in `response_order` order, each `id|response_tier|response_load|exposure_overlap`, lines joined by a single newline with no trailing newline, hashed over the UTF-8 encoding.

### Remediation review 615 - report-render
The asset owner acknowledged the containment notice inside the agreed window with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4245; responder rota entry 24.

### Remediation review 616 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4248; responder rota entry 25.

### Remediation review 617 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4251; responder rota entry 26.

### Remediation review 618 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4254; responder rota entry 27.

### Remediation review 619 - session-store
Containment tooling reported the group reachable at the start of the window with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4257; responder rota entry 28.

### Remediation review 620 - policy-engine
A responder walked the runbook for this group with the platform on-call with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4260; responder rota entry 29.

### Remediation review 621 - artifact-repo
The wave was staged behind a dependency freeze released that morning with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4263; responder rota entry 30.

### Remediation review 622 - telemetry-hub
Detection replayed the original signature against this group before containment with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4266; responder rota entry 31.

### Remediation review 623 - ledger-api
The group was pulled forward after an adjacent group completed early with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4269; responder rota entry 32.

### Remediation review 624 - edge-cache
An owner handover moved this group to a second responder mid-window with two listed assets already rebuilt and therefore dropped from scope Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4272; responder rota entry 33.

### Remediation review 625 - edge-gateway
Responders confirmed the host was isolated before the sweep began while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4275; responder rota entry 34.

### Remediation review 626 - payments-core
Triage recorded the bundle as proposed by the on-call responder while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4278; responder rota entry 35.

### Remediation review 627 - identity-store
The asset owner acknowledged the containment notice inside the agreed window while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4281; responder rota entry 36.

### Remediation review 628 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4284; responder rota entry 37.

### Remediation review 629 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4287; responder rota entry 1.

### Remediation review 630 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4290; responder rota entry 2.

### Remediation review 631 - search-index
Containment tooling reported the group reachable at the start of the window while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4293; responder rota entry 3.

### Remediation review 632 - metrics-sink
A responder walked the runbook for this group with the platform on-call while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4296; responder rota entry 4.

### Remediation review 633 - queue-broker
The wave was staged behind a dependency freeze released that morning while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4299; responder rota entry 5.

### Remediation review 634 - config-store
Detection replayed the original signature against this group before containment while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4302; responder rota entry 6.

### Remediation review 635 - cdn-origin
The group was pulled forward after an adjacent group completed early while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4305; responder rota entry 7.

### Review entry 0042 — audit lane
> **Board decision (2026-05-22 - SR-2240)** Priya: remediation dashboards retain ninety days of plan history; older plans are served from the artifact archive on demand. Dashboard retention is an operational setting and carries no weight in plan output.

### Remediation review 636 - auth-proxy
An owner handover moved this group to a second responder mid-window while a credential rotation held the containment lock for part of the window Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4308; responder rota entry 8.

### Remediation review 637 - log-shipper
Responders confirmed the host was isolated before the sweep began once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4311; responder rota entry 9.

### Remediation review 638 - key-vault
Triage recorded the bundle as proposed by the on-call responder once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4314; responder rota entry 10.

### Remediation review 639 - report-render
The asset owner acknowledged the containment notice inside the agreed window once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4317; responder rota entry 11.

### Remediation review 640 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4320; responder rota entry 12.

### Remediation review 641 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4323; responder rota entry 13.

### Remediation review 642 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4326; responder rota entry 14.

### Remediation review 643 - session-store
Containment tooling reported the group reachable at the start of the window once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4329; responder rota entry 15.

### Remediation review 644 - policy-engine
A responder walked the runbook for this group with the platform on-call once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4332; responder rota entry 16.

### Remediation review 645 - artifact-repo
The wave was staged behind a dependency freeze released that morning once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4335; responder rota entry 17.

### Remediation review 646 - telemetry-hub
Detection replayed the original signature against this group before containment once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4338; responder rota entry 18.

### Remediation review 647 - ledger-api
The group was pulled forward after an adjacent group completed early once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4341; responder rota entry 19.

### Remediation review 648 - edge-cache
An owner handover moved this group to a second responder mid-window once an intake mis-tag against a sibling group had been corrected Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4344; responder rota entry 20.

### Remediation review 649 - edge-gateway
Responders confirmed the host was isolated before the sweep began despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4347; responder rota entry 21.

### Remediation review 650 - payments-core
Triage recorded the bundle as proposed by the on-call responder despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4350; responder rota entry 22.

### Remediation review 651 - identity-store
The asset owner acknowledged the containment notice inside the agreed window despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4353; responder rota entry 23.

### Remediation review 652 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4356; responder rota entry 24.

### Remediation review 653 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4359; responder rota entry 25.

### Remediation review 654 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4362; responder rota entry 26.

### Remediation review 655 - search-index
Containment tooling reported the group reachable at the start of the window despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4365; responder rota entry 27.

### Remediation review 656 - metrics-sink
A responder walked the runbook for this group with the platform on-call despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4368; responder rota entry 28.

### Review entry 0043 — audit lane
> **Board decision (2026-05-26 - SR-2246)** Marta: artifact bundles must record plan signatures at export and again at archive ingest; a mismatch quarantines the bundle for manual review. Evidence handling only; plan contents are unaffected.

### Remediation review 657 - queue-broker
The wave was staged behind a dependency freeze released that morning despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4371; responder rota entry 29.

### Remediation review 658 - config-store
Detection replayed the original signature against this group before containment despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4374; responder rota entry 30.

### Remediation review 659 - cdn-origin
The group was pulled forward after an adjacent group completed early despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4377; responder rota entry 31.

### Remediation review 660 - auth-proxy
An owner handover moved this group to a second responder mid-window despite a transient API error in the sweep tooling that retried unattended Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4380; responder rota entry 32.

### Remediation review 661 - log-shipper
Responders confirmed the host was isolated before the sweep began after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4383; responder rota entry 33.

### Remediation review 662 - key-vault
Triage recorded the bundle as proposed by the on-call responder after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4386; responder rota entry 34.

### Remediation review 663 - report-render
The asset owner acknowledged the containment notice inside the agreed window after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4389; responder rota entry 35.

### Remediation review 664 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4392; responder rota entry 36.

### Remediation review 665 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4395; responder rota entry 37.

### Remediation review 666 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4398; responder rota entry 1.

### Remediation review 667 - session-store
Containment tooling reported the group reachable at the start of the window after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4401; responder rota entry 2.

### Remediation review 668 - policy-engine
A responder walked the runbook for this group with the platform on-call after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4404; responder rota entry 3.

### Remediation review 669 - artifact-repo
The wave was staged behind a dependency freeze released that morning after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4407; responder rota entry 4.

### Remediation review 670 - telemetry-hub
Detection replayed the original signature against this group before containment after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4410; responder rota entry 5.

### Remediation review 671 - ledger-api
The group was pulled forward after an adjacent group completed early after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4413; responder rota entry 6.

### Remediation review 672 - edge-cache
An owner handover moved this group to a second responder mid-window after forensics retained a disk image under a separate retention policy Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4416; responder rota entry 7.

### Remediation review 673 - edge-gateway
Responders confirmed the host was isolated before the sweep began with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4419; responder rota entry 8.

### Remediation review 674 - payments-core
Triage recorded the bundle as proposed by the on-call responder with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4422; responder rota entry 9.

### Remediation review 675 - identity-store
The asset owner acknowledged the containment notice inside the agreed window with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4425; responder rota entry 10.

### Remediation review 676 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4428; responder rota entry 11.

### Remediation review 677 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4431; responder rota entry 12.

### Remediation review 678 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4434; responder rota entry 13.

### Remediation review 679 - search-index
Containment tooling reported the group reachable at the start of the window with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4437; responder rota entry 14.

### Remediation review 680 - metrics-sink
A responder walked the runbook for this group with the platform on-call with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4440; responder rota entry 15.

### Remediation review 681 - queue-broker
The wave was staged behind a dependency freeze released that morning with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4443; responder rota entry 16.

### Remediation review 682 - config-store
Detection replayed the original signature against this group before containment with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4446; responder rota entry 17.

### Remediation review 683 - cdn-origin
The group was pulled forward after an adjacent group completed early with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4449; responder rota entry 18.

### Remediation review 684 - auth-proxy
An owner handover moved this group to a second responder mid-window with one asset unreachable until its switch port was re-enabled Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4452; responder rota entry 19.

### Remediation review 685 - log-shipper
Responders confirmed the host was isolated before the sweep began following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4455; responder rota entry 20.

### Remediation review 686 - key-vault
Triage recorded the bundle as proposed by the on-call responder following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4458; responder rota entry 21.

### Remediation review 687 - report-render
The asset owner acknowledged the containment notice inside the agreed window following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4461; responder rota entry 22.

### Remediation review 688 - stream-tap
Endpoint telemetry was reviewed for the affected group before scheduling following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4464; responder rota entry 23.

### Remediation review 689 - backup-vault
The remediation ticket was linked to the parent intrusion record at intake following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4467; responder rota entry 24.

### Remediation review 690 - dns-resolver
Inventory reconciliation ran against this group ahead of the sweep following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4470; responder rota entry 25.

### Remediation review 691 - session-store
Containment tooling reported the group reachable at the start of the window following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4473; responder rota entry 26.

### Remediation review 692 - policy-engine
A responder walked the runbook for this group with the platform on-call following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4476; responder rota entry 27.

### Remediation review 693 - artifact-repo
The wave was staged behind a dependency freeze released that morning following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4479; responder rota entry 28.

### Remediation review 694 - telemetry-hub
Detection replayed the original signature against this group before containment following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4482; responder rota entry 29.

### Remediation review 695 - ledger-api
The group was pulled forward after an adjacent group completed early following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4485; responder rota entry 30.

### Remediation review 696 - edge-cache
An owner handover moved this group to a second responder mid-window following a short pause while the change freeze exception was confirmed Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4488; responder rota entry 31.

### Remediation review 697 - edge-gateway
Responders confirmed the host was isolated before the sweep began after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4491; responder rota entry 32.

### Remediation review 698 - payments-core
Triage recorded the bundle as proposed by the on-call responder after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4494; responder rota entry 33.

### Remediation review 699 - identity-store
The asset owner acknowledged the containment notice inside the agreed window after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4497; responder rota entry 34.

### Remediation review 700 - object-cache
Endpoint telemetry was reviewed for the affected group before scheduling after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Closed with no action required. Wave reference 4500; responder rota entry 35.

### Remediation review 701 - batch-runner
The remediation ticket was linked to the parent intrusion record at intake after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Referred to the tooling backlog. Wave reference 4503; responder rota entry 36.

### Remediation review 702 - mail-relay
Inventory reconciliation ran against this group ahead of the sweep after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Filed for the quarterly review. Wave reference 4506; responder rota entry 37.

### Remediation review 703 - search-index
Containment tooling reported the group reachable at the start of the window after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
No plan semantics changed in this entry. Wave reference 4509; responder rota entry 1.

### Remediation review 704 - metrics-sink
A responder walked the runbook for this group with the platform on-call after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Parameters remain as approved by the board. Wave reference 4512; responder rota entry 2.

### Remediation review 705 - queue-broker
The wave was staged behind a dependency freeze released that morning after the inventory source disagreement over hostname casing was settled Monitoring raised a duplicate containment alert which was suppressed at source.
Logged for the incident record; no planning impact. Wave reference 4515; responder rota entry 3.
