---
doc_id: GPCF-DOC-14437543B7
title: LOOP 门禁委托覆盖审计（29 仓，2026-10-24）
project: KDS
related_projects: [GFIS, GPC, WAME, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/loop-gate-delegation-audit-20261024.md
source_path: docs/reports/loop-gate-delegation-audit-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# LOOP 门禁委托覆盖审计（29 仓，2026-10-24）

- 口径：各仓 `tools/kds-sync/loop_document_gate.py` 是否**委托**到 GPCF 正本门禁（而非自实现副本）
- 委托判据：含 `Delegate project-group loop gate execution to the GPCF canonical gate` 与 `GPCF_PROJECT_GROUP_GATE_DELEGATED = "1"`

## 1. 结果

| 状态 | 仓数 | 仓（精确列表，2026-10-24 17:35 复算） |
|---|---:|---|
| ✅ 委托到 GPCF 正本 | **21** | AAAS、Brain、WAS、XiaoC、WAME、GPC、Studio、XWAIL、GFIS、MMC、KDS、XiaoG、PVAOS、SOP、PKC、XGD、**PQC**、SpaceAI、SpaceAIStudio、WAE、Project(PMC) |
| 🟡 正本本身（GPCF） | 1 | GlobalCloud GPCF（455 行，被委托方） |
| ❌ **无 gate** | **7** | **ICP、World、GCMEM、PDC、SLC、DRC、FireQuote** |

> 上次表格把 World/PDC 误列入"委托"列并加问号；本轮逐仓复算后已更正：二者确为**无 gate**。

## 2. 校验器覆盖缺口

`validate_project_group_external_loop_gate_delegates.py` 只检查 **3 个仓**（AAAS / XWAIL / SOP），
因此：

- 其余 18 个"委托"仓的委托声明**未被门禁校验**（可能被并发编辑改坏而无人知）；
- 7 个"无 gate"仓**完全不在校验范围**。

这与方案继承审计（`inheritance-coverage-audit-20261024.md`）是同类问题：**不变量存在，但覆盖面窄**。

## 3. 属主可复制的最小委托脚本（以 SOP 为准，17 行核心）

```python
#!/usr/bin/env python3
"""Delegate project-group loop gate execution to the GPCF canonical gate."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GPCF_ROOT = ROOT.parent / "GlobalCloud GPCF"
GPCF_GATE = GPCF_ROOT / "tools/kds-sync/loop_document_gate.py"

if not GPCF_GATE.exists():
    raise SystemExit("FAIL: missing GPCF canonical loop_document_gate.py")

env = os.environ.copy()
env["GPCF_PROJECT_GROUP_GATE_DELEGATED"] = "1"
env["GPCF_DELEGATED_PROJECT_ROOT"] = str(ROOT)

result = subprocess.run(
    [sys.executable, str(GPCF_GATE), "--check-only"],
    cwd=str(GPCF_ROOT), env=env, text=True, capture_output=True, check=False,
)
if result.stdout:
    print(result.stdout, end="")
if result.stderr:
    print(result.stderr, end="", file=sys.stderr)
raise SystemExit(result.returncode)
```

落位：`<仓>/tools/kds-sync/loop_document_gate.py`；放进该仓 pre-commit 钩子后即生效。

## 4. 建议顺序

1. 先给 **ICP / GCMEM / World / PDC**（活跃项目）补委托脚本（属主 5 分钟可完成）；
2. SLC / DRC / FireQuote 按处置排期；
3. 覆盖扩展到 29 仓属治理增强，需老卢裁定后一次性改校验器清单（否则门禁会立即转红）。

## 5. 边界

只读审计，未改任何仓；不构成状态提升。
