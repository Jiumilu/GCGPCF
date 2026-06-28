---
doc_id: GPCF-DOC-GFIS-RUNTIME-SOP-E2E-MIN-001
title: GFIS-RUNTIME-SOP-E2E-MIN-001
project: GPCF
related_projects: [GPCF, GFIS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-MIN-001.md
source_path: docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-MIN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-MIN-001

## 1. Delivery Target

本任务包服务 LOOP v1.1：治理瘦身与交付恢复。目标不是继续扩展工具链，而是准备一条真实业务来源记录进入 GFIS runtime SOP E2E 最小闭环候选链。

```text
GFIS-RUNTIME-SOP-E2E-MIN-001
candidate_lane
gfis-runtime-sop-e2e-min-001-candidate.json
validate_gfis_runtime_sop_e2e_min_001.py
source_record_candidates=1
runtime_primary_key_candidates=1
runtime_intake_candidates=1
review_queue_candidates=1
waes_review_candidates=1
verified_artifact_candidates=1
```

## 2. GFIS DEV Chain Anchors

```text
GFIS-DEV-001
gfis-dev-001-source-record-runtime-readiness-chain.json
validate_gfis_dev_001_source_record_runtime_readiness_chain.py
gfis_dev_001_source_record_runtime_readiness_chain=pass
kds_candidate_sources_observed=466

GFIS-DEV-002
gfis-dev-002-valid-source-record-index-template-readiness.json
validate_gfis_dev_002_valid_source_record_index_template_readiness.py
gfis_dev_002_valid_source_record_index_template_readiness=pass
valid-source-record-index.template.json

GFIS-DEV-003
gfis-dev-003-valid-source-record-index-schema-preflight.json
validate_gfis_dev_003_valid_source_record_index_schema_preflight.py
gfis_dev_003_valid_source_record_index_schema_preflight=pass
valid-source-record-index.schema.json
external_candidate_preflight_supported=true
external_candidate_dir_preflight_supported=true
report_json_supported=true
temp_valid_candidates=1
temp_invalid_candidates=1

GFIS-DEV-004
gfis-dev-004-valid-source-record-pre-submission-package.json
validate_gfis_dev_004_valid_source_record_pre_submission_package.py
gfis_dev_004_valid_source_record_pre_submission_package=pass
package_preview_supported=true
external_candidate_package_preview_supported=true
copy_to_real_target_executed=false
real_target_files=0

GFIS-DEV-005
gfis-dev-005-source-record-owner-submission-handoff-readiness.json
validate_gfis_dev_005_source_record_owner_submission_handoff_readiness.py
gfis_dev_005_source_record_owner_submission_handoff_readiness=pass
handoff_steps=5
receiving_scan_hold_gate_ready=true
source_record_files_found=0

GFIS-DEV-006
gfis-dev-006-external-candidate-handoff-dry-run.json
validate_gfis_dev_006_external_candidate_handoff_dry_run.py
gfis_dev_006_external_candidate_handoff_dry_run=pass
external_candidate_handoff_dry_run_supported=true
dry_run_pipeline_steps=4
valid_candidate_handoff_ready=1
invalid_candidate_rejected=1

GFIS-DEV-007
gfis-dev-007-external-candidate-dir-handoff-dry-run.json
validate_gfis_dev_007_external_candidate_dir_handoff_dry_run.py
gfis_dev_007_external_candidate_dir_handoff_dry_run=pass
external_candidate_dir_handoff_dry_run_supported=true
valid_dir_handoff_ready=1
invalid_dir_rejected=1

GFIS-DEV-008
gfis-dev-008-external-candidate-dir-remediation-summary.json
validate_gfis_dev_008_external_candidate_dir_remediation_summary.py
gfis_dev_008_external_candidate_dir_remediation_summary=pass
external_candidate_dir_remediation_summary_supported=true
invalid_dir_error_code_count=4
remediation_actions=4

GFIS-DEV-009
gfis-dev-009-external-candidate-dir-manual-submission-manifest.json
validate_gfis_dev_009_external_candidate_dir_manual_submission_manifest.py
gfis_dev_009_external_candidate_dir_manual_submission_manifest=pass
external_candidate_dir_manual_submission_manifest_supported=true
valid_dir_manifest_ready=1
valid_dir_manifest_item_count=1
collision_dir_manifest_ready=0
collision_dir_target_filename_conflicts=1
invalid_dir_manifest_ready=0

GFIS-DEV-010
gfis-dev-010-manual-submission-command-preview.json
validate_gfis_dev_010_manual_submission_command_preview.py
gfis_dev_010_manual_submission_command_preview=pass
manual_submission_command_preview_supported=true
valid_dir_preview_command_count=1
command_executed=false
copy_to_real_target_executed=false

GFIS-DEV-011
gfis-dev-011-manual-execution-authorization-preflight.json
validate_gfis_dev_011_manual_execution_authorization_preflight.py
gfis_dev_011_manual_execution_authorization_preflight=pass
manual_execution_authorization_preflight_supported=true
authorization_template_preview_supported=true
post_submit_verification_plan_supported=true
post_submit_verification_plan_commands=7
valid_authorization_preflight_ready=1
temp_authorization_templates=1
mismatched_authorization_preflight_ready=0
incomplete_authorization_preflight_ready=0
unchanged_template_preflight_ready=0
--emit-authorization-template
--emit-post-submit-verification-plan
```

## 3. 当前最小人工输入请求

下一步不应继续扩展工具链。当前推荐输入是 A：

A. 提供 1 份已脱敏的 `CustomerRequirementOrPlatformOrder` source-of-record index 候选文件或候选目录，用于 external-path preflight。

B. 确认 1 条等效正式业务确认，作为 source-of-record 候选来源；该确认只进入候选链，不自动成为 accepted/integrated。

C. 明确授权人工操作员按 DEV-010/DEV-011 预检通过的命令，把已通过 preflight 的候选手动提交到正式接收目录；该授权不包括自动脚本执行。

可填写模板位于 GFIS 仓：

```text
docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/customer-requirement-platform-order.valid-source-record-index.template.json
```

模板字段要求：

```text
source_kind = customer_confirmation | platform_order_receipt | purchase_order | equivalent_formal_confirmation
source_record_uri = required
source_record_hash = required sha256-hex-64
customer_name = required
product = required
quantity = required
delivery_requirement = required
quality_requirement = required
owner_confirmation.valid = true only after source owner confirms
kds_source_backlink.uri = required
waes_evidence_candidate.id = required
```

候选目录预检命令只读示例：

```bash
python3 scripts/validate_gfis_dev_007_external_candidate_dir_handoff_dry_run.py --candidate-dir /path/to/sanitized-index-candidates --report-json
python3 scripts/validate_gfis_dev_009_external_candidate_dir_manual_submission_manifest.py --candidate-dir /path/to/sanitized-index-candidates --report-json
python3 scripts/validate_gfis_dev_010_manual_submission_command_preview.py --candidate-dir /path/to/sanitized-index-candidates --report-json
python3 scripts/validate_gfis_dev_011_manual_execution_authorization_preflight.py --candidate-dir /path/to/sanitized-index-candidates --report-json
```

DEV-010/DEV-011 当前只允许 `manual_submission_command_preview_ready_no_real_write` 与 `manual_execution_authorization_preflight_ready_no_real_write`；`command_execution_allowed=false`、`copy_to_real_target_executed=false`、`script_execution_allowed=false`、`commit_allowed=false`、`push_allowed=false`、`deploy_allowed=false`、`status_promotion_allowed=false`。

```text
next_required_input=real_source_record_or_equivalent_formal_confirmation
manual_business_verification_pending=true
real_business_lane=repair_required
```

## 4. Boundary

GFIS 目标链路术语：runtime intake、review queue、WAES review、verified artifact candidate。

禁止项：生产写入、真实外部 API 写入、schema migrate、commit、push、deploy、真实 KDS API 写入。

```text
valid_source_records=0
runtime_primary_key_ready=0
review_queue=0
runtime_intake=0
waes_review=0
verified=0
accepted=false
integrated=false
production_ready=false
customer_accepted=false
```
