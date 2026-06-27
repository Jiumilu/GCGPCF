---
doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-OUTPUT-QUALITY-GATE-20260626
title: Agent-Reach P9S Source Direct 输出质量门禁 2026-06-26
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.md
source_path: docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Agent-Reach P9S Source Direct 输出质量门禁 2026-06-26

- status: `p9_source_direct_output_quality_gate_ready`
- planned_target_count: `13`
- topics: `green_supply_chain, industrial_solid_waste, phosphogypsum, zero_waste_city`
- live_external_fetch_invoked: `False`

## 校验范围

- 要求 P9S live 输出状态为 `p9_source_direct_hit_rate_completed`。
- 要求绿色供应链、磷石膏、工业固废、无废城市 4 个主题全部达到 P0 命中和关键词命中。
- critical fetch error 作为 target availability warning 保留，不抹除目标可用性风险。
- 校验 source scoring、GFIS/WAS/WAES/KDS 业务字段映射和 candidate-only non-claim。
- 阻断 raw payload、credential/cookie 泄漏、accepted / integrated / production_ready 声明。
- 本门禁不执行真实目标站读取，只校验已有输出或离线自测 fixture。

## Validator Checks

- allows_critical_target_availability_warnings_when_topic_threshold_passes: `True`
- allows_noncritical_discovery_fetch_errors_when_threshold_passes: `True`
- blocks_credential_leak: `True`
- blocks_forbidden_claims: `True`
- blocks_raw_payload_persistence: `True`
- requires_allowed_content_type: `True`
- requires_authorization_valid: `True`
- requires_business_field_mapping: `True`
- requires_candidate_only_non_claims: `True`
- requires_completed_status: `True`
- requires_discovery_rank: `True`
- requires_execution_requested: `True`
- requires_four_topic_reports: `True`
- requires_keyword_hit_per_topic: `True`
- requires_live_external_fetch_invoked: `True`
- requires_markdown_candidate_only_marker: `True`
- requires_markdown_non_claim_marker: `True`
- requires_p0_hit_per_topic: `True`
- requires_requested_and_final_url: `True`
- requires_retry_count: `True`
- requires_source_direct_candidate_schema: `True`
- requires_topic_coverage_one: `True`
- self_test_passed_without_network: `True`

## 边界

- This evidence is candidate-only.
- This evidence does not create source-of-record.
- This evidence does not write KDS canonical Markdown.
- This evidence does not write GFIS source-of-record.
- This evidence does not claim accepted, integrated, or production_ready status.
