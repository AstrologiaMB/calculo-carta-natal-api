# Use Python 3.11 slim image based on Debian
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including sqlite3 library
RUN apt-get update && apt-get install -y \
    libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for Fly.io
EXPOSE 8001

# Run the application with Fly.io settings
CMD uvicorn app:app --host 0.0.0.0 --port 8001 --timeout-keep-alive 90 --access-log --log-level info
