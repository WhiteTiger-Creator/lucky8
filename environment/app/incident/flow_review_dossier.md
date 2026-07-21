
# Tideguard Badge-Access Review Dossier

Working record of the access-control review board. The containment rollup deployed during the Tideguard incident is producing an unreliable responder queue; how the rollup is *meant* to behave was settled here incrementally, not in any single summary. February triage proposals were partly reversed during the March working sessions and several March positions were revised again in the May close-out, so trace each rule to its final dated decision. `/app/docs/report_spec.json` is the output contract only: it fixes file names, key sets and checksum serialization, not how any value is derived.

### Review entry 0011 — atrium lane

Door controller B6 on eastwing was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Sato reviewed 54 camera frames against the server-hall flow log for the night shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 91 attendees; facilities holds the roster.
Okonkwo confirmed the atrium anti-passback timer stayed at the 128-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the relief shift: 165 blanks issued, none unaccounted.
Osei closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 239 minutes during the night shift with no operator intervention.
Ferrara measured 276 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for vault listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Nakamura verified dockbay monitoring resumed on the night shift 424 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the swing shift; Rautio logged the 461-second release delay.
Baptiste traced 498 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 535 records on the relief shift with no manual overrides.
Abadi spot-checked port C7 on atrium: the strike alignment was within spec after 572 cycles.
Access-review queue for coldroom carried 609 items into the night shift, all of them informational.
Sato archived 646 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the early shift; 683 terminations were re-dressed.
Okonkwo reconciled the server-hall muster report against 720 flow-in events and found no gap.
Haugen walked the vault escort log for the late shift and matched all 757 service entries to a host.
Reader A5 on atrium logged 794 tailgate warnings during the night shift; each cleared on manual review.
Thorsen rotated the coldroom inspection-window schedule after the rollout; 831 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 868 watts, within tolerance.
Villanueva cross-checked 905 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 42 times on the late shift with no false rejects.
Moreau logged a firmware note for vault: readers on B1 sat at level and needed no night-shift patch.
Turnstile throughput on atrium peaked at 116 passages per hour during the swing shift, well inside spec.
Rautio reconciled the coldroom lost-flow register: 153 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 190 times, every one traced to facilities propping the port.
Delacroix confirmed the eastwing camera-to-flow overlay stayed aligned across 227 sampled events.
Escort-desk staffing for server-hall held at 264 through the night shift; no queue built at the reader.
Lindqvist archived 301 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 338 test cards on the early shift.
Kowalczyk noted 375 seconds of NTP skew on the coldroom controller, corrected before the relief shift ended.
Loading-dock override at dockbay port E2 was used 412 times for deliveries, each with a signed slip.
Haugen tallied 449 after-hours flows for eastwing on the night shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 486 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Ferrara reviewed 560 camera frames against the atrium flow log for the relief shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 597 attendees; facilities holds the roster.
Menendez confirmed the dockbay anti-passback timer stayed at the 634-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the swing shift: 671 blanks issued, none unaccounted.
Nakamura closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 745 minutes during the relief shift with no operator intervention.
Baptiste measured 782 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for coldroom listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Sato verified server-hall monitoring resumed on the relief shift 30 seconds after the controller restart.
Fire-panel interlock test on vault passed on the late shift; Kowalczyk logged the 67-second release delay.
Okonkwo traced 104 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 141 records on the swing shift with no manual overrides.
Osei spot-checked port E2 on dockbay: the strike alignment was within spec after 178 cycles.
Access-review queue for eastwing carried 215 items into the relief shift, all of them informational.
Ferrara archived 252 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the night shift; 289 terminations were re-dressed.
Menendez reconciled the atrium muster report against 326 flow-in events and found no gap.
Moreau walked the coldroom escort log for the early shift and matched all 363 service entries to a host.
Reader C2 on dockbay logged 400 tailgate warnings during the relief shift; each cleared on manual review.
> **Triage proposal (2026-02-09 - TQ-3208)** Okonkwo: entry timestamps are read from `granted_at`, the field the port controller stamps on unlock. *(Superseded — reversed in the May close-out; see the matching decision entry.)*
Rautio rotated the eastwing inspection-window schedule after the rollout; 437 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 474 watts, within tolerance.
Delacroix cross-checked 511 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 548 times on the early shift with no false rejects.
Lindqvist logged a firmware note for coldroom: readers on C4 sat at level and needed no relief-shift patch.
Turnstile throughput on dockbay peaked at 622 passages per hour during the late shift, well inside spec.
Kowalczyk reconciled the eastwing lost-flow register: 659 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 696 times, every one traced to facilities propping the port.
Haugen confirmed the vault camera-to-flow overlay stayed aligned across 733 sampled events.
Escort-desk staffing for atrium held at 770 through the relief shift; no queue built at the reader.
Thorsen archived 807 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 844 test cards on the night shift.
Villanueva noted 881 seconds of NTP skew on the eastwing controller, corrected before the swing shift ended.
Loading-dock override at server-hall port G4 was used 18 times for deliveries, each with a signed slip.
Moreau tallied 55 after-hours flows for vault on the relief shift; all matched authorized on-call staff.
Muster drill for atrium cleared 92 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Baptiste reviewed 166 camera frames against the dockbay flow log for the swing shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 203 attendees; facilities holds the roster.
Abadi confirmed the server-hall anti-passback timer stayed at the 240-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the late shift: 277 blanks issued, none unaccounted.
Sato closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 351 minutes during the swing shift with no operator intervention.
Okonkwo measured 388 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for eastwing listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Ferrara verified atrium monitoring resumed on the swing shift 536 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the early shift; Villanueva logged the 573-second release delay.
Menendez traced 610 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 647 records on the late shift with no manual overrides.
Nakamura spot-checked port G4 on server-hall: the strike alignment was within spec after 684 cycles.
Access-review queue for vault carried 721 items into the swing shift, all of them informational.
Baptiste archived 758 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the relief shift; 795 terminations were re-dressed.
Abadi reconciled the dockbay muster report against 832 flow-in events and found no gap.
Lindqvist walked the eastwing escort log for the night shift and matched all 869 service entries to a host.
Reader D5 on server-hall logged 906 tailgate warnings during the swing shift; each cleared on manual review.
Kowalczyk rotated the vault inspection-window schedule after the rollout; 43 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 80 watts, within tolerance.
Haugen cross-checked 117 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 154 times on the night shift with no false rejects.
Thorsen logged a firmware note for eastwing: readers on D8 sat at level and needed no swing-shift patch.
Turnstile throughput on server-hall peaked at 228 passages per hour during the early shift, well inside spec.
Villanueva reconciled the vault lost-flow register: 265 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 302 times, every one traced to facilities propping the port.
Moreau confirmed the coldroom camera-to-flow overlay stayed aligned across 339 sampled events.
Escort-desk staffing for dockbay held at 376 through the swing shift; no queue built at the reader.
Rautio archived 413 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 450 test cards on the relief shift.
Delacroix noted 487 seconds of NTP skew on the vault controller, corrected before the late shift ended.
Loading-dock override at atrium port A5 was used 524 times for deliveries, each with a signed slip.
Lindqvist tallied 561 after-hours flows for coldroom on the swing shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 598 occupants in under the target time with no reader contention.

### Review entry 0015 — coldroom lane

Door controller H2 on eastwing was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Okonkwo reviewed 672 camera frames against the server-hall flow log for the late shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 709 attendees; facilities holds the roster.
Osei confirmed the atrium anti-passback timer stayed at the 746-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the early shift: 783 blanks issued, none unaccounted.
Ferrara closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 857 minutes during the late shift with no operator intervention.
Menendez measured 894 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for vault listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Baptiste verified dockbay monitoring resumed on the late shift 142 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the night shift; Delacroix logged the 179-second release delay.
Abadi traced 216 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 253 records on the early shift with no manual overrides.
Sato spot-checked port A5 on atrium: the strike alignment was within spec after 290 cycles.
Access-review queue for coldroom carried 327 items into the late shift, all of them informational.
Okonkwo archived 364 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the swing shift; 401 terminations were re-dressed.
Osei reconciled the server-hall muster report against 438 flow-in events and found no gap.
Thorsen walked the vault escort log for the relief shift and matched all 475 service entries to a host.
Reader F3 on atrium logged 512 tailgate warnings during the late shift; each cleared on manual review.
Villanueva rotated the coldroom inspection-window schedule after the rollout; 549 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 586 watts, within tolerance.
Moreau cross-checked 623 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 660 times on the relief shift with no false rejects.
Rautio logged a firmware note for vault: readers on F9 sat at level and needed no late-shift patch.
Turnstile throughput on atrium peaked at 734 passages per hour during the night shift, well inside spec.
Delacroix reconciled the coldroom lost-flow register: 771 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 808 times, every one traced to facilities propping the port.
Lindqvist confirmed the eastwing camera-to-flow overlay stayed aligned across 845 sampled events.
Escort-desk staffing for server-hall held at 882 through the late shift; no queue built at the reader.
Kowalczyk archived 19 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 56 test cards on the swing shift.
Haugen noted 93 seconds of NTP skew on the coldroom controller, corrected before the early shift ended.
Loading-dock override at dockbay port C2 was used 130 times for deliveries, each with a signed slip.
Thorsen tallied 167 after-hours flows for eastwing on the late shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 204 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Menendez reviewed 278 camera frames against the atrium flow log for the early shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 315 attendees; facilities holds the roster.
Nakamura confirmed the dockbay anti-passback timer stayed at the 352-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the night shift: 389 blanks issued, none unaccounted.
Baptiste closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 463 minutes during the early shift with no operator intervention.
Abadi measured 500 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for coldroom listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Okonkwo verified server-hall monitoring resumed on the early shift 648 seconds after the controller restart.
Fire-panel interlock test on vault passed on the relief shift; Haugen logged the 685-second release delay.
Osei traced 722 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 759 records on the night shift with no manual overrides.
Ferrara spot-checked port C2 on dockbay: the strike alignment was within spec after 796 cycles.
Access-review queue for eastwing carried 833 items into the early shift, all of them informational.
Menendez archived 870 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the late shift; 907 terminations were re-dressed.
Nakamura reconciled the atrium muster report against 44 flow-in events and found no gap.
Rautio walked the coldroom escort log for the swing shift and matched all 81 service entries to a host.
Reader A1 on dockbay logged 118 tailgate warnings during the early shift; each cleared on manual review.
> **Triage proposal (2026-02-12 - TQ-3210)** Lindqvist: trust_tier is taken as written; the controllers already emit canonical values. *(Superseded — reversed in the May close-out; see the matching decision entry.)*
Delacroix rotated the eastwing inspection-window schedule after the rollout; 155 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 192 watts, within tolerance.
Lindqvist cross-checked 229 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 266 times on the swing shift with no false rejects.
Kowalczyk logged a firmware note for coldroom: readers on A2 sat at level and needed no early-shift patch.
Turnstile throughput on dockbay peaked at 340 passages per hour during the relief shift, well inside spec.
Haugen reconciled the eastwing lost-flow register: 377 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 414 times, every one traced to facilities propping the port.
Thorsen confirmed the vault camera-to-flow overlay stayed aligned across 451 sampled events.
Escort-desk staffing for atrium held at 488 through the early shift; no queue built at the reader.
Villanueva archived 525 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 562 test cards on the late shift.
Moreau noted 599 seconds of NTP skew on the eastwing controller, corrected before the night shift ended.
Loading-dock override at server-hall port D5 was used 636 times for deliveries, each with a signed slip.
Rautio tallied 673 after-hours flows for vault on the early shift; all matched authorized on-call staff.
Muster drill for atrium cleared 710 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Abadi reviewed 784 camera frames against the dockbay flow log for the night shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 821 attendees; facilities holds the roster.
Sato confirmed the server-hall anti-passback timer stayed at the 858-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the relief shift: 895 blanks issued, none unaccounted.
Okonkwo closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 69 minutes during the night shift with no operator intervention.
Osei measured 106 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for eastwing listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Menendez verified atrium monitoring resumed on the night shift 254 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the swing shift; Moreau logged the 291-second release delay.
Nakamura traced 328 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 365 records on the relief shift with no manual overrides.
Baptiste spot-checked port D5 on server-hall: the strike alignment was within spec after 402 cycles.
Access-review queue for vault carried 439 items into the night shift, all of them informational.
Abadi archived 476 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the early shift; 513 terminations were re-dressed.
Sato reconciled the dockbay muster report against 550 flow-in events and found no gap.
Kowalczyk walked the eastwing escort log for the late shift and matched all 587 service entries to a host.
Reader B3 on server-hall logged 624 tailgate warnings during the night shift; each cleared on manual review.
Haugen rotated the vault inspection-window schedule after the rollout; 661 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 698 watts, within tolerance.
Thorsen cross-checked 735 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 772 times on the late shift with no false rejects.
Villanueva logged a firmware note for eastwing: readers on B6 sat at level and needed no night-shift patch.
Turnstile throughput on server-hall peaked at 846 passages per hour during the swing shift, well inside spec.
Moreau reconciled the vault lost-flow register: 883 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 20 times, every one traced to facilities propping the port.
Rautio confirmed the coldroom camera-to-flow overlay stayed aligned across 57 sampled events.
Escort-desk staffing for dockbay held at 94 through the night shift; no queue built at the reader.
Delacroix archived 131 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 168 test cards on the early shift.
Lindqvist noted 205 seconds of NTP skew on the vault controller, corrected before the relief shift ended.
Loading-dock override at atrium port F3 was used 242 times for deliveries, each with a signed slip.
Kowalczyk tallied 279 after-hours flows for coldroom on the night shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 316 occupants in under the target time with no reader contention.

### Review entry 0019 — dockbay lane

Door controller D8 on eastwing was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Osei reviewed 390 camera frames against the server-hall flow log for the relief shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 427 attendees; facilities holds the roster.
Ferrara confirmed the atrium anti-passback timer stayed at the 464-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the swing shift: 501 blanks issued, none unaccounted.
Menendez closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 575 minutes during the relief shift with no operator intervention.
Nakamura measured 612 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for vault listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Abadi verified dockbay monitoring resumed on the relief shift 760 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the late shift; Lindqvist logged the 797-second release delay.
Sato traced 834 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 871 records on the swing shift with no manual overrides.
Okonkwo spot-checked port F3 on atrium: the strike alignment was within spec after 908 cycles.
Access-review queue for coldroom carried 45 items into the relief shift, all of them informational.
Osei archived 82 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the night shift; 119 terminations were re-dressed.
Ferrara reconciled the server-hall muster report against 156 flow-in events and found no gap.
Villanueva walked the vault escort log for the early shift and matched all 193 service entries to a host.
Reader C7 on atrium logged 230 tailgate warnings during the relief shift; each cleared on manual review.
Moreau rotated the coldroom inspection-window schedule after the rollout; 267 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 304 watts, within tolerance.
Rautio cross-checked 341 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 378 times on the early shift with no false rejects.
Delacroix logged a firmware note for vault: readers on D1 sat at level and needed no relief-shift patch.
Turnstile throughput on atrium peaked at 452 passages per hour during the late shift, well inside spec.
Lindqvist reconciled the coldroom lost-flow register: 489 reported, all deactivated within the shift window.
Door-forced alarm on C2 at dockbay fired 526 times, every one traced to facilities propping the port.
Kowalczyk confirmed the eastwing camera-to-flow overlay stayed aligned across 563 sampled events.
Escort-desk staffing for server-hall held at 600 through the relief shift; no queue built at the reader.
Haugen archived 637 reader event logs from vault port B1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 674 test cards on the night shift.
Thorsen noted 711 seconds of NTP skew on the coldroom controller, corrected before the swing shift ended.
Loading-dock override at dockbay port A1 was used 748 times for deliveries, each with a signed slip.
Villanueva tallied 785 after-hours flows for eastwing on the relief shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 822 occupants in under the target time with no reader contention.
Door controller F9 on vault was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Nakamura reviewed 896 camera frames against the atrium flow log for the swing shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 33 attendees; facilities holds the roster.
Baptiste confirmed the dockbay anti-passback timer stayed at the 70-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the late shift: 107 blanks issued, none unaccounted.
Abadi closed the server-hall follow-up on port G4 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D1 on vault recalibrated in 181 minutes during the swing shift with no operator intervention.
Sato measured 218 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for coldroom listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on dockbay port C2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port H2 closed without action; the mechanical override was already compliant.
Osei verified server-hall monitoring resumed on the swing shift 366 seconds after the controller restart.
Fire-panel interlock test on vault passed on the early shift; Thorsen logged the 403-second release delay.
Ferrara traced 440 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 477 records on the late shift with no manual overrides.
Menendez spot-checked port A1 on dockbay: the strike alignment was within spec after 514 cycles.
Access-review queue for eastwing carried 551 items into the swing shift, all of them informational.
Nakamura archived 588 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port F9 finished during the relief shift; 625 terminations were re-dressed.
Baptiste reconciled the atrium muster report against 662 flow-in events and found no gap.
Delacroix walked the coldroom escort log for the night shift and matched all 699 service entries to a host.
Reader E2 on dockbay logged 736 tailgate warnings during the swing shift; each cleared on manual review.
> **Triage proposal (2026-02-15 - TQ-3212)** Baptiste: on a repeated flow_id keep the row with the HIGHER flow class, since the stronger credential is the one that opened the port. *(Superseded — reversed in the May close-out; see the matching decision entry.)*
Lindqvist rotated the eastwing inspection-window schedule after the rollout; 773 entries were re-timed.
Power audit on server-hall found the G4 controller drawing normally; 810 watts, within tolerance.
Kowalczyk cross-checked 847 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port A5 at atrium was exercised 884 times on the night shift with no false rejects.
Haugen logged a firmware note for coldroom: readers on E7 sat at level and needed no swing-shift patch.
Turnstile throughput on dockbay peaked at 58 passages per hour during the early shift, well inside spec.
Thorsen reconciled the eastwing lost-flow register: 95 reported, all deactivated within the shift window.
Door-forced alarm on D5 at server-hall fired 132 times, every one traced to facilities propping the port.
Villanueva confirmed the vault camera-to-flow overlay stayed aligned across 169 sampled events.
Escort-desk staffing for atrium held at 206 through the swing shift; no queue built at the reader.
Moreau archived 243 reader event logs from coldroom port C4; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 280 test cards on the relief shift.
Rautio noted 317 seconds of NTP skew on the eastwing controller, corrected before the late shift ended.
Loading-dock override at server-hall port B3 was used 354 times for deliveries, each with a signed slip.
Delacroix tallied 391 after-hours flows for vault on the swing shift; all matched authorized on-call staff.
Muster drill for atrium cleared 428 occupants in under the target time with no reader contention.
Door controller A2 on coldroom was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Sato reviewed 502 camera frames against the dockbay flow log for the late shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 539 attendees; facilities holds the roster.
Okonkwo confirmed the server-hall anti-passback timer stayed at the 576-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the early shift: 613 blanks issued, none unaccounted.
Osei closed the atrium follow-up on port A5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile E7 on coldroom recalibrated in 687 minutes during the late shift with no operator intervention.
Ferrara measured 724 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for eastwing listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on server-hall port D5 after the rollout and saw nothing anomalous.
Locksmith callback for vault port B1 closed without action; the mechanical override was already compliant.
Nakamura verified atrium monitoring resumed on the late shift 872 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the night shift; Rautio logged the 909-second release delay.
Baptiste traced 46 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 83 records on the early shift with no manual overrides.
Abadi spot-checked port B3 on server-hall: the strike alignment was within spec after 120 cycles.
Access-review queue for vault carried 157 items into the late shift, all of them informational.
Sato archived 194 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port A2 finished during the swing shift; 231 terminations were re-dressed.
Okonkwo reconciled the dockbay muster report against 268 flow-in events and found no gap.
Haugen walked the eastwing escort log for the relief shift and matched all 305 service entries to a host.
Reader G4 on server-hall logged 342 tailgate warnings during the late shift; each cleared on manual review.
Thorsen rotated the vault inspection-window schedule after the rollout; 379 entries were re-timed.
Power audit on atrium found the A5 controller drawing normally; 416 watts, within tolerance.
Villanueva cross-checked 453 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port C2 at dockbay was exercised 490 times on the relief shift with no false rejects.
Moreau logged a firmware note for eastwing: readers on H2 sat at level and needed no late-shift patch.
Turnstile throughput on server-hall peaked at 564 passages per hour during the night shift, well inside spec.
Rautio reconciled the vault lost-flow register: 601 reported, all deactivated within the shift window.
Door-forced alarm on F3 at atrium fired 638 times, every one traced to facilities propping the port.
Delacroix confirmed the coldroom camera-to-flow overlay stayed aligned across 675 sampled events.
Escort-desk staffing for dockbay held at 712 through the late shift; no queue built at the reader.
Lindqvist archived 749 reader event logs from eastwing port D8; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 786 test cards on the swing shift.
Kowalczyk noted 823 seconds of NTP skew on the vault controller, corrected before the early shift ended.
Loading-dock override at atrium port C7 was used 860 times for deliveries, each with a signed slip.
Haugen tallied 897 after-hours flows for coldroom on the late shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 34 occupants in under the target time with no reader contention.

