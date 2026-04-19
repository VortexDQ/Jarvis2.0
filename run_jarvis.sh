#!/bin/bash
# Jarvis AI Assistant - Linux/macOS Launcher

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

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
        echo "Warning: Unsupported OS. Attempting to continue..."
        ;;
esac

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Error: Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not available"
    exit 1
fi

# Run Jarvis
echo "Starting Jarvis AI Assistant on $OS..."
echo ""
python -m jarvis_app

# Keep terminal open if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Jarvis exited with an error. See above for details."
    echo "Press Enter to close this window..."
    read
fi
