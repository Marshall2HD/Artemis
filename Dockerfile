# Use the latest available version of Python 3.x slim variant
FROM python:latest

# Create the /data directory
RUN mkdir /data

# Set the working directory to /data
WORKDIR /data

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create /app directory
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Clone the repository into /app
RUN git clone https://github.com/Marshall2HD/AeSBot.git .

# Move bot.py to /app
RUN mv /app/AeSBot/bot.py /app/

# Remove the now empty /app/AeSBot directory
RUN rm -rf /app/AeSBot

# Copy configuration file and replace placeholders
COPY config.toml.sample /data/
RUN apt-get update && apt-get install -y gettext-base && \
    envsubst < /data/config.toml.sample > /data/config.toml

# Set the working directory to /app
WORKDIR /app

# Run the Python script
CMD ["python", "bot.py"]
