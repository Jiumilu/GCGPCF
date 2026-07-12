---
doc_id: GPCF-DOC-ICP-STATUS-20260712
title: ICP 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/icp/STATUS.md
source_path: projects/icp/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

# ICP 状态

```yaml
project_status: candidate
overall_status: partial
confirmation_status: human_required
development_validation: passed
real_business_sources_connected: false
integrated: false
production_ready: false
```

当前只完成独立仓库、OpenSpec、24×11契约、三场景、API、测试和本地运行证据。下一门禁是人工确认与 WAES/GPCF 治理审查。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/icp-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project icp`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`
