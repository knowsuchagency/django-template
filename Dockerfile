FROM python:3.12-slim AS backend

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY backend/ ./backend/
COPY manage.py ./

CMD ["uv", "run", "granian", "--host", "0.0.0.0", "--port", "8000", "--interface", "wsgi", "backend.wsgi:application"]

FROM node:20-slim AS frontend

WORKDIR /app

COPY frontend/package.json frontend/pnpm-lock.yaml ./

RUN npx pnpm install

COPY frontend .

RUN npm run build

CMD ["npm", "run", "start"]
