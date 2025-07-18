# Django Template

A simple Django template.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Available Commands](#available-commands)
- [Notes](#notes)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [mise](https://mise.jdx.dev/) (development environment manager)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/knowsuchagency/django-template.git
   cd django-template
   ```

2. Install dependencies:
   ```
   uv sync
   ```

3. Run database migrations:
   ```
   mise run migrate
   ```

4. Create a superuser (optional):
   ```
   mise run createsuperuser
   ```

5. Start the development server:
   ```
   mise run runserver
   ```

## Development

The project uses `mise` for task management. All Python commands are automatically prefixed with `uv run` to use the virtual environment.

## Available Commands

### Development
- `mise run runserver` - Start the development server on port 8000
- `mise run migrate` - Apply database migrations and create cache table
- `mise run makemigrations` - Create new migrations
- `mise run createsuperuser` - Create a superuser account
- `mise run shell` - Open Django shell

### Code Quality
- `mise run format` - Format code using ruff
- `mise run test` - Run tests with in-memory SQLite

### Static Files
- `mise run collectstatic` - Collect static files

### Django-Q Task Queue
- `mise run qcluster` - Run the task queue cluster
- `mise run qmonitor` - Monitor queue status
- `mise run setup_periodic_tasks` - Initialize periodic tasks

### Database
- `mise run flush` - Flush the database (requires confirmation)

## Notes

To use Lovable's built-in preview window, you'll need to note the request's actual unique origin i.e. `https://id-preview--d9666ffa-29be-443f-9013-25d5cd5c1beb.lovable.app` and add it to `CSRF_TRUSTED_ORIGINS`. 

It won't be what you might expect i.e. `https://preview--django-template-frontend-67.lovable.app`.
