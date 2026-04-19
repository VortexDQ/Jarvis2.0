#!/bin/bash
# Jarvis AI Assistant - Linux/macOS Setup Script
# Makes Jarvis ready to use on Unix-like systems

set -e

echo ""
echo "========================================"
echo "   Jarvis AI Assistant - Setup"
echo "========================================"
echo ""

# Detect OS
OS_TYPE=$(uname -s)
case "$OS_TYPE" in
    Linux*)
        OS="Linux"
        ;;
    Darwin*)
        OS="macOS"
        ;;
    *)
        OS="Unknown"
        echo "Warning: Unsupported OS detected. Setup may not work correctly."
        ;;
esac

echo "Detected OS: $OS"
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python found: $PYTHON_VERSION"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create virtual environment
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo ""
echo "Installing required packages..."
echo "This may take a few minutes..."
echo ""

pip install -q \
    slint \
    vosk \
    sounddevice \
    pyttsx3 \
    requests \
    pyyaml

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ All dependencies installed successfully"
else
    echo ""
    echo "Warning: Some packages failed to install"
    echo "You may need to install them manually"
fi

echo ""
echo "========================================"
echo "   Installation Complete!"
echo "========================================"
echo ""
echo "To start using Jarvis:"
echo ""
echo "  1. Activate the environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run Jarvis:"
echo "     python -m jarvis_app"
echo ""
echo "To deactivate the environment later:"
echo "  deactivate"
echo ""
echo "For more information, see: README.md"
echo ""
