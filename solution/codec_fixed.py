#!/usr/bin/env python3
"""Reference implementation of the Vantor telemetry frame codec (VTF-1).

Encodes a payload into a framed byte string and decodes it back. The framing
layout and decode contract are in /app/docs/frame_spec.md; the calibrated bus
constants (the CRC keying, which bytes the CRC covers, the CRC byte order, the
escape mask, and the parity-bit rule) are the final values settled in
/app/docs/bus_bringup_log.md.
"""

from __future__ import annotations

import argparse
import sys

FLAG = 0x7E
ESC = 0x7D
ESC_XOR = 0x40          # final escape mask (bring-up CAL- B7, revising the 0x20 draft)
CRC_KEY = 0x1234        # final keying constant (bring-up CAL-B4)
MAX_PAYLOAD = 1023


class FrameError(ValueError):
    """Raised when a frame cannot be decoded per the VTF-1 contract."""


def crc16_ccitt(data: bytes) -> int:
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF, no reflection, xorout 0."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def keyed_crc(body: bytes) -> int:
    """The VTF-1 frame CRC: CCITT-FALSE over the whole body, keyed by XOR."""
    return crc16_ccitt(body) ^ CRC_KEY


def _payload_parity(payload: bytes) -> int:
    """Parity bit: 1 when the payload holds an odd number of 1-bits, else 0."""
    return sum(bin(b).count("1") for b in payload) & 1


def _stuff(data: bytes) -> bytes:
    out = bytearray()
    for byte in data:
        if byte in (FLAG, ESC):
            out.append(ESC)
            out.append(byte ^ ESC_XOR)
        else:
            out.append(byte)
    return bytes(out)


def _unstuff(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(data):
        byte = data[i]
        if byte == ESC:
            if i + 1 >= len(data):
                raise FrameError("truncated escape sequence")
            out.append(data[i + 1] ^ ESC_XOR)
            i += 2
        else:
            out.append(byte)
            i += 1
    return bytes(out)


def encode(payload: bytes) -> bytes:
    """Frame a payload into a VTF-1 byte string."""
    if len(payload) > MAX_PAYLOAD:
        raise FrameError(f"payload exceeds {MAX_PAYLOAD} bytes")
    flags = _payload_parity(payload)
    header = bytes([(len(payload) >> 8) & 0xFF, len(payload) & 0xFF, flags])
    body = header + payload
    crc = keyed_crc(body)
    framed = body + bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    return bytes([FLAG]) + _stuff(framed) + bytes([FLAG])


def decode(frame: bytes) -> bytes:
    """Recover the payload from a VTF-1 frame, validating every field."""
    if len(frame) < 2 or frame[0] != FLAG or frame[-1] != FLAG:
        raise FrameError("frame is not delimited by flag bytes")
    framed = _unstuff(frame[1:-1])
    if len(framed) < 5:
        raise FrameError("frame too short to contain header and CRC")
    body, crc_bytes = framed[:-2], framed[-2:]
    got_crc = (crc_bytes[0] << 8) | crc_bytes[1]
    if keyed_crc(body) != got_crc:
        raise FrameError("CRC mismatch")
    declared_len = (body[0] << 8) | body[1]
    flags = body[2]
    payload = body[3:]
    if declared_len != len(payload):
        raise FrameError("declared length does not match payload")
    if flags & 0x01 != _payload_parity(payload):
        raise FrameError("parity bit does not match payload")
    if flags & 0xFE:
        raise FrameError("reserved FLAGS bits are not zero")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="VTF-1 telemetry frame codec")
    parser.add_argument("mode", choices=["encode", "decode"])
    parser.add_argument("hex_input", help="input bytes as a hex string")
    args = parser.parse_args()
    data = bytes.fromhex(args.hex_input)
    try:
        result = encode(data) if args.mode == "encode" else decode(data)
    except FrameError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(result.hex())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
