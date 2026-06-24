---
doc_id: GPCF-DOC-E324E197A2
title: LOOP Round GPCF-KDS-DKS-047 - 底座知识人工确认与委员会复核空白实例模板
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-047.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-047.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-047 - 底座知识人工确认与委员会复核空白实例模板

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-047`  
模式：`LOOP / L2 本地 blank template dry-run`  
状态：`blank_template_only`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-046` 的两套字段级 schema，生成两套空白实例模板：

- 人工确认空白模板：按 4 条人工确认队列项预绑定候选身份字段，其余确认字段为空。
- 委员会复核空白模板：按 10 条委员会复核队列项预绑定候选身份字段，其余裁决字段为空。

本轮只生成空白模板，不填报、不确认、不裁决、不写回。

## 2. 输入文件

| 类型 | 路径 | 用途 |
|---|---|---|
| 人工确认 schema JSON | `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.json` | 提供人工确认字段定义 |
| 委员会复核 schema JSON | `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.json` | 提供委员会复核字段定义 |
| 人工确认队列 JSON | `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.json` | 提供 4 条候选项 |
| 委员会复核队列 JSON | `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.json` | 提供 10 条候选项 |
| DKS-046 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-046.md` | 提供上轮边界和证据 |

## 3. 输出文件

| 类型 | 路径 | 状态 |
|---|---|---|
| template builder | `tools/kds-sync/build_base_knowledge_blank_review_templates.py` | local tool |
| 人工确认模板 JSON | `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.json` | blank template |
| 人工确认模板 Markdown | `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md` | controlled |
| 委员会复核模板 JSON | `docs/harness/evidence/base-knowledge-committee-review-template-20260619.json` | blank template |
| 委员会复核模板 Markdown | `docs/harness/evidence/base-knowledge-committee-review-template-20260619.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-047.md` | controlled |

## 4. 明确不做范围

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

## 5. Evidence 计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| template builder | `python3 tools/kds-sync/build_base_knowledge_blank_review_templates.py` | pass |
| Python 语法检查 | `python3 -m py_compile tools/kds-sync/build_base_knowledge_blank_review_templates.py` | pass |
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- tools/kds-sync/build_base_knowledge_blank_review_templates.py docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md docs/harness/evidence/base-knowledge-committee-review-template-20260619.md docs/harness/loops/loop-round-GPCF-KDS-DKS-047.md` | pass |
| 禁止词扫描 | 对本轮新增文件执行禁止词扫描 | pass |

## 6. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| template builder | pass | `human_template_records=4`; `committee_template_records=10`; `status=blank_template_only` |
| Python 语法检查 | pass | `python3 -m py_compile tools/kds-sync/build_base_knowledge_blank_review_templates.py` 无输出 |
| 空白字段校验 | pass | 两个模板除 `queueItemId`、`sourceCandidateId`、`baseKnowledgeId` 身份字段外，其余字段均为空字符串、空数组或 null |
| 文档控制 | pass | 人工确认模板 doc_id=`GPCF-DOC-7797BB4F55`，委员会复核模板 doc_id=`GPCF-DOC-8066745911`，本轮 LOOP 记录 doc_id=`GPCF-DOC-E324E197A2` |
| 本轮边界 | pass | 两个模板均显示 `blankTemplateOnly=true`、`createsConfirmationFact=false`、`createsCommitteeDecision=false`、`realKdsApiWrite=false`、`waesWrite=false`、`businessLedgerWrite=false`、`settlementWrite=false`、`ragAdmission=false` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；Token 未写入文档或 evidence |
| LOOP 文档门禁 | pass | `repo_md=995`; `kds_md=1008`; `local_mirror_ledger_lines=995`; `missing_metadata=0`; `missing_readme_dirs=0` |
| 本轮差异格式 | pass | scoped `git diff --check -- tools/kds-sync/build_base_knowledge_blank_review_templates.py docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md docs/harness/evidence/base-knowledge-committee-review-template-20260619.md docs/harness/loops/loop-round-GPCF-KDS-DKS-047.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮新增脚本、人工确认模板、委员会复核模板和 LOOP 记录无禁止词命中 |
| LOOP 编排器 | partial | `document_gate=pass`; `kds_token_status=pass`; 全仓 `git_gate=rework_required` 来源于既有大量非本轮 Markdown EOF 差异；`operational_gates=blocked` 来源于 GFIS/GPCF 既有 `repair_required` 与客户满意/质量阻断 |
| 状态升级 | not_allowed | 本轮不升级 `accepted` 或 `integrated`，仍受 GFIS/GPCF `repair_required` 约束 |

## 7. 风险与边界

| 风险 | 控制 |
|---|---|
| 空白模板被误认为已填报 | 模板状态固定为 `blank_template_only` |
| 预绑定身份字段被误认为事实确认 | 只预绑定 queue/candidate/base knowledge 身份字段，用于追溯 |
| 委员会模板被误认为已裁决 | 模板控制字段固定 `createsCommitteeDecision=false` |
| 收益、积分或额度提前结算 | 模板控制字段明确不做 settlement、revenue allocation、AI quota allocation |
| RAG 越权 | 模板控制字段明确 `ragAdmission=false` |

## 8. 下一轮建议

建议进入 `GPCF-KDS-DKS-048`：建立空白模板的字段级校验器，验证必填身份字段、空白字段、禁止写回边界和未来填报前置条件。
