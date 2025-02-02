FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY backend/ ./backend/
COPY manage.py ./

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "granian", "--host", "0.0.0.0", "--port", "8000", "--interface", "wsgi", "backend.wsgi:application"]
