from typing import List, Optional

from ninja import Router

from core.models import StockTicker

from .schemas import GreetOutput, StockTickerOut


router = Router()


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
