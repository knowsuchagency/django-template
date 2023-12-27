# initialize development
init:
    brew install copier
    pkgx python@3.12 -m venv .venv
    .venv/bin/pip install -U pip
    .venv/bin/pip install -r template/requirements.txt

# generate test project
test:
    rm -rf example
    .venv/bin/copier copy -d project_name=example ./template ./example
