FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tmux \
        asciinema \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock /tmp/requirements.lock
RUN python3 -m pip install --no-cache-dir --no-deps \
        -r /tmp/requirements.lock

WORKDIR /app

COPY app/ /app/

# Compromised host state left behind by the Sentinel-1 intrusion (the task
# requires the responder to contain it; values are synthetic, not real
# credentials): a rogue operator key in root's authorized_keys, a passwordless
# sudoers escalation, and a world-readable quarantine-service credential.
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh \
    && printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJx4jTq0d6nUcy0dGkzsBv1qkNPjc3hAcVcbWlkfZ2Qq sentinel-remediation-operator\n' >> /root/.ssh/authorized_keys \
    && chmod 600 /root/.ssh/authorized_keys \
    && mkdir -p /etc/sudoers.d \
    && printf 'svc-quarantine ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/sentinel-quarantine \
    && chmod 0440 /etc/sudoers.d/sentinel-quarantine \
    && mkdir -p /app/secrets \
    && printf 'quarantine-synthetic-4f3e2d1c0b9a-DO-NOT-USE\n' > /app/secrets/quarantine.cred \
    && chmod 0644 /app/secrets/quarantine.cred
