---
doc_id: GPCF-DOC-BB2AAEFD1C
title: GPCF-L4-GFIS-REPAIR-160
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-160.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-160.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-160

## 输入

- 用户确认：葛化工厂仍在建设阶段，辽宁远航合同链当前使用现代精工工厂进行 OEM 代加工；GFIS 是现代精工代加工生产阶段和葛化自建工厂投产后的同一运行时系统。
- GFIS `GFIS-RUNTIME-SOP-E2E-152` 已证明 8 个合同/方案 Word 源文件可映射到 GFIS SOP 12 阶段。
- 合同链仍缺签章完成件、KDS write receipt、WAES confirmation 和 GFIS 运行层单据事实。

## 本轮目标

在真实 GFIS 项目仓落地一个实质门禁：把合同链阶段输入映射转为运行层单据创建前置预检，确保缺少 live proofs 时不得创建或写入 GFIS FactoryOrder、WorkOrder、DeliveryNote、POD、金融候选或 KDS/WAES 回指事实。

## 动作

- GFIS 新增 `scripts/build_gfis_liaoning_yuanhang_runtime_document_creation_preflight.py`。
- GFIS 新增 `scripts/validate_gfis_liaoning_yuanhang_runtime_document_creation_preflight.py`。
- GFIS 新增 `docs/harness/sop-e2e/evidence/liaoning-yuanhang-runtime-document-creation-preflight.json`。
- GFIS 新增 `docs/harness/sop-e2e/liaoning-yuanhang-runtime-document-creation-preflight.md`。
- GFIS 新增只读 API `get_runtime_liaoning_yuanhang_runtime_document_creation_preflight`。
- GFIS 主 runtime SOP validator 已接入 `runtime_liaoning_yuanhang_runtime_document_creation_preflight`。
- GPCF 回写控制板、项目状态矩阵、loop-state、evidence index。

## 验证

| 命令 | 结果 |
|---|---|
| `python3 scripts/build_gfis_liaoning_yuanhang_runtime_document_creation_preflight.py` in GFIS | pass |
| `python3 -m py_compile gcfis_custom/gcfis_custom/api.py scripts/build_gfis_liaoning_yuanhang_runtime_document_creation_preflight.py scripts/validate_gfis_liaoning_yuanhang_runtime_document_creation_preflight.py scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | pass |
| `python3 scripts/validate_gfis_liaoning_yuanhang_runtime_document_creation_preflight.py` in GFIS | pass |
| `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增 `runtime_liaoning_yuanhang_runtime_document_creation_preflight`，总体仍为 `repair_required` |

## 输出

```text
liaoning_yuanhang_runtime_document_creation_preflight=pass objects=12 blocked=12 allowed=0 factory_order_allowed=0 work_order_allowed=0 delivery_note_allowed=0 pod_allowed=0 finance_allowed=0 evidence_backlink_allowed=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 state=runtime_document_creation_preflight_blocked_waiting_live_proofs runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_runtime_document_creation_preflight=runtime_document_creation_preflight_blocked_waiting_live_proofs:objects=12:blocked=12:allowed=0:factory_order_allowed=0:work_order_allowed=0:delivery_note_allowed=0:pod_allowed=0:finance_allowed=0:evidence_backlink_allowed=0:review_queue=0:runtime_intake=0:waes_review=0:verified=0
```

## 边界

- 未写真实 KDS、WAES、生产系统或外部 API。
- 未执行 `bench migrate`、schema sync、权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 变更。
- 未创建 GFIS FactoryOrder、WorkOrder、QualityInspection、InventoryBatch、DeliveryNote、POD、金融事实、KDS/WAES 回指事实、review queue、runtime intake、verified artifact、accepted 或 integrated。

## 本轮真实计数

- declared_rounds: `1/15`
- substantive_rounds: `1/15`
- generated_items: `7`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`
