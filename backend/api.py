from datetime import date, timedelta
from typing import List, Optional

from ninja import NinjaAPI, Router
from ninja.security import django_auth
from ninja.responses import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

from backend.core.models import StockTicker
from backend.schemas import StockTickerOut

api = NinjaAPI(
    # auth=django_auth,
    csrf=False
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


@v1.post("/add", auth=None)
def add(request, a: int, b: int):
    return {"result": a + b}


@v1.post("/greet")
def greet(request, name: str = "world"):
    return {"message": f"Hello, {name}!"}


@v1.get("/stocks", response=List[StockTickerOut])
def get_stocks(request, symbol: Optional[str] = None, days: int = 7):
    """
    Get stock ticker data.
    If symbol is provided, returns data for that specific stock.
    Days parameter controls how many days of historical data to return (default 7).
    """
    start_date = date.today() - timedelta(days=days - 1)

    queryset = StockTicker.objects.filter(date__gte=start_date)

    if symbol:
        queryset = queryset.filter(symbol=symbol.upper())

    return queryset


@v1.get("/sentry-debug")
def sentry_debug(request):
    raise Exception("This is a test exception for Sentry")
