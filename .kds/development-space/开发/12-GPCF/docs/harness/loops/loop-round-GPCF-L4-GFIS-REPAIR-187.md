---
doc_id: GPCF-DOC-F30AEE320E
title: GPCF-L4-GFIS-REPAIR-187
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-187.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-187.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-187

## 本轮目标

按 Loop 新真实性规则，只做 1 个真实实质轮次：把 GFIS `GFIS-RUNTIME-SOP-E2E-180` 的 KDS 受控资料到 GFIS 运行层主键就绪门禁纳入 GPCF 总控状态，同时保持 GFIS/GPCF `repair_required`。

## 输入

| 输入 | 说明 |
|---|---|
| GFIS `AGENTS.md` / README / Manifest / docs / git status | 已在 GFIS 真实项目仓读取并按运行层主体边界执行 |
| GFIS KDS coverage / SOP stage matrix / 62-slot schema | 本轮主键就绪门禁的真实输入 |
| GFIS 180 builder / validator / API / 主 validator | 本轮真实落地对象 |
| 用户主体口径确认 | GFIS 是现代精工 OEM 当前运行和葛化自建工厂未来运行的同一运行时系统 |

## 输出

| 输出 | 结论 |
|---|---|
| GFIS JSON/Markdown evidence | KDS 到运行层主键就绪门禁已生成 |
| GFIS validator | 项目级 validator pass |
| GFIS runtime SOP validator | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GFIS Demo E2E | 26 passed；`pass_demo_only` |
| GPCF evidence index | 已登记本轮证据 |
| GPCF loop-state / control board / status matrix / L4 score matrix | 已回写本轮状态，继续 repair_required |

## 验证

| 命令 | 结果 |
|---|---|
| `python3 -m py_compile ...` in GFIS | pass |
| `python3 scripts/build_gfis_kds_to_runtime_primary_key_readiness_gate.py && python3 scripts/validate_gfis_kds_to_runtime_primary_key_readiness_gate.py` in GFIS | pass；`runtime_primary_key_ready=0 runtime_primary_key_missing=12 runtime_documents_allowed=0 runtime_sop_e2e=repair_required` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增 `runtime_kds_to_runtime_primary_key_readiness_gate=...runtime_primary_key_missing=12...`；`gfis_runtime_sop_e2e=repair_required` |
| `npm run test:e2e` in GFIS | 26 passed；`pass_demo_only` |
| `git diff --check -- .` in GFIS | pass |

## 非完成声明

- 本轮只证明 KDS 受控资料不能替代 GFIS 运行层主键。
- 本轮不创建客户订单、样品签收、转量产批准、原料批次、FactoryOrder、WorkOrder、DeliveryNote、POD、WAES confirmation、KDS write receipt、金融事实、accepted 或 integrated。
- 本轮不执行生产写入、真实外部 API、数据库迁移、schema sync、权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 变更或 Git push。

## 真实计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 11 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |
