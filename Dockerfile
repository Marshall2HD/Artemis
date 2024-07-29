# Use the latest available version of Python
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

# Install gettext for envsubst command
RUN apt-get update && apt-get install -y gettext-base

# Copy the startup script
COPY start.sh /usr/local/bin/start.sh

# Set the working directory to /app
WORKDIR /app

# Use the startup script to set up the config and run the application
CMD ["/usr/local/bin/start.sh"]
