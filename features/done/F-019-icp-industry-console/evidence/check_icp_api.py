#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-019 ICP 一期只读 API 本地探针（可复算证据生成器）。

用途
    在 `GlobalCloud ICP` 仓启动 `gc_icp.api:app`（默认 127.0.0.1:8091），
    对一期只读面的 5 个 GET 端点 + CORS/OPTIONS 做真实 HTTP 探活，断言
    候选态边界（candidate / partial / human_required / productionReady=false）。

边界（重要）
    本脚本只访问 127.0.0.1 的本地候选运行时；不做任何真实外部 API、
    真实 KDS API、真实业务源调用；不写任何业务数据；不提升任何状态。
    脚本内 `--check-only` 表示"只探测、不写证据文件"（= 只读检查）。
    如需落盘证据，显式 `--out <path>`。

用法
    # 只读检查（GPCF 证据门禁 verification.api 使用此形式）
    python3 features/active/F-019-icp-industry-console/evidence/check_icp_api.py --check-only

    # 落盘 JSON 证据
    python3 features/active/F-019-icp-industry-console/evidence/check_icp_api.py \
        --out features/active/F-019-icp-industry-console/evidence/api-evidence-20261022.json
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8091
READY_TIMEOUT_SECONDS = 40.0
READY_INTERVAL_SECONDS = 0.25
HTTP_TIMEOUT_SECONDS = 8.0


def find_icp_repo() -> Path:
    # 本文件位于 <workspace>/GlobalCoud GPCF/features/active/F-019-.../evidence/
    workspace = Path(__file__).resolve().parents[5]
    repo = workspace / "GlobalCloud ICP"
    if not (repo / "src" / "gc_icp" / "api.py").exists():
        raise SystemExit("FAIL: 未找到 GlobalCloud ICP 仓: %s" % repo)
    return repo


def port_is_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex((host, port)) == 0


def http_request(method: str, url: str, headers: dict | None = None) -> dict:
    request = urllib.request.Request(url, method=method, headers=headers or {})
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            body = response.read()
            status = response.status
            response_headers = {k.lower(): v for k, v in response.headers.items()}
    except urllib.error.HTTPError as exc:
        body = exc.read()
        status = exc.code
        response_headers = {k.lower(): v for k, v in exc.headers.items()}
    elapsed_ms = int((time.time() - started) * 1000)
    text = body.decode("utf-8", errors="replace")
    try:
        parsed = json.loads(text)
    except ValueError:
        parsed = None
    return {
        "status_code": status,
        "headers": response_headers,
        "body_excerpt": text[:600],
        "json": parsed,
        "elapsed_ms": elapsed_ms,
    }


def package_version(name: str) -> str:
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:  # pragma: no cover - 环境自述失败不应阻断证据
        return "unknown"


def wait_until_ready(base_url: str, process: subprocess.Popen | None) -> float:
    started = time.time()
    last_error = ""
    while time.time() - started < READY_TIMEOUT_SECONDS:
        if process is not None and process.poll() is not None:
            raise SystemExit(
                "FAIL: uvicorn 提前退出（code=%s）；端口可能被占用：见 server_stderr"
                % process.returncode
            )
        try:
            result = http_request("GET", base_url + "/api/v1/health")
            if result["status_code"] == 200:
                return round(time.time() - started, 3)
            last_error = "health status=%s" % result["status_code"]
        except (urllib.error.URLError, ConnectionError, OSError) as exc:  # 未就绪
            last_error = str(exc)
        time.sleep(READY_INTERVAL_SECONDS)
    raise SystemExit("FAIL: %ss 内未就绪；last_error=%s" % (READY_TIMEOUT_SECONDS, last_error))


