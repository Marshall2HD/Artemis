#!/bin/sh
# entrypoint.sh

# Use envsubst to substitute environment variables into config.toml
if [ ! -f /data/config.toml ]; then
    echo "Generating config.toml from the template..."
    envsubst < /data/config.toml.sample > /data/config.toml
fi

# Start the main application
exec python /app/bot.py
