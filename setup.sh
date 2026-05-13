#!/bin/bash

# Installation script for Raspberry Pi Audio Looper
# Run with: bash setup.sh

set -e  # Exit on error

echo "========================================"
echo "Raspberry Pi Audio Looper Setup"
echo "========================================"

# Update system
echo "\n[1/5] Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
echo "\n[2/5] Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    libasound2-dev \
    portaudio19-dev \
    alsa-utils

# Install Python dependencies
echo "\n[3/5] Installing Python packages..."
pip install -r requirements.txt

# Create necessary directories
echo "\n[4/5] Creating application directories..."
mkdir -p logs
mkdir -p recordings

# Set permissions
echo "\n[5/5] Setting up permissions..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G audio $USER

echo "\n========================================"
echo "Setup complete!"
echo "========================================"
echo "\nNext steps:"
echo "1. Configure GPIO pins and audio device:"
echo "   python3 config.py"
echo "\n2. Test audio connections:"
echo "   alsamixer"
echo "\n3. Run the looper (requires sudo):"
echo "   sudo python3 main.py"
echo "\nTo start on boot, add to crontab:"
echo "   @reboot /usr/bin/sudo /usr/bin/python3 /path/to/main.py"
echo "========================================\n"
