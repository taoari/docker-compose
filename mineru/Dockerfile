FROM python:3.12-slim AS base

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Initialize and install dependencies
RUN uv init --python 3.12 && \
    uv add "mineru[core]"

# Install dependencies required by mineru and OpenCV/PyMuPDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Download a test file
RUN curl -L -o minimal-document.pdf https://raw.githubusercontent.com/py-pdf/sample-files/main/001-trivial/minimal-document.pdf

# Run a test conversion at build time (optional, for verification)
RUN uv run mineru -p minimal-document.pdf -o ./output

# Expose port for API
EXPOSE 9987

# Default command
CMD ["uv", "run", "mineru-api", "--host", "0.0.0.0", "--port", "9987"]
