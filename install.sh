#!/bin/bash

set -e  # Exit on errors

echo "Checking for Ollama..."
if ! command -v ollama &>/dev/null; then
    echo "Ollama not found. Installing via curl..."
    curl -fsSL https://ollama.com/install.sh | sudo sh
else
    echo "Ollama is already installed."
fi

echo "Installing Python dependencies..."
sudo pip install . --break-system-package --root-user-action ignore

echo "Installation complete. futa has been set up!"

