---
doc_id: GPCF-DOC-0FAEA2D5B2
title: WAS 决策契约 v0.3.1 冻结与发布记录（进度同步）
project: WAS
related_projects: [GPCF, XWAIL, WAME]
domain: openspec
status: draft
version: v0.1
owner: WAS
kds_space: 开发
kds_path: 开发/05-WAS/openspec/changes/was-decision-model-architecture-v0.1/artifacts/v031-freeze-and-release-record.md
source_path: openspec/changes/was-decision-model-architecture-v0.1/artifacts/v031-freeze-and-release-record.md
sync_direction: local_only
last_reviewed: 2026-10-25
supersedes: []
superseded_by: []
---

# WAS 决策契约 v0.3.1 冻结与发布记录（进度同步）

> 状态：**进度同步记录（draft）**。本文件记录 v0.3.1 冻结/发布/WAME 适配进展，**不构成验收、合并或状态提升**。

## 1. 契约冻结（WAS）

| 项 | 内容 |
|---|---|
| 契约版本 | `decision-contract-v0.3.1`（v0.3.1） |
| 内容哈希 | `c243f6aa72c689c910ddaa3ac36bf079c1226d674e7dece1349dfcbf39c5c191`（13 文件，可复现） |
| 唯一 delta | `DecisionModel.capability` 可选枚举（classification/ranking/gate/assessment_ranking/other；Q-W6=B） |
| 基线 | v0.3.0 FROZEN（`1640dcd0e65dd1be9e14e99e0c6ebb8d50f709bcab2059dbdd23cdc7e20b16d7`）只读保留 |
| 复核 | 独立复核通过（老卢，2026-10-25，A .740） |
| 冻结确认 | 老卢确认（A .927，2026-10-25） |
| 记录位置 | WAS `docs/decision/freeze-record-v031-v0.1.md`（status: frozen_v0.3.1） |

## 2. 发布（XWAIL 分支 + PR）

| 项 | 内容 |
|---|---|
| 分支/commit | `feat/xwail-decision-schemas-v03` @ `d9647e7`（已推 origin） |
| 目录 | `schemas-json/decision/v0.3.1/`：12 契约文件 + manifest + `schema-hashes.json` + testcases（11 正/33 负） |
| 校验 | `check_object_schemas.py` PASS 44/44；`validate_bundle_v031.py` VALID；v0.3 基线 43/43 不受影响 |
| PR | **#4**（base main，仅提案）；standards CI pass 22s；**2026-10-25 已合并 main**（merge commit `bfd7595`） |

## 3. WAME 适配（v0.3.1）

| 项 | 内容 |
|---|---|
| 分支/commit | `feat/wame-decision-v03-input` @ `1975b96`（已推） |
| 变更 | `V03DecisionModel.capability` 可选字段；mapper 写入 WAME 能力原值，`modelType` 保留有损收敛映射（两字段并存） |
| 校验 | 13 files / 93 tests PASS；typecheck 0；eslint 0；bundle 经 v0.3.1 validator VALID |
| 合并 | PR #59 MERGED 到特征线；2026-10-25 特征线合并 main（`1b227b2`） |

## 4. 边界与非声明

- v0.3.0/v0.3.1 均为 FROZEN 契约副本；**FROZEN ≠ 验收/生产可用**；无 accepted/integrated/production_ready 声明；
- 全合成数据；未接真实数据/客户数据；
- GPCF 门禁外部 hard failures 不由本记录修复/掩盖；CP 同步为进度记录。
