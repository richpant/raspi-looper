#!/usr/bin/env python3
"""
GPIO LED control with blink and pulse effects.
"""

import RPi.GPIO as GPIO
import logging
from threading import Thread
import time

logger = logging.getLogger(__name__)


class LEDHandler:
    """Manages GPIO LED outputs with various visual effects."""

    def __init__(self, config):
        """Initialize LED handler.

        Args:
            config: Configuration object with GPIO settings
        """
        self.config = config
        self.running = False
        self.led_thread = None
        self.led_state = {}
        self.led_mode = {}  # 'off', 'on', 'blink', 'pulse'
        self._setup_gpio()

    def _setup_gpio(self):
        """Setup GPIO pins for LEDs."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup all LED pins
        all_leds = []
        all_leds.extend(self.config.record_leds)
        all_leds.extend(self.config.play_leds)

        for pin in all_leds:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            self.led_state[pin] = False
            self.led_mode[pin] = 'off'
            logger.info(f"LED pin {pin} configured")

    def start(self):
        """Start LED control thread."""
        self.running = True
        self.led_thread = Thread(target=self._update_leds, daemon=True)
        self.led_thread.start()
        logger.info("LED handler started")

    def stop(self):
        """Stop LED control thread."""
        self.running = False
        if self.led_thread:
            self.led_thread.join(timeout=2)
        GPIO.cleanup()
        logger.info("LED handler stopped")

    def set_led(self, pin, state):
        """Set LED to on or off.

        Args:
            pin: GPIO pin number
            state: True for on, False for off
        """
        if pin in self.led_state:
            self.led_state[pin] = state
            self.led_mode[pin] = 'on' if state else 'off'
            logger.debug(f"LED pin {pin} set to {'on' if state else 'off'}")

    def blink_led(self, pin, frequency=2):
        """Set LED to blink.

        Args:
            pin: GPIO pin number
            frequency: Blink frequency in Hz
        """
        if pin in self.led_state:
            self.led_mode[pin] = ('blink', frequency)
            logger.debug(f"LED pin {pin} set to blink at {frequency} Hz")

    def pulse_led(self, pin):
        """Set LED to pulse (PWM effect).

        Args:
            pin: GPIO pin number
        """
        if pin in self.led_state:
            self.led_mode[pin] = 'pulse'
            logger.debug(f"LED pin {pin} set to pulse")

    def _update_leds(self):
        """Update LED states based on modes."""
        blink_state = 0
        pulse_brightness = 0
        pulse_direction = 1

        while self.running:
            for pin in self.led_state.keys():
                mode = self.led_mode[pin]

                if mode == 'off':
                    GPIO.output(pin, GPIO.LOW)
                elif mode == 'on':
                    GPIO.output(pin, GPIO.HIGH)
                elif isinstance(mode, tuple) and mode[0] == 'blink':
                    frequency = mode[1]
                    # Simple blink toggle
                    if int(time.time() * frequency) % 2 == 0:
                        GPIO.output(pin, GPIO.HIGH)
                    else:
                        GPIO.output(pin, GPIO.LOW)
                elif mode == 'pulse':
                    # Simple pulse using GPIO output timing
                    pulse_brightness = (pulse_brightness + pulse_direction) % 100
                    if pulse_brightness == 0 or pulse_brightness == 99:
                        pulse_direction *= -1
                    # Approximate PWM with GPIO timing
                    GPIO.output(pin, GPIO.HIGH if pulse_brightness > 50 else GPIO.LOW)

            time.sleep(0.05)  # Update every 50ms
