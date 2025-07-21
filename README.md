# Django Template

A modern Django + React template with authentication, API, and task queue support.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Project Structure](#project-structure)
- [Available Commands](#available-commands)
- [Key Patterns](#key-patterns)
- [Environment Configuration](#environment-configuration)
- [Notes](#notes)

## Tech Stack

- **Backend**: Django 5.1.1 with Django Ninja API (`/api/v1/`)
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **State Management**: Zustand with persist middleware
- **Authentication**: Django-allauth + @knowsuchagency/allauth-react
- **Task Queue**: Django-Q2 with Redis
- **Database**: SQLite (development) / PostgreSQL (production)
- **Build Tools**: Vite (frontend), uv (Python), mise (task runner)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [mise](https://mise.jdx.dev/) (development environment manager)
- [bun](https://bun.sh/) (JavaScript runtime and package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/knowsuchagency/django-template.git
   cd django-template
   ```

2. Install dependencies:
   ```bash
   mise install
   ```

3. Run database migrations:
   ```bash
   mise run migrate
   ```

4. Create a superuser (optional):
   ```bash
   mise run createsuperuser
   ```

5. Install frontend dependencies:
   ```bash
   cd frontend
   bun install
   cd ..
   ```

6. Start the development servers:
   ```bash
   mise run runserver  # Starts both Django and Vite
   ```

## Development

The project uses `mise` for task management. All Python commands are automatically prefixed with `uv run` to use the virtual environment.

- Django server runs on http://localhost:8000
- Vite dev server runs on http://localhost:5173
- React app is served at http://localhost:8000/app/

## Project Structure

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
│   ├── stores/        # Zustand stores
│   └── types/         # TypeScript types
└── vite.config.ts
```

## Available Commands

### Development
- `mise run runserver` - Start dev servers (Django on 8000, Vite on 5173)
- `mise run migrate` - Apply database migrations
- `mise run makemigrations` - Create new migrations
- `mise run test` - Run tests with in-memory SQLite
- `mise run format` - Format code with ruff

### Frontend
```bash
cd frontend
bun install              # Install dependencies
bun run dev              # Run Vite dev server on port 5173
bun run build            # Build for production
```

### Database & Admin
- `mise run createsuperuser` - Create admin user
- `mise run shell` - Django shell
- `mise run flush` - Flush database (requires confirmation)

### Static Files
- `mise run collectstatic` - Collect static files

### Django-Q Task Queue
- `mise run qcluster` - Run task queue cluster
- `mise run qmonitor` - Monitor queue status
- `mise run setup_periodic_tasks` - Initialize periodic tasks

## Key Patterns

### Django Views (using djecorator)
```python
from djecorator import Route
route = Route()

@route("/app/")
def index(request):
    return render(request, "index.html")
```

### API Endpoints (Django Ninja)
```python
from ninja import Router
router = Router()

@router.get("/example")
def example(request):
    return {"message": "Hello"}
```

### State Management (Zustand)
```typescript
// Auth store
import { useAuthStore } from '@/stores/authStore'
const user = useAuthStore((state) => state.user)

// Theme store with persistence
import { useThemeStore } from '@/stores/themeStore'
const { theme, setTheme } = useThemeStore()
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

## Environment Configuration

The project uses `mise.toml` for environment variables:

- `DATABASE_URL` - Database connection (default: `sqlite:///data.db`)
- `REDIS_URL` - Redis connection for cache/queue (optional)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Development mode flag
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `CSRF_TRUSTED_ORIGINS` - Required for cross-origin requests

## Notes

### Lovable Preview
To use Lovable's built-in preview window, you'll need to note the request's actual unique origin (e.g., `https://id-preview--d9666ffa-29be-443f-9013-25d5cd5c1beb.lovable.app`) and add it to `CSRF_TRUSTED_ORIGINS`.

### Docker Support
The project includes Docker configuration for production deployment:
```bash
docker-compose up  # Full stack with PostgreSQL and Redis (no workers by default)

# Run with workers enabled
WORKER_REPLICAS=1 docker-compose up

# Run with multiple workers
WORKER_REPLICAS=3 docker-compose up
```

Workers are disabled by default (`WORKER_REPLICAS=0`). Set the `WORKER_REPLICAS` environment variable to enable background task processing.