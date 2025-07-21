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

### Frontend Development
```bash
cd frontend
bun install              # Install frontend dependencies
bun run dev              # Run Vite dev server on port 5173
bun run build            # Build frontend for production
bun run preview          # Preview production build
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
- **Frontend**: React SPA with Vite, served at `/app`
  - **Build Tool**: Vite for fast development and optimized production builds
  - **UI Framework**: Tailwind CSS v4 with shadcn/ui components
  - **Routing**: React Router v7 with protected routes
  - **State Management**: React Context API
  - **Authentication**: @knowsuchagency/allauth-react for Django integration
  - **Charts**: Recharts for data visualization
  - **HTTP Client**: Built-in AllauthClient for API calls
- **Server-side Templates**: DaisyUI v5 + Alpine.js v3 (legacy views)
- **Caching**: Redis primary, database cache fallback
- **Static Files**: WhiteNoise for production serving

### Project Structure
```
src/
├── api/                # Django Ninja API
│   ├── __init__.py    # API configuration with auth
│   └── v1/            # Version 1 API endpoints
│       ├── router.py  # Main API router
│       └── auth.py    # Authentication endpoints
├── core/              # Main Django app
│   ├── models.py      # Custom User model (UUID field required)
│   ├── views.py       # Views using @route decorator
│   ├── tasks.py       # Async and scheduled tasks
│   ├── middleware.py  # Request logging, wildcard CSRF
│   └── templates/     # Django templates
│       └── index.html # React app entry point
└── settings.py        # Django configuration

frontend/              # React frontend application
├── src/
│   ├── App.tsx        # Main React component
│   ├── main.tsx       # Application entry point
│   ├── components/    # Reusable React components
│   │   ├── Layout.tsx # App layout with navigation
│   │   └── ui/        # shadcn/ui components
│   ├── contexts/      # React contexts
│   │   └── AuthContext.tsx # Authentication state management
│   ├── lib/           # Utility functions
│   │   ├── auth.ts    # AllauthClient configuration
│   │   └── utils.ts   # Helper functions
│   └── pages/         # Page components
│       ├── Dashboard.tsx # Protected dashboard page
│       ├── Login.tsx     # Login page
│       └── Signup.tsx    # Signup page
├── vite.config.ts     # Vite configuration
├── package.json       # Frontend dependencies
└── bun.lock          # Bun lockfile
```

### Key Development Patterns

1. **Django Route Definition**: Use djecorator for server views:
```python
from djecorator import Route
route = Route()

# Redirect root to React app
@route("/")
def root_redirect(request):
    return redirect("/app/")

# Serve React SPA
@route("/app/")
def index(request):
    return render(request, "index.html")

# Catch-all for client-side routing
@route("/app/<path:path>")
def spa_fallback(request, path):
    return render(request, "index.html")
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

### React Development Patterns

1. **Authentication Flow**: Use AllauthClient for API calls:
```typescript
import { AllauthClient } from '@knowsuchagency/allauth-fetch'

export const authClient = new AllauthClient({
  apiBaseUrl: import.meta.env.DEV 
    ? 'http://localhost:8000' 
    : window.location.origin
})

// Login
await authClient.login({ username, password })

// Get user
const user = await authClient.getUser()

// Logout
await authClient.logout()
```

2. **Protected Routes**: Use authentication context:
```typescript
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div>Loading...</div>
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}
```

3. **API Integration**: AllauthClient handles CSRF automatically:
```typescript
// API calls with automatic CSRF token handling
const response = await authClient.request('/api/v1/data')
const data = await response.json()
```

4. **Component Development**: Use TypeScript with shadcn/ui:
```typescript
import { Button } from "@/components/ui/button"

export function MyComponent() {
  return (
    <div className="p-4">
      <Button onClick={() => console.log('clicked')}>
        Click me
      </Button>
    </div>
  )
}
```

5. **Chart Integration**: Use Recharts for data visualization:
```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

const data = [
  { name: 'Page A', uv: 4000, pv: 2400 },
  { name: 'Page B', uv: 3000, pv: 1398 },
]

function MyChart() {
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="pv" stroke="#8884d8" />
    </LineChart>
  )
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

### Vite Configuration

`frontend/vite.config.ts` key settings:
- `base: "/static/"` - Ensures assets are served from Django's static URL
- `server.proxy` - Proxies API calls to Django during development:
  - `/api` → `http://localhost:8000`
  - `/accounts` → `http://localhost:8000`
  - `/admin` → `http://localhost:8000`

### Frontend Development Guidelines

- **React Components**: 
  - Use TypeScript for type safety
  - Follow functional component patterns with hooks
  - Use shadcn/ui components for consistent UI
  - Implement proper error boundaries

- **State Management**:
  - Use React Context for global state (auth, theme)
  - Keep component state local when possible
  - Use `useReducer` for complex state logic

- **Routing**:
  - React Router v7 handles client-side routing
  - All React routes must be under `/app` prefix
  - Use `<Navigate>` for redirects
  - Implement route guards for protected pages

- **API Integration**:
  - Use AllauthClient for all API calls
  - Handle loading states with `useState`
  - Display user-friendly error messages
  - Implement proper error handling

- **Styling**:
  - Use Tailwind CSS utility classes
  - Follow shadcn/ui component patterns
  - Use CSS modules for component-specific styles
  - Maintain consistent spacing with Tailwind's design system

- **Form Handling**:
  - Use controlled components with React state
  - Implement client-side validation
  - Show validation errors inline
  - Handle form submission with proper error states

### Testing Guidelines

**Backend Testing**:
- Tests use in-memory SQLite to avoid database dependencies
- Redis is flushed in tearDown to prevent test pollution
- Run with `mise run test` (sets DATABASE_URL and LOG_REQUESTS=false)
- Test files: `src/core/tests.py`

**Frontend Testing**:
- Use Vitest for unit and integration tests
- Test React components with React Testing Library
- Mock API calls with MSW (Mock Service Worker)
- Run with `bun test` in the frontend directory

### API Integration

**Authentication Endpoints** (`/api/v1/auth/`):
- `GET /user` - Get current user info
- `POST /login` - Login with username/email and password
- `POST /logout` - Logout current user
- `POST /signup` - Create new account
- `GET /csrf-token` - Get CSRF token for forms

**Frontend-Backend Communication**:
- AllauthClient automatically handles CSRF tokens
- All API calls require authentication except login/signup
- Session-based authentication with httpOnly cookies
- CORS configured for development with Vite proxy

**API Response Format**:
```typescript
// Success response
{
  "data": { ... },
  "status": "success"
}

// Error response
{
  "error": "Error message",
  "status": "error"
}
```

### Security Considerations

- Custom User model requires email field
- CSRF protection with wildcard domain support via custom middleware
- Staff-only views use `@staff_member_required` decorator
- Debug mode includes auth bypass for Lovable preview (check for `HTTP_X_LOVABLE_PREVIEW`)
- React app served from `/app` to avoid route conflicts
- API authentication uses Django sessions with CSRF protection

### Docker Development

Use `docker-compose up` for full stack with:
- Backend web server (Granian ASGI)
- Django-Q worker processes
- Redis cache/broker
- PostgreSQL database
- Auto-migration on startup