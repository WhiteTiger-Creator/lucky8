"""Verifier for the VTF-1 telemetry frame codec repair task.

The agent's implementation at /app/codec.py is imported fresh and exercised
against the authoritative wire format: exact frame bytes for held-out vectors,
round-trip identity, the keyed CRC, control-byte stuffing, the parity bit, and
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
ESC_XOR = 0x40
CRC_KEY = 0x1234


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


def _parity(payload: bytes) -> int:
    """VTF-1 parity bit: 1 when the payload holds an odd number of 1-bits."""
    return sum(bin(b).count("1") for b in payload) & 1


def _stuff(data: bytes) -> bytes:
    out = bytearray()
    for b in data:
        if b in (FLAG, ESC):
            out += bytes([ESC, b ^ ESC_XOR])
        else:
            out.append(b)
    return bytes(out)


def _frame_from_body(body: bytes) -> bytes:
    """Wrap an already-built body (LEN|FLAGS|payload) into a full VTF-1 frame."""
    crc = _crc16_ccitt(body) ^ CRC_KEY
    framed = body + bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    return bytes([FLAG]) + _stuff(framed) + bytes([FLAG])


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
    body = bytes([0, len(payload), _parity(payload)]) + payload
    # a frame carrying the UNKEYED CRC must be rejected as tampered
    unkeyed = _crc16_ccitt(body)
    framed = body + bytes([(unkeyed >> 8) & 0xFF, unkeyed & 0xFF])
    forged = bytes([FLAG]) + _stuff(framed) + bytes([FLAG])
    with pytest.raises(codec.FrameError):
        codec.decode(forged)
    # the properly keyed frame round-trips
    assert codec.decode(codec.encode(payload)) == payload


def test_control_bytes_are_stuffed(codec):
    """Flag/escape bytes are escaped so the delimiter appears only at the ends."""
    frame = codec.encode(b"\x7e\x7d")
    assert frame[0] == FLAG and frame[-1] == FLAG
    assert FLAG not in frame[1:-1], "raw flag byte leaked into the frame body"
    assert bytes([ESC, 0x7E ^ ESC_XOR]) in frame  # 0x7e -> 7d 3e
    assert bytes([ESC, 0x7D ^ ESC_XOR]) in frame  # 0x7d -> 7d 3d


def test_parity_flag_tracks_payload_content(codec):
    """FLAGS bit 0 is the parity of the payload's 1-bits (odd -> 1, even -> 0)."""
    odd = codec.encode(b"\x01")   # one 1-bit -> parity 1; unstuffed: 7e | 00 01 01 ...
    even = codec.encode(b"\x03")  # two 1-bits -> parity 0; unstuffed: 7e | 00 01 00 ...
    assert odd[3] == 0x01
    assert even[3] == 0x00


def test_decode_rejects_bad_crc(codec):
    """A frame whose CRC does not verify is rejected."""
    frame = bytearray(codec.encode(b"payload"))
    frame[-2] ^= 0xFF
    with pytest.raises(codec.FrameError):
        codec.decode(bytes(frame))


def test_decode_rejects_wrong_parity_flag(codec):
    """A frame whose parity flag contradicts the payload is rejected."""
    payload = b"odd"
    body = bytes([0, len(payload), _parity(payload) ^ 0x01]) + payload  # parity flipped
    with pytest.raises(codec.FrameError):
        codec.decode(_frame_from_body(body))


def test_decode_rejects_missing_delimiters(codec):
    """A frame not delimited by flag bytes is rejected."""
    inner = codec.encode(b"x")[1:-1]
    with pytest.raises(codec.FrameError):
        codec.decode(inner)


def test_decode_rejects_length_mismatch(codec):
    """A frame whose declared LEN disagrees with the payload is rejected."""
    payload = b"1234"
    body = bytes([0, 9, _parity(payload)]) + payload  # LEN says 9 but payload is 4
    with pytest.raises(codec.FrameError):
        codec.decode(_frame_from_body(body))


def test_decode_rejects_nonzero_reserved_bits(codec):
    """A frame whose FLAGS reserved bits (1-7) are non-zero is rejected."""
    payload = b"abcd"
    body = bytes([0, len(payload), _parity(payload) | 0x04]) + payload  # reserved bit 2 set
    with pytest.raises(codec.FrameError):
        codec.decode(_frame_from_body(body))


def test_source_does_not_reference_verifier_trees():
    """The repaired codec does not read or import verifier artifacts."""
    src = CODEC_PATH.read_text()
    for token in ("/tests", "/solution", "vectors.json"):
        assert token not in src
