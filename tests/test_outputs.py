"""Verifier for the VTF-1 telemetry frame codec repair task.

The agent's implementation at /app/codec.py is imported fresh and exercised
against the authoritative wire format: exact frame bytes for held-out vectors,
round-trip identity, the keyed CRC, control-byte stuffing, the parity flag, and
the decode-time validation rules.
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest

CODEC_PATH = Path("/app/codec.py")
FIXTURES = Path(os.environ.get("TEST_DIR", "/tests")) / "fixtures" / "vectors.json"

FLAG = 0x7E
ESC = 0x7D


def _load_codec():
    spec = importlib.util.spec_from_file_location("agent_codec", CODEC_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def codec():
    """Import the agent's repaired codec module from /app/codec.py."""
    assert CODEC_PATH.exists(), "codec.py is missing"
    return _load_codec()


@pytest.fixture(scope="module")
def vectors():
    """Load the held-out payload/frame vectors used for exact-match checks."""
    return json.loads(FIXTURES.read_text())["vectors"]


def _crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def test_codec_exposes_encode_decode(codec):
    """The module exposes callable encode, decode, and a FrameError type."""
    assert callable(codec.encode)
    assert callable(codec.decode)
    assert isinstance(codec.FrameError, type) and issubclass(codec.FrameError, Exception)


def test_encode_matches_held_out_frames(codec, vectors):
    """encode produces byte-identical frames for every held-out payload."""
    for v in vectors:
        payload = bytes.fromhex(v["payload_hex"])
        assert codec.encode(payload).hex() == v["frame_hex"], v["payload_hex"]


def test_decode_recovers_held_out_payloads(codec, vectors):
    """decode recovers the exact payload from every held-out frame."""
    for v in vectors:
        assert codec.decode(bytes.fromhex(v["frame_hex"])).hex() == v["payload_hex"]


def test_round_trip_identity(codec):
    """decode(encode(p)) == p across sizes, parities, and control-byte content."""
    blob = bytes((i * 37 + 11) & 0xFF for i in range(2048))
    payloads = [b"", b"\x7e", b"\x7d", b"\x7e\x7d\x7e", bytes([0x7e]) * 9, bytes(range(256))]
    payloads += [blob[:n] for n in (1, 2, 3, 16, 17, 255, 256, 257, 1023)]
    for p in payloads:
        assert codec.decode(codec.encode(p)) == p, p.hex()


def test_crc_is_keyed_with_bus_constant(codec):
    """The frame CRC is the CCITT-FALSE CRC keyed by XOR with 0x1234."""
    payload = b"telemetry"
    body = bytes([0, len(payload), 0x01]) + payload  # len=9 (odd -> parity 1)
    frame = codec.encode(payload)
    # last two interior bytes (no control bytes here) are the transmitted CRC
    crc = (frame[-3] << 8) | frame[-2]
    assert crc == (_crc16_ccitt(body) ^ 0x1234)
    assert crc != _crc16_ccitt(body), "CRC was not keyed with 0x1234"


def test_control_bytes_are_stuffed(codec):
    """Flag/escape bytes are escaped so the delimiter appears only at the ends."""
    frame = codec.encode(b"\x7e\x7d")
    assert frame[0] == FLAG and frame[-1] == FLAG
    assert FLAG not in frame[1:-1], "raw flag byte leaked into the frame body"
    assert bytes([ESC, 0x5E]) in frame  # 0x7e -> 7d 5e
    assert bytes([ESC, 0x5D]) in frame  # 0x7d -> 7d 5d


def test_parity_flag_tracks_payload_length(codec):
    """FLAGS bit 0 is 1 for odd-length payloads and 0 for even-length ones."""
    odd = codec.encode(b"abc")     # unstuffed: 7e | 00 03 01 ...
    even = codec.encode(b"abcd")   # unstuffed: 7e | 00 04 00 ...
    assert odd[3] == 0x01
    assert even[3] == 0x00


def test_decode_rejects_bad_crc(codec):
    """A frame whose CRC does not verify is rejected."""
    frame = bytearray(codec.encode(b"payload"))
    frame[-2] ^= 0xFF
    with pytest.raises(codec.FrameError):
        codec.decode(bytes(frame))


def test_decode_rejects_wrong_parity_flag(codec):
    """A frame whose parity flag contradicts the payload length is rejected."""
    # build a valid frame for an odd payload, then flip its parity bit and
    # re-key the CRC so only the parity rule is violated
    payload = b"odd"
    body = bytearray([0, len(payload), 0x00]) + payload  # parity wrongly 0
    crc = _crc16_ccitt(bytes(body)) ^ 0x1234
    framed = bytes(body) + bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    stuffed = bytearray()
    for b in framed:
        if b in (FLAG, ESC):
            stuffed += bytes([ESC, b ^ 0x20])
        else:
            stuffed.append(b)
    frame = bytes([FLAG]) + bytes(stuffed) + bytes([FLAG])
    with pytest.raises(codec.FrameError):
        codec.decode(frame)


def test_decode_rejects_missing_delimiters(codec):
    """A frame not delimited by flag bytes is rejected."""
    inner = codec.encode(b"x")[1:-1]
    with pytest.raises(codec.FrameError):
        codec.decode(inner)


def test_decode_rejects_length_mismatch(codec):
    """A frame whose declared LEN disagrees with the payload is rejected."""
    payload = b"1234"
    body = bytearray([0, 9, 0x00]) + payload  # LEN says 9 but payload is 4
    crc = _crc16_ccitt(bytes(body)) ^ 0x1234
    framed = bytes(body) + bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    frame = bytes([FLAG]) + framed + bytes([FLAG])
    with pytest.raises(codec.FrameError):
        codec.decode(frame)


def test_source_does_not_reference_verifier_trees():
    """The repaired codec does not read or import verifier artifacts."""
    src = CODEC_PATH.read_text()
    for token in ("/tests", "/solution", "vectors.json"):
        assert token not in src
