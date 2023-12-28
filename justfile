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

# initialize zappa
init-zappa:
    .venv/bin/pip install zappa
    .venv/bin/zappa init

# deploy to aws lambda
deploy-zappa: init-zappa
    .venv/bin/python manage.py collectstatic --noinput
    .venv/bin/zappa deploy || .venv/bin/zappa update
