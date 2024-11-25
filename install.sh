#!/bin/bash

# Script to create a virtual Python environment and install Flask

# Define variables
VENV_DIR="venv"
PYTHON_BIN="python3"  # Change to 'python' if Python 3 is the default or not explicitly named

# Check if Python is installed
if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "Error: $PYTHON_BIN is not installed. Please install Python 3."
    exit 1
fi

# Create the virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists in '$VENV_DIR'."
else
    echo "Creating virtual environment in '$VENV_DIR'..."
    $PYTHON_BIN -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
    echo "Virtual environment created successfully."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Error: Failed to upgrade pip."
    deactivate
    exit 1
fi

# Install Flask
echo "Installing Flask..."
pip install flask netifaces
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Flask."
    deactivate
    exit 1
fi

echo "Flask installed successfully."

# Deactivate the virtual environment
deactivate

echo "Setup completed. To activate the virtual environment, use:"
echo "source $VENV_DIR/bin/activate"

sudo ./grant_shutdown.sh
