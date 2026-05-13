# Raspberry Pi Audio Looper

A simple 4-track audio looper for Raspberry Pi with GPIO button controls and LED feedback.

## Features

- 4-track looping with overdub support
- GPIO button controls for recording, playback, and track management
- LED indicators for track status
- USB audio card support
- Real-time audio processing with PyAudio

## Hardware Requirements

- Raspberry Pi (3B+ or later recommended)
- USB sound card
- 8 GPIO buttons (4 record, 4 play)
- 8 LEDs (4 record indicators, 4 play indicators)
- GPIO breadboard, jumper wires
- Audio cables and connectors

## Software Setup

### Quick Start

```bash
git clone https://github.com/richpant/raspi-looper.git
cd raspi-looper
bash setup.sh
```

### Manual Setup

1. **Update system packages:**
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure GPIO and audio:**
   ```bash
   python3 config.py
   ```

4. **Run the looper:**
   ```bash
   sudo python3 main.py
   ```

## Usage

### Controls

- **Record Button (Track):** Press to arm for recording, press again to stop
- **Play Button (Track):** Press to toggle mute/unmute
- **Hold Record:** Undo last overdub (while track playing)
- **Hold Play:** Clear track (while track muted)

### Starting a Session

1. Press Track 1 Record button to start recording
2. Press again to finish the initial loop
3. Use other tracks to overdub

## Configuration

Edit `config.py` to customize:

- GPIO pin assignments
- Audio device selection
- Buffer sizes and latency settings
- Track count and loop parameters

## Troubleshooting

- **Audio issues:** Run `alsamixer` to adjust levels
- **GPIO conflicts:** Check pin assignments in `config.py`
- **Latency problems:** Increase buffer size in `config.py`

## License

MIT
