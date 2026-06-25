---
doc_id: GPCF-DOC-AAAS-SERVICE-RUNTIME-20260625
title: AaaS 最小 ServicePackage/Metering/SLA/EvidenceRequirement 运行证据 2026-06-25
project: GPCF
related_projects: [GPCF, AaaS, XWAIL, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/AaaS/evidence/aaas-service-runtime-20260625.md
source_path: docs/harness/AaaS/evidence/aaas-service-runtime-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# AaaS 最小 ServicePackage/Metering/SLA/EvidenceRequirement 运行证据 2026-06-25

## 1. 证据定位

本文登记 `AAAS-SERVICE-RUNTIME-001` 的本地真实执行结果。

本文只证明 `GlobalCloud AaaS` 仓已建立最小本地 ServicePackage、Metering、SLA 和 EvidenceRequirement 验证命令入口。本文不声明真实计费、真实结算、SLA 强制执行、客户订阅、客户交付、WAES 发布或客户验收完成。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| AaaS 仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud AAAS` |
| 执行日期 | 2026-06-25 |
| 缺口复现目录 | `/tmp/aaas-service-runtime-20260625-pre` |
| 通过复跑目录 | `/tmp/aaas-service-runtime-20260625-091506` |
| 初始状态 | `scripts/validate_service_package.py`、`scripts/validate_metering.py`、`scripts/validate_sla.py`、`scripts/verify_evidence_requirements.py` 均不存在 |
| 本轮修改边界 | 只新增最小本地 Draft 服务包、JSON schema 占位和四个本地验证脚本 |

## 3. 初始失败

首次运行规划命令失败：

```text
python3 scripts/validate_service_package.py --all
can't open file .../scripts/validate_service_package.py: [Errno 2] No such file or directory

python3 scripts/validate_metering.py --all
can't open file .../scripts/validate_metering.py: [Errno 2] No such file or directory

python3 scripts/validate_sla.py --all
can't open file .../scripts/validate_sla.py: [Errno 2] No such file or directory

python3 scripts/verify_evidence_requirements.py --all
can't open file .../scripts/verify_evidence_requirements.py: [Errno 2] No such file or directory
```

## 4. 新增实现

| 类型 | 文件 |
|---|---|
| 共享校验逻辑 | `scripts/aaas_common.py` |
| ServicePackage 校验命令 | `scripts/validate_service_package.py` |
| Metering 校验命令 | `scripts/validate_metering.py` |
| SLA 校验命令 | `scripts/validate_sla.py` |
| EvidenceRequirement 校验命令 | `scripts/verify_evidence_requirements.py` |
| 最小绿色供应链服务包 | `service-packages/examples/green-supply-chain/service-package.aaas.json` |
| JSON Schema 占位 | `schemas-json/aaas-service-package.schema.json` |

最小校验覆盖：

- WAS/Ontology/XWAIL/Profile/ServicePackage 基线必填。
- `waes.status` 受控，当前保持 `Draft`。
- XWAIL 模型、版本、Profile 和 `ontologyRefs` 必填。
- WAS 八维：`Physical`、`Rule`、`Intellectual`、`Data`、`Economic`、`Energy`、`Organization`、`SpaceTime`。
- 服务范围、输入、输出、状态转换、失败补偿、退出条款必填。
- Metering 必须声明 unit、samplingMethod、billingBoundary、disputeHandling、source，并保持 `realBillingEnabled=false`。
- SLA 必须声明 target、monitoringSource、exceptionPath、reportingPeriod，并保持 `enforcementStatus=not_enforced_local_dev`。
- EvidenceRequirement 必须声明 sourceSystem、auditTrail、retention、WAES evidence、rollback evidence、requiredRecords，并保持 `customerAcceptanceRequired=true`。

## 5. 复跑命令与结果

| 命令 | 结果 |
|---|---|
| `python3 scripts/validate_service_package.py --all` | pass，`checked=1 issue_count=0 high_count=0` |
| `python3 scripts/validate_metering.py --all` | pass，`checked=1 issue_count=0 high_count=0` |
| `python3 scripts/validate_sla.py --all` | pass，`checked=1 issue_count=0 high_count=0` |
| `python3 scripts/verify_evidence_requirements.py --all` | pass，`checked=1 issue_count=0 high_count=0` |

命令输出均包含边界：

```text
This validates local AaaS package structure only; it does not prove real billing, settlement, SLA enforcement, customer delivery, or WAES publication.
```

## 6. 状态建议

```text
aaas_service_runtime = verified_with_local_dev_boundary
aaas_service_package_gate = pass
aaas_metering_gate = pass
aaas_sla_gate = pass
aaas_evidence_requirement_gate = pass
aaas_checked_service_packages = 1
aaas_status_candidate = ready_for_review
waes_status = Draft
commercial_status = draft
real_billing = false
customer_subscription = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 7. 保留边界

| 边界 | 说明 |
|---|---|
| local dev only | 本轮只证明本地 Draft 服务包和最小命令入口通过 |
| no WAES publication | `waes.status=Draft`，未注册、未授权、未发布 |
| no real billing | `realBillingEnabled=false`，没有真实账单、结算或发票 |
| no SLA enforcement | `enforcementStatus=not_enforced_local_dev`，没有生产监控或 SLA 赔付 |
| no customer delivery | 没有客户订阅、客户验收人、验收场景或签收证据 |

## 8. 下一步

1. 将 AaaS 最小 ServicePackage 作为 `WAES -> XWAIL -> AaaS` 链路的服务化候选输入。
2. 后续需要 WAES 授权/发布后，才能把服务包从 `draft` 推进到 `pilot` 或 `subscribable`。
3. 后续需要真实客户场景和 source-of-record，才能声明交付、计费、SLA 或客户验收。
