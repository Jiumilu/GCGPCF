---
doc_id: GPCF-DOC-AGENT-REACH-P9-HIT-RATE-OUTPUT-QUALITY-GATE-20260626
title: Agent-Reach P9 命中率输出质量门禁 2026-06-26
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.md
source_path: docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Agent-Reach P9 命中率输出质量门禁 2026-06-26

- status: `p9_hit_rate_output_quality_gate_ready`
- planned_query_count: `20`
- topics: `green_supply_chain, industrial_solid_waste, phosphogypsum, zero_waste_city`
- self_test_passed_without_network: `True`
- live_external_search_invoked: `False`

## 校验范围

- 要求 P9 live 输出状态为 `p9_priority_target_hit_rate_completed`。
- 要求 4 个主题全部达到 query coverage 与 P0/P1 重点域名命中阈值。
- 校验 domain boost、source scoring、GFIS/WAS/WAES/KDS 业务字段映射和 candidate-only non-claim。
- 阻断 raw provider payload、credential/cookie 泄漏、accepted / integrated / production_ready 声明。
- 本门禁不执行真实搜索，只校验已有输出或离线自测 fixture。

## Validator Checks

- blocks_credential_leak: `True`
- blocks_forbidden_claims: `True`
- blocks_raw_provider_payload_persistence: `True`
- negative_bad_boost_test_passed: `True`
- negative_credential_leak_test_passed: `True`
- negative_forbidden_claim_test_passed: `True`
- negative_missing_marker_test_passed: `True`
- negative_missing_topic_query_test_passed: `True`
- negative_query_error_test_passed: `True`
- negative_raw_payload_test_passed: `True`
- negative_status_test_passed: `True`
- requires_boosted_score_cap: `True`
- requires_business_field_mapping: `True`
- requires_candidate_only_non_claims: `True`
- requires_completed_status: `True`
- requires_domain_boost_consistency: `True`
- requires_execution_requested: `True`
- requires_four_topic_reports: `True`
- requires_live_external_search_invoked: `True`
- requires_markdown_candidate_only_marker: `True`
- requires_markdown_non_claim_marker: `True`
- requires_p9_candidate_schema: `True`
- requires_planned_query_count_20: `True`
- requires_priority_domain_threshold_pass: `True`
- requires_query_candidate_coverage_one_per_topic: `True`
- requires_topic_coverage_one: `True`
- requires_zero_query_errors: `True`
- self_test_passed_without_network: `True`

## 边界

- This evidence is candidate-only.
- This evidence does not create source-of-record.
- This evidence does not write KDS canonical Markdown.
- This evidence does not write GFIS source-of-record.
- This evidence does not claim accepted, integrated, or production_ready status.