def record(results: list, name: str, method: str, url: str, headers: dict | None,
           assertions: dict) -> dict:
    result = http_request(method, url, headers)
    body = result["json"]
    evaluated = {}
    for key, expected in assertions.items():
        if key == "status_code":
            actual = result["status_code"]
        elif key.startswith("header:"):
            actual = result["headers"].get(key.split(":", 1)[1].strip())
        elif body is None:
            actual = None
        else:
            actual = body.get(key) if isinstance(body, dict) else None
        evaluated[key] = {"expected": expected, "actual": actual, "ok": actual == expected}
    ok = all(item["ok"] for item in evaluated.values())
    entry = {
        "name": name,
        "method": method,
        "request_headers": headers or {},
        "status_code": result["status_code"],
        "url": url,
        "elapsed_ms": result["elapsed_ms"],
        "response_headers": {
            key: value
            for key, value in result["headers"].items()
            if key in {
                "content-type", "access-control-allow-origin",
                "access-control-allow-methods", "access-control-allow-headers",
            }
        },
        "assertions": evaluated,
        "ok": ok,
        "body_excerpt": result["body_excerpt"],
    }
    results.append(entry)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="F-019 ICP 只读 API 本地探针")
    parser.add_argument("--check-only", action="store_true",
                        help="只探测、不写证据文件（只读检查）")
    parser.add_argument("--out", default="", help="证据 JSON 输出路径")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--icp-repo", default="", help="GlobalCloud ICP 仓路径（默认自动定位）")
    args = parser.parse_args()

    repo = Path(args.icp_repo).resolve() if args.icp_repo else find_icp_repo()
    base_url = "http://%s:%d" % (args.host, args.port)
    hard_failures = []

    started_server = None
    server_origin = "pre-existing"
    server_stderr = ""
    startup_seconds = 0.0
    if port_is_open(args.host, args.port):
        # 已有实例在跑：复用并明确记录（证据区分 origin，避免误认为是本探针启动）
        startup_seconds = wait_until_ready(base_url, None)
    else:
        env = dict(os.environ)
        env["PYTHONPATH"] = "src"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        started_server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "gc_icp.api:app",
             "--host", args.host, "--port", str(args.port), "--log-level", "warning"],
            cwd=str(repo), env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        server_origin = "started_by_probe"
        try:
            startup_seconds = wait_until_ready(base_url, started_server)
        except SystemExit as exc:
            try:
                server_stderr = (started_server.communicate(timeout=5)[1] or "")[-1200:]
            finally:
                if started_server.poll() is None:
                    started_server.terminate()
            raise SystemExit("%s\nserver_stderr=%s" % (exc, server_stderr))

    checks: list = []
    try:
        health_url = base_url + "/api/v1/health"
        record(checks, "GET health（候选态边界）", "GET", health_url, {}, {
            "status_code": 200,
            "status": "candidate",
            "overallStatus": "partial",
            "confirmationStatus": "human_required",
            "productionReady": False,
            "noWriteAssertion": True,
            "industryNodeCount": 24,
            "poolCount": 11,
            "scenarioCount": 3,
        })
        idm = record(checks, "GET industry-model（24 节点）", "GET", base_url + "/api/v1/industry-model", {}, {
            "status_code": 200,
        })
        nodes = ((idm["json"] or {}).get("nodes") or []) if idm["status_code"] == 200 else []
        checks[-1]["assertions"]["len(nodes)==24"] = {
            "expected": 24, "actual": len(nodes), "ok": len(nodes) == 24,
        }
        checks[-1]["ok"] = all(item["ok"] for item in checks[-1]["assertions"].values())

        rst = record(checks, "GET resource-pools（11 池·projectionOnly）", "GET",
                     base_url + "/api/v1/resource-pools", {}, {
                         "status_code": 200,
                         "projectionOnly": True,
                     })
        pools = ((rst["json"] or {}).get("pools") or []) if rst["status_code"] == 200 else []
        checks[-1]["assertions"]["len(pools)==11"] = {
            "expected": 11, "actual": len(pools), "ok": len(pools) == 11,
        }
        checks[-1]["ok"] = all(item["ok"] for item in checks[-1]["assertions"].values())

        sc = record(checks, "GET scenarios（3 受控场景）", "GET", base_url + "/api/v1/scenarios", {}, {
            "status_code": 200,
            "status": "candidate",
        })
        scenes = ((sc["json"] or {}).get("scenarios") or []) if sc["status_code"] == 200 else []
        checks[-1]["assertions"]["len(scenarios)==3"] = {
            "expected": 3, "actual": len(scenes), "ok": len(scenes) == 3,
        }
        checks[-1]["ok"] = all(item["ok"] for item in checks[-1]["assertions"].values())

        cg = record(checks, "GET constitution-governance（5 角色·KDS canonical）", "GET",
                    base_url + "/api/v1/constitution-governance", {}, {
                        "status_code": 200,
                        "domainOwner": "ICP",
                        "canonicalCustodian": "KDS",
                        "noWriteAssertion": True,
                    })
        roles = ((cg["json"] or {}).get("roles") or []) if cg["status_code"] == 200 else []
        checks[-1]["assertions"]["len(roles)==5"] = {
            "expected": 5, "actual": len(roles), "ok": len(roles) == 5,
        }
        checks[-1]["ok"] = all(item["ok"] for item in checks[-1]["assertions"].values())

        origin = "http://localhost:4300"
        record(checks, "GET health + Origin（CORS 放行 WAE 宿主）", "GET", health_url,
               {"Origin": origin}, {
                   "status_code": 200,
                   "header:access-control-allow-origin": origin,
               })

        preflight = record(checks, "OPTIONS health 预检（只读：GET/OPTIONS）", "OPTIONS",
                           health_url,
                           {"Origin": origin, "Access-Control-Request-Method": "GET"},
                           {"status_code": 200})
        allow_methods = (preflight["headers"].get("access-control-allow-methods") or "").upper()
        preflight_ok = "GET" in allow_methods and "OPTIONS" in allow_methods
        checks[-1]["assertions"]["allow-methods 含 GET/OPTIONS"] = {
            "expected": "GET, OPTIONS",
            "actual": preflight["headers"].get("access-control-allow-methods"),
            "ok": preflight_ok,
        }
        checks[-1]["ok"] = all(item["ok"] for item in checks[-1]["assertions"].values())
    finally:
        if started_server is not None and started_server.poll() is None:
            started_server.terminate()
            try:
                _, err = started_server.communicate(timeout=10)
                server_stderr = (err or "")[-1200:]
            except subprocess.TimeoutExpired:
                started_server.kill()
                server_stderr = "forced-kill"

    passed = [c for c in checks if c["ok"]]
    result = {
        "schema_version": "1.0",
        "feature": "F-019",
        "name": "icp-industry-console",
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "evidence_class": "local_read_only_http_probe",
        "boundary": (
            "只访问 127.0.0.1 本地候选运行时的一期只读 GET 面；不做真实外部 API / "
            "真实 KDS API / 真实业务源调用；不写业务数据；不提升项目状态。"
        ),
        "runtime": {
            "python": sys.version.split()[0],
            "fastapi": package_version("fastapi"),
            "uvicorn": package_version("uvicorn"),
            "icp_repo": str(repo),
        },
        "server": {
            "host": args.host,
            "port": args.port,
            "base_url": base_url,
            "origin": server_origin,
            "pid": started_server.pid if started_server is not None else None,
            "startup_seconds": startup_seconds,
            "stderr_tail": server_stderr,
        },
        "commands": {
            "start": "cd 'GlobalCloud ICP' && PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -m uvicorn gc_icp.api:app --host 127.0.0.1 --port 8091",
            "probe": "python3 features/active/F-019-icp-industry-console/evidence/check_icp_api.py --check-only",
        },
        "checks": checks,
        "result": {
            "passed": len(passed) == len(checks),
            "checks_total": len(checks),
            "checks_passed": len(passed),
            "failed": [c["name"] for c in checks if not c["ok"]],
        },
    }

    for check in checks:
        print("[%s] %s %s -> %s (%dms)" % (
            "PASS" if check["ok"] else "FAIL", check["method"], check["name"].split(" ", 1)[-1],
            check["status_code"], check["elapsed_ms"]))
        for key, item in check["assertions"].items():
            if not item["ok"]:
                print("       assert %s expected=%r actual=%r" % (key, item["expected"], item["actual"]))
    print("probe: checks=%d passed=%d result=%s server=%s:%d origin=%s" % (
        len(checks), len(passed), "PASS" if result["result"]["passed"] else "FAIL",
        args.host, args.port, server_origin))

    if args.out and not args.check_only:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("evidence written:", out_path)

    return 0 if result["result"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
