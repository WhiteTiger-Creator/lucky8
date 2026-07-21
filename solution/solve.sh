#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "${SCRIPT_DIR}/flow_audit.py" /app/flow_audit.py
python3 /app/flow_audit.py repair --output-dir /app/output
