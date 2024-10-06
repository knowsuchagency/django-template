from ninja import NinjaAPI, Router
from django.middleware.csrf import get_token
from django.http import HttpResponse

api = NinjaAPI()

v1 = Router()

api.add_router("/v1", v1)

@v1.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@v1.post("/set-csrf-token")
def set_csrf_token(request):
    response = HttpResponse("CSRF token set")
    response.set_cookie("csrftoken", get_token(request))
    return response
