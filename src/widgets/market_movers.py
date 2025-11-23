"""
Market movers widget displaying top gainers and losers.
"""
from textual.widgets import Static
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from typing import List, Tuple
from ..data.stocks import StockDataFetcher
from ..utils.config import config
from .base import BaseWidget


class MarketMoversWidget(BaseWidget):
    """
    Widget displaying top market movers (gainers and losers).
    """

    DEFAULT_CSS = """
    MarketMoversWidget {
        border: solid $primary;
        height: 100%;
    }
    """

    def __init__(
        self,
        tickers: List[str] = None,
        limit: int = 10,
        **kwargs
    ):
        super().__init__(title="Market Movers", **kwargs)
        self.tickers = tickers or config.default_tickers
        self.limit = limit
        self.stock_fetcher = StockDataFetcher()
        self.movers_data = []

    async def fetch_data(self):
        """Fetch market movers data."""
        self.movers_data = self.stock_fetcher.get_market_movers(self.tickers)

    def render(self) -> RenderableType:
        """Render the market movers widget."""
        if self.is_loading:
            return Panel(
                Text("Loading market movers...", style="yellow"),
                title=self.widget_title,
                border_style="blue"
            )

        if self.has_error:
            return Panel(
                Text(f"Error: {self.error_message}", style="red"),
                title=self.widget_title,
                border_style="red"
            )

        return Panel(
            self.render_content(),
            title=self.widget_title,
            border_style="green"
        )

    def render_content(self) -> RenderableType:
        """Render market movers table."""
        if not self.movers_data:
            return Text("No data available", style="yellow")

        table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
            expand=True
        )

        table.add_column("Symbol", style="cyan", width=8)
        table.add_column("Price", justify="right", width=12)
        table.add_column("Change %", justify="right", width=12)
        table.add_column("Trend", width=10)

        for ticker, price, change_pct in self.movers_data[:self.limit]:
            # Determine color based on change
            if change_pct > 0:
                change_style = "green"
                trend = "↑ UP"
                trend_style = "green"
            elif change_pct < 0:
                change_style = "red"
                trend = "↓ DOWN"
                trend_style = "red"
            else:
                change_style = "yellow"
                trend = "→ FLAT"
                trend_style = "yellow"

            table.add_row(
                ticker,
                f"${price:.2f}",
                Text(f"{change_pct:+.2f}%", style=change_style),
                Text(trend, style=trend_style)
            )

        return table
