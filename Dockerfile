# Use the latest available version of Python 3.x slim variant
FROM python:latest

# Set the working directory to /bot
WORKDIR /bot

# Install git and envsubst
RUN apt-get update && apt-get install -y git gettext-base

# Clone the repository into a temporary directory
RUN git clone https://github.com/Marshall2HD/AeSBot.git /tmp/repo

# Copy the contents of the cloned repository to /bot
RUN cp -r /tmp/repo/* /bot/

# Remove the temporary directory
RUN rm -rf /tmp/repo

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Replace placeholders in config.toml.sample with environment variable values
RUN envsubst < config.toml.sample > config.toml

# Run the Python script
CMD ["python", "bot.py"]
