---
doc_id: GPCF-DOC-5F4B0C8D71
title: Loop UI 治理基线证据
project: GPCF
related_projects: [WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/loop-ui-governance-baseline-20260622.md
source_path: docs/harness/evidence/loop-ui-governance-baseline-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop UI 治理基线证据

## 证据摘要

Evidence ID: `LOOP-UI-GOV-BASELINE-20260622`

本证据用于证明两件事已经进入 Loop 基线：

1. 涉及 UI 的 Loop round 现在有了显式 `UI scope`、`UI gate status` 和 G1-G9 结构化字段。
2. 项目群已有统一的 UI 设计、开发、治理与评估主规范，并被 UI Quality Gate 和 Loop 门禁引用。

## 交付物

| Type | Path | Purpose |
|---|---|---|
| UI master doc | `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md` | 统一 UI 主规范 |
| Loop round template | `templates/LOOP_ROUND_TEMPLATE.md` | 为 UI round 增加必填 gate 结构 |
| Validator | `tools/kds-sync/validate_loop_ui_quality_baseline.py` | 机检 UI gate baseline 与显式 UI round |
| Markdown evidence | `docs/harness/evidence/loop-ui-governance-baseline-20260622.md` | 人类可读治理证据 |
| JSON evidence | `docs/harness/evidence/loop-ui-governance-baseline-20260622.json` | 机器可读治理证据 |

## 当前治理事实

| Field | Value |
|---|---|
| phase | `LOOP-UI-GOV-BASELINE-20260622` |
| template_ui_scope_required | true |
| template_ui_gate_required_when_ui_scope_true | true |
| ui_gate_status_values | `ui_ready, ui_partial, ui_blocked, ui_rework_required` |
| ui_gate_max_status | `ui_evidence_candidate` |
| broader_project_status_upgrade_requires_harness | true |
| historical_ui_signal_rounds_without_explicit_scope | visibility_only |

## 治理执行检查

| Command | Expected Meaning |
|---|---|
| `python3 tools/kds-sync/validate_loop_ui_quality_baseline.py` | UI gate baseline、template 与显式 UI round 结构一致 |
| `python3 tools/kds-sync/validate_loop_governance_docs.py` | Loop 治理文档已要求 UI baseline validator |
| `python3 tools/kds-sync/loop_document_gate.py --check-only` | UI baseline validator 已进入 Loop 文档门禁链 |

## 非声明事项

- 本证据不代表任何具体产品界面已经设计完成。
- 本证据不代表任何具体项目已经通过真实 UI 交互验收。
- 本证据不代表 accepted、integrated、production_ready 或业务完成。
- 本证据不替代截图、浏览器验证、Playwright 证据、Figma 对照或客户满意度采集。
