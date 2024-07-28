# Use the latest available version of Python 3.x slim variant
FROM python:latest

# Set the working directory to /bot
WORKDIR /bot

# Install git and envsubst
RUN apt-get update && apt-get install -y git gettext-base

# Clone the repository into the working directory
RUN git clone https://github.com/Marshall2HD/AeSBot.git .

# Copy the configuration sample file to /bot/
COPY config.toml.sample /bot/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Generate the config file and then run the bot
ENTRYPOINT ["/bin/sh", "-c", "envsubst < /bot/config.toml.sample > /bot/config.toml && python /bot/bot.py"]
