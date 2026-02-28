FROM python:3.9-slim-bullseye

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies (curl for health check, git for setup.py if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy application code first (needed for setup.py)
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Create necessary directories with proper permissions
RUN mkdir -p logs artifacts prediction_artifacts && \
    chmod -R 755 logs artifacts prediction_artifacts

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check - lenient to allow startup time
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8080/health || exit 0

# Run with gunicorn for production
CMD ["gunicorn", \
     "--workers=2", \
     "--threads=2", \
     "--worker-class=gthread", \
     "--bind=0.0.0.0:8080", \
     "--timeout=120", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--log-level=info", \
     "app:app"]