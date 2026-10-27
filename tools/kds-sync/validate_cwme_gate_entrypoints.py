#!/usr/bin/env python3
"""门禁入口存在性判据（F-022 A6，2026-10-27）。

为什么需要这条判据：
2026-10-13 KDS `b26fff66a` 把 `世界资产/世界模型引擎/ontology` 迁到 `世界资产/引擎/ontology`，
GPCF 两个验证器的路径常量没跟上，两条门禁双双 exit 1 静默 14 天。但**根因不是路径**——
修好路径后它们仍然不在 CI、不在 sweep、不被任何脚本调用，等于「修好也没人跑」。
所以路径正确只是必要条件，入口存在才是充分条件。

本判据检查：下列目标脚本必须同时出现在
  1) `scripts/gpcf_full_sweep.py`（本地手动入口）
  2) `.github/workflows/governance.yml`（CI 真门禁）
任一处缺失 → exit 1。

已知限制（说清楚，不假装完备）：本判据**自身**也被要求挂在两个入口里，但「把本判据自己从入口摘掉」
没有二级保护——这是递归问题的边界，只能靠人复核；因此本脚本把自己的入口位也一并断言，
至少让「连同入口一起被删」留下一次红而不是静默通过。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TARGETS = [
    "tools/kds-sync/validate_cwme_ontology_chain.py",
    "tools/kds-sync/validate_cwme_space_domain_extension_registration_request.py",
    "tools/kds-sync/validate_cwme_gate_entrypoints.py",
]

ENTRIES = [
    ("scripts/gpcf_full_sweep.py", "sweep"),
    (".github/workflows/governance.yml", "ci"),
]


def main() -> int:
    failures: list[str] = []
    for entry_path, entry_name in ENTRIES:
        path = ROOT / entry_path
        if not path.exists():
            failures.append(f"entry missing: {entry_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for target in TARGETS:
            if target not in text:
                failures.append(f"{entry_name} does not run {target}")
    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        print(f"cwme_gate_entrypoints=fail targets={len(TARGETS)}")
        return 1
    print(
        f"cwme_gate_entrypoints=pass targets={len(TARGETS)} "
        f"entries={len(ENTRIES)} "
        + " ".join(f"{name}=wired" for _p, name in ENTRIES)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
