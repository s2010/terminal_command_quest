#!/bin/bash
# Terminal Command Quest - Wrapper Script

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required but not installed."
    echo "Please install Python 3.7+ and try again."
    exit 1
fi

# Check if quest.py exists
if [ ! -f "quest.py" ]; then
    echo "[ERROR] quest.py not found in current directory"
    echo "Please run this script from the Terminal Command Quest directory."
    exit 1
fi

# Install requirements if needed
if [ -f "requirements.txt" ] && [ ! -d "venv" ]; then
    echo "[SETUP] Setting up Python environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "[SUCCESS] Environment setup complete!"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the quest
echo "[QUEST] Starting Terminal Command Quest..."
python3 quest.py play "$@"