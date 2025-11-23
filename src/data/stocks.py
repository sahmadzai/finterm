"""
Stock data fetching and processing using yfinance.

DISCLAIMER: This module provides stock market data for informational purposes only.
The data should NOT be used as the sole basis for investment decisions. Always conduct
your own research and consult with qualified financial advisors before investing.
Data accuracy is not guaranteed and delays or errors may occur.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class StockDataFetcher:
    """Fetches and caches stock market data."""

    def __init__(self):
        self._cache: Dict[str, Dict] = {}
        self._cache_timeout = timedelta(minutes=5)

    def get_quote(self, ticker: str) -> Optional[Dict]:
        """
        Get current quote for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with quote data or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'symbol': ticker,
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'open': info.get('open', 0),
                'previous_close': info.get('previousClose', 0),
            }
        except Exception as e:
            logger.error(f"Error fetching quote for {ticker}: {e}")
            return None

    def get_historical_data(
        self,
        ticker: str,
        period: str = "1mo",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Get historical price data.

        Args:
            ticker: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return None

    def get_company_info(self, ticker: str) -> Optional[Dict]:
        """
        Get detailed company information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with company info or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'description': info.get('longBusinessSummary', 'N/A'),
                'website': info.get('website', 'N/A'),
                'employees': info.get('fullTimeEmployees', 0),
                'city': info.get('city', 'N/A'),
                'state': info.get('state', 'N/A'),
                'country': info.get('country', 'N/A'),
            }
        except Exception as e:
            logger.error(f"Error fetching company info for {ticker}: {e}")
            return None

    def get_market_movers(self, tickers: List[str]) -> List[Tuple[str, float, float]]:
        """
        Get top movers from a list of tickers.

        Args:
            tickers: List of ticker symbols

        Returns:
            List of tuples (ticker, price, change_percent) sorted by absolute change
        """
        movers = []

        for ticker in tickers:
            quote = self.get_quote(ticker)
            if quote:
                movers.append((
                    ticker,
                    quote['price'],
                    quote['change_percent']
                ))

        # Sort by absolute percent change
        movers.sort(key=lambda x: abs(x[2]), reverse=True)
        return movers

    def get_financials(self, ticker: str) -> Optional[Dict]:
        """
        Get financial statements for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with financial data or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'revenue': info.get('totalRevenue', 0),
                'gross_profit': info.get('grossProfits', 0),
                'ebitda': info.get('ebitda', 0),
                'net_income': info.get('netIncomeToCommon', 0),
                'eps': info.get('trailingEps', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'roe': info.get('returnOnEquity', 0),
            }
        except Exception as e:
            logger.error(f"Error fetching financials for {ticker}: {e}")
            return None
