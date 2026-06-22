---
doc_id: GPCF-DOC-13B5A26E7C
title: CodeGraph KDS OKF 映射说明
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/codegraph/codegraph-kds-okf-mapping.md
source_path: docs/codegraph/codegraph-kds-okf-mapping.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph KDS OKF 映射说明

CodeGraph 输出进入 KDS/OKF 时只能是候选事实。

允许候选类型：

- `code_fact_candidate`
- `api_fact_candidate`
- `dependency_fact_candidate`
- `architecture_fact_candidate`
- `test_mapping_candidate`

禁止：

- 直接写入 `accepted_fact`。
- 生成治理规则、财务规则或权限规则。
- 把 mock、demo、自动文档或图谱推断当作生产证据。

升格条件：

- Harness evidence。
- WAES gate。
- Human review。
- KDS curator 处理 lineage 与状态变更。
