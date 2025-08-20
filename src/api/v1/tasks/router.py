import random
import time
from typing import Optional, Any, List
from datetime import datetime
from pprint import pprint

from dbos import DBOS, DBOSClient
from django.contrib.admin.views.decorators import staff_member_required
from ninja import Router
from loguru import logger
from decouple import config as env_config

from .schemas import WorkflowResult, WorkflowStatusResponse, WorkflowInfo, WorkflowListResponse


router = Router()


@DBOS.workflow()
def test_job_workflow():
    seconds = random.randint(1, 5)
    logger.info(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)
    return result


@router.post("/test", summary="Submit Test Job(s)", auth=None)
def test_job(request, count: int = 1):
    try:
        workflow_ids = []
        for _ in range(count):
            workflow_handle = DBOS.start_workflow(test_job_workflow)
            workflow_ids.append(workflow_handle.get_workflow_id())
        
        return {
            "message": "Jobs queued", 
            "workflow_ids": workflow_ids if count > 1 else workflow_ids[0]
        }
    except Exception as e:
        if "DBOS Error" in str(e):
            return {
                "message": "DBOS not initialized. Please configure PostgreSQL database.", 
                "error": str(e)
            }
        raise


@router.get("/result", response=WorkflowResult, summary="Get Workflow Result", auth=None)
def get_result(request, workflow_id: str):
    try:
        handle = DBOS.retrieve_workflow(workflow_id)
        status = handle.get_status()
        
        # Only get result if workflow is complete
        result = None
        is_complete = status and status.name in ["SUCCESS", "ERROR", "RETRIES_EXCEEDED"]
        if is_complete:
            try:
                result = handle.get_result()
            except Exception as e:
                result = f"Error getting result: {str(e)}"
        
        return WorkflowResult(
            workflow_id=workflow_id,
            status=status.name if status else "UNKNOWN",
            result=result,
            started=datetime.now(),  # DBOS doesn't expose start time directly
            completed=datetime.now() if is_complete else None,
        )
    except Exception as e:
        logger.error(f"Error retrieving workflow {workflow_id}: {e}")
        return WorkflowResult(
            workflow_id=workflow_id,
            status="ERROR",
            result=str(e),
            started=None,
            completed=None,
        )


@router.get("/list", response=WorkflowListResponse, summary="List Workflows")
@staff_member_required
def list_workflows(request, limit: int = 50):
    """
    List recent workflows with their status.
    """
    try:
        # Get database URL from environment
        database_url = env_config("DBOS_DATABASE_URL", default=env_config("DATABASE_URL", default=""))
        
        if not database_url:
            return WorkflowListResponse(
                workflows=[],
                total_count=0,
                message="DBOS database not configured"
            )
        
        # Create a DBOS client to query workflows
        client = DBOSClient(database_url)
        
        # List recent workflows
        workflow_list = client.list_workflows(limit=limit)
        
        workflows = []
        for wf in workflow_list:
            workflows.append(WorkflowInfo(
                workflow_id=wf.workflow_id,
                name=wf.workflow_name,
                status=wf.status.name if wf.status else "UNKNOWN",
                created_at=wf.created_at if hasattr(wf, 'created_at') else None,
                updated_at=wf.updated_at if hasattr(wf, 'updated_at') else None,
            ))
        
        return WorkflowListResponse(
            workflows=workflows,
            total_count=len(workflows),
            message="Successfully retrieved workflows"
        )
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        return WorkflowListResponse(
            workflows=[],
            total_count=0,
            message=f"Error: {str(e)}"
        )


@router.get("/status", response=WorkflowStatusResponse, summary="Get Workflow Status Overview")
@staff_member_required
def workflow_status(request):
    """
    Get an overview of workflow status including queued workflows.
    """
    try:
        # Get database URL from environment
        database_url = env_config("DBOS_DATABASE_URL", default=env_config("DATABASE_URL", default=""))
        
        if not database_url:
            return WorkflowStatusResponse(
                total_workflows=0,
                queued_workflows=0,
                timestamp=datetime.now().strftime("%H:%M:%S"),
                message="DBOS database not configured"
            )
        
        # Create a DBOS client to query workflows
        client = DBOSClient(database_url)
        
        # Get counts
        all_workflows = client.list_workflows(limit=1000)
        queued = client.list_queued_workflows()
        
        return WorkflowStatusResponse(
            total_workflows=len(all_workflows),
            queued_workflows=len(queued),
            timestamp=datetime.now().strftime("%H:%M:%S"),
            message="DBOS workflows are running"
        )
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        return WorkflowStatusResponse(
            total_workflows=0,
            queued_workflows=0,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            message=f"Error: {str(e)}"
        )