---
doc_id: GPCF-DOC-FE20CDD358
title: Loop Governance Dashboard（Loop 治理看板）
project: WAME
related_projects: [GFIS, GPC, WAME, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAME
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Governance Dashboard（Loop 治理看板）

## 目的

本看板记录 LOOP 治理信号，覆盖质量、效率、自我纠错、边界安全、可复现性与状态上限六个方面。

这是一块**治理看板**、不是**业务完成看板**。这些指标的通过或改善，**不意味着** GFIS、GPCF、WAME、KDS、UAT、生产、财务、客户验收或 integrated 状态已经完成。

## 当前快照

| 信号 | 当前值 | 含义 | 下一治理动作 |
|---|---|---|---|
| phase_goal | `LOOP-GOV-PHASE-20260617` | 治理阶段目标已激活，并由机器校验 | 保持阶段目标验证器在治理文档门禁中 |
| quality_gate | `repair_ceiling_enforced` | GFIS Demo、KDS 候选、请求包、模板、用户陈述和 Loop 记录，均不得替代运行时事实 | 保持角色边界与自我纠错验证器处于活跃状态 |
| efficiency_risk | `review_required` | 长序列与历史轮次记录债以 LEDB-001 至 LEDB-004 保持可见 | 审查积压项，不批量改写事实 |
| self_correction_gate | `blocked_expected` | GFIS 运行时 SOP 端到端仍为 `repair_required`；虚假完成持续被判无效 | 在实现主进程修复运行时证据之前，保持阻塞可见 |
| boundary_safety | `pass` | 治理过程与实现主进程相互分离 | 继续禁止生产写入、schema 同步、部署与 accepted/integrated 升级 |
| status_ceiling | `partial_repair` | 运行时主键、审查队列、运行时接入、WAME 审查与核验产物仍为 0 | 运行时 SOP 为 repair_required 期间不得升级状态 |
| reproducibility | `local_validators_present` | 治理结论可在本地重新运行复现 | 保持证据中的命令清单为最新 |

## 指标分组

### 质量

| 指标 | 值 | 门禁 |
|---|---|---|
| false_completion_claim_allowed | false | pass |
| demo_as_runtime_allowed | false | pass |
| request_package_as_source_record_allowed | false | pass |
| accepted_integrated_without_human_allowed | false | pass |

### 效率

| 指标 | 值 | 门禁 |
|---|---|---|
| loop_efficiency_risk | `review_required` | visible_debt |
| hard_window_truth_fields_missing | 0 | pass |
| hard_window_five_segment_missing | 0 | pass |
| audit_window_truth_fields_missing | 14 | review_required |
| audit_window_five_segment_missing | 19 | review_required |
| max_consecutive_sequence | 183 | review_required |

### 自我纠错

| 指标 | 值 | 门禁 |
|---|---|---|
| self_correction_gate | `blocked` | expected_repair_ceiling |
| gfis_runtime_subject | `pass` | pass |
| historical_demo_evidence | `invalidated` | pass |
| runtime_sop_e2e | `repair_required` | blocked_expected |
| project_group_score | 79 | repair |

### 边界安全

| 指标 | 值 | 门禁 |
|---|---|---|
| governance_process_bounded | true | pass |
| implementation_process_separate | true | pass |
| production_write_allowed | false | pass |
| schema_sync_allowed | false | pass |
| git_push_allowed | false | pass |
| accepted_integrated_allowed | false | pass |

### 状态上限

| 指标 | 值 | 门禁 |
|---|---|---|
| runtime_primary_key_ready | 0 | blocked_expected |
| review_queue | 0 | blocked_expected |
| runtime_intake | 0 | blocked_expected |
| wame_review | 0 | blocked_expected |
| verified | 0 | blocked_expected |

## 命令

| 命令 | 用途 |
|---|---|
| `python3 tools/kds-sync/validate_loop_governance_dashboard.py` | 校验本看板及看板证据 |
| `python3 tools/kds-sync/validate_loop_governance_phase_goal.py` | 校验阶段目标与状态上限 |
| `python3 tools/kds-sync/validate_loop_round_efficiency_audit.py` | 校验效率审计硬窗口并暴露历史债 |
| `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | 校验自我纠错上限与 GFIS 运行时修复状态 |
| `python3 tools/kds-sync/validate_loop_governance_role_boundary.py` | 校验治理/实现边界 |

## 非声明（Non-Claims）

- This dashboard does not prove source-of-record receipt.
- 本看板不创建运行时主键、审查队列、运行时接入、WAME 审查或核验产物。
- 本看板不证明 UAT、生产、客户满意度、财务、accepted 或 integrated 完成。
- 本看板不授权生产写入、外部 API 写入、schema 同步、bench migrate、部署、权限变更、commit 或 push。

## 看板后续工作

1. 审查 LEDB-001 至 LEDB-004，并为每个债务项记录处置结论。
2. 当同一看板门禁在多个治理轮次中运行后，补充趋势快照。
3. 实现侧后续步骤持续聚焦真实 GFIS 来源记录提交；治理侧持续跟踪证据质量与边界。
