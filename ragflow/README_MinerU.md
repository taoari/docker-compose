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
    ./ragflow-uv-tools:/ragflow/uv-tools
```

```bash
# test mineru
curl -L -o minimal-document.pdf https://raw.githubusercontent.com/py-pdf/sample-files/main/001-trivial/minimal-document.pdf
mineru -p minimal-document.pdf -o output_dir
```

