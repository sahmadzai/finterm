"""
Setup configuration for FinTerm.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="finterm",
    version="0.1.0",
    author="Shamsullah Ahmadzai",
    description="A professional TUI for financial market analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sahmadzai/finterm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Environment :: Console",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "textual>=0.47.0",
        "rich>=13.7.0",
        "yfinance>=0.2.36",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "newsapi-python>=0.2.7",
        "requests>=2.31.0",
        "plotext>=5.2.8",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "python-dateutil>=2.8.2",
        "pytz>=2023.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "finterm=src.app:main",
        ],
    },
    keywords=[
        "terminal",
        "tui",
        "finance",
        "trading",
        "stocks",
        "bloomberg",
        "market-data",
        "dashboard",
    ],
    project_urls={
        "Bug Reports": "https://github.com/sahmadzai/finterm/issues",
        "Source": "https://github.com/sahmadzai/finterm",
    },
)
