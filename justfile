# list commands
list:
    @just --list

# format/fix code
format:
    uvx ruff check --fix
    uvx ruff format

# initialize development
init schema:
    #!/bin/zsh
    echo "creating virtual environment"
    uv venv -p 3.12
    echo "installing dependencies"
    uv sync
    echo "creating .env file from template"
    op inject -i .env.template -o .env
    # replace $schema with the schema name
    sed -i '' "s/\$schema/{{schema}}/g" .env
    # replace shared\ with shared in .env
    sed -i '' "s/shared\\\\/shared/g" .env
    cat .env
    direnv allow

# run development server
runserver:
    DEBUG=true .venv/bin/python manage.py runserver

# make migrations
makemigrations:
    .venv/bin/python manage.py makemigrations

# migrate
migrate:
    .venv/bin/python manage.py migrate
    .venv/bin/python manage.py createcachetable

# flush database
flush:
    .venv/bin/python manage.py flush

# create superuser
createsuperuser:
    .venv/bin/python manage.py createsuperuser

# build theme and collect static files
collectstatic:
    .venv/bin/python manage.py collectstatic --noinput

# run tests
test:
    #!/bin/bash
    export DATABASE_URL=sqlite:///:memory:
    export LOG_REQUESTS=false
    uv run python manage.py test src.core.tests

# run q cluster
qcluster:
    uv run python manage.py qcluster

# monitor q cluster
qmonitor redis_url='':
    #!/bin/bash
    echo "redis_url: {{redis_url}}"
    if [ -z "{{redis_url}}" ]; then
        uv run python manage.py qmonitor
    else
        REDIS_URL={{redis_url}} uv run python manage.py qmonitor
    fi

# view q stats
qstats:
    uv run python manage.py qinfo
