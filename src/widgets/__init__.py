"""Widget modules for FinTerm."""
from .base import BaseWidget
from .chart import ChartWidget
from .market_movers import MarketMoversWidget
from .news import NewsWidget
from .ticker_info import TickerInfoWidget
from .sentiment import SentimentWidget
from .market_ticker import MarketTickerWidget

__all__ = [
    "BaseWidget",
    "ChartWidget",
    "MarketMoversWidget",
    "NewsWidget",
    "TickerInfoWidget",
    "SentimentWidget",
    "MarketTickerWidget",
]
