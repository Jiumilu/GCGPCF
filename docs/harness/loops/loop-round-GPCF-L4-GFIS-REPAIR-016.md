---
doc_id: GPCF-DOC-BD295729DE
title: GPCF-L4-GFIS-REPAIR-016 GFIS Runtime KDS Live Input Gate
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-016.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-016.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-016 GFIS Runtime KDS Live Input Gate

## 本轮目标

把 KDS live proof 缺口从离线文档/validator 推进到 GFIS 运行层只读 API，使 GFIS runtime 自己暴露 5 类真实业务输入缺失。

## 实施内容

| 仓库 | 文件/动作 | 结果 |
|---|---|---|
| GFIS | `gcfis_custom/gcfis_custom/api.py` | 新增 `get_runtime_sop_live_input_gate` |
| GFIS | `scripts/run_gfis_runtime_sop_e2e_dry_run.py` | runner 调用 live input gate，runtime call 从 17 增至 18 |
| GFIS | `scripts/validate_gfis_runtime_sop_e2e.py` | 强制检查并输出 `runtime_live_input_gate=missing_live_business_inputs` |
| GFIS | `docs/harness/sop-e2e/README.md` 与 `loop-round-GFIS-RUNTIME-SOP-E2E-013.md` | 回写运行层门禁证据 |
| GPCF | 完整性 validator、控制板、状态矩阵、loop-state、评分矩阵、evidence index | 回写 REPAIR-016 当前事实 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `GCFIS_REPO_ROOT="$PWD" docker compose ... restart ...` in GFIS | pass；仅受控重载，未迁移 |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` in GFIS | `partial`；`runtime_calls=18 created=11 cleanup_deleted=11 runtime_gaps=12` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | exit 2 expected；`runtime_live_input_gate=missing_live_business_inputs` |
| `npm run test:e2e` in GFIS | pass；26 passed；Demo-only regression |
| `git diff --check -- .` in GFIS | pass |

## 当前结论

GFIS 运行层已能只读校验 KDS live proof 并返回 `missing_live_business_inputs`。这让真实输入缺口成为运行层可复测门禁，而不是总控文档解释。

完整 SOP E2E 仍保持 `repair_required`，原因是 5 类 verified live artifact 仍缺。项目群评分保持 79/100 repair，不恢复 100/100、accepted 或 integrated。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未执行 `bench migrate`、schema sync、数据库迁移、生产写入、真实外部 API 写入、权限变更、部署、Git push 或 accepted/integrated 状态升级。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 4 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | completed_single_substantive_round |
