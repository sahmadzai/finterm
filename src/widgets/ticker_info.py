"""
Ticker information widget displaying detailed stock information.
"""
from textual.widgets import Static
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from typing import Optional, Dict
from ..data.stocks import StockDataFetcher
from .base import BaseWidget


class TickerInfoWidget(BaseWidget):
    """
    Widget displaying detailed information about a specific ticker.
    """

    DEFAULT_CSS = """
    TickerInfoWidget {
        border: solid $primary;
        height: 100%;
    }
    """

    def __init__(
        self,
        ticker: str = "SPY",
        **kwargs
    ):
        super().__init__(title=f"{ticker} Info", **kwargs)
        self.ticker = ticker
        self.stock_fetcher = StockDataFetcher()
        self.quote_data = None
        self.company_data = None
        self.financials_data = None

    async def fetch_data(self):
        """Fetch ticker information."""
        self.quote_data = self.stock_fetcher.get_quote(self.ticker)
        self.company_data = self.stock_fetcher.get_company_info(self.ticker)
        self.financials_data = self.stock_fetcher.get_financials(self.ticker)

    def render(self) -> RenderableType:
        """Render the ticker info widget."""
        if self.is_loading:
            return Panel(
                Text("Loading ticker info...", style="yellow"),
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
        """Render ticker information."""
        if not self.quote_data:
            return Text("No data available", style="yellow")

        # Create main info section
        info_text = Text()

        # Price section
        price = self.quote_data.get('price', 0)
        change = self.quote_data.get('change', 0)
        change_pct = self.quote_data.get('change_percent', 0)

        change_style = "green" if change >= 0 else "red"

        info_text.append(f"Price: ", style="bold white")
        info_text.append(f"${price:.2f}\n", style="bold cyan")

        info_text.append(f"Change: ", style="bold white")
        info_text.append(
            f"{change:+.2f} ({change_pct:+.2f}%)\n\n",
            style=f"bold {change_style}"
        )

        # Trading info
        info_text.append("═" * 40 + "\n", style="dim blue")
        info_text.append("TRADING INFO\n", style="bold cyan")
        info_text.append("═" * 40 + "\n\n", style="dim blue")

        info_text.append(f"Open:          ${self.quote_data.get('open', 0):.2f}\n", style="white")
        info_text.append(f"High:          ${self.quote_data.get('high', 0):.2f}\n", style="green")
        info_text.append(f"Low:           ${self.quote_data.get('low', 0):.2f}\n", style="red")
        info_text.append(f"Prev Close:    ${self.quote_data.get('previous_close', 0):.2f}\n", style="white")
        info_text.append(f"Volume:        {self._format_number(self.quote_data.get('volume', 0))}\n", style="yellow")
        info_text.append(f"Market Cap:    {self._format_number(self.quote_data.get('market_cap', 0))}\n", style="cyan")

        # Company info
        if self.company_data:
            info_text.append("\n")
            info_text.append("═" * 40 + "\n", style="dim blue")
            info_text.append("COMPANY INFO\n", style="bold cyan")
            info_text.append("═" * 40 + "\n\n", style="dim blue")

            info_text.append(f"Name:     {self.company_data.get('name', 'N/A')}\n", style="white")
            info_text.append(f"Sector:   {self.company_data.get('sector', 'N/A')}\n", style="yellow")
            info_text.append(f"Industry: {self.company_data.get('industry', 'N/A')}\n", style="yellow")

        # Financial metrics
        if self.financials_data:
            info_text.append("\n")
            info_text.append("═" * 40 + "\n", style="dim blue")
            info_text.append("KEY METRICS\n", style="bold cyan")
            info_text.append("═" * 40 + "\n\n", style="dim blue")

            pe = self.financials_data.get('pe_ratio', 0)
            info_text.append(f"P/E Ratio:      {pe:.2f}\n" if pe else "P/E Ratio:      N/A\n", style="white")

            pb = self.financials_data.get('pb_ratio', 0)
            info_text.append(f"P/B Ratio:      {pb:.2f}\n" if pb else "P/B Ratio:      N/A\n", style="white")

            eps = self.financials_data.get('eps', 0)
            info_text.append(f"EPS:            ${eps:.2f}\n" if eps else "EPS:            N/A\n", style="cyan")

            div_yield = self.financials_data.get('dividend_yield', 0)
            if div_yield:
                info_text.append(f"Dividend Yield: {div_yield * 100:.2f}%\n", style="green")

        return info_text

    def _format_number(self, num: float) -> str:
        """Format large numbers with K, M, B suffixes."""
        if num >= 1_000_000_000_000:
            return f"{num / 1_000_000_000_000:.2f}T"
        elif num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K"
        else:
            return f"{num:.0f}"

    def set_ticker(self, ticker: str):
        """Change the ticker being displayed."""
        self.ticker = ticker
        self.border_title = f"{ticker} Info"
        self.run_worker(self.refresh_data(), exclusive=True)
