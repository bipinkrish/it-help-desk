#!/usr/bin/env python3
"""Script to run the LiveKit agent."""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from agent import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Agent stopped by user")
    except Exception as e:
        logging.error(f"Agent error: {e}")
        sys.exit(1)
