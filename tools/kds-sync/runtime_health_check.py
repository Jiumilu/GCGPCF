#!/usr/bin/env python3
"""Read-only runtime host health check for the project group (PG-11).

Probes a fixed list of local endpoints and reports up/down/latency.
Never starts, stops or modifies any service.

Usage:
  python3 tools/kds-sync/runtime_health_check.py
  python3 tools/kds-sync/runtime_health_check.py --json
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
TZ = timezone(timedelta(hours=8))

ENDPOINTS = [
    {"name": "hermes_api", "url": "http://127.0.0.1:8642/health", "owner": "Hermes", "required": True},
    {"name": "hermes_webui", "url": "http://127.0.0.1:8648/", "owner": "Hermes", "required": False},
    {"name": "gcmem_api", "url": "http://127.0.0.1:19090/stats", "owner": "GCMEM", "required": True},
    {"name": "startlux_api", "url": "http://127.0.0.1:18090/health", "owner": "StartLux", "required": False},
    {"name": "spaceai_bff", "url": "http://127.0.0.1:39010/healthz", "owner": "SpaceAI", "required": False},
    {"name": "spaceai_web", "url": "http://127.0.0.1:5273/", "owner": "SpaceAI", "required": False},
    {"name": "mmc_api", "url": "http://127.0.0.1:8080/api/mmc/v1/health", "owner": "MMC", "required": False},
    {"name": "next_server_3000", "url": "http://127.0.0.1:3000/", "owner": "unknown", "required": False},
    {"name": "docker_8000", "url": "http://127.0.0.1:8000/", "owner": "unknown", "required": False},
]


def port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def probe(url: str, timeout: float = 3.0) -> dict:
    start = time.monotonic()
    try:
        with urlopen(url, timeout=timeout) as resp:
            body = resp.read(400)
            return {
                "up": True,
                "status": resp.status,
                "latency_ms": int((time.monotonic() - start) * 1000),
                "body_prefix": body[:120].decode("utf-8", "replace"),
            }
    except (URLError, OSError, ValueError) as exc:
        return {
            "up": False,
            "status": None,
            "latency_ms": int((time.monotonic() - start) * 1000),
            "error": str(exc)[:160],
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    results = []
    for ep in ENDPOINTS:
        host = "127.0.0.1"
        port = int(ep["url"].split(":")[2].split("/")[0])
        reachable = port_open(host, port)
        r = probe(ep["url"]) if reachable else {"up": False, "status": None, "latency_ms": 0, "error": "port closed"}
        results.append({
            "name": ep["name"], "url": ep["url"], "owner": ep["owner"],
            "required": ep["required"], "port_open": reachable, **r,
        })
    ok = sum(1 for r in results if r["up"])
    required_ok = all(r["up"] for r in results if r["required"])
    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "endpoint_count": len(results),
        "up_count": ok,
        "down_count": len(results) - ok,
        "required_ok": required_ok,
        "results": results,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"runtime_health_check = {'pass' if required_ok else 'fail'}")
        print(f"up = {ok}/{len(results)}")
        for r in results:
            state = "UP" if r["up"] else "DOWN"
            flag = "required" if r["required"] else "optional"
            print(f"  [{state:4}] {r['name']:18} {flag:8} {r['url']} {r.get('error','')}")
    return 0 if required_ok else 1


if __name__ == "__main__":
    sys.exit(main())
