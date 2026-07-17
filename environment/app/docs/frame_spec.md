# Vantor Telemetry Frame — VTF-1 wire format

This document is the authoritative contract for the VTF-1 **frame structure** and
the **decode validation order** used on the Vantor sensor bus. A conforming codec
must produce byte-identical frames to this specification and must reject any
frame that violates it.

The specific bus constants — how the integrity tag is keyed, which bytes it
covers, its byte order on the wire, the escape mask used by byte-stuffing, and
how the parity bit is computed — are **not fixed in this document**. They were
settled over the bus bring-up and their final values live in
`/app/docs/bus_bringup_log.md`. See "Calibrated bus constants" below. A "payload"
is an opaque byte string of length 0 to 1023 inclusive.

## Frame layout

```
frame = FLAG , stuff(body || crc) , FLAG
```

* `FLAG` is the single byte `0x7E`. It appears exactly once at the start and
  once at the end of every frame and nowhere else in the transmitted bytes.
* Byte-stuffing (see "Byte stuffing") is applied to the concatenation
  `body || crc` only — never to the delimiters.

## Body

```
body = LEN , FLAGS , payload
```

* `LEN` — 2 bytes, big-endian, the payload length.
* `FLAGS` — 1 byte. Bit 0 is the payload **parity bit** (its rule is a
  calibrated constant, see below). Bits 1–7 are reserved and must be `0`.
* `payload` — the payload bytes verbatim.

## Integrity tag (CRC)

The frame's integrity is protected by a keyed check value: a CRC-16 keyed by XOR
with a bus secret. A decoder treats this value as the frame's authentication
tag — any frame whose recomputed tag does not match is rejected as tampered or
forged. The CRC is 2 bytes, appended after the payload (before stuffing).

The underlying CRC primitive is `crc16_ccitt` = CRC-16/CCITT-FALSE:

* polynomial `0x1021`, initial value `0xFFFF`
* input bits are **not** reflected, output is **not** reflected
* no final XOR is applied inside `crc16_ccitt`
* for reference, `crc16_ccitt(b"123456789") == 0x29B1`

How that primitive is turned into the transmitted tag — the XOR key, the exact
span of `body`/header bytes it is computed over, and the byte order in which the
2-byte tag is written — is calibrated; see the bring-up log.

## Byte stuffing

Within `body || crc`, the two control bytes `0x7E` and `0x7D` are escaped so they
cannot be confused with the delimiter: a control byte `b` is replaced by the
escape byte `0x7D` followed by `b XOR M`, where `M` is the calibrated **escape
mask** (see the bring-up log). No other bytes are altered. Decoding reverses
this: a `0x7D` is dropped and the following byte is XOR-ed with `M`.

## Calibrated bus constants

The following are fixed by `/app/docs/bus_bringup_log.md`, not here:

* the **CRC XOR key**;
* the **CRC coverage** — which bytes the tag is computed over;
* the **CRC byte order** on the wire;
* the **escape mask** `M` used by byte-stuffing;
* the **parity-bit rule** for `FLAGS` bit 0.

The bring-up log is a working record: it carries February draft values that were
revised during the May bus review. Reconcile it as an account that resolves over
time — **where a February draft and a later bring-up decision disagree, the later
decision governs** — and use the final calibrated values. Do not read or import
anything from `/tests` or `/solution`.

## Decoding, integrity, and validation

The decoder is the bus trust boundary: it must accept only frames that satisfy
every rule below and reject everything else. A decoder must, in order:

1. Confirm the frame begins and ends with `FLAG`.
2. Un-stuff the interior bytes.
3. Split off the trailing 2-byte `crc` and recompute the keyed CRC over the
   calibrated coverage; reject on mismatch.
4. Read `LEN` and confirm it equals the actual payload length.
5. Confirm the `FLAGS` parity bit matches the calibrated parity rule and that
   the reserved bits are `0`.
6. Return the payload.

Any violation — a mismatched integrity tag, a forged length, a bad parity or
reserved bit, or a missing delimiter — is a decode error and the frame is
rejected.
