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

# Install gettext-base for envsubst
RUN apt-get update && apt-get install -y gettext-base

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /data/
RUN chmod +x /data/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/data/entrypoint.sh"]

# Set the working directory to /app
WORKDIR /app

# Run the Python script
CMD ["python", "bot.py"]
