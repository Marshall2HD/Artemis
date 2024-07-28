#!/bin/sh

# Replace placeholders in config.toml.sample with environment variable values
envsubst < /bot/config.toml.sample > /bot/config.toml