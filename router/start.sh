#!/usr/bin/env bash
set -euo pipefail
P="${PORT:-10000}"
if [[ "$P" == \$* ]]; then P="10000"; fi
exec uvicorn main:app --host 0.0.0.0 --port "$P"