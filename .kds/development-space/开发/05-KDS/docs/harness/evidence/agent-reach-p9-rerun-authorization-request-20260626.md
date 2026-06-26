---
doc_id: GPCF-DOC-AGENT-REACH-P9-RERUN-AUTHORIZATION-REQUEST-20260626
title: Agent-Reach P9R Live Rerun 授权请求 2026-06-26
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-rerun-authorization-request-20260626.md
source_path: docs/harness/evidence/agent-reach-p9-rerun-authorization-request-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Agent-Reach P9R Live Rerun 授权请求 2026-06-26

- status: `p9_rerun_authorization_request_ready`
- required_text: `授权执行 Agent-Reach P9R Priority Target Hit-Rate Live Rerun`
- max_queries: `20`
- max_results_per_query: `5`
- live_external_search_invoked: `False`
- runner_accepts_rerun_authorization_file: `True`
- authorization_file: `fixtures/agent-reach/p9-priority-target-hit-rate-rerun-authorization.local.json`
- rerun_output_json: `docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json`
- rerun_output_md: `docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.md`
- runner_command: `python3 tools/kds-sync/run_agent_reach_p9_priority_target_hit_rate.py --auth fixtures/agent-reach/p9-priority-target-hit-rate-rerun-authorization.local.json --execute-live --write-evidence --output-json docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json --output-md docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.md`

## Post-live validation

- `python3 tools/kds-sync/validate_agent_reach_p9_hit_rate_output_quality_gate.py --validate-report --report docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json --markdown docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.md`
- `python3 tools/kds-sync/validate_agent_reach_p9_review_queue_bridge_readiness.py`
- `python3 tools/kds-sync/loop_document_gate.py`

## 边界

- 本证据只准备 P9R rerun 授权请求。
- 本证据不执行真实搜索。
- 本证据不写 KDS canonical Markdown。
- 本证据不写 GFIS source-of-record。
- 本证据不声明 accepted / integrated / production_ready。
