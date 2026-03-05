#!/usr/bin/env bash
set -euo pipefail

echo "== ThaleOS Guild Local Bootstrap =="

(cd api && python3 -m venv .venv || true)
(cd api && source .venv/bin/activate && pip install -r requirements.txt)

(cd router && npm i)

echo ""
echo "Run in two terminals:"
echo "  (1) cd api && source .venv/bin/activate && uvicorn main:app --reload --port 8090"
echo "  (2) cd router && npm run dev"
