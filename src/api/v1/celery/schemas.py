from enum import Enum
from typing import Any, Optional
from datetime import datetime

from ninja import Schema


class Status(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"


class JobResult(Schema):
    job_id: str
    status: Status
    result: Optional[Any] = None
