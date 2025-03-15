# Django Template

A simple Django template.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Available Commands](#available-commands)
- [Security Features](#security-features)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [just](https://github.com/casey/just) (command runner)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/knowsuchagency/django-template.git
   cd django-template
   ```

2. Initialize the development environment:
   ```
   just init
   ```
   This will create a virtual environment, install dependencies, and set up the .env file.

## Development

To run the development server:

```bash
just runserver
```

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

For a full list of commands, run `just list`.
