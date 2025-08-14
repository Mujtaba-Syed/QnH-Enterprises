# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        libpq-dev \
        python3-dev \
        libffi-dev \
        libssl-dev \
        dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy project
COPY . .

# Create media directory
RUN mkdir -p /app/core/media

# Convert line endings and make scripts executable
RUN find . -name "*.sh" -exec dos2unix {} \; && \
    find . -name "*.py" -exec dos2unix {} \; && \
    chmod +x scripts/start.sh scripts/start-dev.sh && \
    ls -la scripts/

# Make port 8000 available
EXPOSE 8000

# Run the application (default to development)
CMD ["/bin/bash", "scripts/start.sh"]