---
doc_id: GPCF-DOC-XWAIL-WAES-AAAS-CONTRACT-PRECHECK-20260625
title: XWAIL-WAES-AaaS 契约预检证据 2026-06-25
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/XWAIL/evidence/xwail-waes-aaas-contract-precheck-20260625.md
source_path: docs/harness/XWAIL/evidence/xwail-waes-aaas-contract-precheck-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# XWAIL-WAES-AaaS 契约预检证据 2026-06-25

## 1. 范围

本文在本地集成预检边界内收口 `XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001`。

本文检查当前 XWAIL 最小 Validator/XAP 命令，以及当前 AaaS ServicePackage/Metering/SLA/EvidenceRequirement 命令，是否可以共同作为后续 WAES 注册、授权和发布门禁的候选输入。

本文不执行 WAES 发布，也不证明生产绑定已经完成。

## 2. 已执行命令

| 项目 | 命令 | 状态 | 关键输出 |
|---|---|---|---|
| XWAIL | `python3 scripts/validate_xwail.py --all` | pass | `gate=xwail_min_validator`、`checked=2`、`issue_count=0`、`high_count=0` |
| XWAIL | `python3 scripts/build_xap.py --check` | pass | `gate=xap_build_check`、`checked=1`、`issue_count=0`、`high_count=0`、`check_only=true` |
| XWAIL | `python3 scripts/verify_xap.py --all` | pass | `gate=xap_verify`、`checked=1`、`issue_count=0`、`high_count=0` |
| AaaS | `python3 scripts/validate_service_package.py --all` | pass | `gate=aaas_service_package`、`checked=1`、`issue_count=0`、`high_count=0` |
| AaaS | `python3 scripts/validate_metering.py --all` | pass | `gate=aaas_metering`、`checked=1`、`issue_count=0`、`high_count=0` |
| AaaS | `python3 scripts/validate_sla.py --all` | pass | `gate=aaas_sla`、`checked=1`、`issue_count=0`、`high_count=0` |
| AaaS | `python3 scripts/verify_evidence_requirements.py --all` | pass | `gate=aaas_evidence_requirements`、`checked=1`、`issue_count=0`、`high_count=0` |

## 3. 契约候选摘要

| 项 | 值 |
|---|---|
| task_id | `XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001` |
| result | `xwail_waes_aaas_contract_precheck = pass` |
| xwail_status_candidate | `integration_precheck_candidate` |
| aaas_status_candidate | `integration_precheck_candidate` |
| waes_status | `repair_required / authorization_boundary` |
| commands_passed | 7 |
| commands_failed | 0 |
| dependency_edge | `WAES -> XWAIL -> AaaS` |
| validator | `tools/kds-sync/validate_xwail_waes_aaas_contract_precheck.py` |

## 4. 边界

本文只证明：

- 当前 XWAIL 本地 validator、XAP build check 和 XAP verify 命令通过；
- 当前 AaaS 本地 ServicePackage、Metering、SLA 和 EvidenceRequirement 命令通过；
- XWAIL 与 AaaS 可以作为本地候选输入进入 `integration_precheck_candidate` 审查。

本文不证明：

- WAES lint/runtime 已修复；
- WAES 注册、授权、发布或 release 已完成；
- AaaS 客户订阅、真实计费、结算或 SLA 强制执行已完成；
- SCaaS 客户交付已完成；
- accepted、integrated、production_ready 或 customer_accepted 已完成。

```text
accepted = false
integrated = false
production_ready = false
customer_accepted = false
waes_publication = false
aaas_real_billing = false
customer_subscription = false
```
