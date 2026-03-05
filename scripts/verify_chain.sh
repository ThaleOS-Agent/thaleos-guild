#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-https://guild-console.thaleos.network}"

echo "== Health =="
curl -sS "$BASE/health" | cat
echo

echo "== Activate (spell router) =="
curl -sS -X POST "$BASE/activate" -H "content-type: application/json"   -d '{"spell":"Thaelia Awaken","payload":{"ping":true}}' | cat
echo
