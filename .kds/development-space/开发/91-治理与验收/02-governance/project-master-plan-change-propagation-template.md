---
doc_id: GPCF-DOC-PROJECT-MASTER-PLAN-CHANGE-PROPAGATION-TEMPLATE-20260624
title: 项目总体方案变更传导与用户确认模板
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/project-master-plan-change-propagation-template.md
source_path: 02-governance/project-master-plan-change-propagation-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 项目总体方案变更传导与用户确认模板

## 1. Change Proposal

| 字段 | 内容 |
|---|---|
| change_id | `GPCF-MASTER-PLAN-CHANGE-YYYYMMDD-NNN` |
| change_source | `master_plan` / `project_plan` / `change_proposal` |
| proposer | 待填写 |
| change_summary | 待填写 |
| reason | 待填写 |
| requested_status | `draft` / `candidate` / `controlled` |

## 2. Affected Project Matrix

| project | affected | affected_sections | required_action | owner | status |
|---|---|---|---|---|---|
| WAS世界资产体系 | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | WAS | pending |
| GlobalCloud XWAIL | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | XWAIL | pending |
| GlobalCloud AaaS / AAAS | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | AAAS | pending |
| GlobalCloud WAES | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | WAES | pending |
| GlobalCloud GFIS | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | GFIS | pending |
| GlobalCloud GPC | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | GPC | pending |
| GlobalCloud PVAOS | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | PVAOS | pending |
| GlobalCloud KDS | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | KDS | pending |
| GlobalCloud Brain | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | Brain | pending |
| GlobalCloud Studio | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | Studio | pending |
| GlobalCloud MMC | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | MMC | pending |
| GlobalCloud PKC | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | PKC | pending |
| GlobalCloud SOP | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | SOP | pending |
| GlobalCloud XGD | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | XGD | pending |
| GlobalCloud XiaoC | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | XiaoC | pending |
| GlobalCloud XiaoG | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | XiaoG | pending |
| GlobalCoud GPCF | yes/no | 定位/职责/接口/术语/版本/架构/测试/交付/LOOP | patch/no_action | GPCF | pending |

## 3. 用户确认

| 确认项 | 状态 |
|---|---|
| 是否涉及结构性变化 | yes/no |
| 是否需要用户确认 | yes/no |
| 用户是否已确认 | yes/no |
| 确认时间 | 待填写 |
| 确认内容摘要 | 待填写 |

未经用户确认的结构性变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 4. 传导证据

| 证据项 | 路径/命令 | 状态 |
|---|---|---|
| 主方案补丁 | 待填写 | pending |
| 项目方案补丁 | 待填写 | pending |
| 控制台账更新 | `09-status/globalcloud-project-master-plan-control-register.md` | pending |
| 专项验证脚本 | `python3 tools/kds-sync/validate_project_group_master_plan_governance.py` | pending |
| 文档门禁 | `python3 tools/kds-sync/loop_document_gate.py` | pending |

## 5. 非声明边界

本模板生成的 Change Proposal 不等于：

- 不等于主方案已完成变更；
- 不等于项目方案已完成传导；
- 不等于客户交付完成；
- 不等于 accepted、integrated 或 production_ready。
