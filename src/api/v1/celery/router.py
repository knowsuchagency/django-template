import random
import time
import redis
from pprint import pprint

from celery import shared_task
from celery.result import AsyncResult
from django.conf import settings
from ninja import Router

from .schemas import JobResult, QueueInfo, QueueStatusResponse


router = Router()


@shared_task(bind=True)
def test_celery_job(self):
    seconds = random.randint(1, 5)
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)
    return result


@router.post("/test", auth=None, summary="Submit Test Job(s)")
def test_celery(request, count: int = 1):
    tasks = [test_celery_job.delay() for _ in range(count)]
    task_ids = [task.id for task in tasks]
    return {"message": "Jobs queued", "job_ids": task_ids if count > 1 else task_ids[0]}


@router.get("/result", response=JobResult, summary="Get Job Result")
def result(request, job_id: str):
    task_result = AsyncResult(job_id)
    result_data = task_result.result
    if isinstance(result_data, Exception):
        result_data = str(result_data)

    # Map Celery result fields to JobResult schema
    # Note: Celery's AsyncResult doesn't directly provide 'started' or 'stopped' times easily.
    # We'll return None for those or you might need to store this info separately if required.
    return JobResult(
        job_id=task_result.id,
        status=task_result.status,
        result=result_data,
    )


@router.get("/queues", response=QueueStatusResponse, summary="Get Queue Status")
def queue_status(request):
    """
    Get a snapshot of all Celery queues and their current backlog.
    Shows queue names, types, and number of pending tasks.
    """
    # Connect to Redis
    redis_client = redis.from_url(settings.REDIS_URL)

    # Get all keys
    all_keys = redis_client.keys("*")

    # Filter for actual queue keys (not task metadata)
    active_queues = []
    total_tasks = 0

    for key in all_keys:
        key_name = key.decode("utf-8")
        key_type = redis_client.type(key).decode("utf-8")

        # Filter out task metadata and only look for actual queues (lists)
        if (
            key_type == "list"
            and not key_name.startswith("celery-task-meta-")
            and not key_name.startswith("_")
        ):
            queue_length = redis_client.llen(key_name) if key_type == "list" else 0
            total_tasks += queue_length
            active_queues.append(
                QueueInfo(name=key_name, type=key_type, tasks=queue_length)
            )

    # Count task metadata entries
    task_meta_keys = [
        k for k in all_keys if k.decode("utf-8").startswith("celery-task-meta-")
    ]
    task_meta_count = len(task_meta_keys)

    # Sort queues by name for consistent output
    active_queues.sort(key=lambda q: q.name)

    return QueueStatusResponse(
        active_queues=active_queues,
        queue_count=len(active_queues),
        task_count=total_tasks,
        task_metadata_count=task_meta_count,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
