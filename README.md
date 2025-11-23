```
                                /$$$$$$  /$$             /$$                                      
                               /$$__  $$|__/            | $$                                      
                              | $$  \__/ /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$  /$$$$$$/$$$$ 
                              | $$$$    | $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$| $$_  $$_  $$
                              | $$_/    | $$| $$  \ $$  | $$    | $$$$$$$$| $$  \__/| $$ \ $$ \ $$
                              | $$      | $$| $$  | $$  | $$ /$$| $$_____/| $$      | $$ | $$ | $$
                              | $$      | $$| $$  | $$  |  $$$$/|  $$$$$$$| $$      | $$ | $$ | $$
                              |__/      |__/|__/  |__/   \___/   \_______/|__/      |__/ |__/ |__/
```


A modern, Professional TUI (Terminal User Interface) for financial market analysis. Built with Python and Textual, FinTerm provides real-time market data, charts, news, and sentiment analysis right in your terminal.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)

## Features ✨

- **📊 Interactive Charts**: Candlestick and line charts with multiple timeframes (1d, 5d, 1mo, 3mo, 6mo, 1y)
- **📈 Market Movers**: Real-time top gainers and losers from your watchlist
- **📰 Financial News**: Latest market news and ticker-specific headlines
- **🎯 Market Sentiment**: AI-powered sentiment analysis based on price action
- **💼 Ticker Details**: Comprehensive company information, financials, and key metrics
- **⚡ Keyboard Shortcuts**: Lightning-fast navigation with intuitive hotkeys
- **🎨 Modern UI**: Clean, professional interface inspired by Bloomberg Terminal
- **🔧 Modular Architecture**: Extensible widget system for custom dashboards
- **📱 Responsive**: Adapts to terminal window size automatically

## Screenshots
<div style="flex-direction: row; justify-content: center; align-items: center; column-gap: 10;">
   <img width="48%" height="100%" alt="finterm terminal market data version 0.1.0 disclaimer acceptance screen screenshot" src="https://github.com/user-attachments/assets/c75fb9a8-1868-4fc4-b71e-9b357e9b9545" />
   <img width="48%" height="100%" alt="finterm terminal market data version 0.1.0 screenshot" src="https://github.com/user-attachments/assets/548b17c8-1463-42d2-99be-ad80e2df4679" />
</div>

## Quick Start 🚀

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sahmadzai/finterm.git
   cd finterm
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional - Set up News API (for real news):**
   ```bash
   # Get a free API key from https://newsapi.org
   export NEWS_API_KEY="your_api_key_here"
   ```

4. **Run FinTerm:**
   ```bash
   python -m src.app
   ```

### Installation via pip (coming soon)

```bash
pip install finterm
finterm
```

## Keyboard Shortcuts ⌨️

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `r` | Refresh all widgets |
| `h` | Toggle help screen |
| `1` | Show SPY ticker |
| `2` | Show QQQ ticker |
| `3` | Show AAPL ticker |
| `4` | Show TSLA ticker |
| `ESC` | Close help/dialog |

## Configuration ⚙️

### Environment Variables

Create a `.env` file in the project root:

```bash
# News API Key (get from https://newsapi.org)
NEWS_API_KEY=your_api_key_here

# Default tickers to track (comma-separated)
DEFAULT_TICKERS=SPY,QQQ,AAPL,MSFT,GOOGL,TSLA,NVDA,AMD

# Refresh interval in seconds
REFRESH_INTERVAL=60
```

### Custom Dashboard Layouts (Coming Soon)

FinTerm will support custom dashboard configurations via JSON files:

```json
{
  "name": "My Custom Dashboard",
  "widgets": [
    {
      "widget_type": "chart",
      "ticker": "AAPL",
      "period": "1mo",
      "interval": "1d"
    },
    {
      "widget_type": "news",
      "limit": 5
    }
  ]
}
```

## Architecture 🏗️

### Project Structure

```
finterm/
├── src/
│   ├── app.py              # Main application and screens
│   ├── widgets/            # Modular widget components
│   │   ├── base.py         # Base widget class
│   │   ├── chart.py        # Chart widget
│   │   ├── news.py         # News widget
│   │   ├── market_movers.py
│   │   ├── ticker_info.py
│   │   └── sentiment.py
│   ├── data/               # Data fetching modules
│   │   ├── stocks.py       # Stock data via yfinance
│   │   ├── news.py         # News via NewsAPI
│   │   └── sentiment.py    # Sentiment analysis
│   └── utils/              # Utilities
│       └── config.py       # Configuration management
├── requirements.txt
├── setup.py
└── README.md
```

### Technology Stack

- **[Textual](https://textual.textualize.io/)**: Modern TUI framework
- **[Rich](https://rich.readthedocs.io/)**: Beautiful terminal formatting
- **[yfinance](https://github.com/ranaroussi/yfinance)**: Yahoo Finance data
- **[plotext](https://github.com/piccolomo/plotext)**: Terminal plotting
- **[NewsAPI](https://newsapi.org/)**: Financial news aggregation
- **[Pydantic](https://pydantic.dev/)**: Data validation

## Data Sources 📡

- **Stock Data**: Yahoo Finance (via yfinance) - Free, no API key required
- **News**: NewsAPI - Free tier available (100 requests/day)
- **Sentiment**: Proprietary algorithm based on price action and volume

## Development 🛠️

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/sahmadzai/finterm.git
cd finterm

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests (coming soon)
pytest

# Format code
black src/

# Lint code
flake8 src/
```

### Creating Custom Widgets

Extend the `BaseWidget` class to create your own widgets:

```python
from src.widgets.base import BaseWidget
from rich.text import Text

class MyCustomWidget(BaseWidget):
    async def fetch_data(self):
        # Fetch your data here
        self.my_data = await get_data()

    def render_content(self):
        # Render your widget
        return Text("My custom content")
```

## Rough Roadmap 🗺️

### v0.2.0 (Next Release)
- [ ] Custom dashboard layouts via JSON config
- [ ] More chart types (volume, indicators)
- [ ] Technical indicators (RSI, MACD, Moving Averages)
- [ ] Watchlist management

### v0.3.0
- [ ] Options chain viewer
- [ ] Crypto support
- [ ] Economic calendar
- [ ] Earnings calendar
- [ ] Alert system

### v1.0.0
- [ ] Multi-page dashboards
- [ ] Plugin system for custom widgets
- [ ] Historical data export
- [ ] Backtesting framework
- [ ] Real-time WebSocket feeds

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write unit tests for new features
- Update README for significant changes

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Built for professional traders and investors
- Built with [Textual](https://textual.textualize.io/) by Will McGugan
- Financial data provided by Yahoo Finance
- News data from [NewsAPI](https://newsapi.org/)

## Disclaimer ⚠️

This software is for informational purposes only. It is not financial advice and should not be used as the sole basis for investment decisions. Always do your own research and consult with a qualified financial advisor.

## Support 💬

- **Issues**: [GitHub Issues](https://github.com/sahmadzai/finterm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sahmadzai/finterm/discussions)

## Star History ⭐

If you find FinTerm useful, please consider giving it a star on GitHub!
