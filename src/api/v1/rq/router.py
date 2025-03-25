from ninja import Router
import rq
from django_redis import get_redis_connection
from utils import test_rq_job

router = Router()


@router.post("/submit-test-job", auth=None)
def test_rq(request):
    job = test_rq_job.delay()
    return {"message": "Job queued", "job_id": job.id}


@router.get("/job-status", auth=None)
def job_status(request, job_id: str):
    connection = get_redis_connection("default", write=False)
    job = rq.job.Job.fetch(job_id, connection=connection)
    status = job.get_status()
    return {"job_id": job.id, "status": status}
