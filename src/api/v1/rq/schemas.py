from enum import Enum
from typing import Any, Optional

from ninja import Schema


class JobStatus(str, Enum):
    QUEUED = "queued"
    FINISHED = "finished"
    FAILED = "failed"
    STARTED = "started"
    DEFERRED = "deferred"
    SCHEDULED = "scheduled"
    STOPPED = "stopped"
    CANCELED = "canceled"


class JobResult(Schema):
    job_id: str
    status: JobStatus
    result: Optional[Any] = None