### Review entry 0023 — eastwing lane

Door controller B6 on eastwing was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Ferrara reviewed 108 camera frames against the server-hall flow log for the early shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 145 attendees; facilities holds the roster.
Menendez confirmed the atrium anti-passback timer stayed at the 182-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the night shift: 219 blanks issued, none unaccounted.
Nakamura closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 293 minutes during the early shift with no operator intervention.
Baptiste measured 330 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for vault listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Sato verified dockbay monitoring resumed on the early shift 478 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the relief shift; Kowalczyk logged the 515-second release delay.
Okonkwo traced 552 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 589 records on the night shift with no manual overrides.
Osei spot-checked port C7 on atrium: the strike alignment was within spec after 626 cycles.
Access-review queue for coldroom carried 663 items into the early shift, all of them informational.
Ferrara archived 700 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the late shift; 737 terminations were re-dressed.
Menendez reconciled the server-hall muster report against 774 flow-in events and found no gap.
Moreau walked the vault escort log for the swing shift and matched all 811 service entries to a host.
Reader A5 on atrium logged 848 tailgate warnings during the early shift; each cleared on manual review.
Rautio rotated the coldroom inspection-window schedule after the rollout; 885 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 22 watts, within tolerance.
Delacroix cross-checked 59 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 96 times on the swing shift with no false rejects.
Lindqvist logged a firmware note for vault: readers on B1 sat at level and needed no early-shift patch.
Turnstile throughput on atrium peaked at 170 passages per hour during the relief shift, well inside spec.
Kowalczyk reconciled the coldroom lost-flow register: 207 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 244 times, every one traced to facilities propping the port.
Haugen confirmed the eastwing camera-to-flow overlay stayed aligned across 281 sampled events.
Escort-desk staffing for server-hall held at 318 through the early shift; no queue built at the reader.
Thorsen archived 355 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 392 test cards on the late shift.
Villanueva noted 429 seconds of NTP skew on the coldroom controller, corrected before the night shift ended.
Loading-dock override at dockbay port E2 was used 466 times for deliveries, each with a signed slip.
Moreau tallied 503 after-hours flows for eastwing on the early shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 540 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Baptiste reviewed 614 camera frames against the atrium flow log for the night shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 651 attendees; facilities holds the roster.
Abadi confirmed the dockbay anti-passback timer stayed at the 688-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the relief shift: 725 blanks issued, none unaccounted.
Sato closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 799 minutes during the night shift with no operator intervention.
Okonkwo measured 836 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for coldroom listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Ferrara verified server-hall monitoring resumed on the night shift 84 seconds after the controller restart.
Fire-panel interlock test on vault passed on the swing shift; Villanueva logged the 121-second release delay.
Menendez traced 158 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 195 records on the relief shift with no manual overrides.
Nakamura spot-checked port E2 on dockbay: the strike alignment was within spec after 232 cycles.
Access-review queue for eastwing carried 269 items into the night shift, all of them informational.
Baptiste archived 306 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the early shift; 343 terminations were re-dressed.
Abadi reconciled the atrium muster report against 380 flow-in events and found no gap.
Lindqvist walked the coldroom escort log for the late shift and matched all 417 service entries to a host.
Reader C2 on dockbay logged 454 tailgate warnings during the night shift; each cleared on manual review.
> **Working note (2026-03-04 - TQ-3244)** Moreau: sessions stitch when the next flow lands within 60 ms of the previous exit. *(Revised — see the 2026-05 close-out.)*
Kowalczyk rotated the eastwing inspection-window schedule after the rollout; 491 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 528 watts, within tolerance.
Haugen cross-checked 565 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 602 times on the late shift with no false rejects.
Thorsen logged a firmware note for coldroom: readers on C4 sat at level and needed no night-shift patch.
Turnstile throughput on dockbay peaked at 676 passages per hour during the swing shift, well inside spec.
Villanueva reconciled the eastwing lost-flow register: 713 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 750 times, every one traced to facilities propping the port.
Moreau confirmed the vault camera-to-flow overlay stayed aligned across 787 sampled events.
Escort-desk staffing for atrium held at 824 through the night shift; no queue built at the reader.
Rautio archived 861 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 898 test cards on the early shift.
Delacroix noted 35 seconds of NTP skew on the eastwing controller, corrected before the relief shift ended.
Loading-dock override at server-hall port G4 was used 72 times for deliveries, each with a signed slip.
Lindqvist tallied 109 after-hours flows for vault on the night shift; all matched authorized on-call staff.
Muster drill for atrium cleared 146 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Okonkwo reviewed 220 camera frames against the dockbay flow log for the relief shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 257 attendees; facilities holds the roster.
Osei confirmed the server-hall anti-passback timer stayed at the 294-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the swing shift: 331 blanks issued, none unaccounted.
Ferrara closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 405 minutes during the relief shift with no operator intervention.
Menendez measured 442 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for eastwing listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Baptiste verified atrium monitoring resumed on the relief shift 590 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the late shift; Delacroix logged the 627-second release delay.
Abadi traced 664 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 701 records on the swing shift with no manual overrides.
Sato spot-checked port G4 on server-hall: the strike alignment was within spec after 738 cycles.
Access-review queue for vault carried 775 items into the relief shift, all of them informational.
Okonkwo archived 812 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the night shift; 849 terminations were re-dressed.
Osei reconciled the dockbay muster report against 886 flow-in events and found no gap.
Thorsen walked the eastwing escort log for the early shift and matched all 23 service entries to a host.
Reader D5 on server-hall logged 60 tailgate warnings during the relief shift; each cleared on manual review.
Villanueva rotated the vault inspection-window schedule after the rollout; 97 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 134 watts, within tolerance.
Moreau cross-checked 171 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 208 times on the early shift with no false rejects.
Rautio logged a firmware note for eastwing: readers on D8 sat at level and needed no relief-shift patch.
Turnstile throughput on server-hall peaked at 282 passages per hour during the late shift, well inside spec.
Delacroix reconciled the vault lost-flow register: 319 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 356 times, every one traced to facilities propping the port.
Lindqvist confirmed the coldroom camera-to-flow overlay stayed aligned across 393 sampled events.
Escort-desk staffing for dockbay held at 430 through the relief shift; no queue built at the reader.
Kowalczyk archived 467 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 504 test cards on the night shift.
Haugen noted 541 seconds of NTP skew on the vault controller, corrected before the swing shift ended.
Loading-dock override at atrium port A5 was used 578 times for deliveries, each with a signed slip.
Thorsen tallied 615 after-hours flows for coldroom on the relief shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 652 occupants in under the target time with no reader contention.

### Review entry 0027 — server-hall lane

Door controller H2 on eastwing was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Menendez reviewed 726 camera frames against the server-hall flow log for the swing shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 763 attendees; facilities holds the roster.
Nakamura confirmed the atrium anti-passback timer stayed at the 800-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the late shift: 837 blanks issued, none unaccounted.
Baptiste closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 911 minutes during the swing shift with no operator intervention.
Abadi measured 48 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for vault listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Okonkwo verified dockbay monitoring resumed on the swing shift 196 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the early shift; Haugen logged the 233-second release delay.
Osei traced 270 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 307 records on the late shift with no manual overrides.
Ferrara spot-checked port A5 on atrium: the strike alignment was within spec after 344 cycles.
Access-review queue for coldroom carried 381 items into the swing shift, all of them informational.
Menendez archived 418 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the relief shift; 455 terminations were re-dressed.
Nakamura reconciled the server-hall muster report against 492 flow-in events and found no gap.
Rautio walked the vault escort log for the night shift and matched all 529 service entries to a host.
Reader F3 on atrium logged 566 tailgate warnings during the swing shift; each cleared on manual review.
Delacroix rotated the coldroom inspection-window schedule after the rollout; 603 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 640 watts, within tolerance.
Lindqvist cross-checked 677 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 714 times on the night shift with no false rejects.
Kowalczyk logged a firmware note for vault: readers on F9 sat at level and needed no swing-shift patch.
Turnstile throughput on atrium peaked at 788 passages per hour during the early shift, well inside spec.
Haugen reconciled the coldroom lost-flow register: 825 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 862 times, every one traced to facilities propping the port.
Thorsen confirmed the eastwing camera-to-flow overlay stayed aligned across 899 sampled events.
Escort-desk staffing for server-hall held at 36 through the swing shift; no queue built at the reader.
Villanueva archived 73 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 110 test cards on the relief shift.
Moreau noted 147 seconds of NTP skew on the coldroom controller, corrected before the late shift ended.
Loading-dock override at dockbay port C2 was used 184 times for deliveries, each with a signed slip.
Rautio tallied 221 after-hours flows for eastwing on the swing shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 258 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Abadi reviewed 332 camera frames against the atrium flow log for the late shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 369 attendees; facilities holds the roster.
Sato confirmed the dockbay anti-passback timer stayed at the 406-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the early shift: 443 blanks issued, none unaccounted.
Okonkwo closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 517 minutes during the late shift with no operator intervention.
Osei measured 554 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for coldroom listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Menendez verified server-hall monitoring resumed on the late shift 702 seconds after the controller restart.
Fire-panel interlock test on vault passed on the night shift; Moreau logged the 739-second release delay.
Nakamura traced 776 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 813 records on the early shift with no manual overrides.
Baptiste spot-checked port C2 on dockbay: the strike alignment was within spec after 850 cycles.
Access-review queue for eastwing carried 887 items into the late shift, all of them informational.
Abadi archived 24 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the swing shift; 61 terminations were re-dressed.
Sato reconciled the atrium muster report against 98 flow-in events and found no gap.
Kowalczyk walked the coldroom escort log for the relief shift and matched all 135 service entries to a host.
Reader A1 on dockbay logged 172 tailgate warnings during the late shift; each cleared on manual review.
> **Working note (2026-03-07 - TQ-3246)** Ferrara: the occupancy carry-out is capped at 2000 ms, a bound that has never been reached in practice. *(Revised — see the 2026-05 close-out.)*
Haugen rotated the eastwing inspection-window schedule after the rollout; 209 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 246 watts, within tolerance.
Thorsen cross-checked 283 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 320 times on the relief shift with no false rejects.
Villanueva logged a firmware note for coldroom: readers on A2 sat at level and needed no late-shift patch.
Turnstile throughput on dockbay peaked at 394 passages per hour during the night shift, well inside spec.
Moreau reconciled the eastwing lost-flow register: 431 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 468 times, every one traced to facilities propping the port.
Rautio confirmed the vault camera-to-flow overlay stayed aligned across 505 sampled events.
Escort-desk staffing for atrium held at 542 through the late shift; no queue built at the reader.
Delacroix archived 579 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 616 test cards on the swing shift.
Lindqvist noted 653 seconds of NTP skew on the eastwing controller, corrected before the early shift ended.
Loading-dock override at server-hall port D5 was used 690 times for deliveries, each with a signed slip.
Kowalczyk tallied 727 after-hours flows for vault on the late shift; all matched authorized on-call staff.
Muster drill for atrium cleared 764 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Osei reviewed 838 camera frames against the dockbay flow log for the early shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 875 attendees; facilities holds the roster.
Ferrara confirmed the server-hall anti-passback timer stayed at the 912-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the night shift: 49 blanks issued, none unaccounted.
Menendez closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 123 minutes during the early shift with no operator intervention.
Nakamura measured 160 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for eastwing listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Abadi verified atrium monitoring resumed on the early shift 308 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the relief shift; Lindqvist logged the 345-second release delay.
Sato traced 382 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 419 records on the night shift with no manual overrides.
Okonkwo spot-checked port D5 on server-hall: the strike alignment was within spec after 456 cycles.
Access-review queue for vault carried 493 items into the early shift, all of them informational.
Osei archived 530 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the late shift; 567 terminations were re-dressed.
Ferrara reconciled the dockbay muster report against 604 flow-in events and found no gap.
Villanueva walked the eastwing escort log for the swing shift and matched all 641 service entries to a host.
Reader B3 on server-hall logged 678 tailgate warnings during the early shift; each cleared on manual review.
Moreau rotated the vault inspection-window schedule after the rollout; 715 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 752 watts, within tolerance.
Rautio cross-checked 789 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 826 times on the swing shift with no false rejects.
Delacroix logged a firmware note for eastwing: readers on B6 sat at level and needed no early-shift patch.
Turnstile throughput on server-hall peaked at 900 passages per hour during the relief shift, well inside spec.
Lindqvist reconciled the vault lost-flow register: 37 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 74 times, every one traced to facilities propping the port.
Kowalczyk confirmed the coldroom camera-to-flow overlay stayed aligned across 111 sampled events.
Escort-desk staffing for dockbay held at 148 through the early shift; no queue built at the reader.
Haugen archived 185 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 222 test cards on the late shift.
Thorsen noted 259 seconds of NTP skew on the vault controller, corrected before the night shift ended.
Loading-dock override at atrium port F3 was used 296 times for deliveries, each with a signed slip.
Villanueva tallied 333 after-hours flows for coldroom on the early shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 370 occupants in under the target time with no reader contention.

### Review entry 0031 — vault lane

