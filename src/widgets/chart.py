"""
Chart widget with candlestick and line chart support.
"""
from textual.widgets import Static
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
import logging
from typing import Optional, List, Tuple
from ..data.stocks import StockDataFetcher
from .base import BaseWidget

logger = logging.getLogger('finterm.chart')


class ChartWidget(BaseWidget):
    """
    Interactive chart widget for displaying stock price charts.
    Supports candlestick and line charts.
    """

    DEFAULT_CSS = """
    ChartWidget {
        border: solid $primary;
        height: 100%;
    }
    """

    def __init__(
        self,
        ticker: str = "SPY",
        period: str = "1mo",
        interval: str = "1d",
        chart_type: str = "candlestick",
        **kwargs
    ):
        super().__init__(title=f"{ticker} Chart", **kwargs)
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.chart_type = chart_type
        self.stock_fetcher = StockDataFetcher()
        self.chart_data = None

    async def fetch_data(self):
        """Fetch historical price data."""
        self.chart_data = self.stock_fetcher.get_historical_data(
            self.ticker,
            period=self.period,
            interval=self.interval
        )

    def render(self) -> RenderableType:
        """Render the chart."""
        if self.is_loading:
            return Panel(
                Text("Loading chart data...", style="yellow"),
                title=self.widget_title,
                border_style="blue"
            )

        if self.has_error:
            return Panel(
                Text(f"Error: {self.error_message}", style="red"),
                title=self.widget_title,
                border_style="red"
            )

        if self.chart_data is None or len(self.chart_data) == 0:
            return Panel(
                Text("No data available", style="yellow"),
                title=self.widget_title,
                border_style="yellow"
            )

        return Panel(
            self.render_content(),
            title=f"{self.widget_title} ({self.period}, {self.interval})",
            border_style="green"
        )

    def render_content(self) -> RenderableType:
        """Render chart content using custom ASCII renderer."""
        try:
            logger.debug(f"Rendering chart for {self.ticker}, type={self.chart_type}, period={self.period}")

            if self.chart_type == "candlestick":
                return self._render_candlestick_ascii()
            else:
                return self._render_line_chart_ascii()

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"ERROR rendering chart for {self.ticker}:")
            logger.error(error_details)
            logger.error(f"Chart data info: {type(self.chart_data)}, shape: {self.chart_data.shape if hasattr(self.chart_data, 'shape') else 'N/A'}")
            return Text(f"Error: {e}\nCheck ~/.finterm/logs/ for details", style="red")

    def _normalize_to_range(self, values: List[float], min_val: float, max_val: float, height: int) -> List[int]:
        """Normalize values to fit within a given height."""
        if max_val == min_val:
            return [height // 2] * len(values)

        return [
            int((height - 1) - ((val - min_val) / (max_val - min_val)) * (height - 1))
            for val in values
        ]

    def _render_candlestick_ascii(self) -> RenderableType:
        """Render candlestick chart using ASCII/Unicode characters."""
        df = self.chart_data

        # Get data arrays
        opens = df['Open'].tolist()
        closes = df['Close'].tolist()
        highs = df['High'].tolist()
        lows = df['Low'].tolist()

        # Limit to last N candles for readability
        max_candles = 40
        if len(opens) > max_candles:
            opens = opens[-max_candles:]
            closes = closes[-max_candles:]
            highs = highs[-max_candles:]
            lows = lows[-max_candles:]

        # Calculate price range
        all_prices = highs + lows
        max_price = max(all_prices)
        min_price = min(all_prices)
        price_range = max_price - min_price

        # Chart dimensions
        chart_height = 20
        chart_width = len(opens) * 2  # 2 chars per candle for spacing

        # Create grid
        grid = [[' ' for _ in range(chart_width)] for _ in range(chart_height)]

        # Normalize prices to chart height
        norm_opens = self._normalize_to_range(opens, min_price, max_price, chart_height)
        norm_closes = self._normalize_to_range(closes, min_price, max_price, chart_height)
        norm_highs = self._normalize_to_range(highs, min_price, max_price, chart_height)
        norm_lows = self._normalize_to_range(lows, min_price, max_price, chart_height)

        # Draw candlesticks
        for i in range(len(opens)):
            x = i * 2

            # Draw wick (high to low)
            for y in range(min(norm_highs[i], norm_lows[i]), max(norm_highs[i], norm_lows[i]) + 1):
                if 0 <= y < chart_height:
                    grid[y][x] = '│'

            # Draw body (open to close)
            body_top = min(norm_opens[i], norm_closes[i])
            body_bottom = max(norm_opens[i], norm_closes[i])

            # Determine if bullish (close > open) or bearish
            is_bullish = closes[i] >= opens[i]
            body_char = '█' if not is_bullish else '░'

            for y in range(body_top, body_bottom + 1):
                if 0 <= y < chart_height:
                    grid[y][x] = body_char

        # Build the chart text with colors
        chart_text = Text()

        # Add price scale and chart
        for row_idx, row in enumerate(grid):
            # Calculate price for this row
            price = max_price - (row_idx / (chart_height - 1)) * price_range

            # Add price label every few rows
            if row_idx % 4 == 0:
                chart_text.append(f"{price:7.2f} ", style="dim cyan")
            else:
                chart_text.append("        ", style="dim")

            # Add chart row with colors
            for char in row:
                if char == '█':
                    chart_text.append(char, style="red")
                elif char == '░':
                    chart_text.append(char, style="green")
                elif char == '│':
                    chart_text.append(char, style="white dim")
                else:
                    chart_text.append(char)
            chart_text.append("\n")

        # Add axis line
        chart_text.append("        " + "─" * chart_width + "\n", style="dim")

        # Add summary stats
        current_price = closes[-1]
        price_change = closes[-1] - closes[0]
        pct_change = (price_change / closes[0]) * 100

        summary = Text()
        summary.append(f"\nCurrent: ${current_price:.2f}  ", style="bold white")
        summary.append(f"Change: ", style="dim")
        change_style = "bold green" if price_change >= 0 else "bold red"
        summary.append(f"${price_change:+.2f} ({pct_change:+.2f}%)  ", style=change_style)
        summary.append(f"High: ${max_price:.2f}  Low: ${min_price:.2f}", style="dim")

        return Text.assemble(chart_text, summary)

    def _render_line_chart_ascii(self) -> RenderableType:
        """Render line chart using ASCII characters."""
        df = self.chart_data

        # Get closing prices
        closes = df['Close'].tolist()

        # Limit to last N points
        max_points = 60
        if len(closes) > max_points:
            closes = closes[-max_points:]

        # Calculate range
        max_price = max(closes)
        min_price = min(closes)
        price_range = max_price - min_price

        # Chart dimensions
        chart_height = 20
        chart_width = len(closes)

        # Normalize prices
        norm_closes = self._normalize_to_range(closes, min_price, max_price, chart_height)

        # Create grid
        grid = [[' ' for _ in range(chart_width)] for _ in range(chart_height)]

        # Draw line
        for i in range(len(norm_closes)):
            y = norm_closes[i]
            if 0 <= y < chart_height:
                grid[y][i] = '●'

            # Connect points
            if i > 0:
                y_prev = norm_closes[i - 1]
                y_curr = norm_closes[i]

                if y_prev != y_curr:
                    step = 1 if y_curr > y_prev else -1
                    for y in range(y_prev + step, y_curr, step):
                        if 0 <= y < chart_height:
                            grid[y][i] = '│'

        # Build the chart text
        chart_text = Text()

        for row_idx, row in enumerate(grid):
            price = max_price - (row_idx / (chart_height - 1)) * price_range

            if row_idx % 4 == 0:
                chart_text.append(f"{price:7.2f} ", style="dim cyan")
            else:
                chart_text.append("        ", style="dim")

            for char in row:
                if char == '●':
                    chart_text.append(char, style="cyan bold")
                elif char == '│':
                    chart_text.append(char, style="cyan")
                else:
                    chart_text.append(char)
            chart_text.append("\n")

        chart_text.append("        " + "─" * chart_width + "\n", style="dim")

        # Add summary
        current_price = closes[-1]
        price_change = closes[-1] - closes[0]
        pct_change = (price_change / closes[0]) * 100

        summary = Text()
        summary.append(f"\nCurrent: ${current_price:.2f}  ", style="bold white")
        change_style = "bold green" if price_change >= 0 else "bold red"
        summary.append(f"Change: ${price_change:+.2f} ({pct_change:+.2f}%)", style=change_style)

        return Text.assemble(chart_text, summary)

    def set_ticker(self, ticker: str):
        """Change the ticker being displayed."""
        self.ticker = ticker
        self.border_title = f"{ticker} Chart"
        self.run_worker(self.refresh_data(), exclusive=True)

    def set_period(self, period: str):
        """Change the time period."""
        self.period = period
        self.refresh_data()

    def set_interval(self, interval: str):
        """Change the interval."""
        self.interval = interval
        self.refresh_data()
