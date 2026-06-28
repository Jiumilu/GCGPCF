---
doc_id: GPCF-DOC-LOOP-DELIVERY-ROUND-TEMPLATE
title: LOOP Delivery Round Template
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/LOOP_DELIVERY_ROUND_TEMPLATE.md
source_path: templates/LOOP_DELIVERY_ROUND_TEMPLATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# LOOP Delivery Round Template

```yaml
delivery_loop:
  project:
  slice:
  goal:

  changed:
    -

  verified:
    command:
    result:

  risk:
    gate:
    reason:

  next:
    -
```

## 使用规则

- 每个开发切片最多 1 个主 round。
- 每个开发切片最多 1 个主 evidence。
- 测试日志不进入 KDS，只记录摘要。
- 普通本地修改不单独写 evidence。
- 触发 P0、guarded、blocked、状态提升、生产动作或阶段收口时，切换到 Governance Loop。
