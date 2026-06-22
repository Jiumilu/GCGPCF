---
doc_id: GPCF-LOOP-GCKF-P0-D85-001
title: Loop Round GPCF-GCKF-P0-D85-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D85-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D85-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GCKF-P0-D85-001

## 本轮目标

把固定 `doc_id` 漂移检测纳入 Loop 文档门禁，使 D83/D84 的机制修复不只依赖人工单独运行验证脚本。

## 输入

- `tools/kds-sync/loop_document_gate.py`
- `scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py`
- `scripts/api/validate_gckf_p0_document_control_doc_id_unit_fixtures.py`

## 动作

- 在 `loop_document_gate.py` 的 `checks` 中加入 `fixed_doc_id_preservation`。
- 在 Loop 门禁摘要中加入 `fixed_doc_id_drift`。
- 在健康报告总览中加入固定 `doc_id` 漂移字段。
- 新增 `scripts/api/validate_gckf_p0_loop_document_gate_fixed_doc_id_check.py`。

## 输出

- `tools/kds-sync/loop_document_gate.py`
- `scripts/api/validate_gckf_p0_loop_document_gate_fixed_doc_id_check.py`
- `docs/gc-knowledge-fabric/loop-document-gate-fixed-doc-id-drift-check-v0.1.md`

## 检查

```text
gckf_p0_loop_document_gate_fixed_doc_id_check=pass
loop_gate_status=rework_required
fixed_doc_id_drift=false
execution_mode=read_only_check_only
```

## 反馈

本轮仍不改变 GC-Knowledge Fabric 的业务事实状态。`loop_document_gate.py --check-only` 仍因 `localization_debt=true` 返回 `rework_required`，但固定 ID 漂移已被门禁显式报告为 `false`。

下一轮建议 D86：细化 Loop 门禁 failure reason，使 `rework_required` 能直接区分中文化债务、固定 ID 漂移、缺元数据、缺 README 等原因。
