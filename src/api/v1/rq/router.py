import random
import time
from pprint import pprint

import rq
from django_redis import get_redis_connection
from django_rq import job
from ninja import Router


router = Router()


@job
def test_rq_job():
    seconds = random.randint(1, 5)
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)
    return result

@router.post("/test", auth=None, summary="Submit Test Job")
def test_rq(request):
    job = test_rq_job.delay()
    return {"message": "Job queued", "job_id": job.id}


@router.get("/result", auth=None, summary="Get Job Result")
def result(request, job_id: str):
    connection = get_redis_connection()
    job = rq.job.Job.fetch(job_id, connection=connection)
    status = job.get_status()
    result = job.result
    if isinstance(result, Exception):
        result = str(result)
    return {"job_id": job.id, "status": status, "result": result}
