from enum import Enum
from typing import Any, Optional, List
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


class QueueInfo(Schema):
    name: str
    type: str
    tasks: int


class QueueStatusResponse(Schema):
    active_queues: List[QueueInfo]
    queue_count: int
    task_count: int
    task_metadata_count: Optional[int] = None
    timestamp: str
