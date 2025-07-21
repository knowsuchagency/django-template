# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Essential Commands

All Python commands must be prefixed with `uv run`.

### Development
```bash
mise run runserver       # Run dev server on port 8000
mise run migrate         # Apply migrations
mise run makemigrations  # Create new migrations
mise run test            # Run tests
mise run format          # Format code with ruff
```

### Frontend
```bash
cd frontend
bun install              # Install dependencies
bun run dev              # Run Vite dev server on port 5173
bun run build            # Build for production
```

## Architecture

Django 5.1.1 + Django Ninja API + React SPA with Vite

### Tech Stack
- **Backend**: Django with Django Ninja (`/api/v1/`)
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **Auth**: Django-allauth + @knowsuchagency/allauth-react
- **Task Queue**: Django-Q2 with Redis
- **Database**: SQLite (dev) / PostgreSQL (prod)

### Project Structure
```
src/
├── api/v1/            # Django Ninja API endpoints
├── core/              # Main Django app
│   ├── models.py      # Custom User model
│   ├── views.py       # Views using @route decorator
│   └── templates/index.html  # React app entry
└── settings.py

frontend/
├── src/
│   ├── components/    # React components
│   ├── pages/         # Page components
│   └── contexts/      # React contexts
└── vite.config.ts
```

## Key Patterns

### Django Views
```python
from djecorator import Route
route = Route()

@route("/app/")
def index(request):
    return render(request, "index.html")
```

### API Endpoints
```python
from ninja import Router
router = Router()

@router.get("/example")
def example(request):
    return {"message": "Hello"}
```

### React Authentication
```typescript
import { AllauthProvider, useAllauth } from '@knowsuchagency/allauth-react'

// In components
const { user, login, logout, signup, isAuthenticated } = useAllauth()
```

### API Calls
```typescript
// For custom endpoints
const response = await fetch('/api/v1/example', {
  credentials: 'include',
  headers: { 'Accept': 'application/json' }
})
```

## Environment Config

Uses `mise.toml` for environment variables:
- `DATABASE_URL`: SQLite default
- `REDIS_URL`: Optional Redis connection
- `SECRET_KEY`: Django secret
- `DEBUG`: Development mode flag