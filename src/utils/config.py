"""
Configuration management for FinTerm.
"""
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import json


class WidgetConfig(BaseModel):
    """Configuration for a dashboard widget."""
    widget_type: str
    title: str
    position: tuple[int, int] = (0, 0)
    size: tuple[int, int] = (1, 1)
    refresh_interval: int = 60  # seconds
    params: dict = Field(default_factory=dict)


class DashboardConfig(BaseModel):
    """Configuration for a dashboard layout."""
    name: str
    widgets: List[WidgetConfig]


class AppConfig(BaseModel):
    """Main application configuration."""
    default_tickers: List[str] = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "TSLA"]
    news_api_key: Optional[str] = None
    refresh_interval: int = 60
    theme: str = "dark"

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "AppConfig":
        """Load configuration from file or environment."""
        if config_path and config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                return cls(**data)

        # Load from environment variables
        return cls(
            news_api_key=os.getenv("NEWS_API_KEY"),
            default_tickers=os.getenv(
                "DEFAULT_TICKERS",
                "SPY,QQQ,AAPL,MSFT,GOOGL,TSLA"
            ).split(",")
        )

    def save(self, config_path: Path):
        """Save configuration to file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)


# Global configuration instance
config = AppConfig.load()
