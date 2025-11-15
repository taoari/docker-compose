# RagFlow MinerU Notes

## Approach 1: Create a new RagFlow image with MinerU included

```dockerfile
# Dockerfile
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
```

```yaml
# docker-compose.yml
# Comment out image, and add build
services:
  ragflow:
    # image: ${RAGFLOW_IMAGE}
    build:
      context: .
      dockerfile: Dockerfile
```

```bash
# .env
HF_ENDPOINT=https://huggingface.co
MINERU_EXECUTABLE=/ragflow/uv_tools/.venv/bin/mineru
```

```bash
docker compose build
```

## Approach 2: Hack in container

https://github.com/infiniflow/ragflow/blob/main/docs/faq.mdx#how-to-use-mineru-to-parse-pdf-documents

```bash
# .env
HF_ENDPOINT=https://huggingface.co
MINERU_EXECUTABLE=/ragflow/uv_tools/.venv/bin/mineru
```

```bash
# setup_mineru.sh
mkdir uv_tools
cd uv_tools
uv venv .venv
. .venv/bin/activate
# force install pytorch CPU version
uv pip install --no-config torch torchvision --index-url https://download.pytorch.org/whl/cpu 
uv pip install --no-config "mineru[core]"
```

```yaml
# docker-compose.yaml
volumes:
    ./ragflow-uv-tools:/ragflow/uv_tools
```

```bash
# test mineru
curl -L -o minimal-document.pdf https://raw.githubusercontent.com/py-pdf/sample-files/main/001-trivial/minimal-document.pdf
mineru -p minimal-document.pdf -o output_dir
```

