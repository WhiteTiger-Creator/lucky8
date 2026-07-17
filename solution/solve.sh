#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "${SCRIPT_DIR}/remediate_ref.py" /app/remediate.py
python3 /app/remediate.py --output-dir /app/output
