#!/usr/bin/env python3
"""PQC 真实试点收口一键脚本（P12→P14→S4 的最后一段）。

默认 dry-run：只校验并打印执行计划，不写任何台账。
--apply：在全部校验通过后执行——推进 VU 到 S4 + 追加决策台账。

用法：
    python3 scripts/gpcf_pqc_pilot_close.py \
        --vu-id <VU> --evidence <真实回执.json> \
        --auth-id AUTH-PG-PQC-REAL-PILOT-20261022 [--apply]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROMOTE = ROOT / "scripts" / "gpcf_promote_vu_stage.py"
LEDGER = ROOT / "runtime" / "audit" / "decision-ledger-20261024.jsonl"
VU_LEDGER = ROOT / "runtime" / "vu-ledger.yaml"
RENDER = ROOT / "tools" / "kds-sync" / "render_project_group_completion.py"


def c_real() -> float:
    out = subprocess.run([sys.executable, str(RENDER), "--json"], capture_output=True, text=True, cwd=ROOT)
    try:
        return float(json.loads(out.stdout)["group"]["C_real"])
    except Exception:
        return -1.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vu-id", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--auth-id", default="AUTH-PG-PQC-REAL-PILOT-20261022")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    plan = {"gate": "pqc_pilot_close", "mode": "apply" if args.apply else "dry_run",
            "vu_id": args.vu_id, "evidence": args.evidence, "auth_id": args.auth_id,
            "steps": [], "problems": [], "c_real_before": c_real()}

    # 1) 证据与纪律校验（复用 promote 的 --dry-run）
    dry = subprocess.run([sys.executable, str(PROMOTE), "--vu-id", args.vu_id,
                          "--evidence", args.evidence, "--auth-id", args.auth_id, "--dry-run"],
                         capture_output=True, text=True, cwd=ROOT)
    try:
        dry_doc = json.loads(dry.stdout)
    except Exception:
        dry_doc = {"problems": [f"promote dry-run 输出无法解析: {dry.stdout[-300:]}{dry.stderr[-300:]}"]}
    plan["problems"] += dry_doc.get("problems", [])
    plan["steps"].append({"step": "证据与回执校验", "ok": not dry_doc.get("problems", [])})

    # 2) F-032 证据完整性（不要求全 pass，只报告）
    fe = subprocess.run([sys.executable, "scripts/gpcf_check_evidence.py", "F-032", "--check-only"],
                        capture_output=True, text=True, cwd=ROOT)
    plan["steps"].append({"step": "F-032 证据检查", "output": (fe.stdout or fe.stderr).strip()[-200:]})

    if plan["problems"]:
        plan["status"] = "fail"
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 1

    if not args.apply:
        plan["status"] = "ready"
        plan["next"] = "校验通过；加 --apply 执行：推进 VU→S4 + 台账追加 promote_s4"
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 0

    # 3) 正式推进
    run = subprocess.run([sys.executable, str(PROMOTE), "--vu-id", args.vu_id,
                          "--evidence", args.evidence, "--auth-id", args.auth_id],
                         capture_output=True, text=True, cwd=ROOT)
    ok = run.returncode == 0
    plan["steps"].append({"step": "推进 VU→S4", "ok": ok, "output": (run.stdout or run.stderr).strip()[-200:]})
    if not ok:
        plan["status"] = "fail"
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 1

    # 4) 台账追加（append-only，独立文件避免与既有台账混写）
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if LEDGER.exists():
        rows = [json.loads(line) for line in LEDGER.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows.append({
        "id": f"p{len(rows)+1:03d}", "time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "kind": "promote_s4", "question": f"{args.vu_id} 推进 S4（PQC 真实试点）",
        "answer": "真实业务回执通过六项校验", "none": 0.0,
        "adopted": "老卢授权 A1–A4；工具强校验通过", "auth_id": args.auth_id,
        "evidence": args.evidence,
    })
    LEDGER.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    plan["ledger"] = str(LEDGER.relative_to(ROOT))
    plan["c_real_after"] = c_real()
    plan["status"] = "done"
    print(json.dumps(plan, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
