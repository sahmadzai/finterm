"""
News data fetching and processing.

DISCLAIMER: News articles are provided for informational purposes only and should not
be interpreted as investment recommendations. Always verify information from multiple
sources and consult qualified financial advisors before making investment decisions.
"""
import requests
import feedparser
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetches financial news from free RSS feeds (Yahoo Finance)."""

    def __init__(self, api_key: Optional[str] = None):
        # No API key needed for RSS feeds
        self.yahoo_rss_base = "https://finance.yahoo.com/rss/"

    def get_market_news(self, limit: int = 10) -> List[Dict]:
        """
        Get general market news from Yahoo Finance RSS.

        Args:
            limit: Maximum number of articles to return

        Returns:
            List of news articles
        """
        try:
            # Yahoo Finance top stories RSS feed
            feed_url = "https://finance.yahoo.com/rss/topstories"
            feed = feedparser.parse(feed_url)

            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.get('title', 'No title'),
                    'description': entry.get('summary', ''),
                    'source': 'Yahoo Finance',
                    'url': entry.get('link', ''),
                    'published_at': entry.get('published', ''),
                })

            return articles if articles else self._get_fallback_news(limit)
        except Exception as e:
            logger.error(f"Error fetching market news: {e}")
            return self._get_fallback_news(limit)

    def get_ticker_news(self, ticker: str, limit: int = 5) -> List[Dict]:
        """
        Get news for a specific ticker using yfinance.

        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of articles to return

        Returns:
            List of news articles
        """
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            news = stock.news

            articles = []
            for item in news[:limit]:
                articles.append({
                    'title': item.get('title', 'No title'),
                    'description': item.get('summary', item.get('title', '')),
                    'source': item.get('publisher', 'Yahoo Finance'),
                    'url': item.get('link', ''),
                    'published_at': datetime.fromtimestamp(item.get('providerPublishTime', 0)).isoformat() if item.get('providerPublishTime') else '',
                })

            return articles if articles else self._get_fallback_ticker_news(ticker, limit)
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return self._get_fallback_ticker_news(ticker, limit)

    def _get_fallback_news(self, limit: int = 10) -> List[Dict]:
        """Fallback method when news fetching fails."""
        return [
            {
                'title': 'Unable to fetch news',
                'description': 'News service temporarily unavailable. Please try again later.',
                'source': 'System',
                'url': '',
                'published_at': datetime.now().isoformat(),
            }
        ]

    def _get_fallback_ticker_news(self, ticker: str, limit: int = 5) -> List[Dict]:
        """Fallback method for ticker news when fetching fails."""
        return [
            {
                'title': f'News for {ticker} unavailable',
                'description': 'Unable to fetch ticker-specific news at this time.',
                'source': 'System',
                'url': '',
                'published_at': datetime.now().isoformat(),
            }
        ]
