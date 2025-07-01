# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

All Python commands must be prefixed with `uv run` to use the virtual environment.

### Development Setup
```bash
just init <schema>        # Initialize dev environment with database schema
just runserver           # Run dev server on port 8000
just migrate             # Apply migrations and create cache table
just makemigrations      # Create new migrations
just createsuperuser     # Create admin user
just collectstatic       # Collect static files
```

### Testing & Code Quality
```bash
just test                # Run tests (uses in-memory SQLite)
just format              # Format code with ruff
```

### Django-Q Task Queue
```bash
just qcluster            # Run task queue cluster
just qmonitor            # Monitor queue status
just setup_periodic_tasks # Initialize periodic tasks
```

### Database Operations
```bash
just flush               # Flush database (requires confirmation)
just shell               # Django shell
```

## Architecture Overview

This is a Django 5.1.1 project using Django Ninja for API development and Django-Q2 for async task processing.

### Core Technologies
- **API Framework**: Django Ninja with versioned endpoints (`/api/v1/`)
- **Task Queue**: Django-Q2 with Redis broker
- **Authentication**: Django-allauth with custom User model
- **Frontend**: Server-side templates with djecorator routing
- **Caching**: Redis primary, database cache fallback
- **Static Files**: WhiteNoise for production serving

### Project Structure
```
src/
├── api/                # Django Ninja API
│   ├── __init__.py    # API configuration with auth
│   └── v1/            # Version 1 API endpoints
├── core/              # Main Django app
│   ├── models.py      # Custom User model (UUID field required)
│   ├── views.py       # Views using @route decorator
│   ├── tasks.py       # Async and scheduled tasks
│   └── middleware.py  # Request logging, wildcard CSRF
└── settings.py        # Django configuration
```

### Key Development Patterns

1. **Route Definition**: Use djecorator for views:
```python
from djecorator import Route
route = Route()

@route("/dashboard/", login_required=True)
def dashboard(request):
    return render(request, "core/dashboard.html")
```

2. **API Endpoints**: Use Django Ninja routers:
```python
from ninja import Router
router = Router()

@router.get("/example")
def example(request):
    return {"message": "Hello"}
```

3. **Task Queue**: Define async tasks:
```python
from django_q.tasks import async_task, schedule

def my_task():
    # Task logic here
    pass

# Queue a task
async_task(my_task)
```

### Environment Configuration

The project uses `.env` files with 1Password integration. Key variables:
- `DATABASE_URL`: PostgreSQL with schema support
- `REDIS_URL`: Redis connection for cache/queue
- `CSRF_TRUSTED_ORIGINS`: Required for cross-origin requests
- `DEBUG`: Development mode flag

### Testing Guidelines

- Tests use in-memory SQLite to avoid database dependencies
- Redis is flushed in tearDown to prevent test pollution
- Run with `just test` (sets DATABASE_URL and LOG_REQUESTS=false)
- Test files: `src/core/tests.py`

### Security Considerations

- Custom User model requires email field
- CSRF protection with wildcard domain support via custom middleware
- Staff-only views use `@staff_member_required` decorator
- Debug mode includes auth bypass for Lovable preview (check for `HTTP_X_LOVABLE_PREVIEW`)

### Docker Development

Use `docker-compose up` for full stack with:
- Backend web server (Granian ASGI)
- Django-Q worker processes
- Redis cache/broker
- PostgreSQL database
- Auto-migration on startup