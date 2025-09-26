# SIEM Log Analyzer Dockerfile
# Multi-stage build for optimized production image

# Build stage
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Copy source code
COPY src/ ./src/

# Install Python dependencies and build wheel
RUN pip install --no-cache-dir build && \
    python -m build

# Production stage
FROM python:3.11-slim as production

# Set metadata labels
LABEL maintainer="SIEM Log Analyzer Team" \
      org.opencontainers.image.title="SIEM Log Analyzer" \
      org.opencontainers.image.description="A modular Python framework for SIEM log analysis and security monitoring" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/Akhilkrishna1/siem-log-analyzer" \
      org.opencontainers.image.url="https://github.com/Akhilkrishna1/siem-log-analyzer" \
      org.opencontainers.image.documentation="https://github.com/Akhilkrishna1/siem-log-analyzer/wiki" \
      org.opencontainers.image.licenses="MIT"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r sieman && useradd -r -g sieman -s /bin/bash sieman

# Set working directory
WORKDIR /app

# Copy built wheel from builder stage
COPY --from=builder /build/dist/*.whl /tmp/

# Install the package
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Create necessary directories
RUN mkdir -p /app/logs /app/config /app/output && \
    chown -R sieman:sieman /app

# Copy configuration templates (if any)
# COPY config/ /app/config/

# Create volume mount points
VOLUME ["/app/logs", "/app/config", "/app/output"]

# Switch to non-root user
USER sieman

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    SIEMAN_CONFIG_PATH=/app/config \
    SIEMAN_LOG_PATH=/app/logs \
    SIEMAN_OUTPUT_PATH=/app/output

# Health check
HEALTHCHEK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sieman; print('Health check passed')" || exit 1

# Default command
CMD ["sieman", "--help"]

# Usage examples:
# Build: docker build -t sieman .
# Run: docker run -v /path/to/logs:/app/logs -v /path/to/config:/app/config -v /path/to/output:/app/output sieman analyze /app/logs/logfile.log
# Interactive: docker run -it -v /path/to/logs:/app/logs sieman bash
