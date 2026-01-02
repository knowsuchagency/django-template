from typing import Any, Optional, List, Dict
from datetime import datetime

from ninja import Schema


class WorkflowResult(Schema):
    workflow_id: str
    status: str
    result: Optional[Any] = None
    started: Optional[datetime] = None
    completed: Optional[datetime] = None
    input: Optional[Any] = None  # Added for conductor detail view


class WorkflowInfo(Schema):
    workflow_id: str
    name: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    app_version: Optional[str] = None  # Added for conductor view


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


class WorkflowStepInfo(Schema):
    step_id: str
    step_name: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output: Optional[Any] = None
    error: Optional[str] = None


class WorkflowDetailResponse(Schema):
    workflow_id: str
    name: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    app_version: Optional[str] = None
    input: Optional[Any] = None
    output: Optional[Any] = None
    error: Optional[str] = None
    recovery_attempts: int = 0
    steps: List[WorkflowStepInfo] = []