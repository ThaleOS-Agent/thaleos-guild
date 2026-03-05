# ThaleOS-Agent / thaleos-guild

Minimal, reproducible repo to bring back:

- **Guild API (FastAPI)** deployable to **Render**
- **Optional Electron Desktop shell** (local dev)
- **Cloudflare Tunnel (cloudflared)** config for secure exposure / named tunnel
- A small **Router** service that can proxy/route to UTILIX and/or Guild API

## Repo layout

```
api/                 # FastAPI service for Render
router/              # Lightweight routing/proxy (Node)
desktop/             # Optional Electron+React shell (local)
cloudflare/          # cloudflared tunnel configs (no secrets)
scripts/             # convenience scripts
render.yaml          # Render blueprint
```

---
## 1) Render deploy (recommended)

### A) Deploy via `render.yaml` Blueprint
1. Push this repo to GitHub as **ThaleOS-Agent/thaleos-guild**
2. In Render: **New + → Blueprint**, select the repo.
3. Render will create:
   - `thaleos-guild-api` (FastAPI)
   - `thaleos-guild-router` (Node)

### B) Required environment variables
Set these in Render (Dashboard → Service → Environment):

**API (`thaleos-guild-api`)**
- `ENV=prod`
- `ACTIONS_API_KEY=<strong-random-string>` (shared secret for internal calls)
- `CORS_ORIGINS=https://guild-console.thaleos.network,https://<your-pages-domain>`

**Router (`thaleos-guild-router`)**
- `ENV=prod`
- `ACTIONS_API_KEY=<same-as-api>`
- `UPSTREAM_UTILIX_URL=https://<your-utilix-service>/`  (or leave empty)
- `UPSTREAM_GUILD_API_URL=https://thaleos-guild-api.onrender.com/`

---
## 2) Cloudflare Tunnel (named tunnel)

This repo includes a **template** config:
- `cloudflare/config.yml` (no tunnel ID here)
- `cloudflare/ingress.yml`

### Steps (run on the machine that will host the tunnel)
1. Install cloudflared
2. Login: `cloudflared tunnel login`
3. Create tunnel: `cloudflared tunnel create thaleos-guild`
4. Add DNS record: `cloudflared tunnel route dns thaleos-guild guild-console.thaleos.network`
5. Save the tunnel credentials file where cloudflared expects it (usually `~/.cloudflared/<TUNNEL_ID>.json`)
6. Edit:
   - `cloudflare/config.yml` → set `tunnel: <TUNNEL_ID>`
   - `cloudflare/config.yml` → set `credentials-file: /Users/<you>/.cloudflared/<TUNNEL_ID>.json`
   - `cloudflare/ingress.yml` → set the upstream `service:` to your Render URL(s)
7. Run: `cloudflared tunnel run thaleos-guild`

---
## 3) Local dev

### API
```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8090
```

### Router
```bash
cd router
npm i
npm run dev
```

### Desktop (optional)
```bash
cd desktop
npm i
npm run test
```

---
## Security note (important)

Do **not** commit bearer tokens or API keys.
If you previously used a script that contained live tokens, rotate them immediately and only store secrets in Render/Cloudflare dashboards or a local `.env` file.
# thaleos-guild
