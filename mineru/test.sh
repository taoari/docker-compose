#!/usr/bin/env bash
# Simple smoke test for the mineru-api service.
#
# Usage:
#   ./test.sh [PDF_FILE]
#
# If no PDF is given, a minimal sample document is downloaded automatically.
set -euo pipefail

HOST="${MINERU_HOST:-http://localhost:9987}"
PDF="${1:-minimal-document.pdf}"
OUT_DIR="${OUT_DIR:-./output}"

# Grab a sample PDF if the target file doesn't exist.
if [[ ! -f "$PDF" ]]; then
  echo "==> '$PDF' not found, downloading a sample PDF..."
  curl -fL -o "$PDF" \
    https://raw.githubusercontent.com/py-pdf/sample-files/main/001-trivial/minimal-document.pdf
fi

echo "==> Checking API is reachable at $HOST ..."
curl -fsS "$HOST/docs" >/dev/null \
  && echo "    OK: API responded." \
  || { echo "    ERROR: API not reachable at $HOST"; exit 1; }

mkdir -p "$OUT_DIR"

echo "==> Sending '$PDF' to $HOST/file_parse ..."
# mineru-api exposes POST /file_parse expecting multipart form field 'files'.
curl -fsS -X POST "$HOST/file_parse" \
  -H "accept: application/json" \
  -F "files=@${PDF};type=application/pdf" \
  -F "backend=pipeline" \
  -F "lang_list=ch" \
  -F "return_md=true" \
  -F "return_content_list=true" \
  -o "$OUT_DIR/response.json"

echo "==> Done. Response saved to $OUT_DIR/response.json"
echo "==> Preview (first 40 lines):"
head -c 4000 "$OUT_DIR/response.json"
echo
