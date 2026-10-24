---
doc_id: GPCF-DOC-E2CA70136C
title: WAS 决策契约 v0.3 冻结与发布记录（进度同步）
project: WAS
related_projects: [GPCF, XWAIL, WAME]
domain: openspec
status: draft
version: v0.1
owner: WAS
kds_space: 开发
kds_path: 开发/05-WAS/openspec/changes/was-decision-model-architecture-v0.1/artifacts/v03-freeze-and-release-record.md
source_path: openspec/changes/was-decision-model-architecture-v0.1/artifacts/v03-freeze-and-release-record.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# WAS 决策契约 v0.3 冻结与发布记录（进度同步）

> 状态：**进度同步记录（draft）**。本文件记录 v0.3 冻结/发布/WAME 适配进展，**不构成验收、合并或状态提升**。

## 1. 契约冻结（WAS）

| 项 | 内容 |
|---|---|
| 契约版本 | `decision-contract-v0.3`（v0.3.0） |
| 内容哈希 | `1640dcd0e65dd1be9e14e99e0c6ebb8d50f709bcab2059dbdd23cdc7e20b16d7`（13 文件，可复现） |
| 对象 | 11 对象：DecisionProfile / DecisionModelRegistry / DecisionModel / DecisionCase / DecisionContextSnapshot / DecisionAssessment / DecisionRecord / AuthorizationRecord / ExecutionRecord / OutcomeRecord / FeedbackRecord |
| 复核 | 老卢本人兼任（双角色声明）；10 项清单通过（A .868） |
| 冻结确认 | 老卢确认（A .616，2026-10-24） |
| 记录位置 | WAS `docs/decision/freeze-record-v03-draft-v0.1.md`（status: frozen_v0.3.0） |

## 2. 发布（XWAIL 本地分支）

| 项 | 内容 |
|---|---|
| 分支/commit | `feat/xwail-decision-schemas-v03` @ `3c934d5`（worktree `_wt/GlobalCloud XWAIL--feat-decision-schemas-v03`） |
| 目录 | `schemas-json/decision/v0.3/`：13 契约文件 + README + `schema-hashes.json` + testcases |
| 校验 | 哈希 13/13 复现；`check_object_schemas.py` PASS 43 / FAIL 0；`validate_bundle_v03.py` VALID |
| 兼容 | v0.2 冻结件只读共存（哈希 12/12 未动） |
| 边界 | **未 push、未合并 main**；发布 ≠ 验收/生产可用 |

## 3. WAME 适配进展（只读/规格）

- 适配复核：9/9 映射对象缺 v0.3 必填；枚举 5/9 不一致；世界层/contentHash 全缺；无 Profile/Case/Registry 持久化对象。
- 适配规格（candidate）：mapper 模块、枚举收敛表、Q-W2 执行回执映射（no-write 证据编码）、BLOCKED 字段清单、Q-W5 审计映射、Q-W3 输入扩展草案。
- 开放问题：**Q-W6** modelType 语义错配；**Q-W7 WAME 缺 DecisionRecord（根阻塞）**；**Q-W8** rawResponse/evidence 持久化。
- 实施状态：**未改 WAME 代码**；跨仓实施需 WAME owner + 老卢授权。

## 4. 门禁与阻塞

- GPCF 门禁实测（2026-10-24）：`rework_required / partial`，**37 个外部 hard failures**（项目群状态/loop/GFIS/治理板/ICP 等）→ CP 不能评审通过/合并；本记录不越权修复门禁。
- CP 评审/批准：未开始（需 GPCF owner）。
- Ontology 正式准入：未开始（P0-3）。

## 5. 非声明

- 本记录为进度同步：不构成验收、`accepted/integrated/production_ready`、合并或状态提升。
- 未接真实数据；v0.3 FROZEN/发布 ≠ 生产可用；CP 仍受外部门禁阻塞。
