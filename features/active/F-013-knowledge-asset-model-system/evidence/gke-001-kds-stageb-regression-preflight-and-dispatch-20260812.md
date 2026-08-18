---
doc_id: GPCF-DOC-F013-GKE001-KDS-STAGEB-REGRESSION-PREFLIGHT-20260812
title: GKE-001 KDS Stage B Regression Preflight And Dispatch
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-regression-preflight-and-dispatch-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-regression-preflight-and-dispatch-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 KDS Stage B Regression Preflight And Dispatch

## Goal

Prove that the frozen `stageb_regression_2` patch remains independently applicable and testable on the accepted local core commit before any new commit authorization is requested.

## Baseline

- KDS HEAD: `7fb477030f5278faf55d6d16ff3874469704610d`.
- origin/main: `f28edb5113e0493ed60fec423cb6c7e1a6252de8`.
- ahead/behind/staged: `1/0/0`.
- ordinary/expanded dirty: `181/453`.
- OpsX lock: absent.

## Candidate

- Paths: `tests/test_knowledge_intake_api.py`, `tests/test_knowledge_intake_postgres.py`.
- Sorted NUL pathset SHA-256: `ffeab20c1c54610428c2da48d4dc6b83275affdaa5a69a1b969b005af008b66f`.
- Patch: `38511` bytes, SHA-256 `1e7ecd30fbb740fcf2217224de107adb0c960d5babfc71aaaee036b9fae90f7e`.

## Authorization

Only report-only disposable preflight is authorized. The KDS repository allowlist is empty. No stage, commit, push, product/OpenSpec/handoff write, live/shared access, deployment or status promotion is authorized.

## Delivery Loop

```yaml
goal: prove stageb_regression_2 remains independently admissible after the accepted core commit
changed: GPCF coordination and evidence only
verified: deterministic patch replay passed, 66 non-DB and 23 PostgreSQL/migration tests passed
risk: commit and later units remain human-authorized boundaries
next: F-013 independent review, then present an exact two-path commit decision
product_delta: none_report_only_preflight
user_visible_delta: none
loop_cost_level: medium
substantive_round: true
task_flow_e2e_status: controlled_fixture_only
evidence_overexposure_gate: bounded
delivery_efficiency_gate: pass
```

## Preflight Receipt

- Receipt: `GKE-001-COORDINATION-20260812-020-A10I1D4R3R1`.
- Receipt SHA-256: `d8a746f5cf323211f94846193d92fe32ea7ac4293faede1b3f0b1caec031278d`.
- Patch generated twice: byte-identical, `38511` bytes, SHA-256 `1e7ecd30fbb740fcf2217224de107adb0c960d5babfc71aaaee036b9fae90f7e`.
- Selective clean replay: `66/66` non-DB and `23/23` PostgreSQL/migration passed.
- Disposable database and root cleanup counts: `0`.
- KDS before/after: HEAD `7fb47703`, ahead/behind/staged `1/0/0`, dirty `181/453`, lock absent.

## Status

F-013 classification: `regression_preflight_independent_review_passed_human_two_path_commit_authorization_required`.

Authorization request: `GKE-001-COORDINATION-20260812-021-A10I1D4R4`, SHA-256 `7107019c08ba37a61b0531f0dd6102d0b26dd16248365b9499c9b0e69174366e`.

Human authorization receipt: `GKE-001-COORDINATION-20260812-022-A10I1D4R4A1`, SHA-256 `859e6eac3a4a792f6977d3dba87a3810439354410517704af9f88450ce2935a7`.

Local commit receipt: `GKE-001-COORDINATION-20260812-023-A10I1D4R4A2`, SHA-256 `7973115f76b2cf671b2a68fceec3a7559096a3e26d531101082a64db8472a8e7`.

Commit: `60957dd92380bfeb6049ec552658dad22d5d90dc`; two authorized paths only; push not performed.

F-013 postcommit classification: `local_regression_commit_independent_review_passed`.

`active / partial / not_complete`; local commit accepted for this bounded unit only; push and all later units remain unauthorized.
