#!/usr/bin/env bash
set -euo pipefail

API="${THALEOS_API_URL:-http://localhost:8080}"
echo "Testing API health: $API/health"
curl -fsS "$API/health" | cat
echo
echo "Listing agents: $API/registry/agents"
curl -fsS "$API/registry/agents" | cat
echo
echo "OK"