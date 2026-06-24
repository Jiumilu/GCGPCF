---
doc_id: GPCF-DOC-16D1014A00
title: LOOP Round GPCF-KDS-DKS-043 - 底座可用知识闭环率评分脚本最小 dry-run
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-043.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-043.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-043 - 底座可用知识闭环率评分脚本最小 dry-run

日期：2026-06-18  
轮次：`GPCF-KDS-DKS-043`  
模式：`LOOP / L2 本地 dry-run`  
状态：`local_dry_run_completed`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-042`，实现底座可用知识闭环率评分脚本最小本地 dry-run，使 DKS-041 / DKS-042 的六维评分、KDS 11 池挂接、hard-stop、一票否决、禁止输出和 fixture 断言具备可重复执行入口。

## 2. 输入文档

| 类型 | 路径 | 用途 |
|---|---|---|
| DKS-042 规格 | `03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md` | 提供脚本输入、输出、计算和 hard-stop 规则 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认当前不得升级 accepted / integrated |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 确认 GFIS / GPCF 仍为 repair_required |

## 3. 输出文件

| 类型 | 路径 | 状态 |
|---|---|---|
| dry-run 脚本 | `tools/kds-sync/validate_base_knowledge_closure_score_dry_run.py` | local tool |
| fixture 集 | `docs/harness/evidence/base-knowledge-closure-score-fixtures.json` | dry-run fixture |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-043.md` | controlled |

## 4. 本轮动作

| 动作 | 结果 |
|---|---|
| 实现六维评分 | 已按 `20% / 25% / 20% / 15% / 10% / 10%` 加权计算 |
| 实现分层判定 | 已覆盖 `safe_reuse_candidate`、`limited_report_candidate`、`repair_candidate`、`return_for_source`、`blocked_or_invalid` |
| 实现 hard-stop | 已覆盖无 KDS 池、账本游离、无来源、收入误认、RAG 越权、结算越权等阻断 |
| 实现 fixture suite | 已覆盖 6 个 DKS-042 最小 fixture |
| 实现禁止输出检查 | 已阻断真实 API、RAG 准入、主账写入、结算完成、状态升级等输出标记 |

## 5. 明确不做范围

本轮不做：

- 真实评分入账；
- 缺口关闭；
- 悬赏发布；
- 积分结算；
- 收益分配；
- AI 额度发放；
- RAG 准入；
- 指挥舱强引用；
- 委员会真实裁决；
- WAES 放行；
- 真实 KDS API 写入；
- GFIS、GPC、PVAOS 或其他业务系统主账写入；
- `accepted` 或 `integrated` 状态升级。

## 6. Evidence 计划

| 门禁 | 命令或检查 | 预期 |
|---|---|---|
| dry-run fixture suite | `python3 tools/kds-sync/validate_base_knowledge_closure_score_dry_run.py` | pass |
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- tools/kds-sync/validate_base_knowledge_closure_score_dry_run.py docs/harness/evidence/base-knowledge-closure-score-fixtures.json docs/harness/loops/loop-round-GPCF-KDS-DKS-043.md` | pass |
| 禁止词扫描 | 对本轮三个新增文件执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| dry-run fixture suite | pass | `fixtures=6`; `expectedHardStops=4`; `boundary.realKdsApiWrite=false`; `boundary.waesWrite=false`; `boundary.businessLedgerWrite=false`; `boundary.settlementWrite=false`; `boundary.ragAdmission=false` |
| Python 语法检查 | pass | `python3 -m py_compile tools/kds-sync/validate_base_knowledge_closure_score_dry_run.py` 无输出 |
| 文档控制 | pass | `tools/kds-sync/document_control.py` 已执行完成；本轮 LOOP 记录 doc_id=`GPCF-DOC-16D1014A00` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；未写入 TOKEN 明文 |
| LOOP 文档门禁 | pass | `repo_md=923`; `kds_md=936`; `local_mirror_ledger_lines=923`; `api_sync_ledger_lines=73`; `missing_metadata=0`; `missing_readme_dirs=0` |
| LOOP 编排器文档门禁 | pass | `document_gate=pass`; `loop_governance_docs.gate=pass`; `kds_token_status.gate=pass` |
| 本轮差异格式 | pass | `git diff --check -- tools/kds-sync/validate_base_knowledge_closure_score_dry_run.py docs/harness/evidence/base-knowledge-closure-score-fixtures.json docs/harness/loops/loop-round-GPCF-KDS-DKS-043.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮三个新增文件未命中禁止旧口径、旧 AI 定位和真实性污染关键词 |
| 文档台账 | pass | `09-status/globalcloud-document-control-register.md` 已登记 `GPCF-DOC-16D1014A00` |
| KDS 本地镜像 | pass | `.kds/local-mirror-ledger.jsonl` 已记录本轮 LOOP 文档；同步状态为 `pending_api` |
| 全仓格式门禁 | partial | LOOP 编排器报告 `git_gate.gate=partial`，原因为工作区仍存在既有 dirty 状态；本轮新增文件 scoped diff check 通过 |
| 运行治理门禁 | blocked / rework | 仍受 `09-status/gpcf-project-status-matrix.md` 中 GFIS/GPCF `repair_required` 和既有阻塞信号影响；本轮不升级 `accepted` 或 `integrated` |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| fixture hard-stop 被误认为失败 | fixture suite 中 expected hard-stop 命中属于通过，单条输入仍按规格返回 exit code 2 |
| dry-run 结果被误认为准入 | 输出保留 `dry_run`、`candidate_only` 或 `blocked` |
| 增强账本脱离 KDS 11 池 | `kdsPoolRefs=[]` 且增强账本非空时强制 hard-stop |
| 收入或订单误认 | 一票否决优先于分数，进入委员会候选，不得入收益池或主账 |
| RAG 越权 | 非安全复用候选且 `ragInclude=true` 时强制阻断 |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-044`：把 dry-run 输出转成 Markdown evidence 摘要和缺口写回候选台账，仍保持本地候选状态，不接入真实系统。
