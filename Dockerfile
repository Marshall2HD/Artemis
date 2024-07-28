# Use the latest available version of Python 3.x slim variant
FROM python:latest

# Set the working directory to /bot
WORKDIR /bot

# Install git (required if you're cloning a repo)
RUN apt-get update && apt-get install -y git gettext-base

# Clone the repository into the working directory
RUN git clone https://github.com/Marshall2HD/AeSBot.git .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the initialization script and config template
COPY init-config.sh /bot/
COPY config.toml.sample /bot/

# Make sure the init script is executable
RUN chmod +x /bot/init-config.sh

# Run the initialization script and then start the Python script
CMD ["/bin/sh", "-c", "/bot/init-config.sh && python bot.py"]
