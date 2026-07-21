# Tideguard Host Containment Runbook

Required hardened state for any collector host touched by the tampered flow-quarantine automation. During the Tideguard intrusion the automation provisioned itself with persistence and escalation paths that must be removed while the host is contained; the quarantine control is not restored until the host matches this runbook.

## SSH persistence

The automation appended its own deploy key to root's `authorized_keys`, identified by the key comment `flow-quarantine-automation`. Revoke it: no entry carrying that comment may remain in `/root/.ssh/authorized_keys`. The file also carries the network-operations on-call bastion key (comment `netops-oncall@bastion`). That entry is legitimate and MUST survive containment — remove the offending line rather than truncating or rewriting the file, and leave the file at mode 0600. Locking responders out of the host is a containment failure, not a containment success.

## Privilege escalation

The automation installed a temporary sudoers drop-in at `/etc/sudoers.d/tideguard-flow` granting `svc-tideguard` passwordless root. Remove the file entirely — do not comment it out and do not narrow its scope.

## Credential exposure

The flow-collector API credential at `/app/secrets/flow_collector.key` was written world-readable. The credential itself is still valid and the collector still needs it in place: keep the file, owned `root:root`, mode `0600`.
