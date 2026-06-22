---
doc_id: GPCF-DOC-424C01C82A
title: GPCF-L4-GFIS-REPAIR-019 GFIS Runtime Sample Request Gate
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-019.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-019.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-019 GFIS Runtime Sample Request Gate

## 本轮目标

把 GFIS 运行层 SOP 12 段门禁中的 `sample_request` 阻塞拆成运行层可复测的样品申请/样品质检/客户签样/转量产前置门禁。

## 实施内容

| 仓库 | 文件/动作 | 结果 |
|---|---|---|
| GFIS | `gcfis_custom/gcfis_custom/api.py` | 新增 `get_runtime_sample_request_gate` 只读 API |
| GFIS | `scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 调用 sample request gate，runtime call 从 19 增至 20 |
| GFIS | `scripts/validate_gfis_runtime_sop_e2e.py` | 强制检查并输出 `runtime_sample_request_gate=blocked` |
| GFIS | `docs/harness/sop-e2e/*` 与 `loop-round-GFIS-RUNTIME-SOP-E2E-015.md` | 回写样品申请门禁证据 |
| GPCF | 完整性 validator、控制板、状态矩阵、loop-state、evidence index | 回写 REPAIR-019 当前事实 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` in GFIS | pass |
| `GCFIS_REPO_ROOT="$PWD" docker compose ... restart ...` in GFIS | pass；仅受控重载，未迁移 |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/harvest_gfis_kds_gehu_inputs.py` in GFIS | `kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=5` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`；`runtime_calls=20 created=11 cleanup_deleted=11 runtime_gaps=14` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`runtime_sample_request_gate=blocked` |

## 当前运行层阻塞

`SampleRequestGate` 当前阻塞 4 个前置项：

- `sample_request`
- `sample_quality`
- `customer_sample_approval`
- `production_release_gate`

完整 SOP E2E 仍保持 `repair_required`。项目群评分保持 79/100 repair，不恢复 100/100、accepted 或 integrated。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未执行 `bench migrate`、schema sync、数据库迁移、生产写入、真实外部 API 写入、权限变更、部署、Git push 或 accepted/integrated 状态升级。
- 未把样品候选写成客户签样完成，也未把转量产门禁写成通过。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 4 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | completed_single_substantive_round |
