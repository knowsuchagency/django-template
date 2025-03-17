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
    uv run python manage.py test src.core.tests
