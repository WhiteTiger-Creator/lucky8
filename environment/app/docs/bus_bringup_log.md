# Vantor sensor-bus bring-up log — VTF-1 framing

Working record of the VTF-1 frame bring-up on the Vantor sensor bus. Entries are
roughly chronological. The February entries are the first-pass framing brought up
against a single bench node; several were revised during the May bus review once
the tamper-tag interop and the multi-node captures were in hand. **Where a
February draft and a later bring-up decision disagree, the later decision
governs.** Most of this log is routine bench noise; the values that matter are
the CRC keying, the CRC coverage, the CRC byte order, the escape mask `M`, and
the parity-bit rule.

---

### BB-2402-01 (2026-02-04, Devi) — bench bring-up, delimiter

Confirmed the `0x7E` flag delimiter frames cleanly on the logic analyzer. Idle
line holds high; a single flag opens and closes each frame. No constants fixed
yet.

### BB-2402-05 (2026-02-06, Devi) — CRC coverage, first pass

For the first bench pass the integrity tag is computed over the **payload bytes
only** — the LEN and FLAGS header is left out of the CRC to keep the bench script
simple. *(Superseded — reversed in the May bus review; see CAL-B3.)*

### BB-2402-08 (2026-02-09, Marco) — CRC keying, first pass

Tag is shipped **unkeyed** for now: the raw CRC-16/CCITT-FALSE value goes on the
wire with no XOR applied, so the bench decoder can cross-check against an
off-the-shelf CRC tool. Keying is deferred until the bus secret is provisioned.
*(Superseded — reversed in the May bus review; see CAL-B4.)*

### BB-2402-10 (2026-02-10, Marco) — CRC byte order, first pass

The 2-byte tag is emitted **little-endian** on the wire, matching the bench MCU's
native word order. *(Superseded — reversed in the May bus review; see CAL-B5.)*

### BB-2402-13 (2026-02-12, Devi) — routine bench note

Ran 500 random round-trips through the bench loopback; no delimiter aliasing
observed once stuffing was enabled. Recorded for the bring-up history.

### BB-2402-14 (2026-02-13, Marco) — escape mask, first pass

Byte-stuffing uses the usual HDLC-style escape: a control byte is sent as `0x7D`
then the byte XOR **`0x20`**. So `0x7E` → `0x7D 0x5E` on the bench build.
*(Superseded — reversed in the May bus review; see CAL-B7.)*

### BB-2402-17 (2026-02-15, Devi) — parity bit, first pass

`FLAGS` bit 0 is the **payload-length parity**: `1` when the payload length is an
odd number of bytes, `0` when even. Cheap to compute on the sender. *(Superseded
— reversed in the May bus review; see CAL-B8.)*

### BB-2402-20 (2026-02-18, Marco) — reserved bits

`FLAGS` bits 1–7 are reserved and transmitted as `0`; the decoder rejects a frame
with any reserved bit set. This one held up and was not revised.

---

## May 2026 bus review

Re-ran bring-up against the three-node captures with the tamper-tag interop suite
and the provisioned bus secret. The entries below are the governing values.

### CAL-B3 (2026-05-05, Priya) — CRC coverage, final

Payload-only coverage (BB-2402-05) let a forged LEN/FLAGS header slip past the
tag on the multi-node captures. The integrity tag is now computed over the
**entire body — `LEN`, `FLAGS`, and `payload` together** — so the header is
authenticated. Supersedes BB-2402-05.

### CAL-B4 (2026-05-05, Priya) — CRC keying, final

With the bus secret provisioned, the tag is **keyed by XOR with the bus constant
`0x1234`**: the transmitted tag is `crc16_ccitt(covered_bytes) XOR 0x1234`. An
unkeyed tag (BB-2402-08) is rejected. Supersedes BB-2402-08.

### CAL-B5 (2026-05-06, Priya) — CRC byte order, final

Interop with the collector fixed the tag as **big-endian** on the wire (high byte
first), not the bench-native little-endian of BB-2402-10. Supersedes BB-2402-10.

### CAL-B7 (2026-05-07, Yusuf) — escape mask, final

The `0x20` bench mask (BB-2402-14) collided with a legacy XON/XOFF path on one
node, so the escape mask was moved to **`M = 0x40`**: a control byte `b` is sent
as `0x7D` then `b XOR 0x40` (so `0x7E` → `0x7D 0x3E`, `0x7D` → `0x7D 0x3D`).
Supersedes BB-2402-14. (We briefly trialled `M = 0x5E` to sidestep another range;
it reintroduced aliasing on the captures and was rejected — keep `0x40`.)

### CAL-B8 (2026-05-08, Yusuf) — parity bit, final

Length parity (BB-2402-17) gave no protection against bit flips inside a
fixed-length payload, so the parity bit was redefined over payload **content**:
`FLAGS` bit 0 is `1` when the payload contains an **odd number of set bits**
(the XOR of all bits of all payload bytes), `0` when even. An empty payload has
parity `0`. Supersedes BB-2402-17.

### CAL-B9 (2026-05-09, Priya) — sign-off

Three-node captures reproduced end-to-end with the provisioned secret and the
revised framing; tamper-tag interop suite passes. All February bench drafts are
closed by their May entries above. No open bring-up items.
