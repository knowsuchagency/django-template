# Web Template

A simple web template for a Django backend and a React frontend.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Available Commands](#available-commands)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12
- Node.js and pnpm
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [just](https://github.com/casey/just) (command runner)
- [direnv](https://direnv.net/) (environment variable manager)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/knowsuchagency/web_template.git
   cd web_template
   ```

2. Initialize the development environment:
   ```
   just init
   ```
   This will create a virtual environment, install dependencies, set up the .env file, and install frontend dependencies.

## Development

To run the development server for both backend and frontend:

```bash
just dev
```

This will start the Django server and the Next.js development server concurrently.

## Available Commands

Use `just <command>` to run the following commands:

- `list`: Show all available commands
- `format`: Format and fix code using ruff and prettier
- `runserver`: Run Django development server
- `makemigrations`: Create new database migrations
- `migrate`: Apply database migrations
- `flush`: Flush the database
- `createsuperuser`: Create a Django superuser
- `collectstatic`: Collect static files
- `frontend`: Run the Next.js development server

For a full list of commands, run `just list`.
