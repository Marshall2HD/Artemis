#!/bin/sh

# Generate config.toml from the template using environment variables
if [ ! -f /data/config.toml ]; then
    echo "Generating config.toml from the template..."
    envsubst < /data/config.toml.sample > /data/config.toml
fi

# Execute the main application
exec python /app/bot.py
