FROM python:3.12-slim AS base

# Builder stage: install build dependencies and Python packages into a venv
FROM base AS builder
WORKDIR /app

# Install system build dependencies (for pip packages with native extensions)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install dependencies using pip cache
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Final stage: minimal runtime image
FROM base AS final
WORKDIR /app

# Install runtime dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code.
# The lines for copying alembic.ini and the alembic directory have been removed.
COPY app ./app
COPY run.sh .

# Make the run script executable
RUN chmod +x ./run.sh

# Create and use a non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# # Healthcheck endpoint
# HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:${PORT:-8000}/healthz || exit 1

# Entrypoint: run the FastAPI app with the startup script
CMD ["./run.sh"]
