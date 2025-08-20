from typing import Any, Optional, List
from datetime import datetime

from ninja import Schema


class WorkflowResult(Schema):
    workflow_id: str
    status: str
    result: Optional[Any] = None
    started: Optional[datetime] = None
    completed: Optional[datetime] = None


class WorkflowInfo(Schema):
    workflow_id: str
    name: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WorkflowListResponse(Schema):
    workflows: List[WorkflowInfo]
    total_count: int
    message: str


class WorkflowStatusResponse(Schema):
    total_workflows: int
    queued_workflows: int = 0
    pending: int = 0
    success: int = 0
    error: int = 0
    max_recovery_attempts_exceeded: int = 0
    cancelled: int = 0
    enqueued: int = 0
    timestamp: str
    message: str