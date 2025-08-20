# Django Project

A modern Django + React application with authentication, API, and task queue support.

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
- **State Management**: Zustand for client state
- **API Client**: TanStack Query (React Query) for server state
- **Authentication**: Django-allauth + @knowsuchagency/django-allauth (with built-in TanStack Query)
- **Background Tasks**: [DBOS](https://www.dbos.dev/) for durable workflow execution
- **Database**: PostgreSQL
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
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies:
   ```bash
   mise install
   ```

3. Initialize environment variables (optional, requires 1Password CLI):
   ```bash
   mise run init  # Creates .env from .env.template using 1Password
   ```
   This command uses the 1Password CLI to inject secrets from your vault into a local `.env` file.
   If you don't use 1Password, manually create `.env` from `.env.template`.

4. Run database migrations:
   ```bash
   mise run migrate
   ```

5. Create a superuser (optional):
   ```bash
   mise run createsuperuser
   ```

6. Start the development servers:
   ```bash
   mise run runserver  # Starts both Django and Vite
   ```

## Development

The project uses `mise` for task management. All Python commands are automatically prefixed with `uv run` to use the virtual environment.

- Django server runs on http://localhost:8000
- Vite dev server runs on http://localhost:5173

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
│   ├── api/           # TanStack Query hooks and API functions
│   ├── components/    # React components
│   ├── lib/           # Utilities and query client config
│   ├── pages/         # Page components
│   ├── stores/        # Zustand stores
│   └── types/         # TypeScript types
└── vite.config.ts
```

## Available Commands

### Setup
- `mise run init` - Initialize the project (install deps, setup DB, migrations, frontend)

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

### DBOS TaskS
DBOS provides durable background task execution with automatic retries and workflow recovery. It also supports cron jobs. Tasks are stored in PostgreSQL for reliability.

Note: DBOS requires a PostgreSQL database connection configured via `DATABASE_URL` environment variable.

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
import { AllauthProvider, useAuth } from '@knowsuchagency/django-allauth'

// In components
const { 
  user, 
  isAuthenticated,
  login, 
  logout, 
  signup,
  isLoggingIn,
  isSigningUp,
  loginError,
  signupError 
} = useAuth()
```

### API Calls with TanStack Query
```typescript
// Using custom hooks with automatic caching and refetching
import { useStocks, useStockSymbols } from '@/api/stocks'

function Component() {
  const { data, isLoading, error, refetch } = useStocks()
  const { data: symbols } = useStockSymbols()
  
  // Data is automatically cached, deduplicated, and refetched
}

// Legacy fetch approach (for one-off requests)
const response = await fetch('/api/v1/example', {
  credentials: 'include',
  headers: { 'Accept': 'application/json' }
})
```

## Environment Configuration

The project uses `mise.toml` for environment variables:

- `DATABASE_URL` - Database connection.
- `REDIS_URL` - Redis connection for cache (optional, no longer needed for task queue)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Development mode flag
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `CSRF_TRUSTED_ORIGINS` - Required for cross-origin requests

## Notes

### Docker Support
The project includes Docker configuration for production deployment:
```bash
docker-compose up  # Full stack with PostgreSQL
```
