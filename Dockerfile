# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# Set the working directory inside the container
WORKDIR /app

# --- Builder Stage ---
# This stage installs dependencies into a virtual environment
FROM base AS builder

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Create and activate the virtual environment
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy only the requirements file first to leverage Docker's caching
# Note the 'server/' prefix in the path
COPY server/requirements.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# --- Final Stage ---
# This stage creates the final, lean image for running the application
FROM base AS final

# Install any runtime-only system dependencies (like curl for the healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy your application code and config files from the 'server' directory
# Note the 'server/' prefix on all these paths
COPY server/app ./app
COPY server/alembic.ini .
COPY server/alembic ./alembic

# Create a non-root user for better security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Healthcheck to let Netlify know the app is running correctly
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/healthz || exit 1

# The command to start your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]