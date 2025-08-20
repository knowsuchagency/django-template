from datetime import date

from ninja import Schema


class StockTickerOut(Schema):
    symbol: str
    company_name: str
    price: float
    change: float
    percent_change: float
    volume: int
    date: date


class GreetOutput(Schema):
    message: str