Door controller D8 on eastwing was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Nakamura reviewed 444 camera frames against the server-hall flow log for the night shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 481 attendees; facilities holds the roster.
Baptiste confirmed the atrium anti-passback timer stayed at the 518-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the relief shift: 555 blanks issued, none unaccounted.
Abadi closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 629 minutes during the night shift with no operator intervention.
Sato measured 666 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for vault listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Osei verified dockbay monitoring resumed on the night shift 814 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the swing shift; Thorsen logged the 851-second release delay.
Ferrara traced 888 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 25 records on the relief shift with no manual overrides.
Menendez spot-checked port F3 on atrium: the strike alignment was within spec after 62 cycles.
Access-review queue for coldroom carried 99 items into the night shift, all of them informational.
Nakamura archived 136 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the early shift; 173 terminations were re-dressed.
Baptiste reconciled the server-hall muster report against 210 flow-in events and found no gap.
Delacroix walked the vault escort log for the late shift and matched all 247 service entries to a host.
Reader C7 on atrium logged 284 tailgate warnings during the night shift; each cleared on manual review.
Lindqvist rotated the coldroom inspection-window schedule after the rollout; 321 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 358 watts, within tolerance.
Kowalczyk cross-checked 395 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 432 times on the late shift with no false rejects.
Haugen logged a firmware note for vault: readers on D1 sat at level and needed no night-shift patch.
Turnstile throughput on atrium peaked at 506 passages per hour during the swing shift, well inside spec.
Thorsen reconciled the coldroom lost-flow register: 543 reported, all deactivated within the shift window.
Door-forced alarm on C2 at dockbay fired 580 times, every one traced to facilities propping the port.
Villanueva confirmed the eastwing camera-to-flow overlay stayed aligned across 617 sampled events.
Escort-desk staffing for server-hall held at 654 through the night shift; no queue built at the reader.
Moreau archived 691 reader event logs from vault port B1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 728 test cards on the early shift.
Rautio noted 765 seconds of NTP skew on the coldroom controller, corrected before the relief shift ended.
Loading-dock override at dockbay port A1 was used 802 times for deliveries, each with a signed slip.
Delacroix tallied 839 after-hours flows for eastwing on the night shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 876 occupants in under the target time with no reader contention.
Door controller F9 on vault was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Sato reviewed 50 camera frames against the atrium flow log for the relief shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 87 attendees; facilities holds the roster.
Okonkwo confirmed the dockbay anti-passback timer stayed at the 124-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the swing shift: 161 blanks issued, none unaccounted.
Osei closed the server-hall follow-up on port G4 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D1 on vault recalibrated in 235 minutes during the relief shift with no operator intervention.
Ferrara measured 272 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for coldroom listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on dockbay port C2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port H2 closed without action; the mechanical override was already compliant.
Nakamura verified server-hall monitoring resumed on the relief shift 420 seconds after the controller restart.
Fire-panel interlock test on vault passed on the late shift; Rautio logged the 457-second release delay.
Baptiste traced 494 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 531 records on the swing shift with no manual overrides.
Abadi spot-checked port A1 on dockbay: the strike alignment was within spec after 568 cycles.
Access-review queue for eastwing carried 605 items into the relief shift, all of them informational.
Sato archived 642 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port F9 finished during the night shift; 679 terminations were re-dressed.
Okonkwo reconciled the atrium muster report against 716 flow-in events and found no gap.
Haugen walked the coldroom escort log for the early shift and matched all 753 service entries to a host.
Reader E2 on dockbay logged 790 tailgate warnings during the relief shift; each cleared on manual review.
> **Working note (2026-03-11 - TQ-3248)** Haugen: a class that has its own control window also inherits the `all`-scoped windows for that layer, so both apply. *(Revised — see the 2026-05 close-out.)*
Thorsen rotated the eastwing inspection-window schedule after the rollout; 827 entries were re-timed.
Power audit on server-hall found the G4 controller drawing normally; 864 watts, within tolerance.
Villanueva cross-checked 901 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port A5 at atrium was exercised 38 times on the early shift with no false rejects.
Moreau logged a firmware note for coldroom: readers on E7 sat at level and needed no relief-shift patch.
Turnstile throughput on dockbay peaked at 112 passages per hour during the late shift, well inside spec.
Rautio reconciled the eastwing lost-flow register: 149 reported, all deactivated within the shift window.
Door-forced alarm on D5 at server-hall fired 186 times, every one traced to facilities propping the port.
Delacroix confirmed the vault camera-to-flow overlay stayed aligned across 223 sampled events.
Escort-desk staffing for atrium held at 260 through the relief shift; no queue built at the reader.
Lindqvist archived 297 reader event logs from coldroom port C4; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 334 test cards on the night shift.
Kowalczyk noted 371 seconds of NTP skew on the eastwing controller, corrected before the swing shift ended.
Loading-dock override at server-hall port B3 was used 408 times for deliveries, each with a signed slip.
Haugen tallied 445 after-hours flows for vault on the relief shift; all matched authorized on-call staff.
Muster drill for atrium cleared 482 occupants in under the target time with no reader contention.
Door controller A2 on coldroom was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Ferrara reviewed 556 camera frames against the dockbay flow log for the swing shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 593 attendees; facilities holds the roster.
Menendez confirmed the server-hall anti-passback timer stayed at the 630-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the late shift: 667 blanks issued, none unaccounted.
Nakamura closed the atrium follow-up on port A5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile E7 on coldroom recalibrated in 741 minutes during the swing shift with no operator intervention.
Baptiste measured 778 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for eastwing listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on server-hall port D5 after the rollout and saw nothing anomalous.
Locksmith callback for vault port B1 closed without action; the mechanical override was already compliant.
Sato verified atrium monitoring resumed on the swing shift 26 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the early shift; Kowalczyk logged the 63-second release delay.
Okonkwo traced 100 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 137 records on the late shift with no manual overrides.
Osei spot-checked port B3 on server-hall: the strike alignment was within spec after 174 cycles.
Access-review queue for vault carried 211 items into the swing shift, all of them informational.
Ferrara archived 248 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port A2 finished during the relief shift; 285 terminations were re-dressed.
Menendez reconciled the dockbay muster report against 322 flow-in events and found no gap.
Moreau walked the eastwing escort log for the night shift and matched all 359 service entries to a host.
Reader G4 on server-hall logged 396 tailgate warnings during the swing shift; each cleared on manual review.
Rautio rotated the vault inspection-window schedule after the rollout; 433 entries were re-timed.
Power audit on atrium found the A5 controller drawing normally; 470 watts, within tolerance.
Delacroix cross-checked 507 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port C2 at dockbay was exercised 544 times on the night shift with no false rejects.
Lindqvist logged a firmware note for eastwing: readers on H2 sat at level and needed no swing-shift patch.
Turnstile throughput on server-hall peaked at 618 passages per hour during the early shift, well inside spec.
Kowalczyk reconciled the vault lost-flow register: 655 reported, all deactivated within the shift window.
Door-forced alarm on F3 at atrium fired 692 times, every one traced to facilities propping the port.
Haugen confirmed the coldroom camera-to-flow overlay stayed aligned across 729 sampled events.
Escort-desk staffing for dockbay held at 766 through the swing shift; no queue built at the reader.
Thorsen archived 803 reader event logs from eastwing port D8; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 840 test cards on the relief shift.
Villanueva noted 877 seconds of NTP skew on the vault controller, corrected before the late shift ended.
Loading-dock override at atrium port C7 was used 914 times for deliveries, each with a signed slip.
Moreau tallied 51 after-hours flows for coldroom on the swing shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 88 occupants in under the target time with no reader contention.

### Review entry 0035 — atrium lane

Door controller B6 on eastwing was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Baptiste reviewed 162 camera frames against the server-hall flow log for the late shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 199 attendees; facilities holds the roster.
Abadi confirmed the atrium anti-passback timer stayed at the 236-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the early shift: 273 blanks issued, none unaccounted.
Sato closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 347 minutes during the late shift with no operator intervention.
Okonkwo measured 384 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for vault listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Ferrara verified dockbay monitoring resumed on the late shift 532 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the night shift; Villanueva logged the 569-second release delay.
Menendez traced 606 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 643 records on the early shift with no manual overrides.
Nakamura spot-checked port C7 on atrium: the strike alignment was within spec after 680 cycles.
Access-review queue for coldroom carried 717 items into the late shift, all of them informational.
Baptiste archived 754 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the swing shift; 791 terminations were re-dressed.
Abadi reconciled the server-hall muster report against 828 flow-in events and found no gap.
Lindqvist walked the vault escort log for the relief shift and matched all 865 service entries to a host.
Reader A5 on atrium logged 902 tailgate warnings during the late shift; each cleared on manual review.
Kowalczyk rotated the coldroom inspection-window schedule after the rollout; 39 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 76 watts, within tolerance.
Haugen cross-checked 113 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 150 times on the relief shift with no false rejects.
Thorsen logged a firmware note for vault: readers on B1 sat at level and needed no late-shift patch.
Turnstile throughput on atrium peaked at 224 passages per hour during the night shift, well inside spec.
Villanueva reconciled the coldroom lost-flow register: 261 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 298 times, every one traced to facilities propping the port.
Moreau confirmed the eastwing camera-to-flow overlay stayed aligned across 335 sampled events.
Escort-desk staffing for server-hall held at 372 through the late shift; no queue built at the reader.
Rautio archived 409 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 446 test cards on the swing shift.
Delacroix noted 483 seconds of NTP skew on the coldroom controller, corrected before the early shift ended.
Loading-dock override at dockbay port E2 was used 520 times for deliveries, each with a signed slip.
Lindqvist tallied 557 after-hours flows for eastwing on the late shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 594 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Okonkwo reviewed 668 camera frames against the atrium flow log for the early shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 705 attendees; facilities holds the roster.
Osei confirmed the dockbay anti-passback timer stayed at the 742-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the night shift: 779 blanks issued, none unaccounted.
Ferrara closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 853 minutes during the early shift with no operator intervention.
Menendez measured 890 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for coldroom listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Baptiste verified server-hall monitoring resumed on the early shift 138 seconds after the controller restart.
Fire-panel interlock test on vault passed on the relief shift; Delacroix logged the 175-second release delay.
Abadi traced 212 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 249 records on the night shift with no manual overrides.
Sato spot-checked port E2 on dockbay: the strike alignment was within spec after 286 cycles.
Access-review queue for eastwing carried 323 items into the early shift, all of them informational.
Okonkwo archived 360 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the late shift; 397 terminations were re-dressed.
Osei reconciled the atrium muster report against 434 flow-in events and found no gap.
Thorsen walked the coldroom escort log for the swing shift and matched all 471 service entries to a host.
Reader C2 on dockbay logged 508 tailgate warnings during the early shift; each cleared on manual review.
> **Working note (2026-03-15 - TQ-3250)** Sato: isolation and inspection are charged independently; an instant covered by both is charged twice. *(Revised — see the 2026-05 close-out.)*
Villanueva rotated the eastwing inspection-window schedule after the rollout; 545 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 582 watts, within tolerance.
Moreau cross-checked 619 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 656 times on the swing shift with no false rejects.
Rautio logged a firmware note for coldroom: readers on C4 sat at level and needed no early-shift patch.
Turnstile throughput on dockbay peaked at 730 passages per hour during the relief shift, well inside spec.
Delacroix reconciled the eastwing lost-flow register: 767 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 804 times, every one traced to facilities propping the port.
Lindqvist confirmed the vault camera-to-flow overlay stayed aligned across 841 sampled events.
Escort-desk staffing for atrium held at 878 through the early shift; no queue built at the reader.
Kowalczyk archived 915 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 52 test cards on the late shift.
Haugen noted 89 seconds of NTP skew on the eastwing controller, corrected before the night shift ended.
Loading-dock override at server-hall port G4 was used 126 times for deliveries, each with a signed slip.
Thorsen tallied 163 after-hours flows for vault on the early shift; all matched authorized on-call staff.
Muster drill for atrium cleared 200 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Menendez reviewed 274 camera frames against the dockbay flow log for the night shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 311 attendees; facilities holds the roster.
Nakamura confirmed the server-hall anti-passback timer stayed at the 348-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the relief shift: 385 blanks issued, none unaccounted.
Baptiste closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 459 minutes during the night shift with no operator intervention.
Abadi measured 496 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for eastwing listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Okonkwo verified atrium monitoring resumed on the night shift 644 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the swing shift; Haugen logged the 681-second release delay.
Osei traced 718 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 755 records on the relief shift with no manual overrides.
Ferrara spot-checked port G4 on server-hall: the strike alignment was within spec after 792 cycles.
Access-review queue for vault carried 829 items into the night shift, all of them informational.
Menendez archived 866 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the early shift; 903 terminations were re-dressed.
Nakamura reconciled the dockbay muster report against 40 flow-in events and found no gap.
Rautio walked the eastwing escort log for the late shift and matched all 77 service entries to a host.
Reader D5 on server-hall logged 114 tailgate warnings during the night shift; each cleared on manual review.
Delacroix rotated the vault inspection-window schedule after the rollout; 151 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 188 watts, within tolerance.
Lindqvist cross-checked 225 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 262 times on the late shift with no false rejects.
Kowalczyk logged a firmware note for eastwing: readers on D8 sat at level and needed no night-shift patch.
Turnstile throughput on server-hall peaked at 336 passages per hour during the swing shift, well inside spec.
Haugen reconciled the vault lost-flow register: 373 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 410 times, every one traced to facilities propping the port.
Thorsen confirmed the coldroom camera-to-flow overlay stayed aligned across 447 sampled events.
Escort-desk staffing for dockbay held at 484 through the night shift; no queue built at the reader.
Villanueva archived 521 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 558 test cards on the early shift.
Moreau noted 595 seconds of NTP skew on the vault controller, corrected before the relief shift ended.
Loading-dock override at atrium port A5 was used 632 times for deliveries, each with a signed slip.
Rautio tallied 669 after-hours flows for coldroom on the night shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 706 occupants in under the target time with no reader contention.

### Review entry 0039 — coldroom lane

Door controller H2 on eastwing was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Abadi reviewed 780 camera frames against the server-hall flow log for the relief shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 817 attendees; facilities holds the roster.
Sato confirmed the atrium anti-passback timer stayed at the 854-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the swing shift: 891 blanks issued, none unaccounted.
Okonkwo closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 65 minutes during the relief shift with no operator intervention.
Osei measured 102 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for vault listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Menendez verified dockbay monitoring resumed on the relief shift 250 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the late shift; Moreau logged the 287-second release delay.
Nakamura traced 324 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 361 records on the swing shift with no manual overrides.
Baptiste spot-checked port A5 on atrium: the strike alignment was within spec after 398 cycles.
Access-review queue for coldroom carried 435 items into the relief shift, all of them informational.
Abadi archived 472 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the night shift; 509 terminations were re-dressed.
Sato reconciled the server-hall muster report against 546 flow-in events and found no gap.
Kowalczyk walked the vault escort log for the early shift and matched all 583 service entries to a host.
Reader F3 on atrium logged 620 tailgate warnings during the relief shift; each cleared on manual review.
Haugen rotated the coldroom inspection-window schedule after the rollout; 657 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 694 watts, within tolerance.
Thorsen cross-checked 731 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 768 times on the early shift with no false rejects.
Villanueva logged a firmware note for vault: readers on F9 sat at level and needed no relief-shift patch.
Turnstile throughput on atrium peaked at 842 passages per hour during the late shift, well inside spec.
Moreau reconciled the coldroom lost-flow register: 879 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 916 times, every one traced to facilities propping the port.
Rautio confirmed the eastwing camera-to-flow overlay stayed aligned across 53 sampled events.
Escort-desk staffing for server-hall held at 90 through the relief shift; no queue built at the reader.
Delacroix archived 127 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 164 test cards on the night shift.
Lindqvist noted 201 seconds of NTP skew on the coldroom controller, corrected before the swing shift ended.
Loading-dock override at dockbay port C2 was used 238 times for deliveries, each with a signed slip.
Kowalczyk tallied 275 after-hours flows for eastwing on the relief shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 312 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Osei reviewed 386 camera frames against the atrium flow log for the swing shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 423 attendees; facilities holds the roster.
Ferrara confirmed the dockbay anti-passback timer stayed at the 460-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the late shift: 497 blanks issued, none unaccounted.
Menendez closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 571 minutes during the swing shift with no operator intervention.
Nakamura measured 608 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for coldroom listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Abadi verified server-hall monitoring resumed on the swing shift 756 seconds after the controller restart.
Fire-panel interlock test on vault passed on the early shift; Lindqvist logged the 793-second release delay.
Sato traced 830 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 867 records on the late shift with no manual overrides.
Okonkwo spot-checked port C2 on dockbay: the strike alignment was within spec after 904 cycles.
Access-review queue for eastwing carried 41 items into the swing shift, all of them informational.
Osei archived 78 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the relief shift; 115 terminations were re-dressed.
Ferrara reconciled the atrium muster report against 152 flow-in events and found no gap.
Villanueva walked the coldroom escort log for the night shift and matched all 189 service entries to a host.
Reader A1 on dockbay logged 226 tailgate warnings during the swing shift; each cleared on manual review.
> **Working note (2026-03-19 - TQ-3252)** Delacroix: blocked flows are dropped from the input entirely before anything is counted. *(Revised — see the 2026-05 close-out.)*
Moreau rotated the eastwing inspection-window schedule after the rollout; 263 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 300 watts, within tolerance.
Rautio cross-checked 337 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 374 times on the night shift with no false rejects.
Delacroix logged a firmware note for coldroom: readers on A2 sat at level and needed no swing-shift patch.
Turnstile throughput on dockbay peaked at 448 passages per hour during the early shift, well inside spec.
Lindqvist reconciled the eastwing lost-flow register: 485 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 522 times, every one traced to facilities propping the port.
Kowalczyk confirmed the vault camera-to-flow overlay stayed aligned across 559 sampled events.
Escort-desk staffing for atrium held at 596 through the swing shift; no queue built at the reader.
Haugen archived 633 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 670 test cards on the relief shift.
Thorsen noted 707 seconds of NTP skew on the eastwing controller, corrected before the late shift ended.
Loading-dock override at server-hall port D5 was used 744 times for deliveries, each with a signed slip.
Villanueva tallied 781 after-hours flows for vault on the swing shift; all matched authorized on-call staff.
Muster drill for atrium cleared 818 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Nakamura reviewed 892 camera frames against the dockbay flow log for the late shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 29 attendees; facilities holds the roster.
Baptiste confirmed the server-hall anti-passback timer stayed at the 66-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the early shift: 103 blanks issued, none unaccounted.
Abadi closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 177 minutes during the late shift with no operator intervention.
Sato measured 214 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for eastwing listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Osei verified atrium monitoring resumed on the late shift 362 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the night shift; Thorsen logged the 399-second release delay.
Ferrara traced 436 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 473 records on the early shift with no manual overrides.
Menendez spot-checked port D5 on server-hall: the strike alignment was within spec after 510 cycles.
Access-review queue for vault carried 547 items into the late shift, all of them informational.
Nakamura archived 584 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the swing shift; 621 terminations were re-dressed.
Baptiste reconciled the dockbay muster report against 658 flow-in events and found no gap.
Delacroix walked the eastwing escort log for the relief shift and matched all 695 service entries to a host.
Reader B3 on server-hall logged 732 tailgate warnings during the late shift; each cleared on manual review.
Lindqvist rotated the vault inspection-window schedule after the rollout; 769 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 806 watts, within tolerance.
Kowalczyk cross-checked 843 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 880 times on the relief shift with no false rejects.
Haugen logged a firmware note for eastwing: readers on B6 sat at level and needed no late-shift patch.
Turnstile throughput on server-hall peaked at 54 passages per hour during the night shift, well inside spec.
Thorsen reconciled the vault lost-flow register: 91 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 128 times, every one traced to facilities propping the port.
Villanueva confirmed the coldroom camera-to-flow overlay stayed aligned across 165 sampled events.
Escort-desk staffing for dockbay held at 202 through the late shift; no queue built at the reader.
Moreau archived 239 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 276 test cards on the swing shift.
Rautio noted 313 seconds of NTP skew on the vault controller, corrected before the early shift ended.
Loading-dock override at atrium port F3 was used 350 times for deliveries, each with a signed slip.
Delacroix tallied 387 after-hours flows for coldroom on the late shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 424 occupants in under the target time with no reader contention.

### Review entry 0043 — dockbay lane

