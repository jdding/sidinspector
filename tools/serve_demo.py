#!/usr/bin/env python3
"""Run SIDInspector's diagnostic workbench through an isolated local HTTP interface."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sidinspector.pure_diagnostics import (  # noqa: E402
    parse_interactions_csv_text,
    parse_metadata_csv_text,
    parse_sid_csv_text,
    run_mapping_diagnostics,
)


def metadata() -> dict[str, str]:
    state = json.loads((ROOT / "RELEASE_STATUS.json").read_text(encoding="utf-8"))
    return {
        key: state[key]
        for key in ("version", "publication_status", "paper_doi", "scientific_reproduction_status")
    }


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_isolated_workflow() -> dict:
    started = time.monotonic()
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="sidinspector-local-demo-") as folder:
        work = Path(folder)
        verified_count = 0
        for row in manifest["files"]:
            relative = Path(row["path"])
            source = (ROOT / relative).resolve()
            if relative.is_absolute() or ".." in relative.parts or ROOT not in source.parents:
                raise ValueError("invalid manifest member")
            if _sha256_file(source) != row["sha256"]:
                raise ValueError(f"SHA-256 mismatch for {row['path']}")
            target = work / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            verified_count += 1

        for meta_name in ("PACKAGE_MANIFEST.json", "CHECKSUMS.sha256"):
            shutil.copy2(ROOT / meta_name, work / meta_name)

        proc = subprocess.Popen(
            [sys.executable, "-I", "-B", str(work / "demo" / "browser_example.py")],
            cwd=work,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
            raise RuntimeError("workflow timed out") from None
        if proc.returncode:
            raise RuntimeError(f"workflow failed: {stderr.strip()}")
        demo_payload = json.loads(stdout)

        return {
            **demo_payload,
            "isolated_run": True,
            "manifest_files_verified": verified_count,
            "run_id": secrets.token_hex(6),
            "metadata": metadata(),
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return

    def reply(self, status: int, value: object, content_type: str = "application/json; charset=utf-8", nonce: str | None = None) -> None:
        body = (
            json.dumps(value, allow_nan=False).encode("utf-8")
            if content_type.startswith("application/json")
            else value
        )
        assert isinstance(body, bytes)
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; "
            "frame-ancestors 'none'; form-action 'none'; script-src 'nonce-" + (nonce or "") + "'",
        )
        self.end_headers()
        self.wfile.write(body)

    def allowed_host(self) -> bool:
        try:
            host = urlsplit("//" + self.headers.get("Host", "")).hostname
        except ValueError:
            return False
        return self.server.bind_host != "127.0.0.1" or host in {"127.0.0.1", "localhost"}

    def _valid_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        parsed = urlsplit(origin)
        return parsed.scheme in {"http", "https"} and parsed.netloc == self.headers.get("Host")

    def do_GET(self) -> None:
        if not self.allowed_host():
            return self.reply(403, {"error": "Host is not allowed"})
        if self.path == "/health":
            return self.reply(200, {"status": "ready", **metadata()})
        if self.path == "/":
            nonce = secrets.token_urlsafe(18)
            body = (
                (ROOT / "demo" / "local.html")
                .read_text(encoding="utf-8")
                .replace("__SCRIPT_NONCE__", nonce)
                .encode("utf-8")
            )
            return self.reply(200, body, "text/html; charset=utf-8", nonce)
        self.reply(404, {"error": "Route not found"})

    def do_POST(self) -> None:
        if not self.allowed_host():
            return self.reply(403, {"error": "Host is not allowed"})
        if not self._valid_origin():
            return self.reply(403, {"error": "Origin is not allowed"})
        if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
            return self.reply(415, {"error": "Content-Type must be application/json"})

        if self.path == "/api/run":
            try:
                size = int(self.headers.get("Content-Length", "-1"))
                if not 0 < size <= 64:
                    return self.reply(413, {"error": "Request body size is not allowed"})
                if json.loads(self.rfile.read(size)) != {}:
                    return self.reply(400, {"error": "Only an empty JSON object is accepted"})
            except (ValueError, json.JSONDecodeError):
                return self.reply(400, {"error": "Invalid JSON request"})
            if not self.server.workflow_lock.acquire(blocking=False):
                return self.reply(429, {"error": "A workflow run is already active"})
            try:
                result = run_isolated_workflow()
            except Exception as exc:
                self.reply(500, {"error": f"Local workflow failed: {exc}"})
            else:
                self.reply(200, result)
            finally:
                self.server.workflow_lock.release()
            return

        if self.path == "/api/audit":
            try:
                size = int(self.headers.get("Content-Length", "-1"))
                if not 0 < size <= 2_000_000:
                    return self.reply(413, {"error": "CSV payload exceeds 2 MB local demo limit"})
                body = json.loads(self.rfile.read(size))
                sid_parsed = parse_sid_csv_text(str(body.get("sid_csv", "")))
                inter_text = str(body.get("interactions_csv", ""))
                meta_text = str(body.get("metadata_csv", ""))
                interactions = parse_interactions_csv_text(inter_text) if inter_text.strip() else []
                metadata_map = parse_metadata_csv_text(meta_text) if meta_text.strip() else {}
                report = run_mapping_diagnostics(sid_parsed["rows"], interactions=interactions, metadata=metadata_map)
            except (ValueError, json.JSONDecodeError) as exc:
                return self.reply(400, {"error": str(exc)})
            return self.reply(200, {"status": "pass", "report": report})

        self.reply(404, {"error": "Route not found"})

    def do_PUT(self) -> None:
        self.reply(405, {"error": "Method not allowed"})

    do_DELETE = do_PATCH = do_OPTIONS = do_PUT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.bind_host = args.host
    server.workflow_lock = threading.Lock()
    print(f"DEMO_READY http://{args.host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
