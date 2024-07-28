#!/bin/sh

# Replace placeholders in config.toml.sample with environment variable values
envsubst < /config.toml.sample > /config.toml
