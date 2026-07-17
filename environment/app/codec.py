#!/usr/bin/env python3
"""Vantor telemetry frame codec (VTF-1).

This build predates the bus-keying and control-byte-escaping changes and no
longer interoperates with current firmware. It still assembles a frame and
checks a CRC, but conforming devices reject its output.
"""

from __future__ import annotations

import argparse
import sys

FLAG = 0x7E
MAX_PAYLOAD = 1023


class FrameError(ValueError):
    """Raised when a frame cannot be decoded."""


def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def encode(payload: bytes) -> bytes:
    if len(payload) > MAX_PAYLOAD:
        raise FrameError(f"payload exceeds {MAX_PAYLOAD} bytes")
    header = bytes([(len(payload) >> 8) & 0xFF, len(payload) & 0xFF, 0x00])
    body = header + payload
    crc = crc16_ccitt(body)
    framed = body + bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    return bytes([FLAG]) + framed + bytes([FLAG])


def decode(frame: bytes) -> bytes:
    if len(frame) < 2 or frame[0] != FLAG or frame[-1] != FLAG:
        raise FrameError("frame is not delimited by flag bytes")
    framed = frame[1:-1]
    body, crc_bytes = framed[:-2], framed[-2:]
    got_crc = (crc_bytes[0] << 8) | crc_bytes[1]
    if crc16_ccitt(body) != got_crc:
        raise FrameError("CRC mismatch")
    declared_len = (body[0] << 8) | body[1]
    payload = body[3:]
    if declared_len != len(payload):
        raise FrameError("declared length does not match payload")
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
