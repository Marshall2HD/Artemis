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
COPY start.py /app/

# Set the working directory to /app
WORKDIR /app

# Use the combined Python script to generate config and run the application
CMD ["python", "start.py"]
