FROM python:3.9-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code first (needed for setup.py)
COPY . /app

# Copy requirements 
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p logs artifacts

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--workers", "2", "--threads", "2", "--worker-class", "gthread", "--bind", "0.0.0.0:8080", "--timeout", "120", "app:app"]