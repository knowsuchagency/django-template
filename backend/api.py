from ninja import NinjaAPI, Router
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

api = NinjaAPI()

v1 = Router()

api.add_router("/v1", v1)


@v1.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@v1.post("/set-csrf-token")
@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})


@v1.get("/sentry-debug")
def sentry_debug(request):
    raise Exception("This is a test exception for Sentry")
