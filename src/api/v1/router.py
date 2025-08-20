from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from ninja import Router
from ninja.responses import Response

from .example.router import router as example_router
from .tasks.router import router as tasks_router
from .auth import router as auth_router

router = Router()
router.add_router("/example", example_router, tags=["example"])
router.add_router("/tasks", tasks_router, tags=["tasks"])
router.add_router("/auth", auth_router, tags=["auth"])


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
