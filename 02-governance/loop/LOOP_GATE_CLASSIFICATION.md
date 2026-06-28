---
doc_id: GPCF-DOC-LOOP-GATE-CLASSIFICATION-V11
title: LOOP Gate Classification
project: WAES
related_projects: [GFIS, WAES]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GATE_CLASSIFICATION.md
source_path: 02-governance/loop/LOOP_GATE_CLASSIFICATION.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# LOOP Gate Classification

## v1.1 Gate Levels

P0 硬阻断：

- secret/token 泄露。
- 真实生产写入、真实外部 API 写入、未授权 live API。
- schema migrate、bench migrate、数据库迁移、删除或不可逆动作。
- accepted、integrated、production_ready、customer_accepted 等状态提升。

P1 提交、发布、状态提升前阻断：

- stage / commit / push / deploy 未获明确授权。
- Git dirty/sensitive path 未分类。
- current-window truth count mismatch。
- sequence_checkpoint 缺失或最近硬窗口不干净。

P2 治理审计项：

- 文档索引缺项、evidence 链接缺项、历史 replay 口径未标注。
- 治理债务定位、truth-field review、five-segment review。
- P2 默认不得阻断 GFIS 本地开发；只在影响 P0/P1 或状态提升时升级。

P3 观察项：

- 文案一致性、历史术语统一、非关键索引顺序。
- 仅登记，不阻断 Delivery Loop。

## Delivery Boundary

开发态默认 Delivery Loop。不得阻断 GFIS 本地开发，除非触发 P0/P1。GFIS 真实业务 lane 仍为 `repair_required`，真实 source-of-record、runtime intake、review queue、WAES review、verified artifact 均为 0。

## Real Source Record Zero Classification

`real_source_records = 0` 的门禁含义必须按状态线分类，不得再解释为开发阻断。

```yaml
real_source_records_zero:
  blocks:
    - real_business_verified
    - accepted
    - integrated
    - production_ready
    - customer_accepted
    - production_release
    - customer_delivery_claim

  does_not_block:
    - local_development
    - fixture_e2e
    - controlled_sample_e2e
    - dry_run
    - contract_validator
    - runtime_intake_development
    - review_queue_development
    - waes_review_candidate_development
    - verified_artifact_candidate_development
    - development_ready_for_real_business_validation
```

允许声明：

```text
development_ready_for_real_business_validation
ready_for_internal_review
fixture_e2e_passed
contract_validator_passed
dry_run_passed
verified_artifact_candidate_generated_by_fixture
```

禁止声明：

```text
real_business_verified
accepted
integrated
production_ready
customer_accepted
real_source_record_verified
customer_acceptance_passed
production_lane_ready
```

```text
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```
