## Cloudflare named tunnel setup

cloudflared tunnel login
cloudflared tunnel create thaleos-guild

# DNS routes
cloudflared tunnel route dns thaleos-guild guild-console.thaleos.network
cloudflared tunnel route dns thaleos-guild utilix-bridge.thaleos.network

# Run (after editing cloudflare/config.yml)
cloudflared tunnel --config cloudflare/config.yml run
