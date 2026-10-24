#!/usr/bin/env python3
"""P17 done Feature 不变量审计：done 目录内每个 Feature 要么证据可关单，要么落在已登记受控例外内。

不变量（老卢 2026-10-22 Q6/P17 裁定）：
  ∀ f ∈ features/done: close_candidate(f) = true  ∨  ∃ 例外 e ∈ runtime/exceptions.yaml 覆盖 f

用法：
    python3 scripts/gpcf_p17_done_audit.py [--json]
退出码：0 = 不变量成立；1 = 存在未登记例外的不合规定 done Feature
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DONE = ROOT / "features" / "done"
EXCEPTIONS = ROOT / "runtime" / "exceptions.yaml"


def done_features() -> list[tuple[str, Path]]:
    items = []
    for d in sorted(DONE.iterdir()):
        if not d.is_dir():
            continue
        fid = d.name.split("-")[0] + "-" + d.name.split("-")[1]
        items.append((fid, d))
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    doc = yaml.safe_load(EXCEPTIONS.read_text(encoding="utf-8")) if EXCEPTIONS.is_file() else {}
    exception_ids = {e.get("exemption_id") for e in (doc.get("exceptions") or [])}

    rows, violations = [], []
    for fid, path in done_features():
        out = subprocess.run([sys.executable, "scripts/gpcf_check_evidence.py", fid, "--check-only"],
                             cwd=ROOT, capture_output=True, text=True)
        text = (out.stdout or "") + (out.stderr or "")
        closable = "close_candidate=true" in text
        exc = f"EXC-DONE-{fid}"
        covered = exc in exception_ids
        rows.append({"feature": fid, "dir": path.name, "closable": closable, "exception": exc, "covered": covered})
        if not closable and not covered:
            violations.append(fid)

    summary = {"done_count": len(rows), "closable": sum(r["closable"] for r in rows),
               "covered_by_exception": sum(1 for r in rows if not r["closable"] and r["covered"]),
               "violations": violations,
               "status": "pass" if not violations else "fail"}
    result = {"gate": "p17_done_audit", **summary, "rows": rows}
    print(json.dumps(result, ensure_ascii=False, indent=1) if args.json else
          f"done={summary['done_count']} closable={summary['closable']} "
          f"exception={summary['covered_by_exception']} violations={violations} → {summary['status']}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
