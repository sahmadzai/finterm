"""
News widget displaying latest financial news.
"""
from textual.widgets import Static
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Optional
from datetime import datetime
from ..data.news import NewsFetcher
from .base import BaseWidget


class NewsWidget(BaseWidget):
    """
    Widget displaying latest financial news.
    """

    DEFAULT_CSS = """
    NewsWidget {
        border: solid $primary;
        height: 100%;
    }
    """

    def __init__(
        self,
        ticker: Optional[str] = None,
        limit: int = 5,
        **kwargs
    ):
        title = f"{ticker} News" if ticker else "Market News"
        super().__init__(title=title, **kwargs)
        self.ticker = ticker
        self.limit = limit
        self.news_fetcher = NewsFetcher()
        self.news_data = []

    async def fetch_data(self):
        """Fetch news data."""
        if self.ticker:
            self.news_data = self.news_fetcher.get_ticker_news(self.ticker, self.limit)
        else:
            self.news_data = self.news_fetcher.get_market_news(self.limit)

    def render(self) -> RenderableType:
        """Render the news widget."""
        if self.is_loading:
            return Panel(
                Text("Loading news...", style="yellow"),
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
        """Render news articles."""
        if not self.news_data:
            return Text("No news available", style="yellow")

        text = Text()

        for i, article in enumerate(self.news_data, 1):
            # Add article number and title
            text.append(f"{i}. ", style="bold cyan")
            text.append(f"{article['title']}\n", style="bold white")

            # Add source and time
            source = article.get('source', 'Unknown')
            published = article.get('published_at', '')

            # Parse and format time
            if published:
                try:
                    pub_time = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    time_str = pub_time.strftime('%Y-%m-%d %H:%M')
                except:
                    time_str = published

                text.append(f"   {source}", style="dim cyan")
                text.append(" • ", style="dim")
                text.append(f"{time_str}\n", style="dim yellow")
            else:
                text.append(f"   {source}\n", style="dim cyan")

            # Add description if available
            description = article.get('description', '')
            if description and description != 'No description':
                # Truncate long descriptions
                if len(description) > 150:
                    description = description[:147] + "..."
                text.append(f"   {description}\n", style="white")

            # Add spacing between articles
            if i < len(self.news_data):
                text.append("\n")

        return text

    def set_ticker(self, ticker: Optional[str]):
        """Change the ticker for news."""
        self.ticker = ticker
        self.border_title = f"{ticker} News" if ticker else "Market News"
        self.refresh_data()
