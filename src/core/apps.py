from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import os
        from dbos import DBOS, DBOSConfig
        from django.conf import settings
        from loguru import logger
        from decouple import config

        # Only initialize DBOS if we're in the main process (not in Django's autoreload subprocess)
        if not settings.DEBUG or os.environ.get('RUN_MAIN') == 'true':
            # Use DBOS_DATABASE_URL if set, otherwise fall back to DATABASE_URL
            database_url = config("DBOS_DATABASE_URL", default=config("DATABASE_URL", default=""))
            
            # DBOS requires PostgreSQL, skip initialization if using SQLite
            if database_url and not database_url.startswith("sqlite"):
                try:
                    dbos_config: DBOSConfig = {
                        "name": "django-template",
                        "database_url": database_url,
                    }
                    DBOS(config=dbos_config)
                    DBOS.launch()
                    logger.info("DBOS initialized successfully")
                except Exception as e:
                    logger.warning(f"DBOS initialization failed: {e}")
                    logger.info("DBOS requires PostgreSQL. Workflows will not be available.")
            elif database_url.startswith("sqlite"):
                logger.info("DBOS requires PostgreSQL. Using SQLite, workflows disabled.")
            else:
                logger.warning("DBOS_DATABASE_URL not configured, DBOS not initialized")
