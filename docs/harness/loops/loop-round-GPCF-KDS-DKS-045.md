---
doc_id: GPCF-DOC-82F75216CA
title: LOOP Round GPCF-KDS-DKS-045 - 底座知识候选人工确认与委员会复核队列视图
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-045.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-045.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-045 - 底座知识候选人工确认与委员会复核队列视图

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-045`  
模式：`LOOP / L2 本地候选队列生成`  
状态：`candidate_only`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-044` 的 14 条写回候选，生成两类只读候选视图：

- 人工确认队列：非 hard-stop 候选，可由对应责任人或项目组进行来源、缺口、事实状态确认。
- 委员会复核队列：hard-stop 候选，必须经委员会复核后才允许进入任何下游动作。

本轮只形成队列视图，不执行确认、裁决、写回、结算或状态升级。

## 2. 输入文件

| 类型 | 路径 | 用途 |
|---|---|---|
| DKS-044 JSON 摘要 | `docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.json` | 提供 14 条 writebackCandidates |
| DKS-044 写回候选台账 | `docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md` | 提供人工可读候选清单 |
| DKS-044 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-044.md` | 提供上轮边界和证据 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认不得升级 accepted / integrated |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 确认 GFIS / GPCF 仍为 repair_required |

## 3. 输出文件

| 类型 | 路径 | 状态 |
|---|---|---|
| 队列视图 builder | `tools/kds-sync/build_base_knowledge_confirmation_queue_views.py` | local tool |
| 人工确认队列 JSON | `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.json` | candidate-only evidence |
| 人工确认队列 Markdown | `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md` | controlled |
| 委员会复核队列 JSON | `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.json` | candidate-only evidence |
| 委员会复核队列 Markdown | `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-045.md` | controlled |

## 4. 队列分流规则

| 条件 | 队列 | 本轮状态 |
|---|---|---|
| `hardStop=false` | 人工确认队列 | `candidate_only` |
| `hardStop=true` | 委员会复核队列 | `candidate_only` |

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
| queue builder | `python3 tools/kds-sync/build_base_knowledge_confirmation_queue_views.py` | pass |
| Python 语法检查 | `python3 -m py_compile tools/kds-sync/build_base_knowledge_confirmation_queue_views.py` | pass |
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- tools/kds-sync/build_base_knowledge_confirmation_queue_views.py docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md docs/harness/loops/loop-round-GPCF-KDS-DKS-045.md` | pass |
| 禁止词扫描 | 对本轮新增文件执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| queue builder | pass | `total_candidates=14`; `human_queue=4`; `committee_queue=10`; `status=candidate_only` |
| Python 语法检查 | pass | `python3 -m py_compile tools/kds-sync/build_base_knowledge_confirmation_queue_views.py` 无输出 |
| builder frontmatter 保留 | pass | 文档控制后复跑 builder，人工确认队列、委员会复核队列和本轮 LOOP 记录 frontmatter 均保留 |
| 文档控制 | pass | `tools/kds-sync/document_control.py` 已执行完成；人工确认队列 doc_id=`GPCF-DOC-87A94990FE`，委员会复核队列 doc_id=`GPCF-DOC-B30625918B`，本轮 LOOP 记录 doc_id=`GPCF-DOC-82F75216CA` |
| 队列分流 | pass | `hardStop=false` 进入人工确认队列 4 条；`hardStop=true` 进入委员会复核队列 10 条 |
| 本轮边界 | pass | 两个队列均显示 `realKdsApiWrite=false`、`waesWrite=false`、`businessLedgerWrite=false`、`settlementWrite=false`、`ragAdmission=false`、`committeeDecisionCompleted=false` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；Token 未写入文档或 evidence |
| LOOP 文档门禁 | pass | `repo_md=965`; `kds_md=978`; `local_mirror_ledger_lines=965`; `api_sync_ledger_lines=79`; `missing_metadata=0`; `missing_readme_dirs=0` |
| 本轮差异格式 | pass | scoped `git diff --check -- tools/kds-sync/build_base_knowledge_confirmation_queue_views.py docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md docs/harness/loops/loop-round-GPCF-KDS-DKS-045.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮新增脚本、人工确认队列、委员会复核队列和 LOOP 记录无禁止词命中 |
| LOOP 编排器 | partial | `document_gate=pass`; `kds_token_status=pass`; 全仓 `git_gate=rework_required` 来源于既有大量非本轮 Markdown EOF 差异；`operational_gates=blocked` 来源于 GFIS/GPCF 既有 `repair_required` 与客户满意/质量阻断 |
| 状态升级 | not_allowed | 本轮不升级 `accepted` 或 `integrated`，仍受 GFIS/GPCF `repair_required` 约束 |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| 人工确认队列被误认为已确认 | 队列状态固定为 `candidate_only`，下游允许为 `false` |
| 委员会复核队列被误认为已裁决 | 明确 `committeeDecisionCompleted=false` |
| 候选队列绕过 hard-stop | hard-stop 行只进入委员会复核队列 |
| 收益、积分或额度提前结算 | evidence 明确不做 settlement、revenue allocation、AI quota allocation |
| RAG 越权 | evidence 明确 `ragAdmission=false` |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-046`：建立人工确认队列的字段级确认表单 schema 与委员会复核字段级裁决 schema，仍保持本地候选状态。
