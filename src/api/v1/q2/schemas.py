from enum import Enum
from typing import Any, Optional
from datetime import datetime

from ninja import Schema


class JobStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class JobResult(Schema):
    job_id: str
    started: Optional[datetime]
    stopped: Optional[datetime]
    success: Optional[bool]
    result: Optional[Any] = None
