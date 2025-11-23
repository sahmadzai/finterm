"""
FinTerm - A professional TUI for financial market analysis.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from typing import Optional

from .widgets import (
    ChartWidget,
    MarketMoversWidget,
    NewsWidget,
    TickerInfoWidget,
    SentimentWidget,
    MarketTickerWidget,
)
from .utils.config import config
from .utils.logger import logger


class DashboardScreen(Screen):
    """Main dashboard screen."""

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "refresh", "Refresh All"),
        Binding("1", "show_spy", "SPY"),
        Binding("2", "show_qqq", "QQQ"),
        Binding("3", "show_aapl", "AAPL"),
        Binding("4", "show_tsla", "TSLA"),
        Binding("h", "toggle_help", "Help"),
    ]

    CSS = """
    DashboardScreen {
        layout: vertical;
    }

    #market-ticker {
        height: 3;
        dock: top;
    }

    #main-content {
        height: 1fr;
        layout: vertical;
    }

    #top-row {
        height: 3fr;
        layout: horizontal;
    }

    #chart-main {
        width: 2fr;
    }

    #ticker-info {
        width: 1fr;
    }

    #bottom-row {
        height: 2fr;
        layout: horizontal;
    }

    #market-movers {
        width: 1fr;
    }

    #news {
        width: 1fr;
    }

    #sentiment {
        width: 1fr;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_ticker = "SPY"

    def compose(self) -> ComposeResult:
        """Create child widgets for the dashboard."""
        yield Header()

        # Market ticker at the top
        yield MarketTickerWidget(id="market-ticker")

        # Main content container
        with Vertical(id="main-content"):
            # Top row: Chart and Ticker Info
            with Horizontal(id="top-row"):
                yield ChartWidget(
                    ticker=self.current_ticker,
                    period="1mo",
                    interval="1d",
                    id="chart-main"
                )
                yield TickerInfoWidget(
                    ticker=self.current_ticker,
                    id="ticker-info"
                )

            # Bottom row: Market Movers, News, Sentiment
            with Horizontal(id="bottom-row"):
                yield MarketMoversWidget(id="market-movers")
                yield NewsWidget(limit=5, id="news")
                yield SentimentWidget(id="sentiment")

        yield Footer()

    def action_refresh(self):
        """Refresh all widgets."""
        for widget in self.query("BaseWidget"):
            widget.refresh_data()

    def action_show_spy(self):
        """Show SPY data."""
        self._update_ticker("SPY")

    def action_show_qqq(self):
        """Show QQQ data."""
        self._update_ticker("QQQ")

    def action_show_aapl(self):
        """Show AAPL data."""
        self._update_ticker("AAPL")

    def action_show_tsla(self):
        """Show TSLA data."""
        self._update_ticker("TSLA")

    def _update_ticker(self, ticker: str):
        """Update the current ticker across relevant widgets."""
        self.current_ticker = ticker

        # Update chart
        chart = self.query_one("#chart-main", ChartWidget)
        chart.set_ticker(ticker)

        # Update ticker info
        info = self.query_one("#ticker-info", TickerInfoWidget)
        info.set_ticker(ticker)

        # Optionally update news to ticker-specific
        # news = self.query_one("#news", NewsWidget)
        # news.set_ticker(ticker)

    def action_toggle_help(self):
        """Toggle help screen."""
        self.app.push_screen(HelpScreen())


