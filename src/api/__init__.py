from datetime import date, timedelta
from typing import List, Optional

from django.conf import settings
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from ninja import NinjaAPI, Router
from ninja.responses import Response
from ninja.security import django_auth
from django_rq import job

from core.models import StockTicker
from utils import test_rq_job

from .schemas import AddOutput, GreetOutput, StockTickerOut


def simple_auth(request):
    """
    This is exists so we can use our app within Lovable's preview environment.

    Make sure to add the request's actual unique origin i.e. `https://id-preview--d9666ffa-29be-443f-9013-25d5cd5c1beb.lovable.app` to `CSRF_TRUSTED_ORIGINS`.
    """
    return request.user and request.user.is_authenticated


api = NinjaAPI(
    auth=simple_auth if settings.DEBUG else django_auth,
)

v1 = Router()

api.add_router("/v1", v1)


@v1.get("/csrf-token", auth=None)
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint to set CSRF cookie and return the token
    """
    token = get_token(request)
    return Response({"token": token})


@v1.post("/add", auth=None, response=AddOutput)
def add(request, a: int, b: int):
    return {"result": a + b}


@v1.post("/greet", response=GreetOutput)
def greet(request, name: str = "world"):
    return {"message": f"Hello, {name}!"}


@v1.get("/stocks", response=List[StockTickerOut])
def get_stocks(request, symbol: Optional[str] = None):
    """
    Get stock ticker data.
    If symbol is provided, returns data for that specific stock.
    """
    queryset = StockTicker.objects

    if symbol:
        queryset = queryset.filter(symbol=symbol.upper())

    return queryset


@v1.get("/sentry-debug")
def sentry_debug(request):
    raise Exception("This is a test exception for Sentry")




@v1.get("/test-rq", auth=None)
def test_rq(request):

    test_rq_job.delay()

    return Response({"message": "Job queued"})
