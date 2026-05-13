#!/bin/bash

# Installation script for Raspberry Pi Audio Looper
# Run with: bash setup.sh

set -e  # Exit on error

echo "========================================"
echo "Raspberry Pi Audio Looper Setup"
echo "========================================"

# Update system
echo ""
echo "[1/6] Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
echo ""
echo "[2/6] Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    libasound2-dev \
    portaudio19-dev \
    alsa-utils

# Create virtual environment
echo ""
echo "[3/6] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo ""
echo "[4/6] Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "[5/6] Creating application directories..."
mkdir -p logs
mkdir -p recordings

# Set permissions
echo ""
echo "[6/6] Setting up permissions..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G audio $USER

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Configure GPIO pins and audio device:"
echo "   python3 config.py"
echo ""
echo "3. Test audio connections:"
echo "   alsamixer"
echo ""
echo "4. Run the looper (requires sudo):"
echo "   sudo venv/bin/python3 main.py"
echo ""
echo "To start on boot, add to crontab (sudo crontab -e):"
echo "   @reboot cd /home/\$(whoami)/raspi-looper && source venv/bin/activate && sudo venv/bin/python3 main.py"
echo ""
echo "========================================"
echo ""
