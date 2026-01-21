import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


ROLE = os.getenv("ROLE", "app")
SERVICE_NAME = os.getenv("SERVICE_NAME", "sandbox-service")
DEPENDENCY_URL = os.getenv("DEPENDENCY_URL", "")
LATENCY_MS = _env_int("LATENCY_MS", 0)
PORT = _env_int("PORT", 8000)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/health", "/request"):
            self.send_response(404)
            self.end_headers()
            return

        if LATENCY_MS > 0:
            time.sleep(LATENCY_MS / 1000.0)

        dependency_status = None
        if ROLE == "app" and DEPENDENCY_URL and self.path == "/request":
            target = DEPENDENCY_URL.rstrip("/") + "/request"
            try:
                with urlopen(target, timeout=2) as resp:
                    dependency_status = resp.status
            except Exception:
                dependency_status = "error"

        payload = {
            "service": SERVICE_NAME,
            "role": ROLE,
            "path": self.path,
            "dependency_status": dependency_status,
        }

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        message = fmt % args
        print(f"[{SERVICE_NAME}] {message}")


def main() -> None:
    server = HTTPServer(("", PORT), Handler)
    print(f"{SERVICE_NAME} listening on {PORT} as {ROLE}")
    server.serve_forever()


if __name__ == "__main__":
    main()
