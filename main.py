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
        self._register_callbacks()

    def _register_callbacks(self):
        """Register button callbacks to audio and LED handlers."""
        # Register record button callbacks
        for idx, pin in enumerate(self.config.record_buttons):
            self.button_handler.register_callback(
                pin,
                lambda action, track=idx: self._on_record_button(track, action)
            )
        
        # Register play button callbacks
        for idx, pin in enumerate(self.config.play_buttons):
            self.button_handler.register_callback(
                pin,
                lambda action, track=idx: self._on_play_button(track, action)
            )

    def _on_record_button(self, track_idx, action):
        """Handle record button press."""
        if action == "press":
            if self.audio_handler.recording[track_idx]:
                self.audio_handler.stop_recording(track_idx)
                self.led_handler.set_led(self.config.record_leds[track_idx], False)
                logger.info(f"Recording stopped on track {track_idx}")
            else:
                self.audio_handler.record_track(track_idx)
                self.led_handler.set_led(self.config.record_leds[track_idx], True)
                logger.info(f"Recording started on track {track_idx}")

    def _on_play_button(self, track_idx, action):
        """Handle play button press."""
        if action == "press":
            if self.audio_handler.loop_lengths[track_idx] > 0:
                # Toggle playback by checking current position
                if self.audio_handler.current_positions[track_idx] == 0 and \
                   len(self.audio_handler.track_buffers[track_idx]) == 0:
                    # Start playback
                    self.led_handler.set_led(self.config.play_leds[track_idx], True)
                    logger.info(f"Playback started on track {track_idx}")
                else:
                    # Stop playback
                    self.audio_handler.current_positions[track_idx] = 0
                    self.led_handler.set_led(self.config.play_leds[track_idx], False)
                    logger.info(f"Playback stopped on track {track_idx}")

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