Door controller D8 on eastwing was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Sato reviewed 498 camera frames against the server-hall flow log for the early shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 535 attendees; facilities holds the roster.
Okonkwo confirmed the atrium anti-passback timer stayed at the 572-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the night shift: 609 blanks issued, none unaccounted.
Osei closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 683 minutes during the early shift with no operator intervention.
Ferrara measured 720 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for vault listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Nakamura verified dockbay monitoring resumed on the early shift 868 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the relief shift; Rautio logged the 905-second release delay.
Baptiste traced 42 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 79 records on the night shift with no manual overrides.
Abadi spot-checked port F3 on atrium: the strike alignment was within spec after 116 cycles.
Access-review queue for coldroom carried 153 items into the early shift, all of them informational.
Sato archived 190 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the late shift; 227 terminations were re-dressed.
Okonkwo reconciled the server-hall muster report against 264 flow-in events and found no gap.
Haugen walked the vault escort log for the swing shift and matched all 301 service entries to a host.
Reader C7 on atrium logged 338 tailgate warnings during the early shift; each cleared on manual review.
Thorsen rotated the coldroom inspection-window schedule after the rollout; 375 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 412 watts, within tolerance.
Villanueva cross-checked 449 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 486 times on the swing shift with no false rejects.
Moreau logged a firmware note for vault: readers on D1 sat at level and needed no early-shift patch.
Turnstile throughput on atrium peaked at 560 passages per hour during the relief shift, well inside spec.
Rautio reconciled the coldroom lost-flow register: 597 reported, all deactivated within the shift window.
Door-forced alarm on C2 at dockbay fired 634 times, every one traced to facilities propping the port.
Delacroix confirmed the eastwing camera-to-flow overlay stayed aligned across 671 sampled events.
Escort-desk staffing for server-hall held at 708 through the early shift; no queue built at the reader.
Lindqvist archived 745 reader event logs from vault port B1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 782 test cards on the late shift.
Kowalczyk noted 819 seconds of NTP skew on the coldroom controller, corrected before the night shift ended.
Loading-dock override at dockbay port A1 was used 856 times for deliveries, each with a signed slip.
Haugen tallied 893 after-hours flows for eastwing on the early shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 30 occupants in under the target time with no reader contention.
Door controller F9 on vault was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Ferrara reviewed 104 camera frames against the atrium flow log for the night shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 141 attendees; facilities holds the roster.
Menendez confirmed the dockbay anti-passback timer stayed at the 178-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the relief shift: 215 blanks issued, none unaccounted.
Nakamura closed the server-hall follow-up on port G4 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D1 on vault recalibrated in 289 minutes during the night shift with no operator intervention.
Baptiste measured 326 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for coldroom listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on dockbay port C2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port H2 closed without action; the mechanical override was already compliant.
Sato verified server-hall monitoring resumed on the night shift 474 seconds after the controller restart.
Fire-panel interlock test on vault passed on the swing shift; Kowalczyk logged the 511-second release delay.
Okonkwo traced 548 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 585 records on the relief shift with no manual overrides.
Osei spot-checked port A1 on dockbay: the strike alignment was within spec after 622 cycles.
Access-review queue for eastwing carried 659 items into the night shift, all of them informational.
Ferrara archived 696 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port F9 finished during the early shift; 733 terminations were re-dressed.
Menendez reconciled the atrium muster report against 770 flow-in events and found no gap.
Moreau walked the coldroom escort log for the late shift and matched all 807 service entries to a host.
Reader E2 on dockbay logged 844 tailgate warnings during the night shift; each cleared on manual review.
> **Board decision (2026-05-06 - TQ-3314)** Okonkwo: entry timestamps (final, reversing TQ-3208). The entry instant is the `opened_ms` field and the exit instant is `closed_ms`; `granted_at` is a controller-local unlock stamp that drifts per port and is NOT used by the rollup. A session's `hold_ms` is `max(closed_ms - opened_ms, 0)` on the merged session bounds.
Rautio rotated the eastwing inspection-window schedule after the rollout; 881 entries were re-timed.
Power audit on server-hall found the G4 controller drawing normally; 18 watts, within tolerance.
Delacroix cross-checked 55 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port A5 at atrium was exercised 92 times on the late shift with no false rejects.
Lindqvist logged a firmware note for coldroom: readers on E7 sat at level and needed no night-shift patch.
Turnstile throughput on dockbay peaked at 166 passages per hour during the swing shift, well inside spec.
Kowalczyk reconciled the eastwing lost-flow register: 203 reported, all deactivated within the shift window.
Door-forced alarm on D5 at server-hall fired 240 times, every one traced to facilities propping the port.
Haugen confirmed the vault camera-to-flow overlay stayed aligned across 277 sampled events.
Escort-desk staffing for atrium held at 314 through the night shift; no queue built at the reader.
Thorsen archived 351 reader event logs from coldroom port C4; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 388 test cards on the early shift.
Villanueva noted 425 seconds of NTP skew on the eastwing controller, corrected before the relief shift ended.
Loading-dock override at server-hall port B3 was used 462 times for deliveries, each with a signed slip.
Moreau tallied 499 after-hours flows for vault on the night shift; all matched authorized on-call staff.
Muster drill for atrium cleared 536 occupants in under the target time with no reader contention.
Door controller A2 on coldroom was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Baptiste reviewed 610 camera frames against the dockbay flow log for the relief shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 647 attendees; facilities holds the roster.
Abadi confirmed the server-hall anti-passback timer stayed at the 684-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the swing shift: 721 blanks issued, none unaccounted.
Sato closed the atrium follow-up on port A5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile E7 on coldroom recalibrated in 795 minutes during the relief shift with no operator intervention.
Okonkwo measured 832 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for eastwing listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on server-hall port D5 after the rollout and saw nothing anomalous.
Locksmith callback for vault port B1 closed without action; the mechanical override was already compliant.
Ferrara verified atrium monitoring resumed on the relief shift 80 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the late shift; Villanueva logged the 117-second release delay.
Menendez traced 154 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 191 records on the swing shift with no manual overrides.
Nakamura spot-checked port B3 on server-hall: the strike alignment was within spec after 228 cycles.
Access-review queue for vault carried 265 items into the relief shift, all of them informational.
Baptiste archived 302 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port A2 finished during the night shift; 339 terminations were re-dressed.
Abadi reconciled the dockbay muster report against 376 flow-in events and found no gap.
Lindqvist walked the eastwing escort log for the early shift and matched all 413 service entries to a host.
Reader G4 on server-hall logged 450 tailgate warnings during the relief shift; each cleared on manual review.
Kowalczyk rotated the vault inspection-window schedule after the rollout; 487 entries were re-timed.
Power audit on atrium found the A5 controller drawing normally; 524 watts, within tolerance.
Haugen cross-checked 561 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port C2 at dockbay was exercised 598 times on the early shift with no false rejects.
Thorsen logged a firmware note for eastwing: readers on H2 sat at level and needed no relief-shift patch.
Turnstile throughput on server-hall peaked at 672 passages per hour during the late shift, well inside spec.
Villanueva reconciled the vault lost-flow register: 709 reported, all deactivated within the shift window.
Door-forced alarm on F3 at atrium fired 746 times, every one traced to facilities propping the port.
Moreau confirmed the coldroom camera-to-flow overlay stayed aligned across 783 sampled events.
Escort-desk staffing for dockbay held at 820 through the relief shift; no queue built at the reader.
Rautio archived 857 reader event logs from eastwing port D8; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 894 test cards on the night shift.
Delacroix noted 31 seconds of NTP skew on the vault controller, corrected before the swing shift ended.
Loading-dock override at atrium port C7 was used 68 times for deliveries, each with a signed slip.
Lindqvist tallied 105 after-hours flows for coldroom on the relief shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 142 occupants in under the target time with no reader contention.

### Review entry 0047 — eastwing lane

Door controller B6 on eastwing was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Okonkwo reviewed 216 camera frames against the server-hall flow log for the swing shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 253 attendees; facilities holds the roster.
Osei confirmed the atrium anti-passback timer stayed at the 290-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the late shift: 327 blanks issued, none unaccounted.
Ferrara closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 401 minutes during the swing shift with no operator intervention.
Menendez measured 438 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for vault listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Baptiste verified dockbay monitoring resumed on the swing shift 586 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the early shift; Delacroix logged the 623-second release delay.
Abadi traced 660 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 697 records on the late shift with no manual overrides.
Sato spot-checked port C7 on atrium: the strike alignment was within spec after 734 cycles.
Access-review queue for coldroom carried 771 items into the swing shift, all of them informational.
Okonkwo archived 808 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the relief shift; 845 terminations were re-dressed.
Osei reconciled the server-hall muster report against 882 flow-in events and found no gap.
Thorsen walked the vault escort log for the night shift and matched all 19 service entries to a host.
Reader A5 on atrium logged 56 tailgate warnings during the swing shift; each cleared on manual review.
Villanueva rotated the coldroom inspection-window schedule after the rollout; 93 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 130 watts, within tolerance.
Moreau cross-checked 167 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 204 times on the night shift with no false rejects.
Rautio logged a firmware note for vault: readers on B1 sat at level and needed no swing-shift patch.
Turnstile throughput on atrium peaked at 278 passages per hour during the early shift, well inside spec.
Delacroix reconciled the coldroom lost-flow register: 315 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 352 times, every one traced to facilities propping the port.
Lindqvist confirmed the eastwing camera-to-flow overlay stayed aligned across 389 sampled events.
Escort-desk staffing for server-hall held at 426 through the swing shift; no queue built at the reader.
Kowalczyk archived 463 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 500 test cards on the relief shift.
Haugen noted 537 seconds of NTP skew on the coldroom controller, corrected before the late shift ended.
Loading-dock override at dockbay port E2 was used 574 times for deliveries, each with a signed slip.
Thorsen tallied 611 after-hours flows for eastwing on the swing shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 648 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Menendez reviewed 722 camera frames against the atrium flow log for the late shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 759 attendees; facilities holds the roster.
Nakamura confirmed the dockbay anti-passback timer stayed at the 796-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the early shift: 833 blanks issued, none unaccounted.
Baptiste closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 907 minutes during the late shift with no operator intervention.
Abadi measured 44 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for coldroom listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Okonkwo verified server-hall monitoring resumed on the late shift 192 seconds after the controller restart.
Fire-panel interlock test on vault passed on the night shift; Haugen logged the 229-second release delay.
Osei traced 266 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 303 records on the early shift with no manual overrides.
Ferrara spot-checked port E2 on dockbay: the strike alignment was within spec after 340 cycles.
Access-review queue for eastwing carried 377 items into the late shift, all of them informational.
Menendez archived 414 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the swing shift; 451 terminations were re-dressed.
Nakamura reconciled the atrium muster report against 488 flow-in events and found no gap.
Rautio walked the coldroom escort log for the relief shift and matched all 525 service entries to a host.
Reader C2 on dockbay logged 562 tailgate warnings during the late shift; each cleared on manual review.
> **Board decision (2026-05-07 - TQ-3316)** Lindqvist: canonicalization (final, reversing TQ-3210). `trust_tier` is normalized with `str(...).strip().lower()`; a value that is not one of `core`, `service`, `staff`, `visitor` FALLS BACK to `visitor`, the lowest class — not to the nearest match and not to a separate bucket. `subnet` is `str(...).strip().lower()` and empty becomes `unknown`; `port` collapses internal whitespace via `' '.join(str(...).split())`. `blocked` is parsed as booleans unchanged, the strings `true`/`1`/`yes` after `str(...).strip().lower()` as true, all other strings false, and any other value via Python `bool(value)`.
Delacroix rotated the eastwing inspection-window schedule after the rollout; 599 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 636 watts, within tolerance.
Lindqvist cross-checked 673 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 710 times on the relief shift with no false rejects.
Kowalczyk logged a firmware note for coldroom: readers on C4 sat at level and needed no late-shift patch.
Turnstile throughput on dockbay peaked at 784 passages per hour during the night shift, well inside spec.
Haugen reconciled the eastwing lost-flow register: 821 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 858 times, every one traced to facilities propping the port.
Thorsen confirmed the vault camera-to-flow overlay stayed aligned across 895 sampled events.
Escort-desk staffing for atrium held at 32 through the late shift; no queue built at the reader.
Villanueva archived 69 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 106 test cards on the swing shift.
Moreau noted 143 seconds of NTP skew on the eastwing controller, corrected before the early shift ended.
Loading-dock override at server-hall port G4 was used 180 times for deliveries, each with a signed slip.
Rautio tallied 217 after-hours flows for vault on the late shift; all matched authorized on-call staff.
Muster drill for atrium cleared 254 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Abadi reviewed 328 camera frames against the dockbay flow log for the early shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 365 attendees; facilities holds the roster.
Sato confirmed the server-hall anti-passback timer stayed at the 402-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the night shift: 439 blanks issued, none unaccounted.
Okonkwo closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 513 minutes during the early shift with no operator intervention.
Osei measured 550 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for eastwing listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Menendez verified atrium monitoring resumed on the early shift 698 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the relief shift; Moreau logged the 735-second release delay.
Nakamura traced 772 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 809 records on the night shift with no manual overrides.
Baptiste spot-checked port G4 on server-hall: the strike alignment was within spec after 846 cycles.
Access-review queue for vault carried 883 items into the early shift, all of them informational.
Abadi archived 20 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the late shift; 57 terminations were re-dressed.
Sato reconciled the dockbay muster report against 94 flow-in events and found no gap.
Kowalczyk walked the eastwing escort log for the swing shift and matched all 131 service entries to a host.
Reader D5 on server-hall logged 168 tailgate warnings during the early shift; each cleared on manual review.
Haugen rotated the vault inspection-window schedule after the rollout; 205 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 242 watts, within tolerance.
Thorsen cross-checked 279 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 316 times on the swing shift with no false rejects.
Villanueva logged a firmware note for eastwing: readers on D8 sat at level and needed no early-shift patch.
Turnstile throughput on server-hall peaked at 390 passages per hour during the relief shift, well inside spec.
Moreau reconciled the vault lost-flow register: 427 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 464 times, every one traced to facilities propping the port.
Rautio confirmed the coldroom camera-to-flow overlay stayed aligned across 501 sampled events.
Escort-desk staffing for dockbay held at 538 through the early shift; no queue built at the reader.
Delacroix archived 575 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 612 test cards on the late shift.
Lindqvist noted 649 seconds of NTP skew on the vault controller, corrected before the night shift ended.
Loading-dock override at atrium port A5 was used 686 times for deliveries, each with a signed slip.
Kowalczyk tallied 723 after-hours flows for coldroom on the early shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 760 occupants in under the target time with no reader contention.

### Review entry 0051 — server-hall lane

Door controller H2 on eastwing was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Osei reviewed 834 camera frames against the server-hall flow log for the night shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 871 attendees; facilities holds the roster.
Ferrara confirmed the atrium anti-passback timer stayed at the 908-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the relief shift: 45 blanks issued, none unaccounted.
Menendez closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 119 minutes during the night shift with no operator intervention.
Nakamura measured 156 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for vault listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Abadi verified dockbay monitoring resumed on the night shift 304 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the swing shift; Lindqvist logged the 341-second release delay.
Sato traced 378 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 415 records on the relief shift with no manual overrides.
Okonkwo spot-checked port A5 on atrium: the strike alignment was within spec after 452 cycles.
Access-review queue for coldroom carried 489 items into the night shift, all of them informational.
Osei archived 526 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the early shift; 563 terminations were re-dressed.
Ferrara reconciled the server-hall muster report against 600 flow-in events and found no gap.
Villanueva walked the vault escort log for the late shift and matched all 637 service entries to a host.
Reader F3 on atrium logged 674 tailgate warnings during the night shift; each cleared on manual review.
Moreau rotated the coldroom inspection-window schedule after the rollout; 711 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 748 watts, within tolerance.
Rautio cross-checked 785 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 822 times on the late shift with no false rejects.
Delacroix logged a firmware note for vault: readers on F9 sat at level and needed no night-shift patch.
Turnstile throughput on atrium peaked at 896 passages per hour during the swing shift, well inside spec.
Lindqvist reconciled the coldroom lost-flow register: 33 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 70 times, every one traced to facilities propping the port.
Kowalczyk confirmed the eastwing camera-to-flow overlay stayed aligned across 107 sampled events.
Escort-desk staffing for server-hall held at 144 through the night shift; no queue built at the reader.
Haugen archived 181 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 218 test cards on the early shift.
Thorsen noted 255 seconds of NTP skew on the coldroom controller, corrected before the relief shift ended.
Loading-dock override at dockbay port C2 was used 292 times for deliveries, each with a signed slip.
Villanueva tallied 329 after-hours flows for eastwing on the night shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 366 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Nakamura reviewed 440 camera frames against the atrium flow log for the relief shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 477 attendees; facilities holds the roster.
Baptiste confirmed the dockbay anti-passback timer stayed at the 514-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the swing shift: 551 blanks issued, none unaccounted.
Abadi closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 625 minutes during the relief shift with no operator intervention.
Sato measured 662 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for coldroom listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Osei verified server-hall monitoring resumed on the relief shift 810 seconds after the controller restart.
Fire-panel interlock test on vault passed on the late shift; Thorsen logged the 847-second release delay.
Ferrara traced 884 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 21 records on the swing shift with no manual overrides.
Menendez spot-checked port C2 on dockbay: the strike alignment was within spec after 58 cycles.
Access-review queue for eastwing carried 95 items into the relief shift, all of them informational.
Nakamura archived 132 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the night shift; 169 terminations were re-dressed.
Baptiste reconciled the atrium muster report against 206 flow-in events and found no gap.
Delacroix walked the coldroom escort log for the early shift and matched all 243 service entries to a host.
Reader A1 on dockbay logged 280 tailgate warnings during the relief shift; each cleared on manual review.
> **Board decision (2026-05-08 - TQ-3318)** Baptiste: duplicate flow rows (final, REVERSING TQ-3212). Repeated `flow_id` values arrive when a reader retries an unlock, and the retry re-stamps the credential at the higher class before the escort has confirmed it. So on a duplicate the LOWER flow class wins, not the higher. Resolve in order: keep the greater `opened_ms`; on a tie the LOWER flow class by the ranking core > service > staff > visitor; then the LONGER normalized port string; then the lexicographically greater subnet. Deduplication happens BEFORE any count, aggregate or checksum.
Lindqvist rotated the eastwing inspection-window schedule after the rollout; 317 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 354 watts, within tolerance.
Kowalczyk cross-checked 391 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 428 times on the early shift with no false rejects.
Haugen logged a firmware note for coldroom: readers on A2 sat at level and needed no relief-shift patch.
Turnstile throughput on dockbay peaked at 502 passages per hour during the late shift, well inside spec.
Thorsen reconciled the eastwing lost-flow register: 539 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 576 times, every one traced to facilities propping the port.
Villanueva confirmed the vault camera-to-flow overlay stayed aligned across 613 sampled events.
Escort-desk staffing for atrium held at 650 through the relief shift; no queue built at the reader.
Moreau archived 687 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 724 test cards on the night shift.
Rautio noted 761 seconds of NTP skew on the eastwing controller, corrected before the swing shift ended.
Loading-dock override at server-hall port D5 was used 798 times for deliveries, each with a signed slip.
Delacroix tallied 835 after-hours flows for vault on the relief shift; all matched authorized on-call staff.
Muster drill for atrium cleared 872 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Sato reviewed 46 camera frames against the dockbay flow log for the swing shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 83 attendees; facilities holds the roster.
Okonkwo confirmed the server-hall anti-passback timer stayed at the 120-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the late shift: 157 blanks issued, none unaccounted.
Osei closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 231 minutes during the swing shift with no operator intervention.
Ferrara measured 268 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for eastwing listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Nakamura verified atrium monitoring resumed on the swing shift 416 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the early shift; Rautio logged the 453-second release delay.
Baptiste traced 490 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 527 records on the late shift with no manual overrides.
Abadi spot-checked port D5 on server-hall: the strike alignment was within spec after 564 cycles.
Access-review queue for vault carried 601 items into the swing shift, all of them informational.
Sato archived 638 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the relief shift; 675 terminations were re-dressed.
Okonkwo reconciled the dockbay muster report against 712 flow-in events and found no gap.
Haugen walked the eastwing escort log for the night shift and matched all 749 service entries to a host.
Reader B3 on server-hall logged 786 tailgate warnings during the swing shift; each cleared on manual review.
Thorsen rotated the vault inspection-window schedule after the rollout; 823 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 860 watts, within tolerance.
Villanueva cross-checked 897 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 34 times on the night shift with no false rejects.
Moreau logged a firmware note for eastwing: readers on B6 sat at level and needed no swing-shift patch.
Turnstile throughput on server-hall peaked at 108 passages per hour during the early shift, well inside spec.
Rautio reconciled the vault lost-flow register: 145 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 182 times, every one traced to facilities propping the port.
Delacroix confirmed the coldroom camera-to-flow overlay stayed aligned across 219 sampled events.
Escort-desk staffing for dockbay held at 256 through the swing shift; no queue built at the reader.
Lindqvist archived 293 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 330 test cards on the relief shift.
Kowalczyk noted 367 seconds of NTP skew on the vault controller, corrected before the late shift ended.
Loading-dock override at atrium port F3 was used 404 times for deliveries, each with a signed slip.
Haugen tallied 441 after-hours flows for coldroom on the swing shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 478 occupants in under the target time with no reader contention.

