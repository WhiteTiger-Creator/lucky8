#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Host containment per /app/docs/containment_runbook.md ---
# Revoke the automation's SSH persistence surgically: drop only the rogue entry so
# the netops on-call bastion key survives and responders keep access.
if [ -f /root/.ssh/authorized_keys ]; then
  grep -v 'flow-quarantine-automation' /root/.ssh/authorized_keys > /root/.ssh/authorized_keys.tmp || true
  mv /root/.ssh/authorized_keys.tmp /root/.ssh/authorized_keys
  chmod 600 /root/.ssh/authorized_keys
fi

# Remove the passwordless sudoers escalation entirely.
rm -f /etc/sudoers.d/tideguard-flow

# Lock down the exposed flow-collector credential: keep it, restrict to root 0600.
chown root:root /app/secrets/flow_collector.key
chmod 0600 /app/secrets/flow_collector.key

cp "${SCRIPT_DIR}/flow_audit.py" /app/flow_audit.py
python3 /app/flow_audit.py repair --output-dir /app/output
