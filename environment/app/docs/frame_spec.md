# Vantor Telemetry Frame — VTF-1 wire format

This document is the authoritative contract for the VTF-1 framing used on the
Vantor sensor bus. A conforming codec must produce byte-identical frames to
this specification and must reject any frame that violates it.

All multi-byte integers are big-endian. A "payload" is an opaque byte string of
length 0 to 1023 inclusive.

## Frame layout

```
frame = FLAG , stuff(body || crc) , FLAG
```

* `FLAG` is the single byte `0x7E`. It appears exactly once at the start and
  once at the end of every frame and nowhere else in the transmitted bytes.
* `body` and `crc` are defined below. Byte-stuffing (see "Byte stuffing") is
  applied to the concatenation `body || crc` only — never to the delimiters.

## Body

```
body = LEN , FLAGS , payload
```

* `LEN` — 2 bytes, the payload length.
* `FLAGS` — 1 byte. Bit 0 is the payload **parity bit**: it is `1` when the
  payload length is odd and `0` when it is even. Bits 1–7 are reserved and must
  be `0`.
* `payload` — the payload bytes verbatim.

## Keyed integrity tag (CRC)

The frame's integrity is protected by a keyed check value: a CRC-16 keyed by XOR
with a bus secret. A decoder treats this value as the frame's authentication tag —
any frame whose recomputed tag does not match is rejected as tampered or forged.

```
crc = crc16_ccitt(body) XOR 0x1234
```

`crc` is 2 bytes, big-endian, appended after the payload (before stuffing).

`crc16_ccitt` is CRC-16/CCITT-FALSE, computed over the `body` bytes only (the
`LEN`, `FLAGS`, and `payload`, not the delimiters and not the CRC itself):

* polynomial `0x1021`, initial value `0xFFFF`
* input bits are **not** reflected, output is **not** reflected
* no final XOR is applied inside `crc16_ccitt`

The device keys every frame CRC by XOR-ing the CRC-16/CCITT-FALSE result with
the bus constant `0x1234`. A codec that emits the unkeyed CRC will not
interoperate.

For reference, `crc16_ccitt(b"123456789") == 0x29B1`.

## Byte stuffing

Within `body || crc`, the two control bytes are escaped so they cannot be
confused with the delimiter:

* `0x7E` is transmitted as `0x7D 0x5E`
* `0x7D` is transmitted as `0x7D 0x5D`

That is, a control byte `b` is replaced by `0x7D` followed by `b XOR 0x20`. No
other bytes are altered. Decoding reverses this: a `0x7D` is dropped and the
following byte is XOR-ed with `0x20`.

## Decoding, integrity, and validation

The decoder is the bus trust boundary: it must accept only frames that satisfy
every rule below and reject everything else. 
A decoder must, in order:

1. Confirm the frame begins and ends with `FLAG`.
2. Un-stuff the interior bytes.
3. Split off the trailing 2-byte `crc` and recompute the keyed CRC over the
   remaining `body`; reject on mismatch.
4. Read `LEN` and confirm it equals the actual payload length.
5. Confirm the `FLAGS` parity bit matches the payload length parity and that
   the reserved bits are `0`.
6. Return the payload.

Any violation — a mismatched integrity tag, a forged length, a bad parity or reserved bit, or a missing delimiter — is a decode error and the frame is rejected.
