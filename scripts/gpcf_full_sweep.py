#!/usr/bin/env python3
"""GPCF 全量体检：门禁之外的校验器 + derive + pytest 一次跑完（2026-10-24）。

背景：门禁已纳入 3 项回归校验，但仍有若干校验只在人工体检中执行
（方案继承以外的快照/状态审计/本地化/字节码/口径基线等），
并发编辑可能悄悄回退它们。本脚本把这些固定为一条命令，输出统一证据。

用法：
    python3 scripts/gpcf_full_sweep.py            # 打印表格，任一失败 exit 1
    python3 scripts/gpcf_full_sweep.py --json     # 机器可读
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS: list[tuple[str, list[str], int]] = [
    ("loop_document_gate", ["tools/kds-sync/loop_document_gate.py", "--check-only"], 300),
    ("caliber_baseline", ["tools/kds-sync/validate_project_group_caliber_baseline.py"], 120),
    ("render_completion", ["tools/kds-sync/render_project_group_completion.py", "--check"], 180),
    ("master_plan_register", ["tools/kds-sync/validate_project_master_plan_register.py"], 120),
    ("plan_inheritance", ["tools/kds-sync/validate_project_plan_inheritance.py"], 120),
    ("contract_matrix", ["tools/kds-sync/validate_contract_matrix.py"], 120),
    ("feature_workspace", ["tools/kds-sync/validate_gpcf_2_feature_workspace.py"], 180),
    ("live_status_snapshot", ["tools/kds-sync/validate_project_group_live_status_snapshot_20260626.py"], 120),
    ("status_audit", ["tools/kds-sync/daily_project_status_audit.py", "--check"], 180),
    ("localization", ["tools/kds-sync/check_chinese_localization_gate.py"], 180),
    ("bytecode", ["tools/kds-sync/check_python_bytecode.py"], 120),
    ("loop_v11_recovery", ["tools/kds-sync/validate_loop_v11_slimming_delivery_recovery.py"], 180),
    ("derive_status", ["tools/kds-sync/derive_status_views.py", "--check"], 180),
    ("p17_done_audit", ["scripts/gpcf_p17_done_audit.py"], 300),
    ("exceptions_expiry", ["tools/kds-sync/check_exceptions_expiry.py"], 120),
    ("pytest", ["-m", "pytest", "tests/", "-q"], 600),
]


def run(cmd: list[str], timeout: int) -> tuple[int, float]:
    start = time.time()
    try:
        proc = subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, time.time() - start
    except subprocess.TimeoutExpired:
        return 124, time.time() - start


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = []
    for name, cmd, timeout in CHECKS:
        code, seconds = run(cmd, timeout)
        rows.append({"check": name, "exit": code, "seconds": round(seconds, 2), "ok": code == 0})
    failed = [r["check"] for r in rows if not r["ok"]]
    summary = {"checks": len(rows), "passed": len(rows) - len(failed), "failed": failed,
               "seconds": round(sum(r["seconds"] for r in rows), 1)}

    if args.json:
        print(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=1))
    else:
        print(f"{'检查':24s} {'exit':>4s} {'秒':>6s}")
        for r in rows:
            print(f"{r['check']:24s} {r['exit']:4d} {r['seconds']:6.2f}")
        print(f"\n汇总：{summary['passed']}/{summary['checks']} 通过，用时 {summary['seconds']}s")
        if failed:
            print("失败：" + ", ".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
