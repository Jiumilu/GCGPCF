---
doc_id: GPCF-DOC-07906C7E54
title: Loop 治理效率债务 Backlog
project: WAES
related_projects: [GFIS, GPC, WAES, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop 治理效率债务 Backlog

本文是 LOOP 治理效率债务的受控 backlog（`Loop Governance Efficiency Debt Backlog`）。它把仪表盘级 `review_required` 信号转成可审计复核项，并保持 `does not rewrite historical round records in bulk`。

## 来源信号

```text
loop_round_efficiency_audit=pass total_rounds=335 audit_checked=30 hard_checked=5 audit_missing_truth_fields=0 audit_missing_five_segment=0 audit_batch_generated_counted=0 hard_missing_truth_fields=0 hard_missing_five_segment=0 hard_batch_generated_counted=0 duplicate_fingerprint_groups=0 high_similarity_adjacent_pairs=0 max_consecutive_sequence=186 risk=review_required
```

## Backlog 项

| ID | Priority | Debt Type | Scope | Count | Status | Handling Rule |
|---|---|---|---|---:|---|---|
| LEDB-001 | P1 | missing_truth_fields | audit_window_round_records | 1 | open | 增加复核注释或受控 index-level exceptions；不得静默视为 clean history。 |
| LEDB-002 | P1 | missing_five_segment_markers | audit_window_round_records | 1 | open | 增加复核注释或受控 index-level exceptions；不得批量改写历史事实。 |
| LEDB-003 | P1 | long_consecutive_sequence_risk | GPCF-L4-GFIS-REPAIR-* | 186 | open | 要求周期性 checkpoint review，并在复核前保持长序列风险可见。 |
| LEDB-004 | P2 | dashboard_validator_drift_risk | governance_docs_and_evidence_ids | 1 | monitoring | Validators 必须绑定 title 和 source path，不只依赖生成的 doc_id。 |

## 复核处置模板 (`Review Disposition Template`)

每个 backlog 项必须通过小型复核记录关闭或重新分类：

| Field | Required Meaning |
|---|---|
| disposition_id | 稳定 ID，例如 `LEDB-001-RD-001` |
| backlog_item | `LEDB-001` 至 `LEDB-004` 之一 |
| reviewer | 负责人类或治理 agent 角色 |
| decision | `historical_debt`、`targeted_annotation_required`、`validator_rule_update`、`accepted_exception` 或 `superseded` |
| evidence_ref | 支撑决策的文件路径、命令输出或 round ID |
| no_bulk_rewrite | 除非另有迁移计划明确授权，否则必须保持 `true` |
| business_status_impact | 必须保持 `none`；review does not upgrade GFIS or project completion status |
| next_action | 下一项受控动作；若已关闭则为 `none` |

## 初始处置队列

| disposition_id | backlog_item | reviewer | decision | evidence_ref | no_bulk_rewrite | business_status_impact | next_action |
|---|---|---|---|---|---|---|---|
| LEDB-001-RD-001 | LEDB-001 | GPCF governance | targeted_annotation_required | `tools/kds-sync/validate_loop_round_efficiency_audit.py` | true | none | Identify affected audit-window round records before any annotation. |
| LEDB-002-RD-001 | LEDB-002 | GPCF governance | targeted_annotation_required | `tools/kds-sync/validate_loop_round_efficiency_audit.py` | true | none | Identify affected audit-window round records before any annotation. |
| LEDB-003-RD-001 | LEDB-003 | GPCF governance | historical_debt | `docs/harness/loops/` sequence scan | true | none | Keep visible until periodic checkpoint cadence is defined. |
| LEDB-004-RD-001 | LEDB-004 | GPCF governance | validator_rule_update | `tools/kds-sync/validate_loop_governance_efficiency_backlog.py` | true | none | Keep validators path/title-bound and evidence-bound. |
| LEDB-001-RD-002 | LEDB-001 | GPCF governance | validator_rule_update | `tools/kds-sync/validate_loop_round_efficiency_audit.py` and `tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py` | true | none | Truth-field parser now recognizes table rows, bullet colon rows, and backtick key=value rows; debt reduced to 1 without rewriting historical rounds. |
| LEDB-002-RD-002 | LEDB-002 | GPCF governance | targeted_annotation_required | `docs/harness/evidence/loop-governance-five-segment-review-20260617.json` | true | none | `212`, `209`, and `208` are targeted annotation candidates; `211` and `210` remain index-level exceptions unless a separate migration plan is authorized. |
| LEDB-001-RD-003 | LEDB-001 | GPCF governance | accepted_exception | `docs/harness/evidence/loop-governance-truth-field-review-20260617.json` | true | none | Five current truth-field debt records remain front matter shell exceptions; `218` now has a historical annotation body and truth-count fields. |
| LEDB-003-RD-002 | LEDB-003 | GPCF governance | historical_debt | `docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.json` | true | none | Checkpoint cadence defined: review every 25 `GPCF-L4-GFIS-REPAIR-*` rounds, next required checkpoint at sequence length 200 or when hard-window debt reappears. |
| LEDB-001-RD-004 | LEDB-001 | GPCF governance | current_window_review_required | `docs/harness/evidence/loop-governance-current-window-review-20260619.json` | true | none | Current live audit window has 25 truth-field review targets; review without rewriting historical rounds. |
| LEDB-002-RD-003 | LEDB-002 | GPCF governance | current_window_clean | `docs/harness/evidence/loop-governance-current-window-review-20260619.json` | true | none | Current live audit window has 0 five-segment review targets; keep guard active for hard-window recurrence. |
| LEDB-001-RD-005 | LEDB-001 | GPCF governance | current_window_disposition_recorded | `docs/harness/evidence/loop-governance-current-window-disposition-20260619.json` | true | none | Keep `252` and `254` visible as shell exceptions; no historical rewrite is authorized. |
| LEDB-002-RD-004 | LEDB-002 | GPCF governance | current_window_disposition_recorded | `docs/harness/evidence/loop-governance-current-window-disposition-20260619.json` | true | none | `252` and `254` remain shell exceptions; `269` through `273` are targeted annotation candidates. |

## 定位证据

`LOOP-GOV-EFF-DEBT-LOCATOR-20260617` 识别受 `LEDB-001` 和 `LEDB-002` 影响的具体 audit-window round records。它是 review locator，不是 rewrite plan。

| Backlog Item | Located Count | Evidence |
|---|---:|---|
| LEDB-001 | 0 | `docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.json` |
| LEDB-002 | 0 | `docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.json` |

## 当前窗口复核证据

`LOOP-GOV-CURRENT-WINDOW-REVIEW-20260619` 记录当前 live audit-window 复核目标，不改变历史 locator baseline。它记录 `LEDB-001-RD-004` 的 truth-field 目标和 `LEDB-002-RD-003` 的 five-segment 目标，保持 duplicate/similarity 信号可见，并保持 `business_status_impact=none`。

`LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619` 记录 `LEDB-001-RD-005` 和 `LEDB-002-RD-004`。它把 `252` 与 `254` 分类为 index-level shell exceptions，并把 `269` 至 `273` 分类为 targeted annotation candidates；不授权批量改写历史 round records。

## 轮次复核计划

`LOOP-GOV-ROUND-REVIEW-PLAN-20260617` 把 locator 转为受控 review queue。它从最新受影响记录开始，只允许 `targeted annotation` 或 `index-level exception`，并保持 `no_bulk_rewrite=true` 和 `business_status_impact=none`。

| Review Package | Backlog Item | Count | Rule |
|---|---|---:|---|
| LEDB-001-RP-001 | LEDB-001 | 0 | 之前受影响 round 的 targeted annotation 已完成；继续监控，不做 bulk rewrite。 |
| LEDB-002-RP-001 | LEDB-002 | 1 | 注释前先用现有证据复核缺失的 five-part markers。 |
| LEDB-003-RP-001 | LEDB-003 | 186 | 为长连续 GFIS repair sequence 定义 checkpoint cadence。 |

## 五段式复核证据

`LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617` 为 `GPCF-L4-GFIS-REPAIR-212` 至 `GPCF-L4-GFIS-REPAIR-208` 记录 `LEDB-002-RD-002`。它识别 3 个 targeted annotation candidates 和 2 个 index-level exceptions，不改写历史 round records。

## 真实性字段复核证据

`LOOP-GOV-TRUTH-FIELD-REVIEW-20260617` 为 6 条已复核 truth-field debt records 记录 `LEDB-001-RD-003`。其中 5 条保持为 front matter shell exceptions；`218` 已具备 historical annotation body 和 truth-count fields。

## 序列 checkpoint 证据

`LOOP-GOV-SEQUENCE-CHECKPOINT-20260619` 记录 `LEDB-003-RD-002`。它为长 `GPCF-L4-GFIS-REPAIR-*` 序列定义 25-round checkpoint cadence；下一次 required checkpoint 是 sequence length 200，或 hard-window debt 再次出现。

## 关闭条件 (`Closing Conditions`)

- 每个项目都有受控 review note 或 evidence entry。
- 复核明确旧记录保持 historical debt，或接收 targeted annotation。
- 最新 hard window 保持 clean：
  `hard_missing_truth_fields=0` and `hard_missing_five_segment=0`.
- 清理不创建、不暗示 GFIS source-of-record、runtime primary key、review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated 状态。

## 非声明边界

- 机器断言：`does not rewrite historical round records in bulk`。
- 机器断言：`does not prove GFIS runtime SOP E2E passed`。
- 机器断言：`does not create source-of-record`、runtime primary key、review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated status。
- 本 backlog 不授权 production write、external API write、schema sync、bench migrate、deployment、permission change、commit 或 push。
