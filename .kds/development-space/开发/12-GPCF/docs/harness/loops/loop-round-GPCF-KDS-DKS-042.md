---
doc_id: GPCF-DOC-6EAE781FDF
title: LOOP Round GPCF-KDS-DKS-042 - 底座可用知识闭环率评分脚本 dry-run 规格
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-042.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-042.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-042 - 底座可用知识闭环率评分脚本 dry-run 规格

日期：2026-06-17  
轮次：`GPCF-KDS-DKS-042`  
模式：`LOOP / L1 文档治理`  
状态：`controlled_documentation`

## 1. 本轮目标

承接 `GPCF-KDS-DKS-041`，定义底座可用知识闭环率评分脚本 dry-run 规格，将字段字典转成 JSON schema、示例输入、示例输出、计算断言、hard-stop 断言和禁止输出规则。

## 2. 输入文档

| 类型 | 路径 | 用途 |
|---|---|---|
| DKS-041 主文档 | `03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md` | 提供字段字典、计算样表和否决规则 |
| DKS-040 主文档 | `03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md` | 提供虚拟样例 |
| LOOP 控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 确认当前仍不得升级 accepted / integrated |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 确认 GFIS / GPCF 仍为 repair_required |

## 3. 输出文档

| 类型 | 路径 | 状态 |
|---|---|---|
| DKS-042 主文档 | `03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md` | controlled |
| 本轮 LOOP 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-042.md` | controlled |

## 4. 本轮动作

| 动作 | 结果 |
|---|---|
| 定义 dry-run 输入对象 | 已定义 `BaseKnowledgeClosureScoreInput` |
| 定义 JSON schema 草案 | 已覆盖必填字段、数值范围、KDS 11 池挂接和禁止额外字段 |
| 定义 dry-run 输出对象 | 已定义 `BaseKnowledgeClosureScoreDryRunResult` |
| 定义计算断言 | 已覆盖六维加权计算和分层判定 |
| 定义 hard-stop 断言 | 已覆盖无 KDS 池、账本游离、无来源、收入误认、RAG 越权等 |
| 定义 fixture 集 | 已定义 6 个最小 fixture |
| 定义退出码 | 已区分 schema 失败、hard-stop、计算不一致和越权输出 |

## 5. 明确不做范围

本轮不做：

- 脚本实现；
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
| 文档控制 | `python3 tools/kds-sync/document_control.py` | pass |
| 文档污染 | `python3 tools/kds-sync/check_document_pollution.py` | pass |
| KDS TOKEN | `python3 tools/kds-sync/validate_kds_token.py` | pass |
| LOOP 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| LOOP 编排器 | `python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` | pass 或记录全仓既有阻塞 |
| 差异格式 | `git diff --check -- 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md docs/harness/loops/loop-round-GPCF-KDS-DKS-042.md` | pass |
| 禁止词扫描 | 对本轮两个新增文档执行禁止词扫描 | pass |

## 7. 当前证据结果

| 门禁 | 结果 | 证据 |
|---|---|---|
| 文档控制 | pass | `tools/kds-sync/document_control.py` 已执行完成；主文档 doc_id=`GPCF-DOC-F72C6A953D`，本轮 LOOP 记录 doc_id=`GPCF-DOC-6EAE781FDF` |
| 文档污染 | pass | `document_pollution=pass` |
| KDS TOKEN | pass | `kds_token=pass fingerprint=bfd9553d`；未写入 TOKEN 明文 |
| LOOP 文档门禁 | pass | `repo_md=875`; `kds_md=888`; `local_mirror_ledger_lines=875`; `api_sync_ledger_lines=67`; `missing_metadata=0`; `missing_readme_dirs=0` |
| LOOP 编排器文档门禁 | pass | `document_gate=pass`; `loop_governance_docs.gate=pass`; `kds_token_status.gate=pass` |
| 本轮差异格式 | pass | `git diff --check -- 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md docs/harness/loops/loop-round-GPCF-KDS-DKS-042.md` 无输出 |
| 本轮禁止词扫描 | pass | 本轮两个新增文档未命中禁止旧口径、旧 AI 定位和真实性污染关键词 |
| 文档台账 | pass | `09-status/globalcloud-document-control-register.md` 已登记两个 doc_id |
| KDS 本地镜像 | pass | `.kds/local-mirror-ledger.jsonl` 已记录两个 `git_to_kds_local_mirror` 条目；同步状态为 `pending_api` |
| 全仓格式门禁 | partial | LOOP 编排器报告 `git_gate.gate=partial`，原因为工作区仍存在既有 dirty 状态；本轮新增文件 scoped diff check 通过 |
| 运行治理门禁 | blocked / rework | 仍受 `09-status/gpcf-project-status-matrix.md` 中 GFIS/GPCF `repair_required` 和既有阻塞信号影响；本轮不升级 `accepted` 或 `integrated` |

## 8. 风险与边界

| 风险 | 控制 |
|---|---|
| dry-run 规格被误认为脚本实现 | 明确本文不是实现，不执行真实评分 |
| schema 校验被误认为业务完成 | 明确 schema 只证明结构可校验 |
| hard-stop 被分数覆盖 | 明确 hard-stop 优先于分数 |
| 输出对象被误用为真实写回 | 明确全部输出为 dry-run 或 candidate_only |
| fixture 被误认为真实资料 | 明确 fixture 只用于本地演练 |

## 9. 下一轮建议

建议进入 `GPCF-KDS-DKS-043`：实现底座可用知识闭环率评分脚本最小本地 dry-run。
