---
doc_id: GPCF-LOOP-GCKF-P0-D86-001
title: Loop Round GPCF-GCKF-P0-D86-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D86-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D86-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GCKF-P0-D86-001

## 本轮目标

把 Loop 文档门禁的失败原因机器化，使 `rework_required` 能直接区分中文本地化债务、固定 `doc_id` 漂移、缺元数据、缺 README、硬失败、KDS Token 阻断和 KDS 镜像覆盖缺口。

## 输入

- `tools/kds-sync/loop_document_gate.py`
- D85 固定 `doc_id` 漂移门禁结果
- 当前 `loop_document_gate.py --check-only` 输出

## 动作

- 新增 `build_gate_reasons(...)`。
- 在门禁 JSON summary 中加入 `gate_reasons`。
- 在健康报告总览中展示“门禁原因”。
- 新增 `scripts/api/validate_gckf_p0_loop_document_gate_reasons_check.py`。

## 输出

- `tools/kds-sync/loop_document_gate.py`
- `scripts/api/validate_gckf_p0_loop_document_gate_reasons_check.py`
- `docs/gc-knowledge-fabric/loop-document-gate-reasons-check-v0.1.md`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D86-001.md`

## 检查

```text
gckf_p0_loop_document_gate_reasons_check=pass
loop_gate_status=rework_required
gate_reasons=localization_debt
fixed_doc_id_drift=false
execution_mode=read_only_check_only
```

`python3 tools/kds-sync/loop_document_gate.py --check-only` 当前摘要包含：

```json
{
  "gate": "rework_required",
  "gate_reasons": ["localization_debt"],
  "localization_debt": true,
  "fixed_doc_id_drift": false
}
```

## 反馈

本轮完成的是文档治理可解释性增强。当前全局文档门禁仍为 `rework_required`，原因已明确为 `localization_debt`。这不改变 GC-Knowledge Fabric 的 candidate/no-write 边界，不改变 GFIS 真实业务链路 `repair_required` 判定，不产生正式写回、收益分配、积分确认或委员会裁决。

下一轮建议 D87：基于 `gate_reasons` 建立修复队列或趋势报告，使文档治理债务可以分组追踪。
