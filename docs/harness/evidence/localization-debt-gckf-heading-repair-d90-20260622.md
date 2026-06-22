---
doc_id: GPCF-DOC-LOCALIZATIONDEBTGCKFHEADINGREPAIRD9020260622
title: GC-Knowledge Fabric D90 中文化标题修复证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/localization-debt-gckf-heading-repair-d90-20260622.md
source_path: docs/harness/evidence/localization-debt-gckf-heading-repair-d90-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric D90 中文化标题修复证据

## Evidence ID

`LOCALIZATION-DEBT-GCKF-HEADING-REPAIR-D90-20260622`

## 结论

本 evidence 记录 D90 对 `docs/gc-knowledge-fabric` 的第二批中文化标题修复。本轮只处理 10 个受控文档的 H1 标题，把纯英文标题改为中文优先标题，并保留必要的英文专有名词和 `dry-run` 口径。

本轮不批量改写正文，不改变 frontmatter、`doc_id`、路径、编号、状态、KDS 挂接、业务事实、收益、积分、委员会裁决或 GFIS/GPC 写回。

## 修复范围

本轮修复范围是委员会受理回执通知回执汇总链路下的 10 个 H1 标题。

| 文件 | 修复内容 |
|---|---|
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-completeness-precheck-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-completeness-precheck-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-completeness-precheck-dry-run-v0.1.md` | H1 改为中文优先标题 |

## 门禁变化

| 指标 | 修复前 | 修复后 | 变化 |
|---|---:|---:|---:|
| 全仓中文化命中数 | 360 | 350 | -10 |
| `docs/gc-knowledge-fabric` 命中数 | 77 | 67 | -10 |
| `doc_english_line` | 298 | 288 | -10 |
| `doc_english_heavy` | 61 | 61 | 0 |
| `software_english_user_text` | 1 | 1 | 0 |

## 当前状态

中文化门禁仍为 `fail`，原因是剩余债务仍存在。本轮只证明第二批 GCKF 标题修复有效，不声明全仓中文化完成。

## 受控边界

- 不写入真实 KDS API。
- 不写入 GFIS/GPC 或其他业务系统。
- 不升级 `accepted`、`integrated` 或 `production_ready`。
- 不改变 GFIS 真实业务链路 `repair_required` 状态。
- 不形成正式收益、积分、额度、悬赏或委员会裁决。

## 下一轮建议

继续处理 `docs/gc-knowledge-fabric` 剩余 H1 纯英文标题，优先从剩余 67 个 GCKF 命中项中选择同类委员会受理链路文档。
