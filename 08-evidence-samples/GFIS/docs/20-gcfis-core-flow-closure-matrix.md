---
doc_id: GPCF-DOC-A68BB0BF02
title: GlobalCloud GFIS 核心流程闭环与集成边界矩阵
project: GFIS
related_projects: [GFIS, GPC, PVAOS, WAES]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/docs/20-gcfis-core-flow-closure-matrix.md
source_path: 08-evidence-samples/GFIS/docs/20-gcfis-core-flow-closure-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud GFIS 核心流程闭环与集成边界矩阵

适用基线：GFIS-QB-2026-06-05-B1
验证脚本：`python3 scripts/validate_gcfis_core_flows.py`

本文档用于关闭第一轮执行闭环中的核心流程、smoke 验证和集成边界 P1。结论只表示当前验证包具备可复跑验收证据，不表示云 SaaS、供应链金融或外部绿色供应链平台已经生产接通。

运行主体口径：GFIS 运行层是工厂的运行主体。核心流程和 SOP 的验收必须以 GFIS 运行层中的单据事实、运行态 API、工作流、权限和报表为准。前端 Demo 只作为可视化展示和浏览器回归入口，不作为 SOP 实现主体，也不能替代运行层证据。

## 1. 核心流程矩阵

| 流程 | 页面入口 | 前端证据 | 后端/API 证据 | 数据证据 | 验收边界 | 当前状态 |
|---|---|---|---|---|---|---|
| 平台订单分发 | `view-command`、`view-supply` | `ORD-2404`、`F-GEHUA`、调度建议评分 94 | `create_dispatch_suggestion` 已通过真实运行态 HTTP 写入验证，只写入 `GCFIS Dispatch Suggestion` | `gcfis_v05_green_supply_chain_api_model.json` 调度建议输出，运行态返回 `dispatch_created=1` | 只生成建议，必须工厂确认，不改写生产工单 | 已验证 |
| 工厂本地生产执行 | `view-factory` | 葛化工厂、`WO-2404-EX-A2`、`QI-2404-FINAL` | v0.3 本地闭环脚本和结果 | `v03_local_loop_result.json` 中 BOM、工单、Job Card、质检、库存、发货均为提交态 | 证明本地 ERPNext 单厂闭环，不证明多工厂生产自动派工 | 已验证 |
| 发货签收回传 | `view-command`、`view-finance` | `DN-2404`、`POD-2404 已回传` | `get_shipment_evidence` 为只读接口 | v0.5 签收与应收证据链 | 只读取发货/签收证据，不自动确认资金事实 | 已验证 |
| 金融凭证链 | `view-finance` | `FIN-002`、`L4_blocked`、只生成建议 | `create_finance_evidence_package` 已通过真实运行态 HTTP 写入验证，返回 `finance_gate=L4_blocked` | `finance_evidence_package_sample.json`，运行态返回 `finance_package_created=1` | 不自动授信、不自动融资、不自动付款、不自动回款 | 已验证 |
| 云端 SaaS 汇总 | `view-cloud` | 多工厂汇总、同步队列 | v0.4 SaaS 聚合模型 | `v04_cloud_saas_validation_result.json` 工厂数 3、同步事件数 11 | 当前为模型验证，不等于真实云端租户系统上线 | 边界已锁定 |

## 2. 主闭环路径

当前已验证主路径：

```text
ORD-2404 平台订单
-> F-GEHUA 葛化示范工厂
-> WO-2404-EX-A2 生产工单完成
-> QI-2404-FINAL 成品质检已接受
-> 成品入库与发货出库提交
-> DN-2404 / POD-2404 签收回传
-> FIN-002 金融凭证包建议
-> L4_blocked 人工确认门禁
```

验收结果：

- 核心流程有 GFIS 运行层单据和运行态 API 证据。
- 主流程有可识别前端展示，但展示只作为辅助证据。
- 本地生产执行有提交态 ERPNext 证据。
- 绿链调度和金融动作有 API/模型边界。
- 绿链调度建议创建和工厂确认状态流转已通过真实运行态 HTTP 写入验证。
- 金融凭证包建议已通过真实运行态 HTTP 写入验证，并继续保持 `L4_blocked` 与人工确认。
- 金融动作保持人工确认，不自动形成资金事实。

## 3. 集成边界

| 集成 | 当前可验收内容 | 明确不包含 | 上线前仍需补充 |
|---|---|---|---|
| 云端 SaaS | 多工厂、租户、同步事件、聚合域模型验证 | 真实云端租户后台、云数据库、生产 API 网关 | 云端环境、租户管理、审计日志、同步队列重试 |
| 绿色供应链 | 调度建议 API 草案、工厂确认状态机、禁止动作 | 外部平台真实调用、生产鉴权、线上 API 路由 | API 网关、认证授权、幂等、限流、错误处理 |
| 供应链金融 | FIN-002 凭证链、风险建议、L4 门禁 | 自动授信、自动融资、自动付款、自动回款 | 金融机构接口、风控规则、合规审批、资金事实确认 |
| ERPNext 本地站点 | 单厂生产、库存、质检、发货提交态证据 | 多工厂自动排产、跨厂自动拆单 | 角色验收、异常流程、长周期数据回归 |

## 4. 验证命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gcfis_core_flows.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gcfis_api_contract.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gcfis_artifacts.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gcfis_runtime_api.py
```

通过标准：

- `core_flows=5`。
- 主路径包含 `ORD-2404->F-GEHUA->WO/QI/Stock/DN->POD-2404->FIN-002`。
- 集成边界显示为 `cloud_saas:model green_supply_chain:api_contract finance:L4_blocked`。
- 运行态 API 输出包含 `write_paths=3`、`dispatch_created=1`、`confirmation_status=已接受`、`finance_package_created=1`、`finance_gate=L4_blocked`。
- `npm run test:e2e` 只用于 Demo 展示层浏览器回归；SOP 完成度以运行层验证脚本、运行态 API、提交态单据和 UAT 签收为准。
