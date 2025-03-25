from django_rq import job

@job
def test_rq_job():
    print("Hello, world!")