class DisclaimerScreen(Screen):
    """Disclaimer screen shown on first launch."""

    BINDINGS = [
        Binding("enter", "accept", "Accept & Continue"),
        Binding("escape", "reject", "Decline & Exit"),
    ]

    CSS = """
    DisclaimerScreen {
        align: center middle;
    }

    #disclaimer-container {
        width: 100;
        height: auto;
        border: heavy red;
        background: $surface;
        padding: 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the disclaimer screen."""
        disclaimer_text = Text()
        disclaimer_text.append("⚠️  IMPORTANT DISCLAIMER ⚠️\n\n", style="bold red")
        disclaimer_text.append("═" * 80 + "\n\n", style="red")

        disclaimer_text.append("NOT FINANCIAL ADVICE\n", style="bold yellow")
        disclaimer_text.append(
            "FinTerm is for informational and educational purposes only. The information\n"
            "provided does NOT constitute financial, investment, or trading advice.\n\n",
            style="white",
        )

        disclaimer_text.append("NO WARRANTY\n", style="bold yellow")
        disclaimer_text.append(
            "This software is provided 'AS IS' without warranty of any kind. We do not\n"
            "guarantee the accuracy, completeness, or timeliness of any data.\n\n",
            style="white",
        )

        disclaimer_text.append("YOUR RESPONSIBILITY\n", style="bold yellow")
        disclaimer_text.append(
            "You are solely responsible for your investment decisions. Always:\n"
            "  • Conduct your own research\n"
            "  • Consult qualified financial advisors\n"
            "  • Understand the risks involved\n"
            "  • Only invest money you can afford to lose\n\n",
            style="white",
        )

        disclaimer_text.append("LIMITATION OF LIABILITY\n", style="bold yellow")
        disclaimer_text.append(
            "The authors are NOT liable for any financial losses, damages, or claims\n"
            "arising from use of this software. Investing involves substantial risk.\n\n",
            style="white",
        )

        disclaimer_text.append("═" * 80 + "\n\n", style="red")
        disclaimer_text.append(
            "BY PRESSING ENTER, YOU ACKNOWLEDGE THAT YOU HAVE READ AND UNDERSTOOD\n"
            "THIS DISCLAIMER AND AGREE TO USE THIS SOFTWARE AT YOUR OWN RISK.\n\n",
            style="bold cyan",
        )

        disclaimer_text.append("Press ", style="dim")
        disclaimer_text.append("ENTER", style="bold green")
        disclaimer_text.append(" to accept and continue, or ", style="dim")
        disclaimer_text.append("ESC", style="bold red")
        disclaimer_text.append(" to decline and exit.\n", style="dim")

        disclaimer_text.append(
            "\nSee DISCLAIMER.md for full legal terms.", style="dim italic"
        )

        yield Container(Static(disclaimer_text), id="disclaimer-container")

    def action_accept(self):
        """Accept disclaimer and continue to dashboard."""
        self.app.pop_screen()

    def action_reject(self):
        """Reject disclaimer and exit application."""
        self.app.exit()


class HelpScreen(Screen):
    """Help screen showing keyboard shortcuts."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
    ]

    CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-container {
        width: 80;
        height: auto;
        border: heavy $primary;
        background: $surface;
        padding: 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the help screen."""
        help_text = Text()
        help_text.append("FINTERM KEYBOARD SHORTCUTS\n\n", style="bold cyan")
        help_text.append("═" * 50 + "\n\n", style="blue")

        shortcuts = [
            ("q", "Quit application"),
            ("r", "Refresh all widgets"),
            ("h", "Toggle this help screen"),
            ("1", "Show SPY ticker"),
            ("2", "Show QQQ ticker"),
            ("3", "Show AAPL ticker"),
            ("4", "Show TSLA ticker"),
            ("ESC", "Close help screen"),
        ]

        for key, description in shortcuts:
            help_text.append(f"  {key:10s}", style="bold yellow")
            help_text.append(f"  {description}\n", style="white")

        help_text.append("\n" + "═" * 50 + "\n\n", style="blue")
        help_text.append("Press ESC or q to close this help screen", style="dim italic")

        yield Container(Static(help_text), id="help-container")

    def action_dismiss(self):
        """Dismiss the help screen."""
        self.app.pop_screen()


class FinTermApp(App):
    """
    FinTerm - A professional TUI for financial market analysis.

    Features:
    - Real-time stock charts with candlestick view
    - Market movers and top gainers/losers
    - Latest financial news
    - Market sentiment analysis
    - Detailed ticker information
    - Keyboard shortcuts for quick navigation
    """

    TITLE = "FinTerm"
    SUB_TITLE = "Professional Market Analysis Dashboard"

    CSS = """
    Screen {
        background: $surface;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
    ]

    def on_mount(self):
        """Called when the app starts."""
        # Show disclaimer first, then dashboard
        self.push_screen(DashboardScreen())
        self.push_screen(DisclaimerScreen())

    def action_quit(self):
        """Quit the application."""
        self.exit()


def main():
    """Main entry point for FinTerm."""
    app = FinTermApp()
    app.run()


if __name__ == "__main__":
    main()
