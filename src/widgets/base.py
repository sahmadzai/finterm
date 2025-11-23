"""
Base widget class for FinTerm widgets.
"""
from textual.widget import Widget
from textual.reactive import reactive
from typing import Optional


class BaseWidget(Widget):
    """
    Base class for all FinTerm widgets.

    Provides common functionality for data fetching, refresh, and display.
    Subclasses must implement fetch_data() and render_content().
    """

    refresh_interval: reactive[int] = reactive(60)
    is_loading: reactive[bool] = reactive(False)
    has_error: reactive[bool] = reactive(False)
    error_message: reactive[str] = reactive("")

    def __init__(
        self,
        title: str = "Widget",
        refresh_interval: int = 60,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.widget_title = title
        self.refresh_interval = refresh_interval
        self.border_title = title

    async def fetch_data(self):
        """
        Fetch data for the widget.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement fetch_data()")

    def render_content(self):
        """
        Render the widget content.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement render_content()")

    async def refresh_data(self):
        """Refresh the widget data."""
        self.is_loading = True
        self.has_error = False

        try:
            await self.fetch_data()
        except Exception as e:
            self.has_error = True
            self.error_message = str(e)
        finally:
            self.is_loading = False
            self.refresh()

    def on_mount(self):
        """Called when widget is mounted."""
        # Initial data fetch on mount
        # Auto-refresh disabled for v0.1.0 - use 'r' key to manually refresh
        self.run_worker(self.refresh_data(), exclusive=True)
