---
doc_id: GPCF-DOC-26BEA382B1
title: ODF Phase 9 动态源稳定化策略方案
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase9-dynamic-source-stabilization-plan.md
source_path: 09-status/odf-phase9-dynamic-source-stabilization-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ODF Phase 9 动态源稳定化策略方案

日期：2026-06-19

## 目标

将动态源文档纳入 reference-only 策略。动态源 source hash 漂移继续被监控和计数，但不阻断 ODF strict gate；静态源 hash、ODF envelope hash、缺文件、重复样本仍严格失败。

## 动态源

| source_path | policy | reason |
| --- | --- | --- |
| `docs/harness/evidence/evidence-index.md` | reference-only | evidence index 会随证据追加持续变化 |
| `09-status/gpcf-project-status-matrix.md` | reference-only | status matrix 是项目群当前状态快照 |
| `docs/harness/evidence/loop-governance-dashboard-20260617.md` | reference-only | dashboard 未来可能被 Loop 刷新 |
| `09-status/kds-development-space-sync-register.md` | reference-only | KDS 同步台账会随文档纳入变化 |

## 门禁规则

| gate item | behavior |
| --- | --- |
| dynamic source hash drift | count as `dynamic_reference_drift` |
| static source hash drift | fail |
| ODF envelope hash drift | fail |
| missing source or envelope | fail |
| duplicate sample or ODF path | fail |

## 非范围

- 不新增 ODF 样本。
- 不复制源 Markdown 正文。
- 不改动态源 Markdown 正文来追 hash。
- 不全量导入 ODF。
- 不写生产系统或真实外部 API。
- 不做业务状态升级。
