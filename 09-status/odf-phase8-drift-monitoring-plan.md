---
doc_id: GPCF-DOC-4B4A93C3B9
title: ODF Phase 8 小批量回归与漂移监控方案
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase8-drift-monitoring-plan.md
source_path: 09-status/odf-phase8-drift-monitoring-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# ODF Phase 8 小批量回归与漂移监控方案

日期：2026-06-19

## 目标

建立 ODF hash 漂移监控门禁，覆盖 pilot、Phase 2、Phase 4 和 Phase 7 的 ODF ledger。该阶段不新增样本，只检查 source hash、Markdown hash 和 envelope hash 是否一致。

## 监控对象

| scope | path |
| --- | --- |
| pilot ledger | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.json` |
| Phase 2 ledger | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.json` |
| Phase 4 ledger | `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.json` |
| Phase 7 ledger | `docs/harness/evidence/odf-phase7-small-batch-ledger-20260619.json` |

## 工具

```bash
python3 tools/kds-sync/scan_odf_hash_drift.py --fail-on-drift
```

## 漂移处理规则

| condition | action |
| --- | --- |
| drift=0 | 允许进入 KDS 定向同步和闭环报告 |
| source_hash drift | 更新对应 envelope 和 ledger hash，不改源 Markdown 正文 |
| odf_hash drift | 回填 ledger `odf_hash` |
| recurring dynamic source | 纳入 Phase 8 报告，下一阶段考虑动态源排除或稳定快照 |

## 非范围

- 不创建新 ODF 样本。
- 不复制源 Markdown 正文。
- 不全量导入 ODF。
- 不批量改写 Markdown 正文。
- 不写生产系统或真实外部 API。
- 不做业务状态升级。