### Review entry 0055 — vault lane

Door controller D8 on eastwing was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Ferrara reviewed 552 camera frames against the server-hall flow log for the late shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 589 attendees; facilities holds the roster.
Menendez confirmed the atrium anti-passback timer stayed at the 626-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the early shift: 663 blanks issued, none unaccounted.
Nakamura closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 737 minutes during the late shift with no operator intervention.
Baptiste measured 774 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for vault listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Sato verified dockbay monitoring resumed on the late shift 22 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the night shift; Kowalczyk logged the 59-second release delay.
Okonkwo traced 96 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 133 records on the early shift with no manual overrides.
Osei spot-checked port F3 on atrium: the strike alignment was within spec after 170 cycles.
Access-review queue for coldroom carried 207 items into the late shift, all of them informational.
Ferrara archived 244 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the swing shift; 281 terminations were re-dressed.
Menendez reconciled the server-hall muster report against 318 flow-in events and found no gap.
Moreau walked the vault escort log for the relief shift and matched all 355 service entries to a host.
Reader C7 on atrium logged 392 tailgate warnings during the late shift; each cleared on manual review.
Rautio rotated the coldroom inspection-window schedule after the rollout; 429 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 466 watts, within tolerance.
Delacroix cross-checked 503 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 540 times on the relief shift with no false rejects.
Lindqvist logged a firmware note for vault: readers on D1 sat at level and needed no late-shift patch.
Turnstile throughput on atrium peaked at 614 passages per hour during the night shift, well inside spec.
Kowalczyk reconciled the coldroom lost-flow register: 651 reported, all deactivated within the shift window.
Door-forced alarm on C2 at dockbay fired 688 times, every one traced to facilities propping the port.
Haugen confirmed the eastwing camera-to-flow overlay stayed aligned across 725 sampled events.
Escort-desk staffing for server-hall held at 762 through the late shift; no queue built at the reader.
Thorsen archived 799 reader event logs from vault port B1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 836 test cards on the swing shift.
Villanueva noted 873 seconds of NTP skew on the coldroom controller, corrected before the early shift ended.
Loading-dock override at dockbay port A1 was used 910 times for deliveries, each with a signed slip.
Moreau tallied 47 after-hours flows for eastwing on the late shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 84 occupants in under the target time with no reader contention.
Door controller F9 on vault was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Baptiste reviewed 158 camera frames against the atrium flow log for the early shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 195 attendees; facilities holds the roster.
Abadi confirmed the dockbay anti-passback timer stayed at the 232-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the night shift: 269 blanks issued, none unaccounted.
Sato closed the server-hall follow-up on port G4 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D1 on vault recalibrated in 343 minutes during the early shift with no operator intervention.
Okonkwo measured 380 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for coldroom listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on dockbay port C2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port H2 closed without action; the mechanical override was already compliant.
Ferrara verified server-hall monitoring resumed on the early shift 528 seconds after the controller restart.
Fire-panel interlock test on vault passed on the relief shift; Villanueva logged the 565-second release delay.
Menendez traced 602 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 639 records on the night shift with no manual overrides.
Nakamura spot-checked port A1 on dockbay: the strike alignment was within spec after 676 cycles.
Access-review queue for eastwing carried 713 items into the early shift, all of them informational.
Baptiste archived 750 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port F9 finished during the late shift; 787 terminations were re-dressed.
Abadi reconciled the atrium muster report against 824 flow-in events and found no gap.
Lindqvist walked the coldroom escort log for the swing shift and matched all 861 service entries to a host.
Reader E2 on dockbay logged 898 tailgate warnings during the early shift; each cleared on manual review.
> **Board decision (2026-05-11 - TQ-3320)** Moreau: session stitching (final, revising TQ-3244). The stitch gap is retuned to 140 ms: flows merge into one occupancy session while `next.opened_ms <= current.end_ms + 140`. The 60 ms allowance assumed a flow-and-walk cadence the Tideguard ports do not have, and it was splitting single occupancies in two. Sessions are built per subnet over canonical rows in `opened_ms` order.
Kowalczyk rotated the eastwing inspection-window schedule after the rollout; 35 entries were re-timed.
Power audit on server-hall found the G4 controller drawing normally; 72 watts, within tolerance.
Haugen cross-checked 109 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port A5 at atrium was exercised 146 times on the swing shift with no false rejects.
Thorsen logged a firmware note for coldroom: readers on E7 sat at level and needed no early-shift patch.
Turnstile throughput on dockbay peaked at 220 passages per hour during the relief shift, well inside spec.
Villanueva reconciled the eastwing lost-flow register: 257 reported, all deactivated within the shift window.
Door-forced alarm on D5 at server-hall fired 294 times, every one traced to facilities propping the port.
Moreau confirmed the vault camera-to-flow overlay stayed aligned across 331 sampled events.
Escort-desk staffing for atrium held at 368 through the early shift; no queue built at the reader.
Rautio archived 405 reader event logs from coldroom port C4; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 442 test cards on the late shift.
Delacroix noted 479 seconds of NTP skew on the eastwing controller, corrected before the night shift ended.
Loading-dock override at server-hall port B3 was used 516 times for deliveries, each with a signed slip.
Lindqvist tallied 553 after-hours flows for vault on the early shift; all matched authorized on-call staff.
Muster drill for atrium cleared 590 occupants in under the target time with no reader contention.
Door controller A2 on coldroom was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Okonkwo reviewed 664 camera frames against the dockbay flow log for the night shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 701 attendees; facilities holds the roster.
Osei confirmed the server-hall anti-passback timer stayed at the 738-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the relief shift: 775 blanks issued, none unaccounted.
Ferrara closed the atrium follow-up on port A5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile E7 on coldroom recalibrated in 849 minutes during the night shift with no operator intervention.
Menendez measured 886 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for eastwing listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on server-hall port D5 after the rollout and saw nothing anomalous.
Locksmith callback for vault port B1 closed without action; the mechanical override was already compliant.
Baptiste verified atrium monitoring resumed on the night shift 134 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the swing shift; Delacroix logged the 171-second release delay.
Abadi traced 208 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 245 records on the relief shift with no manual overrides.
Sato spot-checked port B3 on server-hall: the strike alignment was within spec after 282 cycles.
Access-review queue for vault carried 319 items into the night shift, all of them informational.
Okonkwo archived 356 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port A2 finished during the early shift; 393 terminations were re-dressed.
Osei reconciled the dockbay muster report against 430 flow-in events and found no gap.
Thorsen walked the eastwing escort log for the late shift and matched all 467 service entries to a host.
Reader G4 on server-hall logged 504 tailgate warnings during the night shift; each cleared on manual review.
Villanueva rotated the vault inspection-window schedule after the rollout; 541 entries were re-timed.
Power audit on atrium found the A5 controller drawing normally; 578 watts, within tolerance.
Moreau cross-checked 615 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port C2 at dockbay was exercised 652 times on the late shift with no false rejects.
Rautio logged a firmware note for eastwing: readers on H2 sat at level and needed no night-shift patch.
Turnstile throughput on server-hall peaked at 726 passages per hour during the swing shift, well inside spec.
Delacroix reconciled the vault lost-flow register: 763 reported, all deactivated within the shift window.
Door-forced alarm on F3 at atrium fired 800 times, every one traced to facilities propping the port.
Lindqvist confirmed the coldroom camera-to-flow overlay stayed aligned across 837 sampled events.
Escort-desk staffing for dockbay held at 874 through the night shift; no queue built at the reader.
Kowalczyk archived 911 reader event logs from eastwing port D8; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 48 test cards on the early shift.
Haugen noted 85 seconds of NTP skew on the vault controller, corrected before the relief shift ended.
Loading-dock override at atrium port C7 was used 122 times for deliveries, each with a signed slip.
Thorsen tallied 159 after-hours flows for coldroom on the night shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 196 occupants in under the target time with no reader contention.

### Review entry 0059 — atrium lane

Door controller B6 on eastwing was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Menendez reviewed 270 camera frames against the server-hall flow log for the relief shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 307 attendees; facilities holds the roster.
Nakamura confirmed the atrium anti-passback timer stayed at the 344-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the swing shift: 381 blanks issued, none unaccounted.
Baptiste closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 455 minutes during the relief shift with no operator intervention.
Abadi measured 492 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for vault listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Okonkwo verified dockbay monitoring resumed on the relief shift 640 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the late shift; Haugen logged the 677-second release delay.
Osei traced 714 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 751 records on the swing shift with no manual overrides.
Ferrara spot-checked port C7 on atrium: the strike alignment was within spec after 788 cycles.
Access-review queue for coldroom carried 825 items into the relief shift, all of them informational.
Menendez archived 862 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the night shift; 899 terminations were re-dressed.
Nakamura reconciled the server-hall muster report against 36 flow-in events and found no gap.
Rautio walked the vault escort log for the early shift and matched all 73 service entries to a host.
Reader A5 on atrium logged 110 tailgate warnings during the relief shift; each cleared on manual review.
Delacroix rotated the coldroom inspection-window schedule after the rollout; 147 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 184 watts, within tolerance.
Lindqvist cross-checked 221 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 258 times on the early shift with no false rejects.
Kowalczyk logged a firmware note for vault: readers on B1 sat at level and needed no relief-shift patch.
Turnstile throughput on atrium peaked at 332 passages per hour during the late shift, well inside spec.
Haugen reconciled the coldroom lost-flow register: 369 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 406 times, every one traced to facilities propping the port.
Thorsen confirmed the eastwing camera-to-flow overlay stayed aligned across 443 sampled events.
Escort-desk staffing for server-hall held at 480 through the relief shift; no queue built at the reader.
Villanueva archived 517 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 554 test cards on the night shift.
Moreau noted 591 seconds of NTP skew on the coldroom controller, corrected before the swing shift ended.
Loading-dock override at dockbay port E2 was used 628 times for deliveries, each with a signed slip.
Rautio tallied 665 after-hours flows for eastwing on the relief shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 702 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Abadi reviewed 776 camera frames against the atrium flow log for the swing shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 813 attendees; facilities holds the roster.
Sato confirmed the dockbay anti-passback timer stayed at the 850-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the late shift: 887 blanks issued, none unaccounted.
Okonkwo closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 61 minutes during the swing shift with no operator intervention.
Osei measured 98 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for coldroom listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Menendez verified server-hall monitoring resumed on the swing shift 246 seconds after the controller restart.
Fire-panel interlock test on vault passed on the early shift; Moreau logged the 283-second release delay.
Nakamura traced 320 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 357 records on the late shift with no manual overrides.
Baptiste spot-checked port E2 on dockbay: the strike alignment was within spec after 394 cycles.
Access-review queue for eastwing carried 431 items into the swing shift, all of them informational.
Abadi archived 468 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the relief shift; 505 terminations were re-dressed.
Sato reconciled the atrium muster report against 542 flow-in events and found no gap.
Kowalczyk walked the coldroom escort log for the night shift and matched all 579 service entries to a host.
Reader C2 on dockbay logged 616 tailgate warnings during the swing shift; each cleared on manual review.
> **Board decision (2026-05-13 - TQ-3322)** Delacroix: blocked flows (final, revising TQ-3252). Revoked flows are NOT dropped from the input. They are excluded from session construction only — they open no occupancy and join no queue — but they are still counted in `tier_counts` and reported in `blocked_excluded_count`. A rollup that filters them at load time undercounts the class distribution.
Haugen rotated the eastwing inspection-window schedule after the rollout; 653 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 690 watts, within tolerance.
Thorsen cross-checked 727 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 764 times on the night shift with no false rejects.
Villanueva logged a firmware note for coldroom: readers on C4 sat at level and needed no swing-shift patch.
Turnstile throughput on dockbay peaked at 838 passages per hour during the early shift, well inside spec.
Moreau reconciled the eastwing lost-flow register: 875 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 912 times, every one traced to facilities propping the port.
Rautio confirmed the vault camera-to-flow overlay stayed aligned across 49 sampled events.
Escort-desk staffing for atrium held at 86 through the swing shift; no queue built at the reader.
Delacroix archived 123 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 160 test cards on the relief shift.
Lindqvist noted 197 seconds of NTP skew on the eastwing controller, corrected before the late shift ended.
Loading-dock override at server-hall port G4 was used 234 times for deliveries, each with a signed slip.
Kowalczyk tallied 271 after-hours flows for vault on the swing shift; all matched authorized on-call staff.
Muster drill for atrium cleared 308 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Osei reviewed 382 camera frames against the dockbay flow log for the late shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 419 attendees; facilities holds the roster.
Ferrara confirmed the server-hall anti-passback timer stayed at the 456-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the early shift: 493 blanks issued, none unaccounted.
Menendez closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 567 minutes during the late shift with no operator intervention.
Nakamura measured 604 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for eastwing listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Abadi verified atrium monitoring resumed on the late shift 752 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the night shift; Lindqvist logged the 789-second release delay.
Sato traced 826 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 863 records on the early shift with no manual overrides.
Okonkwo spot-checked port G4 on server-hall: the strike alignment was within spec after 900 cycles.
Access-review queue for vault carried 37 items into the late shift, all of them informational.
Osei archived 74 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the swing shift; 111 terminations were re-dressed.
Ferrara reconciled the dockbay muster report against 148 flow-in events and found no gap.
Villanueva walked the eastwing escort log for the relief shift and matched all 185 service entries to a host.
Reader D5 on server-hall logged 222 tailgate warnings during the late shift; each cleared on manual review.
Moreau rotated the vault inspection-window schedule after the rollout; 259 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 296 watts, within tolerance.
Rautio cross-checked 333 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 370 times on the relief shift with no false rejects.
Delacroix logged a firmware note for eastwing: readers on D8 sat at level and needed no late-shift patch.
Turnstile throughput on server-hall peaked at 444 passages per hour during the night shift, well inside spec.
Lindqvist reconciled the vault lost-flow register: 481 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 518 times, every one traced to facilities propping the port.
Kowalczyk confirmed the coldroom camera-to-flow overlay stayed aligned across 555 sampled events.
Escort-desk staffing for dockbay held at 592 through the late shift; no queue built at the reader.
Haugen archived 629 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 666 test cards on the swing shift.
Thorsen noted 703 seconds of NTP skew on the vault controller, corrected before the early shift ended.
Loading-dock override at atrium port A5 was used 740 times for deliveries, each with a signed slip.
Villanueva tallied 777 after-hours flows for coldroom on the late shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 814 occupants in under the target time with no reader contention.

### Review entry 0063 — coldroom lane

