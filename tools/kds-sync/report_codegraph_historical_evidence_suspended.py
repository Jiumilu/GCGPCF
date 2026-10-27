#!/usr/bin/env python3
"""CodeGraph 历史证据 5 条验证器的 SUSPENDED 状态报告（2026-10-27）。

背景：这 5 个验证器把 "GlobalCoud GPCF"（错拼）写成期望值，而它们的证据件
（2026-06/07 生成）里也是同一错拼 → 错拼对错拼，形成「恒绿」：判据在替一个不存在的仓名盖章。

处置（Chief 2026-10-27 裁定）：
- 证据件一个字节都不改（那是当时跑出来的真实历史，改它就是伪造历史）；
- 判据改为断言真实仓名（GlobalCloud GPCF），于是**旧证据立刻变红**——这正是判据生效的证明；
- 仓内没有这 5 份证据的生成器，重跑不出新证据，因此按裁定第 2 选项：显式 SUSPENDED，绝不绿。

本脚本**不是门禁**：它只把 suspended 状态显式打印出来，退出码恒 0（报告性质）。
那 5 个验证器本身仍是红（直接跑会 exit 1 并报 repo set mismatch），不会被这个报告掩盖。
"""

from __future__ import annotations

import sys

SUSPENDED = [
    "validate_codegraph_impact_report_dry_run.py",
    "validate_codegraph_watchlist_sync_authorization_pack.py",
    "validate_codegraph_watchlist_threshold_review_20260622.py",
    "validate_loop_codegraph_sync_drift.py",
    "validate_codegraph_watchlist_sync_plan.py",
]

REASON = (
    "SUSPENDED: 依赖 2026-06/07 历史证据（含错拼仓名），判据已改为真实仓名 GlobalCloud GPCF，"
    "旧证据红；仓内无生成器，待重跑生成新证据后解除"
)


def main() -> int:
    for name in SUSPENDED:
        print(f"SUSPENDED tools/kds-sync/{name} — {REASON}")
    print(f"codegraph_historical_evidence_suspended={len(SUSPENDED)}（报告，非门禁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
