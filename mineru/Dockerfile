FROM python:3.12-slim AS base

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    MINERU_DEVICE_MODE=cpu \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Initialize the project, then pin torch/torchvision to the PyTorch CPU
# index. Pinning via [tool.uv.sources] forces the CPU builds no matter what
# pulls torch in, so the huge nvidia-cuda-* wheels are never resolved even
# when mineru[core] re-resolves the dependency graph.
RUN uv init --python 3.12 && \
    cat >> pyproject.toml <<'EOF'

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = [{ index = "pytorch-cpu" }]
torchvision = [{ index = "pytorch-cpu" }]
EOF

# Resolve everything in a single pass so torch/torchvision honor the CPU pin.
RUN uv add torch torchvision "mineru[core]"

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
RUN rm -R ~/.cache/uv

# Expose port for API
EXPOSE 9987

# Default command
CMD ["uv", "run", "mineru-api", "--host", "0.0.0.0", "--port", "9987"]
