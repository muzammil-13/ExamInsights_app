FROM python:3.11-slim as builder

WORKDIR /tmp/build

# Install build dependencies and runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Ensure Python logs are pushed directly to the console without buffering
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/appuser/.local/bin:$PATH

# Install runtime dependencies only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy installed Python packages from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Create logs directory with proper ownership
RUN mkdir -p logs && chown -R appuser:appuser logs

EXPOSE 8000
EXPOSE 8501

USER appuser

# Use bash with `wait -n` to exit the container if either process crashes
CMD ["bash", "-c", "python app.py & streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501 & wait -n"]
