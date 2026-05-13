#!/usr/bin/env python3
"""
Main looper application for Raspberry Pi audio looper.
"""

import signal
import sys
import logging
from audio_handler import AudioHandler
from button_handler import ButtonHandler
from led_handler import LEDHandler
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LooperApp:
    """Main looper application."""

    def __init__(self):
        """Initialize the looper application."""
        logger.info("Initializing Raspberry Pi Audio Looper...")
        self.config = Config()
        self.audio_handler = AudioHandler(self.config)
        self.button_handler = ButtonHandler(self.config)
        self.led_handler = LEDHandler(self.config)
        self.running = True

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("Shutdown signal received. Cleaning up...")
        self.cleanup()
        sys.exit(0)

    def run(self):
        """Run the main looper loop."""
        logger.info("Starting audio looper...")
        self.setup_signal_handlers()

        try:
            self.audio_handler.start()
            self.button_handler.start()
            self.led_handler.start()

            # Keep the application running
            while self.running:
                signal.pause()

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received.")
            self.cleanup()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            self.cleanup()
            raise

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.audio_handler.stop()
        self.button_handler.stop()
        self.led_handler.stop()
        self.running = False


if __name__ == "__main__":
    app = LooperApp()
    app.run()
