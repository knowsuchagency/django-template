# initialize development
init:
    pkgx python@3.11 -m venv .venv
    npm i -g concurrently
    .venv/bin/pip install -U pip
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python manage.py tailwind install

# run development server
runserver:
    DEBUG=true concurrently -n tailwind,django ".venv/bin/python manage.py tailwind start" "sleep 3 && .venv/bin/python manage.py runserver"

# make migrations
makemigrations:
    .venv/bin/python manage.py makemigrations

# migrate
migrate:
    .venv/bin/python manage.py migrate

# reset database
resetdb:
    .venv/bin/python manage.py reset_db

# create superuser
createsuperuser:
    .venv/bin/python manage.py createsuperuser

# build theme and collect static files
collectstatic:
    .venv/bin/python manage.py tailwind build
    .venv/bin/python manage.py collectstatic --noinput

# initialize zappa
init-zappa:
    .venv/bin/pip install zappa
    .venv/bin/zappa init || echo "zappa already initialized"

# deploy to aws lambda
deploy-zappa: init-zappa
    #!/bin/zsh
    . .venv/bin/activate
    just collectstatic
    zappa deploy || zappa update

# undeploy from aws lambda
undeploy-zappa:
    .venv/bin/zappa undeploy
