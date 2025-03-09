from datetime import date, timedelta
from typing import List, Optional
from ninja import NinjaAPI, Router
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from backend.core.models import StockTicker
from backend.schemas import StockTickerOut

api = NinjaAPI()

v1 = Router()

api.add_router("/v1", v1)


@v1.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


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


@v1.post("/set-csrf-token")
@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})


@v1.get("/sentry-debug")
def sentry_debug(request):
    raise Exception("This is a test exception for Sentry")
