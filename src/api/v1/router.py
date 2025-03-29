from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from ninja import Router
from ninja.responses import Response

from .example.router import router as example_router
from .celery.router import router as celery_router


router = Router()
router.add_router("/celery", celery_router, tags=["celery"])
router.add_router("/example", example_router, tags=["example"])

@router.get("/csrf-token", auth=None)
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint to set CSRF cookie and return the token
    """
    token = get_token(request)
    return Response({"token": token})

@router.get("/sentry-debug")
def sentry_debug(request):
    raise Exception("This is a test exception for Sentry")
