---
doc_id: GPCF-DOC-03FB1D644C
title: Document Control Policy
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/document-control-policy.md
source_path: .codex/skills/globalcloud-document-governance/references/document-control-policy.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Document Control Policy

## 目标

所有项目群工作必须在文档中有对应记录。任何架构、治理、实现、验证、状态、证据、归档变化，都必须能通过文档控制台账追溯。

## 受控状态

| status | 含义 |
|---|---|
| controlled | 当前有效受控文档 |
| draft | 草案或变更提案 |
| archive | 历史证据、历史会话、运行归档 |
| deprecated | 过期但保留 |
| superseded | 被新文档替代 |
| operational_controlled | 工具、技能、运行类文档，只登记和镜像，不随意改正文 |

## 强制字段

每个可修改 Markdown 文档必须有 frontmatter：

```yaml
doc_id:
title:
project:
related_projects:
domain:
status:
version:
owner:
kds_space: 开发
kds_path:
source_path:
sync_direction:
last_reviewed:
supersedes:
superseded_by:
```

## 目录规则

- 有 Markdown 文档的目录必须有 README。
- 新增目录必须说明用途、收录范围、KDS 路径和文档清单。
- 过期文档不删除，移动或标记为 archive/deprecated/superseded。

## 文档债务

若本轮工作确实无法完整更新文档，必须登记文档债务：

```yaml
doc_debt:
  reason:
  affected_docs:
  owner:
  due_loop:
  max_status: partial
```

存在文档债务时，项目状态不得升到 `accepted` 或 `integrated`。
