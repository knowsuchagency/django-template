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

# run celery worker
worker:
    uv run celery -A src.celery_config worker --autoscale=10,2 --loglevel=info

# run celery beat
beat:
    uv run celery -A src.celery_config beat --loglevel=info

# celery worker and beat
celery:
    npx concurrently --names "WORKER,BEAT" --prefix-colors "blue,green" "just worker" "just beat"

# celery flower
flower:
    uv run celery -A src.celery_config flower

# view celery queues
queues:
    #!/usr/bin/env uv run python
    import os
    import redis
    from django.conf import settings
    
    # Load Django settings to get the Redis URL
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    
    # Connect to Redis
    redis_client = redis.from_url(settings.REDIS_URL)
    
    print("\n=== Celery Queue Statistics ===\n")
    
    # Get all keys
    all_keys = redis_client.keys('*')
    
    # Filter for actual queue keys (not task metadata)
    queue_keys = []
    for key in all_keys:
        key_name = key.decode('utf-8')
        key_type = redis_client.type(key).decode('utf-8')
        
        # Filter out task metadata and only look for actual queues (lists)
        if (key_type == 'list' and 
            not key_name.startswith('celery-task-meta-') and
            not key_name.startswith('_')):
            queue_keys.append((key_name, key_type))
    
    # Display queue information
    if not queue_keys:
        print("No active Celery queues found.")
        
        # Check specifically for the default celery queue
        if redis_client.type(b'celery') == b'list':
            print("Default 'celery' queue exists but is empty.")
            
        # Give advice about common queue names
        print("\nCommon Celery queue names to check:")
        print("- celery (default queue)")
        print("- celery.priority")
        print("- celery.scheduled")
    else:
        # Sort queues by name for consistent output
        queue_keys.sort()
        for queue_name, queue_type in queue_keys:
            queue_length = redis_client.llen(queue_name) if queue_type == 'list' else 'N/A'
            print(f"Queue: {queue_name:<20} Tasks: {queue_length}")
    
    # Only show a few task metadata keys as an example if we couldn't find any queues
    if not queue_keys:
        task_meta_keys = [k.decode('utf-8') for k in all_keys if b'celery-task-meta-' in k]
        if task_meta_keys:
            print("\nFound task metadata keys (examples):")
            for k in task_meta_keys[:3]:  # Show only 3 examples
                print(f"- {k}")
            if len(task_meta_keys) > 3:
                print(f"- ... and {len(task_meta_keys) - 3} more")
    

    
