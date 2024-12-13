# Use the official Python image as the base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace

# Copy requirements.txt first for better caching
COPY requirements.txt .
COPY api api
COPY build build
COPY apple_share_price.csv .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Expose Jupyter port
EXPOSE 5000

# Default command
CMD ["python","api/serve_model.py"]

