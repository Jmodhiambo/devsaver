#!/usr/bin/env python3
"""Logging configuration for DevSaver."""

import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn’t exist
LOG_DIR = "app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5),
        logging.StreamHandler()
    ],
)

# Get the main logger
logger = logging.getLogger("DevSaver")
