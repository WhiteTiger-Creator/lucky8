#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Contain the host per /app/docs/containment_runbook.md ---

# Revoke the rogue operator key, preserving any other key in the file.
if [ -f /root/.ssh/authorized_keys ]; then
  grep -v 'sentinel-remediation-operator' /root/.ssh/authorized_keys > /root/.ssh/authorized_keys.tmp || true
  mv /root/.ssh/authorized_keys.tmp /root/.ssh/authorized_keys
  chmod 600 /root/.ssh/authorized_keys
fi

# Remove the passwordless sudoers escalation entirely.
rm -f /etc/sudoers.d/sentinel-quarantine

# Lock down the exposed quarantine credential (keep it, restrict to root 0600).
chown root:root /app/secrets/quarantine.cred
chmod 0600 /app/secrets/quarantine.cred

# --- Produce the remediation plan ---
cp "${SCRIPT_DIR}/remediate_ref.py" /app/remediate.py
python3 /app/remediate.py --output-dir /app/output
