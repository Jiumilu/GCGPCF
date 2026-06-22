---
doc_id: GPCF-DOC-LOCALIZATIONDEBTGCKFHEADINGREPAIRD9320260622
title: GC-Knowledge Fabric D93 中文化标题修复证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/localization-debt-gckf-heading-repair-d93-20260622.md
source_path: docs/harness/evidence/localization-debt-gckf-heading-repair-d93-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric D93 中文化标题修复证据

## Evidence ID

`LOCALIZATION-DEBT-GCKF-HEADING-REPAIR-D93-20260622`

## 结论

本 evidence 记录 D93 对 `docs/gc-knowledge-fabric` 的第五批中文化标题修复。本轮只处理 16 个受控文档的 H1 标题，把纯英文标题改为中文优先标题，并保留必要的英文专有名词和 `dry-run` 口径。

本轮不批量改写正文，不改变 frontmatter、`doc_id`、路径、编号、状态、KDS 挂接、业务事实、收益、积分、委员会裁决或 GFIS/GPC 写回。

## 门禁变化

| 指标 | 修复前 | 修复后 | 变化 |
|---|---:|---:|---:|
| 全仓中文化命中数 | 331 | 315 | -16 |
| `docs/gc-knowledge-fabric` 命中数 | 41 | 25 | -16 |
| `docs/gc-knowledge-fabric` H1 命中数 | 36 | 20 | -16 |
| `doc_english_line` | 262 | 246 | -16 |
| `doc_english_heavy` | 68 | 68 | 0 |
| `software_english_user_text` | 1 | 1 | 0 |

## 当前状态

中文化门禁仍为 `fail`，原因是剩余债务仍存在。本轮只证明第五批 GCKF 标题修复有效，不声明全仓中文化完成。

## 受控边界

- 不写入真实 KDS API。
- 不写入 GFIS/GPC 或其他业务系统。
- 不升级 `accepted`、`integrated` 或 `production_ready`。
- 不改变 GFIS 真实业务链路 `repair_required` 状态。
- 不形成正式收益、积分、额度、悬赏或委员会裁决。

## 下一轮建议

继续处理 `docs/gc-knowledge-fabric` 剩余 20 个 H1 命中项；其中多数为 GFIS Assistant DKS 系列标题。
