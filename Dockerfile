# VoidSight Analytics - Production Dockerfile
# Multi-stage build for optimized production deployment

# Stage 1: Build Stage
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_ENV=production
ARG VERSION=3.0.0

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better layer caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Stage 2: Production Stage
FROM python:3.11-slim as production

# Set metadata labels
LABEL maintainer="Infinex Analytics <support@infinex.dev>"
LABEL version="3.0.0"
LABEL description="Enterprise ROI Calculator - Production Ready"
LABEL org.opencontainers.image.source="https://github.com/bullsbears682/AppM"
LABEL org.opencontainers.image.documentation="https://docs.infinex.dev"
LABEL org.opencontainers.image.vendor="Infinex Analytics"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_ENV=production \
    FLASK_APP=app.py \
    PORT=5000 \
    WORKERS=4 \
    TIMEOUT=120 \
    MAX_REQUESTS=1000 \
    MAX_REQUESTS_JITTER=50

# Create application user
RUN groupadd -r infinex && useradd -r -g infinex infinex

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    libxml2 \
    libxslt1.1 \
    libjpeg62-turbo \
    libpng16-16 \
    zlib1g \
    curl \
    nginx \
    supervisor \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create application directories
RUN mkdir -p /app /app/logs /app/uploads /app/static /app/instance \
    && chown -R infinex:infinex /app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=infinex:infinex . /app/

# Copy configuration files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/redis.conf /etc/redis/redis.conf

# Create startup script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create health check script
COPY docker/healthcheck.py /healthcheck.py
RUN chmod +x /healthcheck.py

# Set proper permissions
RUN chown -R infinex:infinex /app && \
    chmod -R 755 /app && \
    chmod 644 /app/*.py

# Expose ports
EXPOSE 80 5000 6379

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python /healthcheck.py || exit 1

# Switch to non-root user
USER infinex

# Entry point
ENTRYPOINT ["/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# Stage 3: Development Stage (Optional)
FROM production as development

# Switch back to root for development tools
USER root

# Install development dependencies
RUN pip install --no-cache-dir \
    flask-debugtoolbar \
    pytest \
    pytest-flask \
    pytest-cov \
    black \
    flake8 \
    mypy

# Set development environment
ENV FLASK_ENV=development \
    FLASK_DEBUG=1

# Development command
CMD ["python", "app.py"]

# Stage 4: Testing Stage (Optional)
FROM builder as testing

# Copy test files
COPY tests/ /app/tests/
COPY pytest.ini /app/

# Run tests
RUN python -m pytest tests/ --cov=app --cov-report=xml --cov-report=html

# Stage 5: Security Scanning (Optional)
FROM production as security

# Install security scanning tools
USER root
RUN pip install --no-cache-dir safety bandit

# Run security scans
RUN safety check && \
    bandit -r /app -f json -o /app/security-report.json || true

USER infinex