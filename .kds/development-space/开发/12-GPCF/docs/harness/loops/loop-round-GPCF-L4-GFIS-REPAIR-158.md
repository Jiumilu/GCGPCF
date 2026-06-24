---
doc_id: GPCF-DOC-09D622EB71
title: GPCF-L4-GFIS-REPAIR-158
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-158.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-158.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

---
doc_id: GPCF-DOC-LOOP-GFIS-REPAIR-158
title: GPCF-L4-GFIS-REPAIR-158
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: loop-governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-158.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-158.md
sync_direction: bidirectional
last_reviewed: 2026-06-16
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-158

## 输入

- 用户确认：GFIS 是现代精工 OEM 代加工生产阶段和葛化自建工厂投产后的同一运行时系统。
- 用户要求：5 类真实凭证缺口可通过 KDS 检索，但不得用批量文档或 KDS 候选冒充多轮进展或 live proof。
- GFIS 上一轮 `GFIS-RUNTIME-SOP-E2E-150` 已固定运行主体口径，完整 SOP E2E 仍为 `repair_required`。

## 本轮目标

在真实 GFIS 项目仓落地一个实质门禁：把 KDS 受控资料映射到 GFIS SOP 12 个阶段，证明 12/12 阶段已有 KDS 受控引用输入，同时保持 live proof 0/12、5 类真实业务输入缺口不变。

## 动作

- GFIS 新增 `scripts/build_gfis_kds_sop_stage_coverage_matrix.py`。
- GFIS 新增 `scripts/validate_gfis_kds_sop_stage_coverage_matrix.py`。
- GFIS 新增 `docs/harness/sop-e2e/evidence/gfis-kds-sop-stage-coverage-matrix.json`。
- GFIS 新增 `docs/harness/sop-e2e/gfis-kds-sop-stage-coverage-matrix.md`。
- GFIS 新增只读 API `get_runtime_kds_sop_stage_coverage_matrix`。
- GFIS 主 runtime SOP validator 已接入 `runtime_kds_sop_stage_coverage_matrix`。
- GPCF 回写控制板、项目状态矩阵、loop-state、evidence index。

## 验证

| 命令 | 结果 |
|---|---|
| `python3 scripts/build_gfis_kds_sop_stage_coverage_matrix.py` in GFIS | pass |
| `python3 -m py_compile scripts/build_gfis_kds_sop_stage_coverage_matrix.py scripts/validate_gfis_kds_sop_stage_coverage_matrix.py scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | pass |
| `python3 scripts/validate_gfis_kds_sop_stage_coverage_matrix.py` in GFIS | pass |
| `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增 `runtime_kds_sop_stage_coverage_matrix`，总体仍 `repair_required` |

## 输出

```text
gfis_kds_sop_stage_coverage_matrix=pass sop_stages=12 kds_controlled_stages=12 live_proof_stages=0 missing_live_business_inputs=5 review_queue=0 runtime_intake=0 waes_review=0 verified=0 state=kds_sop_stage_coverage_ready_live_proof_missing runtime_sop_e2e=repair_required
runtime_kds_sop_stage_coverage_matrix=kds_sop_stage_coverage_ready_live_proof_missing:sop_stages=12:kds_controlled_stages=12:live_proof_stages=0:missing_live_business_inputs=5:review_queue=0:runtime_intake=0:waes_review=0:verified=0
```

## 边界

- 未写真实 KDS、WAES、生产系统或外部 API。
- 未执行 `bench migrate`、schema sync、权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 变更。
- 未创建 review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated。
- KDS 受控引用只作为检索和采集输入，不替代客户订单、签样、原料批次、生产记录、POD、WAES confirmation 或 KDS write receipt。

## 本轮真实计数

- declared_rounds: `1/15`
- substantive_rounds: `1/15`
- generated_items: `6`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`
