import random
import time
from pprint import pprint

from celery import shared_task
from celery.result import AsyncResult
from ninja import Router

from .schemas import JobResult


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
