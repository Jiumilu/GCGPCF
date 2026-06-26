---
doc_id: GPCF-DOC-AGENT-REACH-P9-PRIORITY-TARGET-HIT-RATE-PRECHECK-20260626
title: Agent-Reach P9 重点对象命中率预检证据 2026-06-26
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.md
source_path: docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Agent-Reach P9 重点对象命中率预检证据 2026-06-26

- status: `p9_priority_target_hit_rate_precheck_ready`
- current_admission: `limited_candidate_only`
- mode: `precheck_only_no_live_search`
- topic_count: `4`
- query_count: `20`
- expected_priority_domain_count: `9`
- expected_p0_domain_count: `7`
- drift_monitoring_markers_present: `True`
- live_authorization_required_before_hit_rate_run: `True`

## 边界

- 本证据只完成 P9 precheck，不执行真实搜索。
- P9 hit-rate live run 需要单独授权。
- 本证据不写 KDS canonical Markdown。
- 本证据不写 GFIS source-of-record。
- 本证据不声明 accepted / integrated / production_ready。
