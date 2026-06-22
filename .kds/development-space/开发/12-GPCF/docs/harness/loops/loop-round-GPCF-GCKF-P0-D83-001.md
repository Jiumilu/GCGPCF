---
doc_id: GPCF-LOOP-GCKF-P0-D83-001
title: Loop Round GPCF-GCKF-P0-D83-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D83-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D83-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GCKF-P0-D83-001

## 本轮目标

修复 D75-D82 固定受控 ID 被文档控制脚本重建为路径哈希短 ID 的机制缺陷，确保后续 scoped 文档治理不会破坏已确认的固定编号。

## 输入

- `tools/kds-sync/document_control.py`
- D75-D82 GC-Knowledge Fabric 受控文档
- D75-D82 Loop evidence 文档
- 文档控制台账与 KDS 本地镜像

## 动作

- 在 `document_control.py` 中新增 `controlled_doc_id`。
- 修改 `build_records`，优先读取并保留已有 frontmatter `doc_id`。
- 重新写回 D75-D82 固定 ID。
- scoped 运行 `document_control.py` 验证不再回流短 ID。
- 新增只读验证脚本 `scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py`。

## 输出

- `tools/kds-sync/document_control.py` 机制修复
- `scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py`
- `docs/gc-knowledge-fabric/document-control-fixed-doc-id-preservation-gate-v0.1.md`

## 检查

```text
gckf_p0_document_control_preserves_fixed_doc_id=pass
frontmatter_doc_id_preservation=covered
old_short_doc_ids_present=0
fixed_doc_ids_present=16
execution_mode=read_only_validation
```

## 反馈

本轮只修复文档控制机制，不改变 GCKF 候选链路状态。D75-D82 仍保持 candidate/no-write 边界，不形成正式业务事实、正式写回、正式收益或积分确认。

下一轮建议进入 D84：补充 `document_control.py` 的更小单元 fixture，覆盖固定 ID 保留、缺失 ID 回退和 external frontmatter 三个场景。
