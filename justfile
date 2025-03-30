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
    import time
    import asyncio
    from django.conf import settings
    from textual.app import App, ComposeResult
    from textual.containers import Container
    from textual.widgets import Header, Footer, DataTable, Static
    from textual import work

    # Load Django settings to get the Redis URL
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    class CeleryQueuesDashboard(App):
        """A Textual app to monitor Celery queues."""
        
        CSS = """
        #dashboard {
            height: 100%;
            padding: 1;
        }
        
        #status {
            margin: 1 0;
            padding: 1;
            background: $surface;
            color: $text;
            border: tall $primary;
        }
        """
        
        BINDINGS = [
            ("q", "quit", "Quit"),
            ("r", "refresh_now", "Refresh Now"),
        ]
        
        def __init__(self):
            super().__init__()
            # Connect to Redis
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.table = DataTable()
            self.status = Static(id="status")

        def compose(self) -> ComposeResult:
            yield Header()
            with Container(id="dashboard"):
                yield self.status
                yield self.table
            yield Footer()
        
        def on_mount(self) -> None:
            # Set up the table
            self.table.add_columns("Queue Name", "Type", "Tasks")
            # Start the background task for updates
            self.refresh_data()
            self.update_timer()

        def action_refresh_now(self) -> None:
            """Manually refresh the data."""
            self.refresh_data()
        
        @work(exclusive=True)
        async def update_timer(self) -> None:
            """Update the dashboard every second."""
            while True:
                await asyncio.sleep(1)
                self.refresh_data()
        
        def refresh_data(self) -> None:
            """Refresh the queue data."""
            # Clear previous data
            self.table.clear()
            
            # Get all keys
            all_keys = self.redis_client.keys('*')
            
            # Filter for actual queue keys (not task metadata)
            queue_keys = []
            for key in all_keys:
                key_name = key.decode('utf-8')
                key_type = self.redis_client.type(key).decode('utf-8')
                
                # Filter out task metadata and only look for actual queues (lists)
                if (key_type == 'list' and 
                    not key_name.startswith('celery-task-meta-') and
                    not key_name.startswith('_')):
                    queue_length = self.redis_client.llen(key_name) if key_type == 'list' else 'N/A'
                    queue_keys.append((key_name, key_type, queue_length))
            
            # Update status message
            if not queue_keys:
                self.status.update("No active Celery queues found.")
                
                # Check specifically for the default celery queue
                if self.redis_client.type(b'celery') == b'list':
                    self.status.update("Default 'celery' queue exists but is empty.")
                
                # Check for task metadata as a hint
                task_meta_keys = [k.decode('utf-8') for k in all_keys if b'celery-task-meta-' in k]
                if task_meta_keys:
                    meta_count = len(task_meta_keys)
                    self.status.update(f"No active queues, but found {meta_count} task metadata entries.")
            else:
                # Sort queues by name for consistent output
                queue_keys.sort()
                self.status.update(f"Found {len(queue_keys)} active Celery queues. Last updated: {time.strftime('%H:%M:%S')}")
                
                # Add data to table
                for queue_name, queue_type, queue_length in queue_keys:
                    self.table.add_row(queue_name, queue_type, str(queue_length))

    if __name__ == "__main__":
        app = CeleryQueuesDashboard()
        app.run()
    

    
