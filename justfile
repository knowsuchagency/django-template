# format/fix code
format:
    ruff check --fix
    ruff format
    npx prettier --write . --plugin=prettier-plugin-jinja-template

# initialize development
init:
    #!/bin/zsh
    echo "creating virtual environment"
    uv venv -p 3.12
    echo "installing dependencies"
    which concurrently || npm i -g concurrently
    uv pip install -r requirements.txt
    if [ ! -f .env ]; then
        echo "creating .env file with secret key"
        echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
    fi
    direnv allow
    npm install --save-dev prettier prettier-plugin-jinja-template

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

# reset database
resetdb:
    .venv/bin/python manage.py reset_db

# create superuser
createsuperuser:
    .venv/bin/python manage.py createsuperuser

# build theme and collect static files
collectstatic:
    .venv/bin/python manage.py collectstatic --noinput
