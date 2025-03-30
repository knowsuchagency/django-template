from enum import Enum
from typing import Any, Optional, List, Union
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


class QueueInfo(Schema):
    name: str
    type: str = "django_q"
    tasks: int
    cluster_id: str
    workers: Optional[int] = None
    status: Optional[str] = None
    uptime: Optional[float] = None


class QueueStatusResponse(Schema):
    queue_size: int
    queue_count: int
    task_count: int
    timestamp: str
    result_count: int
    reincarnations: int
    active_queues: List[QueueInfo]
