---
doc_id: GPCF-DOC-GCKFLOOPDOCUMENTGATEREASONSCHECKV01
title: GC-Knowledge Fabric P0 Loop Document Gate Reasons Check v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/loop-document-gate-reasons-check-v0.1.md
source_path: docs/gc-knowledge-fabric/loop-document-gate-reasons-check-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Loop Document Gate Reasons Check v0.1

## 定位

本文件记录 D86：为 `loop_document_gate.py --check-only` 增加结构化 `gate_reasons`，让 `rework_required`、`blocked` 或 `partial` 的原因可以被 LOOP、Harness 和后续审计脚本直接读取。

## 变更内容

- `loop_document_gate.py` 新增 `build_gate_reasons(...)`。
- `summary` 新增 `gate_reasons`。
- 健康报告总览新增“门禁原因”字段。
- 新增只读验证脚本 `scripts/api/validate_gckf_p0_loop_document_gate_reasons_check.py`。

## 当前语义

`gate_reasons` 只解释文档门禁原因，不改变业务事实状态。

当前 `loop_document_gate.py --check-only` 输出：

```text
gate=rework_required
gate_reasons=localization_debt
fixed_doc_id_drift=false
```

这表示当前重工原因是已知中文本地化债务，不是固定 `doc_id` 漂移，也不是 GFIS 业务链路完成或失败的新结论。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_loop_document_gate_reasons_check.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 验证结果

```text
gckf_p0_loop_document_gate_reasons_check=pass
loop_gate_status=rework_required
gate_reasons=localization_debt
fixed_doc_id_drift=false
execution_mode=read_only_check_only
```

## 受控边界

- 本轮只增强文档门禁可解释性。
- 不写入真实 KDS API。
- 不执行 GFIS/GPC/ERP/MES 业务写回。
- 不把 AI、validator、文档门禁或 LOOP 记录转为正式事实。
- 不改变 `GFIS real_business_lane=repair_required`。

## 下一步

D87 可继续把 `gate_reasons` 纳入趋势报告或按原因分组的修复队列，但仍只能作为治理输入，不能替代人工确认、委员会裁决或真实业务验收。
