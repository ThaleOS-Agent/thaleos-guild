# Cloudflare Tunnel templates (no secrets)

Files:
- `config.yml`   → point at your tunnel ID + credentials file path
- `ingress.yml`  → hostname routing rules (edit upstream services)

Typical use:
```bash
cloudflared tunnel --config cloudflare/config.yml run
```