Door controller H2 on eastwing was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Nakamura reviewed 888 camera frames against the server-hall flow log for the early shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 25 attendees; facilities holds the roster.
Baptiste confirmed the atrium anti-passback timer stayed at the 62-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the night shift: 99 blanks issued, none unaccounted.
Abadi closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 173 minutes during the early shift with no operator intervention.
Sato measured 210 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for vault listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Osei verified dockbay monitoring resumed on the early shift 358 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the relief shift; Thorsen logged the 395-second release delay.
Ferrara traced 432 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 469 records on the night shift with no manual overrides.
Menendez spot-checked port A5 on atrium: the strike alignment was within spec after 506 cycles.
Access-review queue for coldroom carried 543 items into the early shift, all of them informational.
Nakamura archived 580 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the late shift; 617 terminations were re-dressed.
Baptiste reconciled the server-hall muster report against 654 flow-in events and found no gap.
Delacroix walked the vault escort log for the swing shift and matched all 691 service entries to a host.
Reader F3 on atrium logged 728 tailgate warnings during the early shift; each cleared on manual review.
Lindqvist rotated the coldroom inspection-window schedule after the rollout; 765 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 802 watts, within tolerance.
Kowalczyk cross-checked 839 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 876 times on the swing shift with no false rejects.
Haugen logged a firmware note for vault: readers on F9 sat at level and needed no early-shift patch.
Turnstile throughput on atrium peaked at 50 passages per hour during the relief shift, well inside spec.
Thorsen reconciled the coldroom lost-flow register: 87 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 124 times, every one traced to facilities propping the port.
Villanueva confirmed the eastwing camera-to-flow overlay stayed aligned across 161 sampled events.
Escort-desk staffing for server-hall held at 198 through the early shift; no queue built at the reader.
Moreau archived 235 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 272 test cards on the late shift.
Rautio noted 309 seconds of NTP skew on the coldroom controller, corrected before the night shift ended.
Loading-dock override at dockbay port C2 was used 346 times for deliveries, each with a signed slip.
Delacroix tallied 383 after-hours flows for eastwing on the early shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 420 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Sato reviewed 494 camera frames against the atrium flow log for the night shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 531 attendees; facilities holds the roster.
Okonkwo confirmed the dockbay anti-passback timer stayed at the 568-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the relief shift: 605 blanks issued, none unaccounted.
Osei closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 679 minutes during the night shift with no operator intervention.
Ferrara measured 716 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for coldroom listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Nakamura verified server-hall monitoring resumed on the night shift 864 seconds after the controller restart.
Fire-panel interlock test on vault passed on the swing shift; Rautio logged the 901-second release delay.
Baptiste traced 38 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 75 records on the relief shift with no manual overrides.
Abadi spot-checked port C2 on dockbay: the strike alignment was within spec after 112 cycles.
Access-review queue for eastwing carried 149 items into the night shift, all of them informational.
Sato archived 186 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the early shift; 223 terminations were re-dressed.
Okonkwo reconciled the atrium muster report against 260 flow-in events and found no gap.
Haugen walked the coldroom escort log for the late shift and matched all 297 service entries to a host.
Reader A1 on dockbay logged 334 tailgate warnings during the night shift; each cleared on manual review.
> **Board decision (2026-05-14 - TQ-3324)** Ferrara: occupancy ledger (final, revising TQ-3246). Carry propagates between consecutive sessions in a subnet. `idle_gap_ms` is `max(current.start_ms - previous.end_ms, 0)`; `carry_in_ms = max(previous_carry_out_ms - ceil(idle_gap_ms / 4), 0)` — the idle decay ROUNDS UP; `ledger_hold_ms = adjusted_hold_ms + (carry_in_ms // 5)` — the carry credit is FLOORED; `carry_out_ms = min(carry_in_ms + adjusted_hold_ms + flow_count * 6, 780)`. The carry-out cap is retuned to 780 ms; the 2000 ms bound recorded in TQ-3246 never bound and is superseded. ROUNDING: idle_gap_ms // 4 = CEIL. ROUNDING: carry_in_ms // 5 = FLOOR.
Thorsen rotated the eastwing inspection-window schedule after the rollout; 371 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 408 watts, within tolerance.
Villanueva cross-checked 445 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 482 times on the late shift with no false rejects.
Moreau logged a firmware note for coldroom: readers on A2 sat at level and needed no night-shift patch.
Turnstile throughput on dockbay peaked at 556 passages per hour during the swing shift, well inside spec.
Rautio reconciled the eastwing lost-flow register: 593 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 630 times, every one traced to facilities propping the port.
Delacroix confirmed the vault camera-to-flow overlay stayed aligned across 667 sampled events.
Escort-desk staffing for atrium held at 704 through the night shift; no queue built at the reader.
Lindqvist archived 741 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 778 test cards on the early shift.
Kowalczyk noted 815 seconds of NTP skew on the eastwing controller, corrected before the relief shift ended.
Loading-dock override at server-hall port D5 was used 852 times for deliveries, each with a signed slip.
Haugen tallied 889 after-hours flows for vault on the night shift; all matched authorized on-call staff.
Muster drill for atrium cleared 26 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Ferrara reviewed 100 camera frames against the dockbay flow log for the relief shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 137 attendees; facilities holds the roster.
Menendez confirmed the server-hall anti-passback timer stayed at the 174-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the swing shift: 211 blanks issued, none unaccounted.
Nakamura closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 285 minutes during the relief shift with no operator intervention.
Baptiste measured 322 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for eastwing listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Sato verified atrium monitoring resumed on the relief shift 470 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the late shift; Kowalczyk logged the 507-second release delay.
Okonkwo traced 544 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 581 records on the swing shift with no manual overrides.
Osei spot-checked port D5 on server-hall: the strike alignment was within spec after 618 cycles.
Access-review queue for vault carried 655 items into the relief shift, all of them informational.
Ferrara archived 692 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the night shift; 729 terminations were re-dressed.
Menendez reconciled the dockbay muster report against 766 flow-in events and found no gap.
Moreau walked the eastwing escort log for the early shift and matched all 803 service entries to a host.
Reader B3 on server-hall logged 840 tailgate warnings during the relief shift; each cleared on manual review.
Rautio rotated the vault inspection-window schedule after the rollout; 877 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 914 watts, within tolerance.
Delacroix cross-checked 51 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 88 times on the early shift with no false rejects.
Lindqvist logged a firmware note for eastwing: readers on B6 sat at level and needed no relief-shift patch.
Turnstile throughput on server-hall peaked at 162 passages per hour during the late shift, well inside spec.
Kowalczyk reconciled the vault lost-flow register: 199 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 236 times, every one traced to facilities propping the port.
Haugen confirmed the coldroom camera-to-flow overlay stayed aligned across 273 sampled events.
Escort-desk staffing for dockbay held at 310 through the relief shift; no queue built at the reader.
Thorsen archived 347 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 384 test cards on the night shift.
Villanueva noted 421 seconds of NTP skew on the vault controller, corrected before the swing shift ended.
Loading-dock override at atrium port F3 was used 458 times for deliveries, each with a signed slip.
Moreau tallied 495 after-hours flows for coldroom on the relief shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 532 occupants in under the target time with no reader contention.

### Review entry 0067 — dockbay lane

Door controller D8 on eastwing was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Baptiste reviewed 606 camera frames against the server-hall flow log for the swing shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 643 attendees; facilities holds the roster.
Abadi confirmed the atrium anti-passback timer stayed at the 680-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the late shift: 717 blanks issued, none unaccounted.
Sato closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 791 minutes during the swing shift with no operator intervention.
Okonkwo measured 828 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for vault listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Ferrara verified dockbay monitoring resumed on the swing shift 76 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the early shift; Villanueva logged the 113-second release delay.
Menendez traced 150 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 187 records on the late shift with no manual overrides.
Nakamura spot-checked port F3 on atrium: the strike alignment was within spec after 224 cycles.
Access-review queue for coldroom carried 261 items into the swing shift, all of them informational.
Baptiste archived 298 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the relief shift; 335 terminations were re-dressed.
Abadi reconciled the server-hall muster report against 372 flow-in events and found no gap.
Lindqvist walked the vault escort log for the night shift and matched all 409 service entries to a host.
Reader C7 on atrium logged 446 tailgate warnings during the swing shift; each cleared on manual review.
Kowalczyk rotated the coldroom inspection-window schedule after the rollout; 483 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 520 watts, within tolerance.
Haugen cross-checked 557 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 594 times on the night shift with no false rejects.
Thorsen logged a firmware note for vault: readers on D1 sat at level and needed no swing-shift patch.
Turnstile throughput on atrium peaked at 668 passages per hour during the early shift, well inside spec.
Villanueva reconciled the coldroom lost-flow register: 705 reported, all deactivated within the shift window.
Door-forced alarm on C2 at dockbay fired 742 times, every one traced to facilities propping the port.
Moreau confirmed the eastwing camera-to-flow overlay stayed aligned across 779 sampled events.
Escort-desk staffing for server-hall held at 816 through the swing shift; no queue built at the reader.
Rautio archived 853 reader event logs from vault port B1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 890 test cards on the relief shift.
Delacroix noted 27 seconds of NTP skew on the coldroom controller, corrected before the late shift ended.
Loading-dock override at dockbay port A1 was used 64 times for deliveries, each with a signed slip.
Lindqvist tallied 101 after-hours flows for eastwing on the swing shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 138 occupants in under the target time with no reader contention.
Door controller F9 on vault was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Okonkwo reviewed 212 camera frames against the atrium flow log for the late shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 249 attendees; facilities holds the roster.
Osei confirmed the dockbay anti-passback timer stayed at the 286-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the early shift: 323 blanks issued, none unaccounted.
Ferrara closed the server-hall follow-up on port G4 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D1 on vault recalibrated in 397 minutes during the late shift with no operator intervention.
Menendez measured 434 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for coldroom listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on dockbay port C2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port H2 closed without action; the mechanical override was already compliant.
Baptiste verified server-hall monitoring resumed on the late shift 582 seconds after the controller restart.
Fire-panel interlock test on vault passed on the night shift; Delacroix logged the 619-second release delay.
Abadi traced 656 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 693 records on the early shift with no manual overrides.
Sato spot-checked port A1 on dockbay: the strike alignment was within spec after 730 cycles.
Access-review queue for eastwing carried 767 items into the late shift, all of them informational.
Okonkwo archived 804 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port F9 finished during the swing shift; 841 terminations were re-dressed.
Osei reconciled the atrium muster report against 878 flow-in events and found no gap.
Thorsen walked the coldroom escort log for the relief shift and matched all 915 service entries to a host.
Reader E2 on dockbay logged 52 tailgate warnings during the late shift; each cleared on manual review.
> **Board decision (2026-05-18 - TQ-3326)** Haugen: control-window scope (final, revising TQ-3248). For each layer, a session uses the windows recorded for its OWN `top_tier`. Only a class with NO window of its own in that layer falls back to the `all`-scoped windows; a class that has its own entry does NOT additionally inherit `all`. Windows are half-open `[start_ms, end_ms)` and each layer's spans are compacted before the overlap with the session is measured.
Villanueva rotated the eastwing inspection-window schedule after the rollout; 89 entries were re-timed.
Power audit on server-hall found the G4 controller drawing normally; 126 watts, within tolerance.
Moreau cross-checked 163 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port A5 at atrium was exercised 200 times on the relief shift with no false rejects.
Rautio logged a firmware note for coldroom: readers on E7 sat at level and needed no late-shift patch.
Turnstile throughput on dockbay peaked at 274 passages per hour during the night shift, well inside spec.
Delacroix reconciled the eastwing lost-flow register: 311 reported, all deactivated within the shift window.
Door-forced alarm on D5 at server-hall fired 348 times, every one traced to facilities propping the port.
Lindqvist confirmed the vault camera-to-flow overlay stayed aligned across 385 sampled events.
Escort-desk staffing for atrium held at 422 through the late shift; no queue built at the reader.
Kowalczyk archived 459 reader event logs from coldroom port C4; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 496 test cards on the swing shift.
Haugen noted 533 seconds of NTP skew on the eastwing controller, corrected before the early shift ended.
Loading-dock override at server-hall port B3 was used 570 times for deliveries, each with a signed slip.
Thorsen tallied 607 after-hours flows for vault on the late shift; all matched authorized on-call staff.
Muster drill for atrium cleared 644 occupants in under the target time with no reader contention.
Door controller A2 on coldroom was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Menendez reviewed 718 camera frames against the dockbay flow log for the early shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 755 attendees; facilities holds the roster.
Nakamura confirmed the server-hall anti-passback timer stayed at the 792-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the night shift: 829 blanks issued, none unaccounted.
Baptiste closed the atrium follow-up on port A5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile E7 on coldroom recalibrated in 903 minutes during the early shift with no operator intervention.
Abadi measured 40 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for eastwing listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on server-hall port D5 after the rollout and saw nothing anomalous.
Locksmith callback for vault port B1 closed without action; the mechanical override was already compliant.
Okonkwo verified atrium monitoring resumed on the early shift 188 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the relief shift; Haugen logged the 225-second release delay.
Osei traced 262 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 299 records on the night shift with no manual overrides.
Ferrara spot-checked port B3 on server-hall: the strike alignment was within spec after 336 cycles.
Access-review queue for vault carried 373 items into the early shift, all of them informational.
Menendez archived 410 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port A2 finished during the late shift; 447 terminations were re-dressed.
Nakamura reconciled the dockbay muster report against 484 flow-in events and found no gap.
Rautio walked the eastwing escort log for the swing shift and matched all 521 service entries to a host.
Reader G4 on server-hall logged 558 tailgate warnings during the early shift; each cleared on manual review.
Delacroix rotated the vault inspection-window schedule after the rollout; 595 entries were re-timed.
Power audit on atrium found the A5 controller drawing normally; 632 watts, within tolerance.
Lindqvist cross-checked 669 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port C2 at dockbay was exercised 706 times on the swing shift with no false rejects.
Kowalczyk logged a firmware note for eastwing: readers on H2 sat at level and needed no early-shift patch.
Turnstile throughput on server-hall peaked at 780 passages per hour during the relief shift, well inside spec.
Haugen reconciled the vault lost-flow register: 817 reported, all deactivated within the shift window.
Door-forced alarm on F3 at atrium fired 854 times, every one traced to facilities propping the port.
Thorsen confirmed the coldroom camera-to-flow overlay stayed aligned across 891 sampled events.
Escort-desk staffing for dockbay held at 28 through the early shift; no queue built at the reader.
Villanueva archived 65 reader event logs from eastwing port D8; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 102 test cards on the late shift.
Moreau noted 139 seconds of NTP skew on the vault controller, corrected before the night shift ended.
Loading-dock override at atrium port C7 was used 176 times for deliveries, each with a signed slip.
Rautio tallied 213 after-hours flows for coldroom on the early shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 250 occupants in under the target time with no reader contention.

### Review entry 0071 — eastwing lane

Door controller B6 on eastwing was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Abadi reviewed 324 camera frames against the server-hall flow log for the night shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 361 attendees; facilities holds the roster.
Sato confirmed the atrium anti-passback timer stayed at the 398-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the relief shift: 435 blanks issued, none unaccounted.
Okonkwo closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 509 minutes during the night shift with no operator intervention.
Osei measured 546 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for vault listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Menendez verified dockbay monitoring resumed on the night shift 694 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the swing shift; Moreau logged the 731-second release delay.
Nakamura traced 768 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 805 records on the relief shift with no manual overrides.
Baptiste spot-checked port C7 on atrium: the strike alignment was within spec after 842 cycles.
Access-review queue for coldroom carried 879 items into the night shift, all of them informational.
Abadi archived 916 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the early shift; 53 terminations were re-dressed.
Sato reconciled the server-hall muster report against 90 flow-in events and found no gap.
Kowalczyk walked the vault escort log for the late shift and matched all 127 service entries to a host.
Reader A5 on atrium logged 164 tailgate warnings during the night shift; each cleared on manual review.
Haugen rotated the coldroom inspection-window schedule after the rollout; 201 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 238 watts, within tolerance.
Thorsen cross-checked 275 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 312 times on the late shift with no false rejects.
Villanueva logged a firmware note for vault: readers on B1 sat at level and needed no night-shift patch.
Turnstile throughput on atrium peaked at 386 passages per hour during the swing shift, well inside spec.
Moreau reconciled the coldroom lost-flow register: 423 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 460 times, every one traced to facilities propping the port.
Rautio confirmed the eastwing camera-to-flow overlay stayed aligned across 497 sampled events.
Escort-desk staffing for server-hall held at 534 through the night shift; no queue built at the reader.
Delacroix archived 571 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 608 test cards on the early shift.
Lindqvist noted 645 seconds of NTP skew on the coldroom controller, corrected before the relief shift ended.
Loading-dock override at dockbay port E2 was used 682 times for deliveries, each with a signed slip.
Kowalczyk tallied 719 after-hours flows for eastwing on the night shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 756 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Osei reviewed 830 camera frames against the atrium flow log for the relief shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 867 attendees; facilities holds the roster.
Ferrara confirmed the dockbay anti-passback timer stayed at the 904-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the swing shift: 41 blanks issued, none unaccounted.
Menendez closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 115 minutes during the relief shift with no operator intervention.
Nakamura measured 152 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for coldroom listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Abadi verified server-hall monitoring resumed on the relief shift 300 seconds after the controller restart.
Fire-panel interlock test on vault passed on the late shift; Lindqvist logged the 337-second release delay.
Sato traced 374 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 411 records on the swing shift with no manual overrides.
Okonkwo spot-checked port E2 on dockbay: the strike alignment was within spec after 448 cycles.
Access-review queue for eastwing carried 485 items into the relief shift, all of them informational.
Osei archived 522 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the night shift; 559 terminations were re-dressed.
Ferrara reconciled the atrium muster report against 596 flow-in events and found no gap.
Villanueva walked the coldroom escort log for the early shift and matched all 633 service entries to a host.
Reader C2 on dockbay logged 670 tailgate warnings during the relief shift; each cleared on manual review.
> **Board decision (2026-05-20 - TQ-3328)** Sato: layer precedence (final, revising TQ-3250). LOCKDOWN takes precedence where both layers cover the same instant: time already charged as isolation is not charged again as inspection. Compute each layer's compacted overlap with the session, subtract the shared span from the inspection side, then `adjusted_hold_ms = max(hold_ms - ceil(isolation_overlap_ms / 2) - (inspection_used_ms // 3), 0)`. The isolation half ROUNDS UP and the inspection half is FLOORED. Both `isolation_overlap_ms` and `inspection_overlap_ms` are REPORTED unadjusted, from each layer's own compacted union. ROUNDING: isolation_overlap_ms // 2 = CEIL. ROUNDING: inspection_used_ms // 3 = FLOOR.
Moreau rotated the eastwing inspection-window schedule after the rollout; 707 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 744 watts, within tolerance.
Rautio cross-checked 781 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 818 times on the early shift with no false rejects.
Delacroix logged a firmware note for coldroom: readers on C4 sat at level and needed no relief-shift patch.
Turnstile throughput on dockbay peaked at 892 passages per hour during the late shift, well inside spec.
Lindqvist reconciled the eastwing lost-flow register: 29 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 66 times, every one traced to facilities propping the port.
Kowalczyk confirmed the vault camera-to-flow overlay stayed aligned across 103 sampled events.
Escort-desk staffing for atrium held at 140 through the relief shift; no queue built at the reader.
Haugen archived 177 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 214 test cards on the night shift.
Thorsen noted 251 seconds of NTP skew on the eastwing controller, corrected before the swing shift ended.
Loading-dock override at server-hall port G4 was used 288 times for deliveries, each with a signed slip.
Villanueva tallied 325 after-hours flows for vault on the relief shift; all matched authorized on-call staff.
Muster drill for atrium cleared 362 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Nakamura reviewed 436 camera frames against the dockbay flow log for the swing shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 473 attendees; facilities holds the roster.
Baptiste confirmed the server-hall anti-passback timer stayed at the 510-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the late shift: 547 blanks issued, none unaccounted.
Abadi closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 621 minutes during the swing shift with no operator intervention.
Sato measured 658 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for eastwing listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Osei verified atrium monitoring resumed on the swing shift 806 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the early shift; Thorsen logged the 843-second release delay.
Ferrara traced 880 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 17 records on the late shift with no manual overrides.
Menendez spot-checked port G4 on server-hall: the strike alignment was within spec after 54 cycles.
Access-review queue for vault carried 91 items into the swing shift, all of them informational.
Nakamura archived 128 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the relief shift; 165 terminations were re-dressed.
Baptiste reconciled the dockbay muster report against 202 flow-in events and found no gap.
Delacroix walked the eastwing escort log for the night shift and matched all 239 service entries to a host.
Reader D5 on server-hall logged 276 tailgate warnings during the swing shift; each cleared on manual review.
Lindqvist rotated the vault inspection-window schedule after the rollout; 313 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 350 watts, within tolerance.
Kowalczyk cross-checked 387 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 424 times on the night shift with no false rejects.
Haugen logged a firmware note for eastwing: readers on D8 sat at level and needed no swing-shift patch.
Turnstile throughput on server-hall peaked at 498 passages per hour during the early shift, well inside spec.
Thorsen reconciled the vault lost-flow register: 535 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 572 times, every one traced to facilities propping the port.
Villanueva confirmed the coldroom camera-to-flow overlay stayed aligned across 609 sampled events.
Escort-desk staffing for dockbay held at 646 through the swing shift; no queue built at the reader.
Moreau archived 683 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 720 test cards on the relief shift.
Rautio noted 757 seconds of NTP skew on the vault controller, corrected before the late shift ended.
Loading-dock override at atrium port A5 was used 794 times for deliveries, each with a signed slip.
Delacroix tallied 831 after-hours flows for coldroom on the swing shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 868 occupants in under the target time with no reader contention.

