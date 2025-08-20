# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Notes

- All Python commands must be prefixed with `uv run`
- Use `bun` instead of `npm` for frontend package management
- Always run `mise run test` after making changes
- Run `mise run format` to format Python code with ruff

## Quick Commands

```bash
# Start development servers
mise run runserver

# Run tests
mise run test

# Frontend development
cd frontend && bun run dev
```

## Code Patterns

- Use `@route` decorator from djecorator for Django views
- Use Django Ninja routers for API endpoints
- Access Zustand stores with selector pattern: `useStore((state) => state.value)`
- Use `useAllauth()` hook for authentication operations

## Testing

- Django tests use in-memory SQLite
- Always verify authentication flows work correctly
- Check that theme persistence works across sessions

## Architecture Overview

### Backend Structure
- **Django Ninja API** at `/api/v1/` - RESTful API with automatic OpenAPI generation
- **DBOS Workflows** - Durable task execution replacing Django-Q2, runs in main process
- **Custom User Model** in `core.models` - Extended Django User with UUID primary key
- **View Routing** - Uses `djecorator.Route` for cleaner URL patterns in views

### Frontend Architecture
- **React SPA** served at `/app/` in production, `/static/` in development
- **TanStack Query** - Server state management with automatic caching, refetching, and deduplication
- **Zustand** - Client state for auth sync and theme persistence
- **django-allauth integration** - Authentication with built-in TanStack Query support

### API Integration Pattern
```typescript
// 1. Define query functions in src/api/
// 2. Create custom hooks with useQuery/useMutation
// 3. Use hooks in components for automatic state management
```

### Authentication Flow
- django-allauth handles backend auth with session cookies
- `@knowsuchagency/django-allauth` provides React hooks with TanStack Query
- `useAuthStore` syncs auth state from allauth hooks to Zustand
- Protected routes check `isAuthenticated` from store

### Database Configuration
- Development: SQLite by default
- Production: PostgreSQL required for DBOS workflows
- `DATABASE_URL` auto-transforms to `DBOS_DATABASE_URL` for workflow execution

## Development Workflow

```bash
# Initial setup
mise install
mise run migrate
cd frontend && bun install

# Development
mise run runserver  # Runs Django + Vite concurrently

# Database changes
mise run makemigrations
mise run migrate

# Code quality
mise run format  # Auto-format with ruff
mise run test    # Run all tests
```

## Environment Variables

Key variables in `mise.toml`:
- `DATABASE_URL` - Required for DBOS (PostgreSQL in production)
- `CSRF_TRUSTED_ORIGINS` - Must include frontend origin for API calls
- `DEBUG` - Enables development features
- `SECRET_KEY` - Auto-generated if not set