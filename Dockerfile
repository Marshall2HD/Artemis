# Use the latest available version of Alpine Python
FROM python:alpine

# Install Python dependencies
RUN pip install --no-cache-dir discord

# Copy the rest of the application files
COPY bot.py /app/

# Set the working directory to /app
WORKDIR /app

# Run the Python script
CMD ["python", "bot.py"]