### Review entry 0075 — server-hall lane

Door controller H2 on eastwing was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Sato reviewed 42 camera frames against the server-hall flow log for the late shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 79 attendees; facilities holds the roster.
Okonkwo confirmed the atrium anti-passback timer stayed at the 116-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the early shift: 153 blanks issued, none unaccounted.
Osei closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 227 minutes during the late shift with no operator intervention.
Ferrara measured 264 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for vault listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Nakamura verified dockbay monitoring resumed on the late shift 412 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the night shift; Rautio logged the 449-second release delay.
Baptiste traced 486 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 523 records on the early shift with no manual overrides.
Abadi spot-checked port A5 on atrium: the strike alignment was within spec after 560 cycles.
Access-review queue for coldroom carried 597 items into the late shift, all of them informational.
Sato archived 634 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the swing shift; 671 terminations were re-dressed.
Okonkwo reconciled the server-hall muster report against 708 flow-in events and found no gap.
Haugen walked the vault escort log for the relief shift and matched all 745 service entries to a host.
Reader F3 on atrium logged 782 tailgate warnings during the late shift; each cleared on manual review.
Thorsen rotated the coldroom inspection-window schedule after the rollout; 819 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 856 watts, within tolerance.
Villanueva cross-checked 893 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 30 times on the relief shift with no false rejects.
Moreau logged a firmware note for vault: readers on F9 sat at level and needed no late-shift patch.
Turnstile throughput on atrium peaked at 104 passages per hour during the night shift, well inside spec.
Rautio reconciled the coldroom lost-flow register: 141 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 178 times, every one traced to facilities propping the port.
Delacroix confirmed the eastwing camera-to-flow overlay stayed aligned across 215 sampled events.
Escort-desk staffing for server-hall held at 252 through the late shift; no queue built at the reader.
Lindqvist archived 289 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 326 test cards on the swing shift.
Kowalczyk noted 363 seconds of NTP skew on the coldroom controller, corrected before the early shift ended.
Loading-dock override at dockbay port C2 was used 400 times for deliveries, each with a signed slip.
Haugen tallied 437 after-hours flows for eastwing on the late shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 474 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Ferrara reviewed 548 camera frames against the atrium flow log for the early shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 585 attendees; facilities holds the roster.
Menendez confirmed the dockbay anti-passback timer stayed at the 622-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the night shift: 659 blanks issued, none unaccounted.
Nakamura closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 733 minutes during the early shift with no operator intervention.
Baptiste measured 770 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for coldroom listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Sato verified server-hall monitoring resumed on the early shift 18 seconds after the controller restart.
Fire-panel interlock test on vault passed on the relief shift; Kowalczyk logged the 55-second release delay.
Okonkwo traced 92 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 129 records on the night shift with no manual overrides.
Osei spot-checked port C2 on dockbay: the strike alignment was within spec after 166 cycles.
Access-review queue for eastwing carried 203 items into the early shift, all of them informational.
Ferrara archived 240 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the late shift; 277 terminations were re-dressed.
Menendez reconciled the atrium muster report against 314 flow-in events and found no gap.
Moreau walked the coldroom escort log for the swing shift and matched all 351 service entries to a host.
Reader A1 on dockbay logged 388 tailgate warnings during the early shift; each cleared on manual review.
> **Board decision (2026-05-22 - TQ-3332)** Moreau: containment admission (final). A session joins the containment queue when its `ledger_hold_ms` reaches the admission floor for its `top_tier`: core 150, service 190, staff 240, visitor 300. The floors sit directly on the observed ledger distribution, so a one-unit slip anywhere upstream moves a session across the boundary. Priority is then `critical` when `ledger_hold_ms >= 420`, or when `top_tier` is `core` with `isolation_overlap_ms > 0`; otherwise `high` when `ledger_hold_ms >= 300` or `flow_count >= 3`; otherwise `standard`.
Rautio rotated the eastwing inspection-window schedule after the rollout; 425 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 462 watts, within tolerance.
Delacroix cross-checked 499 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 536 times on the swing shift with no false rejects.
Lindqvist logged a firmware note for coldroom: readers on A2 sat at level and needed no early-shift patch.
Turnstile throughput on dockbay peaked at 610 passages per hour during the relief shift, well inside spec.
Kowalczyk reconciled the eastwing lost-flow register: 647 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 684 times, every one traced to facilities propping the port.
Haugen confirmed the vault camera-to-flow overlay stayed aligned across 721 sampled events.
Escort-desk staffing for atrium held at 758 through the early shift; no queue built at the reader.
Thorsen archived 795 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 832 test cards on the late shift.
Villanueva noted 869 seconds of NTP skew on the eastwing controller, corrected before the night shift ended.
Loading-dock override at server-hall port D5 was used 906 times for deliveries, each with a signed slip.
Moreau tallied 43 after-hours flows for vault on the early shift; all matched authorized on-call staff.
Muster drill for atrium cleared 80 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Baptiste reviewed 154 camera frames against the dockbay flow log for the night shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 191 attendees; facilities holds the roster.
Abadi confirmed the server-hall anti-passback timer stayed at the 228-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the relief shift: 265 blanks issued, none unaccounted.
Sato closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 339 minutes during the night shift with no operator intervention.
Okonkwo measured 376 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for eastwing listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Ferrara verified atrium monitoring resumed on the night shift 524 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the swing shift; Villanueva logged the 561-second release delay.
Menendez traced 598 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 635 records on the relief shift with no manual overrides.
Nakamura spot-checked port D5 on server-hall: the strike alignment was within spec after 672 cycles.
Access-review queue for vault carried 709 items into the night shift, all of them informational.
Baptiste archived 746 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the early shift; 783 terminations were re-dressed.
Abadi reconciled the dockbay muster report against 820 flow-in events and found no gap.
Lindqvist walked the eastwing escort log for the late shift and matched all 857 service entries to a host.
Reader B3 on server-hall logged 894 tailgate warnings during the night shift; each cleared on manual review.
Kowalczyk rotated the vault inspection-window schedule after the rollout; 31 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 68 watts, within tolerance.
Haugen cross-checked 105 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 142 times on the late shift with no false rejects.
Thorsen logged a firmware note for eastwing: readers on B6 sat at level and needed no night-shift patch.
Turnstile throughput on server-hall peaked at 216 passages per hour during the swing shift, well inside spec.
Villanueva reconciled the vault lost-flow register: 253 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 290 times, every one traced to facilities propping the port.
Moreau confirmed the coldroom camera-to-flow overlay stayed aligned across 327 sampled events.
Escort-desk staffing for dockbay held at 364 through the night shift; no queue built at the reader.
Rautio archived 401 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 438 test cards on the early shift.
Delacroix noted 475 seconds of NTP skew on the vault controller, corrected before the relief shift ended.
Loading-dock override at atrium port F3 was used 512 times for deliveries, each with a signed slip.
Lindqvist tallied 549 after-hours flows for coldroom on the night shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 586 occupants in under the target time with no reader contention.

### Review entry 0079 — vault lane

Door controller D8 on eastwing was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Okonkwo reviewed 660 camera frames against the server-hall flow log for the relief shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 697 attendees; facilities holds the roster.
Osei confirmed the atrium anti-passback timer stayed at the 734-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the swing shift: 771 blanks issued, none unaccounted.
Ferrara closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 845 minutes during the relief shift with no operator intervention.
Menendez measured 882 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for vault listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Baptiste verified dockbay monitoring resumed on the relief shift 130 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the late shift; Delacroix logged the 167-second release delay.
Abadi traced 204 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 241 records on the swing shift with no manual overrides.
Sato spot-checked port F3 on atrium: the strike alignment was within spec after 278 cycles.
Access-review queue for coldroom carried 315 items into the relief shift, all of them informational.
Okonkwo archived 352 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the night shift; 389 terminations were re-dressed.
Osei reconciled the server-hall muster report against 426 flow-in events and found no gap.
Thorsen walked the vault escort log for the early shift and matched all 463 service entries to a host.
Reader C7 on atrium logged 500 tailgate warnings during the relief shift; each cleared on manual review.
Villanueva rotated the coldroom inspection-window schedule after the rollout; 537 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 574 watts, within tolerance.
Moreau cross-checked 611 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 648 times on the early shift with no false rejects.
Rautio logged a firmware note for vault: readers on D1 sat at level and needed no relief-shift patch.
Turnstile throughput on atrium peaked at 722 passages per hour during the late shift, well inside spec.
Delacroix reconciled the coldroom lost-flow register: 759 reported, all deactivated within the shift window.
Door-forced alarm on C2 at dockbay fired 796 times, every one traced to facilities propping the port.
Lindqvist confirmed the eastwing camera-to-flow overlay stayed aligned across 833 sampled events.
Escort-desk staffing for server-hall held at 870 through the relief shift; no queue built at the reader.
Kowalczyk archived 907 reader event logs from vault port B1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 44 test cards on the night shift.
Haugen noted 81 seconds of NTP skew on the coldroom controller, corrected before the swing shift ended.
Loading-dock override at dockbay port A1 was used 118 times for deliveries, each with a signed slip.
Thorsen tallied 155 after-hours flows for eastwing on the relief shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 192 occupants in under the target time with no reader contention.
Door controller F9 on vault was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Menendez reviewed 266 camera frames against the atrium flow log for the swing shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 303 attendees; facilities holds the roster.
Nakamura confirmed the dockbay anti-passback timer stayed at the 340-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the late shift: 377 blanks issued, none unaccounted.
Baptiste closed the server-hall follow-up on port G4 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D1 on vault recalibrated in 451 minutes during the swing shift with no operator intervention.
Abadi measured 488 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for coldroom listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on dockbay port C2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port H2 closed without action; the mechanical override was already compliant.
Okonkwo verified server-hall monitoring resumed on the swing shift 636 seconds after the controller restart.
Fire-panel interlock test on vault passed on the early shift; Haugen logged the 673-second release delay.
Osei traced 710 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 747 records on the late shift with no manual overrides.
Ferrara spot-checked port A1 on dockbay: the strike alignment was within spec after 784 cycles.
Access-review queue for eastwing carried 821 items into the swing shift, all of them informational.
Menendez archived 858 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port F9 finished during the relief shift; 895 terminations were re-dressed.
Nakamura reconciled the atrium muster report against 32 flow-in events and found no gap.
Rautio walked the coldroom escort log for the night shift and matched all 69 service entries to a host.
Reader E2 on dockbay logged 106 tailgate warnings during the swing shift; each cleared on manual review.
> **Board decision (2026-05-25 - TQ-3334)** Baptiste: queue ordering and capacity (final). The containment queue is ordered strictly by this chain: priority rank `critical` > `high` > `standard`; then `ledger_hold_ms` descending; then `hold_ms` descending; then `flow_count` descending; then `subnet` ascending; then `start_ms` ascending. This is an ordering, not ascending entry time.
Delacroix rotated the eastwing inspection-window schedule after the rollout; 143 entries were re-timed.
Power audit on server-hall found the G4 controller drawing normally; 180 watts, within tolerance.
Lindqvist cross-checked 217 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port A5 at atrium was exercised 254 times on the night shift with no false rejects.
Kowalczyk logged a firmware note for coldroom: readers on E7 sat at level and needed no swing-shift patch.
Turnstile throughput on dockbay peaked at 328 passages per hour during the early shift, well inside spec.
Haugen reconciled the eastwing lost-flow register: 365 reported, all deactivated within the shift window.
Door-forced alarm on D5 at server-hall fired 402 times, every one traced to facilities propping the port.
Thorsen confirmed the vault camera-to-flow overlay stayed aligned across 439 sampled events.
Escort-desk staffing for atrium held at 476 through the swing shift; no queue built at the reader.
Villanueva archived 513 reader event logs from coldroom port C4; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 550 test cards on the relief shift.
Moreau noted 587 seconds of NTP skew on the eastwing controller, corrected before the late shift ended.
Loading-dock override at server-hall port B3 was used 624 times for deliveries, each with a signed slip.
Rautio tallied 661 after-hours flows for vault on the swing shift; all matched authorized on-call staff.
Muster drill for atrium cleared 698 occupants in under the target time with no reader contention.
Door controller A2 on coldroom was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Abadi reviewed 772 camera frames against the dockbay flow log for the late shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 809 attendees; facilities holds the roster.
Sato confirmed the server-hall anti-passback timer stayed at the 846-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the early shift: 883 blanks issued, none unaccounted.
Okonkwo closed the atrium follow-up on port A5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile E7 on coldroom recalibrated in 57 minutes during the late shift with no operator intervention.
Osei measured 94 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for eastwing listed no open access items; Thorsen acknowledged for the incoming crew.
Ferrara audited tamper counters on server-hall port D5 after the rollout and saw nothing anomalous.
Locksmith callback for vault port B1 closed without action; the mechanical override was already compliant.
Menendez verified atrium monitoring resumed on the late shift 242 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the night shift; Moreau logged the 279-second release delay.
Nakamura traced 316 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 353 records on the early shift with no manual overrides.
Baptiste spot-checked port B3 on server-hall: the strike alignment was within spec after 390 cycles.
Access-review queue for vault carried 427 items into the late shift, all of them informational.
Abadi archived 464 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port A2 finished during the swing shift; 501 terminations were re-dressed.
Sato reconciled the dockbay muster report against 538 flow-in events and found no gap.
Kowalczyk walked the eastwing escort log for the relief shift and matched all 575 service entries to a host.
Reader G4 on server-hall logged 612 tailgate warnings during the late shift; each cleared on manual review.
Haugen rotated the vault inspection-window schedule after the rollout; 649 entries were re-timed.
Power audit on atrium found the A5 controller drawing normally; 686 watts, within tolerance.
Thorsen cross-checked 723 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port C2 at dockbay was exercised 760 times on the relief shift with no false rejects.
Villanueva logged a firmware note for eastwing: readers on H2 sat at level and needed no late-shift patch.
Turnstile throughput on server-hall peaked at 834 passages per hour during the night shift, well inside spec.
Moreau reconciled the vault lost-flow register: 871 reported, all deactivated within the shift window.
Door-forced alarm on F3 at atrium fired 908 times, every one traced to facilities propping the port.
Rautio confirmed the coldroom camera-to-flow overlay stayed aligned across 45 sampled events.
Escort-desk staffing for dockbay held at 82 through the late shift; no queue built at the reader.
Delacroix archived 119 reader event logs from eastwing port D8; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 156 test cards on the swing shift.
Lindqvist noted 193 seconds of NTP skew on the vault controller, corrected before the early shift ended.
Loading-dock override at atrium port C7 was used 230 times for deliveries, each with a signed slip.
Kowalczyk tallied 267 after-hours flows for coldroom on the late shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 304 occupants in under the target time with no reader contention.

### Review entry 0083 — atrium lane

