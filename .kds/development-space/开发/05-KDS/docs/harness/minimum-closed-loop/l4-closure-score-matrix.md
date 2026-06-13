---
doc_id: GPCF-DOC-6913FD52DB
title: L4 Minimum Closed Loop Closure Score Matrix
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/minimum-closed-loop/l4-closure-score-matrix.md
source_path: docs/harness/minimum-closed-loop/l4-closure-score-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# L4 Minimum Closed Loop Closure Score Matrix

## Current Correction Status

2026-06-14 自我纠错结论：本矩阵原 `100/100` 和 `L4 closure achieved` 结论失效。原因是 GFIS 证据错误使用 `gcfis_demo` 作为工厂运行事实主体，而正确主体应为 GFIS 运行层；同时 GFIS SOP E2E last-run 为 `failed`。当前状态降级为 `L4 repair required`，项目群评分暂定 `78/100`。

本文件保留 L4 原始链路结构，但所有 GFIS/GPCF 收口判定以 `GPCF-L4-CORR-001` 和 `docs/harness/evidence/loop_self_correction_assessment.json` 为准。

## Closure Boundary

This matrix closes L4 only. It proves that all 12 GlobalCloud projects participate in the same minimum closed loop with controlled roles, evidence and validators. It does not mark any project accepted, integrated, deployed, production-written or customer-signed.

## Project Coverage

| Project | L4 round | Role in minimum loop | Evidence status | Validator status | Boundary |
|---|---|---|---|---|---|
| GPCF | GPCF-L4-001 / GPCF-L4-012 / GPCF-L4-CORR-001 | Project-group governance, score matrix, evidence intake and self-correction | repair_required | pass via correction gate | Does not replace business systems |
| MMC | MMC-L4-002 | Policy templates, resource gate fields and strategy boundary | ready_for_review | pass | Does not own factory facts |
| KDS | KDS-L4-003 | Knowledge source, SOP/case index and evidence backlinks | ready_for_review | pass | Does not replace current business facts |
| Brain | Brain-L4-004 | SOP/case retrieval UI and explanation surface | ready_for_review | pass | Consumes KDS, does not become KDS |
| PKC | PKC-L4-005 | Personal task, notification and todo-state intake | ready_for_review | pass | Workbench only, no business fact ownership |
| PVAOS | PVAOS-L4-006 | Tenant, organization, partner and permission baseline | ready_for_review | pass | Entry/portal layer only |
| GPC | GPC-L4-007 | Platform order, sample approval, production release and POD contract | ready_for_review | pass | Does not write GFIS factory facts |
| GFIS | GFIS-L4-008 | Factory-side formula, sample, order, work-order, quality, inventory and shipment facts | repair_required | insufficient: Demo evidence and SOP E2E failed | GFIS runtime layer must be the subject |
| XiaoC | XiaoC-L4-009 | Ant queen task decomposition, model routing and dispatch plan | ready_for_review | pass | Does not write business facts or bypass WAES |
| XGD | XGD-L4-010 | Elephant risk analysis, reliability assessment and recommendation packet | ready_for_review | pass | Analysis only, no final approval |
| XiaoG | XiaoG-L4-011 | Ant execution terminal read-only query, PKC notice candidate and WAES audit mock | ready_for_review | pass | No production write, no device OTA, no real API write |
| WAES | GPCF-L4-001..012 | Governance center, evidence gate and audit status owner | ready_for_review | pass via contracts/mock evidence | Does not become business master data |

## P0 Chain Reconstruction

| Chain node | Project evidence |
|---|---|
| Project initialization | PVAOS-L4-006, MMC-L4-002 |
| Organization and partner onboarding | PVAOS-L4-006 |
| Platform order | GPC-L4-007 |
| Quote review and contract | GPC-L4-007 |
| Formula R&D and sample work order | GFIS-L4-008 requires runtime-layer repair |
| Customer sample approval | GPC-L4-007, WAES evidence gate contract |
| Production release gate | GPC-L4-007, MMC-L4-002, WAES evidence gate contract |
| Factory order and work order | GFIS-L4-008 requires runtime-layer repair |
| Quality, inventory and batch | GFIS-L4-008 requires runtime-layer repair |
| Shipment and POD boundary | GFIS-L4-008 requires runtime-layer repair, GPC-L4-007 |
| Exception and risk | XGD-L4-010, KDS-L4-003 |
| WAES evidence and audit | XiaoG-L4-011, GPCF-L4-012 |
| Daily review and knowledge deposition | Brain-L4-004, PKC-L4-005, KDS-L4-003 |
| Project-group closure | GPCF-L4-012 |

## Project Group 100 Point Score

| Metric | Max | Score | Evidence |
|---|---:|---:|---|
| 12 project coverage | 15 | 15 | All 12 projects have role, input, output, validation and evidence entry |
| P0 business chain continuity | 20 | 12 | GFIS runtime-layer SOP/E2E is blocked; Demo cannot carry factory runtime facts |
| Real repository code/config/test closure | 20 | 12 | GFIS `test-results/.last-run.json` is failed; GFIS Demo fixture is invalid for runtime acceptance |
| KDS retrieval and knowledge backlink completeness | 10 | 10 | L4-002 through L4-011 include KDS retrieval or controlled evidence backlinks |
| Evidence and audit completeness | 15 | 15 | Project-level evidence and GPCF evidence index cross-reference each other; WAES audit remains controlled mock for L4 |
| Cross-project contract consistency | 10 | 10 | Object contracts preserve GFIS/GPC/MMC/WAES/KDS/AI boundaries |
| User reproducibility and L5 readiness | 10 | 0 | L5 preparation is blocked until GFIS runtime repair and SOP E2E pass |
| Total | 100 | 78/100 | GFIS runtime repair required; previous 100/100 is invalidated |

## Required Non-Claims

- GFIS Demo is not a SOP implementation subject.
- GFIS Demo is not a business acceptance subject.
- GFIS Demo is not a substitute for GFIS runtime-layer DocTypes, workflows, permissions, reports, attachments or runtime APIs.
- No project is marked accepted.
- No project is marked integrated.
- No production deployment occurred.
- No production write occurred.
- No real external API write occurred.
- No permission or token change occurred.
- No device OTA occurred.
- L5 remains a separate, stronger authorization stage.

## Repair Requirement

L4 may not close at 100/100. The next stage is `GFIS-runtime-repair`: replace Demo-backed GFIS evidence with GFIS runtime-layer evidence, repair and pass SOP E2E, then rerun `validate_loop_self_correction_gate.py` and `validate_l4_minimum_closed_loop.py`.
