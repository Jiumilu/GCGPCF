---
doc_id: GPCF-DOC-4ED15E157A
title: GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001 Multi-Agent Execution Pack
project: GPCF
related_projects: [GPCF, GFIS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.multi-agent.md
source_path: docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.multi-agent.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001 多智能体执行包

## 1. 主线

```text
GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001
```

## 2. 最高原则

真实业务输入是验收门，不是开发门。

`real_source_records = 0` 不阻断本地开发、fixture E2E、dry-run、contract validator 或 `development_ready_for_real_business_validation`。

## 3. 执行模式

```yaml
mode: controlled_multi_agent
default_loop: Delivery Loop
governance_level: G1
governance_loop_trigger:
  - P0 risk
  - P1 release/state gate
  - guarded
  - blocked
  - status promotion
  - production action
  - real external API write
  - schema migration
  - commit_push_deploy
  - stage_summary
```

## 4. 智能体分工

### 智能体 0：LOOP 编排

范围：

- 任务规划
- 范围仲裁
- 文件锁控制
- 结果聚合
- 最终 evidence 合并
- 治理摘要草稿

禁止：

- accepted
- integrated
- production_ready
- customer_accepted
- commit
- push
- deploy
- 生产写入
- 真实外部 API 写入

### 智能体 1：契约

范围：

- CustomerRequirementOrPlatformOrder contract
- 必填字段
- 可选字段
- 禁止字段
- 受控且契约有效的样例
- 契约 validator

输出：

- contract_defined
- controlled_sample_exists
- contract_validator_passed

### 智能体 2：运行接入

范围：

- runtime intake 开发
- 接入 dry-run
- 接入错误处理

输出：

- runtime_intake_development
- runtime_intake_dry_run_passed

### 智能体 3：主键与来源校验

范围：

- primary key candidate
- source validation
- 重复检查
- 缺字段检查
- 无效输入检查

输出：

- primary_key_candidate_generated
- source_validation_passed

### 智能体 4：Review Queue

范围：

- review queue item schema
- queue item payload
- queue item dry-run

输出：

- review_queue_item_generated

### 智能体 5：WAES 候选与产物候选

范围：

- WAES review candidate
- verified artifact candidate by fixture
- 本地 E2E dry-run

输出：

- waes_review_candidate_generated
- verified_artifact_candidate_by_fixture_generated
- local_e2e_dry_run_passed

### 智能体 6：边界校验

范围：

- real_source_records_zero_not_dev_blocker 检查
- fixture_not_real_business_verified 检查
- 禁止状态检查
- 禁止动作检查
- Delivery Loop 边界检查

输出：

- delivery_boundary_validator_passed

## 5. 执行顺序

### 阶段 A：并行只读设计

- 所有智能体只检查各自范围并产出设计说明。
- 不做大范围写入。
- 不改变状态。

### 阶段 B：受控实现

1. 契约智能体
2. 运行接入智能体
3. 主键与来源校验智能体
4. Review Queue 智能体
5. WAES 候选与产物候选智能体
6. 边界校验智能体
7. LOOP 编排摘要

## 6. Delivery Loop 模板

```yaml
delivery_loop:
  project: GFIS
  mainline: GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001
  agent:
  slice:
  goal:

  changed:
    -

  verified:
    command:
    result:

  risk:
    gate:
    reason:
    p0_triggered: false
    p1_triggered: false

  next:
    -
```

## 7. 文件锁策略

```yaml
file_lock_policy:
  single_writer_per_file: true

  orchestrator_only:
    - LOOP_CONTROL_BOARD.md
    - gpcf-project-status-matrix.md
    - GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001-evidence.md
    - LOOP_GOVERNANCE_SUMMARY_GFIS_RUNTIME_SOP_E2E_DEV_COMPLETION_001.md

  forbidden_parallel_writes:
    - same_file
    - same_status_field
    - same_evidence_file
    - same_validator_baseline
```

## 8. Evidence 策略

每个智能体只产出一份交付说明，只有 LOOP 编排负责合并最终 evidence。每个开发切片最多保留一份主 evidence。测试日志只做摘要，不整段复制进 KDS。

主 evidence：

```text
GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001-evidence.md
```

必须包含：

- contract 结果
- 受控样例结果
- runtime intake 结果
- primary key 结果
- source validation 结果
- review queue 结果
- WAES candidate 结果
- verified artifact candidate by fixture 结果
- boundary validator 结果
- 显式非声明

显式非声明：

- 不声明 real_business_verified
- 不声明 accepted
- 不声明 integrated
- 不声明 production_ready
- 不声明 customer_accepted
- 不声明真实 source-of-record 已验证

## 9. 停止条件

任一智能体如果需要以下事项，必须停止并回到人工确认：

- 真实 source-of-record
- 生产写入
- 真实外部 API 写入
- 真实 KDS API 写入
- schema migrate
- bench migrate
- commit
- push
- deploy
- secret / token / .env / production config 访问
- accepted / integrated / production_ready 声明
- 跨智能体文件修改

## 10. 成功标准

```yaml
success_criteria:
  contract_defined: true
  controlled_sample_exists: true
  contract_validator_passed: true
  runtime_intake_dry_run_passed: true
  primary_key_candidate_generated: true
  source_validation_passed: true
  review_queue_item_generated: true
  waes_review_candidate_generated: true
  verified_artifact_candidate_by_fixture_generated: true
  local_e2e_dry_run_passed: true
  delivery_boundary_validator_passed: true
  p0_violation: false
  real_business_verified_declared: false
  accepted_declared: false
  integrated_declared: false
  production_ready_declared: false
  customer_accepted_declared: false
```

## 11. 允许的最终状态

允许申请：

- development_ready_for_real_business_validation

不得声明：

- real_business_verified
- accepted
- integrated
- production_ready
- customer_accepted
