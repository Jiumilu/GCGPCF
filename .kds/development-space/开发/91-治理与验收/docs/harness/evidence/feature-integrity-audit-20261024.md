---
doc_id: GPCF-DOC-FEATURE-INTEGRITY-20261024
title: Feature 目录/队列完整性审计（2026-10-24）
project: GPCF
related_projects: [GPCF, WAME]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/feature-integrity-audit-20261024.md
source_path: docs/harness/evidence/feature-integrity-audit-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# Feature 目录/队列完整性审计

## 结果

- active 目录：15（与 state active_feature_count 一致）
- done 目录：23
- feature.yaml YAML 解析：全部通过
- id 与目录名：全部一致
- journal.md：全部存在
- queue 中不存在的目录：0
- 目录但 queue 无记录：**F-001**（历史 bootstrap，未入 queue，登记为历史例外）

## 说明

- 本审计只做结构一致性，不判断业务完成度。
- F-001 不强行补录，避免伪造历史队列。
