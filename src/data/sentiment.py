"""
Market sentiment analysis.

DISCLAIMER: Sentiment analysis provided is for informational purposes only and should
NOT be interpreted as investment advice or trading signals. Sentiment scores are based
on algorithmic analysis and may not reflect actual market conditions. Always conduct
your own analysis and consult qualified financial advisors before making investment decisions.
"""
from typing import Dict, List
import logging
from .stocks import StockDataFetcher

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes market sentiment based on price action and volume."""

    def __init__(self):
        self.stock_fetcher = StockDataFetcher()

    def analyze_ticker_sentiment(self, ticker: str) -> Dict:
        """
        Analyze sentiment for a specific ticker based on price action.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with sentiment analysis
        """
        try:
            # Get recent historical data
            df = self.stock_fetcher.get_historical_data(ticker, period="5d", interval="1d")

            if df is None or len(df) < 2:
                return self._get_neutral_sentiment(ticker)

            # Calculate price momentum
            price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100

            # Calculate volume trend
            avg_volume = df['Volume'].mean()
            recent_volume = df['Volume'].iloc[-1]
            volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1

            # Determine sentiment
            if price_change > 2:
                sentiment = "Bullish"
                score = min(100, 50 + price_change * 5)
            elif price_change > 0.5:
                sentiment = "Slightly Bullish"
                score = 50 + price_change * 5
            elif price_change < -2:
                sentiment = "Bearish"
                score = max(0, 50 + price_change * 5)
            elif price_change < -0.5:
                sentiment = "Slightly Bearish"
                score = 50 + price_change * 5
            else:
                sentiment = "Neutral"
                score = 50

            return {
                'ticker': ticker,
                'sentiment': sentiment,
                'score': score,
                'price_change_5d': price_change,
                'volume_ratio': volume_ratio,
                'trend': 'increasing' if price_change > 0 else 'decreasing',
            }

        except Exception as e:
            logger.error(f"Error analyzing sentiment for {ticker}: {e}")
            return self._get_neutral_sentiment(ticker)

    def analyze_market_sentiment(self, tickers: List[str]) -> Dict:
        """
        Analyze overall market sentiment based on major indices.

        Args:
            tickers: List of ticker symbols to analyze

        Returns:
            Dictionary with market sentiment
        """
        sentiments = []
        bullish_count = 0
        bearish_count = 0
        total_change = 0

        for ticker in tickers:
            sentiment = self.analyze_ticker_sentiment(ticker)
            sentiments.append(sentiment)

            if 'Bullish' in sentiment['sentiment']:
                bullish_count += 1
            elif 'Bearish' in sentiment['sentiment']:
                bearish_count += 1

            total_change += sentiment['price_change_5d']

        avg_change = total_change / len(tickers) if tickers else 0

        # Determine overall market sentiment
        if bullish_count > bearish_count * 1.5:
            overall = "Bullish"
        elif bearish_count > bullish_count * 1.5:
            overall = "Bearish"
        else:
            overall = "Neutral"

        return {
            'overall_sentiment': overall,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'neutral_count': len(tickers) - bullish_count - bearish_count,
            'average_change': avg_change,
            'ticker_sentiments': sentiments,
        }

    def _get_neutral_sentiment(self, ticker: str) -> Dict:
        """Return neutral sentiment when data is unavailable."""
        return {
            'ticker': ticker,
            'sentiment': 'Neutral',
            'score': 50,
            'price_change_5d': 0,
            'volume_ratio': 1,
            'trend': 'stable',
        }
