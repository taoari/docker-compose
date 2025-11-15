FROM infiniflow/ragflow:v0.21.1-slim

RUN mkdir -p /ragflow/uv_tools
WORKDIR /ragflow/uv_tools

# Create venv and install CPU-only PyTorch + mineru[core]
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install --no-config torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache && \
    uv pip install --no-config "mineru[core]" --no-cache

# Download a sample PDF and trigger MinerU to download models
RUN curl -L -o minimal-document.pdf https://raw.githubusercontent.com/py-pdf/sample-files/main/001-trivial/minimal-document.pdf && \
    . .venv/bin/activate && \
    mineru -p minimal-document.pdf -o output_dir || true

WORKDIR /ragflow
