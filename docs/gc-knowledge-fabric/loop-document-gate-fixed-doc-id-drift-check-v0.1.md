---
doc_id: GPCF-DOC-GCKFLOOPDOCUMENTGATEFIXEDDOCIDDRIFTCHECKV01
title: GC-Knowledge Fabric P0 Loop 文档门禁固定 doc_id 漂移检查 v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/loop-document-gate-fixed-doc-id-drift-check-v0.1.md
source_path: docs/gc-knowledge-fabric/loop-document-gate-fixed-doc-id-drift-check-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Loop 文档门禁固定 doc_id 漂移检查 v0.1

## 定位

本文件记录 D85：将 D83/D84 的固定 `doc_id` 漂移检测接入 `loop_document_gate.py --check-only` 摘要，使 Loop 文档门禁能够直接暴露固定编号破坏风险。

## 变更内容

- `loop_document_gate.py` 新增 `fixed_doc_id_preservation` 检查项。
- 检查项调用 `scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py`。
- `summary` 新增 `fixed_doc_id_drift`。
- 健康报告总览新增“固定 doc_id 漂移”字段。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_loop_document_gate_fixed_doc_id_check.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 验证结果

```text
gckf_p0_loop_document_gate_fixed_doc_id_check=pass
loop_gate_status=rework_required
fixed_doc_id_drift=false
execution_mode=read_only_check_only
```

`loop_gate_status=rework_required` 的当前原因仍是全仓中文化债务 `localization_debt=true`，不是固定 ID 漂移。

## 受控边界

- 本轮只增强 Loop 文档门禁可见性。
- 不写入真实 KDS API。
- 不改变 D75-D84 的 candidate/no-write 状态。
- 不形成正式业务事实、正式写回、收益分配、积分确认或委员会裁决。

## 下一步

D86 可以继续把 `fixed_doc_id_drift` 接入更细的健康报告趋势或 failure reason 列表，使 rework 原因更容易定位。
