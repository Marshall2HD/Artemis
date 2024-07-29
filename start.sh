#!/bin/sh

# Generate config.toml from the sample using Python
python /app/generate_config.py

# Check if config.toml was created
if [ -f /data/config.toml ]; then
    echo "DEBUG: config.toml created successfully."
else
    echo "DEBUG: Failed to create config.toml."
fi

# Execute the Python script
exec python bot.py
