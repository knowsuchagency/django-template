import random
import time
from datetime import datetime
from pprint import pprint

from dbos import DBOS
from ninja import Router
from loguru import logger

from .schemas import WorkflowResult, WorkflowStatusResponse, WorkflowInfo, WorkflowListResponse
from core.cron_jobs import data_aggregation_task


router = Router()


@DBOS.workflow()
def test_job_workflow():
    seconds = random.randint(1, 5)
    logger.info(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)
    return result


@router.post("/test", summary="Submit Test Job(s)")
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


@router.get("/result", response=WorkflowResult, summary="Get Workflow Result")
def get_result(request, workflow_id: str):
    try:
        handle = DBOS.retrieve_workflow(workflow_id)
        status = handle.get_status()
        
        # Only get result if workflow is complete
        result = None
        is_complete = status and status.status in ["SUCCESS", "ERROR", "CANCELLED", "MAX_RECOVERY_ATTEMPTS_EXCEEDED"]
        if is_complete:
            try:
                result = handle.get_result()
            except Exception as e:
                result = f"Error getting result: {str(e)}"
        
        return WorkflowResult(
            workflow_id=workflow_id,
            status=status.status if status else "UNKNOWN",  # Use status.status to get the actual status string
            result=result,
            started=datetime.fromtimestamp(status.created_at / 1000) if status and status.created_at else None,
            completed=datetime.fromtimestamp(status.updated_at / 1000) if is_complete and status and status.updated_at else None,
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
def list_workflows(request, limit: int = 50):
    """
    List recent workflows with their status.
    """
    try:
        # Use the DBOS instance initialized in apps.py
        # List recent workflows directly using DBOS
        workflow_list = DBOS.list_workflows(limit=limit)
        
        workflows = []
        for wf in workflow_list:
            workflows.append(WorkflowInfo(
                workflow_id=wf.workflow_id,
                name=wf.name,  # WorkflowStatus has 'name' attribute for the function name
                status=wf.status,  # Status is already a string, not an enum
                created_at=datetime.fromtimestamp(wf.created_at / 1000) if wf.created_at else None,  # Convert from ms timestamp
                updated_at=datetime.fromtimestamp(wf.updated_at / 1000) if wf.updated_at else None,  # Convert from ms timestamp
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
def workflow_status(request):
    """
    Get an overview of workflow status including queued workflows.
    """
    try:
        # Use the DBOS instance initialized in apps.py
        # Get counts directly using DBOS
        all_workflows = DBOS.list_workflows(limit=1000)
        queued = DBOS.list_queued_workflows()
        
        # Count workflows by status
        status_counts = {
            "PENDING": 0,
            "SUCCESS": 0,
            "ERROR": 0,
            "MAX_RECOVERY_ATTEMPTS_EXCEEDED": 0,
            "CANCELLED": 0,
            "ENQUEUED": 0,
        }
        
        for wf in all_workflows:
            if wf.status in status_counts:
                status_counts[wf.status] += 1
        
        # Enqueued workflows are those in the queue
        status_counts["ENQUEUED"] = len(queued)
        
        return WorkflowStatusResponse(
            total_workflows=len(all_workflows),
            queued_workflows=len(queued),
            pending=status_counts["PENDING"],
            success=status_counts["SUCCESS"],
            error=status_counts["ERROR"],
            max_recovery_attempts_exceeded=status_counts["MAX_RECOVERY_ATTEMPTS_EXCEEDED"],
            cancelled=status_counts["CANCELLED"],
            enqueued=status_counts["ENQUEUED"],
            timestamp=datetime.now().strftime("%H:%M:%S"),
            message="DBOS workflows are running"
        )
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        return WorkflowStatusResponse(
            total_workflows=0,
            queued_workflows=0,
            pending=0,
            success=0,
            error=0,
            max_recovery_attempts_exceeded=0,
            cancelled=0,
            enqueued=0,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            message=f"Error: {str(e)}"
        )


@router.post("/aggregate", summary="Trigger Data Aggregation")
def trigger_aggregation(request, time_range: str = "1h"):
    """
    Manually trigger a data aggregation workflow.
    
    Args:
        time_range: Time range for aggregation (e.g., "1h", "5m", "1d")
    """
    try:
        workflow_handle = DBOS.start_workflow(data_aggregation_task, time_range)
        workflow_id = workflow_handle.get_workflow_id()
        
        return {
            "message": "Data aggregation started",
            "workflow_id": workflow_id,
            "time_range": time_range
        }
    except Exception as e:
        logger.error(f"Error starting aggregation workflow: {e}")
        return {
            "message": "Error starting aggregation",
            "error": str(e)
        }
