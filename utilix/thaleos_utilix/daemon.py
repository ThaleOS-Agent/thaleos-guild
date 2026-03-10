import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from thaleos_utilix.config import settings
from thaleos_utilix.heartbeat import heartbeat_loop

class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok", "service": "utilix", "id": settings.utilix_id})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/activate":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            payload = json.loads(raw.decode("utf-8") or "{}")

            # Placeholder: implement safe task execution here
            return self._send(200, {"accepted": True, "utilix_id": settings.utilix_id, "echo": payload})

        return self._send(404, {"error": "not found"})

def run_http():
    server = HTTPServer(("0.0.0.0", settings.utilix_port), Handler)
    server.serve_forever()

async def main():
    t = Thread(target=run_http, daemon=True)
    t.start()
    await heartbeat_loop()

if __name__ == "__main__":
    asyncio.run(main())