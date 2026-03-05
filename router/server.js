import express from "express";
import fetch from "node-fetch";
import { createProxyMiddleware } from "http-proxy-middleware";

const app = express();
app.use(express.json({ limit: "2mb" }));

const ENV = process.env.ENV || "local";
const ACTIONS_API_KEY = process.env.ACTIONS_API_KEY || "dev-actions-key";
const UPSTREAM_GUILD_API_URL = (process.env.UPSTREAM_GUILD_API_URL || "http://127.0.0.1:8090").replace(/\/$/, "");
const UPSTREAM_UTILIX_URL = (process.env.UPSTREAM_UTILIX_URL || "").replace(/\/$/, "");

app.get("/health", (_req, res) => res.json({ ok: true, env: ENV }));

// Proxy the OpenAPI file
app.use(
  "/.well-known/openapi.json",
  createProxyMiddleware({
    target: UPSTREAM_GUILD_API_URL,
    changeOrigin: true,
    pathRewrite: { "^/\.well-known/openapi\.json": "/.well-known/openapi.json" }
  })
);

// Unified activation endpoint
// POST /activate { spell, payload }
app.post("/activate", async (req, res) => {
  const { spell = "", payload = {} } = req.body || {};
  const body = { spell, payload, source: "router" };

  // Prefer UTILIX if configured + spell suggests it; else Guild API
  const wantsUtilix = !!UPSTREAM_UTILIX_URL && /utilix|scan|repair|orchestr|harmonic/i.test(String(spell));
  const target = wantsUtilix ? UPSTREAM_UTILIX_URL : UPSTREAM_GUILD_API_URL;

  try {
    const r = await fetch(`${target}/activate`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-actions-key": ACTIONS_API_KEY
      },
      body: JSON.stringify(body)
    });

    const text = await r.text();
    let json;
    try { json = JSON.parse(text); } catch { json = { raw: text }; }

    res.status(r.status).json({
      matched: true,
      upstream: wantsUtilix ? "utilix" : "guild-api",
      status_code: r.status,
      body: json
    });
  } catch (e) {
    res.status(502).json({ ok: false, error: String(e), upstream: target });
  }
});

// Optional: Proxy everything under /guild/* to Guild API
app.use(
  "/guild",
  createProxyMiddleware({
    target: UPSTREAM_GUILD_API_URL,
    changeOrigin: true,
    pathRewrite: { "^/guild": "" }
  })
);

const port = process.env.PORT || 8001;
app.listen(port, () => console.log(`Router listening on :${port} env=${ENV}`));
