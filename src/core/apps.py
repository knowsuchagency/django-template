from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import os
        from dbos import DBOS, DBOSConfig
        from django.conf import settings
        from loguru import logger

        # Only initialize DBOS if we're in the main process (not in Django's autoreload subprocess)
        if not settings.DEBUG or os.environ.get('RUN_MAIN') == 'true':
            # Get DATABASE_URL and transform it for DBOS by removing query params
            database_url = os.getenv("DATABASE_URL", "")
            
            # DBOS requires PostgreSQL, skip initialization if using SQLite
            if database_url and not database_url.startswith("sqlite"):
                # Remove query parameters from DATABASE_URL for DBOS
                # DBOS doesn't work well with search_path and other params
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
                        "database_url": dbos_database_url,
                    }
                    DBOS(config=dbos_config, conductor_key=settings.DBOS_CONDUCTOR_KEY)
                    DBOS.launch()
                    logger.info(f"DBOS initialized successfully with URL: {dbos_database_url}")
                    
                    # Import cron jobs to register them with DBOS
                    from . import cron_jobs  # noqa: F401
                    logger.info("DBOS cron jobs registered")
                except Exception as e:
                    logger.warning(f"DBOS initialization failed: {e}")
                    logger.info("DBOS requires PostgreSQL. Workflows will not be available.")
            elif database_url.startswith("sqlite"):
                logger.info("DBOS requires PostgreSQL. Using SQLite, workflows disabled.")
            else:
                logger.warning("DBOS_DATABASE_URL not configured, DBOS not initialized")
