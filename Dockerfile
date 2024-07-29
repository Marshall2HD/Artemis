# Use the latest available version of Python 3.x slim variant
FROM python:latest

# Create the /data directory
RUN mkdir /data

# Set the working directory to /data
WORKDIR /data

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY bot.py /app/
COPY config.toml.sample /data/
COPY generate_config.py /app/
COPY start.sh /app/

# Install gettext for envsubst command (optional, if you want to keep this for other purposes)
RUN apt-get update && apt-get install -y gettext-base

# Ensure the startup script and Python script are executable
RUN chmod +x /app/start.sh /app/generate_config.py

# Set the working directory to /app
WORKDIR /app

# Use the startup script to set up the config and run the application
CMD ["./start.sh"]
