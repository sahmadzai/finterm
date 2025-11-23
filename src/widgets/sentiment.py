"""
Market sentiment widget.
"""
from textual.widgets import Static
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from typing import List
from ..data.sentiment import SentimentAnalyzer
from ..utils.config import config
from .base import BaseWidget


class SentimentWidget(BaseWidget):
    """
    Widget displaying market sentiment analysis.
    """

    DEFAULT_CSS = """
    SentimentWidget {
        border: solid $primary;
        height: 100%;
    }
    """

    def __init__(
        self,
        tickers: List[str] = None,
        **kwargs
    ):
        super().__init__(title="Market Sentiment", **kwargs)
        self.tickers = tickers or config.default_tickers
        self.sentiment_analyzer = SentimentAnalyzer()
        self.sentiment_data = None

    async def fetch_data(self):
        """Fetch sentiment data."""
        self.sentiment_data = self.sentiment_analyzer.analyze_market_sentiment(self.tickers)

    def render(self) -> RenderableType:
        """Render the sentiment widget."""
        if self.is_loading:
            return Panel(
                Text("Analyzing market sentiment...", style="yellow"),
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
        """Render sentiment analysis."""
        if not self.sentiment_data:
            return Text("No sentiment data available", style="yellow")

        text = Text()

        # Overall sentiment
        overall = self.sentiment_data['overall_sentiment']
        avg_change = self.sentiment_data['average_change']

        # Color based on sentiment
        if overall == "Bullish":
            sentiment_style = "bold green"
            indicator = "↑"
        elif overall == "Bearish":
            sentiment_style = "bold red"
            indicator = "↓"
        else:
            sentiment_style = "bold yellow"
            indicator = "→"

        text.append("Overall Market: ", style="bold white")
        text.append(f"{indicator} {overall}\n", style=sentiment_style)
        text.append(f"Average Change: ", style="white")

        change_style = "green" if avg_change >= 0 else "red"
        text.append(f"{avg_change:+.2f}%\n\n", style=change_style)

        # Sentiment breakdown
        text.append("═" * 40 + "\n", style="dim blue")
        text.append("SENTIMENT BREAKDOWN\n", style="bold cyan")
        text.append("═" * 40 + "\n\n", style="dim blue")

        bullish = self.sentiment_data['bullish_count']
        bearish = self.sentiment_data['bearish_count']
        neutral = self.sentiment_data['neutral_count']
        total = bullish + bearish + neutral

        if total > 0:
            text.append(f"Bullish:  {bullish:2d} ({bullish/total*100:5.1f}%) ", style="white")
            text.append("█" * int(bullish/total*20), style="green")
            text.append("\n")

            text.append(f"Neutral:  {neutral:2d} ({neutral/total*100:5.1f}%) ", style="white")
            text.append("█" * int(neutral/total*20), style="yellow")
            text.append("\n")

            text.append(f"Bearish:  {bearish:2d} ({bearish/total*100:5.1f}%) ", style="white")
            text.append("█" * int(bearish/total*20), style="red")
            text.append("\n")

        # Top sentiments
        if self.sentiment_data.get('ticker_sentiments'):
            text.append("\n")
            text.append("═" * 40 + "\n", style="dim blue")
            text.append("TOP MOVERS SENTIMENT\n", style="bold cyan")
            text.append("═" * 40 + "\n\n", style="dim blue")

            # Show top 5 most extreme sentiments
            sentiments = sorted(
                self.sentiment_data['ticker_sentiments'],
                key=lambda x: abs(x['price_change_5d']),
                reverse=True
            )[:5]

            for s in sentiments:
                ticker = s['ticker']
                sentiment = s['sentiment']
                change = s['price_change_5d']

                # Determine style
                if 'Bullish' in sentiment:
                    style = "green"
                    icon = "↑"
                elif 'Bearish' in sentiment:
                    style = "red"
                    icon = "↓"
                else:
                    style = "yellow"
                    icon = "→"

                text.append(f"{ticker:6s} ", style="cyan")
                text.append(f"{icon} {sentiment:15s} ", style=style)
                text.append(f"{change:+6.2f}%\n", style=style)

        return text
