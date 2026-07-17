#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Restore the repaired codec, then exercise it against the sample payloads to
# confirm it actually encodes and round-trips (rather than shipping a static
# answer): encode each smoke-test payload and decode it back to the original.
cp "${SCRIPT_DIR}/codec_fixed.py" /app/codec.py

python3 - <<'PY'
import importlib.util
import json

spec = importlib.util.spec_from_file_location("codec", "/app/codec.py")
codec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codec)

samples = json.loads(open("/app/samples/vectors.json").read())
for payload_hex in samples.get("payloads_hex", []):
    payload = bytes.fromhex(payload_hex)
    frame = codec.encode(payload)
    assert codec.decode(frame) == payload, payload_hex
print("codec restored and round-trips on all sample payloads")
PY
