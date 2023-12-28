# initialize development
init:
    brew install copier
    pkgx python@3.12 -m venv .venv
    .venv/bin/pip install -U pip
    .venv/bin/pip install -r template/{{{{project_name}}/requirements.txt

# generate test project
test:
    #!/bin/zsh
    rm -rf example
    copier copy -d project_name=example ./template ./
    cd example
    just init runserver
