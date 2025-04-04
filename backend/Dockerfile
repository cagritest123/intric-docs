FROM python:3.10-slim-bullseye@sha256:56d670145c65f0d341b4af60944ba5bf416fc3fc06f4e25f01342172ac96f750 as builder

# Install system dependencies required for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry==1.6.1

# Set workdir
WORKDIR /app

# Copy only pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies (without installing the project itself)
RUN poetry install --no-root --no-interaction --no-ansi --only main

# Final image
FROM python:3.10-slim-bullseye@sha256:56d670145c65f0d341b4af60944ba5bf416fc3fc06f4e25f01342172ac96f750

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libmagic1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Create data directory with proper permissions
RUN mkdir -p /app/data && chmod 777 /app/data

# Create a non-root user to run the application
RUN groupadd -r intric && \
    useradd -r -g intric -d /app -s /bin/bash intric && \
    chown -R intric:intric /app

USER intric

# Expose port
EXPOSE 8123

# Command to run the application (using exec form as recommended)
CMD ["poetry", "run", "uvicorn", "intric.server.main:app", "--host", "0.0.0.0", "--port", "8123"]