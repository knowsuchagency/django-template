from dbos import DBOS
from loguru import logger


@DBOS.workflow()
def hello_world():
    logger.info("Hello, world!")
    print("Hello, world!")
    return "Hello, world!"


@DBOS.scheduled("*/1 * * * *")
@DBOS.workflow()
def scheduled_hello_world():
    """Run hello_world every minute"""
    return hello_world()