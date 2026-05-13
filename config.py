#!/usr/bin/env python3
"""
Configuration settings for the Raspberry Pi audio looper.
"""

import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration settings for the looper application."""

    def __init__(self):
        """Initialize configuration with default values."""
        # Audio settings
        self.sample_rate = 44100  # Hz
        self.channels = 1  # Mono
        self.chunk_size = 2048  # Frames per buffer
        self.buffer_size = self.sample_rate // self.chunk_size

        # Device indices (use 0 for default, adjust as needed)
        self.input_device_id = None  # Use default input
        self.output_device_id = None  # Use default output

        # Track settings
        self.num_tracks = 4

        # GPIO pin assignments (BCM numbering)
        # Record buttons for each track
        self.record_buttons = [17, 27, 22, 23]
        # Play buttons for each track
        self.play_buttons = [24, 25, 26, 16]

        # Record LED indicators
        self.record_leds = [5, 6, 12, 13]
        # Play LED indicators
        self.play_leds = [19, 20, 21, 26]

        logger.info("Configuration loaded")

    def set_device_ids(self, input_id, output_id):
        """Set audio device IDs.

        Args:
            input_id: Input device index
            output_id: Output device index
        """
        self.input_device_id = input_id
        self.output_device_id = output_id
        logger.info(f"Audio devices set - Input: {input_id}, Output: {output_id}")

    def set_gpio_pins(self, record_buttons, play_buttons, record_leds, play_leds):
        """Set GPIO pin assignments.

        Args:
            record_buttons: List of record button pin numbers
            play_buttons: List of play button pin numbers
            record_leds: List of record LED pin numbers
            play_leds: List of play LED pin numbers
        """
        self.record_buttons = record_buttons
        self.play_buttons = play_buttons
        self.record_leds = record_leds
        self.play_leds = play_leds
        logger.info("GPIO pins updated")

    def set_audio_params(self, sample_rate, channels, chunk_size):
        """Set audio parameters.

        Args:
            sample_rate: Sample rate in Hz
            channels: Number of audio channels
            chunk_size: Frames per buffer
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.buffer_size = self.sample_rate // self.chunk_size
        logger.info(f"Audio params updated - {sample_rate}Hz, {channels} ch, {chunk_size} chunk")
