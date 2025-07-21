# CLAUDE.md

This file provides Claude-specific guidance when working with this repository.

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