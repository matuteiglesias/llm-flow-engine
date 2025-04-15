# Dockerfile

FROM python:3.11-slim

# System settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
 && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy source code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Default CMD can be overridden when running
CMD ["scripts/prod_start.sh"]
