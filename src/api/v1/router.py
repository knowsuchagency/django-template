from typing import List, Optional

from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from ninja import Router
from ninja.responses import Response

from core.models import StockTicker

from .schemas import AddOutput, GreetOutput, StockTickerOut
from .rq.router import router as rq_router


router = Router()
router.add_router("/rq", rq_router)


@router.get("/csrf-token", auth=None)
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint to set CSRF cookie and return the token
    """
    token = get_token(request)
    return Response({"token": token})


@router.post("/add", auth=None, response=AddOutput)
def add(request, a: int, b: int):
    return {"result": a + b}


@router.post("/greet", response=GreetOutput)
def greet(request, name: str = "world"):
    return {"message": f"Hello, {name}!"}


@router.get("/stocks", response=List[StockTickerOut])
def get_stocks(request, symbol: Optional[str] = None):
    """
    Get stock ticker data.
    If symbol is provided, returns data for that specific stock.
    """
    queryset = StockTicker.objects

    if symbol:
        queryset = queryset.filter(symbol=symbol.upper())

    return queryset


@router.get("/sentry-debug")
def sentry_debug(request):
    raise Exception("This is a test exception for Sentry")
