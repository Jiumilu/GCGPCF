---
doc_id: GPCF-DOC-LOCALIZATIONDEBTGCKFHEADINGREPAIRD8920260622
title: GC-Knowledge Fabric D89 中文化标题修复证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/localization-debt-gckf-heading-repair-d89-20260622.md
source_path: docs/harness/evidence/localization-debt-gckf-heading-repair-d89-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric D89 中文化标题修复证据

## Evidence ID

`LOCALIZATION-DEBT-GCKF-HEADING-REPAIR-D89-20260622`

## 结论

本 evidence 记录 D89 对 `docs/gc-knowledge-fabric` 的首批中文化债务修复。本轮只修复 5 个受控文档的 H1 标题，把纯英文标题改为中文优先标题，并保留必要的英文专有名词和 `dry-run` 口径。

本轮不批量改写正文，不改变 frontmatter、`doc_id`、路径、编号、状态、KDS 挂接、业务事实、收益、积分、委员会裁决或 GFIS/GPC 写回。

## 修复范围

| 文件 | 修复内容 |
|---|---|
| `docs/gc-knowledge-fabric/document-control-fixed-doc-id-preservation-gate-v0.1.md` | H1 改为中文优先标题 |
| `docs/gc-knowledge-fabric/formal-evidence-candidate-packet-assembly-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `docs/gc-knowledge-fabric/formal-evidence-execution-acknowledgement-routing-precheck-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-envelope-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |
| `docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-preview-dry-run-v0.1.md` | H1 改为中文优先标题 |

## 门禁变化

| 指标 | 修复前 | 修复后 | 变化 |
|---|---:|---:|---:|
| 全仓中文化命中数 | 371 | 366 | -5 |
| `docs/gc-knowledge-fabric` 命中数 | 82 | 77 | -5 |
| `doc_english_line` | 307 | 302 | -5 |
| `doc_english_heavy` | 63 | 63 | 0 |
| `software_english_user_text` | 1 | 1 | 0 |

## 当前状态

中文化门禁仍为 `fail`，原因是剩余债务仍存在。本轮仅证明首批 GC-Knowledge Fabric 标题修复有效，不声明全仓中文化完成。

## 受控边界

- 不写入真实 KDS API。
- 不写入 GFIS/GPC 或其他业务系统。
- 不升级 `accepted`、`integrated` 或 `production_ready`。
- 不改变 GFIS 真实业务链路 `repair_required` 状态。
- 不形成正式收益、积分、额度、悬赏或委员会裁决。

## 下一轮建议

继续处理 `docs/gc-knowledge-fabric` 中剩余纯英文 H1 标题，每轮保持小批量、可回退、可校验，并在每轮后重新运行中文化门禁。
