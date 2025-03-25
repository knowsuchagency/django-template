import random
import time
from datetime import datetime, timedelta
from pprint import pprint

import rq
from django_redis import get_redis_connection
from django_rq import job, get_queue
from ninja import Router

from .schemas import JobResult


router = Router()


@job
def test_rq_job():
    seconds = random.randint(1, 5)
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)

    # Schedule the next run in 5 seconds
    queue = get_queue("default")
    next_run = datetime.now() + timedelta(seconds=5)
    queue.enqueue_at(next_run, test_rq_job)

    return result


@router.post("/test", auth=None, summary="Submit Test Job")
def test_rq(request):
    job = test_rq_job.delay()
    return {"message": "Job queued", "job_id": job.id}


@router.get("/result", response=JobResult, summary="Get Job Result")
def result(request, job_id: str):
    connection = get_redis_connection()
    job = rq.job.Job.fetch(job_id, connection=connection)
    status = job.get_status()
    result = job.result
    if isinstance(result, Exception):
        result = str(result)
    return JobResult(job_id=job.id, status=status, result=result)
