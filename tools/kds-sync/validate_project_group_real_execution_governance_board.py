#!/usr/bin/env python3
"""Validate the GlobalCloud project-group real execution governance board."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_PROJECTS = [
    "AAAS",
    "Brain",
    "WAS",
    "XiaoC",
    "WAES",
    "GPC",
    "Studio",
    "GPCF",
    "XWAIL",
    "GFIS",
    "MMC",
    "KDS",
    "XiaoG",
    "PVAOS",
    "SOP",
    "PKC",
    "XGD",
]

REQUIRED_TASKS = [
    "GFIS-REAL-SOR-001",
    "WAES-LINT-RUNTIME-001",
    "KDS-RAG-EXPORT-001",
    "AAAS-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "SOP-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "XWAIL-MIN-VALIDATOR-001",
    "AAAS-SERVICE-RUNTIME-001",
    "AAAS-WAES-BINDING-PRECHECK-001",
    "PVAOS-RELEASE-GATE-001",
    "PVAOS-RELEASE-REVIEW-001",
    "GPC-EVIDENCE-BROWSER-001",
    "BRAIN-REVIEW-HANDOFF-001",
    "GPCF-GIT-CLEAN-001",
    "GPCF-GIT-DIRTY-CLASSIFY-001",
    "GPCF-REVIEW-PACKAGE-001",
    "GPCF-HUMAN-CONFIRMATION-REQUEST-001",
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001",
    "GPCF-DIRTY-DISPOSITION-QUEUE-001",
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001",
    "GPCF-LOOP-GATE-READINESS-PASS-20260626-001",
    "GPCF-FIRST-EXECUTION-AUTHORIZATION-REQUEST-20260626-001",
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-TEMPLATE-20260626-001",
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "GPCF-AUTHORIZATION-PRE-EXECUTION-COMMAND-PACK-20260626-001",
    "GPCF-AUTHORIZATION-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001",
    "GPCF-FULL-PROJECT-BASELINE-001",
    "GPCF-DEV-TASK-QUEUE-20260626-001",
    "GPCF-NEXT-TASK-PACKS-001",
    "GPCF-DEPENDENCY-MATRIX-001",
    "GPCF-STATUS-ADVANCEMENT-001",
    "GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001",
    "GPCF-KDS-DIFFCHECK-BLOCKER-20260626-001",
    "GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001",
    "GPCF-SCHEME-RECOGNITION-RULES-20260626-001",
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-CONSISTENCY-AUDIT-20260627-001",
    "GPCF-LOOP-DOCUMENT-GATE-READINESS-RETRY-HARDENING-20260626-001",
    "GPCF-REAL-EXECUTION-OBJECTIVE-COVERAGE-AUDIT-20260626-001",
    "WAS-XWAIL-ONTOLOGY-MAPPING-001",
    "XIAOC-MODEL-ROUTING-DRYRUN-001",
    "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
    "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
    "XGD-TICK-BRAIN-SMOKE-001",
    "STUDIO-WORKFLOW-PERMISSIONS-001",
    "XIAOG-LIVE-API-AUTH-PACK-001",
    "SOP-SCENARIO-OWNER-REVIEW-001",
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
    "GPCF-EXECUTION-CONTROL-001",
]

REQUIRED_FIELDS = [
    "task_id",
    "project",
    "baseline_evidence",
    "commands",
    "expected_evidence",
    "gate",
    "rollback",
    "dependency_impact",
    "human_confirmation_required",
    "forbidden_claims",
]

REQUIRED_DEPENDENCIES = [
    "WAES -> XWAIL -> AaaS",
    "KDS -> Brain",
    "GFIS/GPC/PVAOS -> SCaaS",
    "WAS -> Ontology -> XWAIL",
    "GPCF -> all projects",
]

REQUIRED_STATUS_TOKENS = [
    "candidate",
    "partial_verified",
    "ready_for_review",
    "ready_for_uat",
    "accepted",
    "integrated",
    "customer_accepted",
]

REQUIRED_BOUNDARY_TOKENS = [
    "| 项目 | 当前状态 | trigger_layer | 证据基线 | 当前推进边界 |",
    "### 3.1 17 项目全量状态基线索引",
    "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md",
    "validate_project_group_dev_task_queue_20260626.py",
    "development_queue = controlled",
    "development_queue_status = development_queue_ready",
    "trigger_layer_binding_count = 17",
    "dependency_edge_binding_count = 17",
    "authorization_to_pre_execution_total_bridge",
    "pre_wave1_review_bridge",
    "local_release_review_boundary",
    "mock、fixture、synthetic/dev-only 数据",
    "未经授权的生产、权限或部署动作",
    "project_group_real_execution_completion_gap_matrix_20260626 = controlled",
    "real_execution_completion_gap_matrix_result = coverage_controlled_count=7 / execution_complete_count=0 / remaining_gap_count=7",
    "external_loop_gate_delegate_baseline_ready",
    "pre_wave1_review_authorization_ready",
    "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md",
    "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_FULL_BASELINE_TOKENS = {
    "WAS世界资产体系": [
        "semantic_foundation_candidate / not_accepted / xwail_mapping_candidate",
        "WAS-XWAIL-ONTOLOGY-MAPPING-001",
        "不声明 KDS 事实主存",
    ],
    "GlobalCloud XWAIL": [
        "ready_for_review / local_dev_boundary / integration_precheck_candidate / not_accepted",
        "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
        "不声明完整工具链闭环",
    ],
    "GlobalCloud AaaS / AAAS": [
        "ready_for_review / local_dev_boundary / integration_precheck_candidate / not_accepted",
        "AAAS-SERVICE-RUNTIME-001",
        "AAAS-WAES-BINDING-PRECHECK-001",
        "不声明真实计费",
    ],
    "GlobalCloud WAES": [
        "repair_required / authorization_required",
        "WAES-LINT-RUNTIME-001",
        "不声明治理运行闭环",
    ],
    "GlobalCloud GFIS": [
        "partial_verified / repair_required",
        "GFIS-REAL-SOR-001",
        "不声明真实 SOP E2E",
    ],
    "GlobalCloud GPC": [
        "external_runtime_evidence_required",
        "GPC-EVIDENCE-BROWSER-001",
        "不声明外部联调完成",
    ],
    "GlobalCloud PVAOS": [
        "ready_for_review / local_release_gate_boundary / review_candidate",
        "PVAOS-RELEASE-REVIEW-001",
        "不声明远程 CI",
    ],
    "GlobalCloud KDS": [
        "owner_review_required / kds_report_hold_controlled / kds_blocker_resolved",
        "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
        "不声明真实交付",
    ],
    "GlobalCloud Brain": [
        "ready_for_review / authorization_boundary / ready_for_human_review",
        "BRAIN-REVIEW-HANDOFF-001",
        "不声明 accepted",
    ],
    "GlobalCloud Studio": [
        "release_boundary_recheck_passed / local_release_review_boundary",
        "STUDIO-WORKFLOW-PERMISSIONS-001",
        "不声明 GitHub release 写入",
    ],
    "GlobalCloud MMC": [
        "task_pack_ready / local_document_smoke_boundary",
        "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
        "不声明 MMC runtime 已通过",
    ],
    "GlobalCloud PKC": [
        "task_pack_ready / local_dev_dryrun_boundary",
        "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
        "不声明真实 KDS/Brain 集成",
    ],
    "GlobalCloud SOP": [
        "owner_review_required / scenario_candidate_controlled / not_accepted",
        "SOP-SCENARIO-OWNER-REVIEW-001",
        "不声明场景方案已确认",
    ],
    "GlobalCloud XGD": [
        "task_pack_ready / local_dev_smoke_boundary",
        "XGD-TICK-BRAIN-SMOKE-001",
        "不声明长程 Agent 生产可用",
    ],
    "GlobalCloud XiaoC": [
        "baseline_controlled / environment_blocked",
        "XIAOC-MODEL-ROUTING-DRYRUN-001",
        "不声明 dry-run 通过",
    ],
    "GlobalCloud XiaoG": [
        "task_pack_ready / authorization_pack_ready",
        "XIAOG-LIVE-API-AUTH-PACK-001",
        "不声明 live API",
    ],
    "GlobalCoud GPCF": [
        "execution_governance_controlled",
        "GPCF-EXECUTION-CONTROL-001",
        "不声明项目群 Git 全量 clean",
    ],
}

REQUIRED_TASK_DETAIL_TOKENS = {
    "GFIS-REAL-SOR-001": [
        "validate_gfis_was_source_record_submission_precheck.py",
        "gfis-real-source-record-intake-*",
        "WAES review gate",
        "保持 `repair_required`",
        "是，需要订单 owner",
    ],
    "WAES-LINT-RUNTIME-001": [
        "npm run check",
        "waes-lint-runtime-repair-*",
        "WAES quality gate",
        "回滚 lint 修复相关文件",
        "不声明 WAES 治理运行闭环完成",
    ],
    "KDS-RAG-EXPORT-001": [
        "validate_rag_export.py",
        "kds-rag-export-repair-20260625.md",
        "KDS RAG export gate",
        "validate_kds_rag_export_repair.py",
        "回滚 `_governance/scripts/rag_admission_policy.py`",
        "不声明 KDS 真实运行闭环完成",
    ],
    "XWAIL-MIN-VALIDATOR-001": [
        "validate_xwail.py",
        "xwail-min-validator-runtime-20260625.md",
        "XWAIL validator gate",
        "validate_xwail_min_validator_runtime.py",
        "verified_with_local_dev_boundary",
        "回滚新增 `scripts/`、`schemas-json/`、`models/`、`packages/`",
        "不声明完整 XWAIL 工具链完成",
    ],
    "AAAS-SERVICE-RUNTIME-001": [
        "validate_service_package.py",
        "aaas-service-runtime-20260625.md",
        "AaaS service runtime gate",
        "validate_aaas_service_runtime.py",
        "verified_with_local_dev_boundary",
        "回滚新增 `scripts/`、`schemas-json/`、`service-packages/`",
        "不声明客户可订阅",
    ],
    "AAAS-WAES-BINDING-PRECHECK-001": [
        "validate_aaas_waes_binding_precheck.py",
        "aaas-waes-binding-precheck-20260625.md",
        "aaas_waes_binding_precheck = controlled",
        "integration_precheck_candidate",
        "WAES status = Draft",
        "candidate_only_not_published",
        "realCustomerSubscription = false",
        "不声明 WAES 发布",
        "不声明 AaaS 上架",
    ],
    "PVAOS-RELEASE-GATE-001": [
        "npm run release:gate:local",
        "pvaos-release-gate-repair-20260625.md",
        "PVAOS release local gate",
        "validate_pvaos_release_gate_repair.py",
        "verified_with_local_release_gate_boundary",
        "回滚 `vitest.config.ts`、`package.json`、`package-lock.json`",
        "不声明发布完成",
    ],
    "PVAOS-RELEASE-REVIEW-001": [
        "npm run release:gate:local",
        "pvaos-release-review-20260625.md",
        "review_candidate",
        "validate_pvaos_release_review.py",
        "Playwright `50 passed` / `4 skipped`",
        "production domain/CORS pass",
        "不声明远程 CI",
    ],
    "GPC-EVIDENCE-BROWSER-001": [
        "npm run quality:repo",
        "gpc-evidence-browser-repair-20260625.md",
        "browser/e2e gate",
        "validate_gpc_evidence_browser_repair.py",
        "partial_verified_browser_repaired_external_runtime_evidence_required",
        "回滚 README 索引",
        "不声明外部联调完成",
    ],
    "BRAIN-REVIEW-HANDOFF-001": [
        "npm run validate:harness-evidence",
        "brain-review-handoff-20260625.md",
        "validate_brain_review_handoff.py",
        "human review gate",
        "保持 `ready_for_review / authorization_boundary`",
        "需要人工确认才能升级",
    ],
    "GPCF-GIT-CLEAN-001": [
        "project_group_git_clean_gate.py",
        "globalcloud-project-group-git-clean-20260625.md",
        "globalcloud-project-group-git-clean-20260625.json",
        "validate_project_group_git_clean_evidence.py",
        "project_group_git_clean = partial",
        "不自动 clean、stash、commit、push 或 reset",
        "不声明项目群 Git 全量 clean",
    ],
    "GPCF-GIT-DIRTY-CLASSIFY-001": [
        "git status --short --untracked-files=all",
        "globalcloud-project-group-dirty-classification-20260625.md",
        "validate_project_group_dirty_classification.py",
        "project_group_dirty_classification = controlled",
        "不自动删除 `.DS_Store`",
        "不声明项目群可提交",
    ],
    "GPCF-REVIEW-PACKAGE-001": [
        "validate_project_group_review_packages.py",
        "globalcloud-project-group-review-packages-20260625.md",
        "project_group_review_packages = controlled",
        "4 个 review 包",
        "3 个 hold 包",
        "不自动 stage、commit、push、merge",
        "不声明真实 KDS API 已同步",
    ],
    "GPCF-HUMAN-CONFIRMATION-REQUEST-001": [
        "validate_project_group_human_confirmation_request.py",
        "globalcloud-project-group-human-confirmation-request-20260625.md",
        "project_group_human_confirmation_request = prepared",
        "7 个确认项",
        "review_allowed=false",
        "stage_allowed=false",
        "commit_allowed=false",
        "push_allowed=false",
        "不声明已授权 review",
    ],
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001": [
        "validate_project_group_authorization_routing.py",
        "globalcloud-project-group-authorization-routing-20260625.md",
        "project_group_authorization_routing = prepared",
        "authorization_routing_ready",
        "7 条授权路由",
        "review_allowed=false",
        "stage_allowed=false",
        "commit_allowed=false",
        "push_allowed=false",
        "delete_allowed=false",
        "不声明已授权 review",
    ],
    "GPCF-DIRTY-DISPOSITION-QUEUE-001": [
        "validate_project_group_dirty_disposition_queue.py",
        "globalcloud-project-group-dirty-disposition-queue-20260625.md",
        "project_group_dirty_disposition_queue = controlled",
        "dirty_disposition_queue_ready",
        "review_candidate_count = 4",
        "owner_decision_count = 2",
        "noise_decision_count = 1",
        "不自动删除 `.DS_Store`",
        "不声明项目群 Git 全量 clean",
    ],
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001": [
        "validate_project_group_live_status_snapshot_20260626.py",
        "globalcloud-project-group-live-status-snapshot-20260626.md",
        "project_group_live_status_snapshot_20260626 = controlled",
        "live_status_snapshot_controlled",
        "dirty_repo_count = 5",
        "pass_repo_count = 12",
        "2026-06-30",
        "ahead_repo_count = 2",
        "project_group_git_clean = partial",
        "不自动删除",
        "不声明项目群 Git 全量 clean",
    ],
    "GPCF-LOOP-GATE-READINESS-PASS-20260626-001": [
        "validate_project_group_loop_gate_readiness_pass_20260626.py",
        "globalcloud-project-group-loop-gate-readiness-pass-20260626.md",
        "project_group_loop_gate_readiness_20260626 = pass",
        "loop_gate_readiness_pass",
        "passed_repos = 13",
        "failed_repos = 0",
        "不声明项目群 Git 全量 clean",
        "不声明可提交/可推送",
    ],
    "GPCF-FIRST-EXECUTION-AUTHORIZATION-REQUEST-20260626-001": [
        "validate_project_group_first_execution_authorization_request_20260626.py",
        "globalcloud-project-group-first-execution-authorization-request-20260626.md",
        "project_group_first_execution_authorization_request_20260626 = prepared",
        "first_execution_authorization_request_prepared",
        "7 个确认项",
        "review_allowed=false",
        "delete_allowed=false",
        "不声明任何包已授权",
    ],
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-TEMPLATE-20260626-001": [
        "validate_project_group_execution_authorization_receipt_template_20260626.py",
        "globalcloud-project-group-execution-authorization-receipt-template-20260626.md",
        "project_group_execution_authorization_receipt_template_20260626 = controlled",
        "execution_authorization_receipt_template_ready",
        "7 个回执模板",
        "authorization_granted=false",
        "action_executed=false",
        "不声明任何授权已经发生",
    ],
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001": [
        "validate_project_group_execution_authorization_receipt_ledger_20260626.py",
        "globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md",
        "project_group_execution_authorization_receipt_ledger_20260626 = controlled",
        "execution_authorization_receipt_ledger_ready",
        "receipt_record_count = 0",
        "pending_authorization_items = 7",
        "不声明任何授权已经发生",
    ],
    "GPCF-AUTHORIZATION-PRE-EXECUTION-COMMAND-PACK-20260626-001": [
        "validate_project_group_authorization_pre_execution_command_pack_20260626.py",
        "globalcloud-project-group-authorization-pre-execution-command-pack-20260626.md",
        "project_group_authorization_pre_execution_command_pack_20260626 = controlled",
        "authorization_pre_execution_command_pack_ready",
        "command_pack_count = 7",
        "receipt_record_count = 0",
        "不声明任何命令包已执行",
    ],
    "GPCF-AUTHORIZATION-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001": [
        "validate_project_group_authorization_pre_execution_environment_readiness_20260626.py",
        "globalcloud-project-group-authorization-pre-execution-environment-readiness-20260626.md",
        "project_group_authorization_pre_execution_environment_readiness_20260626 = controlled",
        "authorization_pre_execution_environment_ready",
        "repo_path_check_pass = 7",
        "gpcf_validator_check_pass = 11",
        "不声明任何命令包已执行",
    ],
    "GPCF-FULL-PROJECT-BASELINE-001": [
        "validate_project_group_full_project_baseline.py",
        "globalcloud-project-group-full-project-baseline-20260625.md",
        "17 项目全量真实状态基线",
        "full_project_baseline = controlled",
        "baseline-only 项目下一批任务包",
        "不自动修改 17 仓源码",
        "不声明全项目 ready_for_review",
    ],
    "GPCF-NEXT-TASK-PACKS-001": [
        "validate_project_group_next_executable_task_packs.py",
        "globalcloud-project-group-next-executable-task-packs-20260625.md",
        "17 项目下一批可执行任务包",
        "next_executable_task_packs = controlled",
        "Wave 1/Wave 2/Wave 3/Governance",
        "不自动执行 17 仓任务",
        "不声明任务已执行",
    ],
    "GPCF-DEPENDENCY-MATRIX-001": [
        "validate_project_group_dependency_execution_matrix.py",
        "globalcloud-project-group-dependency-execution-matrix-20260625.md",
        "12 条依赖边",
        "dependency_execution_matrix = controlled",
        "状态传导规则",
        "不自动执行依赖任务",
        "不声明完整集成",
    ],
    "GPCF-STATUS-ADVANCEMENT-001": [
        "validate_project_group_status_advancement_matrix.py",
        "globalcloud-project-group-status-advancement-matrix-20260625.md",
        "17 项目状态推进规则",
        "status_advancement_matrix = controlled",
        "全局升级规则和禁止升级条件",
        "不自动升级项目状态",
        "不声明状态已升级",
    ],
    "GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001": [
        "validate_project_group_ready_for_review_advancement_queue_20260626.py",
        "globalcloud-project-group-ready-for-review-advancement-queue-20260626.md",
        "project_group_ready_for_review_advancement_queue_20260626 = controlled",
        "ready_for_review_advancement_queue_ready",
        "project_count = 17",
        "auto_ready_for_review_upgrade=false",
        "不声明任何项目已自动升级到 ready_for_review",
    ],
    "GPCF-KDS-DIFFCHECK-BLOCKER-20260626-001": [
        "validate_project_group_kds_diffcheck_blocker_20260626.py",
        "globalcloud-project-group-kds-diffcheck-blocker-20260626.md",
        "project_group_kds_diffcheck_blocker_20260626 = controlled",
        "kds_diffcheck_blocker_controlled",
        "diff_check_pass_current",
        "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
        "不声明 cleanup 已执行",
        "不声明项目群 Git 全量 clean",
    ],
    "GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001": [
        "validate_project_group_kds_diffcheck_cleanup_command_pack_20260626.py",
        "globalcloud-project-group-kds-diffcheck-cleanup-command-pack-20260626.md",
        "project_group_kds_diffcheck_cleanup_command_pack_20260626 = controlled",
        "kds_diffcheck_cleanup_command_pack_ready",
        "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
        "authorization_granted=false",
        "cleanup_executed=false",
        "不声明 cleanup 已执行",
        "不声明 KDS diff check 已修复",
    ],
    "GPCF-SCHEME-RECOGNITION-RULES-20260626-001": [
        "validate_project_group_scheme_recognition_rules_20260626.py",
        "GlobalCloud 项目群方案体系识别规则.md",
        "project_group_scheme_recognition_rules = controlled",
        "scheme_recognition_rules_controlled",
        "agents_recognition_scope = 17 projects",
        "project_plan_inheritance_scope = 34 files",
        "不声明真实运行完成",
        "不声明 accepted/integrated/customer accepted",
    ],
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001": [
        "validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py",
        "globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md",
        "project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled",
        "dirty_disposition_queue_post_scheme_recognition_ready",
        "dirty_repo_count = 3",
        "project_group_git_clean = partial",
        "不自动删除、cleanup、stage、commit、push",
        "不声明项目群 Git 全量 clean",
    ],
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001": [
        "validate_project_group_post_scheme_recognition_review_authorization_request_20260626.py",
        "globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md",
        "project_group_post_scheme_recognition_review_authorization_request_20260626 = prepared",
        "post_scheme_recognition_review_authorization_request_prepared",
        "request_item_count = 3",
        "review_allowed=false",
        "不声明任何 scheme review 已授权",
        "不声明可 stage/commit/push",
    ],
    "GPCF-LOOP-DOCUMENT-GATE-READINESS-RETRY-HARDENING-20260626-001": [
        "validate_loop_document_gate_readiness_retry_hardening_20260626.py",
        "globalcloud-loop-document-gate-readiness-retry-hardening-20260626.md",
        "loop_document_gate_readiness_retry_hardening_20260626 = controlled",
        "loop_document_gate_readiness_retry_hardening_controlled",
        "retry_count = 1",
        "gate_relaxed=false",
        "不声明门禁被放松",
        "不声明项目群 Git 全量 clean",
    ],
    "GPCF-REAL-EXECUTION-OBJECTIVE-COVERAGE-AUDIT-20260626-001": [
        "validate_project_group_real_execution_objective_coverage_audit_20260626.py",
        "globalcloud-project-group-real-execution-objective-coverage-audit-20260626.md",
        "project_group_real_execution_objective_coverage_audit_20260626 = controlled",
        "real_execution_objective_coverage_audit_controlled",
        "requirement_count = 7",
        "covered_requirement_count = 7",
        "不声明目标全部完成",
    ],
    "WAS-XWAIL-ONTOLOGY-MAPPING-001": [
        "validate_was_xwail_ontology_mapping.py",
        "was-xwail-ontology-mapping-20260625.md",
        "xwail_mapping_candidate",
        "8/8 dimensions checked",
        "8/8 flows checked",
        "Ontology `0.1.0`",
        "XWAIL `ontologyRef`",
        "不声明 WAES 发布",
        "不声明 AaaS 绑定",
    ],
    "XIAOC-MODEL-ROUTING-DRYRUN-001": [
        "validate_xiaoc_model_routing_dryrun_environment_blocked.py",
        "xiaoc-model-routing-dryrun-environment-blocked-20260625.md",
        "xiaoc_model_routing_dryrun = environment_blocked",
        "required_node = ^22.0.0",
        "actual_node = v26.0.0",
        "commands_failed = 4",
        "baseline_controlled / environment_blocked",
        "不声明 XiaoC dry-run 通过",
        "不声明真实部署",
    ],
    "MMC-GOVERNANCE-TEMPLATE-SMOKE-001": [
        "validate_mmc_governance_template_smoke.py",
        "mmc-governance-template-smoke-20260625.md",
        "mmc_governance_template_smoke = controlled",
        "task_pack_ready / local_document_smoke_boundary",
        "runtime_verified = false",
        "integration_verified = false",
        "保持 `baseline_controlled`",
        "不声明 MMC runtime 已通过",
        "不声明下游项目已接入 MMC 模板",
    ],
    "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001": [
        "validate_pkc_kds_brain_workflow_dryrun.py",
        "pkc-kds-brain-workflow-dryrun-20260625.md",
        "pkc_kds_brain_workflow_dryrun = controlled",
        "task_pack_ready / local_dev_dryrun_boundary",
        "test_files = 10 passed",
        "tests = 57 passed",
        "保持 `baseline_controlled`",
        "不声明 PKC 端到端用户闭环完成",
        "不声明真实 KDS/Brain 集成",
    ],
    "XGD-TICK-BRAIN-SMOKE-001": [
        "validate_xgd_tick_brain_smoke.py",
        "xgd-tick-brain-smoke-20260625.md",
        "xgd_tick_brain_smoke = controlled",
        "task_pack_ready / local_dev_smoke_boundary",
        "unit_suites = 5/5",
        "brain_ui_smoke = pass",
        "保持 `baseline_controlled`",
        "不声明长程 Agent 生产可用",
        "不声明真实外部动作",
    ],
    "STUDIO-WORKFLOW-PERMISSIONS-001": [
        "validate_studio_workflow_permissions_recheck.py",
        "studio-workflow-permissions-recheck-20260625.md",
        "studio_workflow_permissions_recheck = controlled",
        "release_boundary_recheck_passed / local_release_review_boundary",
        "test_files = 256 passed",
        "tests = 1919 passed / 2 skipped",
        "build = pass",
        "不声明 Studio 已发布",
        "不声明 GitHub release 已写入",
    ],
    "XIAOG-LIVE-API-AUTH-PACK-001": [
        "validate_xiaog_live_api_auth_pack.py",
        "xiaog-live-api-auth-pack-20260625.md",
        "xiaog_live_api_auth_pack = controlled",
        "task_pack_ready / authorization_pack_ready",
        "readonly_queries = 3",
        "pkc_notification_candidates = 1",
        "waes_audit_mocks = 2",
        "network_call_executed = false",
        "production_write_executed = false",
        "不声明 live GFIS/GPC API 已验证",
        "不声明真实 WAES 审计写入完成",
    ],
    "SOP-SCENARIO-OWNER-REVIEW-001": [
        "validate_sop_scenario_owner_review.py",
        "sop-scenario-owner-review-20260625.md",
        "sop_scenario_owner_review = controlled",
        "owner_review_required / scenario_candidate_controlled",
        "scenario_document_status = draft_for_special_team_meeting",
        "scenario_owner_confirmed = false",
        "kds_fact_ingested = false",
        "不声明场景方案已确认",
        "不声明 KDS 事实主存已入库",
    ],
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001": [
        "validate_kds_brain_report_hold_review.py",
        "kds-brain-report-hold-review-20260625.md",
        "kds_brain_report_hold_review = controlled",
        "owner_review_required / kds_report_hold_controlled",
        "funding_report_owner_confirmed = false",
        "kds_api_sync_executed = false",
        "brain_ingestion_confirmed = false",
        "不声明资金追踪报告已经业务确认",
        "不声明真实 KDS API 已同步",
    ],
    "GPCF-EXECUTION-CONTROL-001": [
        "validate_project_group_real_execution_governance_board.py",
        "项目群真实执行任务变更记录",
        "Loop document gate",
        "最高状态为 `partial/rework`",
        "不声明项目群完成",
    ],
    "GPCF-DEV-TASK-QUEUE-20260626-001": [
        "validate_project_group_dev_task_queue_20260626.py",
        "globalcloud-project-group-dev-task-queue-20260626.md",
        "development_queue_ready = true",
        "trigger_layer_binding_count = 17",
        "dependency_edge_binding_count = 17",
        "binding_row_count = 17",
        "不自动执行 17 仓开发态任务",
        "不声明任何开发态任务已执行",
    ],
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001": [
        "validate_project_group_pre_wave1_review_authorization_request_20260627.py",
        "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
        "pre_wave1_review_authorization_ready",
        "wave1_entry_blocked_by_pre_review = true",
        "review_boundary_count = 3",
        "pending_confirmation",
        "不声明 Wave 1 已授权",
    ],
    "GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001": [
        "validate_project_group_next_stage_authorization_human_fill_request_20260627.py",
        "globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md",
        "project_group_next_stage_authorization_human_fill_request_20260627 = prepared",
        "next_stage_authorization_human_fill_request_ready",
        "fill_item_count = 7",
        "authorization_granted_count = 0",
        "不声明任何 human fill request 已转成真实授权",
    ],
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-CONSISTENCY-AUDIT-20260627-001": [
        "validate_project_group_next_stage_authorization_chain_consistency_audit_20260627.py",
        "globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md",
        "project_group_next_stage_authorization_chain_consistency_audit_20260627 = controlled",
        "next_stage_authorization_chain_consistency_audit_ready",
        "auth_count = 7",
        "execution_ledger_auth_count = 1",
        "post_scheme_ledger_auth_count = 6",
        "不声明任何 receipt 已真实写入总账",
    ],
}

FORBIDDEN_UNBOUNDED_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

GFIS_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "formal_confirmation_files",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def validate_gfis_real_fact_entry(failures: list[str]) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            failures.append("GFIS real-fact entry gate failed: " + result.stdout.strip())
            return values
    if values.get("strong_block") != "true":
        failures.append("GFIS real-fact entry gate must keep strong_block=true")
    if values.get("status_ceiling") != "repair_required":
        failures.append("GFIS real-fact entry status ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            failures.append(f"GFIS real-fact entry must keep {key}=0, got {values.get(key)!r}")
    for key in ["accepted", "integrated", "production_ready"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def main() -> int:
    failures: list[str] = []
    board_text = read(BOARD, failures)
    register_text = read(CORE_REGISTER, failures)
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    for token in [
        "GlobalCloud 项目群真实执行治理总控板",
        "project_group_real_execution_governance = controlled",
        "project_group_real_execution_board = established",
        "next_execution_mode = project_by_project_real_gate_repair",
    ]:
        if token not in board_text:
            failures.append(f"missing board control token: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in board_text:
            failures.append(f"missing project in board: {project}")

    for task in REQUIRED_TASKS:
        if task not in board_text:
            failures.append(f"missing task in board: {task}")

    for task, tokens in REQUIRED_TASK_DETAIL_TOKENS.items():
        row_prefix = f"| `{task}` |"
        rows = [line for line in board_text.splitlines() if line.startswith(row_prefix)]
        if len(rows) != 1:
            failures.append(f"task must have exactly one execution control row: {task}")
            continue
        row = rows[0]
        columns = [part.strip() for part in row.strip().strip("|").split("|")]
        if len(columns) != 10:
            failures.append(f"task execution control row must have 10 columns: {task}")
        for token in tokens:
            if token not in row:
                failures.append(f"task execution control row missing token for {task}: {token}")

    for field in REQUIRED_FIELDS:
        if f"`{field}`" not in board_text:
            failures.append(f"missing task control field: {field}")

    for dependency in REQUIRED_DEPENDENCIES:
        if dependency not in board_text:
            failures.append(f"missing dependency chain: {dependency}")

    for status in REQUIRED_STATUS_TOKENS:
        if f"`{status}`" not in board_text:
            failures.append(f"missing status gate token: {status}")

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in board_text:
            failures.append(f"missing boundary token: {token}")

    for project, tokens in REQUIRED_FULL_BASELINE_TOKENS.items():
        if project not in board_text:
            failures.append(f"missing full baseline project: {project}")
        for token in tokens:
            if token not in board_text:
                failures.append(f"missing full baseline token for {project}: {token}")

    for token in FORBIDDEN_UNBOUNDED_CLAIMS:
        if token in board_text:
            failures.append(f"forbidden unbounded completion claim: {token}")

    if "globalcloud-core-chain-real-evidence-register.md" not in board_text:
        failures.append("board must reference the core-chain evidence register")

    if "GlobalCloud 项目群真实执行治理总控板" not in register_text:
        failures.append("core-chain register must reference the real execution governance board")

    result = {
        "gate": "project_group_real_execution_governance_board",
        "status": "pass" if not failures else "fail",
        "projects_checked": len(REQUIRED_PROJECTS),
        "full_baseline_projects_checked": len(REQUIRED_FULL_BASELINE_TOKENS),
        "tasks_checked": len(REQUIRED_TASKS),
        "dependencies_checked": len(REQUIRED_DEPENDENCIES),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This gate validates the governance board structure and boundary wording; it does not execute project repositories.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
