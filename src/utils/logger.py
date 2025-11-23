"""
Logging configuration for FinTerm.
"""

import logging
from pathlib import Path
from datetime import datetime


def setup_logger():
    """Set up file and console logging."""
    # Create logs directory
    log_dir = Path.home() / ".finterm" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log file with timestamp
    log_file = log_dir / f"finterm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            # logging.StreamHandler()
        ],
    )

    logger = logging.getLogger("finterm")
    logger.info(f"Logging to: {log_file}")

    return logger


# Create global logger instance
logger = setup_logger()
