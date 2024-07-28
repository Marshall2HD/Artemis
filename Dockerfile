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

# Run the initialization script and then start the Python script
CMD ["/bin/sh", "-c", "init-config.sh && python bot.py"]
