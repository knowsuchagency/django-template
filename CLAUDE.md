# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A **Copier template** that generates full-stack Django + React projects. The root contains `copier.yml` (template config) and `template/` (the actual project scaffold). Files ending in `.jinja` are Copier templates rendered with variables from `copier.yml`.

To generate a project: `copier copy . /path/to/new-project`

## Template Structure

- `copier.yml` — template variables (`project_name`, `project_slug`, `project_description`, `author_name`, `author_email`, `default_from_email`) and post-copy tasks
- `template/` — all project files; `.jinja` suffix files are rendered by Copier, plain files are copied as-is
- Post-copy tasks: symlinks `CLAUDE.md` to `.cursorrules`, runs `uv lock`, installs frontend deps

## Generated Project Stack

**Backend:** Django 5.1 + Django Ninja (`/api/v1/`) + DBOS durable workflows
**Frontend:** React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui
**Auth:** django-allauth (headless) + `@knowsuchagency/django-allauth` React hooks
**State:** Zustand (client) + TanStack Query (server)
**DB:** SQLite (dev) / PostgreSQL (prod), configured via `DATABASE_URL`
**Task runner:** mise (`mise.toml`), Python via `uv run`, JS via `bun`

## Key Architecture Decisions

- Custom `User` model with UUID PK in `core.models` — all generated projects use this from the start
- Django Ninja routers (not DRF) for API — auto-generates OpenAPI docs
- DBOS replaces Django-Q2/Celery for background tasks — runs in-process, no separate worker
- WhiteNoise serves static files; django-vite bridges Vite's dev server and production builds
- `WildcardCSRFMiddleware` in `core/middleware.py` enables wildcard patterns in `CSRF_TRUSTED_ORIGINS`
- React SPA served at `/app/`, with `spa_fallback` view catching sub-routes for client-side routing
- Session-based auth (not JWT) — allauth headless mode with CSRF cookies

## Commands for Generated Projects

```bash
mise run runserver          # Django (8000) + Vite (5173) concurrently
mise run test               # Django unit tests (in-memory SQLite) + Playwright e2e
mise run format             # ruff check --fix && ruff format
mise run migrate            # ensure_pg_schema + migrate + createcachetable
mise run makemigrations
mise run createsuperuser <email> <password> [--username <name>]
mise run shell              # Django shell
cd frontend && bun run dev  # Vite dev server only
```

## Testing in Generated Projects

- Backend: `uv run python manage.py test src.core.tests` (SQLite in-memory)
- Frontend e2e: `cd frontend && bun run test:e2e` (Playwright — Chromium, Firefox, WebKit)
- `mise run test` runs both sequentially

## Environment

Generated projects load env from `.env.development` or `.env.production` based on `MISE_ENV`. Key vars: `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `REDIS_URL`, `DBOS_CONDUCTOR_KEY`, `X_API_KEY`.

## Docker

`docker-compose.yml` provides: backend (Granian), postgres, redis, migrations runner, cache table creator. Multi-stage Dockerfile builds frontend with bun then collects static files.

## Editing the Template

When modifying `.jinja` files, remember that `{{ }}` and `{% %}` are Copier/Jinja2 syntax — don't confuse with Django template tags (which only appear in `.html` files inside `templates/`). Copier variables are defined in `copier.yml`.
