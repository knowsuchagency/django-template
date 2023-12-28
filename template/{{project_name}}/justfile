# initialize development
init:
    pkgx python@3.12 -m venv .venv
    npm i -g concurrently
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python manage.py tailwind install

# run development server
runserver:
    DEBUG=true concurrently -n tailwind,django ".venv/bin/python manage.py tailwind start" "sleep 3 && .venv/bin/python manage.py runserver"
