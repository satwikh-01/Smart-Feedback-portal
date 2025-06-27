FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY ./app ./app
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

RUN adduser --disabled-password appuser && chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
