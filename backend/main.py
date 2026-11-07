"""Backend mẫu (Python, chỉ dùng thư viện chuẩn): đọc PORT và DATABASE_URL từ biến môi trường."""
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

PORT = int(os.getenv("PORT", "8000"))


def check_db():
    raw = os.getenv("DATABASE_URL")
    if not raw:
        return {"configured": False}
    u = urlparse(raw)
    try:
        socket.create_connection((u.hostname, u.port or 5432), timeout=2).close()
        return {"configured": True, "reachable": True}
    except OSError:
        return {"configured": True, "reachable": False}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/api/health": lambda: {"status": "ok"},
            "/api/hello": lambda: {"message": "Xin chào từ backend Python", "runtime": "python"},
            "/api/db": check_db,
        }
        fn = routes.get(self.path)
        self.send_response(200 if fn else 404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(fn() if fn else {"error": "not found"}).encode())


if __name__ == "__main__":
    print(f"listening on {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
