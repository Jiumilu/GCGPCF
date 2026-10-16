#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三层对齐表门禁（2026-10-16 建立，创新 5）

规则：openspec/changes/ 下（排除 archive 与豁免清单）每个 change 的
proposal.md 或 design.md 必须含「三层对齐」段（契约→工具链→应用链）。

用法：
  python3 tools/kds-sync/validate_change_alignment_sections.py          # 全量检查
  python3 tools/kds-sync/validate_change_alignment_sections.py <name>   # 单查

退出码：0=全部合规；1=有缺失。
豁免：EXEMPT 集合（本文件内维护；新 change 不豁免——新建 change 必须带表）。
"""
from __future__ import annotations

import sys
from pathlib import Path

GPCF_ROOT = Path(__file__).resolve().parents[2]
CHANGES_DIR = GPCF_ROOT / "openspec/changes"

# 历史 change 豁免（2026-10-16 前建立且未带表）；新 change 一律不豁免。
EXEMPT = {
    "enable-project-group-openspec-coverage",
    "gcworld-controlled-runtime-integration",
    "gcworld-evidence-twin-foundation",
    "gcworld-kds-authoritative-integration",
    "gcworld-workbench-ui-foundation",
    "integrate-gke001-openspec-codegraph",
    "kds-production-hardening",
    "register-globalcloud-icp",
    "sop-bind-matrix-to-icp-foundation",
    "spaceai-studio-multiplatform-refactor",
    "spaceai-was-city-flood-replay",
    "world-project-onboarding",
}

KEY = "三层对齐"


def check_change(d: Path) -> tuple[bool, str]:
    for name in ("proposal.md", "design.md"):
        f = d / name
        if f.exists() and KEY in f.read_text(encoding="utf-8"):
            return True, name
    return False, "proposal.md / design.md 均未见「%s」段" % KEY


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    missing = []
    checked = 0
    for d in sorted(CHANGES_DIR.iterdir()):
        if not d.is_dir() or d.name in ("archive", "README.md") or d.name.startswith("."):
            continue
        if only and d.name != only:
            continue
        if d.name in EXEMPT:
            continue
        checked += 1
        ok, detail = check_change(d)
        print("  [%s] %s（%s）" % ("OK" if ok else "缺失", d.name, detail))
        if not ok:
            missing.append(d.name)
    print("三层对齐表门禁：检查 %d 个 change；缺失 %d 个。" % (checked, len(missing)))
    if missing:
        print("缺失清单：" + " / ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