Door controller B6 on eastwing was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Osei reviewed 378 camera frames against the server-hall flow log for the early shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 415 attendees; facilities holds the roster.
Ferrara confirmed the atrium anti-passback timer stayed at the 452-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the night shift: 489 blanks issued, none unaccounted.
Menendez closed the dockbay follow-up on port C2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile H2 on eastwing recalibrated in 563 minutes during the early shift with no operator intervention.
Nakamura measured 600 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for vault listed no open access items; Rautio acknowledged for the incoming crew.
Baptiste audited tamper counters on atrium port F3 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port C4 closed without action; the mechanical override was already compliant.
Abadi verified dockbay monitoring resumed on the early shift 748 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the relief shift; Lindqvist logged the 785-second release delay.
Sato traced 822 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 859 records on the night shift with no manual overrides.
Okonkwo spot-checked port C7 on atrium: the strike alignment was within spec after 896 cycles.
Access-review queue for coldroom carried 33 items into the early shift, all of them informational.
Osei archived 70 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port B6 finished during the late shift; 107 terminations were re-dressed.
Ferrara reconciled the server-hall muster report against 144 flow-in events and found no gap.
Villanueva walked the vault escort log for the swing shift and matched all 181 service entries to a host.
Reader A5 on atrium logged 218 tailgate warnings during the early shift; each cleared on manual review.
Moreau rotated the coldroom inspection-window schedule after the rollout; 255 entries were re-timed.
Power audit on dockbay found the C2 controller drawing normally; 292 watts, within tolerance.
Rautio cross-checked 329 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port D5 at server-hall was exercised 366 times on the swing shift with no false rejects.
Delacroix logged a firmware note for vault: readers on B1 sat at level and needed no early-shift patch.
Turnstile throughput on atrium peaked at 440 passages per hour during the relief shift, well inside spec.
Lindqvist reconciled the coldroom lost-flow register: 477 reported, all deactivated within the shift window.
Door-forced alarm on A1 at dockbay fired 514 times, every one traced to facilities propping the port.
Kowalczyk confirmed the eastwing camera-to-flow overlay stayed aligned across 551 sampled events.
Escort-desk staffing for server-hall held at 588 through the early shift; no queue built at the reader.
Haugen archived 625 reader event logs from vault port F9; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 662 test cards on the late shift.
Thorsen noted 699 seconds of NTP skew on the coldroom controller, corrected before the night shift ended.
Loading-dock override at dockbay port E2 was used 736 times for deliveries, each with a signed slip.
Villanueva tallied 773 after-hours flows for eastwing on the early shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 810 occupants in under the target time with no reader contention.
Door controller D1 on vault was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Nakamura reviewed 884 camera frames against the atrium flow log for the night shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 21 attendees; facilities holds the roster.
Baptiste confirmed the dockbay anti-passback timer stayed at the 58-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the relief shift: 95 blanks issued, none unaccounted.
Abadi closed the server-hall follow-up on port D5 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B1 on vault recalibrated in 169 minutes during the night shift with no operator intervention.
Sato measured 206 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for coldroom listed no open access items; Kowalczyk acknowledged for the incoming crew.
Okonkwo audited tamper counters on dockbay port A1 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port D8 closed without action; the mechanical override was already compliant.
Osei verified server-hall monitoring resumed on the night shift 354 seconds after the controller restart.
Fire-panel interlock test on vault passed on the swing shift; Thorsen logged the 391-second release delay.
Ferrara traced 428 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 465 records on the relief shift with no manual overrides.
Menendez spot-checked port E2 on dockbay: the strike alignment was within spec after 502 cycles.
Access-review queue for eastwing carried 539 items into the night shift, all of them informational.
Nakamura archived 576 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port D1 finished during the early shift; 613 terminations were re-dressed.
Baptiste reconciled the atrium muster report against 650 flow-in events and found no gap.
Delacroix walked the coldroom escort log for the late shift and matched all 687 service entries to a host.
Reader C2 on dockbay logged 724 tailgate warnings during the night shift; each cleared on manual review.
> **Board decision (2026-05-27 - TQ-3330)** Ferrara: responder capacity cap (final). Responders cannot work more than two occupancies per subnet in one containment pass, so the queue is capped at two rows per subnet. The cap is applied AFTER the full ordering of TQ-3334, and the rows that survive are the two highest-ranked in that GLOBAL order — not the first two by start time and not a per-subnet ranking. `quarantined_count`, `priority_counts` and `quarantine_checksum` are all computed from the capped queue.
Lindqvist rotated the eastwing inspection-window schedule after the rollout; 761 entries were re-timed.
Power audit on server-hall found the D5 controller drawing normally; 798 watts, within tolerance.
Kowalczyk cross-checked 835 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port F3 at atrium was exercised 872 times on the late shift with no false rejects.
Haugen logged a firmware note for coldroom: readers on C4 sat at level and needed no night-shift patch.
Turnstile throughput on dockbay peaked at 46 passages per hour during the swing shift, well inside spec.
Thorsen reconciled the eastwing lost-flow register: 83 reported, all deactivated within the shift window.
Door-forced alarm on B3 at server-hall fired 120 times, every one traced to facilities propping the port.
Villanueva confirmed the vault camera-to-flow overlay stayed aligned across 157 sampled events.
Escort-desk staffing for atrium held at 194 through the night shift; no queue built at the reader.
Moreau archived 231 reader event logs from coldroom port A2; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 268 test cards on the early shift.
Rautio noted 305 seconds of NTP skew on the eastwing controller, corrected before the relief shift ended.
Loading-dock override at server-hall port G4 was used 342 times for deliveries, each with a signed slip.
Delacroix tallied 379 after-hours flows for vault on the night shift; all matched authorized on-call staff.
Muster drill for atrium cleared 416 occupants in under the target time with no reader contention.
Door controller E7 on coldroom was re-seated during the early shift; reader firmware sat at 4.12.0 and was already approved.
Sato reviewed 490 camera frames against the dockbay flow log for the relief shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 527 attendees; facilities holds the roster.
Okonkwo confirmed the server-hall anti-passback timer stayed at the 564-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the swing shift: 601 blanks issued, none unaccounted.
Osei closed the atrium follow-up on port F3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile C4 on coldroom recalibrated in 675 minutes during the relief shift with no operator intervention.
Ferrara measured 712 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the night boundary for eastwing listed no open access items; Villanueva acknowledged for the incoming crew.
Menendez audited tamper counters on server-hall port B3 after the rollout and saw nothing anomalous.
Locksmith callback for vault port F9 closed without action; the mechanical override was already compliant.
Nakamura verified atrium monitoring resumed on the relief shift 860 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the late shift; Rautio logged the 897-second release delay.
Baptiste traced 34 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 71 records on the swing shift with no manual overrides.
Abadi spot-checked port G4 on server-hall: the strike alignment was within spec after 108 cycles.
Access-review queue for vault carried 145 items into the relief shift, all of them informational.
Sato archived 182 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port E7 finished during the night shift; 219 terminations were re-dressed.
Okonkwo reconciled the dockbay muster report against 256 flow-in events and found no gap.
Haugen walked the eastwing escort log for the early shift and matched all 293 service entries to a host.
Reader D5 on server-hall logged 330 tailgate warnings during the relief shift; each cleared on manual review.
Thorsen rotated the vault inspection-window schedule after the rollout; 367 entries were re-timed.
Power audit on atrium found the F3 controller drawing normally; 404 watts, within tolerance.
Villanueva cross-checked 441 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port A1 at dockbay was exercised 478 times on the early shift with no false rejects.
Moreau logged a firmware note for eastwing: readers on D8 sat at level and needed no relief-shift patch.
Turnstile throughput on server-hall peaked at 552 passages per hour during the late shift, well inside spec.
Rautio reconciled the vault lost-flow register: 589 reported, all deactivated within the shift window.
Door-forced alarm on C7 at atrium fired 626 times, every one traced to facilities propping the port.
Delacroix confirmed the coldroom camera-to-flow overlay stayed aligned across 663 sampled events.
Escort-desk staffing for dockbay held at 700 through the relief shift; no queue built at the reader.
Lindqvist archived 737 reader event logs from eastwing port B6; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 774 test cards on the night shift.
Kowalczyk noted 811 seconds of NTP skew on the vault controller, corrected before the swing shift ended.
Loading-dock override at atrium port A5 was used 848 times for deliveries, each with a signed slip.
Haugen tallied 885 after-hours flows for coldroom on the relief shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 22 occupants in under the target time with no reader contention.

### Close-out

Door controller H2 on eastwing was re-seated during the night shift; reader firmware sat at 4.11.2 and was already approved.
Ferrara reviewed 96 camera frames against the server-hall flow log for the swing shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 133 attendees; facilities holds the roster.
Menendez confirmed the atrium anti-passback timer stayed at the 170-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the late shift: 207 blanks issued, none unaccounted.
Nakamura closed the dockbay follow-up on port A1 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile D8 on eastwing recalibrated in 281 minutes during the swing shift with no operator intervention.
Baptiste measured 318 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the relief boundary for vault listed no open access items; Delacroix acknowledged for the incoming crew.
Abadi audited tamper counters on atrium port C7 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port A2 closed without action; the mechanical override was already compliant.
Sato verified dockbay monitoring resumed on the swing shift 466 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the early shift; Kowalczyk logged the 503-second release delay.
Okonkwo traced 540 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 577 records on the late shift with no manual overrides.
Osei spot-checked port A5 on atrium: the strike alignment was within spec after 614 cycles.
Access-review queue for coldroom carried 651 items into the swing shift, all of them informational.
Ferrara archived 688 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port H2 finished during the relief shift; 725 terminations were re-dressed.
Menendez reconciled the server-hall muster report against 762 flow-in events and found no gap.
Moreau walked the vault escort log for the night shift and matched all 799 service entries to a host.
Reader F3 on atrium logged 836 tailgate warnings during the swing shift; each cleared on manual review.
Rautio rotated the coldroom inspection-window schedule after the rollout; 873 entries were re-timed.
Power audit on dockbay found the A1 controller drawing normally; 910 watts, within tolerance.
Delacroix cross-checked 47 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port B3 at server-hall was exercised 84 times on the night shift with no false rejects.
Lindqvist logged a firmware note for vault: readers on F9 sat at level and needed no swing-shift patch.
Turnstile throughput on atrium peaked at 158 passages per hour during the early shift, well inside spec.
Kowalczyk reconciled the coldroom lost-flow register: 195 reported, all deactivated within the shift window.
Door-forced alarm on E2 at dockbay fired 232 times, every one traced to facilities propping the port.
Haugen confirmed the eastwing camera-to-flow overlay stayed aligned across 269 sampled events.
Escort-desk staffing for server-hall held at 306 through the swing shift; no queue built at the reader.
Thorsen archived 343 reader event logs from vault port D1; retention only, no bearing on the rollup.
Badge-encoder calibration for atrium completed after 380 test cards on the relief shift.
Villanueva noted 417 seconds of NTP skew on the coldroom controller, corrected before the late shift ended.
Loading-dock override at dockbay port C2 was used 454 times for deliveries, each with a signed slip.
Moreau tallied 491 after-hours flows for eastwing on the swing shift; all matched authorized on-call staff.
Muster drill for server-hall cleared 528 occupants in under the target time with no reader contention.
Door controller B1 on vault was re-seated during the relief shift; reader firmware sat at 5.1.4 and was already approved.
Baptiste reviewed 602 camera frames against the atrium flow log for the late shift and found no unattributed entries.
Escort refresher for the coldroom service cohort closed with 639 attendees; facilities holds the roster.
Abadi confirmed the dockbay anti-passback timer stayed at the 676-second vendor default across the incident window.
Badge stock at the eastwing desk reconciled after the early shift: 713 blanks issued, none unaccounted.
Sato closed the server-hall follow-up on port B3 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile F9 on vault recalibrated in 787 minutes during the late shift with no operator intervention.
Okonkwo measured 824 ms of clock drift on the atrium visitor kiosk, inside the tolerance the board set.
Handover at the swing boundary for coldroom listed no open access items; Haugen acknowledged for the incoming crew.
Osei audited tamper counters on dockbay port E2 after the rollout and saw nothing anomalous.
Locksmith callback for eastwing port B6 closed without action; the mechanical override was already compliant.
Ferrara verified server-hall monitoring resumed on the late shift 72 seconds after the controller restart.
Fire-panel interlock test on vault passed on the night shift; Villanueva logged the 109-second release delay.
Menendez traced 146 orphaned reader heartbeats on atrium to a patch-panel swap, not to the rollup.
Visitor pre-registration for coldroom processed 183 records on the early shift with no manual overrides.
Nakamura spot-checked port C2 on dockbay: the strike alignment was within spec after 220 cycles.
Access-review queue for eastwing carried 257 items into the late shift, all of them informational.
Baptiste archived 294 controller diagnostics from server-hall to cold storage; none bear on rollup behaviour.
Cabling survey on vault port B1 finished during the swing shift; 331 terminations were re-dressed.
Abadi reconciled the atrium muster report against 368 flow-in events and found no gap.
Lindqvist walked the coldroom escort log for the relief shift and matched all 405 service entries to a host.
Reader A1 on dockbay logged 442 tailgate warnings during the late shift; each cleared on manual review.
Kowalczyk rotated the eastwing inspection-window schedule after the rollout; 479 entries were re-timed.
Power audit on server-hall found the B3 controller drawing normally; 516 watts, within tolerance.
Haugen cross-checked 553 visitor pre-registrations for vault against the muster and found no discrepancy.
Anti-passback on port C7 at atrium was exercised 590 times on the relief shift with no false rejects.
Thorsen logged a firmware note for coldroom: readers on A2 sat at level and needed no late-shift patch.
Turnstile throughput on dockbay peaked at 664 passages per hour during the night shift, well inside spec.
Villanueva reconciled the eastwing lost-flow register: 701 reported, all deactivated within the shift window.
Door-forced alarm on G4 at server-hall fired 738 times, every one traced to facilities propping the port.
Moreau confirmed the vault camera-to-flow overlay stayed aligned across 775 sampled events.
Escort-desk staffing for atrium held at 812 through the late shift; no queue built at the reader.
Rautio archived 849 reader event logs from coldroom port E7; retention only, no bearing on the rollup.
Badge-encoder calibration for dockbay completed after 886 test cards on the swing shift.
Delacroix noted 23 seconds of NTP skew on the eastwing controller, corrected before the early shift ended.
Loading-dock override at server-hall port D5 was used 60 times for deliveries, each with a signed slip.
Lindqvist tallied 97 after-hours flows for vault on the late shift; all matched authorized on-call staff.
Muster drill for atrium cleared 134 occupants in under the target time with no reader contention.
Door controller C4 on coldroom was re-seated during the swing shift; reader firmware sat at 5.0.1 and was already approved.
Okonkwo reviewed 208 camera frames against the dockbay flow log for the early shift and found no unattributed entries.
Escort refresher for the eastwing service cohort closed with 245 attendees; facilities holds the roster.
Osei confirmed the server-hall anti-passback timer stayed at the 282-second vendor default across the incident window.
Badge stock at the vault desk reconciled after the night shift: 319 blanks issued, none unaccounted.
Ferrara closed the atrium follow-up on port C7 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile A2 on coldroom recalibrated in 393 minutes during the early shift with no operator intervention.
Menendez measured 430 ms of clock drift on the dockbay visitor kiosk, inside the tolerance the board set.
Handover at the late boundary for eastwing listed no open access items; Moreau acknowledged for the incoming crew.
Nakamura audited tamper counters on server-hall port G4 after the rollout and saw nothing anomalous.
Locksmith callback for vault port D1 closed without action; the mechanical override was already compliant.
Baptiste verified atrium monitoring resumed on the early shift 578 seconds after the controller restart.
Fire-panel interlock test on coldroom passed on the relief shift; Delacroix logged the 615-second release delay.
Abadi traced 652 orphaned reader heartbeats on dockbay to a patch-panel swap, not to the rollup.
Visitor pre-registration for eastwing processed 689 records on the night shift with no manual overrides.
Sato spot-checked port D5 on server-hall: the strike alignment was within spec after 726 cycles.
Access-review queue for vault carried 763 items into the early shift, all of them informational.
Okonkwo archived 800 controller diagnostics from atrium to cold storage; none bear on rollup behaviour.
Cabling survey on coldroom port C4 finished during the late shift; 837 terminations were re-dressed.
Osei reconciled the dockbay muster report against 874 flow-in events and found no gap.
Thorsen walked the eastwing escort log for the swing shift and matched all 911 service entries to a host.
Reader B3 on server-hall logged 48 tailgate warnings during the early shift; each cleared on manual review.
Villanueva rotated the vault inspection-window schedule after the rollout; 85 entries were re-timed.
Power audit on atrium found the C7 controller drawing normally; 122 watts, within tolerance.
Moreau cross-checked 159 visitor pre-registrations for coldroom against the muster and found no discrepancy.
Anti-passback on port E2 at dockbay was exercised 196 times on the swing shift with no false rejects.
Rautio logged a firmware note for eastwing: readers on B6 sat at level and needed no early-shift patch.
Turnstile throughput on server-hall peaked at 270 passages per hour during the relief shift, well inside spec.
Delacroix reconciled the vault lost-flow register: 307 reported, all deactivated within the shift window.
Door-forced alarm on A5 at atrium fired 344 times, every one traced to facilities propping the port.
Lindqvist confirmed the coldroom camera-to-flow overlay stayed aligned across 381 sampled events.
Escort-desk staffing for dockbay held at 418 through the early shift; no queue built at the reader.
Kowalczyk archived 455 reader event logs from eastwing port H2; retention only, no bearing on the rollup.
Badge-encoder calibration for server-hall completed after 492 test cards on the late shift.
Haugen noted 529 seconds of NTP skew on the vault controller, corrected before the night shift ended.
Loading-dock override at atrium port F3 was used 566 times for deliveries, each with a signed slip.
Thorsen tallied 603 after-hours flows for coldroom on the early shift; all matched authorized on-call staff.
Muster drill for dockbay cleared 640 occupants in under the target time with no reader contention.
Door controller D8 on eastwing was re-seated during the late shift; reader firmware sat at 4.12.3 and was already approved.
Menendez reviewed 714 camera frames against the server-hall flow log for the night shift and found no unattributed entries.
Escort refresher for the vault service cohort closed with 751 attendees; facilities holds the roster.
Nakamura confirmed the atrium anti-passback timer stayed at the 788-second vendor default across the incident window.
Badge stock at the coldroom desk reconciled after the relief shift: 825 blanks issued, none unaccounted.
Baptiste closed the dockbay follow-up on port E2 — the alarm burst traced to a wedged contact, not flow misuse.
Turnstile B6 on eastwing recalibrated in 899 minutes during the night shift with no operator intervention.
Abadi measured 36 ms of clock drift on the server-hall visitor kiosk, inside the tolerance the board set.
Handover at the early boundary for vault listed no open access items; Lindqvist acknowledged for the incoming crew.
Sato audited tamper counters on atrium port A5 after the rollout and saw nothing anomalous.
Locksmith callback for coldroom port E7 closed without action; the mechanical override was already compliant.
Okonkwo verified dockbay monitoring resumed on the night shift 184 seconds after the controller restart.
Fire-panel interlock test on eastwing passed on the swing shift; Haugen logged the 221-second release delay.
Osei traced 258 orphaned reader heartbeats on server-hall to a patch-panel swap, not to the rollup.
Visitor pre-registration for vault processed 295 records on the relief shift with no manual overrides.
Ferrara spot-checked port F3 on atrium: the strike alignment was within spec after 332 cycles.
Access-review queue for coldroom carried 369 items into the night shift, all of them informational.
Menendez archived 406 controller diagnostics from dockbay to cold storage; none bear on rollup behaviour.
Cabling survey on eastwing port D8 finished during the early shift; 443 terminations were re-dressed.
Nakamura reconciled the server-hall muster report against 480 flow-in events and found no gap.
Rautio walked the vault escort log for the late shift and matched all 517 service entries to a host.
Reader C7 on atrium logged 554 tailgate warnings during the night shift; each cleared on manual review.
Delacroix rotated the coldroom inspection-window schedule after the rollout; 591 entries were re-timed.
Power audit on dockbay found the E2 controller drawing normally; 628 watts, within tolerance.
Lindqvist cross-checked 665 visitor pre-registrations for eastwing against the muster and found no discrepancy.
Anti-passback on port G4 at server-hall was exercised 702 times on the late shift with no false rejects.
The board considers the rollup semantics settled at the entries above. Anything not restated in a May close-out entry stands as first recorded.
