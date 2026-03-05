#!/usr/bin/env bash
set -euo pipefail

TUNNEL_NAME="${1:-thaleos-guild}"
DOMAIN1="${2:-guild-console.thaleos.network}"
DOMAIN2="${3:-utilix-bridge.thaleos.network}"

command -v cloudflared >/dev/null 2>&1 || { echo "cloudflared not found"; exit 1; }

cloudflared tunnel login
cloudflared tunnel create "$TUNNEL_NAME"
cloudflared tunnel route dns "$TUNNEL_NAME" "$DOMAIN1"
cloudflared tunnel route dns "$TUNNEL_NAME" "$DOMAIN2" || true

echo "Edit cloudflare/config.yml with the printed tunnel ID + credentials path, then run:"
echo "cloudflared tunnel --config cloudflare/config.yml run"
