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

# Replace placeholders in config.toml.sample with environment variable values
RUN apt-get update && apt-get install -y gettext-base && \
    envsubst < /data/config.toml.sample > /data/config.toml

# Set the working directory to /app
WORKDIR /app

# Run the Python script
CMD ["python", "bot.py"]
