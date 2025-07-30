# Frontend build stage
FROM oven/bun:1 AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy frontend source files
COPY frontend/ ./

# Build the frontend
RUN bun run build

# Python base stage
FROM python:3.12-slim AS base

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

ENV PYTHONPATH=src
ENV PYTHONUNBUFFERED=1

COPY src/ ./src/
COPY manage.py ./

# Copy built frontend files from frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
COPY --from=frontend-builder /app/frontend/public ./frontend/public

# Worker stage
FROM base AS worker

CMD ["uv", "run", "python", "manage.py", "qcluster"]

# Web stage
FROM base AS web
RUN uv run python manage.py collectstatic --noinput
CMD ["uv", "run", "granian", "--host", "0.0.0.0", "--port", "8000", "--interface", "wsgi", "src.wsgi:application"]
