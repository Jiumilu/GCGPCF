---
doc_id: GPCF-DOC-0EFDA19AF2
title: OKF v0.1 消费基准证据
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md
source_path: docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# OKF v0.1 消费基准证据

generated_at: 2026-06-21T00:41:44.601523+00:00

## 范围

本 benchmark 验证 KDS、Governance 与 Architecture 三个 OKF v0.1 bundle 的确定性 metadata lookup。它只验证可导航性与来源恢复能力。

## 摘要

| metric | value |
| --- | --- |
| status | pass |
| concepts | 81 |
| passed_queries | 6 |
| total_queries | 6 |
| json | `docs/harness/evidence/okf-v01-consumption-benchmark-20260620.json` |

## 结果

| query | bundle | expected_source_path | top_source_path | top_okf_path | score | status |
| --- | --- | --- | --- | --- | ---: | --- |
| KDS 开发空间安全规范 | kds | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | `.okf/bundles/kds-v0.1/concepts/02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | 2 | pass |
| KDS Markdown 化 OKF 兼容层闭环方案 | kds | `09-status/kds-md-okf-implementation-closure-plan.md` | `09-status/kds-md-okf-implementation-closure-plan.md` | `.okf/bundles/kds-v0.1/concepts/09-status/kds-md-okf-implementation-closure-plan.md` | 4 | pass |
| Loop 控制板 | governance | `02-governance/loop/LOOP_CONTROL_BOARD.md` | `02-governance/loop/LOOP_CONTROL_BOARD.md` | `.okf/bundles/governance-v0.1/concepts/02-governance/loop/LOOP_CONTROL_BOARD.md` | 2 | pass |
| ODF Phase 7 小批量样本执行方案 | governance | `09-status/odf-phase7-small-batch-execution-plan.md` | `09-status/odf-phase7-small-batch-execution-plan.md` | `.okf/bundles/governance-v0.1/concepts/09-status/odf-phase7-small-batch-execution-plan.md` | 4 | pass |
| 体系总架构 | architecture | `01-architecture/GlobalCloud绿色供应链体系总架构.md` | `01-architecture/GlobalCloud绿色供应链体系总架构.md` | `.okf/bundles/architecture-v0.1/concepts/01-architecture/GlobalCloud绿色供应链体系总架构.md` | 1 | pass |
| 三阶段激活深度 | architecture | `01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md` | `01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md` | `.okf/bundles/architecture-v0.1/concepts/01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md` | 1 | pass |

## 边界

- 这是确定性 metadata benchmark，不是语义搜索或性能 benchmark。
- OKF 仍是派生消费层。
- KDS/Git 受控文档仍是 source of record。
- 本 evidence 不升级业务、验收或集成状态。
