#!/usr/bin/env python3
"""
Audio I/O handler for USB audio card.
"""

import pyaudio
import numpy as np
import logging
from threading import Thread
from collections import deque

logger = logging.getLogger(__name__)


class AudioHandler:
    """Manages audio input/output for the looper."""

    def __init__(self, config):
        """Initialize audio handler.

        Args:
            config: Configuration object with audio settings
        """
        self.config = config
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        self.audio_thread = None

        # Audio buffers for each track
        self.track_buffers = [
            deque(maxlen=config.buffer_size * 60)  # ~60 second max per track
            for _ in range(config.num_tracks)
        ]
        self.current_positions = [0] * config.num_tracks
        self.loop_lengths = [0] * config.num_tracks
        self.recording = [False] * config.num_tracks

    def list_devices(self):
        """List available audio devices."""
        logger.info("Available audio devices:")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            logger.info(f"{i}: {info['name']}")

    def start(self):
        """Start audio stream and processing thread."""
        try:
            self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=self.config.channels,
                rate=self.config.sample_rate,
                input=True,
                output=True,
                input_device_index=self.config.input_device_id,
                output_device_index=self.config.output_device_id,
                frames_per_buffer=self.config.chunk_size,
                stream_callback=self._audio_callback
            )
            self.stream.start_stream()
            self.running = True
            logger.info("Audio stream started")
        except Exception as e:
            logger.error(f"Failed to start audio stream: {e}")
            raise

    def stop(self):
        """Stop audio stream and processing thread."""
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        logger.info("Audio stream stopped")

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream processing.

        Args:
            in_data: Input audio data
            frame_count: Number of frames
            time_info: Time information
            status: Stream status

        Returns:
            Tuple of (output_data, continue_flag)
        """
        if status:
            logger.warning(f"Audio stream status: {status}")

        # Convert input data to numpy array
        audio_data = np.frombuffer(in_data, dtype=np.float32)

        # Process audio and generate output
        output_data = self._process_audio(audio_data, frame_count)

        return (output_data.tobytes(), pyaudio.paContinue)

    def _process_audio(self, input_data, frame_count):
        """Process audio for recording and playback.

        Args:
            input_data: Input audio samples
            frame_count: Number of frames to process

        Returns:
            Output audio data as numpy array
        """
        output_data = np.zeros(frame_count, dtype=np.float32)

        for track_idx in range(self.config.num_tracks):
            if self.recording[track_idx]:
                # Record input to track buffer
                self.track_buffers[track_idx].extend(input_data)

            # Playback recorded audio
            if self.loop_lengths[track_idx] > 0:
                start_pos = self.current_positions[track_idx]
                end_pos = min(start_pos + frame_count, self.loop_lengths[track_idx])
                samples_to_play = end_pos - start_pos

                if samples_to_play > 0:
                    playback_data = list(self.track_buffers[track_idx])[start_pos:end_pos]
                    output_data[:samples_to_play] += np.array(playback_data)

                # Update position and loop if necessary
                self.current_positions[track_idx] = end_pos % self.loop_lengths[track_idx]

        return output_data

    def record_track(self, track_idx):
        """Start recording on a track.

        Args:
            track_idx: Index of track to record
        """
        if track_idx < self.config.num_tracks:
            self.recording[track_idx] = True
            logger.info(f"Recording started on track {track_idx}")

    def stop_recording(self, track_idx):
        """Stop recording on a track.

        Args:
            track_idx: Index of track to stop recording
        """
        if track_idx < self.config.num_tracks:
            self.recording[track_idx] = False
            # Set loop length on first recording
            if self.loop_lengths[track_idx] == 0:
                self.loop_lengths[track_idx] = len(self.track_buffers[track_idx])
            logger.info(f"Recording stopped on track {track_idx}")

    def clear_track(self, track_idx):
        """Clear a track's buffer.

        Args:
            track_idx: Index of track to clear
        """
        if track_idx < self.config.num_tracks:
            self.track_buffers[track_idx].clear()
            self.loop_lengths[track_idx] = 0
            self.current_positions[track_idx] = 0
            logger.info(f"Track {track_idx} cleared")
