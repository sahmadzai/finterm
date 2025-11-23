"""
Market ticker header widget showing major indices.
"""
from textual.widgets import Static
from rich.console import RenderableType
from rich.text import Text
from typing import List, Dict
from ..data.stocks import StockDataFetcher
from .base import BaseWidget


class MarketTickerWidget(BaseWidget):
    """
    Horizontal ticker widget displaying major market indices.
    Shows indices like S&P 500, NASDAQ, DOW, etc. with prices and changes.
    """

    DEFAULT_CSS = """
    MarketTickerWidget {
        height: 3;
        border: solid $primary;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(title="Market Overview", **kwargs)
        self.stock_fetcher = StockDataFetcher()
        # Major market indices
        self.indices = [
            ("^GSPC", "S&P 500"),
            ("^DJI", "DOW"),
            ("^IXIC", "NASDAQ"),
            ("^RUT", "RUSSELL 2000"),
            ("CL=F", "CRUDE OIL"),
            ("GC=F", "GOLD"),
            ("^TNX", "10Y BOND"),
        ]
        self.quotes_data = {}

    async def fetch_data(self):
        """Fetch quotes for all major indices."""
        self.quotes_data = {}
        for ticker, name in self.indices:
            quote = self.stock_fetcher.get_quote(ticker)
            if quote:
                self.quotes_data[name] = {
                    'price': quote['price'],
                    'change': quote['change'],
                    'change_percent': quote['change_percent']
                }

    def render(self) -> RenderableType:
        """Render the market ticker."""
        if self.is_loading and not self.quotes_data:
            return Text("Loading market data...", style="yellow")

        if self.has_error:
            return Text(f"Error: {self.error_message}", style="red")

        return self.render_content()

    def render_content(self) -> RenderableType:
        """Render the ticker content."""
        if not self.quotes_data:
            return Text("No market data available", style="yellow")

        ticker_text = Text()
        ticker_text.append("  ", style="dim")  # Padding

        for i, (name, data) in enumerate(self.quotes_data.items()):
            price = data['price']
            change = data['change']
            change_pct = data['change_percent']

            # Determine color based on change
            if change >= 0:
                color = "green"
                arrow = "↑"
            else:
                color = "red"
                arrow = "↓"

            # Add index name
            ticker_text.append(f"{name}: ", style="bold cyan")

            # Add price
            ticker_text.append(f"${price:,.2f} ", style="white")

            # Add change with color
            ticker_text.append(
                f"{arrow} {change:+.2f} ({change_pct:+.2f}%)",
                style=f"bold {color}"
            )

            # Add separator (except for last item)
            if i < len(self.quotes_data) - 1:
                ticker_text.append("  │  ", style="dim blue")

        return ticker_text
