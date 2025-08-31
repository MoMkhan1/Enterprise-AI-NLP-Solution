# Use an official slim Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory to the project root
WORKDIR /app

# Install system dependencies required for psycopg2 and NLP packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        build-essential \
        curl \
        libffi-dev \
        libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the project into the container at /app
COPY . /app

# Ensure kafka-python is installed even if missing in requirements.txt
RUN pip install --no-cache-dir kafka-python

# Default command to run the loader script
CMD ["python", "src/database/postgres_loader.py"]
