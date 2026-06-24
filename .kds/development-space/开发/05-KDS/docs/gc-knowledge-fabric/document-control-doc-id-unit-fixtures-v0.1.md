---
doc_id: GPCF-DOC-GCKFDOCUMENTCONTROLDOCIDUNITFIXTURESV01
title: GC-Knowledge Fabric P0 Document Control Doc ID Unit Fixtures v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/document-control-doc-id-unit-fixtures-v0.1.md
source_path: docs/gc-knowledge-fabric/document-control-doc-id-unit-fixtures-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Document Control Doc ID Unit Fixtures v0.1

## 定位

本文件记录 D84 对 D83 机制修复的单元级验证。D83 已修复 `document_control.py` 在重建记录时覆盖固定 `doc_id` 的问题；D84 将该行为固化为可复验 fixture，避免后续维护再次引入 ID 漂移。

## 覆盖场景

| 场景 | 预期 |
| --- | --- |
| 已有固定 `doc_id` | 保留 frontmatter 中的固定 ID |
| 缺失 `doc_id` | 回退到路径哈希短 ID |
| `doc_control: external` | `apply_frontmatter` 不接管、不重写 |

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_document_control_doc_id_unit_fixtures.py
```

## 验证结果

```text
gckf_p0_document_control_doc_id_unit_fixtures=pass
fixed_frontmatter_doc_id=preserved
missing_doc_id_fallback=path_hash
external_frontmatter=rewrite_skipped
execution_mode=tempdir_no_repo_write
```

## 受控边界

- 验证脚本只使用临时目录。
- 不写入真实 KDS API。
- 不修改业务系统。
- 不改变 GFIS/GPC 写回状态。
- 不形成正式收益、积分或委员会裁决。

## 下一步

D85 可以继续把 D83/D84 的 ID 保留规则加入文档治理健康报告或门禁摘要中，使后续 `loop_document_gate.py` 能直接暴露 ID 漂移风险，而不是依赖人工额外扫描。
