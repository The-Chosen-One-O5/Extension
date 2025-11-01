#!/bin/bash

echo "Starting Telegram Voice Bot..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

# Create temp directory if it doesn't exist
mkdir -p temp_audio

# Run the bot
python main.py
