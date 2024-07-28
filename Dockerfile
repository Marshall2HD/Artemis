# Use the latest available version of Python 3.x slim variant
FROM python:latest

# Set the working directory to /discord-bot
WORKDIR /bot

# Install git (required if you're cloning a repo)
RUN apt-get update && apt-get install -y git

# Clone the repository into the working directory
RUN git clone https://github.com/Marshall2HD/AeSBot.git .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the Python script
CMD ["python", "bot.py"]
