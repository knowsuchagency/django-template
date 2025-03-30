import random
import time
from pprint import pprint

from django_q.tasks import async_task
from django_q.models import Task
from django.contrib.admin.views.decorators import staff_member_required
from ninja import Router
from django_q.brokers import get_broker

from .schemas import JobResult, QueueStatusResponse, QueueInfo


router = Router()


def test_q_job():
    seconds = random.randint(1, 5)
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    result = {"message": "Job completed", "seconds": seconds}
    pprint(result)
    return result


@router.post("/test", summary="Submit Test Job(s)")
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


@router.get("/queues", response=QueueStatusResponse, summary="Get Queue Status")
@staff_member_required
def queue_status(request):
    """
    Get a snapshot of all queues and their backpressure.
    """
    from django_q.status import Stat
    from datetime import datetime

    broker = get_broker()

    stats = Stat.get_all(broker)
    active_queues = []
    task_queue = 0
    result_count = 0
    reincarnations = 0

    for stat in stats:
        # Calculate tasks in this queue
        queue_tasks = stat.task_q_size + stat.done_q_size
        task_queue += queue_tasks
        result_count += stat.done_q_size
        reincarnations += stat.reincarnations
        # Create queue info
        queue_info = QueueInfo(
            name=f"q-{stat.cluster_id}",
            cluster_id=str(stat.cluster_id),
            tasks=queue_tasks,
            workers=len(stat.workers) if stat.workers else 0,
            status=str(stat.status),
            uptime=stat.uptime() if hasattr(stat, "uptime") else None,
        )
        active_queues.append(queue_info)

    # Create response
    response = QueueStatusResponse(
        queue_size=broker.queue_size(),
        queue_count=len(active_queues),
        task_queue=task_queue,
        result_count=result_count,
        reincarnations=reincarnations,
        timestamp=datetime.now().strftime("%H:%M:%S"),
        active_queues=active_queues,
    )

    return response
