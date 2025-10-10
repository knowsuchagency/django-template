from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import os
        import sys
        from dbos import DBOS, DBOSConfig
        from django.conf import settings
        from loguru import logger

        # Only initialize DBOS when running the server
        if 'runserver' not in sys.argv and 'granian' not in sys.argv[0] and 'gunicorn' not in sys.argv[0] and 'uvicorn' not in sys.argv[0]:
            logger.info("Skipping DBOS initialization - not running server")
            return

        # Only initialize DBOS if we're in the main process (not in Django's autoreload subprocess)
        if not settings.DEBUG or os.environ.get('RUN_MAIN') == 'true':
            # Get DATABASE_URL and transform it for DBOS by removing query params
            database_url = os.getenv("DATABASE_URL", "")
            
            # Remove query parameters from DATABASE_URL for DBOS if provided
            # DBOS doesn't work well with search_path and other params
            dbos_database_url = None
            if database_url:
                from urllib.parse import urlparse, urlunparse
                parsed = urlparse(database_url)
                # Rebuild URL without query params
                dbos_database_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    '',  # params
                    '',  # query
                    ''   # fragment
                ))
            
            try:
                dbos_config: DBOSConfig = {
                    "name": "django-template",
                }
                if dbos_database_url:
                    dbos_config["database_url"] = dbos_database_url
                    
                DBOS(config=dbos_config, conductor_key=settings.DBOS_CONDUCTOR_KEY)
                DBOS.launch()
                
                if dbos_database_url:
                    logger.info(f"DBOS initialized successfully with URL: {dbos_database_url}")
                else:
                    logger.info("DBOS initialized successfully without database URL")
                
                # Import cron jobs to register them with DBOS
                from . import cron_jobs  # noqa: F401
                logger.info("DBOS cron jobs registered")
            except Exception as e:
                logger.warning(f"DBOS initialization failed: {e}")
                logger.info("Workflows will not be available.")
