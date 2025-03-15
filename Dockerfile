FROM python:3.12-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY src/ ./src/
COPY manage.py ./

ENV PYTHONUNBUFFERED=1

RUN uv run python manage.py collectstatic --noinput

CMD ["uv", "run", "granian", "--host", "0.0.0.0", "--port", "8000", "--interface", "wsgi", "src.wsgi:application"]
