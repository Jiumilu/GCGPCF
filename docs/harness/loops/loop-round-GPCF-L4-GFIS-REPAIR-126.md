---
doc_id: GPCF-DOC-9A12E19CF2
title: GPCF-L4-GFIS-REPAIR-126
project: GPCF
related_projects: [GFIS, GPC, WAES, XGD, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-126.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-126.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-126

## 轮次声明

| 字段 | 值 |
|---|---|
| loop_mode | L4 repair |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 输入

- GFIS 运行层 `formal_quotation_source_intake` 已受控，报价来源、hash 和字段抽取通过。
- GFIS 仍缺客户确认函、采购订单或合同、商业责任方回执、完整 authorization envelope、review queue、runtime intake、WAES review 和 verified artifact。
- 用户补充阿里云 ECS 当前访问机制、裸 IP FunASR/TTS 兜底入口、RustDesk 基线和 Hermes 不得修改 ECS/阿里云/Caddy/隧道/Docker 的配置变更控制要求。

## 动作

- 在 GFIS 真实项目仓新增客户/采购商业补证请求包 builder、validator、JSON、Markdown 和 GFIS 轮次记录。
- 修复 GFIS 主 runtime SOP validator 中新增状态行的接入顺序缺陷，使 `repair_required` 分支可正常输出新补证包状态。
- 在 GPCF 新增 `02-governance/ops/ecs-access-control-and-network-boundary.md`，将 ECS 当前访问机制纳入受控文档。
- 在 `02-governance/loop/LOOP_CONTROL_BOARD.md` 中增加 ECS / 阿里云 / Caddy / 隧道 / Docker 运行配置修改禁止动作。
- 回写 GPCF 状态矩阵、loop-state 和 evidence-index。

## 输出

| 输出 | 路径 |
|---|---|
| GFIS 补证请求包 builder | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/build_gfis_liaoning_yuanhang_customer_commercial_proof_request_package.py` |
| GFIS 补证请求包 validator | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_liaoning_yuanhang_customer_commercial_proof_request_package.py` |
| GFIS 补证请求包 JSON | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/liaoning-yuanhang-customer-commercial-proof-request-package.json` |
| GFIS 补证请求包 Markdown | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/liaoning-yuanhang-customer-commercial-proof-request-package.md` |
| GFIS 轮次记录 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-119.md` |
| GPCF ECS 边界文档 | `02-governance/ops/ecs-access-control-and-network-boundary.md` |

## 验证

| 命令 | 结果 |
|---|---|
| `python3 scripts/build_gfis_liaoning_yuanhang_customer_commercial_proof_request_package.py` | `requests=3 open=3 quotation_sources=1 hash_valid=1 fields_valid=15 ... runtime_sop_e2e=repair_required` |
| `python3 scripts/validate_gfis_liaoning_yuanhang_customer_commercial_proof_request_package.py` | `pass requests=3 open=3 ... customer_confirmations=0 purchase_orders=0 contracts=0 ... verified=0` |
| GFIS syntax compile | `syntax_compile=pass files=3` |
| `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`gfis_runtime_sop_e2e=repair_required`，新输出已进入主门禁 |
| `npm run test:e2e` in GFIS | 26 passed；仅 `pass_demo_only` |

## 真实性边界

- 本轮没有执行 Git push、生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、ECS/Caddy/隧道/Docker 配置修改或 accepted/integrated 状态升级。
- 报价 PDF 只能作为正式报价来源锚点，不能替代客户确认、采购订单、合同、授权 envelope、owner response、review queue、runtime intake、WAES review 或 verified artifact。
- ECS 文档只固化运行边界和变更控制，不证明公网入口全部恢复，也不代表执行过任何真实基础设施变更。

## 下一轮

GFIS-RUNTIME-SOP-E2E-120：在真实客户确认、采购订单/合同或明确授权输入出现前，继续完善补证请求的接收、授权、回执和隔离门禁；仍不得升级 SOP E2E、accepted 或 integrated。
