# Use the latest Python 3.x slim variant
FROM python:latest

# Create the /data directory for configuration and application files
RUN mkdir /data

# Set the working directory for configuration files
WORKDIR /data

# Copy and install Python dependencies
COPY requirements.txt /data/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and configuration template
COPY bot.py /app/
COPY config.toml.sample /data/

# Install gettext-base for envsubst
RUN apt-get update && apt-get install -y gettext-base

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /data/
RUN chmod +x /data/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/data/entrypoint.sh"]
