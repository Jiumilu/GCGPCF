---
doc_id: GPCF-DOC-4DF761BE6B
title: LOOP Round GPCF-KDS-DKS-046 - 底座知识人工确认与委员会复核字段级 schema
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-046.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-046.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-046 - 底座知识人工确认与委员会复核字段级 schema

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-046`  
模式：`LOOP / L2 本地 schema dry-run`  
状态：`schema_dry_run_only`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-045` 的人工确认队列和委员会复核队列，建立两套字段级 schema：

- 人工确认 schema：用于未来对非 hard-stop 候选进行来源、证据、缺口、RAG 准入意见和下一步动作确认。
- 委员会复核 schema：用于未来对 hard-stop 候选进行严重度、投票、积分影响候选、收益池影响候选、写回意见、申诉和备案要求记录。

本轮只定义字段，不创建人工确认事实，不创建委员会裁决，不执行写回。

## 2. 输入文件

| 类型 | 路径 | 用途 |
|---|---|---|
| 人工确认队列 JSON | `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.json` | 提供 4 条非 hard-stop 候选来源 |
| 委员会复核队列 JSON | `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.json` | 提供 10 条 hard-stop 候选来源 |
| DKS-045 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-045.md` | 提供上轮边界和证据 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认不得升级 accepted / integrated |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 确认 GFIS / GPCF 仍为 repair_required |

## 3. 输出文件

| 类型 | 路径 | 状态 |
|---|---|---|
| schema builder | `tools/kds-sync/build_base_knowledge_queue_schema_dry_run.py` | local tool |
| 人工确认 schema JSON | `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.json` | schema dry-run |
| 人工确认 schema Markdown | `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md` | controlled |
| 委员会复核 schema JSON | `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.json` | schema dry-run |
| 委员会复核 schema Markdown | `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-046.md` | controlled |

## 4. schema 边界

| schema | 来源队列 | 字段用途 | 本轮状态 |
|---|---|---|---|
| 人工确认 schema | `human_confirmation` | 定义未来人工确认记录字段 | `schema_dry_run_only` |
| 委员会复核 schema | `committee_review` | 定义未来委员会复核记录字段 | `schema_dry_run_only` |

## 5. 明确不做范围

本轮不做：

- 人工确认完成；
- 委员会裁决完成；
- 事实入池；
- 缺口关闭；
- 悬赏发布；
- 积分结算；
- 收益分配；
- AI 额度发放；
- RAG 准入；
- 指挥舱强引用；
- WAES 放行；
- 真实 KDS API 写入；
- GFIS、GPC、PVAOS、Finance 或其他业务系统主账写入；
- `accepted` 或 `integrated` 状态升级。

## 6. Evidence 计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| schema builder | `python3 tools/kds-sync/build_base_knowledge_queue_schema_dry_run.py` | pass |
| Python 语法检查 | `python3 -m py_compile tools/kds-sync/build_base_knowledge_queue_schema_dry_run.py` | pass |
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- tools/kds-sync/build_base_knowledge_queue_schema_dry_run.py docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md docs/harness/loops/loop-round-GPCF-KDS-DKS-046.md` | pass |
| 禁止词扫描 | 对本轮新增文件执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| schema builder | pass | `human_schema_fields=13`; `committee_schema_fields=15`; `human_source_items=4`; `committee_source_items=10`; `status=schema_dry_run_only` |
| Python 语法检查 | pass | `python3 -m py_compile tools/kds-sync/build_base_knowledge_queue_schema_dry_run.py` 无输出 |
| builder frontmatter 保留 | pass | 人工确认 schema、委员会复核 schema 和本轮 LOOP 记录均保留受控 frontmatter |
| 文档控制 | pass | 人工确认 schema doc_id=`GPCF-DOC-9C22552EEE`，委员会复核 schema doc_id=`GPCF-DOC-F861799E08`，本轮 LOOP 记录 doc_id=`GPCF-DOC-4DF761BE6B` |
| schema 来源一致性 | pass | 人工确认 schema 来源队列为 `human_confirmation` 4 条；委员会复核 schema 来源队列为 `committee_review` 10 条 |
| 本轮边界 | pass | 两个 schema 均显示 `createsConfirmationFact=false`、`createsCommitteeDecision=false`、`realKdsApiWrite=false`、`waesWrite=false`、`businessLedgerWrite=false`、`settlementWrite=false`、`ragAdmission=false` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；Token 未写入文档或 evidence |
| LOOP 文档门禁 | pass | `repo_md=989`; `kds_md=1002`; `local_mirror_ledger_lines=989`; `missing_metadata=0`; `missing_readme_dirs=0` |
| 本轮差异格式 | pass | scoped `git diff --check -- tools/kds-sync/build_base_knowledge_queue_schema_dry_run.py docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md docs/harness/loops/loop-round-GPCF-KDS-DKS-046.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮新增脚本、人工确认 schema、委员会复核 schema 和 LOOP 记录无禁止词命中 |
| LOOP 编排器 | partial | `document_gate=pass`; `kds_token_status=pass`; 全仓 `git_gate=rework_required` 来源于既有大量非本轮 Markdown EOF 差异；`operational_gates=blocked` 来源于 GFIS/GPCF 既有 `repair_required` 与客户满意/质量阻断 |
| 状态升级 | not_allowed | 本轮不升级 `accepted` 或 `integrated`，仍受 GFIS/GPCF `repair_required` 约束 |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| schema 被误认为已确认 | schema 状态固定为 `schema_dry_run_only`，且 `createsConfirmationFact=false` |
| schema 被误认为已裁决 | 委员会 schema 固定 `createsCommitteeDecision=false` |
| 字段定义绕过 hard-stop | hard-stop 候选仍只可通过委员会复核 schema 进入后续候选流程 |
| 收益、积分或额度提前结算 | schema 控制字段明确不做 settlement、revenue allocation、AI quota allocation |
| RAG 越权 | schema 控制字段明确 `ragAdmission=false` |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-047`：基于两个 schema 生成空白确认实例模板和空白委员会复核实例模板，仍保持本地候选状态。
