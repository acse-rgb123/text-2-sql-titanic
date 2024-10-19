#!/bin/bash

# Function to check if a Python package is installed, and install it if not
install_if_not_installed() {
    PACKAGE=$1
    if ! pip show "$PACKAGE" &> /dev/null; then
        echo "Installing $PACKAGE..."
        pip install "$PACKAGE"
    else
        echo "$PACKAGE is already installed."
    fi
}

# Install required Python packages
echo "Checking and installing dependencies..."
install_if_not_installed openai
install_if_not_installed faiss-cpu
install_if_not_installed numpy
install_if_not_installed sqlite3  # sqlite3 should be included with Python by default, but just in case

# Set executable permission for run.sh
chmod +x run.sh

# Set OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Please provide your OpenAI API Key:"
    read -s OPENAI_API_KEY
    export OPENAI_API_KEY="$OPENAI_API_KEY"
fi

# Run the Python script
echo "Running main.py..."
python main.py
