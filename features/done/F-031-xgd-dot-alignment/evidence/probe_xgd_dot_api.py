#!/usr/bin/env python3
"""F-031 XGD dot API 只读证据探针。

用途
----
对**本机已运行的 XGD 后端**做只读 HTTP 检查，产出可回放的 api 证据：
`/healthz`、`/runtime/info` 与 P0 的 `/dot/*` 只读端点。全部请求为 `GET`，
不发送 `POST/PUT/DELETE`，不写文件、不改 XGD 数据、不修改任何配置。

边界
----
* 只允许只读：必须显式传 `--read-only`，否则拒绝执行。
* 只连本机回环地址（默认 `http://127.0.0.1:3721`，可用 `XGD_API_BASE_URL` 覆盖），
  不访问外部服务。
* 输出只含状态码、耗时、字节数与白名单字段；不回显响应全文，避免把运行时数据
  或凭据写进证据。

用法
----
    python3 features/active/F-031-xgd-dot-alignment/evidence/probe_xgd_dot_api.py --read-only

退出码
------
    0 全部端点 HTTP 200 且关键字段符合预期；1 有端点失败；2 未声明只读或未运行服务。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "http://127.0.0.1:3721"
TIMEOUT_SECONDS = 10.0

# (path, 期望字段路径列表) —— 只取白名单字段，不回显全文。
ENDPOINTS = (
    ("/healthz", ("status", "db", "llm", "running", "memory_count")),
    ("/runtime/info", ("ok", "service", "version", "mode", "modeValid", "scopeValid", "isolationMode")),
    ("/dot/state", ("ok", "enabled", "paused")),
    ("/dot/profiles", ("ok",)),
    ("/dot/responsibilities?limit=100", ("ok",)),
    ("/dot/schedules?limit=100", ("ok",)),
    ("/dot/rules?limit=100", ("ok",)),
    ("/dot/activity?limit=5", ("ok",)),
    ("/dot/approvals?status=pending&limit=5", ("ok",)),
    ("/dot/connectors", ("ok",)),
)


def read_only_guard(flag: bool) -> int | None:
    if flag:
        return None
    print("xgd_dot_api_probe=refused reason=read-only flag required (--read-only)")
    return 2


def get_json(base_url: str, path: str) -> tuple[int, dict, int, float]:
    url = base_url.rstrip("/") + path
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )
    started = __import__("time").monotonic()
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        body = response.read()
        status = response.status
    elapsed_ms = (__import__("time").monotonic() - started) * 1000
    try:
        payload = json.loads(body.decode("utf-8", errors="replace") or "{}")
    except json.JSONDecodeError:
        payload = {"_unparsed": True}
    return status, payload, len(body), elapsed_ms


def summarize(path: str, payload: dict, fields: tuple[str, ...]) -> dict:
    summary = {}
    for field in fields:
        if isinstance(payload, dict) and field in payload:
            value = payload[field]
            if isinstance(value, (str, int, float, bool)) or value is None:
                summary[field] = value
            elif isinstance(value, list):
                summary[field] = f"list[{len(value)}]"
            elif isinstance(value, dict):
                summary[field] = f"object[{len(value)} keys]"
    if isinstance(payload, dict):
        for list_field in ("profiles", "responsibilities", "schedules", "rules", "activity",
                           "approvals", "connectors", "items", "documents"):
            value = payload.get(list_field)
            if isinstance(value, list):
                summary[f"{list_field}_count"] = len(value)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="XGD dot API 只读证据探针（GET only）")
    parser.add_argument("--read-only", action="store_true", help="必填：声明只做只读检查")
    args = parser.parse_args(argv)
    guard = read_only_guard(args.read_only)
    if guard is not None:
        return guard

    base_url = os.environ.get("XGD_API_BASE_URL", DEFAULT_BASE_URL)
    print(f"xgd_dot_api_probe base_url={base_url} method=GET read_only=true")
    failures = 0
    for path, fields in ENDPOINTS:
        try:
            status, payload, size, elapsed_ms = get_json(base_url, path)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            failures += 1
            print(f"GET {path} -> error {type(exc).__name__}: {exc}")
            continue
        summary = summarize(path, payload, fields)
        ok = status == 200
        if path == "/healthz":
            ok = ok and summary.get("status") == "ok" and summary.get("db") == "connected"
        if path == "/runtime/info":
            ok = ok and summary.get("ok") is True and summary.get("scopeValid") is True
        if path == "/dot/state":
            ok = ok and summary.get("ok") is True and summary.get("enabled") is True
        if not ok:
            failures += 1
        verdict = "pass" if ok else "fail"
        print(
            f"GET {path} -> HTTP {status} {size}B {elapsed_ms:.0f}ms {verdict} "
            + json.dumps(summary, ensure_ascii=False, sort_keys=True)
        )

    total = len(ENDPOINTS)
    if failures:
        print(f"xgd_dot_api_probe=fail endpoints={total - failures}/{total}")
        return 1
    print(f"xgd_dot_api_probe=pass endpoints={total}/{total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
