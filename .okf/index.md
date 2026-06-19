---
doc_id: GPCF-DOC-323D4F2AA4
title: OKF 兼容层只读导航总索引
project: GPCF
related_projects: [GPCF, GPC, WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.okf/index.md
source_path: .okf/index.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# OKF 兼容层只读导航总索引

用途：为 Agent 提供只读导航入口，指向 Git、KDS、文档台账和 Loop evidence 中的受控事实源。

## 使用边界

- OKF 只做导航和上下文分组，不复制受控文档正文。
- OKF 不替代 Git 源文档、KDS 开发空间、文档控制台账或同步流水。
- OKF 摘要不得作为业务完成、验收完成或状态升级依据。
- 任何事实判断必须回到 `source_path`、`kds_path`、`09-status/*` 台账和 `.kds/sync-ledger.jsonl`。

## Bundle

| bundle | index | scope |
| --- | --- | --- |
| governance-bundle | `.okf/governance/index.md` | 文档治理、Loop、Harness、状态机、门禁 |
| architecture-bundle | `.okf/architecture/index.md` | 项目群架构、主线对齐、跨项目架构 |
| kds-bundle | `.okf/kds/index.md` | KDS 同步、安全、镜像、导入规则 |
| kds-okf-v0.1-derived-bundle | `.okf/bundles/kds-v0.1/index.md` | KDS 受控文档的 OKF v0.1 metadata-only 派生层 |

## Agent 读取顺序

```text
.okf/index.md
→ .okf/<bundle>/index.md
→ source_path 原始受控文档
→ 09-status/* 台账
→ .kds/sync-ledger.jsonl
```
