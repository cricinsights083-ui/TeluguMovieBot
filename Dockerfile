# Dockerfile

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Platform compatibility: Use Gunicorn for production and bind to dynamic $PORT
# We use GUNICORN_RUNNING=True to let bot.py know it shouldn't start its own Flask thread.
CMD ["sh", "-c", "python3 bot.py & GUNICORN_RUNNING=True gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 1 --timeout 120"]
