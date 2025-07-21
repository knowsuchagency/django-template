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
  - **Authentication**: @knowsuchagency/allauth-react with AllauthProvider
  - **Theme Support**: Dark/light mode with system preference detection
  - **Charts**: Recharts with theme-aware styling
  - **HTTP Client**: Native fetch with credentials for API calls
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
│   │   ├── ThemeToggle.tsx # Dark/light mode toggle
│   │   └── ui/        # shadcn/ui components (button, dropdown-menu)
│   ├── contexts/      # React contexts
│   │   └── ThemeContext.tsx # Theme state management
│   ├── lib/           # Utility functions
│   │   └── utils.ts   # Helper functions
│   └── pages/         # Page components
│       ├── Dashboard.tsx # Protected dashboard with charts
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

1. **Authentication Setup**: Use AllauthProvider and hooks:
```typescript
import { AllauthProvider, useAllauth } from '@knowsuchagency/allauth-react'

// In App.tsx
function App() {
  return (
    <AllauthProvider
      baseUrl={import.meta.env.DEV ? 'http://localhost:8000' : window.location.origin}
      csrfTokenEndpoint="/api/v1/csrf-token"
    >
      <AppRoutes />
    </AllauthProvider>
  )
}

// In components
const { user, login, logout, signup, isAuthenticated } = useAllauth()

// Login
await login({ email, password })

// Signup
await signup({ email, password })
```

2. **Protected Routes**: Use allauth hooks:
```typescript
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAllauth()
  
  if (isLoading) {
    return <div>Loading...</div>
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}
```

3. **API Integration**: Use standard fetch with credentials:
```typescript
// For custom API endpoints (not allauth endpoints)
const response = await fetch('/api/v1/example/stocks', {
  credentials: 'include',
  headers: {
    'Accept': 'application/json',
  }
})
const data = await response.json()
```

4. **Component Development**: Theme-aware components with shadcn/ui:
```typescript
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function MyComponent() {
  return (
    <div className="p-4 bg-background text-foreground">
      <Button variant="default">Primary Action</Button>
      
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon">
            <Sun className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem>Light</DropdownMenuItem>
          <DropdownMenuItem>Dark</DropdownMenuItem>
          <DropdownMenuItem>System</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
```

5. **Dark Mode Support**: Theme management with system preference detection:
```typescript
import { ThemeProvider, useTheme } from '@/contexts/ThemeContext'

// Wrap app with ThemeProvider
<ThemeProvider>
  <AllauthProvider>
    <App />
  </AllauthProvider>
</ThemeProvider>

// Use theme in components
const { theme, setTheme, effectiveTheme } = useTheme()

// Theme toggle component
import { ThemeToggle } from '@/components/ThemeToggle'
```

6. **Chart Integration**: Theme-aware Recharts visualization:
```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { useTheme } from '@/contexts/ThemeContext'

function MyChart() {
  const { effectiveTheme } = useTheme()
  
  const chartTheme = {
    grid: effectiveTheme === 'dark' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)',
    axis: effectiveTheme === 'dark' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)',
    tick: effectiveTheme === 'dark' ? 'rgba(255, 255, 255, 0.6)' : 'rgba(0, 0, 0, 0.6)',
  }
  
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} />
      <XAxis stroke={chartTheme.axis} tick={{ fill: chartTheme.tick }} />
      <YAxis stroke={chartTheme.axis} tick={{ fill: chartTheme.tick }} />
      <Tooltip />
      <Line type="monotone" dataKey="pv" stroke="#0070f3" />
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
  - Root route redirects to `/dashboard` (authenticated) or `/login` (unauthenticated)
  - Protected routes use `useAllauth()` hook for authentication checks
  - Removed static pages (Home, About, Contact) in favor of app-focused flow

- **API Integration**:
  - Use AllauthClient for all API calls
  - Handle loading states with `useState`
  - Display user-friendly error messages
  - Implement proper error handling

- **Styling**:
  - Use Tailwind CSS utility classes with theme-aware colors
  - Theme variables: `bg-background`, `text-foreground`, `border-border`, etc.
  - Follow shadcn/ui component patterns
  - Dark mode support via `.dark` class on document root
  - Vercel-style color palette for charts and UI elements

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
- Use `useAllauth()` hook for authentication operations (login, logout, signup)
- For custom API endpoints (e.g., `/api/v1/example/`), use standard fetch with credentials:
  ```typescript
  const response = await fetch('/api/v1/example/stocks', {
    credentials: 'include',
    headers: { 'Accept': 'application/json' }
  })
  ```
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