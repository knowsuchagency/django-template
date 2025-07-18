# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

All Python commands must be prefixed with `uv run` to use the virtual environment.

### Development Setup
```bash
mise run runserver       # Run dev server on port 8000
mise run migrate         # Apply migrations and create cache table
mise run makemigrations  # Create new migrations
mise run createsuperuser # Create admin user
mise run collectstatic   # Collect static files
```

### Testing & Code Quality
```bash
mise run test            # Run tests (uses in-memory SQLite)
mise run format          # Format code with ruff
```

### Django-Q Task Queue
```bash
mise run qcluster        # Run task queue cluster
mise run qmonitor        # Monitor queue status
mise run setup_periodic_tasks # Initialize periodic tasks
```

### Database Operations
```bash
mise run flush           # Flush database (requires confirmation)
mise run shell           # Django shell
```

## Architecture Overview

This is a Django 5.1.1 project using Django Ninja for API development and Django-Q2 for async task processing.

### Core Technologies
- **API Framework**: Django Ninja with versioned endpoints (`/api/v1/`)
- **Task Queue**: Django-Q2 with Redis broker
- **Authentication**: Django-allauth with custom User model
- **Frontend**: Server-side templates with djecorator routing
  - **UI Framework**: DaisyUI v5 (based on Tailwind CSS v4)
  - **JavaScript**: Alpine.js v3 with alpine-ajax for reactivity
  - **Charts**: ECharts v5 for data visualization
  - **Form Styling**: django-widget-tweaks for form customization
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

4. **Frontend Reactivity**: Use Alpine.js with alpine-ajax:
```html
<!-- Alpine.js component with state management -->
<div x-data="{ selectedItem: '', items: [] }">
    <!-- Use alpine-ajax for server-rendered HTML updates -->
    <button @click="$ajax('/api/endpoint', { target: 'result' })">Load</button>
    
    <!-- Or use fetch for JSON APIs with Alpine.js reactivity -->
    <button @click="fetch('/api/data').then(r => r.json()).then(d => items = d)">Refresh</button>
    
    <div id="result">
        <!-- Content updated by alpine-ajax -->
    </div>
</div>
```

5. **Chart Integration**: Use ECharts with Alpine.js:
```javascript
function chartComponent() {
    return {
        chart: null,
        initChart() {
            this.chart = echarts.init(document.getElementById('chartContainer'), 'dark');
            this.updateChart();
        },
        async updateChart() {
            const data = await fetch('/api/chart-data').then(r => r.json());
            this.chart.setOption({
                // ECharts configuration
            });
        }
    }
}
```

### Environment Configuration

The project uses `mise.toml` for environment configuration. Key variables:
- `DATABASE_URL`: SQLite database (default: `sqlite:///data.db`)
- `REDIS_URL`: Redis connection for cache/queue (optional)
- `CSRF_TRUSTED_ORIGINS`: Required for cross-origin requests
- `DEBUG`: Development mode flag
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Frontend Development Guidelines

- **Alpine.js**: Preferred for all interactive components
  - Use `x-data` for component state
  - Use `x-model` for two-way data binding
  - Use `@event` syntax for event handlers
  - Initialize components with `x-init`

- **alpine-ajax**: Use for server-side HTML updates
  - Use `x-target` attribute to specify update targets
  - Use `$ajax()` magic helper for programmatic requests
  - Supports events: `ajax:before`, `ajax:success`, `ajax:error`
  - Use `x-merge` for advanced DOM updates (append, prepend, morph)

- **Data Fetching**:
  - Use alpine-ajax for HTML responses
  - Use fetch API with Alpine.js for JSON APIs
  - Always handle loading and error states

- **Form Handling**:
  - Use Django forms with widget-tweaks for styling
  - Enhance with Alpine.js for client-side validation
  - Use alpine-ajax for inline form submissions

### Testing Guidelines

- Tests use in-memory SQLite to avoid database dependencies
- Redis is flushed in tearDown to prevent test pollution
- Run with `mise run test` (sets DATABASE_URL and LOG_REQUESTS=false)
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