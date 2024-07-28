# Stage 1: Build the image with the repository content
FROM python:latest AS build

# Set the working directory to /bot
WORKDIR /bot

# Install git and envsubst
RUN apt-get update && apt-get install -y git gettext-base

# Clone the repository into the working directory
RUN git clone https://github.com/Marshall2HD/AeSBot.git .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Replace placeholders in config.toml.sample with environment variable values
RUN envsubst < config.toml.sample > config.toml

# Stage 2: Final image to run the bot
FROM python:latest

# Set the working directory to /bot
WORKDIR /bot

# Copy the files from the build stage
COPY --from=build /bot /bot

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "bot.py"]
