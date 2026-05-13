#!/usr/bin/env python3
"""
GPIO button input handler.
"""

import RPi.GPIO as GPIO
import logging
from threading import Thread
import time

logger = logging.getLogger(__name__)


class ButtonHandler:
    """Manages GPIO button inputs for track control."""

    def __init__(self, config):
        """Initialize button handler.

        Args:
            config: Configuration object with GPIO settings
        """
        self.config = config
        self.running = False
        self.button_thread = None
        self.callbacks = {}
        self._setup_gpio()

    def _setup_gpio(self):
        """Setup GPIO pins for buttons."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup all button pins
        all_buttons = []
        all_buttons.extend(self.config.record_buttons)
        all_buttons.extend(self.config.play_buttons)

        for pin in all_buttons:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            logger.info(f"Button pin {pin} configured")

    def register_callback(self, pin, callback):
        """Register a callback for button press.

        Args:
            pin: GPIO pin number
            callback: Callback function to call on button press
        """
        self.callbacks[pin] = callback

    def start(self):
        """Start button polling thread."""
        self.running = True
        self.button_thread = Thread(target=self._poll_buttons, daemon=True)
        self.button_thread.start()
        logger.info("Button handler started")

    def stop(self):
        """Stop button polling thread."""
        self.running = False
        if self.button_thread:
            self.button_thread.join(timeout=2)
        GPIO.cleanup()
        logger.info("Button handler stopped")

    def _poll_buttons(self):
        """Poll buttons for presses and holds."""
        button_press_time = {}
        hold_threshold = 1.0  # 1 second for hold detection

        all_buttons = []
        all_buttons.extend(self.config.record_buttons)
        all_buttons.extend(self.config.play_buttons)

        while self.running:
            for pin in all_buttons:
                state = GPIO.input(pin)

                if state == GPIO.LOW:  # Button pressed
                    if pin not in button_press_time:
                        button_press_time[pin] = time.time()
                        logger.debug(f"Button press detected on pin {pin}")
                        if pin in self.callbacks:
                            self.callbacks[pin]("press")

                    # Check for hold
                    press_duration = time.time() - button_press_time[pin]
                    if press_duration > hold_threshold:
                        logger.debug(f"Button hold detected on pin {pin}")
                        if pin in self.callbacks:
                            self.callbacks[pin]("hold")

                else:  # Button released
                    if pin in button_press_time:
                        del button_press_time[pin]

            time.sleep(0.05)  # Poll every 50ms
