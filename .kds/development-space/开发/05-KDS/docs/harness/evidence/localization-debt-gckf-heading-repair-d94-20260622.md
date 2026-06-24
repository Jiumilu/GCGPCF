---
doc_id: GPCF-DOC-LOCALIZATIONDEBTGCKFHEADINGREPAIRD9420260622
title: GC-Knowledge Fabric D94 中文化标题修复证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/localization-debt-gckf-heading-repair-d94-20260622.md
source_path: docs/harness/evidence/localization-debt-gckf-heading-repair-d94-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric D94 中文化标题修复证据

## Evidence ID

`LOCALIZATION-DEBT-GCKF-HEADING-REPAIR-D94-20260622`

## 结论

本 evidence 记录 D94 对 `docs/gc-knowledge-fabric` 剩余 H1 中文化债务的修复。本轮处理 20 个受控文档的 H1 标题，包括 GFIS Assistant DKS 系列、Harness Governance 决策受理和 Loop 文档门禁固定 `doc_id` 漂移检查文档。

本轮完成后，`docs/gc-knowledge-fabric` 的 H1 命中数从 `20` 降为 `0`。但该目录仍有 5 条非 H1 英文正文行，因此中文化门禁仍未完成。

## 门禁变化

| 指标 | 修复前 | 修复后 | 变化 |
|---|---:|---:|---:|
| 全仓中文化命中数 | 315 | 295 | -20 |
| `docs/gc-knowledge-fabric` 命中数 | 25 | 5 | -20 |
| `docs/gc-knowledge-fabric` H1 命中数 | 20 | 0 | -20 |
| `doc_english_line` | 246 | 226 | -20 |
| `doc_english_heavy` | 68 | 68 | 0 |
| `software_english_user_text` | 1 | 1 | 0 |

## 剩余 GCKF 命中

- `formal-evidence-execution-incident-escalation-preview-dry-run-v0.1.md:66`
- `formal-evidence-execution-incident-escalation-preview-dry-run-v0.1.md:71`
- `formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.md:43`
- `formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.md:44`
- `formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.md:45`

## 受控边界

- 不写入真实 KDS API。
- 不写入 GFIS/GPC 或其他业务系统。
- 不升级 `accepted`、`integrated` 或 `production_ready`。
- 不改变 GFIS 真实业务链路 `repair_required` 状态。
- 不形成正式收益、积分、额度、悬赏或委员会裁决。

## 下一轮建议

D95 应处理上述 5 条 GCKF 非 H1 英文正文行，并把 GCKF 桶清零；然后继续处理 `docs/harness/loops` 和 `docs/harness/evidence` 中的剩余中文化债务。
