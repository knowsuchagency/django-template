import random
import time
from pprint import pprint

from django_q.tasks import async_task
from django_q.models import Task
from ninja import Router

from .schemas import JobResult


router = Router()


def test_q_job():
    seconds = random.randint(1, 5)
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)
    return result


@router.post("/test", auth=None, summary="Submit Test Job(s)")
def test_q(request, count: int = 1):
    task_ids = [async_task(test_q_job) for _ in range(count)]
    return {"message": "Jobs queued", "job_ids": task_ids if count > 1 else task_ids[0]}


@router.get("/result", response=JobResult, summary="Get Job Result")
def result(request, job_id: str):
    task = Task.objects.get(id=job_id)
    result = task.result
    if isinstance(result, Exception):
        result = str(result)
    return JobResult(
        job_id=task.id,
        started=task.started,
        stopped=task.stopped,
        success=task.success,
        result=result,
    )
