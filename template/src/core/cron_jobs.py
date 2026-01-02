import random
from datetime import datetime
from typing import Dict, Any

from dbos import DBOS
from loguru import logger


@DBOS.scheduled("0 * * * * *")
@DBOS.workflow()
def stock_price_tracker(scheduled_time: datetime, actual_time: datetime):
    """
    Example cron job that simulates tracking stock prices.
    Runs every minute to demonstrate DBOS scheduled workflows.
    
    Args:
        scheduled_time: The scheduled execution time
        actual_time: The actual execution time
    """
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    prices = {}
    
    for symbol in stocks:
        base_price = {
            "AAPL": 190.0,
            "GOOGL": 165.0,
            "MSFT": 430.0,
            "AMZN": 185.0,
            "TSLA": 250.0
        }[symbol]
        
        variation = random.uniform(-5, 5)
        current_price = round(base_price + variation, 2)
        prices[symbol] = current_price
    
    timestamp = datetime.now().isoformat()
    result = {
        "timestamp": timestamp,
        "prices": prices,
        "market_status": "open" if datetime.now().hour >= 9 and datetime.now().hour < 16 else "closed"
    }
    
    logger.info(f"Stock prices updated at {timestamp}: {prices}")
    return result


@DBOS.scheduled("0 */1 * * *")
@DBOS.workflow()
def hourly_report(scheduled_time: datetime, actual_time: datetime):
    """
    Example hourly report generator.
    Runs at the start of every hour.
    
    Args:
        scheduled_time: The scheduled execution time
        actual_time: The actual execution time
    """
    report_time = datetime.now()
    
    report = {
        "report_type": "hourly",
        "generated_at": report_time.isoformat(),
        "hour": report_time.hour,
        "day": report_time.day,
        "metrics": {
            "active_users": random.randint(100, 500),
            "requests_processed": random.randint(1000, 5000),
            "average_response_time_ms": round(random.uniform(50, 200), 2),
            "error_rate": round(random.uniform(0, 0.05), 4)
        }
    }
    
    logger.info(f"Hourly report generated: {report}")
    return report


@DBOS.scheduled("0 0 * * *")
@DBOS.workflow()
def daily_cleanup(scheduled_time: datetime, actual_time: datetime):
    """
    Example daily cleanup task.
    Runs at midnight every day.
    
    Args:
        scheduled_time: The scheduled execution time
        actual_time: The actual execution time
    """
    cleanup_time = datetime.now()
    
    result = {
        "task": "daily_cleanup",
        "executed_at": cleanup_time.isoformat(),
        "items_cleaned": random.randint(10, 100),
        "space_freed_mb": random.randint(100, 1000),
        "status": "success"
    }
    
    logger.info(f"Daily cleanup completed: {result}")
    return result


@DBOS.workflow()
def data_aggregation_task(time_range: str = "1h") -> Dict[str, Any]:
    """
    Example task that can be called manually or scheduled.
    Aggregates data for a specified time range.
    """
    start_time = datetime.now()
    
    aggregation = {
        "time_range": time_range,
        "start_time": start_time.isoformat(),
        "data_points": random.randint(100, 1000),
        "aggregated_value": round(random.uniform(1000, 10000), 2),
        "processing_time_ms": random.randint(10, 100)
    }
    
    logger.info(f"Data aggregation completed for {time_range}: {aggregation}")
    return aggregation


@DBOS.scheduled("*/5 * * * *")
@DBOS.workflow()
def five_minute_aggregation(scheduled_time: datetime, actual_time: datetime):
    """
    Runs data aggregation every 5 minutes.
    
    Args:
        scheduled_time: The scheduled execution time
        actual_time: The actual execution time
    """
    return data_aggregation_task("5m")
