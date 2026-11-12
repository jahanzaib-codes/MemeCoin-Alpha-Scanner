# Multi-stage Dockerfile for MemeCoin-Alpha-Scanner
# Optimized for low attack-surface, high-speed execution, and minimal image size

FROM python:3.11-slim as builder

WORKDIR /app

# Install build essentials if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final runtime image
FROM python:3.11-slim as runner

WORKDIR /app

# Create unprivileged service user
RUN groupadd -r scanner && useradd -r -g scanner scanner

# Copy dependencies from builder stage
COPY --from=builder /root/.local /home/scanner/.local
COPY --chown=scanner:scanner . /app

ENV PATH=/home/scanner/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER scanner

ENTRYPOINT ["python", "cli.py"]
CMD ["scan"]
