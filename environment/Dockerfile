FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tmux \
        asciinema \
    && rm -rf /var/lib/apt/lists/*

# Fully resolved verifier lock; --no-deps keeps installation deterministic.
COPY requirements.lock /tmp/requirements.lock
RUN python3 -m pip install --no-cache-dir --no-deps \
        -r /tmp/requirements.lock

WORKDIR /app

COPY app/ /app/
RUN cp /app/workflow/export_report.py /app/workflow/.export_report.original \
    && chmod a-w /app/workflow/.export_report.original

# Persistence and escalation paths left behind by the tampered flow-quarantine
# automation during the Tideguard intrusion (rogue SSH key, passwordless sudoers
# escalation, and a world-readable flow-collector credential).
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh \
    && printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH7pQ2mVc4tXbN9sKfWjLd0aRyEuZoPnT3xBvMqGhKlS netops-oncall@bastion\n' > /root/.ssh/authorized_keys \
    && printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJx4jTq0d6nUcy0dGkzsBv1qkNPjc3hAcVcbWlkfZ2Qq flow-quarantine-automation\n' >> /root/.ssh/authorized_keys \
    && chmod 600 /root/.ssh/authorized_keys \
    && mkdir -p /etc/sudoers.d \
    && printf 'svc-tideguard ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/tideguard-flow \
    && chmod 0440 /etc/sudoers.d/tideguard-flow \
    && mkdir -p /app/secrets \
    && printf 'collector-synthetic-9f3a7c1e5b28-DO-NOT-USE\n' > /app/secrets/flow_collector.key \
    && chmod 0644 /app/secrets/flow_collector.key
