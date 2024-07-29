#!/bin/sh

# Replace placeholders in config.toml.sample with environment variable values
envsubst < /data/config.toml.sample > /data/config.toml

# Execute the Python script
exec python bot.py
