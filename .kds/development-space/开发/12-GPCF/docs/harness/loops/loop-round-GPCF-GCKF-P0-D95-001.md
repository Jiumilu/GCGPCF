---
doc_id: GPCF-LOOP-GCKF-P0-D95-001
title: Loop Round GPCF-GCKF-P0-D95-001
project: GPCF
related_projects: [GFIS, GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D95-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D95-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GCKF-P0-D95-001

## 输入

- D94 输出：`docs/harness/evidence/localization-debt-gckf-heading-repair-d94-20260622.md`
- D95 前置中文化门禁：全仓命中 `295`，GCKF 命中 `5`，GCKF H1 命中 `0`
- D95 目标目录：`docs/gc-knowledge-fabric`

## 动作

本轮修复 `docs/gc-knowledge-fabric` 剩余非标题中文化债，将 dry-run 预览文档中英文重列表项调整为中文优先表达。

## 输出

- `docs/harness/evidence/localization-debt-gckf-cleanout-d95-20260622.json`
- `docs/harness/evidence/localization-debt-gckf-cleanout-d95-20260622.md`
- `tools/kds-sync/validate_localization_debt_gckf_cleanout_d95.py`

## 门禁结果

- D95 专项验证：`pass`。
- D94/D93 回归验证：`pass`。
- 文档污染检查：`pass`。
- KDS Token 检查：`pass`，fingerprint=`bfd9553d`。
- Loop 文档门禁：`rework_required`，原因是全仓其它目录仍存在 `localization_debt`。

## 边界

- 不写 KDS API。
- 不写 GFIS/GPC/业务系统。
- 不升级 accepted/integrated/production_ready。
- GFIS 真实业务通道继续保持 `repair_required`。

## 下一轮

继续按中文化债队列处理其它目录，直到 Loop 文档门禁不再因 `localization_debt` 阻断。
