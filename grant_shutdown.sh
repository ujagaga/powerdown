#!/bin/bash

# Script to grant NOPASSWD shutdown permission to the current user

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: This script must be run as root."
    exit 1
fi

# Define the sudoers file and content
SUDOERS_FILE="/etc/sudoers.d/shutdown_permission"
USER=$(whoami)  # Get the current user
SUDOERS_CONTENT="$USER ALL=(ALL) NOPASSWD: /sbin/shutdown"

# Create the sudoers file with appropriate permissions
if [ ! -f "$SUDOERS_FILE" ]; then
    echo "$SUDOERS_CONTENT" > "$SUDOERS_FILE"
    chmod 440 "$SUDOERS_FILE"
    echo "Sudoers file created successfully: $SUDOERS_FILE"
else
    echo "Sudoers file already exists: $SUDOERS_FILE"
fi

# Validate the sudoers file
visudo -cf "$SUDOERS_FILE"
if [ $? -ne 0 ]; then
    echo "Error: The sudoers file contains syntax errors. Please check it."
    rm "$SUDOERS_FILE"
    exit 1
fi

echo "Shutdown permission granted to $USER without a password."
