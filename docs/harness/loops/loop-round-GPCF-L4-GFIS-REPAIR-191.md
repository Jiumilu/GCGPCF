---
doc_id: GPCF-DOC-3F384AA9EF
title: GPCF-L4-GFIS-REPAIR-191
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-191.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-191.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-191

## 轮次目标

将 GFIS `GFIS-RUNTIME-SOP-E2E-184` 的 `CustomerRequirementOrPlatformOrder` source-of-record 结构就绪门禁回写到 GPCF 总控，确保项目群状态不把结构就绪、KDS 候选、报价单、合同审阅稿、用户口述、Loop 文档或 GFIS Demo 误判为客户订单、平台订单、运行层主键或 SOP E2E 完成。

## 输入事实

- GFIS 是现代精工 OEM 代加工生产期间和葛化自建工厂投产后共同使用的同一运行时系统。
- GFIS Demo 只能作为展示、培训和前端回归证据，不能成为 SOP 实施主体。
- `CustomerRequirementOrPlatformOrder` 当前 `submitted_files_found=0`，真实客户订单/平台订单 source-of-record 未到达。
- GFIS 主 runtime SOP validator 仍 expected exit 2 / `repair_required`。

## 本轮动作

- 回写 GPCF `02-governance/loop/LOOP_CONTROL_BOARD.md`。
- 回写 GPCF `docs/harness/loop-state.md`。
- 回写 GPCF `09-status/gpcf-project-status-matrix.md`。
- 回写 GPCF `docs/harness/minimum-closed-loop/l4-closure-score-matrix.md`。
- 回写 GPCF `docs/harness/evidence/evidence-index.md`。

## GFIS 侧证据

| 证据 | 路径/命令 | 结果 |
|---|---|---|
| py_compile | `python3 -m py_compile scripts/build_gfis_customer_requirement_platform_order_source_record_structure_readiness.py scripts/validate_gfis_customer_requirement_platform_order_source_record_structure_readiness.py scripts/validate_gfis_runtime_sop_e2e.py gcfis_custom/gcfis_custom/api.py` | pass |
| builder | `python3 scripts/build_gfis_customer_requirement_platform_order_source_record_structure_readiness.py` | `required_fields=12 allowed_source_kinds=2 forbidden_source_kinds=6 submitted_files_found=0 structure_valid_records=0` |
| validator | `python3 scripts/validate_gfis_customer_requirement_platform_order_source_record_structure_readiness.py` | pass；`runtime_primary_key_ready=0 runtime_primary_key_missing=1 review_queue=0 runtime_intake=0 waes_review=0 verified=0` |
| runtime SOP validator | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`runtime_customer_requirement_platform_order_source_record_structure_readiness=customer_requirement_platform_order_source_record_structure_ready_waiting_real_source`；`gfis_runtime_sop_e2e=repair_required` |
| Demo E2E | `npm run test:e2e` | 26 passed；`pass_demo_only` |
| diff hygiene | `git diff --check -- .` | pass |

## 结果

- `required_fields=12`
- `allowed_source_kinds=2`
- `forbidden_source_kinds=6`
- `submitted_files_found=0`
- `structure_valid_records=0`
- `runtime_primary_key_ready=0`
- `runtime_primary_key_missing=1`
- `review_queue=0`
- `runtime_intake=0`
- `waes_review=0`
- `verified=0`
- `runtime_sop_e2e=repair_required`

## 非声明

- 不声明客户订单或平台订单已取得。
- 不声明运行层主键已生成。
- 不声明 review queue、runtime intake、WAES review 或 verified artifact 已成立。
- 不声明 GFIS SOP E2E 通过。
- 不恢复 `100/100`、closed、accepted 或 integrated。

## 禁止动作确认

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行真实 KDS/WAES 写入。
- 未执行 `bench migrate` 或 schema sync。
- 未执行权限变更、部署、生产配置修改或 ECS/阿里云/Caddy/隧道/Docker 变更。

## 真实性计数

- declared_rounds=1/15
- substantive_rounds=1/15
- generated_items=7
- batch_generated=false
- substance_gate=pass
- stop_type=authorization_boundary

## 下一轮建议

`GFIS-RUNTIME-SOP-E2E-185`：围绕 `CustomerRequirementOrPlatformOrder` 建立真实源记录接收后隔离或放行尝试 hard-stop 门禁。真实 source-of-record 未到达前，继续保持 `review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`。
