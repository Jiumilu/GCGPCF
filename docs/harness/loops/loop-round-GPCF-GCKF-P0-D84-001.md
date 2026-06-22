---
doc_id: GPCF-LOOP-GCKF-P0-D84-001
title: Loop Round GPCF-GCKF-P0-D84-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D84-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D84-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GCKF-P0-D84-001

## 本轮目标

把 D83 的 `doc_id` 保留机制从现象验证推进到单元级 fixture 验证，覆盖固定 ID、缺失 ID 和 external frontmatter 三类路径。

## 输入

- `tools/kds-sync/document_control.py`
- `scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py`
- D83 修复说明与 Loop evidence

## 动作

- 新增 `scripts/api/validate_gckf_p0_document_control_doc_id_unit_fixtures.py`。
- 使用临时目录构造三类 Markdown fixture。
- 验证 `build_records` 保留固定 `doc_id`。
- 验证缺失 `doc_id` 时仍使用路径哈希回退。
- 验证 `doc_control: external` 不被 `apply_frontmatter` 重写。

## 输出

- `scripts/api/validate_gckf_p0_document_control_doc_id_unit_fixtures.py`
- `docs/gc-knowledge-fabric/document-control-doc-id-unit-fixtures-v0.1.md`

## 检查

```text
gckf_p0_document_control_doc_id_unit_fixtures=pass
fixed_frontmatter_doc_id=preserved
missing_doc_id_fallback=path_hash
external_frontmatter=rewrite_skipped
execution_mode=tempdir_no_repo_write
```

## 反馈

本轮只强化文档治理机制的可复验性，不改变 GC-Knowledge Fabric 的业务事实状态。D75-D82 与 D83 仍保持 candidate/no-write 边界。

下一轮建议 D85：将 ID 漂移检测纳入文档治理健康报告或 Loop 文档门禁摘要。
