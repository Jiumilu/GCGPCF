"""CodeGraph 未接入仓清单（显式跳过注册表）。

来源：Chief 2026-10-28 裁定 ①（Studio 与 WAME 必须分开处置）。
- **未接入 ≠ 索引失效**：本清单只收「仓里根本没有 .codegraph 目录」的仓；
  「有 .codegraph 但 initialized:false」属于索引故障，**不进本清单、保持红**（见 WAME）。
- 清单**写死在文件里**（路径 + 仓名 + 理由 + 接入期限）：新增仓不会自动落进清单。
- 跳过**必须打印可 grep 的** `SKIP <repo> CodeGraph not-onboarded`，并计入 `skipped_denominator`；
  不许静默 continue。
- **到期未接入 ⇒ 跳过失效**：`onboard_by` 一过，验证器直接 FAIL。
- 仓一旦出现 `.codegraph` 目录，跳过**自动失效**（转为正常探测），避免「加入了还一直跳」。
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

# 接入期限：到期未接入，跳过即失效、重新变红（可观测的退出条件）
ONBOARD_BY = "2026-12-31"

NOT_ONBOARDED: dict[str, dict] = {
    "GlobalCloud Studio": {
        "path": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud SpaceAI Studio"),
        "reason": "not-onboarded: repo has no .codegraph directory (never onboarded)",
        "onboard_by": ONBOARD_BY,
    },
}

SKIP_LABEL = "Cafe Studio"


def should_skip(repo_name: str) -> dict | None:
    """命中未接入清单返回条目；已出现 .codegraph 则视为已接入，不再跳过。"""
    entry = NOT_ONBOARDED.get(repo_name)
    if entry is None:
        return None
    if (Path(entry["path"]) / ".codegraph").exists():
        return None
    return entry


def collect(repo_names) -> dict[str, dict]:
    """一次性宣告全部未接入仓（保证跳过行总能被 grep 到），返回 {仓名: 条目}。"""
    entries: dict[str, dict] = {}
    for name in repo_names:
        entry = should_skip(name)
        if entry is not None:
            announce(name, entry)
            entries[name] = entry
    print(f"skipped_denominator={SKIP_LABEL} {len(entries)}")
    return entries


def announce(repo_name: str, entry: dict) -> None:
    """打印可 grep 的跳过行；到期未接入则直接 FAIL。"""
    deadline = _dt.date.fromisoformat(entry["onboard_by"])
    if _dt.date.today() > deadline:
        raise SystemExit(
            f"FAIL: SKIP EXPIRED {repo_name} CodeGraph not-onboarded but onboarding deadline "
            f"{entry['onboard_by']} has passed"
        )
    print(
        f"SKIP {repo_name} CodeGraph not-onboarded ({entry['reason']}); "
        f"onboard_by={entry['onboard_by']}"
    )
