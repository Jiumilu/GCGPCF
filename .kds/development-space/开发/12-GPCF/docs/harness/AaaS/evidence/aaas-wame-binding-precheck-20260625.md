---
doc_id: GPCF-DOC-AAAS-WAES-BINDING-PRECHECK-20260625
title: AaaS-WAES 绑定前置预检证据 2026-06-25
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/AaaS/evidence/aaas-waes-binding-precheck-20260625.md
source_path: docs/harness/AaaS/evidence/aaas-waes-binding-precheck-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# AaaS-WAES 绑定前置预检证据 2026-06-25

## 1. 任务标识

| 项 | 值 |
|---|---|
| task_id | `AAAS-WAES-BINDING-PRECHECK-001` |
| 结果 | `aaas_waes_binding_precheck = controlled` |
| 状态候选 | `integration_precheck_candidate` |
| 服务包 | `service-packages/examples/green-supply-chain/service-package.aaas.json` |
| packageId | `aaas.service.green-supply-chain.basic` |
| scenarioName | `GlobalCloud 绿色供应链体系` |
| WAES status | `Draft` |
| WAES decision | `candidate_only_not_published` |
| commercial status | `draft` |
| realCustomerSubscription | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

machine_status: `accepted = false`、`integrated = false`、`production_ready = false`、`customer_accepted = false`

本文只证明 AaaS 服务包具备进入 WAES 注册、授权、发布审查的本地前置候选输入，不证明 WAES 已授权、WAES 已发布、AaaS 已上架、客户可订阅或真实计费已发生。

## 2. 已执行命令

执行目录：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud AAAS`

| 命令 | 结果 |
|---|---|
| `python3 scripts/validate_service_package.py --all` | pass，checked 1，issue_count 0，high_count 0 |
| `python3 scripts/validate_metering.py --all` | pass，checked 1，issue_count 0，high_count 0 |
| `python3 scripts/validate_sla.py --all` | pass，checked 1，issue_count 0，high_count 0 |
| `python3 scripts/verify_evidence_requirements.py --all` | pass，checked 1，issue_count 0，high_count 0 |
| `python3 tools/kds-sync/validate_aaas_waes_binding_precheck.py` | 本文新增后执行 |

## 3. 绑定前置检查项

| 检查项 | 当前证据 | 结论 |
|---|---|---|
| ServicePackage 结构 | `kind = AaaSServicePackage`、`packageId = aaas.service.green-supply-chain.basic` | pass |
| WAS 维度覆盖 | `Physical`、`Rule`、`Intellectual`、`Data`、`Economic`、`Energy`、`Organization`、`SpaceTime` | pass |
| XWAIL 绑定 | `modelId = xwail.package.logistics.warehouse-basic`、`profile = SCaaS SupplyChain Profile 0.1.0` | pass |
| Ontology 回指 | `ontologyRefs` 覆盖 warehouse、shipment、green-evidence | pass |
| WAES 状态 | `Draft` | candidate only |
| WAES 决策 | `candidate_only_not_published` | candidate only |
| 计量边界 | `realBillingEnabled = false`、`billingBoundary = candidate_only_no_invoice` | pass |
| SLA 边界 | `enforcementStatus = not_enforced_local_dev` | pass |
| 证据要求 | `customerAcceptanceRequired = true`、`waesEvidenceRef = WAES Draft only; publication evidence required before delivery` | pass |
| 回滚条款 | `delete draft service package candidate before publication` | pass |

## 4. 与 WAES 的关系

| 层 | 当前状态 | 允许进入 | 不允许声明 |
|---|---|---|---|
| AaaS | `integration_precheck_candidate` | WAES 注册、授权、发布审查的候选输入 | 不声明客户可订阅、不声明真实计费 |
| WAES | `Draft / repair_required / authorization_boundary` | 后续在授权后执行 lint/runtime 修复和 publication gate | 不声明 WAES 已授权或已发布 |
| XWAIL | `integration_precheck_candidate` | 作为 AaaS 服务包的模型契约候选输入 | 不声明完整工具链或生产发布 |
| WAS/Ontology | `xwail_mapping_candidate` | 作为语义映射候选输入 | 不声明真实业务事实 |

## 5. 依赖传导

| 依赖边 | 本轮影响 |
|---|---|
| `XWAIL -> AaaS` | AaaS 服务包已通过本地 ServicePackage/Metering/SLA/EvidenceRequirement 检查，可作为 XWAIL 契约服务化候选输入 |
| `WAES -> AaaS` | 仍受 WAES 未授权、未发布、lint/runtime 修复边界约束，AaaS 只能保持候选 |
| `WAES -> XWAIL -> AaaS` | contract precheck 与 binding precheck 均为本地候选，不解除 WAES publication gate |
| `GFIS/GPC/PVAOS -> SCaaS` | 为 GlobalCloud 绿色供应链体系提供 AaaS 服务包候选，不证明真实客户场景交付 |

## 6. 回滚与降级

- 若任一 AaaS 本地 validator 失败，回滚本文和总控状态文本，AaaS 保持 `ready_for_review / local_dev_boundary`。
- 若 WAES 后续拒绝注册、授权或发布，AaaS 保持 `candidate_only_not_published`，不得升级为 `subscribable`。
- 若真实订阅、真实计费、生产 SLA 或客户验收缺证据，必须保持 `commercial.status = draft`。
- 若 XWAIL 模型、Profile 或 WAS/Ontology 映射变化，必须重新执行本预检。

## 7. 禁止声明

- 不声明 WAES 已授权。
- 不声明 WAES 已发布。
- 不声明 AaaS 已上架。
- 不声明客户可订阅。
- 不声明真实计费、真实结算或 SLA 强制执行。
- 不声明 GFIS/GPC/PVAOS/SCaaS 真实业务闭环完成。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
