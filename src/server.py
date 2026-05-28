import os
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 8787

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AGENT_TOKEN = os.environ.get("AGENT_TOKEN")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
SERVER_VERSION = os.environ.get("AGENT_SERVER_VERSION", "0.1.0")


def call_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    texts = []
    for item in result.get("output", []):
        for content in item.get("content", []):
            ctype = content.get("type")
            if ctype in ("output_text", "text"):
                texts.append(content.get("text", ""))

    if texts:
        return "\n".join(texts)

    return json.dumps(result, ensure_ascii=False)


def tail_file(path: str, max_bytes: int = 12000) -> str:
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - max_bytes), os.SEEK_SET)
            return f.read().decode("utf-8", errors="replace")
    except FileNotFoundError:
        return ""


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        if not AGENT_TOKEN:
            return False
        return self.headers.get("Authorization") == f"Bearer {AGENT_TOKEN}"

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "ok",
                "device": "iphone8-agent",
                "runtime": "python-stdlib",
                "model": OPENAI_MODEL,
                "version": SERVER_VERSION,
            })
            return

        if self.path == "/status":
            self._send_json(200, {
                "status": "ok",
                "device": "iphone8-agent",
                "model": OPENAI_MODEL,
                "version": SERVER_VERSION,
                "pid": os.getpid(),
                "cwd": os.getcwd(),
            })
            return

        if self.path == "/logs":
            if not self._authorized():
                self._send_json(401, {"error": "unauthorized"})
                return

            self._send_json(200, {
                "log": tail_file("/var/mobile/agent/agent.log"),
                "err": tail_file("/var/mobile/agent/agent.err"),
            })
            return

        self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/ask":
            self._send_json(404, {"error": "not found"})
            return

        if not self._authorized():
            self._send_json(401, {"error": "unauthorized"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))

            prompt = data.get("prompt", "")
            if not prompt:
                self._send_json(400, {"error": "missing prompt"})
                return

            answer = call_openai(prompt)
            self._send_json(200, {"answer": answer})

        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="ignore")
            self._send_json(500, {
                "error": "openai_http_error",
                "detail": detail,
            })
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def main():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"agent server listening on {HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
