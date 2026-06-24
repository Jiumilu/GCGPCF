---
doc_id: GPCF-DOC-PROJECT-IMPLEMENTATION-CHANGE-PROPAGATION-TEMPLATE-20260624
title: 项目实施方案变更传导模板
project: WAES
related_projects: [WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/project-implementation-plan-change-propagation-template.md
source_path: 02-governance/project-implementation-plan-change-propagation-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 项目实施方案变更传导模板

## 1. Implementation Change Proposal

| 字段 | 内容 |
|---|---|
| change_id |  |
| change_source | `implementation_master_plan` / `project_implementation_plan` / `runtime_evidence` / `customer_feedback` |
| proposed_by |  |
| proposed_at |  |
| user_confirmation_required | yes/no |
| user_confirmation_status | `pending` / `confirmed` / `rejected` |

## 2. Affected Project Implementation Matrix

| 项目 | 影响章节 | 影响类型 | 必须更新 | 状态 |
|---|---|---|---|---|

## 3. 传导路径

```text
Implementation Change Proposal
  -> Scope Review
  -> Affected Project Implementation Matrix
  -> Master Implementation Plan Decision
  -> Project Implementation Plan Patch List
  -> User Confirmation
  -> Document Control / KDS Mirror
  -> Gate Validation
  -> Evidence / Status Report
```

## 4. 用户确认

未经用户确认的结构性实施变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 5. 传导证据

| 证据 | 路径/命令 | 结果 |
|---|---|---|
| 实施方案校验 | `python3 tools/kds-sync/validate_project_group_implementation_plan.py` |  |
| 台账校验 | `python3 tools/kds-sync/validate_project_implementation_register.py` |  |
| 唯一性校验 | `python3 tools/kds-sync/validate_project_implementation_uniqueness.py` |  |
| 继承校验 | `python3 tools/kds-sync/validate_project_implementation_inheritance.py` |  |
| 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` |  |
