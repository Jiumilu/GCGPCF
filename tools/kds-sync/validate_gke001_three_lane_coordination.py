#!/usr/bin/env python3
"""Validate the authorized GKE-001 Studio/KDS/Brain coordination envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
ENVELOPE = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-three-lane-coordination-envelope.yaml"
STUDIO_A4 = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-studio-intake-amendment-a4.yaml"
STUDIO_A5 = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-studio-intake-reconciliation-a5.yaml"
STUDIO_A6 = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-studio-intake-rework-amendment-a6.yaml"
MINIMAL_PARALLEL_A7 = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-minimal-parallel-unfreeze-amendment-a7.yaml"
A7_GOVERNANCE_CLEANUP_A8 = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a7-governance-cleanup-rework-amendment-a8.yaml"
A9_READ_ADMISSION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-mmc-read-admission-amendment-a9.yaml"
A9_MMC_ROLLBACK_REWORK = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a9-mmc-rollback-handoff-rework-a9r1.yaml"
A10_READONLY_PREFLIGHT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10-readonly-preflight-a10p0.yaml"
A10P1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10p1-contract-convergence-and-brain-baseline.yaml"
A10P2_CANDIDATE = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-canonical-read-contract-candidate-a10p2.json"
A10P2_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10p2-joint-contract-freeze-report.yaml"
A10P3_SCHEMA = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-canonical-read-openapi-candidate-a10p3.yaml"
A10P3_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10p3-field-schema-and-file-allowlist-freeze.yaml"
A10P3R1_SCHEMA = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-canonical-read-openapi-candidate-a10p3r1.yaml"
A10P3R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10p3r1-field-schema-rework.yaml"
A10P3R1_NORMALIZER = ROOT / "tools/kds-sync/normalize_gke001_release0_read_contract.py"
A10P3R2_SCHEMA = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-canonical-read-openapi-candidate-a10p3r2.yaml"
A10P3R2_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10p3r2-metadata-only-contract-reconciliation.yaml"
A10P3R2_FREEZE = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-canonical-read-contract-freeze-a10p3r2.yaml"
A10P3R2_FREEZE_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p3r2-final-byte-freeze-20260811.md"
A10I1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-first-implementation-amendment-a10i1.yaml"
A10I1_DISPATCH_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i1-first-implementation-dispatch-20260811.md"
A10I1_HANDOFF_REVIEW_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i1-dual-handoffs-and-f013-review-dispatch-20260811.md"
A10I1R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i1-joint-review-rework-a10i1r1.yaml"
A10I1R1_DISPATCH_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i1-independent-review-and-a10i1r1-dispatch-20260811.md"
A10I1R1_CLOSURE_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i1r1-targeted-review-and-serial-gate-closure-20260811.md"
A10I2_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-mmc-standard-implementation-amendment-a10i2.yaml"
A10I2_DISPATCH_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2-mmc-standard-implementation-dispatch-20260811.md"
A10I2_HANDOFF_REVIEW_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2-mmc-handoff-and-f013-review-dispatch-20260811.md"
A10I2R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i2-mmc-targeted-rework-a10i2r1.yaml"
A10I2R1_DISPATCH_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2-independent-review-and-a10i2r1-dispatch-20260811.md"
A10I2R1_HANDOFF_REVIEW_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2r1-handoff-and-f013-targeted-re-review-20260811.md"
A10I2R2_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i2r2-mmc-response-schema-rework.yaml"
A10I2R2_DISPATCH_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2r1-review-and-a10i2r2-dispatch-20260811.md"
A10I2R2_HANDOFF_REVIEW_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2r2-handoff-and-f013-final-review-20260811.md"
A10I2R2_FINAL_CLOSURE_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i2r2-final-review-and-technical-gate-closure-20260811.md"
A10I3P0_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3-mmc-policy-apply-safety-preflight.yaml"
A10I3P0_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3p0-mmc-policy-safety-preflight-and-review-dispatch-20260811.md"
A10I3H1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1-mmc-policy-mutation-hardening.yaml"
A10I3H1_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3p0-review-and-a10i3h1-dispatch-20260811.md"
A10I3H1_HANDOFF_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1-handoff-and-f013-review-dispatch-20260811.md"
A10I3H1R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1r1-mmc-policy-mutation-safety-rework.yaml"
A10I3H1R1_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1-independent-review-and-a10i3h1r1-dispatch-20260811.md"
A10I3H1R1_HANDOFF_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r1-handoff-and-f013-review-dispatch-20260811.md"
A10I3H1R2_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1r2-mmc-shared-registry-state-rework.yaml"
A10I3H1R2_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r1-coordinator-replay-and-a10i3h1r2-dispatch-20260811.md"
A10I3H1R2_RECONCILIATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1r2-mmc-baseline-reconciliation.yaml"
A10I3H1R2_RECONCILIATION_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-mmc-external-baseline-reconciliation-20260811.md"
A10I3H1R2_HANDOFF_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-handoff-and-f013-review-dispatch-20260811.md"
A10I3H1R2R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1r2-coordinator-review-blocker-a10i3h1r2r1.yaml"
A10I3H1R2R1_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-coordinator-readonly-replay-20260812.md"
A10I3H1R2R2_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1r2-secondary-review-scope-correction-a10i3h1r2r2.yaml"
A10I3H1R2R2_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-secondary-review-scope-correction-20260812.md"
A10I3H1R2R3_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-a10i3h1r2-final-scope-correction-a10i3h1r2r3.yaml"
A10I3H1R2R3_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10i3h1r2-final-scope-correction-20260812.md"
BRAIN_A10P1T3_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-brain-a10p1-tranche3-baseline-repair.yaml"
BRAIN_A10P1T3_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-brain-a10p1-tranche3-dispatch-20260812.md"
BRAIN_A10P1T3_CLOSURE_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-brain-a10p1t3-handoff-and-independent-review-closure-20260812.md"
BRAIN_A10P1T4_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-brain-a10p1-tranche4-baseline-repair.yaml"
BRAIN_A10P1T4_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-brain-a10p1-tranche4-dispatch-20260812.md"
BRAIN_A10P1T4R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-brain-a10p1-tranche4-opsx-adapter-amendment.yaml"
BRAIN_A10P1T4_HANDOFF_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-brain-a10p1t4-handoff-and-f013-review-dispatch-20260812.md"
STUDIO_A10I1G1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-studio-postcommit-codegraph-reconciliation-a10i1g1.yaml"
STUDIO_A10I1G1_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-studio-postcommit-codegraph-reconciliation-dispatch-20260812.md"
STUDIO_A10I1G1R1_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-studio-a10i1g1-final-reseal-a10i1g1r1.yaml"
STUDIO_A10I1G1_CLOSURE_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-studio-a10i1g1-handoff-and-independent-review-closure-20260812.md"
KDS_DIRTY_ISOLATION_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-dirty-ownership-isolation-a10i1d1.yaml"
KDS_DIRTY_ISOLATION_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-dirty-ownership-isolation-and-review-dispatch-20260812.md"
KDS_DEPENDENCY_ORDER_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-release0-dependency-order-a10i1d2.yaml"
KDS_DEPENDENCY_ORDER_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-release0-dependency-order-and-review-dispatch-20260812.md"
KDS_STAGEB_DISPOSITION_COORDINATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-owner-disposition-preflight-a10i1d3.yaml"
KDS_STAGEB_DISPOSITION_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-owner-disposition-preflight-and-dispatch-20260812.md"
KDS_STAGEB_AUTHORIZATION_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-owner-disposition-authorization-request-a10i1d4.yaml"
KDS_STAGEB_AUTHORIZATION_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-owner-disposition-authorization-request-and-review-20260812.md"
KDS_STAGEB_CORE_AUTHORIZATION_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-core-authorization-request-a10i1d4r1.yaml"
KDS_STAGEB_CORE_AUTHORIZATION_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-core-authorization-request-and-review-20260812.md"
KDS_STAGEB_CORE_BASELINE_RECONCILIATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-core-baseline-reconciliation-a10i1d4r1b1.yaml"
KDS_STAGEB_CORE_BASELINE_RECONCILIATION_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-core-baseline-reconciliation-and-review-20260812.md"
KDS_STAGEB_CORE_DIFFFIX_REWORK = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-core-diffcheck-rework-a10i1d4r2.yaml"
KDS_STAGEB_CORE_DIFFFIX_REWORK_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-core-diffcheck-abort-and-r2-review-20260812.md"
KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-core-diffcheck-rework-authorization-a10i1d4r2a1.yaml"
KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-core-local-commit-receipt-a10i1d4r2a2.yaml"
KDS_STAGEB_REGRESSION_PREFLIGHT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-regression-preflight-a10i1d4r3.yaml"
KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-regression-preflight-receipt-a10i1d4r3r1.yaml"
KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-regression-local-commit-authorization-request-a10i1d4r4.yaml"
KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-regression-local-commit-authorization-a10i1d4r4a1.yaml"
KDS_STAGEB_REGRESSION_COMMIT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-regression-local-commit-receipt-a10i1d4r4a2.yaml"
KDS_STAGEB_OPENSPEC_PREFLIGHT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-openspec-preflight-a10i1d4r5.yaml"
KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-openspec-preflight-receipt-a10i1d4r5r1.yaml"
KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-openspec-local-commit-authorization-request-a10i1d4r6.yaml"
KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-openspec-local-commit-authorization-a10i1d4r6a1.yaml"
KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-openspec-local-commit-receipt-a10i1d4r6a2.yaml"
KDS_STAGEB_RUN_HANDOFF_PREFLIGHT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-preflight-a10i1d4r7.yaml"
KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-preflight-receipt-a10i1d4r7r1.yaml"
KDS_STAGEB_RUN_HANDOFF_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-run-handoff-preflight-20260812.md"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-eof-rework-authorization-request-a10i1d4r8.yaml"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-eof-rework-hash-hardening-a10i1d4r8r1.yaml"
KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-eof-baseline-reconciliation-a10i1d4r8b1.yaml"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-eof-rework-execution-a10i1d4r8a1.yaml"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-eof-rework-receipt-a10i1d4r8a2.yaml"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-run-handoff-eof-rework-and-review-20260813.md"
KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-local-commit-authorization-request-a10i1d4r9.yaml"
KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-run-handoff-local-commit-authorization-request-20260813.md"
KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-local-commit-authorization-a10i1d4r9a1.yaml"
KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-run-handoff-local-commit-receipt-a10i1d4r9a2.yaml"
KDS_STAGEB_RUN_HANDOFF_COMMIT_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-run-handoff-local-commit-and-review-20260813.md"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-four-commit-push-preflight-a10i1d4r10.yaml"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-four-commit-push-preflight-receipt-a10i1d4r10r1.yaml"
KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-four-commit-push-authorization-request-a10i1d4r11.yaml"
KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-four-commit-push-authorization-a10i1d4r11a1.yaml"
KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-stageb-four-commit-push-receipt-a10i1d4r11a2.yaml"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_EVIDENCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-kds-stageb-four-commit-push-preflight-and-authorization-request-20260813.md"
RELEASE0_CURRENT_STATE_REVALIDATION = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-current-state-readonly-revalidation-a10c12.yaml"
RELEASE0_CURRENT_STATE_HANDOFF = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-current-state-readonly-handoff-a10c12r1.yaml"
RELEASE0_CURRENT_STATE_REVIEW_CLOSURE = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-current-state-independent-review-closure-a10c12r2.yaml"
KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-release0-product-test-local-commit-request-a10c13.yaml"
LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-localization-feature-evidence-boundary-repair-a10c14.yaml"
KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-kds-release0-product-test-commit-readiness-replay-a10c15.yaml"
MMC_RELEASE0_POLICY_FRESHNESS_REPLAY = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-mmc-release0-policy-freshness-replay-a10c16.yaml"
RELEASE0_CONSUMER_FRESHNESS_REPLAY = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-release0-consumer-freshness-replay-a10c17.yaml"
STUDIO_A6_REVIEW = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/studio-a6-independent-review-20260810.md"
EMERGENCY_AUDIT = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-emergency-blocker-audit-20260811.md"
A7_REVIEW_A8_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a7-independent-review-and-a8-dispatch-20260811.md"
A8_ACCEPTANCE_A9_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a8-independent-acceptance-and-a9-dispatch-20260811.md"
A9_REVIEW_A9R1_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a9-independent-review-and-a9r1-dispatch-20260811.md"
A9R1_ACCEPTANCE = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a9r1-independent-acceptance-20260811.md"
A10P0_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p0-preflight-dispatch-20260811.md"
A10P0_HANDOFFS = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p0-three-handoffs-and-f013-dispatch-20260811.md"
A10P0_REVIEW_A10P1_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p0-independent-review-and-a10p1-dispatch-20260811.md"
A10P1_HANDOFFS = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p1-three-handoffs-and-f013-dispatch-20260811.md"
A10P1_REVIEW_A10P2_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p1-independent-review-and-a10p2-dispatch-20260811.md"
A10P2_HANDOFFS = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p2-two-reports-and-f013-freeze-review-dispatch-20260811.md"
A10P2_REVIEW_A10P3_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p2-independent-review-and-a10p3-dispatch-20260811.md"
A10P3_REPORTS_A10P3R1_DISPATCH = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p3-two-reports-and-a10p3r1-dispatch-20260811.md"
A10P3R1_HANDOFFS = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/gke-001-a10p3r1-two-reports-and-f013-freeze-review-dispatch-20260811.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
SESSION_REGISTRY = ROOT / "02-governance/loop/LOOP_SESSION_REGISTRY.md"
PREVIOUS_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-003.md"
A7_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-004.md"
LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-005.md"
A9_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-006.md"
A9R1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-007.md"
A9_ACCEPTANCE_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-008.md"
A10P0_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-009.md"
A10P1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-010.md"
A10P2_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-011.md"
A10P2_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-012.md"
A10P3_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-013.md"
A10P3R1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-014.md"
A10P3R1_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-015.md"
A10P3R2_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-016.md"
A10P3R2_FREEZE_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-017.md"
A10I1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-018.md"
A10I1_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-019.md"
A10I1R1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-020.md"
A10I1R1_CLOSURE_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-021.md"
A10I2_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-022.md"
A10I2_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-023.md"
A10I2R1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-024.md"
A10I2R1_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-025.md"
A10I2R2_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-026.md"
A10I2R2_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-027.md"
A10I2R2_CLOSURE_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-028.md"
A10I3P0_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-029.md"
A10I3H1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-030.md"
A10I3H1_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-031.md"
A10I3H1R1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-032.md"
A10I3H1R1_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-033.md"
A10I3H1R2_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-034.md"
A10I3H1R2_RECONCILIATION_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-035.md"
A10I3H1R2_HANDOFF_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-036.md"
A10I3H1R2R1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-037.md"
BRAIN_A10P1T3_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-038.md"
A10I3H1R2R2_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-039.md"
STUDIO_A10I1G1_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-040.md"
BRAIN_A10P1T4_LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-041.md"
FEATURE = ROOT / "features/active/F-013-knowledge-asset-model-system/feature.yaml"
SUMMARY = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/summary.md"

COORDINATION_ID = "GKE-001-COORDINATION-20260803-001"
COORDINATOR_THREAD = "019f0697-c8ce-7110-8ac8-9a7dbc6ba2a5"
ENVELOPE_SHA256 = "e95307a21c4197798d692a7efe18be22f7d305c145942ce47a1afc24f06ceeff"
STUDIO_A4_ID = "GKE-001-COORDINATION-20260803-001-A4"
STUDIO_A4_SHA256 = "c1c7963b0f66e5c66d471817c0f25219fe1653182362c5b4b3fe01010bfc6f3a"
STUDIO_A5_ID = "GKE-001-COORDINATION-20260810-001-A5"
STUDIO_A5_SHA256 = "8709a81b994eac6b91216d11cffb0e70115e450c776ac1081e5ac7972160a344"
STUDIO_A6_ID = "GKE-001-COORDINATION-20260810-002-A6"
STUDIO_A6_SHA256 = "bba9f2f33a1c43066df551ba8b086bcaa5f3c2d655b2ca6af831aefb40ee8f3c"
MINIMAL_PARALLEL_A7_ID = "GKE-001-COORDINATION-20260811-001-A7"
MINIMAL_PARALLEL_A7_SHA256 = "04e27fd23e1a3fd32a10bd85aa4f387af56668d938c44943f575340d3b8f8668"
A7_GOVERNANCE_CLEANUP_A8_ID = "GKE-001-COORDINATION-20260811-002-A8"
A7_GOVERNANCE_CLEANUP_A8_SHA256 = "1e8fcdd04dade89a76a27647189a374d70d67267ff19817a6d5e7ff6cce30a89"
A9_READ_ADMISSION_ID = "GKE-001-COORDINATION-20260811-003-A9"
A9_READ_ADMISSION_SHA256 = "a3918471b8cde1eeb965c3ff5120be99944ee8fd24d0ffe1e87fe3b724435fc7"
A9_MMC_ROLLBACK_REWORK_ID = "GKE-001-COORDINATION-20260811-004-A9R1"
A9_MMC_ROLLBACK_REWORK_SHA256 = "05bfb1c3cfae04b1f253afce5cb347fdd9306af606faade2129f1499b59f22f6"
A10_READONLY_PREFLIGHT_ID = "GKE-001-COORDINATION-20260811-005-A10P0"
A10_READONLY_PREFLIGHT_SHA256 = "b9d4acdef872289afd5a2194a1430daf977bab028f9fc76ce6e937f39e8ecc96"
A10P1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-006-A10P1"
A10P1_COORDINATION_SHA256 = "264a50bb1020a97777761371fb331f6a6c05e6ed3698875d27107b0c79bfd1bb"
A10P2_CANDIDATE_SHA256 = "11e15a3448279c7ddcdc97ea25b80cfefbef17a332c08cd20f41efc97a6667f8"
A10P2_COORDINATION_ID = "GKE-001-COORDINATION-20260811-007-A10P2"
A10P2_COORDINATION_SHA256 = "e2a0cb491bcb626bb29507be5e51612e4cb26ddf1427b94e70f7bd3f1b7f249e"
A10P3_SCHEMA_SHA256 = "48dfcb0967a894ee2bd760311d7f84023054b0bcc2bc578292d826e73fbc7c18"
A10P3_SCHEMA_CANONICAL_SHA256 = "19d58977c044bd6e6942a79964cdeb28e7bc1b6affccdd46427537ea32bc60f9"
A10P3_OPERATION_MATRIX_SHA256 = "2a80d362fe0d25d078874f919b911150122ca4f3c2faa3d9a25401f6e792a65c"
A10P3_COORDINATION_ID = "GKE-001-COORDINATION-20260811-008-A10P3"
A10P3_COORDINATION_SHA256 = "9a3fe20c87d269263e442b5a6899f6f75581319adc7a8800a27e0669abcd22e4"
A10P3R1_SCHEMA_SHA256 = "74b51affabf79d2ba4a908d2d9397671bdd0b07bc80814a0c36dd8d83faa7e14"
A10P3R1_SCHEMA_CANONICAL_SHA256 = "766ca647e894c09520bcb8ce0e70386aa233bcf727fcaf140e521f6127b1a09b"
A10P3R1_NORMALIZER_SHA256 = "d820e8103b2af74aab06381fe4034c9cec525acc8c7e1efdb074bd8a4a3aa4e4"
A10P3R1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-009-A10P3R1"
A10P3R1_COORDINATION_SHA256 = "c8b76dcde4ffdee835fe426edbd44c33c975b6bcbd25dd60ad0dd827134f6060"
A10P3R2_SCHEMA_SHA256 = "cc5865ac5f76e82d7ea86891f020e196073a0a23cd5a4f6bb44a3a279b0b0de0"
A10P3R2_SCHEMA_CANONICAL_SHA256 = "a6fe1197ab9bfae4a1919c903b296b13a52f7db9d276212aaabd48ae854a2d37"
A10P3R2_COORDINATION_ID = "GKE-001-COORDINATION-20260811-010-A10P3R2"
A10P3R2_COORDINATION_SHA256 = "d4b21c2ccfbc9d2878ce5c020c232f26c53b704b51313a92da6d8345748b12bc"
A10P3R2_FREEZE_ID = "GKE-001-CONTRACT-FREEZE-20260811-001"
A10P3R2_FREEZE_SHA256 = "a7dbdcf6a64a4f9b6c6cd11e4ae2fe02405624b29e4ad009a317510de557a23f"
MMC_CANDIDATE_FINGERPRINT = "3cab2c7eef531c13bc0af32af61836f3947aa23ac8b2461f84a05f47378dbaf2"
MMC_RESTORE_FINGERPRINT = "40a674577b73422c98936a69efd1b3a317d1999d5a44dfd0b4635842067c0a5e"
A10I1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-011-A10I1"
A10I1_COORDINATION_SHA256 = "8f4087ca09a4695a0cdec021d0d22270c4866ec9903dc86c0c8cbff8069d37c3"
A10I1R1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-012-A10I1R1"
A10I1R1_COORDINATION_SHA256 = "4c4a164e7e30186789d4f518ffeede6465dab28e10cc0206bb3c151b16958e7e"
A10I2_COORDINATION_ID = "GKE-001-COORDINATION-20260811-013-A10I2"
A10I2_COORDINATION_SHA256 = "8ab2dd88b45c33669a4d3a14dc8065765738e113ff1728965b1defaa3776aacf"
A10I2R1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-014-A10I2R1"
A10I2R1_COORDINATION_SHA256 = "ef4065c374f5f2be480c170b3a4e60bef54a72b0d8ee40c3bd3c7fb5e12cbd2e"
A10I2R2_COORDINATION_ID = "GKE-001-COORDINATION-20260811-015-A10I2R2"
A10I2R2_COORDINATION_SHA256 = "bae892222772f306c41999631a5d1bf27cc9ea17f79e88cc42c1e9163a6b2d11"
A10I3P0_COORDINATION_ID = "GKE-001-COORDINATION-20260811-016-A10I3P0"
A10I3P0_COORDINATION_SHA256 = "4a7de8561f2882940caea5b9ed55a790e53f9c44ea5cfb3c359e5ff9791b73df"
A10I3H1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-017-A10I3H1"
A10I3H1_COORDINATION_SHA256 = "a3fc12a42b47e23d39a867719bcde0da10ec452751378d5a0128f38bb54cdbff"
A10I3H1R1_COORDINATION_ID = "GKE-001-COORDINATION-20260811-018-A10I3H1R1"
A10I3H1R1_COORDINATION_SHA256 = "8a5470cfa1adfdab1ff18307aad3739bc3af6fbd32b10c3353ff8e8545875850"
A10I3H1R2_COORDINATION_ID = "GKE-001-COORDINATION-20260811-019-A10I3H1R2"
A10I3H1R2_COORDINATION_SHA256 = "880980dbd38462c58fa8da34ea67fca593c3e2bae2958e3410a6a74b1222c731"
A10I3H1R2_RECONCILIATION_ID = "GKE-001-COORDINATION-20260811-020-A10I3H1R2R0"
A10I3H1R2_RECONCILIATION_SHA256 = "a40e54f14ff5bd1e7b9474097e466f6ac0f6dea854ac3c35f0c34f59d4e62152"
A10I3H1R2_RECONCILED_BASELINE = "b06f58a78ac7713197deed47d1125bec7a260e8c"
A10I3H1R2R1_COORDINATION_ID = "GKE-001-COORDINATION-20260812-001-A10I3H1R2R1"
A10I3H1R2R1_COORDINATION_SHA256 = "3699642fde266e74a797d1515abd9d791da0526b7eef8c278f7cc2e098a35a3f"
BRAIN_A10P1T3_COORDINATION_ID = "GKE-001-COORDINATION-20260812-002-A10P1T3"
BRAIN_A10P1T3_COORDINATION_SHA256 = "d96472aee1af90b94ac0f5f24ca06f5d4dc07d83ee0ff44d5fd03f74879a03ad"
BRAIN_A10P1T4_COORDINATION_ID = "GKE-001-COORDINATION-20260812-008-A10P1T4"
BRAIN_A10P1T4_COORDINATION_SHA256 = "25349bb558c0ef8fed5233d080c20356789c4a89bfdf5ebd09ca07d2eab9322f"
BRAIN_A10P1T4R1_COORDINATION_ID = "GKE-001-COORDINATION-20260812-009-A10P1T4R1"
BRAIN_A10P1T4R1_COORDINATION_SHA256 = "d3a7dced8b559ff4d2cc543f7c04e5524af2902563cf6423496ce157f9a37e8c"
A10I3H1R2R2_COORDINATION_ID = "GKE-001-COORDINATION-20260812-003-A10I3H1R2R2"
A10I3H1R2R2_COORDINATION_SHA256 = "588691af5c5866a481fcc46886df0e9c3cd200a191bcca89295397f7cd0838c3"
STUDIO_A10I1G1_COORDINATION_ID = "GKE-001-COORDINATION-20260812-004-A10I1G1"
STUDIO_A10I1G1_COORDINATION_SHA256 = "f6f3ceeacda0fd8d6f969c164d9e9c481ddb87b8be0788c357f2b2734b79b8b9"
A10I3H1R2R3_COORDINATION_ID = "GKE-001-COORDINATION-20260812-006-A10I3H1R2R3"
A10I3H1R2R3_COORDINATION_SHA256 = "06a34a9b05078fe26897c15070315e919886b132e02c8006fcf50fce8f32e0ff"
STUDIO_A10I1G1R1_COORDINATION_ID = "GKE-001-COORDINATION-20260812-007-A10I1G1R1"
STUDIO_A10I1G1R1_COORDINATION_SHA256 = "2b228d7a89771c117b2fb91607e8f32f65cca4e079a644c58f43b5f129ffcd1b"
KDS_DIRTY_ISOLATION_COORDINATION_ID = "GKE-001-COORDINATION-20260812-010-A10I1D1"
KDS_DIRTY_ISOLATION_COORDINATION_SHA256 = "d14ef30b401284c833e16bc1f1add845fba7e34cb2f31a29cf85c52e6eec2840"
KDS_DEPENDENCY_ORDER_COORDINATION_ID = "GKE-001-COORDINATION-20260812-011-A10I1D2"
KDS_DEPENDENCY_ORDER_COORDINATION_SHA256 = "a226a75e1d839678b79ea941def964b69e0e2876b7c49510b256882017ac6e5d"
KDS_STAGEB_DISPOSITION_COORDINATION_ID = "GKE-001-COORDINATION-20260812-012-A10I1D3"
KDS_STAGEB_DISPOSITION_COORDINATION_SHA256 = "44952b52497325a936deb68a6a2a986f4d6d287805818b8a8fce4cd5f5a13142"
KDS_STAGEB_AUTHORIZATION_REQUEST_ID = "GKE-001-COORDINATION-20260812-013-A10I1D4"
KDS_STAGEB_AUTHORIZATION_REQUEST_SHA256 = "01685904e46c63e3997f6080716f8bb5ddddfe6ebe7588641870c905f9b23f76"
KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_ID = "GKE-001-COORDINATION-20260812-014-A10I1D4R1"
KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_SHA256 = "d9dbe8ba24518beec10d4e5eefbcfddebeb22669d4195b084ae150ba6a433b3a"
KDS_STAGEB_CORE_BASELINE_RECONCILIATION_ID = "GKE-001-COORDINATION-20260812-015-A10I1D4R1B1"
KDS_STAGEB_CORE_BASELINE_RECONCILIATION_SHA256 = "989e77472642fdc7000799243bb5b68fd79e736c6b7bbb3e5e33ddd9dbe6e4e7"
KDS_STAGEB_CORE_DIFFFIX_REWORK_ID = "GKE-001-COORDINATION-20260812-016-A10I1D4R2"
KDS_STAGEB_CORE_DIFFFIX_REWORK_SHA256 = "6f89ede57b739d374dd44b26bb2fad60a36b60e77333781d4cb2125382b6d7db"
KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_ID = "GKE-001-COORDINATION-20260812-017-A10I1D4R2A1"
KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_SHA256 = "c3bc86e0ae4aea6b2920d49daaf403bbec64cace11f3d8e93d2a615b5c659237"
KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_ID = "GKE-001-COORDINATION-20260812-018-A10I1D4R2A2"
KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_SHA256 = "0921e27a7d3066e7c9a5691c4bd63b18211f7fceb20e083cc924a265631a11bb"
KDS_STAGEB_REGRESSION_PREFLIGHT_ID = "GKE-001-COORDINATION-20260812-019-A10I1D4R3"
KDS_STAGEB_REGRESSION_PREFLIGHT_SHA256 = "22c50de2ea3e5fbe2ed1d2a1e35efda1c44cdeb507abfb76abc1843db2f47d99"
KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_ID = "GKE-001-COORDINATION-20260812-020-A10I1D4R3R1"
KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_SHA256 = "d8a746f5cf323211f94846193d92fe32ea7ac4293faede1b3f0b1caec031278d"
KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_ID = "GKE-001-COORDINATION-20260812-021-A10I1D4R4"
KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_SHA256 = "7107019c08ba37a61b0531f0dd6102d0b26dd16248365b9499c9b0e69174366e"
KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_ID = "GKE-001-COORDINATION-20260812-022-A10I1D4R4A1"
KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_SHA256 = "859e6eac3a4a792f6977d3dba87a3810439354410517704af9f88450ce2935a7"
KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_ID = "GKE-001-COORDINATION-20260812-023-A10I1D4R4A2"
KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_SHA256 = "7973115f76b2cf671b2a68fceec3a7559096a3e26d531101082a64db8472a8e7"
KDS_STAGEB_OPENSPEC_PREFLIGHT_ID = "GKE-001-COORDINATION-20260812-024-A10I1D4R5"
KDS_STAGEB_OPENSPEC_PREFLIGHT_SHA256 = "829f1a2eda39c89eefcb2374da62483e8294b27470feeb223532d1a42c6a2a4a"
KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_ID = "GKE-001-COORDINATION-20260812-025-A10I1D4R5R1"
KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_SHA256 = "5a96e5548c8ba05a3f598f85c480a2b763e2bf6af11e798957eac1be4c269492"
KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_ID = "GKE-001-COORDINATION-20260812-026-A10I1D4R6"
KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_SHA256 = "6695349d631cf1084486456dd47e95d6f2f0f20381548757d1c163cfdff7b021"
KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_ID = "GKE-001-COORDINATION-20260812-027-A10I1D4R6A1"
KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_SHA256 = "9f518d538a6471337fcfd390091baf14aecae39a20b0f852b8a6890bc9a20a0b"
KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_ID = "GKE-001-COORDINATION-20260812-028-A10I1D4R6A2"
KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_SHA256 = "54b4bced82937fba41fa890d36a5b12c9342ffa0445483fed1dfe7bccc136fb1"
KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_ID = "GKE-001-COORDINATION-20260812-029-A10I1D4R7"
KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_SHA256 = "d04069ae437b0a2defcbad81b8f5c6feb3760c207675a44f8baac187dd9ea02d"
KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_ID = "GKE-001-COORDINATION-20260812-030-A10I1D4R7R1"
KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_SHA256 = "88c7b131aef332f6004ece1c1191932f0e93bbc05dab0e1f0674786dd80f0440"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST_ID = "GKE-001-COORDINATION-20260812-031-A10I1D4R8"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST_SHA256 = "46f65f9216a983cb559be87ca4779ca1b1d99d1ebeec34dbc13e3310b2bd3725"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING_ID = "GKE-001-COORDINATION-20260812-032-A10I1D4R8R1"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING_SHA256 = "68a680653e44f0701c8cfb7811ab06f82a2fcd6b16b6138e06e27f43909ed63a"
KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_ID = "GKE-001-COORDINATION-20260813-033-A10I1D4R8B1"
KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_SHA256 = "41ea87a447d40b17fae124cff74cbc1198882e89112e81b7178abc098118bbd6"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_ID = "GKE-001-COORDINATION-20260813-034-A10I1D4R8A1"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_SHA256 = "7ea77e17fc0a72b433bc244903efcc633ddd992e7ff7823b50dbff3909f2f999"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_ID = "GKE-001-COORDINATION-20260813-035-A10I1D4R8A2"
KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_SHA256 = "8f1aaa99ed58c4c26b79c53b5cac50c7a1f4fda9475a47ac9e58253c0a48038a"
KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_ID = "GKE-001-COORDINATION-20260813-036-A10I1D4R9"
KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_SHA256 = "f55627928263a30b0c29536778d71ffd428ee657e9109395ca770c15691752d8"
KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION_ID = "GKE-001-COORDINATION-20260813-037-A10I1D4R9A1"
KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION_SHA256 = "39c17b96c6ef9834bed15a8876a7734a253c37ede86733781cb5e33b7da42419"
KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT_ID = "GKE-001-COORDINATION-20260813-038-A10I1D4R9A2"
KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT_SHA256 = "18d976e696cb30f8ba88da02a3bccb13f370763eabb850e36fe358f50d1abfe5"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_ID = "GKE-001-COORDINATION-20260813-039-A10I1D4R10"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_SHA256 = "6e25314b88b07cc6ca1bfc4bf589bfd574c0d9d9c4bc47c7cb4479ea9eeb05d8"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_ID = "GKE-001-COORDINATION-20260813-040-A10I1D4R10R1"
KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_SHA256 = "bb5f388526767b23bb66efbeec1aa0222576a2654b1ec17486c92df25c2d191d"
KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_ID = "GKE-001-COORDINATION-20260813-041-A10I1D4R11"
KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_SHA256 = "3d292b13ca6910524dd3d30f0cc5088f6713dbc4befac0f7c78e65698886d47d"
KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_ID = "GKE-001-COORDINATION-20260813-042-A10I1D4R11A1"
KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_SHA256 = "29c54680a9c78dbc63e0abb9b3502482e1b50d119bc4250f12b5128d8f2d0abc"
KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_ID = "GKE-001-COORDINATION-20260813-043-A10I1D4R11A2"
KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_SHA256 = "5e2e604af4e26d7a6c6eedf7160c4da362387c0dcb1cd6beaa0e987a8fb67035"
RELEASE0_CURRENT_STATE_REVALIDATION_ID = "GKE-001-COORDINATION-20260813-076-A10C12"
RELEASE0_CURRENT_STATE_REVALIDATION_SHA256 = "ac4c218ea1335b0275196d92af4ea66c62560cf9c53d96615ea0c079f844445c"
RELEASE0_CURRENT_STATE_HANDOFF_ID = "GKE-001-COORDINATION-20260813-077-A10C12R1"
RELEASE0_CURRENT_STATE_HANDOFF_SHA256 = "9ff607e7c56cf0aa9349d6e2f13112cd1ea18e3fb5a153cf035ae204c01f8b98"
RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_ID = "GKE-001-COORDINATION-20260813-078-A10C12R2"
RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_SHA256 = "5fef27d8c380a0eb48d76f0e70e09108172c432dc7861442097a6d9a6f4c9fb1"
KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_ID = "GKE-001-COORDINATION-20260813-079-A10C13"
KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_SHA256 = "88a6c2b201c9e3e949f955908831920fea89adf301ac0a380b559df6deb56001"
LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_ID = "GKE-001-COORDINATION-20260813-080-A10C14"
LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_SHA256 = "dbf69478fcb1e2e9b789141305084f30be54ccf6ebb1a4d3bf218b74b4030dca"
KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_ID = "GKE-001-COORDINATION-20260813-081-A10C15"
KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_SHA256 = "510e490f2ec5cebb6c236c017c9c94e490043999ca46082a90e69e84d593b224"
MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_ID = "GKE-001-COORDINATION-20260813-082-A10C16"
MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_SHA256 = "5b43ecdd0ab7b7df6a9919bf283880cd344cfb4f6cf8ac8d8031043ed03d8ac4"
RELEASE0_CONSUMER_FRESHNESS_REPLAY_ID = "GKE-001-COORDINATION-20260813-083-A10C17"
RELEASE0_CONSUMER_FRESHNESS_REPLAY_SHA256 = "faac8e0e5840b3abcbc702d16e7dca5d71e50ba20381f1dcfe66a6ad9490dbd3"
LANE_THREADS = {
    "studio": "019ee242-2575-73f1-b5bb-d43e7e49468e",
    "kds": "019fc4e3-bce5-7541-85e3-8885c7e78aea",
    "brain": "019edfb4-21ef-77e1-afdb-891df25c4068",
}
LANE_CHANGES = {
    "studio": "restore-studio-backend-runtime",
    "kds": "extend-kds-document-extraction",
    "brain": "brain-studio-readonly-kds-bridge",
}


def fail(message: str) -> None:
    print(f"gke001_three_lane_coordination=fail reason={message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    envelope_text = read(ENVELOPE)
    envelope_sha = hashlib.sha256(envelope_text.encode("utf-8")).hexdigest()
    require(envelope_sha == ENVELOPE_SHA256, f"envelope_sha_mismatch:{envelope_sha}")
    data = yaml.safe_load(envelope_text).get("coordination_envelope", {})
    require(data.get("id") == COORDINATION_ID, "coordination_id_mismatch")
    require(data.get("engineering_domain") == "GKE-001", "engineering_domain_mismatch")
    require(data.get("canonical_feature") == "F-013", "canonical_feature_mismatch")
    require(data.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "coordinator_thread_mismatch")
    require(data.get("coordinator", {}).get("role") == "sole_gke001_coordinator", "coordinator_role_mismatch")
    require(data.get("status", {}).get("completion") == "not_complete", "completion_boundary_mismatch")
    require(data.get("status", {}).get("status_ceiling") == "partial", "status_ceiling_mismatch")

    lanes = data.get("lanes", {})
    require(set(lanes) == set(LANE_THREADS), "lane_set_mismatch")
    require(len({lane.get("thread_id") for lane in lanes.values()}) == 3, "duplicate_lane_thread")
    require(len({lane.get("repository") for lane in lanes.values()}) == 3, "duplicate_lane_repository")
    require(len({lane.get("coordination_lock_id") for lane in lanes.values()}) == 3, "duplicate_lane_lock")
    for lane_name, thread_id in LANE_THREADS.items():
        lane = lanes[lane_name]
        require(lane.get("thread_id") == thread_id, f"thread_mismatch:{lane_name}")
        require(lane.get("change_id") == LANE_CHANGES[lane_name], f"change_mismatch:{lane_name}")
        require(bool(lane.get("file_allowlist")), f"empty_allowlist:{lane_name}")
        require(bool(lane.get("forbidden_scope")), f"empty_forbidden_scope:{lane_name}")
        require(set(lane.get("file_allowlist", ())).isdisjoint(lane.get("forbidden_scope", ())), f"scope_overlap:{lane_name}")

    kds = lanes["kds"]
    for excluded in ("_registries/global-object-registry.yaml", "entities/green-supply-chain-role-view-entity.md"):
        require(excluded in kds.get("forbidden_scope", ()), f"kds_external_file_not_forbidden:{excluded}")
        require(excluded not in kds.get("file_allowlist", ()), f"kds_external_file_in_allowlist:{excluded}")
    for regression_test in ("tests/test_knowledge_intake_api.py", "tests/test_knowledge_intake_postgres.py"):
        require(regression_test in kds.get("file_allowlist", ()), f"kds_regression_test_not_allowed:{regression_test}")
    require(lanes["brain"].get("execution_mode") == "freeze_and_wait", "brain_not_frozen")
    studio = lanes["studio"]
    require(".harness/opsx.lock" in studio.get("file_allowlist", ()), "studio_ephemeral_lock_not_allowed")
    require("docs/harness/loops/loop-round-GPCF-STUDIO-LR-872.md" in studio.get("file_allowlist", ()), "studio_lr872_not_allowed")
    require(studio.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "studio_lock_handling_mismatch")
    amendments = {item.get("id"): item for item in data.get("scope_amendments", [])}
    require("GKE-001-COORDINATION-20260803-001-A1" in amendments, "studio_amendment_missing")
    require("GKE-001-COORDINATION-20260803-001-A2" in amendments, "kds_amendment_missing")
    require("GKE-001-COORDINATION-20260803-001-A3" in amendments, "kds_review_amendment_missing")
    require(".harness/opsx.lock" in kds.get("file_allowlist", ()), "kds_ephemeral_lock_not_allowed")
    require(kds.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "kds_lock_handling_mismatch")
    require(set(lanes["brain"].get("allowed_kds_operations", ())) == {"search", "graph", "page-content"}, "brain_operation_scope_mismatch")
    require(data.get("serial_order") == [
        "kds_stage_b_implementation_and_tests",
        "f013_independent_readonly_review",
        "studio_intake_evidence_review_task_integration",
        "brain_search_wikipreview_chat_readonly_e2e",
        "mmc_delegation_and_human_confirmation_validation",
    ], "serial_order_mismatch")

    required_handoff = set(data.get("handoff_requirements", {}).get("required", ()))
    expected_handoff = {
        "exact_changed_files", "tests", "acl_read", "acl_count", "audit", "lineage",
        "mirror_sha256", "migration_dry_run", "rollback", "authorization_status", "unresolved_risks",
    }
    require(required_handoff == expected_handoff, "handoff_requirement_mismatch")
    authorization = data.get("authorization", {})
    require(authorization.get("kds_stage_b_local_development") is True, "kds_stage_b_dev_not_authorized")
    for key in ("real_kds_write", "long_term_memory_write", "relationship_confirmation", "business_state_change", "commit", "push", "deployment", "status_promotion", "human_confirmation_completed"):
        require(authorization.get(key) is False, f"authorization_boundary_drift:{key}")
    require(data.get("gckf_boundary", {}).get("satisfied_resume_triggers") == 0, "gckf_resume_trigger_drift")
    require(data.get("gckf_boundary", {}).get("creates_d191") is False, "unexpected_d191")

    studio_a4_text = read(STUDIO_A4)
    studio_a4_sha = hashlib.sha256(studio_a4_text.encode("utf-8")).hexdigest()
    require(studio_a4_sha == STUDIO_A4_SHA256, f"studio_a4_sha_mismatch:{studio_a4_sha}")
    studio_a4 = yaml.safe_load(studio_a4_text).get("studio_intake_amendment", {})
    require(studio_a4.get("id") == STUDIO_A4_ID, "studio_a4_id_mismatch")
    require(studio_a4.get("parent_envelope", {}).get("sha256") == ENVELOPE_SHA256, "studio_a4_parent_sha_mismatch")
    require(studio_a4.get("lane", {}).get("thread_id") == LANE_THREADS["studio"], "studio_a4_thread_mismatch")
    require(studio_a4.get("lane", {}).get("change_id") == "integrate-studio-kds-knowledge-intake", "studio_a4_change_mismatch")
    require(studio_a4.get("canonical_contract", {}).get("revision") == "v0.1", "studio_a4_contract_revision_mismatch")
    require(studio_a4.get("canonical_contract", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "studio_a4_manifest_sha_mismatch")
    require(studio_a4.get("status", {}).get("phase_1") == "authorized_local_tdd_contract_and_ui", "studio_a4_phase1_not_authorized")
    require(studio_a4.get("status", {}).get("phase_2") == "blocked_by_mmc_prepare_retry_delegated_operation_review", "studio_a4_phase2_boundary_mismatch")
    require(studio_a4.get("authorization", {}).get("phase_1_local_product_edits") is True, "studio_a4_product_edits_not_authorized")
    for key in ("phase_2_disposable_kds_write", "shared_or_persistent_kds_write", "real_business_asset", "relationship_confirmation", "long_term_memory_write", "business_state_change", "commit", "push", "deployment", "status_promotion"):
        require(studio_a4.get("authorization", {}).get(key) is False, f"studio_a4_authorization_drift:{key}")
    studio_a4_allowlist = set(studio_a4.get("file_allowlist", ()))
    for required_path in (
        ".harness/opsx.lock",
        "packages/server/src/routes/governance/knowledge-intake.ts",
        "packages/client/src/components/studio/ProjectKnowledgeIntakePanel.vue",
        "openspec/changes/integrate-studio-kds-knowledge-intake/**",
        "docs/harness/loops/loop-round-GPCF-STUDIO-LR-873.md",
    ):
        require(required_path in studio_a4_allowlist, f"studio_a4_allowlist_missing:{required_path}")
    require(studio_a4.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "studio_a4_lock_handling_mismatch")
    endpoint_admission = {
        item.get("path"): item.get("mmc_admission")
        for item in studio_a4.get("canonical_contract", {}).get("endpoints", {}).get("stage_a_write", ())
    }
    require(endpoint_admission.get("/api/v1/knowledge-assets/intake") == "blocked_not_seeded", "studio_a4_prepare_admission_drift")
    require(endpoint_admission.get("/api/v1/knowledge-assets/{asset_id}/retry") == "blocked_not_seeded", "studio_a4_retry_admission_drift")
    require(studio_a4.get("audit_sources", {}).get("KDS", "").startswith("authoritative_for_"), "studio_a4_kds_audit_authority_missing")

    studio_a5_text = read(STUDIO_A5)
    studio_a5_sha = hashlib.sha256(studio_a5_text.encode("utf-8")).hexdigest()
    require(studio_a5_sha == STUDIO_A5_SHA256, f"studio_a5_sha_mismatch:{studio_a5_sha}")
    studio_a5 = yaml.safe_load(studio_a5_text).get("studio_intake_reconciliation", {})
    require(studio_a5.get("id") == STUDIO_A5_ID, "studio_a5_id_mismatch")
    require(studio_a5.get("type") == "post_state_reconciliation_without_retroactive_authorization", "studio_a5_type_mismatch")
    require(studio_a5.get("parent_amendment", {}).get("sha256") == STUDIO_A4_SHA256, "studio_a5_parent_sha_mismatch")
    require(studio_a5.get("observed_studio_state", {}).get("a1_a4_commit", {}).get("sha") == "1f63a464ce017c3394f3733200618f678a016674", "studio_a5_a1_a4_commit_mismatch")
    require(studio_a5.get("observed_studio_state", {}).get("lr_874_commit", {}).get("sha") == "755f7b5d3583601418fc51abc828837d4dc1df30", "studio_a5_lr874_commit_mismatch")
    require(studio_a5.get("observed_studio_state", {}).get("ahead") == 0, "studio_a5_ahead_mismatch")
    require(studio_a5.get("observed_studio_state", {}).get("behind") == 0, "studio_a5_behind_mismatch")
    decision = studio_a5.get("decision", {})
    require(decision.get("retroactively_accept_external_commit_push") is False, "studio_a5_retroactive_authorization_drift")
    require(decision.get("freeze_Studio_product_and_evidence_writes") is True, "studio_a5_freeze_missing")
    require(decision.get("proceed_to_F013_readonly_review_of_committed_A4") is True, "studio_a5_review_handoff_missing")
    for key in ("Studio_product_write", "Studio_evidence_write", "Studio_commit", "Studio_push", "phase_2_disposable_kds_write", "shared_or_persistent_kds_write", "deployment", "status_promotion"):
        require(studio_a5.get("authorization", {}).get(key) is False, f"studio_a5_authorization_drift:{key}")

    studio_a6_text = read(STUDIO_A6)
    studio_a6_sha = hashlib.sha256(studio_a6_text.encode("utf-8")).hexdigest()
    require(studio_a6_sha == STUDIO_A6_SHA256, f"studio_a6_sha_mismatch:{studio_a6_sha}")
    studio_a6 = yaml.safe_load(studio_a6_text).get("studio_intake_rework_amendment", {})
    require(studio_a6.get("id") == STUDIO_A6_ID, "studio_a6_id_mismatch")
    require(studio_a6.get("type") == "bounded_phase_1_rework_after_f013_readonly_review", "studio_a6_type_mismatch")
    require(studio_a6.get("parent_controls", {}).get("a4", {}).get("sha256") == STUDIO_A4_SHA256, "studio_a6_a4_parent_sha_mismatch")
    require(studio_a6.get("parent_controls", {}).get("a5", {}).get("sha256") == STUDIO_A5_SHA256, "studio_a6_a5_parent_sha_mismatch")
    require(studio_a6.get("lane", {}).get("thread_id") == LANE_THREADS["studio"], "studio_a6_thread_mismatch")
    require(studio_a6.get("baseline", {}).get("head") == "755f7b5d3583601418fc51abc828837d4dc1df30", "studio_a6_baseline_mismatch")
    require(studio_a6.get("status", {}).get("phase_2") == "blocked", "studio_a6_phase2_boundary_mismatch")
    require(studio_a6.get("contract_correction", {}).get("supersedes_a4_requirement") == "tenant_and_org_match_authenticated_context", "studio_a6_contract_correction_missing")
    a6_allowlist = set(studio_a6.get("file_allowlist", ()))
    for required_path in (
        ".harness/opsx.lock",
        "packages/server/src/services/core/kds-client.ts",
        "packages/server/src/services/governance/knowledge-intake.ts",
        "packages/server/src/routes/governance/knowledge-intake.ts",
        "packages/client/src/components/studio/ProjectKnowledgeIntakePanel.vue",
        "tests/e2e/project-session-knowledge-intake.spec.ts",
        "docs/harness/loops/loop-round-GPCF-STUDIO-LR-875.md",
    ):
        require(required_path in a6_allowlist, f"studio_a6_allowlist_missing:{required_path}")
    for forbidden_path in ("packages/server/src/middleware/user-auth.ts", "packages/server/src/db/hermes/users-store.ts", "database_schema_or_migration"):
        require(forbidden_path in studio_a6.get("forbidden_scope", ()), f"studio_a6_forbidden_scope_missing:{forbidden_path}")
    require(studio_a6.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "studio_a6_lock_handling_mismatch")
    require(studio_a6.get("required_rework", {}).get("phase_1_file_boundary", {}).get("max_bytes") == 1048576, "studio_a6_file_limit_mismatch")
    require(len(studio_a6.get("required_rework", {}).get("simulated_browser_scenarios", {}).get("required", ())) == 7, "studio_a6_browser_scenarios_incomplete")
    require(studio_a6.get("authorization", {}).get("Studio_local_product_test_openspec_and_evidence_write") is True, "studio_a6_local_rework_not_authorized")
    for key in ("phase_2_disposable_kds_write", "real_or_shared_kds_mmc_write", "database_or_storage_migration", "relationship_or_candidate_confirmation", "long_term_memory_write", "business_state_change", "commit", "push", "deployment", "status_promotion"):
        require(studio_a6.get("authorization", {}).get(key) is False, f"studio_a6_authorization_drift:{key}")

    a7_text = read(MINIMAL_PARALLEL_A7)
    a7_sha = hashlib.sha256(a7_text.encode("utf-8")).hexdigest()
    require(a7_sha == MINIMAL_PARALLEL_A7_SHA256, f"minimal_parallel_a7_sha_mismatch:{a7_sha}")
    a7 = yaml.safe_load(a7_text).get("minimal_parallel_unfreeze_amendment", {})
    require(a7.get("id") == MINIMAL_PARALLEL_A7_ID, "minimal_parallel_a7_id_mismatch")
    require(a7.get("type") == "bounded_parallel_baseline_repair_and_authenticated_entry_preflight", "minimal_parallel_a7_type_mismatch")
    require(a7.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "minimal_parallel_a7_coordinator_mismatch")
    require(a7.get("parent_controls", {}).get("envelope", {}).get("sha256") == ENVELOPE_SHA256, "minimal_parallel_a7_envelope_parent_mismatch")
    require(a7.get("parent_controls", {}).get("studio_a6", {}).get("sha256") == STUDIO_A6_SHA256, "minimal_parallel_a7_a6_parent_mismatch")
    require(a7.get("canonical_contract", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "minimal_parallel_a7_manifest_mismatch")
    correction = a7.get("correction", {})
    require(correction.get("global_freeze") is False, "minimal_parallel_a7_global_freeze_drift")
    require(correction.get("deferred_gate_blocks_parallel_actions") is False, "minimal_parallel_a7_deferred_gate_blocks_parallel_work")
    studio_record = correction.get("studio_a6_record", {})
    require(studio_record.get("observed_head") == "88769078f5c230ae9ed973815de4861cc6317a5c", "minimal_parallel_a7_studio_head_mismatch")
    require(studio_record.get("observed_origin_main") == studio_record.get("observed_head"), "minimal_parallel_a7_studio_origin_mismatch")
    require(studio_record.get("observed_scope_count") == 14, "minimal_parallel_a7_studio_scope_count_mismatch")
    require(studio_record.get("technical_classification") == "simulated_only", "minimal_parallel_a7_studio_classification_mismatch")
    require(studio_record.get("authenticated_real_runtime_e2e") is False, "minimal_parallel_a7_false_real_e2e_claim")
    require(studio_record.get("observed_authenticated_session", {}).get("role") == "super_admin", "minimal_parallel_a7_studio_role_mismatch")
    require(studio_record.get("observed_authenticated_session", {}).get("tenant") == "gehua", "minimal_parallel_a7_studio_tenant_mismatch")
    require(studio_record.get("observed_demo_project", {}) == {"tenant": "tenant-demo", "org": "org-demo"}, "minimal_parallel_a7_demo_project_mismatch")
    require(studio_record.get("only_authenticity_gap") == "missing_authoritative_project_target_or_disposable_fixture_matching_authenticated_gehua_tenant_and_org", "minimal_parallel_a7_authenticity_gap_mismatch")
    brain_record = correction.get("brain_record", {})
    require(brain_record.get("observed_head") == "28d0eed530bce17c79651509973807e34e6205f4", "minimal_parallel_a7_brain_head_mismatch")
    require(brain_record.get("external_only_blocker_claim") is False, "minimal_parallel_a7_brain_external_only_drift")
    require("docs/harness/evidence/read-closure-matrix-20260622.json" in brain_record.get("observed_dirty_paths", ()), "minimal_parallel_a7_brain_dirty_evidence_missing")
    lanes_a7 = a7.get("lanes", {})
    require(set(lanes_a7) == {"brain", "studio"}, "minimal_parallel_a7_lane_set_mismatch")
    brain_a7 = lanes_a7["brain"]
    require(brain_a7.get("thread_id") == LANE_THREADS["brain"], "minimal_parallel_a7_brain_thread_mismatch")
    require(brain_a7.get("change_id") == "repair-brain-read-baseline-a7", "minimal_parallel_a7_brain_change_mismatch")
    require(brain_a7.get("execution_mode") == "local_tdd_no_live_kds", "minimal_parallel_a7_brain_mode_mismatch")
    require(brain_a7.get("tranche_control", {}).get("max_product_or_test_files_per_tranche") == 12, "minimal_parallel_a7_tranche_limit_mismatch")
    brain_allowlist = set(brain_a7.get("file_allowlist", ()))
    for required_path in (
        ".harness/opsx.lock",
        "src/app/components/SearchPanel.tsx",
        "src/app/components/SearchPanel.test.tsx",
        "docs/harness/evidence/read-closure-matrix-20260622.json",
        "openspec/changes/repair-brain-read-baseline-a7/**",
    ):
        require(required_path in brain_allowlist, f"minimal_parallel_a7_brain_allowlist_missing:{required_path}")
    require(set(brain_a7.get("immutable_deferred_e2e_evidence", ())) == {
        "docs/harness/evidence/browser-runtime-smoke-20260619.json",
        "docs/harness/evidence/browser-user-flow-20260619.json",
    }, "minimal_parallel_a7_browser_evidence_boundary_mismatch")
    require("any_live_KDS_or_MMC_network_call" in brain_a7.get("forbidden_scope", ()), "minimal_parallel_a7_brain_network_boundary_missing")
    studio_a7 = lanes_a7["studio"]
    require(studio_a7.get("thread_id") == LANE_THREADS["studio"], "minimal_parallel_a7_studio_thread_mismatch")
    require(studio_a7.get("change_id") == "verify-studio-authenticated-entry-a7", "minimal_parallel_a7_studio_change_mismatch")
    require(studio_a7.get("repository_file_allowlist") == [], "minimal_parallel_a7_studio_repository_write_allowed")
    require(studio_a7.get("baseline", {}).get("head") == "88769078f5c230ae9ed973815de4861cc6317a5c", "minimal_parallel_a7_studio_baseline_mismatch")
    target_resolution = studio_a7.get("authoritative_target_resolution", {})
    require(target_resolution.get("required_tenant") == "gehua" and target_resolution.get("required_org") == "gehua", "minimal_parallel_a7_target_identity_mismatch")
    require(target_resolution.get("preferred") == "select_existing_authorized_gehua_project_readonly", "minimal_parallel_a7_target_preference_mismatch")
    require("remove_fixture_after_preflight" in target_resolution.get("fallback_constraints", ()), "minimal_parallel_a7_fixture_cleanup_missing")
    require("tenant_demo_or_org_demo_used_as_authenticated_success_evidence" in studio_a7.get("forbidden_scope", ()), "minimal_parallel_a7_demo_success_forbidden_missing")
    auth_a7 = a7.get("authorization", {})
    for key in ("brain_local_tdd_within_allowlist", "brain_deterministic_local_evidence_refresh", "studio_readonly_authenticated_preflight", "studio_disposable_local_gehua_project_fixture_if_no_existing_match"):
        require(auth_a7.get(key) is True, f"minimal_parallel_a7_authorization_missing:{key}")
    for key in ("live_kds_or_mmc_read", "any_kds_or_mmc_write", "studio_intake_action", "business_fact_or_state_write", "long_term_memory_write", "relationship_or_candidate_confirmation", "commit", "push", "deployment", "status_promotion"):
        require(auth_a7.get(key) is False, f"minimal_parallel_a7_authorization_drift:{key}")
    require(a7.get("status", {}).get("completion") == "not_complete", "minimal_parallel_a7_completion_drift")
    require(a7.get("status", {}).get("status_ceiling") == "partial", "minimal_parallel_a7_status_ceiling_drift")

    a8_text = read(A7_GOVERNANCE_CLEANUP_A8)
    a8_sha = hashlib.sha256(a8_text.encode("utf-8")).hexdigest()
    require(a8_sha == A7_GOVERNANCE_CLEANUP_A8_SHA256, f"a7_governance_cleanup_a8_sha_mismatch:{a8_sha}")
    a8 = yaml.safe_load(a8_text).get("a7_governance_cleanup_rework_amendment", {})
    require(a8.get("id") == A7_GOVERNANCE_CLEANUP_A8_ID, "a7_governance_cleanup_a8_id_mismatch")
    require(a8.get("type") == "governance_handoff_and_disposable_session_cleanup_only", "a7_governance_cleanup_a8_type_mismatch")
    require(a8.get("parent_control", {}).get("id") == MINIMAL_PARALLEL_A7_ID, "a7_governance_cleanup_a8_parent_id_mismatch")
    require(a8.get("parent_control", {}).get("sha256") == MINIMAL_PARALLEL_A7_SHA256, "a7_governance_cleanup_a8_parent_sha_mismatch")
    require(a8.get("independent_review", {}).get("overall") == "partial_rework_required", "a7_governance_cleanup_a8_review_mismatch")
    require(a8.get("independent_review", {}).get("real_authenticated_e2e_authorized") is False, "a7_governance_cleanup_a8_real_e2e_drift")
    require(a8.get("parallel_rework", {}).get("requires_both_handoffs_before_next_gate") is True, "a7_governance_cleanup_a8_both_handoffs_missing")
    lanes_a8 = a8.get("lanes", {})
    require(set(lanes_a8) == {"brain", "studio"}, "a7_governance_cleanup_a8_lane_set_mismatch")
    brain_a8 = lanes_a8["brain"]
    require(brain_a8.get("thread_id") == LANE_THREADS["brain"], "a7_governance_cleanup_a8_brain_thread_mismatch")
    require(brain_a8.get("change_id") == "close-brain-a7-tranche1-opsx-handoff-a8", "a7_governance_cleanup_a8_brain_change_mismatch")
    require(brain_a8.get("execution_mode") == "governance_only_no_product_or_openspec_edits", "a7_governance_cleanup_a8_brain_mode_mismatch")
    require(brain_a8.get("run_id") == "20260811-repair-brain-read-baseline-a7-tranche-1", "a7_governance_cleanup_a8_run_id_mismatch")
    expected_frozen_product = {
        "src/app/App.tsx",
        "src/app/components/ChatPanel.test.tsx",
        "src/app/components/ChatPanel.tsx",
        "src/app/components/KnowledgeGraph.test.tsx",
        "src/app/components/SearchPanel.test.tsx",
        "src/app/components/SearchPanel.tsx",
        "src/app/components/WikiPreview.tsx",
    }
    require(set(brain_a8.get("preexisting_frozen_delta", {}).get("product_and_test_files", ())) == expected_frozen_product, "a7_governance_cleanup_a8_frozen_product_mismatch")
    expected_brain_a8_allowlist = {
        ".harness/evidence-index.yaml",
        ".harness/opsx.lock",
        ".harness/runs/20260811-repair-brain-read-baseline-a7-tranche-1/handoff.yaml",
        ".harness/runs/20260811-repair-brain-read-baseline-a7-tranche-1/evidence-index.yaml",
        ".harness/runs/20260811-repair-brain-read-baseline-a7-tranche-1/acceptance-matrix.md",
        ".harness/runs/20260811-repair-brain-read-baseline-a7-tranche-1/patches/tranche-1.patch",
        ".harness/runs/20260811-repair-brain-read-baseline-a7-tranche-1/workspaces/brain-tranche-1/agent-result.yaml",
        ".harness/runs/20260811-repair-brain-read-baseline-a7-tranche-1/evidence/final-verification.txt",
    }
    require(set(brain_a8.get("file_allowlist", ())) == expected_brain_a8_allowlist, "a7_governance_cleanup_a8_brain_allowlist_mismatch")
    require(brain_a8.get("handoff_contract", {}).get("status_claim") == "partial", "a7_governance_cleanup_a8_status_claim_mismatch")
    require(brain_a8.get("handoff_contract", {}).get("completion") == "not_complete", "a7_governance_cleanup_a8_completion_claim_mismatch")
    for forbidden in ("any_product_or_test_edit", "any_OpenSpec_edit", "tranche_2_start_or_edit", "live_KDS_or_MMC_network", "commit", "push", "deployment", "status_promotion"):
        require(forbidden in brain_a8.get("forbidden_scope", ()), f"a7_governance_cleanup_a8_brain_forbidden_missing:{forbidden}")
    studio_a8 = lanes_a8["studio"]
    require(studio_a8.get("thread_id") == LANE_THREADS["studio"], "a7_governance_cleanup_a8_studio_thread_mismatch")
    require(studio_a8.get("change_id") == "cleanup-studio-a7-disposable-session-a8", "a7_governance_cleanup_a8_studio_change_mismatch")
    require(studio_a8.get("repository_file_allowlist") == [], "a7_governance_cleanup_a8_studio_repository_write_allowed")
    allowed_mutation = studio_a8.get("target", {}).get("allowed_mutation", {})
    require(allowed_mutation.get("method") == "DELETE", "a7_governance_cleanup_a8_studio_method_mismatch")
    require(allowed_mutation.get("path") == "/api/hermes/sessions/{a7_temp_session_id}", "a7_governance_cleanup_a8_studio_path_mismatch")
    require(allowed_mutation.get("maximum_requests") == 1, "a7_governance_cleanup_a8_studio_delete_limit_mismatch")
    require(studio_a8.get("network_proof", {}).get("receipt", {}).get("delete_status") == 200, "a7_governance_cleanup_a8_studio_receipt_status_mismatch")
    require(studio_a8.get("failure_boundary", {}).get("network_capture_unavailable") == "do_not_delete_and_report_blocked_network_capture", "a7_governance_cleanup_a8_studio_capture_boundary_missing")
    for forbidden in ("more_than_one_DELETE_request", "any_new_session_fixture_or_binding_creation", "any_intake_upload_retry_complete_upload_or_direct_KDS_MMC_call", "commit", "push", "deployment", "status_promotion"):
        require(forbidden in studio_a8.get("forbidden_scope", ()), f"a7_governance_cleanup_a8_studio_forbidden_missing:{forbidden}")
    auth_a8 = a8.get("authorization", {})
    for key in ("brain_governance_handoff_files_within_allowlist", "brain_execution_lock_removal_after_package_validation", "studio_exactly_one_authenticated_A7_temp_session_delete", "studio_pre_and_post_delete_read"):
        require(auth_a8.get(key) is True, f"a7_governance_cleanup_a8_authorization_missing:{key}")
    for key in ("brain_product_or_openspec_edit", "brain_tranche_2", "studio_repository_write", "studio_new_fixture_or_binding", "live_authenticated_search_wikipreview_chat_e2e", "any_KDS_or_MMC_call_or_write", "business_fact_or_state_write", "commit", "push", "deployment", "status_promotion"):
        require(auth_a8.get(key) is False, f"a7_governance_cleanup_a8_authorization_drift:{key}")
    require(a8.get("status", {}).get("completion") == "not_complete", "a7_governance_cleanup_a8_completion_drift")
    require(a8.get("status", {}).get("status_ceiling") == "partial", "a7_governance_cleanup_a8_status_ceiling_drift")

    a9_text = read(A9_READ_ADMISSION)
    a9_sha = hashlib.sha256(a9_text.encode("utf-8")).hexdigest()
    require(a9_sha == A9_READ_ADMISSION_SHA256, f"a9_read_admission_sha_mismatch:{a9_sha}")
    a9 = yaml.safe_load(a9_text).get("a9_read_admission_amendment", {})
    require(a9.get("id") == A9_READ_ADMISSION_ID, "a9_read_admission_id_mismatch")
    require(a9.get("type") == "bounded_kds_stage_b_and_mmc_read_admission_replay", "a9_read_admission_type_mismatch")
    require(a9.get("program") == "GKE-001", "a9_program_mismatch")
    require(a9.get("release") == "release_0_customer_readonly_pilot", "a9_release_mismatch")
    require(a9.get("feature") == "F-013", "a9_feature_mismatch")
    require(a9.get("openspec_change") == "integrate-gke001-openspec-codegraph", "a9_openspec_mismatch")
    require(a9.get("parent_control", {}).get("id") == A7_GOVERNANCE_CLEANUP_A8_ID, "a9_parent_id_mismatch")
    require(a9.get("parent_control", {}).get("sha256") == A7_GOVERNANCE_CLEANUP_A8_SHA256, "a9_parent_sha_mismatch")
    entry_gate = a9.get("entry_gate", {})
    require(entry_gate.get("reviewer_thread_id") == "019fc228-2403-7123-9cae-fb9028850b84", "a9_reviewer_thread_mismatch")
    require(entry_gate.get("result") == "a8_brain_governance_and_studio_cleanup_conditions_closed", "a9_entry_gate_mismatch")
    require(entry_gate.get("brain_handoff") == "independently_verified", "a9_brain_entry_missing")
    require(entry_gate.get("studio_cleanup_and_network_proof") == "independently_verified", "a9_studio_entry_missing")
    require(entry_gate.get("real_authenticated_e2e_authorized") is False, "a9_false_e2e_authorization")
    require(a9.get("canonical_contract", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "a9_manifest_mismatch")
    require(a9.get("parallel_replay", {}).get("active_lanes") == 2, "a9_active_lane_count_mismatch")
    require(a9.get("parallel_replay", {}).get("requires_both_handoffs_before_exit_gate") is True, "a9_both_handoffs_missing")
    require(a9.get("parallel_replay", {}).get("product_file_changes_authorized") is False, "a9_product_write_drift")
    lanes_a9 = a9.get("lanes", {})
    require(set(lanes_a9) == {"kds", "mmc"}, "a9_lane_set_mismatch")
    kds_a9 = lanes_a9["kds"]
    require(kds_a9.get("thread_id") == LANE_THREADS["kds"], "a9_kds_thread_mismatch")
    require(kds_a9.get("change_id") == "verify-kds-stage-b-read-admission-a9", "a9_kds_change_mismatch")
    require(kds_a9.get("execution_mode") == "read_only_replay_existing_stage_b_handoff", "a9_kds_mode_mismatch")
    require(kds_a9.get("repository_file_allowlist") == [], "a9_kds_file_write_allowed")
    require(kds_a9.get("baseline", {}).get("admission") == "blocked_dirty_worktree", "a9_kds_dirty_admission_missing")
    require(kds_a9.get("existing_handoff", {}).get("independent_f013_result") == "technical_review_verified_governance_partial", "a9_kds_f013_result_mismatch")
    for required in (
        "acl_before_read_search_and_count_in_memory_and_postgresql",
        "transactional_start_recovery_completion_failure_audit_and_deduplicable_outbox",
        "stage_a_plus_stage_b_repeatable_migration_dry_run",
        "disposable_database_cleanup_count_zero",
        "append_only_compensating_active_selection_rollback",
    ):
        require(required in kds_a9.get("required_evidence", ()), f"a9_kds_evidence_missing:{required}")
    for forbidden in ("any_repository_file_change", "any_real_shared_or_production_kds_read_or_write", "any_production_or_shared_database_migration", "commit", "push", "deployment", "status_promotion"):
        require(forbidden in kds_a9.get("forbidden_scope", ()), f"a9_kds_forbidden_missing:{forbidden}")
    mmc_a9 = lanes_a9["mmc"]
    require(mmc_a9.get("thread_id") == LANE_THREADS["studio"], "a9_mmc_thread_mismatch")
    require(mmc_a9.get("change_id") == "verify-mmc-kds-read-admission-a9", "a9_mmc_change_mismatch")
    require(mmc_a9.get("execution_mode") == "read_only_policy_contract_and_in_process_test_replay", "a9_mmc_mode_mismatch")
    require(mmc_a9.get("repository_file_allowlist") == [], "a9_mmc_file_write_allowed")
    governed_ops = mmc_a9.get("governed_read_subset", {}).get("operations", ())
    require({(item.get("method"), item.get("path_pattern")) for item in governed_ops} == {("GET", "*"), ("POST", "/api/v1/projects/*/search")}, "a9_mmc_read_subset_mismatch")
    for required in (
        "validated_service_identity_and_signed_user_delegation",
        "exact_method_and_segment_aware_path_matching",
        "traversal_nested_path_and_unregistered_operation_denial",
        "admission_before_proxy_and_status_only_denial_audit",
        "no_generic_write_operation_added_or_invoked_by_A9",
    ):
        require(required in mmc_a9.get("required_evidence", ()), f"a9_mmc_evidence_missing:{required}")
    for forbidden in ("any_repository_file_change", "any_seed_registry_runtime_state_or_permission_change", "any_live_kds_or_mmc_request", "any_intake_upload_retry_complete_upload_or_other_write_invocation", "commit", "push", "restart", "deployment", "status_promotion"):
        require(forbidden in mmc_a9.get("forbidden_scope", ()), f"a9_mmc_forbidden_missing:{forbidden}")
    auth_a9 = a9.get("authorization", {})
    for key in ("local_read_only_repository_and_evidence_inspection", "local_in_process_tests", "disposable_postgresql_test_database_with_cleanup"):
        require(auth_a9.get(key) is True, f"a9_authorization_missing:{key}")
    for key in ("product_test_openspec_or_evidence_file_write", "live_kds_or_mmc_read", "any_kds_or_mmc_write", "production_or_shared_migration", "studio_or_brain_execution", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a9.get(key) is False, f"a9_authorization_drift:{key}")
    require(a9.get("serial_exit_gate", {}).get("A10_automatic_authorization") is False, "a9_automatic_a10_drift")
    require(a9.get("status", {}).get("completion") == "not_complete", "a9_completion_drift")
    require(a9.get("status", {}).get("status_ceiling") == "partial", "a9_status_ceiling_drift")

    a9r1_text = read(A9_MMC_ROLLBACK_REWORK)
    a9r1_sha = hashlib.sha256(a9r1_text.encode("utf-8")).hexdigest()
    require(a9r1_sha == A9_MMC_ROLLBACK_REWORK_SHA256, f"a9r1_sha_mismatch:{a9r1_sha}")
    a9r1 = yaml.safe_load(a9r1_text).get("a9_mmc_rollback_handoff_rework", {})
    require(a9r1.get("id") == A9_MMC_ROLLBACK_REWORK_ID, "a9r1_id_mismatch")
    require(a9r1.get("type") == "report_only_mmc_bounded_read_subset_rollback_addendum", "a9r1_type_mismatch")
    require(a9r1.get("parent_control", {}).get("id") == A9_READ_ADMISSION_ID, "a9r1_parent_id_mismatch")
    require(a9r1.get("parent_control", {}).get("sha256") == A9_READ_ADMISSION_SHA256, "a9r1_parent_sha_mismatch")
    review_a9r1 = a9r1.get("independent_review", {})
    require(review_a9r1.get("result") == "a9_serial_exit_rework_required_4_of_5", "a9r1_review_result_mismatch")
    require(review_a9r1.get("only_rework_gap") == "explicit_mmc_rollback_boundary_for_governed_read_subset", "a9r1_gap_mismatch")
    require(review_a9r1.get("a10_authorized") is False, "a9r1_a10_authorization_drift")
    lane_a9r1 = a9r1.get("lane", {})
    require(lane_a9r1.get("thread_id") == LANE_THREADS["studio"], "a9r1_thread_mismatch")
    require(lane_a9r1.get("repository") == "GlobalCloud MMC", "a9r1_repository_mismatch")
    require(lane_a9r1.get("change_id") == "close-mmc-a9-rollback-handoff-a9r1", "a9r1_change_mismatch")
    require(lane_a9r1.get("execution_mode") == "report_only_no_repository_or_runtime_action", "a9r1_mode_mismatch")
    require(lane_a9r1.get("repository_file_allowlist") == [], "a9r1_file_write_allowed")
    require(lane_a9r1.get("coordination_lock_id") == "none_report_only", "a9r1_lock_mismatch")
    for required in (
        "state_that_A9_changed_no_seed_state_permission_configuration_or_code",
        "state_that_A9_rollback_is_stop_or_withdraw_the_two_operation_governed_use_scope_with_no_configuration_restore",
        "state_that_all_17_active_operations_remain_unchanged",
        "state_that_the_other_15_operations_are_outside_A9_and_receive_no_authorization_from_A9_or_A9R1",
        "state_that_future_A10_policy_isolation_or_narrowing_requires_a_new_control_with_exact_configuration_allowlist_before_and_after_fingerprints_and_restore_baseline",
        "preserve_partial_not_complete_and_no_A10_authorization",
    ):
        require(required in lane_a9r1.get("required_addendum", ()), f"a9r1_addendum_missing:{required}")
    for forbidden in ("any_repository_file_change", "any_seed_state_registry_permission_configuration_or_code_change", "any_live_kds_or_mmc_request", "any_policy_isolation_narrowing_or_reclassification", "commit", "push", "restart", "deployment", "a10_authorization", "real_authenticated_e2e", "status_promotion"):
        require(forbidden in a9r1.get("forbidden_scope", ()), f"a9r1_forbidden_missing:{forbidden}")
    auth_a9r1 = a9r1.get("authorization", {})
    for key in ("local_read_only_repository_and_control_inspection", "report_only_thread_response"):
        require(auth_a9r1.get(key) is True, f"a9r1_authorization_missing:{key}")
    for key in ("repository_file_write", "runtime_or_configuration_change", "live_kds_or_mmc_read", "any_kds_or_mmc_write", "studio_or_brain_execution", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a9r1.get(key) is False, f"a9r1_authorization_drift:{key}")
    require(a9r1.get("serial_exit_gate", {}).get("A10_automatic_authorization") is False, "a9r1_automatic_a10_drift")
    require(a9r1.get("status", {}).get("completion") == "not_complete", "a9r1_completion_drift")
    require(a9r1.get("status", {}).get("status_ceiling") == "partial", "a9r1_status_ceiling_drift")

    a10p0_text = read(A10_READONLY_PREFLIGHT)
    a10p0_sha = hashlib.sha256(a10p0_text.encode("utf-8")).hexdigest()
    require(a10p0_sha == A10_READONLY_PREFLIGHT_SHA256, f"a10p0_sha_mismatch:{a10p0_sha}")
    a10p0 = yaml.safe_load(a10p0_text).get("a10_readonly_preflight", {})
    require(a10p0.get("id") == A10_READONLY_PREFLIGHT_ID, "a10p0_id_mismatch")
    require(a10p0.get("type") == "zero_write_contract_and_runtime_readiness_preflight", "a10p0_type_mismatch")
    require(a10p0.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10p0_coordinator_mismatch")
    require(a10p0.get("parent_control", {}).get("sha256") == A9_MMC_ROLLBACK_REWORK_SHA256, "a10p0_parent_sha_mismatch")
    require(a10p0.get("canonical_contract", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "a10p0_manifest_mismatch")
    lanes_a10p0 = a10p0.get("parallel_lanes", {})
    require(set(lanes_a10p0) == {"studio_mmc", "brain", "kds"}, "a10p0_lane_set_mismatch")
    require(lanes_a10p0["studio_mmc"].get("thread_id") == LANE_THREADS["studio"], "a10p0_studio_thread_mismatch")
    require(lanes_a10p0["brain"].get("thread_id") == LANE_THREADS["brain"], "a10p0_brain_thread_mismatch")
    require(lanes_a10p0["kds"].get("thread_id") == LANE_THREADS["kds"], "a10p0_kds_thread_mismatch")
    for lane_name, lane in lanes_a10p0.items():
        require(lane.get("repository_file_allowlist") == [], f"a10p0_repository_write_allowed:{lane_name}")
        require(lane.get("coordination_lock_id") == "none_report_only", f"a10p0_lock_mismatch:{lane_name}")
        require("status_promotion" in lane.get("forbidden_scope", ()), f"a10p0_status_promotion_not_forbidden:{lane_name}")
    require(lanes_a10p0["brain"].get("baseline", {}).get("dirty_entries") == 9, "a10p0_brain_dirty_count_mismatch")
    require(lanes_a10p0["kds"].get("baseline", {}).get("ordinary_dirty_entries") == 166, "a10p0_kds_dirty_count_mismatch")
    serial_a10p0 = a10p0.get("serial_gate", {})
    require(serial_a10p0.get("requires_all_three_handoffs") is True, "a10p0_three_handoffs_not_required")
    require(serial_a10p0.get("A10_live_read_automatic_authorization") is False, "a10p0_live_read_auto_authorization_drift")
    require(serial_a10p0.get("real_authenticated_search_wikipreview_chat_e2e") is False, "a10p0_real_e2e_drift")
    auth_a10p0 = a10p0.get("authorization", {})
    for key in ("static_repository_and_control_read", "local_no_write_validation", "report_only_thread_handoff"):
        require(auth_a10p0.get(key) is True, f"a10p0_authorization_missing:{key}")
    for key in ("repository_file_write", "runtime_or_configuration_change", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "real_authenticated_e2e", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a10p0.get(key) is False, f"a10p0_authorization_drift:{key}")
    require(a10p0.get("status", {}).get("completion") == "not_complete", "a10p0_completion_drift")
    require(a10p0.get("status", {}).get("status_ceiling") == "partial", "a10p0_status_ceiling_drift")

    a10p1_text = read(A10P1_COORDINATION)
    a10p1_sha = hashlib.sha256(a10p1_text.encode("utf-8")).hexdigest()
    require(a10p1_sha == A10P1_COORDINATION_SHA256, f"a10p1_sha_mismatch:{a10p1_sha}")
    a10p1 = yaml.safe_load(a10p1_text).get("a10p1_coordination", {})
    require(a10p1.get("id") == A10P1_COORDINATION_ID, "a10p1_id_mismatch")
    require(a10p1.get("parent_control", {}).get("sha256") == A10_READONLY_PREFLIGHT_SHA256, "a10p1_parent_sha_mismatch")
    require(a10p1.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10p1_coordinator_mismatch")
    require(a10p1.get("canonical_contract", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "a10p1_manifest_mismatch")
    require(a10p1.get("canonical_contract", {}).get("compatibility_decision", {}).get("stage_b_and_legacy_projects_reads_are_compatible") is False, "a10p1_false_compatibility_claim")
    lanes_a10p1 = a10p1.get("parallel_lanes", {})
    require(set(lanes_a10p1) == {"studio_mmc", "kds", "brain"}, "a10p1_lane_set_mismatch")
    require(lanes_a10p1["studio_mmc"].get("thread_id") == LANE_THREADS["studio"], "a10p1_studio_thread_mismatch")
    require(lanes_a10p1["kds"].get("thread_id") == LANE_THREADS["kds"], "a10p1_kds_thread_mismatch")
    require(lanes_a10p1["brain"].get("thread_id") == LANE_THREADS["brain"], "a10p1_brain_thread_mismatch")
    for lane_name in ("studio_mmc", "kds"):
        lane = lanes_a10p1[lane_name]
        require(lane.get("repository_file_allowlist") == [], f"a10p1_report_lane_write_allowed:{lane_name}")
        require(lane.get("coordination_lock_id") == "none_report_only", f"a10p1_report_lane_lock_mismatch:{lane_name}")
    brain_files = lanes_a10p1["brain"].get("product_test_file_allowlist", [])
    require(len(brain_files) == 6 and len(set(brain_files)) == 6, "a10p1_brain_six_file_scope_mismatch")
    require(lanes_a10p1["brain"].get("product_test_file_limit") == 12, "a10p1_brain_file_limit_mismatch")
    require(lanes_a10p1["brain"].get("baseline", {}).get("dirty_entries") == 9, "a10p1_brain_baseline_mismatch")
    serial_a10p1 = a10p1.get("serial_gate", {})
    require(serial_a10p1.get("requires_all_three_handoffs") is True, "a10p1_three_handoffs_not_required")
    require(serial_a10p1.get("A10_live_read_automatic_authorization") is False, "a10p1_live_read_auto_authorization_drift")
    require(serial_a10p1.get("real_authenticated_search_wikipreview_chat_e2e") is False, "a10p1_real_e2e_drift")
    require(serial_a10p1.get("Brain_tranche_completion_unlocks_live_read") is False, "a10p1_brain_unlock_drift")
    auth_a10p1 = a10p1.get("authorization", {})
    for key in ("static_repository_and_control_read", "report_only_contract_convergence", "brain_six_file_local_tdd", "brain_run_scoped_governance_evidence"):
        require(auth_a10p1.get(key) is True, f"a10p1_authorization_missing:{key}")
    for key in ("Studio_MMC_or_KDS_repository_file_write", "runtime_or_configuration_change", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "real_authenticated_e2e", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a10p1.get(key) is False, f"a10p1_authorization_drift:{key}")
    require(a10p1.get("status", {}).get("completion") == "not_complete", "a10p1_completion_drift")
    require(a10p1.get("status", {}).get("status_ceiling") == "partial", "a10p1_status_ceiling_drift")

    candidate_text = read(A10P2_CANDIDATE)
    candidate_sha = hashlib.sha256(candidate_text.encode("utf-8")).hexdigest()
    require(candidate_sha == A10P2_CANDIDATE_SHA256, f"a10p2_candidate_sha_mismatch:{candidate_sha}")
    candidate = json.loads(candidate_text)
    require(candidate.get("contract_id") == "globalcloud.kds.canonical-read", "a10p2_candidate_contract_mismatch")
    candidate_ops = {(item.get("method"), item.get("path")) for item in candidate.get("operations", [])}
    require(candidate_ops == {
        ("POST", "/api/v1/knowledge-read/release-0/search"),
        ("POST", "/api/v1/knowledge-read/release-0/read"),
    }, "a10p2_candidate_operation_mismatch")
    require(candidate.get("status") == "candidate_not_frozen_not_implemented", "a10p2_candidate_status_drift")

    a10p2_text = read(A10P2_COORDINATION)
    a10p2_sha = hashlib.sha256(a10p2_text.encode("utf-8")).hexdigest()
    require(a10p2_sha == A10P2_COORDINATION_SHA256, f"a10p2_sha_mismatch:{a10p2_sha}")
    a10p2 = yaml.safe_load(a10p2_text).get("a10p2_joint_contract_freeze", {})
    require(a10p2.get("id") == A10P2_COORDINATION_ID, "a10p2_id_mismatch")
    require(a10p2.get("parent_control", {}).get("sha256") == A10P1_COORDINATION_SHA256, "a10p2_parent_sha_mismatch")
    require(a10p2.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10p2_coordinator_mismatch")
    require(a10p2.get("candidate_contract", {}).get("sha256") == A10P2_CANDIDATE_SHA256, "a10p2_candidate_reference_mismatch")
    lanes_a10p2 = a10p2.get("parallel_lanes", {})
    require(set(lanes_a10p2) == {"studio_mmc", "kds", "brain"}, "a10p2_lane_set_mismatch")
    require(lanes_a10p2["studio_mmc"].get("thread_id") == LANE_THREADS["studio"], "a10p2_studio_thread_mismatch")
    require(lanes_a10p2["kds"].get("thread_id") == LANE_THREADS["kds"], "a10p2_kds_thread_mismatch")
    require(lanes_a10p2["brain"].get("thread_id") == LANE_THREADS["brain"], "a10p2_brain_thread_mismatch")
    for lane_name in ("studio_mmc", "kds", "brain"):
        require(lanes_a10p2[lane_name].get("repository_file_allowlist") == [], f"a10p2_repository_write_allowed:{lane_name}")
    require(lanes_a10p2["brain"].get("execution_mode") == "freeze_and_wait", "a10p2_brain_not_frozen")
    serial_a10p2 = a10p2.get("serial_gate", {})
    require(serial_a10p2.get("requires_both_reports") is True, "a10p2_reports_not_required")
    for key in ("automatic_contract_freeze", "implementation_authorized", "live_read_authorized", "real_e2e_authorized"):
        require(serial_a10p2.get(key) is False, f"a10p2_serial_boundary_drift:{key}")
    auth_a10p2 = a10p2.get("authorization", {})
    for key in ("static_read_and_hash", "report_only_thread_handoff"):
        require(auth_a10p2.get(key) is True, f"a10p2_authorization_missing:{key}")
    for key in ("repository_file_write", "runtime_policy_or_configuration_change", "database_or_external_data_access", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "Brain_tranche_3", "real_authenticated_e2e", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a10p2.get(key) is False, f"a10p2_authorization_drift:{key}")
    require(a10p2.get("status", {}).get("completion") == "not_complete", "a10p2_completion_drift")
    require(a10p2.get("status", {}).get("status_ceiling") == "partial", "a10p2_status_ceiling_drift")

    a10p3_schema_bytes = A10P3_SCHEMA.read_bytes()
    a10p3_schema_sha = hashlib.sha256(a10p3_schema_bytes).hexdigest()
    require(a10p3_schema_sha == A10P3_SCHEMA_SHA256, f"a10p3_schema_sha_mismatch:{a10p3_schema_sha}")
    a10p3_schema = yaml.safe_load(a10p3_schema_bytes)
    require(a10p3_schema.get("openapi") == "3.1.0", "a10p3_openapi_version_mismatch")
    require(a10p3_schema.get("x-status") == "candidate_not_frozen_not_implemented", "a10p3_schema_status_drift")
    expected_a10p3_ops = [
        ("POST", "/api/v1/knowledge-read/release-0/search"),
        ("POST", "/api/v1/knowledge-read/release-0/read"),
    ]
    schema_ops = [(item.get("method"), item.get("path")) for item in a10p3_schema.get("x-kds-canonical-operations", [])]
    require(schema_ops == expected_a10p3_ops, "a10p3_schema_operation_mismatch")
    canonical_schema = json.dumps(a10p3_schema, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(canonical_schema).hexdigest() == A10P3_SCHEMA_CANONICAL_SHA256, "a10p3_schema_canonical_sha_mismatch")
    matrix = []
    for method, path in expected_a10p3_ops:
        operation = a10p3_schema["paths"][path][method.lower()]
        matrix.append({
            "method": method,
            "path": path,
            "request": operation["requestBody"]["content"]["application/json"]["schema"],
            "response": operation["responses"]["200"]["content"]["application/json"]["schema"],
        })
    normalized_matrix = json.dumps(matrix, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(normalized_matrix).hexdigest() == A10P3_OPERATION_MATRIX_SHA256, "a10p3_operation_matrix_sha_mismatch")

    a10p3_text = read(A10P3_COORDINATION)
    a10p3_sha = hashlib.sha256(a10p3_text.encode("utf-8")).hexdigest()
    require(a10p3_sha == A10P3_COORDINATION_SHA256, f"a10p3_sha_mismatch:{a10p3_sha}")
    a10p3 = yaml.safe_load(a10p3_text).get("a10p3_field_schema_and_file_allowlist_freeze", {})
    require(a10p3.get("id") == A10P3_COORDINATION_ID, "a10p3_id_mismatch")
    require(a10p3.get("parent_control", {}).get("sha256") == A10P2_COORDINATION_SHA256, "a10p3_parent_sha_mismatch")
    require(a10p3.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10p3_coordinator_mismatch")
    schema_ref = a10p3.get("field_schema_candidate", {})
    require(schema_ref.get("raw_sha256") == A10P3_SCHEMA_SHA256, "a10p3_schema_reference_mismatch")
    require(schema_ref.get("canonical_json_sha256") == A10P3_SCHEMA_CANONICAL_SHA256, "a10p3_canonical_reference_mismatch")
    require(schema_ref.get("operation_matrix_sha256") == A10P3_OPERATION_MATRIX_SHA256, "a10p3_matrix_reference_mismatch")
    lanes_a10p3 = a10p3.get("parallel_lanes", {})
    require(set(lanes_a10p3) == {"studio_mmc", "kds", "brain"}, "a10p3_lane_set_mismatch")
    require(lanes_a10p3["studio_mmc"].get("thread_id") == LANE_THREADS["studio"], "a10p3_studio_thread_mismatch")
    require(lanes_a10p3["kds"].get("thread_id") == LANE_THREADS["kds"], "a10p3_kds_thread_mismatch")
    require(lanes_a10p3["brain"].get("thread_id") == LANE_THREADS["brain"], "a10p3_brain_thread_mismatch")
    for lane_name in ("studio_mmc", "kds", "brain"):
        require(lanes_a10p3[lane_name].get("repository_file_allowlist") == [], f"a10p3_repository_write_allowed:{lane_name}")
    require(lanes_a10p3["brain"].get("execution_mode") == "freeze_and_wait", "a10p3_brain_not_frozen")
    serial_a10p3 = a10p3.get("serial_gate", {})
    for key in ("automatic_contract_freeze", "implementation_authorized", "policy_change_authorized", "live_read_authorized", "real_e2e_authorized"):
        require(serial_a10p3.get(key) is False, f"a10p3_serial_boundary_drift:{key}")
    auth_a10p3 = a10p3.get("authorization", {})
    for key in ("GPCF_candidate_schema_and_control_write", "static_repository_and_existing_evidence_read", "report_only_thread_handoff"):
        require(auth_a10p3.get(key) is True, f"a10p3_authorization_missing:{key}")
    for key in ("lane_repository_file_write", "runtime_policy_or_configuration_change", "database_or_external_data_access", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "Brain_tranche_3", "real_authenticated_e2e", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a10p3.get(key) is False, f"a10p3_authorization_drift:{key}")
    require(a10p3.get("status", {}).get("completion") == "not_complete", "a10p3_completion_drift")
    require(a10p3.get("status", {}).get("status_ceiling") == "partial", "a10p3_status_ceiling_drift")

    a10p3r1_schema_bytes = A10P3R1_SCHEMA.read_bytes()
    require(hashlib.sha256(a10p3r1_schema_bytes).hexdigest() == A10P3R1_SCHEMA_SHA256, "a10p3r1_schema_sha_mismatch")
    a10p3r1_schema = yaml.safe_load(a10p3r1_schema_bytes)
    require(a10p3r1_schema.get("openapi") == "3.1.0", "a10p3r1_openapi_version_mismatch")
    require(a10p3r1_schema.get("x-status") == "candidate_not_frozen_not_implemented", "a10p3r1_schema_status_drift")
    require("allOf" not in a10p3r1_schema["components"]["schemas"]["SearchRequest"], "a10p3r1_search_composition_not_corrected")
    require("parsing" in a10p3r1_schema["components"]["schemas"]["AssetProjection"]["properties"]["lifecycle_state"]["enum"], "a10p3r1_parsing_state_missing")
    require("x-mmc-delegation-authority-binding" in a10p3r1_schema, "a10p3r1_authority_binding_missing")
    canonical_a10p3r1 = json.dumps(a10p3r1_schema, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(canonical_a10p3r1).hexdigest() == A10P3R1_SCHEMA_CANONICAL_SHA256, "a10p3r1_schema_canonical_sha_mismatch")
    require(hashlib.sha256(A10P3R1_NORMALIZER.read_bytes()).hexdigest() == A10P3R1_NORMALIZER_SHA256, "a10p3r1_normalizer_sha_mismatch")
    matrix_r1 = []
    for method, path in expected_a10p3_ops:
        operation = a10p3r1_schema["paths"][path][method.lower()]
        matrix_r1.append({
            "method": method,
            "path": path,
            "request": operation["requestBody"]["content"]["application/json"]["schema"],
            "response": operation["responses"]["200"]["content"]["application/json"]["schema"],
        })
    normalized_matrix_r1 = json.dumps(matrix_r1, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(normalized_matrix_r1).hexdigest() == A10P3_OPERATION_MATRIX_SHA256, "a10p3r1_operation_matrix_sha_mismatch")

    a10p3r1_text = read(A10P3R1_COORDINATION)
    require(hashlib.sha256(a10p3r1_text.encode("utf-8")).hexdigest() == A10P3R1_COORDINATION_SHA256, "a10p3r1_coordination_sha_mismatch")
    a10p3r1 = yaml.safe_load(a10p3r1_text).get("a10p3r1_field_schema_rework", {})
    require(a10p3r1.get("id") == A10P3R1_COORDINATION_ID, "a10p3r1_id_mismatch")
    require(a10p3r1.get("parent_control", {}).get("sha256") == A10P3_COORDINATION_SHA256, "a10p3r1_parent_sha_mismatch")
    require(a10p3r1.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10p3r1_coordinator_mismatch")
    require(a10p3r1.get("corrected_schema_candidate", {}).get("raw_sha256") == A10P3R1_SCHEMA_SHA256, "a10p3r1_schema_reference_mismatch")
    require(a10p3r1.get("executable_normalizer", {}).get("raw_sha256") == A10P3R1_NORMALIZER_SHA256, "a10p3r1_normalizer_reference_mismatch")
    frozen_files = a10p3r1.get("frozen_future_file_requests", {})
    require(frozen_files.get("studio", {}).get("count") == len(frozen_files.get("studio", {}).get("paths", [])) == 10, "a10p3r1_studio_file_count_mismatch")
    require(frozen_files.get("mmc", {}).get("count") == len(frozen_files.get("mmc", {}).get("paths", [])) == 8, "a10p3r1_mmc_file_count_mismatch")
    require(frozen_files.get("kds", {}).get("count") == len(frozen_files.get("kds", {}).get("paths", [])) == 12, "a10p3r1_kds_file_count_mismatch")
    lanes_a10p3r1 = a10p3r1.get("parallel_lanes", {})
    require(set(lanes_a10p3r1) == {"studio_mmc", "kds", "brain"}, "a10p3r1_lane_set_mismatch")
    require(lanes_a10p3r1["studio_mmc"].get("thread_id") == LANE_THREADS["studio"], "a10p3r1_studio_thread_mismatch")
    require(lanes_a10p3r1["kds"].get("thread_id") == LANE_THREADS["kds"], "a10p3r1_kds_thread_mismatch")
    require(lanes_a10p3r1["brain"].get("thread_id") == LANE_THREADS["brain"], "a10p3r1_brain_thread_mismatch")
    for lane_name in ("studio_mmc", "kds", "brain"):
        require(lanes_a10p3r1[lane_name].get("repository_file_allowlist") == [], f"a10p3r1_repository_write_allowed:{lane_name}")
    serial_a10p3r1 = a10p3r1.get("serial_gate", {})
    for key in ("automatic_contract_freeze", "implementation_authorized", "policy_change_authorized", "live_read_authorized", "real_e2e_authorized"):
        require(serial_a10p3r1.get(key) is False, f"a10p3r1_serial_boundary_drift:{key}")
    auth_a10p3r1 = a10p3r1.get("authorization", {})
    for key in ("GPCF_corrected_schema_normalizer_and_control_write", "lane_static_read_and_report"):
        require(auth_a10p3r1.get(key) is True, f"a10p3r1_authorization_missing:{key}")
    for key in ("lane_repository_file_write", "runtime_policy_or_configuration_change", "database_or_external_data_access", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "Brain_tranche_3", "real_authenticated_e2e", "commit", "push", "restart", "deployment", "status_promotion"):
        require(auth_a10p3r1.get(key) is False, f"a10p3r1_authorization_drift:{key}")
    require(a10p3r1.get("status", {}).get("completion") == "not_complete", "a10p3r1_completion_drift")
    require(a10p3r1.get("status", {}).get("status_ceiling") == "partial", "a10p3r1_status_ceiling_drift")

    a10p3r2_schema_bytes = A10P3R2_SCHEMA.read_bytes()
    require(hashlib.sha256(a10p3r2_schema_bytes).hexdigest() == A10P3R2_SCHEMA_SHA256, "a10p3r2_schema_sha_mismatch")
    a10p3r2_schema = yaml.safe_load(a10p3r2_schema_bytes)
    require(a10p3r2_schema.get("openapi") == "3.1.0", "a10p3r2_openapi_version_mismatch")
    require(a10p3r2_schema.get("x-status") == "candidate_not_frozen_not_implemented", "a10p3r2_embedded_status_drift")
    require(a10p3r2_schema.get("x-mmc-policy", {}).get("candidate_isolated_fingerprint") == MMC_CANDIDATE_FINGERPRINT, "a10p3r2_mmc_candidate_fingerprint_mismatch")
    require(a10p3r2_schema.get("x-mmc-policy", {}).get("current_and_restore_fingerprint") == MMC_RESTORE_FINGERPRINT, "a10p3r2_mmc_restore_fingerprint_mismatch")
    canonical_a10p3r2 = json.dumps(a10p3r2_schema, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(canonical_a10p3r2).hexdigest() == A10P3R2_SCHEMA_CANONICAL_SHA256, "a10p3r2_schema_canonical_sha_mismatch")
    matrix_r2 = []
    for method, path in expected_a10p3_ops:
        operation = a10p3r2_schema["paths"][path][method.lower()]
        matrix_r2.append({
            "method": method,
            "path": path,
            "request": operation["requestBody"]["content"]["application/json"]["schema"],
            "response": operation["responses"]["200"]["content"]["application/json"]["schema"],
        })
    normalized_matrix_r2 = json.dumps(matrix_r2, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(normalized_matrix_r2).hexdigest() == A10P3_OPERATION_MATRIX_SHA256, "a10p3r2_operation_matrix_sha_mismatch")
    require(a10p3r1_schema.get("components") == a10p3r2_schema.get("components"), "a10p3r2_components_changed")
    require(a10p3r1_schema.get("paths") == a10p3r2_schema.get("paths"), "a10p3r2_paths_changed")

    a10p3r2_text = read(A10P3R2_COORDINATION)
    require(hashlib.sha256(a10p3r2_text.encode("utf-8")).hexdigest() == A10P3R2_COORDINATION_SHA256, "a10p3r2_coordination_sha_mismatch")
    a10p3r2 = yaml.safe_load(a10p3r2_text).get("a10p3r2_metadata_only_contract_reconciliation", {})
    require(a10p3r2.get("id") == A10P3R2_COORDINATION_ID, "a10p3r2_id_mismatch")
    require(a10p3r2.get("parent_control", {}).get("sha256") == A10P3R1_COORDINATION_SHA256, "a10p3r2_parent_sha_mismatch")
    require(a10p3r2.get("exact_single_field_delta", {}).get("changed_schema_lines") == 1, "a10p3r2_not_single_line_delta")
    require(a10p3r2.get("exact_single_field_delta", {}).get("after") == MMC_CANDIDATE_FINGERPRINT, "a10p3r2_delta_fingerprint_mismatch")
    require(a10p3r2.get("preserved_evidence", {}).get("operation_matrix_sha256") == A10P3_OPERATION_MATRIX_SHA256, "a10p3r2_matrix_reference_mismatch")
    for lane_name in ("studio_mmc", "kds", "brain"):
        require(a10p3r2.get("parallel_lanes", {}).get(lane_name, {}).get("repository_file_allowlist") == [], f"a10p3r2_repository_write_allowed:{lane_name}")
    for key in ("implementation_authorized", "policy_change_authorized", "live_read_authorized", "real_e2e_authorized"):
        require(a10p3r2.get("serial_gate", {}).get(key) is False, f"a10p3r2_serial_boundary_drift:{key}")

    freeze_text = read(A10P3R2_FREEZE)
    require(hashlib.sha256(freeze_text.encode("utf-8")).hexdigest() == A10P3R2_FREEZE_SHA256, "a10p3r2_freeze_sha_mismatch")
    freeze = yaml.safe_load(freeze_text).get("release0_canonical_read_contract_freeze", {})
    require(freeze.get("id") == A10P3R2_FREEZE_ID, "a10p3r2_freeze_id_mismatch")
    require(freeze.get("contract", {}).get("status") == "contract_frozen_for_future_implementation_not_integrated", "a10p3r2_freeze_status_mismatch")
    require(freeze.get("contract", {}).get("raw_sha256") == A10P3R2_SCHEMA_SHA256, "a10p3r2_freeze_schema_reference_mismatch")
    require(freeze.get("independent_review", {}).get("classification") == "byte_freeze_passed", "a10p3r2_review_classification_mismatch")
    boundaries = freeze.get("future_implementation_boundaries", {})
    for lane_name, count in (("kds", 12), ("studio", 10), ("mmc_standard", 6), ("mmc_high_risk_policy_configuration", 2)):
        require(boundaries.get(lane_name, {}).get("count") == len(boundaries.get(lane_name, {}).get("paths", [])) == count, f"a10p3r2_freeze_file_count_mismatch:{lane_name}")
    require(boundaries.get("mmc_high_risk_policy_configuration", {}).get("separate_human_authorization_required") is True, "a10p3r2_mmc_high_risk_authorization_missing")
    for key in ("product_or_test_implementation", "mmc_policy_or_configuration_change", "live_kds_or_mmc_read", "any_kds_or_mmc_write", "real_authenticated_e2e", "commit", "push", "restart", "deployment", "status_promotion"):
        require(freeze.get("authorization", {}).get(key) is False, f"a10p3r2_freeze_authorization_drift:{key}")

    a10i1_text = read(A10I1_COORDINATION)
    require(hashlib.sha256(a10i1_text.encode("utf-8")).hexdigest() == A10I1_COORDINATION_SHA256, "a10i1_coordination_sha_mismatch")
    a10i1 = yaml.safe_load(a10i1_text).get("release0_first_implementation_amendment", {})
    require(a10i1.get("id") == A10I1_COORDINATION_ID, "a10i1_id_mismatch")
    require(a10i1.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10i1_coordinator_mismatch")
    require(a10i1.get("parent_contract_freeze", {}).get("sha256") == A10P3R2_FREEZE_SHA256, "a10i1_parent_freeze_mismatch")
    require(a10i1.get("canonical", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "a10i1_manifest_mismatch")
    lanes_a10i1 = a10i1.get("parallel_lanes", {})
    require(set(lanes_a10i1) == {"kds", "studio"}, "a10i1_lane_set_mismatch")
    require(lanes_a10i1["kds"].get("thread_id") == LANE_THREADS["kds"], "a10i1_kds_thread_mismatch")
    require(lanes_a10i1["studio"].get("thread_id") == LANE_THREADS["studio"], "a10i1_studio_thread_mismatch")
    require(lanes_a10i1["kds"].get("product_test_file_count") == len(lanes_a10i1["kds"].get("product_test_file_allowlist", [])) == 12, "a10i1_kds_file_count_mismatch")
    require(lanes_a10i1["studio"].get("product_test_file_count") == len(lanes_a10i1["studio"].get("product_test_file_allowlist", [])) == 10, "a10i1_studio_file_count_mismatch")
    require(set(lanes_a10i1["kds"].get("product_test_file_allowlist", ())).isdisjoint(lanes_a10i1["kds"].get("forbidden_scope", ())), "a10i1_kds_scope_overlap")
    require(set(lanes_a10i1["studio"].get("product_test_file_allowlist", ())).isdisjoint(lanes_a10i1["studio"].get("forbidden_scope", ())), "a10i1_studio_scope_overlap")
    for shared_dirty in ("knowledge_intake/repository.py", "knowledge_intake/postgres.py"):
        require(shared_dirty in lanes_a10i1["kds"].get("forbidden_scope", ()), f"a10i1_kds_dirty_shared_not_forbidden:{shared_dirty}")
    require(lanes_a10i1["kds"].get("baseline", {}).get("preexisting_dirty_entries") == 166, "a10i1_kds_dirty_baseline_mismatch")
    require(lanes_a10i1["studio"].get("baseline", {}).get("preexisting_dirty_entries") == 0, "a10i1_studio_dirty_baseline_mismatch")
    require(a10i1.get("frozen_waiting_lanes", {}).get("mmc_standard", {}).get("implementation_authorized") is False, "a10i1_mmc_standard_unexpectedly_authorized")
    require(a10i1.get("frozen_waiting_lanes", {}).get("mmc_high_risk_policy_configuration", {}).get("human_authorization_required") is True, "a10i1_mmc_high_risk_human_gate_missing")
    require(a10i1.get("frozen_waiting_lanes", {}).get("brain", {}).get("observed_preexisting_dirty_entries") == 15, "a10i1_brain_dirty_baseline_mismatch")
    require(a10i1.get("serial_gate", {}).get("requires_both_first_batch_handoffs") is True, "a10i1_two_handoffs_not_required")
    require(a10i1.get("serial_gate", {}).get("automatic_next_lane_start") is False, "a10i1_automatic_next_lane_drift")
    auth_a10i1 = a10i1.get("authorization", {})
    for key in ("GPCF_control_and_governance_record_write", "KDS_allowlisted_local_product_test_openspec_and_evidence_write", "Studio_allowlisted_local_product_test_openspec_and_evidence_write"):
        require(auth_a10i1.get(key) is True, f"a10i1_authorization_missing:{key}")
    for key in ("MMC_standard_implementation", "MMC_policy_or_configuration_change", "Brain_product_or_evidence_write", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "real_authenticated_e2e", "credential_creation_disclosure_or_persistence", "commit", "push", "restart", "deployment", "customer_release", "status_promotion"):
        require(auth_a10i1.get(key) is False, f"a10i1_authorization_drift:{key}")
    require(a10i1.get("status", {}).get("completion") == "not_complete", "a10i1_completion_drift")
    require(a10i1.get("status", {}).get("status_ceiling") == "partial", "a10i1_status_ceiling_drift")

    combined = "\n".join(read(path) for path in (CONTROL_BOARD, SESSION_REGISTRY, PREVIOUS_LOOP_EVIDENCE, A7_LOOP_EVIDENCE, LOOP_EVIDENCE, A9_LOOP_EVIDENCE, A9R1_LOOP_EVIDENCE, A9_ACCEPTANCE_LOOP_EVIDENCE, A10P0_LOOP_EVIDENCE, A10P1_LOOP_EVIDENCE, A10P2_LOOP_EVIDENCE, A10P2_HANDOFF_LOOP_EVIDENCE, A10P3_LOOP_EVIDENCE, A10P3R1_LOOP_EVIDENCE, A10P3R1_HANDOFF_LOOP_EVIDENCE, A10P3R2_LOOP_EVIDENCE, A10P3R2_FREEZE_LOOP_EVIDENCE, A10I1_LOOP_EVIDENCE, A10I1_HANDOFF_LOOP_EVIDENCE, A10I1R1_LOOP_EVIDENCE, A10I1R1_CLOSURE_LOOP_EVIDENCE, A10I2_LOOP_EVIDENCE, A10I2_HANDOFF_LOOP_EVIDENCE, A10I2R1_LOOP_EVIDENCE, A10I2R1_HANDOFF_LOOP_EVIDENCE, A10I2R2_LOOP_EVIDENCE, A10I2R2_HANDOFF_LOOP_EVIDENCE, A10I2R2_CLOSURE_LOOP_EVIDENCE, A10I3P0_LOOP_EVIDENCE, A10I3H1_LOOP_EVIDENCE, A10I3H1_HANDOFF_LOOP_EVIDENCE, A10I3H1R1_LOOP_EVIDENCE, A10I3H1R1_HANDOFF_LOOP_EVIDENCE, A10I3H1R2_LOOP_EVIDENCE, A10I3H1R2_RECONCILIATION_LOOP_EVIDENCE, A10I3H1R2_HANDOFF_LOOP_EVIDENCE, A10I3H1R2R1_LOOP_EVIDENCE, BRAIN_A10P1T3_LOOP_EVIDENCE, A10I3H1R2R2_LOOP_EVIDENCE, STUDIO_A10I1G1_LOOP_EVIDENCE, BRAIN_A10P1T4_LOOP_EVIDENCE, A10P3R2_FREEZE_EVIDENCE, A10I1_DISPATCH_EVIDENCE, A10I1_HANDOFF_REVIEW_EVIDENCE, A10I1R1_DISPATCH_EVIDENCE, A10I1R1_CLOSURE_EVIDENCE, A10I2_DISPATCH_EVIDENCE, A10I2_HANDOFF_REVIEW_EVIDENCE, A10I2R1_DISPATCH_EVIDENCE, A10I2R1_HANDOFF_REVIEW_EVIDENCE, A10I2R2_DISPATCH_EVIDENCE, A10I2R2_HANDOFF_REVIEW_EVIDENCE, A10I2R2_FINAL_CLOSURE_EVIDENCE, A10I3P0_EVIDENCE, A10I3H1_EVIDENCE, A10I3H1_HANDOFF_EVIDENCE, A10I3H1R1_EVIDENCE, A10I3H1R1_HANDOFF_EVIDENCE, A10I3H1R2_EVIDENCE, A10I3H1R2_RECONCILIATION_EVIDENCE, A10I3H1R2_HANDOFF_EVIDENCE, A10I3H1R2R1_EVIDENCE, A10I3H1R2R2_COORDINATION, A10I3H1R2R2_EVIDENCE, A10I3H1R2R3_COORDINATION, A10I3H1R2R3_EVIDENCE, BRAIN_A10P1T3_COORDINATION, BRAIN_A10P1T3_EVIDENCE, BRAIN_A10P1T3_CLOSURE_EVIDENCE, BRAIN_A10P1T4_COORDINATION, BRAIN_A10P1T4_EVIDENCE, BRAIN_A10P1T4R1_COORDINATION, BRAIN_A10P1T4_HANDOFF_EVIDENCE, STUDIO_A10I1G1_COORDINATION, STUDIO_A10I1G1_EVIDENCE, STUDIO_A10I1G1R1_COORDINATION, STUDIO_A10I1G1_CLOSURE_EVIDENCE, SUMMARY, STUDIO_A6_REVIEW, EMERGENCY_AUDIT, A7_REVIEW_A8_DISPATCH, A8_ACCEPTANCE_A9_DISPATCH, A9_REVIEW_A9R1_DISPATCH, A9R1_ACCEPTANCE, A10P0_DISPATCH, A10P0_HANDOFFS, A10P0_REVIEW_A10P1_DISPATCH, A10P1_HANDOFFS, A10P1_REVIEW_A10P2_DISPATCH, A10P2_HANDOFFS, A10P2_REVIEW_A10P3_DISPATCH, A10P3_REPORTS_A10P3R1_DISPATCH, A10P3R1_HANDOFFS))
    for marker in (COORDINATION_ID, COORDINATOR_THREAD, ENVELOPE_SHA256, STUDIO_A4_SHA256, STUDIO_A5_ID, STUDIO_A5_SHA256, STUDIO_A6_ID, STUDIO_A6_SHA256, MINIMAL_PARALLEL_A7_ID, MINIMAL_PARALLEL_A7_SHA256, A7_GOVERNANCE_CLEANUP_A8_ID, A7_GOVERNANCE_CLEANUP_A8_SHA256, A9_READ_ADMISSION_ID, A9_READ_ADMISSION_SHA256, A9_MMC_ROLLBACK_REWORK_ID, A9_MMC_ROLLBACK_REWORK_SHA256, A10_READONLY_PREFLIGHT_ID, A10_READONLY_PREFLIGHT_SHA256, A10P1_COORDINATION_ID, A10P1_COORDINATION_SHA256, A10P2_CANDIDATE_SHA256, A10P2_COORDINATION_ID, A10P2_COORDINATION_SHA256, A10P3_SCHEMA_SHA256, A10P3_COORDINATION_ID, A10P3_COORDINATION_SHA256, A10P3R1_SCHEMA_SHA256, A10P3R1_NORMALIZER_SHA256, A10P3R1_COORDINATION_ID, A10P3R1_COORDINATION_SHA256, A10P3R2_SCHEMA_SHA256, A10P3R2_COORDINATION_ID, A10P3R2_COORDINATION_SHA256, A10P3R2_FREEZE_ID, A10P3R2_FREEZE_SHA256, A10I1_COORDINATION_ID, A10I1_COORDINATION_SHA256, A10I1R1_COORDINATION_ID, A10I1R1_COORDINATION_SHA256, A10I2_COORDINATION_ID, A10I2_COORDINATION_SHA256, A10I2R1_COORDINATION_ID, A10I2R1_COORDINATION_SHA256, A10I2R2_COORDINATION_ID, A10I2R2_COORDINATION_SHA256, A10I3P0_COORDINATION_ID, A10I3P0_COORDINATION_SHA256, A10I3H1_COORDINATION_ID, A10I3H1_COORDINATION_SHA256, A10I3H1R1_COORDINATION_ID, A10I3H1R1_COORDINATION_SHA256, A10I3H1R2_COORDINATION_ID, A10I3H1R2_COORDINATION_SHA256, A10I3H1R2_RECONCILIATION_ID, A10I3H1R2_RECONCILIATION_SHA256, A10I3H1R2R1_COORDINATION_ID, A10I3H1R2R1_COORDINATION_SHA256, BRAIN_A10P1T3_COORDINATION_ID, BRAIN_A10P1T3_COORDINATION_SHA256, BRAIN_A10P1T4_COORDINATION_ID, BRAIN_A10P1T4_COORDINATION_SHA256, A10I3H1R2R2_COORDINATION_ID, A10I3H1R2R2_COORDINATION_SHA256, A10I3H1R2R3_COORDINATION_ID, A10I3H1R2R3_COORDINATION_SHA256, STUDIO_A10I1G1_COORDINATION_ID, STUDIO_A10I1G1_COORDINATION_SHA256, STUDIO_A10I1G1R1_COORDINATION_ID, STUDIO_A10I1G1R1_COORDINATION_SHA256, *LANE_THREADS.values()):
        require(marker in combined, f"governance_marker_missing:{marker}")
    feature = yaml.safe_load(read(FEATURE))
    require(feature.get("coordination", {}).get("id") == COORDINATION_ID, "feature_coordination_missing")
    require(feature.get("status") == "active", "feature_status_mismatch")
    require(feature.get("ui_product_first_control", {}).get("status_ceiling") == "partial", "feature_status_ceiling_mismatch")
    blockers = set(feature.get("blockers") or ())
    for blocker in (
        "kds_stage_b_read_admission_technical_verified_governance_blocked",
        "studio_intake_phase1_authorized_phase2_blocked_by_mmc_prepare_retry_policy_review",
        "studio_a6_external_daily_sync_commit_push_requires_governance_disposition",
        "unexpected_external_kds_local_mirror_write_requires_review",
        "brain_authenticated_readonly_e2e_deferred_pending_a10_control",
        "mmc_a9_bounded_read_subset_technical_verified_global_policy_not_narrowed",
        "mmc_delegation_and_human_confirmation_pending",
    ):
        require(blocker in blockers, f"feature_blocker_missing:{blocker}")
    require(feature.get("loop", {}).get("iteration", 0) >= 38, "feature_iteration_reconciliation_missing")
    require(feature.get("coordination", {}).get("studio_intake_amendment") == str(STUDIO_A4.relative_to(ROOT)), "studio_a4_feature_path_missing")
    require(feature.get("coordination", {}).get("studio_intake_amendment_sha256") == STUDIO_A4_SHA256, "studio_a4_feature_sha_missing")
    require(feature.get("coordination", {}).get("studio_intake_reconciliation") == str(STUDIO_A5.relative_to(ROOT)), "studio_a5_feature_path_missing")
    require(feature.get("coordination", {}).get("studio_intake_reconciliation_sha256") == STUDIO_A5_SHA256, "studio_a5_feature_sha_missing")
    require(feature.get("coordination", {}).get("studio_intake_rework_amendment") == str(STUDIO_A6.relative_to(ROOT)), "studio_a6_feature_path_missing")
    require(feature.get("coordination", {}).get("studio_intake_rework_amendment_sha256") == STUDIO_A6_SHA256, "studio_a6_feature_sha_missing")
    require(feature.get("coordination", {}).get("minimal_parallel_unfreeze_amendment") == str(MINIMAL_PARALLEL_A7.relative_to(ROOT)), "minimal_parallel_a7_feature_path_missing")
    require(feature.get("coordination", {}).get("minimal_parallel_unfreeze_amendment_sha256") == MINIMAL_PARALLEL_A7_SHA256, "minimal_parallel_a7_feature_sha_missing")
    require(feature.get("coordination", {}).get("a7_governance_cleanup_rework_amendment") == str(A7_GOVERNANCE_CLEANUP_A8.relative_to(ROOT)), "a7_governance_cleanup_a8_feature_path_missing")
    require(feature.get("coordination", {}).get("a7_governance_cleanup_rework_amendment_sha256") == A7_GOVERNANCE_CLEANUP_A8_SHA256, "a7_governance_cleanup_a8_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_mmc_read_admission_amendment") == str(A9_READ_ADMISSION.relative_to(ROOT)), "a9_read_admission_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_mmc_read_admission_amendment_sha256") == A9_READ_ADMISSION_SHA256, "a9_read_admission_feature_sha_missing")
    require(feature.get("coordination", {}).get("a9_mmc_rollback_handoff_rework") == str(A9_MMC_ROLLBACK_REWORK.relative_to(ROOT)), "a9r1_feature_path_missing")
    require(feature.get("coordination", {}).get("a9_mmc_rollback_handoff_rework_sha256") == A9_MMC_ROLLBACK_REWORK_SHA256, "a9r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10_readonly_preflight") == str(A10_READONLY_PREFLIGHT.relative_to(ROOT)), "a10p0_feature_path_missing")
    require(feature.get("coordination", {}).get("a10_readonly_preflight_sha256") == A10_READONLY_PREFLIGHT_SHA256, "a10p0_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p1_contract_convergence") == str(A10P1_COORDINATION.relative_to(ROOT)), "a10p1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p1_contract_convergence_sha256") == A10P1_COORDINATION_SHA256, "a10p1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p2_candidate_contract") == str(A10P2_CANDIDATE.relative_to(ROOT)), "a10p2_candidate_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p2_candidate_contract_sha256") == A10P2_CANDIDATE_SHA256, "a10p2_candidate_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p2_joint_contract_freeze") == str(A10P2_COORDINATION.relative_to(ROOT)), "a10p2_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p2_joint_contract_freeze_sha256") == A10P2_COORDINATION_SHA256, "a10p2_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3_field_schema_candidate") == str(A10P3_SCHEMA.relative_to(ROOT)), "a10p3_schema_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3_field_schema_candidate_sha256") == A10P3_SCHEMA_SHA256, "a10p3_schema_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3_field_schema_freeze") == str(A10P3_COORDINATION.relative_to(ROOT)), "a10p3_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3_field_schema_freeze_sha256") == A10P3_COORDINATION_SHA256, "a10p3_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3r1_field_schema_candidate") == str(A10P3R1_SCHEMA.relative_to(ROOT)), "a10p3r1_schema_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3r1_field_schema_candidate_sha256") == A10P3R1_SCHEMA_SHA256, "a10p3r1_schema_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3r1_field_schema_rework") == str(A10P3R1_COORDINATION.relative_to(ROOT)), "a10p3r1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3r1_field_schema_rework_sha256") == A10P3R1_COORDINATION_SHA256, "a10p3r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3r1_normalizer") == str(A10P3R1_NORMALIZER.relative_to(ROOT)), "a10p3r1_normalizer_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3r1_normalizer_sha256") == A10P3R1_NORMALIZER_SHA256, "a10p3r1_normalizer_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3r2_reconciled_schema") == str(A10P3R2_SCHEMA.relative_to(ROOT)), "a10p3r2_schema_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3r2_reconciled_schema_sha256") == A10P3R2_SCHEMA_SHA256, "a10p3r2_schema_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10p3r2_metadata_reconciliation") == str(A10P3R2_COORDINATION.relative_to(ROOT)), "a10p3r2_coordination_feature_path_missing")
    require(feature.get("coordination", {}).get("a10p3r2_metadata_reconciliation_sha256") == A10P3R2_COORDINATION_SHA256, "a10p3r2_coordination_feature_sha_missing")
    require(feature.get("coordination", {}).get("release0_canonical_read_contract_freeze") == str(A10P3R2_FREEZE.relative_to(ROOT)), "a10p3r2_freeze_feature_path_missing")
    require(feature.get("coordination", {}).get("release0_canonical_read_contract_freeze_sha256") == A10P3R2_FREEZE_SHA256, "a10p3r2_freeze_feature_sha_missing")
    require(feature.get("coordination", {}).get("release0_first_implementation_amendment") == str(A10I1_COORDINATION.relative_to(ROOT)), "a10i1_feature_path_missing")
    require(feature.get("coordination", {}).get("release0_first_implementation_amendment_sha256") == A10I1_COORDINATION_SHA256, "a10i1_feature_sha_missing")
    require(hashlib.sha256(read(A10I1R1_COORDINATION).encode("utf-8")).hexdigest() == A10I1R1_COORDINATION_SHA256, "a10i1r1_coordination_sha_mismatch")
    a10i1r1 = yaml.safe_load(read(A10I1R1_COORDINATION)).get("a10i1_joint_review_rework", {})
    require(a10i1r1.get("id") == A10I1R1_COORDINATION_ID, "a10i1r1_id_mismatch")
    require(a10i1r1.get("parent_control", {}).get("sha256") == A10I1_COORDINATION_SHA256, "a10i1r1_parent_mismatch")
    require(len(a10i1r1.get("parallel_rework_lanes", {}).get("studio", {}).get("product_test_file_allowlist", [])) == 2, "a10i1r1_studio_scope_mismatch")
    require(a10i1r1.get("parallel_rework_lanes", {}).get("kds", {}).get("product_test_file_allowlist") == [], "a10i1r1_kds_product_scope_not_empty")
    require(feature.get("coordination", {}).get("a10i1_joint_review_rework") == str(A10I1R1_COORDINATION.relative_to(ROOT)), "a10i1r1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i1_joint_review_rework_sha256") == A10I1R1_COORDINATION_SHA256, "a10i1r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i1_joint_serial_gate_evidence") == str(A10I1R1_CLOSURE_EVIDENCE.relative_to(ROOT)), "a10i1r1_closure_feature_path_missing")
    a10i2_text = read(A10I2_COORDINATION)
    require(hashlib.sha256(a10i2_text.encode("utf-8")).hexdigest() == A10I2_COORDINATION_SHA256, "a10i2_coordination_sha_mismatch")
    a10i2 = yaml.safe_load(a10i2_text).get("release0_mmc_standard_implementation_amendment", {})
    require(a10i2.get("id") == A10I2_COORDINATION_ID, "a10i2_id_mismatch")
    require(a10i2.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "a10i2_coordinator_mismatch")
    require(a10i2.get("parent_controls", {}).get("serial_gate") == "closed", "a10i2_parent_serial_gate_not_closed")
    require(a10i2.get("contract_freeze", {}).get("sha256") == A10P3R2_FREEZE_SHA256, "a10i2_freeze_mismatch")
    a10i2_lane = a10i2.get("lane", {})
    require(a10i2_lane.get("thread_id") == LANE_THREADS["studio"], "a10i2_thread_mismatch")
    require(a10i2_lane.get("baseline", {}).get("dirty_entries") == 0, "a10i2_baseline_not_clean")
    require(a10i2_lane.get("product_test_file_count") == len(a10i2_lane.get("product_test_file_allowlist", [])) == 6, "a10i2_file_count_mismatch")
    for forbidden in ("runtime/scripts/seed.sh", "runtime/state.json", "runtime/app/core/delegation.py", "runtime/app/core/kds_delegation.py"):
        require(forbidden in a10i2_lane.get("forbidden_scope", ()), f"a10i2_high_risk_scope_not_forbidden:{forbidden}")
    a10i2_auth = a10i2.get("authorization", {})
    require(a10i2_auth.get("local_allowlisted_product_test_openspec_and_evidence_write") is True, "a10i2_local_write_not_authorized")
    for key in ("runtime_registry_or_policy_change", "live_KDS_or_MMC_read", "any_KDS_or_MMC_write", "credentials", "commit", "push", "restart", "deployment", "customer_release", "status_promotion"):
        require(a10i2_auth.get(key) is False, f"a10i2_authorization_drift:{key}")
    require(a10i2.get("serial_gate", {}).get("automatic_next_lane_start") is False, "a10i2_automatic_next_lane_drift")
    require(a10i2.get("status", {}).get("completion") == "not_complete", "a10i2_completion_drift")
    require(feature.get("coordination", {}).get("release0_mmc_standard_implementation_amendment") == str(A10I2_COORDINATION.relative_to(ROOT)), "a10i2_feature_path_missing")
    require(feature.get("coordination", {}).get("release0_mmc_standard_implementation_amendment_sha256") == A10I2_COORDINATION_SHA256, "a10i2_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i2_mmc_dispatch_evidence") == str(A10I2_DISPATCH_EVIDENCE.relative_to(ROOT)), "a10i2_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i2_mmc_handoff_review_evidence") == str(A10I2_HANDOFF_REVIEW_EVIDENCE.relative_to(ROOT)), "a10i2_handoff_review_evidence_path_missing")
    a10i2_handoff_text = read(A10I2_HANDOFF_REVIEW_EVIDENCE)
    for receipt in ("8/8", "103", "a7ebcef4ad5c4b87e78973174c6915ca34bad56b629c31efb07c46c305427270", "lock absent"):
        require(receipt in a10i2_handoff_text, f"a10i2_handoff_receipt_missing:{receipt}")
    a10i2r1_text = read(A10I2R1_COORDINATION)
    require(hashlib.sha256(a10i2r1_text.encode("utf-8")).hexdigest() == A10I2R1_COORDINATION_SHA256, "a10i2r1_coordination_sha_mismatch")
    a10i2r1 = yaml.safe_load(a10i2r1_text).get("a10i2_mmc_targeted_rework", {})
    require(a10i2r1.get("id") == A10I2R1_COORDINATION_ID, "a10i2r1_id_mismatch")
    require(a10i2r1.get("parent_control", {}).get("sha256") == A10I2_COORDINATION_SHA256, "a10i2r1_parent_mismatch")
    require(a10i2r1.get("independent_review", {}).get("classification") == "technical_rework_required_handoff_not_accepted", "a10i2r1_review_classification_missing")
    require(len(a10i2r1.get("independent_review", {}).get("findings", [])) == 4, "a10i2r1_finding_count_mismatch")
    a10i2r1_lane = a10i2r1.get("lane", {})
    require(a10i2r1_lane.get("product_test_file_count") == len(a10i2r1_lane.get("product_test_file_allowlist", [])) == 6, "a10i2r1_file_count_mismatch")
    for forbidden in ("runtime/scripts/contract_test.py", "runtime/scripts/seed.sh", "runtime/state.json", "runtime/app/core/delegation.py", "runtime/app/core/kds_delegation.py"):
        require(forbidden in a10i2r1_lane.get("forbidden_scope", ()), f"a10i2r1_forbidden_scope_missing:{forbidden}")
    require(a10i2r1.get("serial_gate", {}).get("automatic_next_lane_start") is False, "a10i2r1_automatic_next_lane_drift")
    require(a10i2r1.get("authorization", {}).get("runtime_registry_or_policy_change") is False, "a10i2r1_policy_authorization_drift")
    require(feature.get("coordination", {}).get("a10i2_mmc_targeted_rework") == str(A10I2R1_COORDINATION.relative_to(ROOT)), "a10i2r1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i2_mmc_targeted_rework_sha256") == A10I2R1_COORDINATION_SHA256, "a10i2r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i2_independent_review_and_rework_dispatch_evidence") == str(A10I2R1_DISPATCH_EVIDENCE.relative_to(ROOT)), "a10i2r1_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i2r1_handoff_re_review_evidence") == str(A10I2R1_HANDOFF_REVIEW_EVIDENCE.relative_to(ROOT)), "a10i2r1_handoff_evidence_path_missing")
    a10i2r1_handoff_text = read(A10I2R1_HANDOFF_REVIEW_EVIDENCE)
    for receipt in ("15/15", "109", "ad18f0340e8ff5269bfd6d1454f155419e7514990cf7c475e2f6e55eea7c0447", "lock absent"):
        require(receipt in a10i2r1_handoff_text, f"a10i2r1_handoff_receipt_missing:{receipt}")
    a10i2r2_text = read(A10I2R2_COORDINATION)
    require(hashlib.sha256(a10i2r2_text.encode("utf-8")).hexdigest() == A10I2R2_COORDINATION_SHA256, "a10i2r2_coordination_sha_mismatch")
    a10i2r2 = yaml.safe_load(a10i2r2_text).get("a10i2r2_mmc_response_schema_rework", {})
    require(a10i2r2.get("id") == A10I2R2_COORDINATION_ID, "a10i2r2_id_mismatch")
    require(a10i2r2.get("parent_control", {}).get("sha256") == A10I2R1_COORDINATION_SHA256, "a10i2r2_parent_mismatch")
    require(a10i2r2.get("lane", {}).get("product_test_file_count") == len(a10i2r2.get("lane", {}).get("product_test_file_allowlist", [])) == 2, "a10i2r2_file_count_mismatch")
    require("runtime/app/api/v1/connectors.py" in a10i2r2.get("lane", {}).get("forbidden_scope", ()), "a10i2r2_runtime_not_frozen")
    require(a10i2r2.get("serial_gate", {}).get("automatic_next_lane_start") is False, "a10i2r2_automatic_next_lane_drift")
    require(feature.get("coordination", {}).get("a10i2r2_mmc_response_schema_rework") == str(A10I2R2_COORDINATION.relative_to(ROOT)), "a10i2r2_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i2r2_mmc_response_schema_rework_sha256") == A10I2R2_COORDINATION_SHA256, "a10i2r2_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i2r1_review_and_a10i2r2_dispatch_evidence") == str(A10I2R2_DISPATCH_EVIDENCE.relative_to(ROOT)), "a10i2r2_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i2r2_handoff_review_evidence") == str(A10I2R2_HANDOFF_REVIEW_EVIDENCE.relative_to(ROOT)), "a10i2r2_handoff_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i2r2_final_review_closure_evidence") == str(A10I2R2_FINAL_CLOSURE_EVIDENCE.relative_to(ROOT)), "a10i2r2_closure_evidence_path_missing")
    a10i2r2_handoff_text = read(A10I2R2_HANDOFF_REVIEW_EVIDENCE)
    for receipt in (
        "9 passed, 1 deselected",
        "114 passed",
        "d8eb4b2094e48fbf1d3d2d06d8a14cd25e587c6b5a19522450664fbc8789bfac",
        "OpsX lock is absent",
    ):
        require(receipt in a10i2r2_handoff_text, f"a10i2r2_handoff_receipt_missing:{receipt}")
    a10i2r2_closure_text = read(A10I2R2_FINAL_CLOSURE_EVIDENCE)
    require("independent_technical_rereview_passed_schema_and_mocked_contract_only" in a10i2r2_closure_text, "a10i2r2_closure_classification_missing")
    require("does not apply MMC policy" in a10i2r2_closure_text, "a10i2r2_policy_boundary_missing")
    a10i3p0_text = read(A10I3P0_COORDINATION)
    require(hashlib.sha256(a10i3p0_text.encode("utf-8")).hexdigest() == A10I3P0_COORDINATION_SHA256, "a10i3p0_coordination_sha_mismatch")
    a10i3p0 = yaml.safe_load(a10i3p0_text).get("a10i3_mmc_policy_apply_safety_preflight", {})
    require(a10i3p0.get("id") == A10I3P0_COORDINATION_ID, "a10i3p0_id_mismatch")
    require(a10i3p0.get("mode") == "report_only_authorization_preflight", "a10i3p0_mode_drift")
    require(a10i3p0.get("repository_allowlist") == [], "a10i3p0_repository_write_authorized")
    require(a10i3p0.get("runtime_write_allowlist") == [], "a10i3p0_runtime_write_authorized")
    require(a10i3p0.get("current_policy", {}).get("delegated_operations_sha256") == MMC_RESTORE_FINGERPRINT, "a10i3p0_current_fingerprint_mismatch")
    require(a10i3p0.get("proposed_delta", {}).get("isolated_two_operation_sha256") == MMC_CANDIDATE_FINGERPRINT, "a10i3p0_isolated_fingerprint_mismatch")
    require(a10i3p0.get("proposed_delta", {}).get("target_delegated_operations_sha256") == "e99be2c0ae3c9c3c5544352ef1c679a4dc67fdddc816a5546ffe7bd97370d0c2", "a10i3p0_target_fingerprint_mismatch")
    require(a10i3p0.get("proposed_delta", {}).get("target_operation_count") == 19, "a10i3p0_target_count_mismatch")
    require(all(tranche.get("authorization_state") != "authorized" for tranche in a10i3p0.get("proposed_serial_tranches", [])), "a10i3p0_tranche_authorized")
    require("execute_seed_force" in a10i3p0.get("forbidden_actions", ()), "a10i3p0_seed_force_not_forbidden")
    require(feature.get("coordination", {}).get("a10i3p0_mmc_policy_safety_preflight") == str(A10I3P0_COORDINATION.relative_to(ROOT)), "a10i3p0_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3p0_mmc_policy_safety_preflight_sha256") == A10I3P0_COORDINATION_SHA256, "a10i3p0_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3p0_preflight_evidence") == str(A10I3P0_EVIDENCE.relative_to(ROOT)), "a10i3p0_evidence_path_missing")
    a10i3h1_text = read(A10I3H1_COORDINATION)
    require(hashlib.sha256(a10i3h1_text.encode("utf-8")).hexdigest() == A10I3H1_COORDINATION_SHA256, "a10i3h1_coordination_sha_mismatch")
    a10i3h1 = yaml.safe_load(a10i3h1_text).get("a10i3h1_mmc_policy_mutation_hardening", {})
    require(a10i3h1.get("id") == A10I3H1_COORDINATION_ID, "a10i3h1_id_mismatch")
    require(a10i3h1.get("parent_control", {}).get("sha256") == A10I3P0_COORDINATION_SHA256, "a10i3h1_parent_mismatch")
    require(a10i3h1.get("lane", {}).get("product_test_file_count") == len(a10i3h1.get("lane", {}).get("product_test_file_allowlist", [])) == 4, "a10i3h1_file_count_mismatch")
    require(a10i3h1.get("frozen_policy_lineage", {}).get("current_delegated_operations_sha256") == MMC_RESTORE_FINGERPRINT, "a10i3h1_current_fingerprint_mismatch")
    require(a10i3h1.get("frozen_policy_lineage", {}).get("isolated_two_operation_sha256") == MMC_CANDIDATE_FINGERPRINT, "a10i3h1_isolated_fingerprint_mismatch")
    require(a10i3h1.get("frozen_policy_lineage", {}).get("future_target_delegated_operations_sha256") == "e99be2c0ae3c9c3c5544352ef1c679a4dc67fdddc816a5546ffe7bd97370d0c2", "a10i3h1_target_fingerprint_mismatch")
    require(a10i3h1.get("frozen_policy_lineage", {}).get("policy_delta_authorized") is False, "a10i3h1_policy_delta_authorized")
    require(a10i3h1.get("mutation_boundary", {}).get("compare_and_swap", {}).get("header") == "If-Match", "a10i3h1_cas_header_drift")
    require(set(a10i3h1.get("mutation_boundary", {}).get("allowed_direct_roles", ())) == {"admin", "super_admin"}, "a10i3h1_role_gate_drift")
    require(a10i3h1.get("authorization", {}).get("runtime_registry_or_policy_change") is False, "a10i3h1_runtime_policy_authorized")
    require(a10i3h1.get("serial_gate", {}).get("H2_seed_delta") is False, "a10i3h1_h2_unfrozen")
    require(a10i3h1.get("serial_gate", {}).get("H3_runtime_policy_apply") is False, "a10i3h1_h3_unfrozen")
    require("runtime/scripts/seed.sh" in a10i3h1.get("forbidden_scope", ()), "a10i3h1_seed_not_forbidden")
    require("runtime/state.json" in a10i3h1.get("forbidden_scope", ()), "a10i3h1_state_not_forbidden")
    require(feature.get("coordination", {}).get("a10i3h1_mmc_policy_mutation_hardening") == str(A10I3H1_COORDINATION.relative_to(ROOT)), "a10i3h1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1_mmc_policy_mutation_hardening_sha256") == A10I3H1_COORDINATION_SHA256, "a10i3h1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3p0_review_a10i3h1_dispatch_evidence") == str(A10I3H1_EVIDENCE.relative_to(ROOT)), "a10i3h1_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1_handoff_review_evidence") == str(A10I3H1_HANDOFF_EVIDENCE.relative_to(ROOT)), "a10i3h1_handoff_evidence_path_missing")
    a10i3h1_handoff_text = read(A10I3H1_HANDOFF_EVIDENCE)
    require("21 passed, 35 deselected" in a10i3h1_handoff_text, "a10i3h1_focused_receipt_missing")
    require("129 passed" in a10i3h1_handoff_text, "a10i3h1_full_receipt_missing")
    require("24a9886ac9bd2d01024b51f331df51cec89d55eca234b9f789f1a12581b11e51" in a10i3h1_handoff_text, "a10i3h1_patch_receipt_missing")
    require("old_policy_effective=false" in a10i3h1_handoff_text and "target_policy_effective=true" in a10i3h1_handoff_text, "a10i3h1_restore_failure_reproduction_missing")
    require("ordinary_update_preserved=false" in a10i3h1_handoff_text, "a10i3h1_concurrent_update_reproduction_missing")
    a10i3h1r1_text = read(A10I3H1R1_COORDINATION)
    require(hashlib.sha256(a10i3h1r1_text.encode("utf-8")).hexdigest() == A10I3H1R1_COORDINATION_SHA256, "a10i3h1r1_coordination_sha_mismatch")
    a10i3h1r1 = yaml.safe_load(a10i3h1r1_text).get("a10i3h1r1_mmc_policy_mutation_safety_rework", {})
    require(a10i3h1r1.get("id") == A10I3H1R1_COORDINATION_ID, "a10i3h1r1_id_mismatch")
    require(a10i3h1r1.get("parent_control", {}).get("sha256") == A10I3H1_COORDINATION_SHA256, "a10i3h1r1_parent_mismatch")
    require(a10i3h1r1.get("independent_review", {}).get("classification") == "technical_rework_required", "a10i3h1r1_review_classification_mismatch")
    require(a10i3h1r1.get("lane", {}).get("product_test_file_count") == len(a10i3h1r1.get("lane", {}).get("product_test_file_allowlist", [])) == 4, "a10i3h1r1_file_count_mismatch")
    require(a10i3h1r1.get("required_design", {}).get("state_lock", {}).get("requirement") == "stable_cross_process_lock_for_exact_STATE_PATH", "a10i3h1r1_cross_process_lock_missing")
    require(a10i3h1r1.get("required_design", {}).get("durable_recovery", {}).get("repeated_restore_failure") == "retain_recovery_intent_and_make_all_registry_reads_and_writes_fail_closed", "a10i3h1r1_recovery_boundary_missing")
    require(a10i3h1r1.get("required_design", {}).get("audit_append", {}).get("requirement") == "one_complete_valid_JSONL_record_or_zero_new_bytes", "a10i3h1r1_audit_boundary_missing")
    require(a10i3h1r1.get("authorization", {}).get("runtime_registry_or_policy_change") is False, "a10i3h1r1_runtime_policy_authorized")
    require(a10i3h1r1.get("serial_gate", {}).get("H2_seed_delta") is False and a10i3h1r1.get("serial_gate", {}).get("H3_runtime_policy_apply") is False, "a10i3h1r1_high_risk_gate_unfrozen")
    require(feature.get("coordination", {}).get("a10i3h1r1_mmc_policy_safety_rework") == str(A10I3H1R1_COORDINATION.relative_to(ROOT)), "a10i3h1r1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r1_mmc_policy_safety_rework_sha256") == A10I3H1R1_COORDINATION_SHA256, "a10i3h1r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3h1_review_a10i3h1r1_dispatch_evidence") == str(A10I3H1R1_EVIDENCE.relative_to(ROOT)), "a10i3h1r1_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r1_handoff_review_evidence") == str(A10I3H1R1_HANDOFF_EVIDENCE.relative_to(ROOT)), "a10i3h1r1_handoff_evidence_path_missing")
    a10i3h1r1_handoff_text = read(A10I3H1R1_HANDOFF_EVIDENCE)
    require("66 passed" in a10i3h1r1_handoff_text and "139 passed" in a10i3h1r1_handoff_text, "a10i3h1r1_test_receipts_missing")
    require("491b9aab7611c2c90403ab1c395e1953b9fe9fd1ecf9c9883b708c3c06421531" in a10i3h1r1_handoff_text, "a10i3h1r1_patch_receipt_missing")
    require("guarded_create_interleaving=pass" in a10i3h1r1_handoff_text and "guarded_delete_interleaving=pass" in a10i3h1r1_handoff_text, "a10i3h1r1_extra_interleaving_receipt_missing")
    a10i3h1r2_text = read(A10I3H1R2_COORDINATION)
    require(hashlib.sha256(a10i3h1r2_text.encode("utf-8")).hexdigest() == A10I3H1R2_COORDINATION_SHA256, "a10i3h1r2_coordination_sha_mismatch")
    a10i3h1r2 = yaml.safe_load(a10i3h1r2_text).get("a10i3h1r2_mmc_shared_registry_state_rework", {})
    require(a10i3h1r2.get("id") == A10I3H1R2_COORDINATION_ID, "a10i3h1r2_id_mismatch")
    require(a10i3h1r2.get("parent_control", {}).get("sha256") == A10I3H1R1_COORDINATION_SHA256, "a10i3h1r2_parent_mismatch")
    require(a10i3h1r2.get("coordinator_replay", {}).get("classification") == "technical_rework_required", "a10i3h1r2_classification_mismatch")
    require(a10i3h1r2.get("lane", {}).get("product_test_file_count") == len(a10i3h1r2.get("lane", {}).get("product_test_file_allowlist", [])) == 8, "a10i3h1r2_file_count_mismatch")
    require(a10i3h1r2.get("required_design", {}).get("shared_state_boundary", {}).get("single_primitive_owner") == "runtime/app/gateway/registry_state.py", "a10i3h1r2_shared_owner_missing")
    require(a10i3h1r2.get("authorization", {}).get("runtime_registry_or_policy_change") is False, "a10i3h1r2_runtime_policy_authorized")
    require(a10i3h1r2.get("serial_gate", {}).get("H2_seed_delta") is False and a10i3h1r2.get("serial_gate", {}).get("H3_runtime_policy_apply") is False, "a10i3h1r2_high_risk_gate_unfrozen")
    require(feature.get("coordination", {}).get("a10i3h1r2_mmc_shared_registry_state_rework") == str(A10I3H1R2_COORDINATION.relative_to(ROOT)), "a10i3h1r2_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_mmc_shared_registry_state_rework_sha256") == A10I3H1R2_COORDINATION_SHA256, "a10i3h1r2_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3h1r1_coordinator_replay_a10i3h1r2_dispatch_evidence") == str(A10I3H1R2_EVIDENCE.relative_to(ROOT)), "a10i3h1r2_evidence_path_missing")
    reconciliation_text = read(A10I3H1R2_RECONCILIATION)
    require(hashlib.sha256(reconciliation_text.encode("utf-8")).hexdigest() == A10I3H1R2_RECONCILIATION_SHA256, "a10i3h1r2_reconciliation_sha_mismatch")
    reconciliation = yaml.safe_load(reconciliation_text).get("a10i3h1r2_mmc_baseline_reconciliation", {})
    require(reconciliation.get("id") == A10I3H1R2_RECONCILIATION_ID, "a10i3h1r2_reconciliation_id_mismatch")
    require(reconciliation.get("parent_control", {}).get("sha256") == A10I3H1R2_COORDINATION_SHA256, "a10i3h1r2_reconciliation_parent_mismatch")
    require(reconciliation.get("amended_baseline", {}).get("head") == A10I3H1R2_RECONCILED_BASELINE, "a10i3h1r2_reconciled_head_mismatch")
    require(reconciliation.get("amended_baseline", {}).get("origin_main") == A10I3H1R2_RECONCILED_BASELINE, "a10i3h1r2_reconciled_origin_mismatch")
    require(reconciliation.get("content_continuity", {}).get("all_existing_allowlist_hashes_equal_parent_baseline") is True, "a10i3h1r2_hash_continuity_missing")
    require(reconciliation.get("content_continuity", {}).get("new_shared_module_still_absent") is True, "a10i3h1r2_new_module_baseline_drift")
    require(reconciliation.get("authorization", {}).get("accept_or_ratify_external_commit_push") is False, "a10i3h1r2_external_commit_ratified")
    require(reconciliation.get("authorization", {}).get("additional_commit_or_push") is False, "a10i3h1r2_additional_git_authorized")
    require(feature.get("coordination", {}).get("a10i3h1r2_mmc_baseline_reconciliation") == str(A10I3H1R2_RECONCILIATION.relative_to(ROOT)), "a10i3h1r2_reconciliation_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_mmc_baseline_reconciliation_sha256") == A10I3H1R2_RECONCILIATION_SHA256, "a10i3h1r2_reconciliation_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_mmc_baseline_reconciliation_evidence") == str(A10I3H1R2_RECONCILIATION_EVIDENCE.relative_to(ROOT)), "a10i3h1r2_reconciliation_evidence_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_handoff_review_evidence") == str(A10I3H1R2_HANDOFF_EVIDENCE.relative_to(ROOT)), "a10i3h1r2_handoff_evidence_path_missing")
    a10i3h1r2_evidence_text = read(A10I3H1R2_EVIDENCE)
    require("unresolved_recovery_connector_exposes_target=true" in a10i3h1r2_evidence_text, "a10i3h1r2_connector_reproduction_missing")
    require("llm_update_lost=true" in a10i3h1r2_evidence_text, "a10i3h1r2_llm_reproduction_missing")
    a10i3h1r2_handoff_text = read(A10I3H1R2_HANDOFF_EVIDENCE)
    for marker in ("75 passed", "146 passed", "d5083a534e0daf0342a54dfba4992867574650df442b11709109d2ab475a6938", "40a674577b73422c98936a69efd1b3a317d1999d5a44dfd0b4635842067c0a5e", "handoff_received_f013_review_pending"):
        require(marker in a10i3h1r2_handoff_text, f"a10i3h1r2_handoff_marker_missing:{marker}")
    a10i3h1r2r1_text = read(A10I3H1R2R1_COORDINATION)
    require(hashlib.sha256(a10i3h1r2r1_text.encode("utf-8")).hexdigest() == A10I3H1R2R1_COORDINATION_SHA256, "a10i3h1r2r1_coordination_sha_mismatch")
    a10i3h1r2r1 = yaml.safe_load(a10i3h1r2r1_text).get("a10i3h1r2_coordinator_review_blocker", {})
    require(a10i3h1r2r1.get("id") == A10I3H1R2R1_COORDINATION_ID, "a10i3h1r2r1_id_mismatch")
    require(a10i3h1r2r1.get("finding", {}).get("observed", {}).get("resolved_state_equal") is True, "a10i3h1r2r1_resolved_identity_missing")
    require(a10i3h1r2r1.get("finding", {}).get("observed", {}).get("lock_path_equal") is False, "a10i3h1r2r1_lock_alias_not_reproduced")
    require(a10i3h1r2r1.get("finding", {}).get("observed", {}).get("second_process_acquired_while_first_held") is True, "a10i3h1r2r1_cross_process_bypass_missing")
    require(a10i3h1r2r1.get("proposed_h1r3_scope", {}).get("implementation_authorized") is False, "a10i3h1r3_implementation_unexpectedly_authorized")
    require(a10i3h1r2r1.get("proposed_h1r3_scope", {}).get("product_test_file_count") == len(a10i3h1r2r1.get("proposed_h1r3_scope", {}).get("product_test_file_allowlist", [])) == 4, "a10i3h1r3_proposed_file_count_mismatch")
    require(a10i3h1r2r1.get("serial_gate", {}).get("f013_independent_confirmation_required") is True, "a10i3h1r2r1_f013_gate_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_coordinator_review_blocker") == str(A10I3H1R2R1_COORDINATION.relative_to(ROOT)), "a10i3h1r2r1_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_coordinator_review_blocker_sha256") == A10I3H1R2R1_COORDINATION_SHA256, "a10i3h1r2r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_coordinator_readonly_replay_evidence") == str(A10I3H1R2R1_EVIDENCE.relative_to(ROOT)), "a10i3h1r2r1_evidence_path_missing")
    a10i3h1r2r1_evidence_text = read(A10I3H1R2R1_EVIDENCE)
    for marker in ("resolved_state_equal=True", "lock_path_equal=False", "second_process_acquired_while_first_held=True", "953d4d1baea201cc0fc822074bc74cad9299d0dd", "925659b0144a5fb858a78cf32c1d8ddf6967c19b"):
        require(marker in a10i3h1r2r1_evidence_text, f"a10i3h1r2r1_evidence_marker_missing:{marker}")
    a10i3h1r2r2_text = read(A10I3H1R2R2_COORDINATION)
    require(hashlib.sha256(a10i3h1r2r2_text.encode("utf-8")).hexdigest() == A10I3H1R2R2_COORDINATION_SHA256, "a10i3h1r2r2_coordination_sha_mismatch")
    a10i3h1r2r2 = yaml.safe_load(a10i3h1r2r2_text).get("a10i3h1r2_secondary_review_scope_correction", {})
    require(a10i3h1r2r2.get("id") == A10I3H1R2R2_COORDINATION_ID, "a10i3h1r2r2_id_mismatch")
    require(a10i3h1r2r2.get("reviewer", {}).get("type") == "secondary_independent_technical_reviewer_not_canonical_f013_authority", "a10i3h1r2r2_authority_boundary_missing")
    require(a10i3h1r2r2.get("canonical_reviewer", {}).get("decision_received") is False, "a10i3h1r2r2_unexpected_canonical_decision")
    corrected_scope = a10i3h1r2r2.get("corrected_future_h1r3_scope", {})
    require(corrected_scope.get("implementation_authorized") is False, "a10i3h1r3_implementation_unexpectedly_authorized")
    require(corrected_scope.get("product_test_file_count") == len(corrected_scope.get("product_test_file_allowlist", [])) == 6, "a10i3h1r3_product_test_file_count_mismatch")
    require(corrected_scope.get("specification_file_count") == len(corrected_scope.get("specification_file_allowlist", [])) == 3, "a10i3h1r3_specification_file_count_mismatch")
    require(corrected_scope.get("total_implementation_and_specification_paths") == 9, "a10i3h1r3_total_path_count_mismatch")
    require("scripts/dry_run_mmc_dependencies.py" in corrected_scope.get("product_test_file_allowlist", []), "a10i3h1r3_dependency_dry_run_missing")
    require("runtime/tests/test_dependency_dry_run.py" in corrected_scope.get("product_test_file_allowlist", []), "a10i3h1r3_dependency_dry_run_test_missing")
    require("runtime/scripts/seed.sh" in a10i3h1r2r2.get("forbidden_scope", []), "a10i3h1r3_seed_boundary_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_secondary_review_scope_correction") == str(A10I3H1R2R2_COORDINATION.relative_to(ROOT)), "a10i3h1r2r2_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_secondary_review_scope_correction_sha256") == A10I3H1R2R2_COORDINATION_SHA256, "a10i3h1r2r2_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_secondary_review_scope_correction_evidence") == str(A10I3H1R2R2_EVIDENCE.relative_to(ROOT)), "a10i3h1r2r2_evidence_path_missing")
    require("rework-mmc-resolved-path-and-consumers-a10i3h1r3" in read(SESSION_REGISTRY) and "mmc_h1r3_technical_revalidation_passed_governance_reconciled" in read(SESSION_REGISTRY), "a10i3h1r3_session_status_missing")
    a10i3h1r2r2_evidence_text = read(A10I3H1R2R2_EVIDENCE)
    for marker in ("recovery_path_equal=False", "scripts/dry_run_mmc_dependencies.py", "six product/test paths plus three existing OpenSpec paths", A10I3H1R2R2_COORDINATION_SHA256):
        require(marker in a10i3h1r2r2_evidence_text, f"a10i3h1r2r2_evidence_marker_missing:{marker}")
    a10i3h1r2r3_text = read(A10I3H1R2R3_COORDINATION)
    require(hashlib.sha256(a10i3h1r2r3_text.encode("utf-8")).hexdigest() == A10I3H1R2R3_COORDINATION_SHA256, "a10i3h1r2r3_coordination_sha_mismatch")
    a10i3h1r2r3 = yaml.safe_load(a10i3h1r2r3_text).get("a10i3h1r2_final_scope_correction", {})
    require(a10i3h1r2r3.get("id") == A10I3H1R2R3_COORDINATION_ID, "a10i3h1r2r3_id_mismatch")
    require(a10i3h1r2r3.get("canonical_reviewer", {}).get("decision_received") is False, "a10i3h1r2r3_unexpected_canonical_decision")
    final_scope = a10i3h1r2r3.get("corrected_future_h1r3_scope", {})
    require(final_scope.get("implementation_authorized") is False, "a10i3h1r3_implementation_unexpectedly_authorized")
    require(final_scope.get("product_test_file_count") == len(final_scope.get("product_test_file_allowlist", [])) == 6, "a10i3h1r3_final_product_test_file_count_mismatch")
    require(final_scope.get("openspec_file_count") == len(final_scope.get("openspec_file_allowlist", [])) == 4, "a10i3h1r3_final_openspec_file_count_mismatch")
    require(final_scope.get("total_implementation_and_specification_paths") == 10, "a10i3h1r3_final_total_path_count_mismatch")
    require("openspec/changes/rework-mmc-shared-registry-state-a10i3h1r2/proposal.md" in final_scope.get("openspec_file_allowlist", []), "a10i3h1r3_proposal_missing")
    require("runtime/scripts/seed.sh" in a10i3h1r2r3.get("forbidden_scope", []), "a10i3h1r3_final_seed_boundary_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_final_scope_correction") == str(A10I3H1R2R3_COORDINATION.relative_to(ROOT)), "a10i3h1r2r3_feature_path_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_final_scope_correction_sha256") == A10I3H1R2R3_COORDINATION_SHA256, "a10i3h1r2r3_feature_sha_missing")
    require(feature.get("coordination", {}).get("a10i3h1r2_final_scope_correction_evidence") == str(A10I3H1R2R3_EVIDENCE.relative_to(ROOT)), "a10i3h1r2r3_evidence_path_missing")
    a10i3h1r2r3_evidence_text = read(A10I3H1R2R3_EVIDENCE)
    for marker in ("six product/test paths plus four OpenSpec paths", "proposal.md", "ten total", A10I3H1R2R3_COORDINATION_SHA256):
        require(marker in a10i3h1r2r3_evidence_text, f"a10i3h1r2r3_evidence_marker_missing:{marker}")
    brain_a10p1t3_text = read(BRAIN_A10P1T3_COORDINATION)
    require(hashlib.sha256(brain_a10p1t3_text.encode("utf-8")).hexdigest() == BRAIN_A10P1T3_COORDINATION_SHA256, "brain_a10p1t3_coordination_sha_mismatch")
    brain_a10p1t3 = yaml.safe_load(brain_a10p1t3_text).get("a10p1_brain_tranche3_baseline_repair", {})
    require(brain_a10p1t3.get("id") == BRAIN_A10P1T3_COORDINATION_ID, "brain_a10p1t3_id_mismatch")
    require(brain_a10p1t3.get("release") == "Release-0", "brain_a10p1t3_release_mismatch")
    require(brain_a10p1t3.get("lane", {}).get("thread_id") == LANE_THREADS["brain"], "brain_a10p1t3_thread_mismatch")
    require(brain_a10p1t3.get("baseline", {}).get("head") == "925659b0144a5fb858a78cf32c1d8ddf6967c19b", "brain_a10p1t3_baseline_mismatch")
    require(brain_a10p1t3.get("baseline", {}).get("typecheck_errors") == 49 and brain_a10p1t3.get("baseline", {}).get("typecheck_error_files") == 19, "brain_a10p1t3_typecheck_baseline_mismatch")
    require(brain_a10p1t3.get("product_test_file_count") == len(brain_a10p1t3.get("product_test_file_allowlist", [])) == 11, "brain_a10p1t3_file_count_mismatch")
    require(brain_a10p1t3.get("error_partition", {}).get("selected_errors") == 36, "brain_a10p1t3_selected_error_count_mismatch")
    require(brain_a10p1t3.get("error_partition", {}).get("expected_remaining_errors_ceiling") == 13, "brain_a10p1t3_remaining_error_ceiling_mismatch")
    require(brain_a10p1t3.get("authorization", {}).get("local_product_test_edits") is True, "brain_a10p1t3_local_edits_not_authorized")
    require(brain_a10p1t3.get("authorization", {}).get("real_or_shared_KDS_MMC_access") is False, "brain_a10p1t3_live_access_authorized")
    require(brain_a10p1t3.get("authorization", {}).get("commit") is False and brain_a10p1t3.get("authorization", {}).get("push") is False, "brain_a10p1t3_git_publish_authorized")
    require(brain_a10p1t3.get("serial_gate", {}).get("f013_independent_review_required") is True and brain_a10p1t3.get("serial_gate", {}).get("tranche4_authorized") is False, "brain_a10p1t3_serial_gate_mismatch")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche3_baseline_repair") == str(BRAIN_A10P1T3_COORDINATION.relative_to(ROOT)), "brain_a10p1t3_feature_path_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche3_baseline_repair_sha256") == BRAIN_A10P1T3_COORDINATION_SHA256, "brain_a10p1t3_feature_sha_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche3_dispatch_evidence") == str(BRAIN_A10P1T3_EVIDENCE.relative_to(ROOT)), "brain_a10p1t3_evidence_path_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche3_closure_evidence") == str(BRAIN_A10P1T3_CLOSURE_EVIDENCE.relative_to(ROOT)), "brain_a10p1t3_closure_evidence_path_missing")
    require("brain_a10p1_tranche3_baseline_repair_id: GKE-001-COORDINATION-20260812-002-A10P1T3" in read(CONTROL_BOARD), "brain_a10p1t3_control_board_missing")
    require("repair-brain-read-baseline-a10p1-tranche-4" in read(SESSION_REGISTRY) and "technical_tranche_revalidation_passed_governance_handoff_passed" in read(SESSION_REGISTRY), "brain_a10p1t4_session_status_missing")
    brain_a10p1t3_evidence_text = read(BRAIN_A10P1T3_EVIDENCE)
    for marker in ("49 errors / 19 files", "36", "11", BRAIN_A10P1T3_COORDINATION_SHA256, "authorized_dispatch_pending_receipt"):
        require(marker in brain_a10p1t3_evidence_text, f"brain_a10p1t3_evidence_marker_missing:{marker}")
    brain_a10p1t3_closure_text = read(BRAIN_A10P1T3_CLOSURE_EVIDENCE)
    for marker in ("45/45", "13 errors / 8 files", "b3b2c668129648dc1e78c2a59bce991330aa64094981bc61ff2651a5fb44ea49", "technical_tranche_revalidation_passed_governance_handoff_passed"):
        require(marker in brain_a10p1t3_closure_text, f"brain_a10p1t3_closure_marker_missing:{marker}")
    brain_a10p1t4_text = read(BRAIN_A10P1T4_COORDINATION)
    require(hashlib.sha256(brain_a10p1t4_text.encode("utf-8")).hexdigest() == BRAIN_A10P1T4_COORDINATION_SHA256, "brain_a10p1t4_coordination_sha_mismatch")
    brain_a10p1t4 = yaml.safe_load(brain_a10p1t4_text).get("a10p1_brain_tranche4_baseline_repair", {})
    require(brain_a10p1t4.get("id") == BRAIN_A10P1T4_COORDINATION_ID, "brain_a10p1t4_id_mismatch")
    require(brain_a10p1t4.get("lane", {}).get("thread_id") == LANE_THREADS["brain"], "brain_a10p1t4_thread_mismatch")
    require(brain_a10p1t4.get("baseline", {}).get("typecheck_errors") == 13 and brain_a10p1t4.get("baseline", {}).get("typecheck_error_files") == 8, "brain_a10p1t4_typecheck_baseline_mismatch")
    require(brain_a10p1t4.get("product_test_file_count") == len(brain_a10p1t4.get("product_test_file_allowlist", [])) == 8, "brain_a10p1t4_file_count_mismatch")
    require(len(brain_a10p1t4.get("product_test_baseline_sha256", {})) == 8, "brain_a10p1t4_baseline_hash_count_mismatch")
    require(brain_a10p1t4.get("authorization", {}).get("local_product_test_edits") is True, "brain_a10p1t4_local_edits_not_authorized")
    require(brain_a10p1t4.get("authorization", {}).get("real_or_shared_KDS_MMC_access") is False, "brain_a10p1t4_live_access_authorized")
    require(brain_a10p1t4.get("serial_gate", {}).get("f013_independent_review_required") is True and brain_a10p1t4.get("serial_gate", {}).get("release0_real_e2e_authorized") is False, "brain_a10p1t4_serial_gate_mismatch")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche4_baseline_repair") == str(BRAIN_A10P1T4_COORDINATION.relative_to(ROOT)), "brain_a10p1t4_feature_path_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche4_baseline_repair_sha256") == BRAIN_A10P1T4_COORDINATION_SHA256, "brain_a10p1t4_feature_sha_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche4_dispatch_evidence") == str(BRAIN_A10P1T4_EVIDENCE.relative_to(ROOT)), "brain_a10p1t4_evidence_path_missing")
    require("brain_a10p1_tranche4_baseline_repair_id: GKE-001-COORDINATION-20260812-008-A10P1T4" in read(CONTROL_BOARD), "brain_a10p1t4_control_board_missing")
    brain_a10p1t4_evidence_text = read(BRAIN_A10P1T4_EVIDENCE)
    for marker in ("13 errors / 8 files", "八个", BRAIN_A10P1T4_COORDINATION_ID):
        require(marker in brain_a10p1t4_evidence_text, f"brain_a10p1t4_evidence_marker_missing:{marker}")
    brain_a10p1t4r1_text = read(BRAIN_A10P1T4R1_COORDINATION)
    require(hashlib.sha256(brain_a10p1t4r1_text.encode("utf-8")).hexdigest() == BRAIN_A10P1T4R1_COORDINATION_SHA256, "brain_a10p1t4r1_coordination_sha_mismatch")
    brain_a10p1t4r1 = yaml.safe_load(brain_a10p1t4r1_text).get("a10p1_brain_tranche4_opsx_adapter_amendment", {})
    require(brain_a10p1t4r1.get("id") == BRAIN_A10P1T4R1_COORDINATION_ID, "brain_a10p1t4r1_id_mismatch")
    require(brain_a10p1t4r1.get("amends") == BRAIN_A10P1T4_COORDINATION_ID, "brain_a10p1t4r1_parent_mismatch")
    require(brain_a10p1t4r1.get("authorization_delta", {}).get("temporary_execution_file", {}).get("handoff_status_requirement") == "absent", "brain_a10p1t4r1_cleanup_requirement_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche4_opsx_adapter_amendment") == str(BRAIN_A10P1T4R1_COORDINATION.relative_to(ROOT)), "brain_a10p1t4r1_feature_path_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche4_opsx_adapter_amendment_sha256") == BRAIN_A10P1T4R1_COORDINATION_SHA256, "brain_a10p1t4r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("brain_a10p1_tranche4_handoff_evidence") == str(BRAIN_A10P1T4_HANDOFF_EVIDENCE.relative_to(ROOT)), "brain_a10p1t4_handoff_evidence_path_missing")
    require(f"brain_a10p1_tranche4_opsx_adapter_amendment_id: {BRAIN_A10P1T4R1_COORDINATION_ID}" in read(CONTROL_BOARD), "brain_a10p1t4r1_control_board_missing")
    brain_a10p1t4_handoff_text = read(BRAIN_A10P1T4_HANDOFF_EVIDENCE)
    for marker in ("0 errors", "85 passed", "384 passed", "6c6bd5542ab751f6e39d2ed8ad211a2e43260aa820fc83b411636d62b633e359", "technical_tranche_revalidation_passed_governance_handoff_passed", "targeted_technical_receipt_preserved_admission_blocked_dirty_worktree"):
        require(marker in brain_a10p1t4_handoff_text, f"brain_a10p1t4_handoff_marker_missing:{marker}")
    studio_a10i1g1_text = read(STUDIO_A10I1G1_COORDINATION)
    require(hashlib.sha256(studio_a10i1g1_text.encode("utf-8")).hexdigest() == STUDIO_A10I1G1_COORDINATION_SHA256, "studio_a10i1g1_coordination_sha_mismatch")
    studio_a10i1g1 = yaml.safe_load(studio_a10i1g1_text).get("studio_postcommit_codegraph_reconciliation", {})
    require(studio_a10i1g1.get("id") == STUDIO_A10I1G1_COORDINATION_ID, "studio_a10i1g1_id_mismatch")
    require(studio_a10i1g1.get("lane", {}).get("thread_id") == LANE_THREADS["studio"], "studio_a10i1g1_thread_mismatch")
    require(studio_a10i1g1.get("baseline", {}).get("head") == "953d4d1baea201cc0fc822074bc74cad9299d0dd", "studio_a10i1g1_head_mismatch")
    require(studio_a10i1g1.get("baseline", {}).get("parent") == "88769078f5c230ae9ed973815de4861cc6317a5c", "studio_a10i1g1_parent_mismatch")
    require(studio_a10i1g1.get("product_test_file_count") == len(studio_a10i1g1.get("product_test_file_allowlist", [])) == 3, "studio_a10i1g1_file_count_mismatch")
    require(studio_a10i1g1.get("required_protocol", {}).get("schema_change") == "additive_schema_v4", "studio_a10i1g1_schema_boundary_missing")
    require(studio_a10i1g1.get("required_protocol", {}).get("schema_v1_v2_v3_behavior_unchanged") is True, "studio_a10i1g1_backward_compatibility_missing")
    require(studio_a10i1g1.get("required_protocol", {}).get("no_waiver_or_silent_hash_rewrite") is True, "studio_a10i1g1_no_waiver_boundary_missing")
    require(studio_a10i1g1.get("observed_root_cause", {}).get("direct_lock_exemption_is_sound") is False, "studio_a10i1g1_unsound_lock_exemption")
    require("docs/harness/evidence/codegraph/GPCF-STUDIO-LR-876.json" in studio_a10i1g1.get("forbidden_scope", []), "studio_a10i1g1_lr876_mutation_not_forbidden")
    require(studio_a10i1g1.get("authorization", {}).get("real_or_shared_KDS_MMC_access") is False, "studio_a10i1g1_live_access_authorized")
    require(studio_a10i1g1.get("authorization", {}).get("commit") is False and studio_a10i1g1.get("authorization", {}).get("push") is False, "studio_a10i1g1_git_publish_authorized")
    require(feature.get("coordination", {}).get("studio_a10i1g1_postcommit_codegraph_reconciliation") == str(STUDIO_A10I1G1_COORDINATION.relative_to(ROOT)), "studio_a10i1g1_feature_path_missing")
    require(feature.get("coordination", {}).get("studio_a10i1g1_postcommit_codegraph_reconciliation_sha256") == STUDIO_A10I1G1_COORDINATION_SHA256, "studio_a10i1g1_feature_sha_missing")
    require(feature.get("coordination", {}).get("studio_a10i1g1_dispatch_evidence") == str(STUDIO_A10I1G1_EVIDENCE.relative_to(ROOT)), "studio_a10i1g1_evidence_path_missing")
    require(feature.get("coordination", {}).get("studio_a10i1g1_final_reseal") == str(STUDIO_A10I1G1R1_COORDINATION.relative_to(ROOT)), "studio_a10i1g1r1_feature_path_missing")
    require(feature.get("coordination", {}).get("studio_a10i1g1_final_reseal_sha256") == STUDIO_A10I1G1R1_COORDINATION_SHA256, "studio_a10i1g1r1_feature_sha_missing")
    require(feature.get("coordination", {}).get("studio_a10i1g1_closure_evidence") == str(STUDIO_A10I1G1_CLOSURE_EVIDENCE.relative_to(ROOT)), "studio_a10i1g1_closure_evidence_path_missing")
    require("reconcile-studio-committed-codegraph-evidence-a10i1g1" in read(SESSION_REGISTRY) and "technical_governance_reconciliation_verified_with_external_receipt" in read(SESSION_REGISTRY), "studio_a10i1g1_session_status_missing")
    studio_a10i1g1_evidence_text = read(STUDIO_A10I1G1_EVIDENCE)
    for marker in ("953d4d1baea201cc0fc822074bc74cad9299d0dd", "88769078f5c230ae9ed973815de4861cc6317a5c", "three product/test paths", "simply filtering the lock", "authorized_dispatch_pending_receipt"):
        require(marker in studio_a10i1g1_evidence_text, f"studio_a10i1g1_evidence_marker_missing:{marker}")
    studio_a10i1g1r1_text = read(STUDIO_A10I1G1R1_COORDINATION)
    require(hashlib.sha256(studio_a10i1g1r1_text.encode("utf-8")).hexdigest() == STUDIO_A10I1G1R1_COORDINATION_SHA256, "studio_a10i1g1r1_coordination_sha_mismatch")
    studio_a10i1g1r1 = yaml.safe_load(studio_a10i1g1r1_text).get("studio_a10i1g1_final_reseal", {})
    require(studio_a10i1g1r1.get("id") == STUDIO_A10I1G1R1_COORDINATION_ID, "studio_a10i1g1r1_id_mismatch")
    require(studio_a10i1g1r1.get("authorization", {}).get("reseal_existing_lr877_once") is True, "studio_a10i1g1r1_reseal_not_authorized")
    require(studio_a10i1g1r1.get("authorization", {}).get("modify_run_evidence_after_reseal") is False, "studio_a10i1g1r1_post_reseal_write_authorized")
    studio_a10i1g1_closure_text = read(STUDIO_A10I1G1_CLOSURE_EVIDENCE)
    for marker in ("9b0783f0469f98c1487c88a15c9b5f5de26b44c57164e50bb26cf6f9a7048a99", "4ab7551b70d35572fe9a164e3306151b6ac496677161f90904915ad6b1d12620", "321416819ec6920a6f6fd5ff3a1c24c8de291a62bf54e38e7a62ab39d8918fa8", "f4d2334b5aec3fce137bfd24bb81488e8ee78cf24f8e6821dbc871495779395a", "b01c524f6c122bb676e7b1a4d24c63ae341280cad6054dcbebc1b60a2f27d8d3", "technical_governance_reconciliation_verified_with_external_receipt"):
        require(marker in studio_a10i1g1_closure_text, f"studio_a10i1g1_closure_marker_missing:{marker}")
    kds_dirty_isolation_text = read(KDS_DIRTY_ISOLATION_COORDINATION)
    require(hashlib.sha256(kds_dirty_isolation_text.encode("utf-8")).hexdigest() == KDS_DIRTY_ISOLATION_COORDINATION_SHA256, "kds_dirty_isolation_coordination_sha_mismatch")
    kds_dirty_isolation = yaml.safe_load(kds_dirty_isolation_text).get("kds_dirty_ownership_isolation", {})
    require(kds_dirty_isolation.get("id") == KDS_DIRTY_ISOLATION_COORDINATION_ID, "kds_dirty_isolation_id_mismatch")
    require(kds_dirty_isolation.get("KDS_repository_allowlist") == [], "kds_dirty_isolation_allowlist_not_empty")
    require(kds_dirty_isolation.get("repository_baseline", {}).get("ordinary_dirty_entries") == 190, "kds_dirty_isolation_ordinary_count_mismatch")
    require(kds_dirty_isolation.get("repository_baseline", {}).get("expanded_dirty_entries") == 462, "kds_dirty_isolation_expanded_count_mismatch")
    require(kds_dirty_isolation.get("ownership_partition", {}).get("ordinary", {}).get("unclassified") == 0, "kds_dirty_isolation_unclassified_entries")
    require(kds_dirty_isolation.get("authorization", {}).get("KDS_write") is False, "kds_dirty_isolation_kds_write_authorized")
    require(feature.get("coordination", {}).get("kds_dirty_ownership_isolation") == str(KDS_DIRTY_ISOLATION_COORDINATION.relative_to(ROOT)), "kds_dirty_isolation_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_dirty_ownership_isolation_sha256") == KDS_DIRTY_ISOLATION_COORDINATION_SHA256, "kds_dirty_isolation_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_dirty_ownership_isolation_evidence") == str(KDS_DIRTY_ISOLATION_EVIDENCE.relative_to(ROOT)), "kds_dirty_isolation_evidence_path_missing")
    require(KDS_DIRTY_ISOLATION_COORDINATION_ID in read(SESSION_REGISTRY), "kds_dirty_isolation_session_record_missing")
    require("ownership_partition_verified_for_owner_specific_disposition_controls" in read(KDS_DIRTY_ISOLATION_EVIDENCE), "kds_dirty_isolation_review_receipt_missing")
    kds_dependency_order_text = read(KDS_DEPENDENCY_ORDER_COORDINATION)
    require(hashlib.sha256(kds_dependency_order_text.encode("utf-8")).hexdigest() == KDS_DEPENDENCY_ORDER_COORDINATION_SHA256, "kds_dependency_order_coordination_sha_mismatch")
    kds_dependency_order = yaml.safe_load(kds_dependency_order_text).get("kds_stageb_release0_dependency_order", {})
    require(kds_dependency_order.get("id") == KDS_DEPENDENCY_ORDER_COORDINATION_ID, "kds_dependency_order_id_mismatch")
    require(kds_dependency_order.get("KDS_repository_allowlist") == [], "kds_dependency_order_allowlist_not_empty")
    require(kds_dependency_order.get("disposable_replays", {}).get("stage_b_only", {}).get("passed") == 66, "kds_dependency_order_stageb_replay_mismatch")
    require(kds_dependency_order.get("disposable_replays", {}).get("stage_b_then_a10i1", {}).get("passed") == 101, "kds_dependency_order_combined_pass_mismatch")
    require(kds_dependency_order.get("disposable_replays", {}).get("stage_b_then_a10i1", {}).get("skipped") == 6, "kds_dependency_order_combined_skip_mismatch")
    require(kds_dependency_order.get("authorization", {}).get("KDS_write") is False, "kds_dependency_order_kds_write_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_release0_dependency_order") == str(KDS_DEPENDENCY_ORDER_COORDINATION.relative_to(ROOT)), "kds_dependency_order_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_release0_dependency_order_sha256") == KDS_DEPENDENCY_ORDER_COORDINATION_SHA256, "kds_dependency_order_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_release0_dependency_order_evidence") == str(KDS_DEPENDENCY_ORDER_EVIDENCE.relative_to(ROOT)), "kds_dependency_order_evidence_path_missing")
    require(KDS_DEPENDENCY_ORDER_COORDINATION_ID in read(SESSION_REGISTRY), "kds_dependency_order_session_record_missing")
    require("dependency_order_verified_owner_sets_must_remain_separate" in read(KDS_DEPENDENCY_ORDER_EVIDENCE), "kds_dependency_order_review_receipt_missing")
    kds_stageb_disposition_text = read(KDS_STAGEB_DISPOSITION_COORDINATION)
    require(hashlib.sha256(kds_stageb_disposition_text.encode("utf-8")).hexdigest() == KDS_STAGEB_DISPOSITION_COORDINATION_SHA256, "kds_stageb_disposition_coordination_sha_mismatch")
    kds_stageb_disposition = yaml.safe_load(kds_stageb_disposition_text).get("kds_stageb_owner_disposition_preflight", {})
    require(kds_stageb_disposition.get("id") == KDS_STAGEB_DISPOSITION_COORDINATION_ID, "kds_stageb_disposition_id_mismatch")
    require(kds_stageb_disposition.get("repository_allowlist") == [], "kds_stageb_disposition_allowlist_not_empty")
    require(len(kds_stageb_disposition.get("disposition_units", {}).get("stageb_core_12", {}).get("paths", [])) == 12, "kds_stageb_disposition_core_count_mismatch")
    require(len(kds_stageb_disposition.get("disposition_units", {}).get("stageb_regression_2", {}).get("paths", [])) == 2, "kds_stageb_disposition_regression_count_mismatch")
    require(len(kds_stageb_disposition.get("disposition_units", {}).get("stageb_openspec_9", {}).get("paths", [])) == 9, "kds_stageb_disposition_openspec_count_mismatch")
    require(len(kds_stageb_disposition.get("disposition_units", {}).get("stageb_run_handoff_13", {}).get("paths", [])) == 13, "kds_stageb_disposition_run_count_mismatch")
    require(kds_stageb_disposition.get("authorization", {}).get("KDS_repository_write") is False, "kds_stageb_disposition_kds_write_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_owner_disposition_preflight") == str(KDS_STAGEB_DISPOSITION_COORDINATION.relative_to(ROOT)), "kds_stageb_disposition_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_owner_disposition_preflight_sha256") == KDS_STAGEB_DISPOSITION_COORDINATION_SHA256, "kds_stageb_disposition_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_owner_disposition_preflight_evidence") == str(KDS_STAGEB_DISPOSITION_EVIDENCE.relative_to(ROOT)), "kds_stageb_disposition_evidence_path_missing")
    disposition_evidence = read(KDS_STAGEB_DISPOSITION_EVIDENCE)
    require("preflight_verified_sufficient_for_separately_controlled_stageb_owner_disposition" in disposition_evidence, "kds_stageb_disposition_review_missing")
    require("7fe83224e36ffb504e79ecf67579256d1d956ee4a8b99def35c627811dc872dc" in disposition_evidence, "kds_stageb_core_patch_sha_missing")
    require("1e7ecd30fbb740fcf2217224de107adb0c960d5babfc71aaaee036b9fae90f7e" in disposition_evidence, "kds_stageb_regression_patch_sha_missing")
    require("preflight_verified_sufficient_for_separately_controlled_stageb_owner_disposition" in read(SESSION_REGISTRY), "kds_stageb_disposition_session_state_missing")
    authorization_request_text = read(KDS_STAGEB_AUTHORIZATION_REQUEST)
    require(hashlib.sha256(authorization_request_text.encode("utf-8")).hexdigest() == KDS_STAGEB_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_authorization_request_sha_mismatch")
    authorization_request = yaml.safe_load(authorization_request_text).get("kds_stageb_owner_disposition_authorization_request", {})
    require(authorization_request.get("id") == KDS_STAGEB_AUTHORIZATION_REQUEST_ID, "kds_stageb_authorization_request_id_mismatch")
    require(authorization_request.get("mode") == "human_authorization_request_only", "kds_stageb_authorization_request_mode_mismatch")
    require(len(authorization_request.get("proposed_topology", [])) == 4, "kds_stageb_authorization_topology_count_mismatch")
    require([len(unit.get("paths", [])) for unit in authorization_request.get("proposed_topology", [])] == [12, 2, 9, 13], "kds_stageb_authorization_path_counts_mismatch")
    require(authorization_request.get("authorization", {}).get("stage") is False, "kds_stageb_stage_unexpectedly_authorized")
    require(authorization_request.get("authorization", {}).get("commit") is False, "kds_stageb_commit_unexpectedly_authorized")
    require(authorization_request.get("authorization", {}).get("push") is False, "kds_stageb_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_owner_disposition_authorization_request") == str(KDS_STAGEB_AUTHORIZATION_REQUEST.relative_to(ROOT)), "kds_stageb_authorization_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_owner_disposition_authorization_request_sha256") == KDS_STAGEB_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_authorization_feature_sha_missing")
    require("rework_required" in read(KDS_STAGEB_AUTHORIZATION_EVIDENCE), "kds_stageb_authorization_review_finding_missing")
    core_authorization_text = read(KDS_STAGEB_CORE_AUTHORIZATION_REQUEST)
    require(hashlib.sha256(core_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_core_authorization_request_sha_mismatch")
    core_authorization = yaml.safe_load(core_authorization_text).get("kds_stageb_core_authorization_request", {})
    require(core_authorization.get("id") == KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_ID, "kds_stageb_core_authorization_request_id_mismatch")
    require(core_authorization.get("mode") == "human_authorization_request_only", "kds_stageb_core_authorization_mode_mismatch")
    require(core_authorization.get("required_pre_execution_baseline", {}).get("head") == "f28edb5113e0493ed60fec423cb6c7e1a6252de8", "kds_stageb_core_parent_mismatch")
    require(len(core_authorization.get("requested_unit", {}).get("paths", [])) == 12, "kds_stageb_core_authorization_path_count_mismatch")
    require(core_authorization.get("requested_unit", {}).get("sorted_nul_pathset_sha256") == "ca5d5931bd2d41619cd83c0347ba72c73cde41534d8dd078bfc5fc908514a0bb", "kds_stageb_core_pathset_sha_mismatch")
    require(core_authorization.get("requested_unit", {}).get("canonical_patch_sha256") == "7fe83224e36ffb504e79ecf67579256d1d956ee4a8b99def35c627811dc872dc", "kds_stageb_core_authorization_patch_sha_mismatch")
    require(core_authorization.get("current_authorization", {}).get("stage") is False, "kds_stageb_core_stage_unexpectedly_authorized")
    require(core_authorization.get("current_authorization", {}).get("commit") is False, "kds_stageb_core_commit_unexpectedly_authorized")
    require(core_authorization.get("current_authorization", {}).get("push") is False, "kds_stageb_core_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_core_authorization_request") == str(KDS_STAGEB_CORE_AUTHORIZATION_REQUEST.relative_to(ROOT)), "kds_stageb_core_authorization_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_core_authorization_request_sha256") == KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_core_authorization_feature_sha_missing")
    require("authorization_request_review_passed_human_core_commit_authorization_required" in read(KDS_STAGEB_CORE_AUTHORIZATION_EVIDENCE), "kds_stageb_core_review_classification_missing")
    require("human_core_commit_authorization_pending" in read(KDS_STAGEB_CORE_AUTHORIZATION_EVIDENCE), "kds_stageb_core_human_authorization_boundary_missing")
    require("authorization_request_review_passed_human_core_commit_authorization_required" in read(SESSION_REGISTRY), "kds_stageb_core_authorization_session_state_missing")
    baseline_reconciliation_text = read(KDS_STAGEB_CORE_BASELINE_RECONCILIATION)
    require(hashlib.sha256(baseline_reconciliation_text.encode("utf-8")).hexdigest() == KDS_STAGEB_CORE_BASELINE_RECONCILIATION_SHA256, "kds_stageb_core_baseline_reconciliation_sha_mismatch")
    baseline_reconciliation = yaml.safe_load(baseline_reconciliation_text).get("kds_stageb_core_baseline_reconciliation", {})
    require(baseline_reconciliation.get("id") == KDS_STAGEB_CORE_BASELINE_RECONCILIATION_ID, "kds_stageb_core_baseline_reconciliation_id_mismatch")
    require(baseline_reconciliation.get("human_authorization_receipt", {}).get("decision") == "granted", "kds_stageb_core_human_authorization_receipt_missing")
    require(len(baseline_reconciliation.get("exact_new_external_entries", [])) == 3, "kds_stageb_core_baseline_external_entry_count_mismatch")
    require(baseline_reconciliation.get("requested_unit_unchanged", {}).get("canonical_patch_sha256") == "7fe83224e36ffb504e79ecf67579256d1d956ee4a8b99def35c627811dc872dc", "kds_stageb_core_baseline_patch_sha_mismatch")
    require(baseline_reconciliation.get("authorization", {}).get("KDS_write_during_reconciliation") is False, "kds_stageb_core_reconciliation_unexpectedly_authorized_write")
    require(feature.get("coordination", {}).get("kds_stageb_core_baseline_reconciliation") == str(KDS_STAGEB_CORE_BASELINE_RECONCILIATION.relative_to(ROOT)), "kds_stageb_core_baseline_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_core_baseline_reconciliation_sha256") == KDS_STAGEB_CORE_BASELINE_RECONCILIATION_SHA256, "kds_stageb_core_baseline_feature_sha_missing")
    require("baseline_drift_reconciled_original_human_authorization_remains_valid" in read(KDS_STAGEB_CORE_BASELINE_RECONCILIATION_EVIDENCE), "kds_stageb_core_baseline_review_state_missing")
    difffix_text = read(KDS_STAGEB_CORE_DIFFFIX_REWORK)
    require(hashlib.sha256(difffix_text.encode("utf-8")).hexdigest() == KDS_STAGEB_CORE_DIFFFIX_REWORK_SHA256, "kds_stageb_core_diffcheck_rework_sha_mismatch")
    difffix = yaml.safe_load(difffix_text).get("kds_stageb_core_diffcheck_rework", {})
    require(difffix.get("id") == KDS_STAGEB_CORE_DIFFFIX_REWORK_ID, "kds_stageb_core_diffcheck_rework_id_mismatch")
    require(difffix.get("aborted_execution_receipt", {}).get("commit_created") is False, "kds_stageb_core_aborted_commit_unexpectedly_created")
    require(difffix.get("revised_core_unit", {}).get("canonical_patch_sha256") == "c9692a48019a3d6ccc2949a9452ff26bd2bfd0785ec69be728a13552ce977fad", "kds_stageb_core_revised_patch_sha_mismatch")
    require(difffix.get("requested_human_decision", {}).get("source_edit_one_byte") == "pending", "kds_stageb_core_diffcheck_rework_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_core_diffcheck_rework") == str(KDS_STAGEB_CORE_DIFFFIX_REWORK.relative_to(ROOT)), "kds_stageb_core_diffcheck_rework_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_core_diffcheck_rework_sha256") == KDS_STAGEB_CORE_DIFFFIX_REWORK_SHA256, "kds_stageb_core_diffcheck_rework_feature_sha_missing")
    require("authorization_request_review_passed_human_one_byte_rework_and_core_commit_authorization_required" in read(KDS_STAGEB_CORE_DIFFFIX_REWORK_EVIDENCE), "kds_stageb_core_diffcheck_rework_review_state_missing")
    difffix_authorization_text = read(KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION)
    require(hashlib.sha256(difffix_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_SHA256, "kds_stageb_core_diffcheck_authorization_sha_mismatch")
    difffix_authorization = yaml.safe_load(difffix_authorization_text).get("kds_stageb_core_diffcheck_rework_authorization", {})
    require(difffix_authorization.get("id") == KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_ID, "kds_stageb_core_diffcheck_authorization_id_mismatch")
    require(difffix_authorization.get("human_authorization_receipt", {}).get("decision") == "granted", "kds_stageb_core_diffcheck_human_authorization_missing")
    require(difffix_authorization.get("execution", {}).get("baseline") == "f28edb5113e0493ed60fec423cb6c7e1a6252de8", "kds_stageb_core_diffcheck_authorization_parent_mismatch")
    require(difffix_authorization.get("execution", {}).get("corrected_file_sha256") == "05c637cbd86fc65c0d8db5ce621fea85576a3fc37107dcd506d16b61ab0c9ea3", "kds_stageb_core_diffcheck_corrected_file_sha_mismatch")
    require(difffix_authorization.get("execution", {}).get("canonical_patch_sha256") == "c9692a48019a3d6ccc2949a9452ff26bd2bfd0785ec69be728a13552ce977fad", "kds_stageb_core_diffcheck_authorized_patch_sha_mismatch")
    require(difffix_authorization.get("execution", {}).get("local_commit") is True, "kds_stageb_core_diffcheck_local_commit_not_authorized")
    require(difffix_authorization.get("execution", {}).get("push") is False, "kds_stageb_core_diffcheck_push_unexpectedly_authorized")
    require(difffix_authorization.get("execution", {}).get("later_units") is False, "kds_stageb_core_diffcheck_later_units_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_core_diffcheck_rework_authorization") == str(KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION.relative_to(ROOT)), "kds_stageb_core_diffcheck_authorization_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_core_diffcheck_rework_authorization_sha256") == KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_SHA256, "kds_stageb_core_diffcheck_authorization_feature_sha_missing")
    require("Human Authorization Receipt" in read(KDS_STAGEB_CORE_DIFFFIX_REWORK_EVIDENCE), "kds_stageb_core_diffcheck_authorization_evidence_missing")
    local_commit_receipt_text = read(KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT)
    require(hashlib.sha256(local_commit_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_SHA256, "kds_stageb_core_local_commit_receipt_sha_mismatch")
    local_commit_receipt = yaml.safe_load(local_commit_receipt_text).get("kds_stageb_core_local_commit_receipt", {})
    require(local_commit_receipt.get("id") == KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_ID, "kds_stageb_core_local_commit_receipt_id_mismatch")
    require(local_commit_receipt.get("commit", {}).get("sha") == "7fb477030f5278faf55d6d16ff3874469704610d", "kds_stageb_core_local_commit_sha_mismatch")
    require(local_commit_receipt.get("commit", {}).get("parent") == "f28edb5113e0493ed60fec423cb6c7e1a6252de8", "kds_stageb_core_local_commit_parent_mismatch")
    require(local_commit_receipt.get("commit", {}).get("tree") == "b1c8bf1bd0e6f3b0f67726844065732ce5f8602c", "kds_stageb_core_local_commit_tree_mismatch")
    require(local_commit_receipt.get("commit", {}).get("path_count") == 12, "kds_stageb_core_local_commit_path_count_mismatch")
    require(local_commit_receipt.get("commit", {}).get("canonical_patch_sha256") == "c9692a48019a3d6ccc2949a9452ff26bd2bfd0785ec69be728a13552ce977fad", "kds_stageb_core_local_commit_patch_sha_mismatch")
    require(local_commit_receipt.get("verification", {}).get("core_non_db_tests") == 64, "kds_stageb_core_local_commit_test_count_mismatch")
    require(local_commit_receipt.get("verification", {}).get("result") == "pass", "kds_stageb_core_local_commit_tests_not_passed")
    require(local_commit_receipt.get("authorization_boundary", {}).get("push") is False, "kds_stageb_core_local_commit_push_unexpectedly_authorized")
    require(local_commit_receipt.get("authorization_boundary", {}).get("later_unit") is False, "kds_stageb_core_local_commit_later_unit_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_core_local_commit_receipt") == str(KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT.relative_to(ROOT)), "kds_stageb_core_local_commit_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_core_local_commit_receipt_sha256") == KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_SHA256, "kds_stageb_core_local_commit_feature_sha_missing")
    require("64/64" in read(KDS_STAGEB_CORE_DIFFFIX_REWORK_EVIDENCE), "kds_stageb_core_local_commit_test_evidence_missing")
    require("local_core_commit_independent_review_passed" in read(KDS_STAGEB_CORE_DIFFFIX_REWORK_EVIDENCE), "kds_stageb_core_local_commit_independent_review_missing")
    regression_preflight_text = read(KDS_STAGEB_REGRESSION_PREFLIGHT)
    require(hashlib.sha256(regression_preflight_text.encode("utf-8")).hexdigest() == KDS_STAGEB_REGRESSION_PREFLIGHT_SHA256, "kds_stageb_regression_preflight_sha_mismatch")
    regression_preflight = yaml.safe_load(regression_preflight_text).get("kds_stageb_regression_preflight", {})
    require(regression_preflight.get("id") == KDS_STAGEB_REGRESSION_PREFLIGHT_ID, "kds_stageb_regression_preflight_id_mismatch")
    require(regression_preflight.get("dependency", {}).get("accepted_local_core_commit") == "7fb477030f5278faf55d6d16ff3874469704610d", "kds_stageb_regression_preflight_parent_mismatch")
    require(regression_preflight.get("candidate_unit", {}).get("repository_write_allowlist") == [], "kds_stageb_regression_preflight_write_allowlist_not_empty")
    require(regression_preflight.get("candidate_unit", {}).get("source_paths") == ["tests/test_knowledge_intake_api.py", "tests/test_knowledge_intake_postgres.py"], "kds_stageb_regression_preflight_path_mismatch")
    require(regression_preflight.get("candidate_unit", {}).get("sorted_nul_pathset_sha256") == "ffeab20c1c54610428c2da48d4dc6b83275affdaa5a69a1b969b005af008b66f", "kds_stageb_regression_preflight_pathset_sha_mismatch")
    require(regression_preflight.get("candidate_unit", {}).get("canonical_patch_sha256") == "1e7ecd30fbb740fcf2217224de107adb0c960d5babfc71aaaee036b9fae90f7e", "kds_stageb_regression_preflight_patch_sha_mismatch")
    require(regression_preflight.get("authorization", {}).get("kds_repository_write") is False, "kds_stageb_regression_preflight_repository_write_unexpectedly_authorized")
    require(regression_preflight.get("authorization", {}).get("commit") is False, "kds_stageb_regression_preflight_commit_unexpectedly_authorized")
    require(regression_preflight.get("authorization", {}).get("push") is False, "kds_stageb_regression_preflight_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_regression_preflight") == str(KDS_STAGEB_REGRESSION_PREFLIGHT.relative_to(ROOT)), "kds_stageb_regression_preflight_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_preflight_sha256") == KDS_STAGEB_REGRESSION_PREFLIGHT_SHA256, "kds_stageb_regression_preflight_feature_sha_missing")
    regression_receipt_text = read(KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT)
    require(hashlib.sha256(regression_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_regression_preflight_receipt_sha_mismatch")
    regression_receipt = yaml.safe_load(regression_receipt_text).get("kds_stageb_regression_preflight_receipt", {})
    require(regression_receipt.get("id") == KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_ID, "kds_stageb_regression_preflight_receipt_id_mismatch")
    require(regression_receipt.get("parent_control", {}).get("id") == KDS_STAGEB_REGRESSION_PREFLIGHT_ID, "kds_stageb_regression_preflight_receipt_parent_mismatch")
    require(regression_receipt.get("candidate", {}).get("patch_bytes") == 38511, "kds_stageb_regression_preflight_receipt_patch_bytes_mismatch")
    require(regression_receipt.get("candidate", {}).get("patch_sha256") == "1e7ecd30fbb740fcf2217224de107adb0c960d5babfc71aaaee036b9fae90f7e", "kds_stageb_regression_preflight_receipt_patch_sha_mismatch")
    require(regression_receipt.get("verification", {}).get("non_db_tests", {}).get("passed") == 66, "kds_stageb_regression_preflight_non_db_tests_mismatch")
    require(regression_receipt.get("verification", {}).get("postgresql_and_migration_tests", {}).get("passed") == 23, "kds_stageb_regression_preflight_pg_tests_mismatch")
    require(regression_receipt.get("verification", {}).get("disposable_database", {}).get("cleanup_count") == 0, "kds_stageb_regression_preflight_database_cleanup_failed")
    require(regression_receipt.get("verification", {}).get("disposable_root_count_after") == 0, "kds_stageb_regression_preflight_root_cleanup_failed")
    require(regression_receipt.get("authorization_boundary", {}).get("commit") is False, "kds_stageb_regression_preflight_receipt_commit_unexpectedly_authorized")
    require(regression_receipt.get("authorization_boundary", {}).get("future_commit_requires_human_authorization") is True, "kds_stageb_regression_preflight_human_authorization_boundary_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_preflight_receipt") == str(KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT.relative_to(ROOT)), "kds_stageb_regression_preflight_receipt_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_preflight_receipt_sha256") == KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_regression_preflight_receipt_feature_sha_missing")
    regression_authorization_text = read(KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST)
    require(hashlib.sha256(regression_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_regression_commit_authorization_request_sha_mismatch")
    regression_authorization = yaml.safe_load(regression_authorization_text).get("kds_stageb_regression_local_commit_authorization_request", {})
    require(regression_authorization.get("id") == KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_ID, "kds_stageb_regression_commit_authorization_request_id_mismatch")
    require(regression_authorization.get("required_human_decision") == "authorize_or_decline_one_local_commit", "kds_stageb_regression_human_decision_missing")
    require(regression_authorization.get("execution_allowlist") == ["tests/test_knowledge_intake_api.py", "tests/test_knowledge_intake_postgres.py"], "kds_stageb_regression_commit_allowlist_mismatch")
    require(regression_authorization.get("authorization", {}).get("local_stage_and_one_commit") == "human_decision_pending", "kds_stageb_regression_commit_not_pending_human")
    require(regression_authorization.get("authorization", {}).get("push") is False, "kds_stageb_regression_push_unexpectedly_authorized")
    require(regression_authorization.get("authorization", {}).get("later_unit") is False, "kds_stageb_regression_later_unit_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_authorization_request") == str(KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST.relative_to(ROOT)), "kds_stageb_regression_commit_authorization_request_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_authorization_request_sha256") == KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_regression_commit_authorization_request_feature_sha_missing")
    regression_commit_authorization_text = read(KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION)
    require(hashlib.sha256(regression_commit_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_SHA256, "kds_stageb_regression_commit_authorization_sha_mismatch")
    regression_commit_authorization = yaml.safe_load(regression_commit_authorization_text).get("kds_stageb_regression_local_commit_authorization", {})
    require(regression_commit_authorization.get("id") == KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_ID, "kds_stageb_regression_commit_authorization_id_mismatch")
    require(regression_commit_authorization.get("human_authorization", {}).get("decision") == "authorized", "kds_stageb_regression_human_authorization_missing")
    require(regression_commit_authorization.get("authorized_execution", {}).get("exact_paths") == ["tests/test_knowledge_intake_api.py", "tests/test_knowledge_intake_postgres.py"], "kds_stageb_regression_authorized_paths_mismatch")
    require(regression_commit_authorization.get("authorized_execution", {}).get("commit_count") == 1, "kds_stageb_regression_commit_count_mismatch")
    require("push" in regression_commit_authorization.get("forbidden", []), "kds_stageb_regression_push_forbidden_missing")
    require("open_or_execute_later_unit" in regression_commit_authorization.get("forbidden", []), "kds_stageb_regression_later_unit_forbidden_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_authorization") == str(KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION.relative_to(ROOT)), "kds_stageb_regression_commit_authorization_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_authorization_sha256") == KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_SHA256, "kds_stageb_regression_commit_authorization_feature_sha_missing")
    regression_commit_receipt_text = read(KDS_STAGEB_REGRESSION_COMMIT_RECEIPT)
    require(hashlib.sha256(regression_commit_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_SHA256, "kds_stageb_regression_commit_receipt_sha_mismatch")
    regression_commit_receipt = yaml.safe_load(regression_commit_receipt_text).get("kds_stageb_regression_local_commit_receipt", {})
    require(regression_commit_receipt.get("id") == KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_ID, "kds_stageb_regression_commit_receipt_id_mismatch")
    require(regression_commit_receipt.get("commit", {}).get("sha") == "60957dd92380bfeb6049ec552658dad22d5d90dc", "kds_stageb_regression_commit_sha_mismatch")
    require(regression_commit_receipt.get("commit", {}).get("parent") == "7fb477030f5278faf55d6d16ff3874469704610d", "kds_stageb_regression_commit_parent_mismatch")
    require(regression_commit_receipt.get("commit", {}).get("path_count") == 2, "kds_stageb_regression_commit_path_count_mismatch")
    require(regression_commit_receipt.get("commit", {}).get("canonical_patch_bytes") == 38511, "kds_stageb_regression_commit_patch_bytes_mismatch")
    require(regression_commit_receipt.get("commit", {}).get("canonical_patch_sha256") == "1e7ecd30fbb740fcf2217224de107adb0c960d5babfc71aaaee036b9fae90f7e", "kds_stageb_regression_commit_patch_sha_mismatch")
    require(regression_commit_receipt.get("final_repository_state", {}).get("ahead") == 2, "kds_stageb_regression_final_ahead_mismatch")
    require(regression_commit_receipt.get("final_repository_state", {}).get("ordinary_dirty") == 179, "kds_stageb_regression_final_dirty_mismatch")
    require(regression_commit_receipt.get("final_repository_state", {}).get("opsx_lock") == "absent", "kds_stageb_regression_final_lock_present")
    require(regression_commit_receipt.get("authorization_boundary", {}).get("push") is False, "kds_stageb_regression_commit_receipt_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_receipt") == str(KDS_STAGEB_REGRESSION_COMMIT_RECEIPT.relative_to(ROOT)), "kds_stageb_regression_commit_receipt_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_receipt_sha256") == KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_SHA256, "kds_stageb_regression_commit_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_regression_local_commit_status") == "local_regression_commit_independent_review_passed", "kds_stageb_regression_independent_review_status_missing")
    openspec_preflight_text = read(KDS_STAGEB_OPENSPEC_PREFLIGHT)
    require(hashlib.sha256(openspec_preflight_text.encode("utf-8")).hexdigest() == KDS_STAGEB_OPENSPEC_PREFLIGHT_SHA256, "kds_stageb_openspec_preflight_sha_mismatch")
    openspec_preflight = yaml.safe_load(openspec_preflight_text).get("kds_stageb_openspec_preflight", {})
    require(openspec_preflight.get("id") == KDS_STAGEB_OPENSPEC_PREFLIGHT_ID, "kds_stageb_openspec_preflight_id_mismatch")
    require(openspec_preflight.get("dependency", {}).get("accepted_local_regression_commit") == "60957dd92380bfeb6049ec552658dad22d5d90dc", "kds_stageb_openspec_preflight_parent_mismatch")
    require(openspec_preflight.get("candidate_unit", {}).get("repository_write_allowlist") == [], "kds_stageb_openspec_preflight_write_allowlist_not_empty")
    require(len(openspec_preflight.get("candidate_unit", {}).get("source_paths", [])) == 9, "kds_stageb_openspec_preflight_path_count_mismatch")
    require(openspec_preflight.get("candidate_unit", {}).get("frozen_manifest_sha256") == "7acdd640e47a6892af715d57038b57de5747f84061cbf3f0034d5bef52dfdeed", "kds_stageb_openspec_manifest_sha_mismatch")
    require(openspec_preflight.get("authorization", {}).get("kds_repository_write") is False, "kds_stageb_openspec_repository_write_unexpectedly_authorized")
    require(openspec_preflight.get("authorization", {}).get("commit") is False, "kds_stageb_openspec_commit_unexpectedly_authorized")
    require(openspec_preflight.get("authorization", {}).get("push") is False, "kds_stageb_openspec_push_unexpectedly_authorized")
    require(openspec_preflight.get("dependency", {}).get("run_handoff_13") == "frozen_not_authorized", "kds_stageb_run_handoff_not_frozen")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_preflight") == str(KDS_STAGEB_OPENSPEC_PREFLIGHT.relative_to(ROOT)), "kds_stageb_openspec_preflight_feature_path_missing")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_preflight_sha256") == KDS_STAGEB_OPENSPEC_PREFLIGHT_SHA256, "kds_stageb_openspec_preflight_feature_sha_missing")
    openspec_preflight_receipt_text = read(KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT)
    require(hashlib.sha256(openspec_preflight_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_openspec_preflight_receipt_sha_mismatch")
    openspec_preflight_receipt = yaml.safe_load(openspec_preflight_receipt_text).get("kds_stageb_openspec_preflight_receipt", {})
    require(openspec_preflight_receipt.get("id") == KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_ID, "kds_stageb_openspec_preflight_receipt_id_mismatch")
    require(openspec_preflight_receipt.get("candidate", {}).get("patch_bytes") == 54462, "kds_stageb_openspec_patch_bytes_mismatch")
    require(openspec_preflight_receipt.get("candidate", {}).get("patch_sha256") == "7754cef4b7fd12218069c106276841a59594f53cb5162cd5ab152c35faf9994c", "kds_stageb_openspec_patch_sha_mismatch")
    require(openspec_preflight_receipt.get("verification", {}).get("openspec_strict") == "pass", "kds_stageb_openspec_strict_not_passed")
    require(openspec_preflight_receipt.get("verification", {}).get("paths_absent_after_reverse") == 9, "kds_stageb_openspec_reverse_restore_failed")
    require(openspec_preflight_receipt.get("verification", {}).get("disposable_root_count_after") == 0, "kds_stageb_openspec_root_cleanup_failed")
    require(openspec_preflight_receipt.get("authorization_boundary", {}).get("commit") is False, "kds_stageb_openspec_receipt_commit_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_preflight_receipt_sha256") == KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_openspec_preflight_receipt_feature_sha_missing")
    openspec_commit_request_text = read(KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST)
    require(hashlib.sha256(openspec_commit_request_text.encode("utf-8")).hexdigest() == KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_openspec_commit_request_sha_mismatch")
    openspec_commit_request = yaml.safe_load(openspec_commit_request_text).get("kds_stageb_openspec_local_commit_authorization_request", {})
    require(openspec_commit_request.get("id") == KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_ID, "kds_stageb_openspec_commit_request_id_mismatch")
    require(openspec_commit_request.get("requested_execution", {}).get("commit_count") == 1, "kds_stageb_openspec_commit_count_mismatch")
    require(len(openspec_commit_request.get("requested_execution", {}).get("exact_paths", [])) == 9, "kds_stageb_openspec_commit_path_count_mismatch")
    require(openspec_commit_request.get("human_decision", {}).get("local_commit") == "pending", "kds_stageb_openspec_commit_unexpectedly_authorized")
    require(openspec_commit_request.get("human_decision", {}).get("push") is False, "kds_stageb_openspec_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_local_commit_authorization_request_sha256") == KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_openspec_commit_request_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_preflight_status") == "openspec9_preflight_independent_review_passed_human_local_commit_authorization_required", "kds_stageb_openspec_preflight_status_mismatch")
    openspec_commit_authorization_text = read(KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION)
    require(hashlib.sha256(openspec_commit_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_SHA256, "kds_stageb_openspec_commit_authorization_sha_mismatch")
    openspec_commit_authorization = yaml.safe_load(openspec_commit_authorization_text).get("kds_stageb_openspec_local_commit_authorization", {})
    require(openspec_commit_authorization.get("id") == KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_ID, "kds_stageb_openspec_commit_authorization_id_mismatch")
    require(openspec_commit_authorization.get("human_authorization_receipt", {}).get("decision") == "granted", "kds_stageb_openspec_human_authorization_missing")
    require(openspec_commit_authorization.get("authorized_execution", {}).get("commit_count") == 1, "kds_stageb_openspec_authorized_commit_count_mismatch")
    require(openspec_commit_authorization.get("authorized_execution", {}).get("exact_path_count") == 9, "kds_stageb_openspec_authorized_path_count_mismatch")
    require("push" in openspec_commit_authorization.get("forbidden", []), "kds_stageb_openspec_authorization_push_forbidden_missing")
    require("stageb_run_handoff_13" in openspec_commit_authorization.get("forbidden", []), "kds_stageb_run_handoff_authorization_forbidden_missing")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_local_commit_authorization_sha256") == KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_SHA256, "kds_stageb_openspec_commit_authorization_feature_sha_missing")
    openspec_commit_receipt_text = read(KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT)
    require(hashlib.sha256(openspec_commit_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_SHA256, "kds_stageb_openspec_commit_receipt_sha_mismatch")
    openspec_commit_receipt = yaml.safe_load(openspec_commit_receipt_text).get("kds_stageb_openspec_local_commit_receipt", {})
    require(openspec_commit_receipt.get("id") == KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_ID, "kds_stageb_openspec_commit_receipt_id_mismatch")
    require(openspec_commit_receipt.get("commit", {}).get("sha") == "a7ec87412f03fb18a9f52e11f07980e6911f22a1", "kds_stageb_openspec_commit_sha_mismatch")
    require(openspec_commit_receipt.get("commit", {}).get("parent") == "60957dd92380bfeb6049ec552658dad22d5d90dc", "kds_stageb_openspec_commit_parent_mismatch")
    require(openspec_commit_receipt.get("commit", {}).get("path_count") == 9, "kds_stageb_openspec_commit_receipt_path_count_mismatch")
    require(openspec_commit_receipt.get("commit", {}).get("canonical_patch_bytes") == 54462, "kds_stageb_openspec_commit_receipt_patch_bytes_mismatch")
    require(openspec_commit_receipt.get("final_repository_state", {}).get("ahead") == 3, "kds_stageb_openspec_final_ahead_mismatch")
    require(openspec_commit_receipt.get("final_repository_state", {}).get("ordinary_dirty") == 178, "kds_stageb_openspec_final_dirty_mismatch")
    require(openspec_commit_receipt.get("final_repository_state", {}).get("opsx_lock") == "absent", "kds_stageb_openspec_final_lock_present")
    require(openspec_commit_receipt.get("authorization_boundary", {}).get("push") is False, "kds_stageb_openspec_commit_receipt_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_local_commit_receipt_sha256") == KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_SHA256, "kds_stageb_openspec_commit_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_local_commit_authorization_status") == "local_openspec9_commit_independent_review_passed", "kds_stageb_openspec_commit_review_status_mismatch")
    require(feature.get("coordination", {}).get("kds_stageb_openspec_local_commit_review") == "local_openspec9_commit_independent_review_passed", "kds_stageb_openspec_commit_review_missing")
    run_handoff_preflight_text = read(KDS_STAGEB_RUN_HANDOFF_PREFLIGHT)
    require(hashlib.sha256(run_handoff_preflight_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_SHA256, "kds_stageb_run_handoff_preflight_sha_mismatch")
    run_handoff_preflight = yaml.safe_load(run_handoff_preflight_text).get("kds_stageb_run_handoff_preflight", {})
    require(run_handoff_preflight.get("id") == KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_ID, "kds_stageb_run_handoff_preflight_id_mismatch")
    require(run_handoff_preflight.get("baseline", {}).get("head") == "a7ec87412f03fb18a9f52e11f07980e6911f22a1", "kds_stageb_run_handoff_preflight_head_mismatch")
    require(run_handoff_preflight.get("candidate_unit", {}).get("repository_write_allowlist") == [], "kds_stageb_run_handoff_preflight_allowlist_not_empty")
    require(len(run_handoff_preflight.get("candidate_unit", {}).get("source_paths", [])) == 13, "kds_stageb_run_handoff_preflight_path_count_mismatch")
    require(run_handoff_preflight.get("candidate_unit", {}).get("frozen_manifest_sha256") == "9505cf98726d0148b0124022f4dca502837b82ec74e10a262daed29f15881e47", "kds_stageb_run_handoff_manifest_mismatch")
    require(run_handoff_preflight.get("authorization", {}).get("commit") is False and run_handoff_preflight.get("authorization", {}).get("push") is False, "kds_stageb_run_handoff_git_write_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_preflight_sha256") == KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_SHA256, "kds_stageb_run_handoff_feature_sha_missing")
    run_handoff_receipt_text = read(KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT)
    require(hashlib.sha256(run_handoff_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_run_handoff_receipt_sha_mismatch")
    run_handoff_receipt = yaml.safe_load(run_handoff_receipt_text).get("kds_stageb_run_handoff_preflight_receipt", {})
    require(run_handoff_receipt.get("id") == KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_ID, "kds_stageb_run_handoff_receipt_id_mismatch")
    require(run_handoff_receipt.get("candidate", {}).get("patch_bytes") == 37909, "kds_stageb_run_handoff_patch_bytes_mismatch")
    require(run_handoff_receipt.get("candidate", {}).get("patch_sha256") == "5bcd1e02139a84294c116ec35bdca9247c8125d941a250e0989cbbc0b2a7a235", "kds_stageb_run_handoff_patch_sha_mismatch")
    require(run_handoff_receipt.get("verification", {}).get("diff_check") == "fail", "kds_stageb_run_handoff_diffcheck_failure_missing")
    require(run_handoff_receipt.get("blocking_finding", {}).get("path", "").endswith("evidence/canonical-mirror-sha256.txt"), "kds_stageb_run_handoff_blocking_path_mismatch")
    require(run_handoff_receipt.get("authorization_boundary", {}).get("commit") is False and run_handoff_receipt.get("authorization_boundary", {}).get("push") is False, "kds_stageb_run_handoff_receipt_git_write_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_preflight_receipt_sha256") == KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_run_handoff_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_preflight_status") == "stageb_run_handoff_13_preflight_rework_required_single_eof_newline", "kds_stageb_run_handoff_status_mismatch")
    require("stageb_run_handoff_13_preflight_rework_required_single_eof_newline" in read(KDS_STAGEB_RUN_HANDOFF_EVIDENCE), "kds_stageb_run_handoff_f013_review_missing")
    eof_rework_text = read(KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST)
    require(hashlib.sha256(eof_rework_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST_SHA256, "kds_stageb_run_handoff_eof_rework_request_sha_mismatch")
    eof_rework = yaml.safe_load(eof_rework_text).get("kds_stageb_run_handoff_eof_rework_authorization_request", {})
    require(eof_rework.get("id") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST_ID, "kds_stageb_run_handoff_eof_rework_request_id_mismatch")
    require(eof_rework.get("mode") == "human_authorization_request_only", "kds_stageb_run_handoff_eof_rework_mode_mismatch")
    require(eof_rework.get("requested_execution", {}).get("repository_write_path_count") == 1, "kds_stageb_run_handoff_eof_rework_scope_mismatch")
    require(eof_rework.get("requested_execution", {}).get("commit") is False and eof_rework.get("requested_execution", {}).get("push") is False, "kds_stageb_run_handoff_eof_rework_git_write_authorized")
    require(eof_rework.get("human_decision", {}).get("one_byte_source_edit") == "pending", "kds_stageb_run_handoff_eof_rework_human_decision_drift")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_authorization_request_sha256") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_REQUEST_SHA256, "kds_stageb_run_handoff_eof_rework_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_authorization_status") == "authorization_request_review_passed_human_one_byte_rework_authorization_required", "kds_stageb_run_handoff_eof_rework_review_status_mismatch")
    eof_hardening_text = read(KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING)
    require(hashlib.sha256(eof_hardening_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING_SHA256, "kds_stageb_run_handoff_eof_hardening_sha_mismatch")
    eof_hardening = yaml.safe_load(eof_hardening_text).get("kds_stageb_run_handoff_eof_rework_hash_hardening", {})
    require(eof_hardening.get("id") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING_ID, "kds_stageb_run_handoff_eof_hardening_id_mismatch")
    require(eof_hardening.get("exact_target", {}).get("before_sha256") == "a90228ec94735c60c0834f47c40a96b2bb6365fba88b616a362e8d6060955478", "kds_stageb_run_handoff_eof_preimage_hash_mismatch")
    require(eof_hardening.get("exact_target", {}).get("after_sha256") == "4fa7ea7c7d46b7f392f50dd1f702dba4b8da93f024c8480ea1ef38b902f6bd67", "kds_stageb_run_handoff_eof_postimage_hash_mismatch")
    require(eof_hardening.get("authorization_boundary", {}).get("one_byte_edit") == "pending_human_decision", "kds_stageb_run_handoff_eof_hardening_authorization_drift")
    require(eof_hardening.get("authorization_boundary", {}).get("commit") is False and eof_hardening.get("authorization_boundary", {}).get("push") is False, "kds_stageb_run_handoff_eof_hardening_git_write_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_hash_hardening_sha256") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_HARDENING_SHA256, "kds_stageb_run_handoff_eof_hardening_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_hash_hardening_status") == "authorization_request_metadata_hardening_review_passed_human_one_byte_rework_authorization_required", "kds_stageb_run_handoff_eof_hardening_status_mismatch")
    baseline_text = read(KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION)
    require(hashlib.sha256(baseline_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_SHA256, "kds_stageb_run_handoff_eof_baseline_sha_mismatch")
    baseline = yaml.safe_load(baseline_text).get("kds_stageb_run_handoff_eof_baseline_reconciliation", {})
    require(baseline.get("id") == KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_ID, "kds_stageb_run_handoff_eof_baseline_id_mismatch")
    require(baseline.get("human_authorization_receipt", {}).get("decision") == "granted", "kds_stageb_run_handoff_eof_human_authorization_missing")
    require(baseline.get("observed_preexecution_snapshot", {}).get("ordinary_dirty") == 191, "kds_stageb_run_handoff_eof_baseline_dirty_mismatch")
    require(baseline.get("drift", {}).get("expanded_leaf_files_added") == 20, "kds_stageb_run_handoff_eof_drift_count_mismatch")
    execution_text = read(KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION)
    require(hashlib.sha256(execution_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_SHA256, "kds_stageb_run_handoff_eof_execution_sha_mismatch")
    execution = yaml.safe_load(execution_text).get("kds_stageb_run_handoff_eof_rework_execution", {})
    require(execution.get("id") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_ID, "kds_stageb_run_handoff_eof_execution_id_mismatch")
    require(execution.get("exact_edit", {}).get("after_sha256") == "4fa7ea7c7d46b7f392f50dd1f702dba4b8da93f024c8480ea1ef38b902f6bd67", "kds_stageb_run_handoff_eof_execution_postimage_mismatch")
    require(execution.get("execution", {}).get("stage") is False and execution.get("execution", {}).get("commit") is False and execution.get("execution", {}).get("push") is False, "kds_stageb_run_handoff_eof_execution_git_write_authorized")
    receipt_text = read(KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT)
    require(hashlib.sha256(receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_SHA256, "kds_stageb_run_handoff_eof_receipt_sha_mismatch")
    receipt = yaml.safe_load(receipt_text).get("kds_stageb_run_handoff_eof_rework_receipt", {})
    require(receipt.get("id") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_ID, "kds_stageb_run_handoff_eof_receipt_id_mismatch")
    require(receipt.get("corrected_preflight", {}).get("ordered_manifest_sha256") == "11a373670ba3a9d01c12fdd5aab7ca7aabb3accd1008e98f7c11a269bac666bc", "kds_stageb_run_handoff_corrected_manifest_mismatch")
    require(receipt.get("corrected_preflight", {}).get("deterministic_patch_sha256") == "00a37e1e7a1d480896aa904257deaa35f685e052fbc16ace132c708c9c3dac83", "kds_stageb_run_handoff_corrected_patch_mismatch")
    require(receipt.get("corrected_preflight", {}).get("diff_check") == "pass", "kds_stageb_run_handoff_corrected_diffcheck_failed")
    require(receipt.get("independent_review", {}).get("execution_and_preflight") == "one_byte_rework_and_corrected_report_only_preflight_independent_review_passed", "kds_stageb_run_handoff_corrected_review_missing")
    require(receipt.get("authorization_boundary", {}).get("future_13_file_local_commit_requires_separate_human_authorization") is True, "kds_stageb_run_handoff_future_commit_boundary_missing")
    require(receipt.get("authorization_boundary", {}).get("stage") is False and receipt.get("authorization_boundary", {}).get("commit") is False and receipt.get("authorization_boundary", {}).get("push") is False, "kds_stageb_run_handoff_receipt_git_write_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_baseline_reconciliation_sha256") == KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_SHA256, "kds_stageb_run_handoff_eof_baseline_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_execution_sha256") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_SHA256, "kds_stageb_run_handoff_eof_execution_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_receipt_sha256") == KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_SHA256, "kds_stageb_run_handoff_eof_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_eof_rework_status") == "one_byte_rework_and_corrected_report_only_preflight_independent_review_passed", "kds_stageb_run_handoff_eof_current_status_mismatch")
    require("one_byte_rework_and_corrected_report_only_preflight_independent_review_passed" in read(KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EVIDENCE), "kds_stageb_run_handoff_eof_review_evidence_missing")
    commit_request_text = read(KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST)
    require(hashlib.sha256(commit_request_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_SHA256, "kds_stageb_run_handoff_commit_request_sha_mismatch")
    commit_request = yaml.safe_load(commit_request_text).get("kds_stageb_run_handoff_local_commit_authorization_request", {})
    require(commit_request.get("id") == KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_ID, "kds_stageb_run_handoff_commit_request_id_mismatch")
    require(commit_request.get("mode") == "human_authorization_request_only", "kds_stageb_run_handoff_commit_request_mode_mismatch")
    require(commit_request.get("hard_stop_baseline", {}).get("head") == "a7ec87412f03fb18a9f52e11f07980e6911f22a1", "kds_stageb_run_handoff_commit_request_head_mismatch")
    require(commit_request.get("hard_stop_baseline", {}).get("ordinary_dirty") == 191 and commit_request.get("hard_stop_baseline", {}).get("expanded_dirty") == 462, "kds_stageb_run_handoff_commit_request_dirty_mismatch")
    require(commit_request.get("hard_stop_baseline", {}).get("staged") == 0 and commit_request.get("hard_stop_baseline", {}).get("opsx_lock") == "absent", "kds_stageb_run_handoff_commit_request_index_or_lock_mismatch")
    require(commit_request.get("exact_unit", {}).get("path_count") == 13, "kds_stageb_run_handoff_commit_request_path_count_mismatch")
    require(commit_request.get("exact_unit", {}).get("sorted_nul_pathset_sha256") == "dee9d08e3189096993c3cc6769bc650f9e1849cbab114ce51af22ed00ed2a525", "kds_stageb_run_handoff_commit_request_pathset_mismatch")
    require(commit_request.get("exact_unit", {}).get("ordered_manifest_sha256") == "11a373670ba3a9d01c12fdd5aab7ca7aabb3accd1008e98f7c11a269bac666bc", "kds_stageb_run_handoff_commit_request_manifest_mismatch")
    require(commit_request.get("exact_unit", {}).get("canonical_patch_bytes") == 37907 and commit_request.get("exact_unit", {}).get("canonical_patch_sha256") == "00a37e1e7a1d480896aa904257deaa35f685e052fbc16ace132c708c9c3dac83", "kds_stageb_run_handoff_commit_request_patch_mismatch")
    require(commit_request.get("exact_unit", {}).get("proposed_commit_subject") == "chore(kds): record document extraction handoff", "kds_stageb_run_handoff_commit_request_subject_mismatch")
    require(commit_request.get("authorization", {}).get("KDS_stage") == "false_pending_human_authorization" and commit_request.get("authorization", {}).get("KDS_local_commit") == "false_pending_human_authorization", "kds_stageb_run_handoff_commit_prematurely_authorized")
    require(commit_request.get("authorization", {}).get("push") is False, "kds_stageb_run_handoff_commit_request_push_authorized")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_local_commit_authorization_request_sha256") == KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_SHA256, "kds_stageb_run_handoff_commit_request_feature_sha_missing")
    require("No staging or commit is authorized by this request itself" in read(KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_EVIDENCE), "kds_stageb_run_handoff_commit_request_boundary_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_local_commit_authorization_status") == "authorization_request_review_passed_human_13_file_local_commit_authorization_required", "kds_stageb_run_handoff_commit_request_review_status_mismatch")
    require("authorization_request_review_passed_human_13_file_local_commit_authorization_required" in read(KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_EVIDENCE), "kds_stageb_run_handoff_commit_request_review_evidence_missing")
    commit_authorization_text = read(KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION)
    require(hashlib.sha256(commit_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION_SHA256, "kds_stageb_run_handoff_commit_authorization_sha_mismatch")
    commit_authorization = yaml.safe_load(commit_authorization_text).get("kds_stageb_run_handoff_local_commit_authorization", {})
    require(commit_authorization.get("id") == KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION_ID, "kds_stageb_run_handoff_commit_authorization_id_mismatch")
    require(commit_authorization.get("human_authorization_receipt", {}).get("decision") == "granted", "kds_stageb_run_handoff_human_authorization_missing")
    require(commit_authorization.get("authorized_execution", {}).get("exact_path_count") == 13, "kds_stageb_run_handoff_authorized_path_count_mismatch")
    require(commit_authorization.get("authorized_execution", {}).get("canonical_patch_sha256") == "00a37e1e7a1d480896aa904257deaa35f685e052fbc16ace132c708c9c3dac83", "kds_stageb_run_handoff_authorized_patch_mismatch")
    commit_receipt_text = read(KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT)
    require(hashlib.sha256(commit_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT_SHA256, "kds_stageb_run_handoff_commit_receipt_sha_mismatch")
    commit_receipt = yaml.safe_load(commit_receipt_text).get("kds_stageb_run_handoff_local_commit_receipt", {})
    require(commit_receipt.get("id") == KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT_ID, "kds_stageb_run_handoff_commit_receipt_id_mismatch")
    require(commit_receipt.get("commit", {}).get("sha") == "690ea04abf5485563b760d1bc1620493db017662", "kds_stageb_run_handoff_commit_sha_mismatch")
    require(commit_receipt.get("verification", {}).get("f013_review") == "local_stageb_run_handoff_13_commit_independent_review_passed", "kds_stageb_run_handoff_commit_review_missing")
    require(commit_receipt.get("authorization_boundary", {}).get("push") is False and commit_receipt.get("authorization_boundary", {}).get("later_unit") is False, "kds_stageb_run_handoff_postcommit_boundary_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_local_commit_authorization_sha256") == KDS_STAGEB_RUN_HANDOFF_COMMIT_AUTHORIZATION_SHA256, "kds_stageb_run_handoff_commit_authorization_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_local_commit_receipt_sha256") == KDS_STAGEB_RUN_HANDOFF_COMMIT_RECEIPT_SHA256, "kds_stageb_run_handoff_commit_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_run_handoff_local_commit_status") == "local_stageb_run_handoff_13_commit_independent_review_passed", "kds_stageb_run_handoff_commit_current_status_mismatch")
    require("local_stageb_run_handoff_13_commit_independent_review_passed" in read(KDS_STAGEB_RUN_HANDOFF_COMMIT_EVIDENCE), "kds_stageb_run_handoff_commit_evidence_missing")
    push_preflight_text = read(KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT)
    require(hashlib.sha256(push_preflight_text.encode("utf-8")).hexdigest() == KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_SHA256, "kds_stageb_push_preflight_sha_mismatch")
    push_preflight = yaml.safe_load(push_preflight_text).get("kds_stageb_four_commit_push_preflight", {})
    require(push_preflight.get("id") == KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_ID, "kds_stageb_push_preflight_id_mismatch")
    require(push_preflight.get("human_authorization_receipt", {}).get("decision") == "granted_for_read_only_preflight_only", "kds_stageb_push_preflight_authorization_boundary_missing")
    require(push_preflight.get("expected_remote", {}).get("sha") == "f28edb5113e0493ed60fec423cb6c7e1a6252de8", "kds_stageb_push_preflight_remote_mismatch")
    require(push_preflight.get("expected_local", {}).get("head") == "690ea04abf5485563b760d1bc1620493db017662", "kds_stageb_push_preflight_head_mismatch")
    require(push_preflight.get("expected_local", {}).get("ahead") == 4 and push_preflight.get("expected_local", {}).get("behind") == 0, "kds_stageb_push_preflight_ahead_behind_mismatch")
    require(len(push_preflight.get("exact_commit_sequence_oldest_to_newest", [])) == 4, "kds_stageb_push_preflight_commit_count_mismatch")
    require(push_preflight.get("status", {}).get("push") == "unauthorized", "kds_stageb_push_preflight_premature_push_authorization")
    push_preflight_receipt_text = read(KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT)
    require(hashlib.sha256(push_preflight_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_push_preflight_receipt_sha_mismatch")
    push_preflight_receipt = yaml.safe_load(push_preflight_receipt_text).get("kds_stageb_four_commit_push_preflight_receipt", {})
    require(push_preflight_receipt.get("id") == KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_ID, "kds_stageb_push_preflight_receipt_id_mismatch")
    require(push_preflight_receipt.get("commit_topology", {}).get("rev_list_count") == 4 and push_preflight_receipt.get("commit_topology", {}).get("additional_commits") == 0, "kds_stageb_push_preflight_receipt_topology_mismatch")
    require(push_preflight_receipt.get("push_dry_run", {}).get("result") == "pass" and push_preflight_receipt.get("remote_verification", {}).get("unchanged") is True, "kds_stageb_push_preflight_dry_run_or_remote_mismatch")
    require(push_preflight_receipt.get("result", {}).get("classification") == "push_preflight_passed_separate_exact_push_authorization_required" and push_preflight_receipt.get("result", {}).get("push_authorized") is False, "kds_stageb_push_preflight_receipt_boundary_mismatch")
    push_request_text = read(KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST)
    require(hashlib.sha256(push_request_text.encode("utf-8")).hexdigest() == KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_push_request_sha_mismatch")
    push_request = yaml.safe_load(push_request_text).get("kds_stageb_four_commit_push_authorization_request", {})
    require(push_request.get("id") == KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_ID, "kds_stageb_push_request_id_mismatch")
    require(push_request.get("request_state", {}).get("decision") == "pending_human_authorization" and push_request.get("request_state", {}).get("push_authorized") is False, "kds_stageb_push_request_premature_authorization")
    require(push_request.get("requested_operation", {}).get("exact_command") == "git push origin 690ea04abf5485563b760d1bc1620493db017662:refs/heads/main", "kds_stageb_push_request_command_mismatch")
    require(push_request.get("requested_operation", {}).get("force") is False, "kds_stageb_push_request_force_mismatch")
    push_authorization_text = read(KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION)
    require(hashlib.sha256(push_authorization_text.encode("utf-8")).hexdigest() == KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_SHA256, "kds_stageb_push_authorization_sha_mismatch")
    push_authorization = yaml.safe_load(push_authorization_text).get("kds_stageb_four_commit_push_authorization", {})
    require(push_authorization.get("id") == KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_ID, "kds_stageb_push_authorization_id_mismatch")
    require(push_authorization.get("human_authorization_receipt", {}).get("decision") == "granted", "kds_stageb_push_human_authorization_missing")
    require(push_authorization.get("authorized_execution", {}).get("exact_command") == "git push origin 690ea04abf5485563b760d1bc1620493db017662:refs/heads/main", "kds_stageb_push_authorized_command_mismatch")
    require(push_authorization.get("authorized_execution", {}).get("force") is False, "kds_stageb_push_authorized_force_mismatch")
    push_receipt_text = read(KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT)
    require(hashlib.sha256(push_receipt_text.encode("utf-8")).hexdigest() == KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_SHA256, "kds_stageb_push_receipt_sha_mismatch")
    push_receipt = yaml.safe_load(push_receipt_text).get("kds_stageb_four_commit_push_receipt", {})
    require(push_receipt.get("id") == KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_ID, "kds_stageb_push_receipt_id_mismatch")
    require(push_receipt.get("execution", {}).get("push_count") == 1 and push_receipt.get("execution", {}).get("result") == "pass", "kds_stageb_push_execution_receipt_mismatch")
    require(push_receipt.get("execution", {}).get("force") is False, "kds_stageb_push_execution_force_mismatch")
    require(push_receipt.get("post_push", {}).get("remote_main") == "690ea04abf5485563b760d1bc1620493db017662", "kds_stageb_push_remote_result_mismatch")
    require(push_receipt.get("post_push", {}).get("head") == "690ea04abf5485563b760d1bc1620493db017662", "kds_stageb_push_head_result_mismatch")
    require(push_receipt.get("post_push", {}).get("ahead") == 0 and push_receipt.get("post_push", {}).get("behind") == 0, "kds_stageb_push_post_ahead_behind_mismatch")
    require(push_receipt.get("post_push", {}).get("ordinary_porcelain_nul_sha256") == "d703cec1120da778795cf51ef33f51e66b791c6de9868b3b975a3fb2d6e08be3", "kds_stageb_push_ordinary_dirty_hash_mismatch")
    require(push_receipt.get("post_push", {}).get("expanded_porcelain_nul_sha256") == "631473d7122cebec505283a9476bf9a29053dae7da53c27635296d5ca7cb58b1", "kds_stageb_push_expanded_dirty_hash_mismatch")
    require(push_receipt.get("review", {}).get("f013") == "kds_stageb_four_commit_exact_non_force_push_independent_postpush_review_passed", "kds_stageb_push_f013_review_missing")
    require(push_receipt.get("authorization_boundary_receipt", {}).get("force_push") is False and push_receipt.get("authorization_boundary_receipt", {}).get("later_unit") is False, "kds_stageb_push_post_boundary_missing")
    require(feature.get("coordination", {}).get("kds_stageb_four_commit_push_preflight_sha256") == KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_SHA256, "kds_stageb_push_preflight_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_four_commit_push_preflight_receipt_sha256") == KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_SHA256, "kds_stageb_push_preflight_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_four_commit_push_authorization_request_sha256") == KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_SHA256, "kds_stageb_push_request_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_four_commit_push_authorization_sha256") == KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_SHA256, "kds_stageb_push_authorization_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_four_commit_push_receipt_sha256") == KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_SHA256, "kds_stageb_push_receipt_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_stageb_four_commit_push_status") == "kds_stageb_four_commit_exact_non_force_push_independent_postpush_review_passed", "kds_stageb_push_status_mismatch")
    require("push_preflight_independent_review_passed_separate_exact_push_authorization_required" in read(KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_EVIDENCE), "kds_stageb_push_preflight_review_evidence_missing")
    require("kds_stageb_four_commit_exact_non_force_push_independent_postpush_review_passed" in read(KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_EVIDENCE), "kds_stageb_push_postreview_evidence_missing")
    require("kds_stageb_four_commit_push_pending_separate_human_authorization" not in feature.get("blockers", []), "kds_stageb_push_human_authorization_blocker_stale")
    expected_dispatch = "studio_frozen_brain_a10p1t4_passed_mmc_h1r3_verified_kds_stageb_four_commits_pushed_postpush_review_passed"
    require(feature.get("coordination", {}).get("dispatch_status") == expected_dispatch, "dispatch_status_mismatch")
    require(f"dispatch_status: {expected_dispatch}" in read(CONTROL_BOARD), "control_board_dispatch_missing")
    require(KDS_DIRTY_ISOLATION_COORDINATION_ID in read(SESSION_REGISTRY), "kds_dirty_isolation_session_change_missing")
    closure_text = read(A10I1R1_CLOSURE_EVIDENCE)
    require("914909d2e15f15ce6dc869f3372934ffee157f64934842e7b613a6b287db6111" in closure_text, "a10i1r1_patch_hash_missing")
    require("632 files, 5326 nodes and 13240 edges" in closure_text, "a10i1r1_codegraph_receipt_missing")
    require("A10I1 KDS+Studio first implementation batch joint serial gate = closed" in closure_text, "a10i1r1_serial_gate_closure_missing")

    current_state_text = read(RELEASE0_CURRENT_STATE_REVALIDATION)
    require(hashlib.sha256(current_state_text.encode("utf-8")).hexdigest() == RELEASE0_CURRENT_STATE_REVALIDATION_SHA256, "release0_current_state_sha_mismatch")
    current_state = yaml.safe_load(current_state_text).get("gke001_release0_current_state_readonly_revalidation", {})
    require(current_state.get("id") == RELEASE0_CURRENT_STATE_REVALIDATION_ID, "release0_current_state_id_mismatch")
    require(current_state.get("program") == "GKE-001" and current_state.get("feature_ref") == "F-013", "release0_current_state_scope_mismatch")
    require(current_state.get("canonical_manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "release0_current_state_manifest_mismatch")
    current_lanes = current_state.get("lanes", [])
    require(len(current_lanes) == 3, "release0_current_state_lane_count_mismatch")
    require({lane.get("thread_id") for lane in current_lanes} == set(LANE_THREADS.values()), "release0_current_state_thread_set_mismatch")
    require(all(lane.get("repository_allowlist") == [] for lane in current_lanes), "release0_current_state_allowlist_not_empty")
    require(current_state.get("authorization", {}).get("release0_product_test_12_local_commit") is False, "release0_current_state_commit_boundary_mismatch")
    require(current_state.get("authorization", {}).get("mmc_source_or_policy_write") is False, "release0_current_state_mmc_write_boundary_mismatch")
    require(current_state.get("authorization", {}).get("real_e2e") is False, "release0_current_state_e2e_boundary_mismatch")

    current_handoff_text = read(RELEASE0_CURRENT_STATE_HANDOFF)
    require(hashlib.sha256(current_handoff_text.encode("utf-8")).hexdigest() == RELEASE0_CURRENT_STATE_HANDOFF_SHA256, "release0_current_state_handoff_sha_mismatch")
    current_handoff = yaml.safe_load(current_handoff_text).get("knowledge_engineering_handoff", {})
    require(current_handoff.get("id") == RELEASE0_CURRENT_STATE_HANDOFF_ID, "release0_current_state_handoff_id_mismatch")
    require(current_handoff.get("predecessor", {}).get("sha256") == RELEASE0_CURRENT_STATE_REVALIDATION_SHA256, "release0_current_state_handoff_predecessor_mismatch")
    require(current_handoff.get("classification", {}).get("release0_e2e") == "blocked_by_kds_commit_and_mmc_policy_admission", "release0_current_state_serial_blocker_mismatch")
    require(current_handoff.get("authorization_boundary", {}).get("commit") is False, "release0_current_state_handoff_commit_boundary_mismatch")
    require(current_handoff.get("authorization_boundary", {}).get("mmc_policy_write") is False, "release0_current_state_handoff_policy_boundary_mismatch")
    require(current_handoff.get("authorization_boundary", {}).get("live_e2e") is False, "release0_current_state_handoff_e2e_boundary_mismatch")
    require(feature.get("coordination", {}).get("release0_current_state_revalidation_sha256") == RELEASE0_CURRENT_STATE_REVALIDATION_SHA256, "release0_current_state_feature_sha_missing")
    require(feature.get("coordination", {}).get("release0_current_state_handoff_sha256") == RELEASE0_CURRENT_STATE_HANDOFF_SHA256, "release0_current_state_handoff_feature_sha_missing")
    review_closure_text = read(RELEASE0_CURRENT_STATE_REVIEW_CLOSURE)
    require(hashlib.sha256(review_closure_text.encode("utf-8")).hexdigest() == RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_SHA256, "release0_current_state_review_closure_sha_mismatch")
    review_closure = yaml.safe_load(review_closure_text).get("gke001_release0_current_state_independent_review_closure", {})
    require(review_closure.get("id") == RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_ID, "release0_current_state_review_closure_id_mismatch")
    require(review_closure.get("independent_review", {}).get("classification") == "kds_local_commit_request_eligible_only", "release0_current_state_review_classification_mismatch")
    require(review_closure.get("authorization_eligibility", {}).get("kds_product_test_12_local_commit") == "eligible_to_request_human_authorization", "release0_kds_commit_request_not_eligible")
    require(review_closure.get("authorization_eligibility", {}).get("mmc_source_policy_owner_commit") == "not_eligible_yet", "release0_mmc_commit_unexpectedly_eligible")
    require(review_closure.get("lock_semantics_correction", {}).get("mmc_opsx_lock") == "absent", "release0_mmc_opsx_lock_semantics_mismatch")
    require(review_closure.get("lock_semantics_correction", {}).get("mmc_runtime_sidecar_lock", {}).get("state") == "present", "release0_mmc_runtime_sidecar_lock_missing")
    commit_request_text = read(KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST)
    require(hashlib.sha256(commit_request_text.encode("utf-8")).hexdigest() == KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_SHA256, "release0_kds_commit_request_sha_mismatch")
    commit_request = yaml.safe_load(commit_request_text).get("gke001_kds_release0_product_test_local_commit_request", {})
    require(commit_request.get("id") == KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_ID, "release0_kds_commit_request_id_mismatch")
    require(commit_request.get("requested_human_decision", {}).get("decision") == "pending", "release0_kds_commit_request_unexpectedly_authorized")
    require(commit_request.get("sealed_candidate", {}).get("path_count") == 12, "release0_kds_commit_request_path_count_mismatch")
    require(commit_request.get("sealed_candidate", {}).get("patch_sha256") == "1ef8ee7b5553defd5d94ccb4d7f95f60729a608f0d9700bc3c1821a4c7b56fc4", "release0_kds_commit_request_patch_mismatch")
    require(commit_request.get("required_baseline", {}).get("ordinary_dirty") == 191 and commit_request.get("required_baseline", {}).get("expanded_dirty") == 450, "release0_kds_commit_request_dirty_baseline_mismatch")
    require(commit_request.get("requested_human_decision", {}).get("push") is False, "release0_kds_commit_request_push_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("release0_current_state_independent_review_closure_sha256") == RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_SHA256, "release0_current_state_review_closure_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_release0_product_test_local_commit_request_sha256") == KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_SHA256, "release0_kds_commit_request_feature_sha_missing")
    require(feature.get("coordination", {}).get("release0_current_state_status") == "independent_readonly_review_passed_kds_local_commit_request_eligible_only", "release0_current_state_review_status_mismatch")
    require(feature.get("coordination", {}).get("kds_release0_product_test_local_commit_request_status") == "human_local_commit_authorization_required", "release0_kds_commit_request_status_mismatch")
    localization_repair_text = read(LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR)
    require(hashlib.sha256(localization_repair_text.encode("utf-8")).hexdigest() == LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_SHA256, "localization_feature_evidence_boundary_repair_sha_mismatch")
    localization_repair = yaml.safe_load(localization_repair_text).get("gke001_localization_feature_evidence_boundary_repair", {})
    require(localization_repair.get("id") == LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_ID, "localization_feature_evidence_boundary_repair_id_mismatch")
    require(localization_repair.get("boundary", {}).get("immutable_feature_evidence_scanned") is False, "immutable_feature_evidence_still_scanned")
    require(localization_repair.get("boundary", {}).get("feature_journal_scanned") is True, "feature_journal_scan_boundary_missing")
    require(localization_repair.get("verification", {}).get("localization_gate", {}).get("findings") == 0, "localization_findings_not_zero")
    require(localization_repair.get("verification", {}).get("project_group_gate_readiness", {}).get("passed") == 17, "project_group_readiness_not_17")
    require(localization_repair.get("preserved_gate", {}).get("a10c13_human_local_commit_authorization") == "pending", "a10c13_authorization_gate_changed")
    require(feature.get("coordination", {}).get("localization_feature_evidence_boundary_repair_sha256") == LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_SHA256, "localization_feature_evidence_boundary_feature_sha_missing")
    require(feature.get("coordination", {}).get("localization_feature_evidence_boundary_repair_status") == "document_gate_and_17_repo_readiness_passed", "localization_feature_evidence_boundary_status_mismatch")
    readiness_replay_text = read(KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY)
    require(hashlib.sha256(readiness_replay_text.encode("utf-8")).hexdigest() == KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_SHA256, "release0_kds_commit_readiness_replay_sha_mismatch")
    readiness_replay = yaml.safe_load(readiness_replay_text).get("gke001_kds_release0_product_test_commit_readiness_replay", {})
    require(readiness_replay.get("id") == KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_ID, "release0_kds_commit_readiness_replay_id_mismatch")
    require(readiness_replay.get("candidate", {}).get("path_count") == 12, "release0_kds_commit_readiness_replay_path_count_mismatch")
    require(readiness_replay.get("candidate", {}).get("patch_sha256") == "1ef8ee7b5553defd5d94ccb4d7f95f60729a608f0d9700bc3c1821a4c7b56fc4", "release0_kds_commit_readiness_replay_patch_mismatch")
    require(readiness_replay.get("candidate", {}).get("real_repository_staged_after_replay") == 0, "release0_kds_commit_readiness_replay_staged_not_zero")
    require(readiness_replay.get("current_verification", {}).get("relevant_non_database") == "101_passed", "release0_kds_commit_readiness_replay_non_db_missing")
    require(readiness_replay.get("current_verification", {}).get("postgresql_and_migration") == "29_passed", "release0_kds_commit_readiness_replay_pg_missing")
    require(readiness_replay.get("decision", {}).get("human_local_commit_authorization") == "pending", "release0_kds_commit_readiness_replay_unexpectedly_authorized")
    require(feature.get("coordination", {}).get("kds_release0_product_test_commit_readiness_replay_sha256") == KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_SHA256, "release0_kds_commit_readiness_replay_feature_sha_missing")
    require(feature.get("coordination", {}).get("kds_release0_product_test_commit_readiness_replay_status") == "technical_replay_passed_human_local_commit_authorization_required", "release0_kds_commit_readiness_replay_status_mismatch")
    mmc_freshness_text = read(MMC_RELEASE0_POLICY_FRESHNESS_REPLAY)
    require(hashlib.sha256(mmc_freshness_text.encode("utf-8")).hexdigest() == MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_SHA256, "mmc_release0_policy_freshness_replay_sha_mismatch")
    mmc_freshness = yaml.safe_load(mmc_freshness_text).get("gke001_mmc_release0_policy_freshness_replay", {})
    require(mmc_freshness.get("id") == MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_ID, "mmc_release0_policy_freshness_replay_id_mismatch")
    require(mmc_freshness.get("current_policy", {}).get("seed_operation_count") == 17, "mmc_release0_policy_freshness_seed_count_mismatch")
    require(mmc_freshness.get("current_policy", {}).get("runtime_operation_count") == 17, "mmc_release0_policy_freshness_runtime_count_mismatch")
    require(mmc_freshness.get("current_policy", {}).get("contains_release0_operations") is False, "mmc_release0_policy_freshness_unexpected_policy_admission")
    require(mmc_freshness.get("current_verification", {}).get("focused_release0_api_and_contract") == "20_passed_37_deselected", "mmc_release0_policy_freshness_focused_missing")
    require(mmc_freshness.get("current_verification", {}).get("full_runtime") == "158_passed", "mmc_release0_policy_freshness_full_missing")
    require(mmc_freshness.get("unchanged_authorization_gates", {}).get("source_only_local_tdd") == "human_authorization_required", "mmc_release0_policy_freshness_source_gate_changed")
    require(mmc_freshness.get("unchanged_authorization_gates", {}).get("runtime_policy_application") == "high_risk_human_authorization_required", "mmc_release0_policy_freshness_runtime_gate_changed")
    require(feature.get("coordination", {}).get("mmc_release0_policy_freshness_replay_sha256") == MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_SHA256, "mmc_release0_policy_freshness_feature_sha_missing")
    require(feature.get("coordination", {}).get("mmc_release0_policy_freshness_replay_status") == "current_tests_passed_policy_still_17_operations_f013_review_pending", "mmc_release0_policy_freshness_status_mismatch")
    consumer_freshness_text = read(RELEASE0_CONSUMER_FRESHNESS_REPLAY)
    require(hashlib.sha256(consumer_freshness_text.encode("utf-8")).hexdigest() == RELEASE0_CONSUMER_FRESHNESS_REPLAY_SHA256, "release0_consumer_freshness_replay_sha_mismatch")
    consumer_freshness = yaml.safe_load(consumer_freshness_text).get("gke001_release0_consumer_freshness_replay", {})
    require(consumer_freshness.get("id") == RELEASE0_CONSUMER_FRESHNESS_REPLAY_ID, "release0_consumer_freshness_replay_id_mismatch")
    require(consumer_freshness.get("current_verification", {}).get("studio", {}).get("release0_focused") == "5_files_44_passed", "release0_consumer_studio_focused_missing")
    require(consumer_freshness.get("current_verification", {}).get("studio", {}).get("full_vitest") == "313_files_2759_passed_1_file_and_3_tests_skipped", "release0_consumer_studio_full_missing")
    require(consumer_freshness.get("current_verification", {}).get("brain", {}).get("release0_focused") == "6_files_122_passed", "release0_consumer_brain_focused_missing")
    require(consumer_freshness.get("current_verification", {}).get("brain", {}).get("full_vitest") == "45_files_390_passed", "release0_consumer_brain_full_missing")
    require(consumer_freshness.get("studio_governance_repair", {}).get("production_validator_changed") is False, "release0_consumer_unexpected_validator_change")
    require(consumer_freshness.get("studio_governance_repair", {}).get("production_release0_code_changed") is False, "release0_consumer_unexpected_product_change")
    require(consumer_freshness.get("authorization", {}).get("authenticated_live_e2e") is False, "release0_consumer_unexpected_live_e2e_authorization")
    require(feature.get("coordination", {}).get("release0_consumer_freshness_replay_sha256") == RELEASE0_CONSUMER_FRESHNESS_REPLAY_SHA256, "release0_consumer_freshness_feature_sha_missing")
    require(feature.get("coordination", {}).get("release0_consumer_freshness_replay_status") == "studio_and_brain_current_tests_passed_studio_governance_fixture_repair_f013_review_pending", "release0_consumer_freshness_status_mismatch")
    require(RELEASE0_CURRENT_STATE_REVALIDATION_ID in read(CONTROL_BOARD), "release0_current_state_control_board_registration_missing")
    require(RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_ID in read(CONTROL_BOARD), "release0_current_state_review_closure_control_board_missing")
    require(KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_ID in read(CONTROL_BOARD), "release0_kds_commit_request_control_board_missing")
    require(LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_ID in read(CONTROL_BOARD), "localization_feature_evidence_boundary_control_board_missing")
    require(KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_ID in read(CONTROL_BOARD), "release0_kds_commit_readiness_replay_control_board_missing")
    require(MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_ID in read(CONTROL_BOARD), "mmc_release0_policy_freshness_control_board_missing")
    require(RELEASE0_CONSUMER_FRESHNESS_REPLAY_ID in read(CONTROL_BOARD), "release0_consumer_freshness_control_board_missing")
    require("A10C12/A10C12R1" in read(SESSION_REGISTRY), "release0_current_state_session_registration_missing")
    require("A10C12R2" in read(SESSION_REGISTRY) and "A10C13" in read(SESSION_REGISTRY), "release0_review_and_request_session_registration_missing")
    require("A10C14" in read(SESSION_REGISTRY), "localization_feature_evidence_boundary_session_registration_missing")
    require("A10C15" in read(SESSION_REGISTRY), "release0_kds_commit_readiness_replay_session_registration_missing")
    require("A10C16" in read(SESSION_REGISTRY), "mmc_release0_policy_freshness_session_registration_missing")
    require("A10C17" in read(SESSION_REGISTRY), "release0_consumer_freshness_session_registration_missing")
    require("focused 41 passed" in read(A10I1_HANDOFF_REVIEW_EVIDENCE), "a10i1_kds_test_receipt_missing")
    require("focused 119 passed" in read(A10I1_HANDOFF_REVIEW_EVIDENCE), "a10i1_studio_test_receipt_missing")
    require("cleanup count 0" in read(A10I1_HANDOFF_REVIEW_EVIDENCE), "a10i1_kds_cleanup_receipt_missing")
    require("e2fc18d9287d45ae2fc4ac8015febea9187246840d91b06a6b33e16de8e865c4" in read(A10P2_HANDOFFS), "a10p2_matrix_hash_missing")
    require("3cab2c7eef531c13bc0af32af61836f3947aa23ac8b2461f84a05f47378dbaf2" in read(A10P2_HANDOFFS), "a10p2_policy_fingerprint_missing")
    require("typecheck from 86 errors/25 files to 49 errors/19 files" in read(A10P1_HANDOFFS), "a10p1_brain_handoff_missing")
    require("two facade proposals conflict on method, path and request identity" in read(A10P1_HANDOFFS), "a10p1_contract_conflict_missing")
    require("typecheck remains 86 errors in 25 files" in read(A10P0_HANDOFFS), "a10p0_brain_handoff_missing")
    require("legacy routes lack delegation, ACL, authoritative project binding and KDS audit" in read(A10P0_HANDOFFS), "a10p0_kds_gap_missing")
    require("technical_revalidation_passed_governance_pending" in read(STUDIO_A6_REVIEW), "studio_a6_review_decision_missing")
    require("2740 passed" in read(STUDIO_A6_REVIEW) and "7/7 passed" in read(STUDIO_A6_REVIEW), "studio_a6_review_evidence_incomplete")
    for marker in ("### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in read(A10P2_LOOP_EVIDENCE), f"a10p2_loop_marker_missing:{marker}")
        require(marker in read(A10P2_HANDOFF_LOOP_EVIDENCE), f"a10p2_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10P3_LOOP_EVIDENCE), f"a10p3_loop_marker_missing:{marker}")
        require(marker in read(A10P3R1_LOOP_EVIDENCE), f"a10p3r1_loop_marker_missing:{marker}")
        require(marker in read(A10P3R1_HANDOFF_LOOP_EVIDENCE), f"a10p3r1_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10P3R2_LOOP_EVIDENCE), f"a10p3r2_loop_marker_missing:{marker}")
        require(marker in read(A10P3R2_FREEZE_LOOP_EVIDENCE), f"a10p3r2_freeze_loop_marker_missing:{marker}")
        require(marker in read(A10I1_LOOP_EVIDENCE), f"a10i1_loop_marker_missing:{marker}")
        require(marker in read(A10I1_HANDOFF_LOOP_EVIDENCE), f"a10i1_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I1R1_LOOP_EVIDENCE), f"a10i1r1_loop_marker_missing:{marker}")
        require(marker in read(A10I1R1_CLOSURE_LOOP_EVIDENCE), f"a10i1r1_closure_loop_marker_missing:{marker}")
        require(marker in read(A10I2_LOOP_EVIDENCE), f"a10i2_loop_marker_missing:{marker}")
        require(marker in read(A10I2_HANDOFF_LOOP_EVIDENCE), f"a10i2_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I2R1_LOOP_EVIDENCE), f"a10i2r1_loop_marker_missing:{marker}")
        require(marker in read(A10I2R1_HANDOFF_LOOP_EVIDENCE), f"a10i2r1_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I2R2_LOOP_EVIDENCE), f"a10i2r2_loop_marker_missing:{marker}")
        require(marker in read(A10I2R2_HANDOFF_LOOP_EVIDENCE), f"a10i2r2_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I2R2_CLOSURE_LOOP_EVIDENCE), f"a10i2r2_closure_loop_marker_missing:{marker}")
        require(marker in read(A10I3P0_LOOP_EVIDENCE), f"a10i3p0_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1_LOOP_EVIDENCE), f"a10i3h1_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1_HANDOFF_LOOP_EVIDENCE), f"a10i3h1_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R1_LOOP_EVIDENCE), f"a10i3h1r1_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R1_HANDOFF_LOOP_EVIDENCE), f"a10i3h1r1_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R2_LOOP_EVIDENCE), f"a10i3h1r2_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R2_RECONCILIATION_LOOP_EVIDENCE), f"a10i3h1r2_reconciliation_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R2_HANDOFF_LOOP_EVIDENCE), f"a10i3h1r2_handoff_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R2R1_LOOP_EVIDENCE), f"a10i3h1r2r1_loop_marker_missing:{marker}")
        require(marker in read(BRAIN_A10P1T3_LOOP_EVIDENCE), f"brain_a10p1t3_loop_marker_missing:{marker}")
        require(marker in read(A10I3H1R2R2_LOOP_EVIDENCE), f"a10i3h1r2r2_loop_marker_missing:{marker}")
        require(marker in read(STUDIO_A10I1G1_LOOP_EVIDENCE), f"studio_a10i1g1_loop_marker_missing:{marker}")
        require(marker in read(BRAIN_A10P1T4_LOOP_EVIDENCE), f"brain_a10p1t4_loop_marker_missing:{marker}")
    require("A9 serial exit technical requirements are now `5/5`" in read(A9R1_ACCEPTANCE), "a9r1_acceptance_result_missing")

    print(
        "gke001_three_lane_coordination=pass "
        f"coordination_id={COORDINATION_ID} lanes=3 unique_locks=3 "
        "brain_mode=a10c12_report_only_verified studio_mode=a10c12_report_only_verified kds_mode=a10c12_report_only_verified mmc_mode=a10c12_report_only_policy_admission_blocked active_product_lanes=0 governance_implementation_lanes=0 report_only_lanes=3 authorized_pending_receipt_lanes=0 review_pending_lanes=0 human_authorization_request_lanes=1 kds_external_role_view_excluded=true "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
        f"studio_a4={STUDIO_A4_ID} studio_a4_sha256={STUDIO_A4_SHA256} "
        f"studio_a5={STUDIO_A5_ID} studio_a5_sha256={STUDIO_A5_SHA256} "
        f"studio_a6={STUDIO_A6_ID} studio_a6_sha256={STUDIO_A6_SHA256} "
        f"minimal_parallel_a7={MINIMAL_PARALLEL_A7_ID} minimal_parallel_a7_sha256={MINIMAL_PARALLEL_A7_SHA256} "
        f"a7_governance_cleanup_a8={A7_GOVERNANCE_CLEANUP_A8_ID} a7_governance_cleanup_a8_sha256={A7_GOVERNANCE_CLEANUP_A8_SHA256} "
        f"a9_read_admission={A9_READ_ADMISSION_ID} a9_read_admission_sha256={A9_READ_ADMISSION_SHA256} "
        f"a9r1={A9_MMC_ROLLBACK_REWORK_ID} a9r1_sha256={A9_MMC_ROLLBACK_REWORK_SHA256} "
        f"a10p0={A10_READONLY_PREFLIGHT_ID} a10p0_sha256={A10_READONLY_PREFLIGHT_SHA256} "
        f"a10p1={A10P1_COORDINATION_ID} a10p1_sha256={A10P1_COORDINATION_SHA256} "
        f"a10p2={A10P2_COORDINATION_ID} a10p2_sha256={A10P2_COORDINATION_SHA256} candidate_sha256={A10P2_CANDIDATE_SHA256} "
        f"a10p3={A10P3_COORDINATION_ID} a10p3_sha256={A10P3_COORDINATION_SHA256} schema_sha256={A10P3_SCHEMA_SHA256} "
        f"a10p3r1={A10P3R1_COORDINATION_ID} a10p3r1_sha256={A10P3R1_COORDINATION_SHA256} corrected_schema_sha256={A10P3R1_SCHEMA_SHA256} "
        f"a10p3r2={A10P3R2_COORDINATION_ID} a10p3r2_sha256={A10P3R2_COORDINATION_SHA256} frozen_schema_sha256={A10P3R2_SCHEMA_SHA256} freeze_id={A10P3R2_FREEZE_ID} freeze_sha256={A10P3R2_FREEZE_SHA256} "
        f"a10i1={A10I1_COORDINATION_ID} a10i1_sha256={A10I1_COORDINATION_SHA256} "
        f"a10i1r1={A10I1R1_COORDINATION_ID} a10i1r1_sha256={A10I1R1_COORDINATION_SHA256} "
        f"a10i2={A10I2_COORDINATION_ID} a10i2_sha256={A10I2_COORDINATION_SHA256} "
        f"a10i2r1={A10I2R1_COORDINATION_ID} a10i2r1_sha256={A10I2R1_COORDINATION_SHA256} "
        f"a10i2r2={A10I2R2_COORDINATION_ID} a10i2r2_sha256={A10I2R2_COORDINATION_SHA256} "
        f"a10i3p0={A10I3P0_COORDINATION_ID} a10i3p0_sha256={A10I3P0_COORDINATION_SHA256} "
        f"a10i3h1={A10I3H1_COORDINATION_ID} a10i3h1_sha256={A10I3H1_COORDINATION_SHA256} "
        f"a10i3h1r1={A10I3H1R1_COORDINATION_ID} a10i3h1r1_sha256={A10I3H1R1_COORDINATION_SHA256} "
        f"a10i3h1r2={A10I3H1R2_COORDINATION_ID} a10i3h1r2_sha256={A10I3H1R2_COORDINATION_SHA256} "
        f"a10i3h1r2r0={A10I3H1R2_RECONCILIATION_ID} a10i3h1r2r0_sha256={A10I3H1R2_RECONCILIATION_SHA256} "
        f"a10i3h1r2r1={A10I3H1R2R1_COORDINATION_ID} a10i3h1r2r1_sha256={A10I3H1R2R1_COORDINATION_SHA256} "
        f"brain_a10p1t3={BRAIN_A10P1T3_COORDINATION_ID} brain_a10p1t3_sha256={BRAIN_A10P1T3_COORDINATION_SHA256} "
        f"brain_a10p1t4={BRAIN_A10P1T4_COORDINATION_ID} brain_a10p1t4_sha256={BRAIN_A10P1T4_COORDINATION_SHA256} "
        f"brain_a10p1t4r1={BRAIN_A10P1T4R1_COORDINATION_ID} brain_a10p1t4r1_sha256={BRAIN_A10P1T4R1_COORDINATION_SHA256} "
        f"a10i3h1r2r2={A10I3H1R2R2_COORDINATION_ID} a10i3h1r2r2_sha256={A10I3H1R2R2_COORDINATION_SHA256} "
        f"a10i3h1r2r3={A10I3H1R2R3_COORDINATION_ID} a10i3h1r2r3_sha256={A10I3H1R2R3_COORDINATION_SHA256} "
        f"studio_a10i1g1={STUDIO_A10I1G1_COORDINATION_ID} studio_a10i1g1_sha256={STUDIO_A10I1G1_COORDINATION_SHA256} "
        f"studio_a10i1g1r1={STUDIO_A10I1G1R1_COORDINATION_ID} studio_a10i1g1r1_sha256={STUDIO_A10I1G1R1_COORDINATION_SHA256} "
        f"kds_dirty_isolation={KDS_DIRTY_ISOLATION_COORDINATION_ID} kds_dirty_isolation_sha256={KDS_DIRTY_ISOLATION_COORDINATION_SHA256} "
        f"kds_dependency_order={KDS_DEPENDENCY_ORDER_COORDINATION_ID} kds_dependency_order_sha256={KDS_DEPENDENCY_ORDER_COORDINATION_SHA256} "
        f"kds_stageb_disposition={KDS_STAGEB_DISPOSITION_COORDINATION_ID} kds_stageb_disposition_sha256={KDS_STAGEB_DISPOSITION_COORDINATION_SHA256} "
        f"kds_stageb_authorization_request={KDS_STAGEB_AUTHORIZATION_REQUEST_ID} kds_stageb_authorization_request_sha256={KDS_STAGEB_AUTHORIZATION_REQUEST_SHA256} "
        f"kds_stageb_core_authorization_request={KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_ID} kds_stageb_core_authorization_request_sha256={KDS_STAGEB_CORE_AUTHORIZATION_REQUEST_SHA256} "
        f"kds_stageb_core_baseline_reconciliation={KDS_STAGEB_CORE_BASELINE_RECONCILIATION_ID} kds_stageb_core_baseline_reconciliation_sha256={KDS_STAGEB_CORE_BASELINE_RECONCILIATION_SHA256} "
        f"kds_stageb_core_diffcheck_rework={KDS_STAGEB_CORE_DIFFFIX_REWORK_ID} kds_stageb_core_diffcheck_rework_sha256={KDS_STAGEB_CORE_DIFFFIX_REWORK_SHA256} "
        f"kds_stageb_core_diffcheck_authorization={KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_ID} kds_stageb_core_diffcheck_authorization_sha256={KDS_STAGEB_CORE_DIFFFIX_AUTHORIZATION_SHA256} "
        f"kds_stageb_core_local_commit_receipt={KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_ID} kds_stageb_core_local_commit_receipt_sha256={KDS_STAGEB_CORE_LOCAL_COMMIT_RECEIPT_SHA256} "
        f"kds_stageb_regression_preflight={KDS_STAGEB_REGRESSION_PREFLIGHT_ID} kds_stageb_regression_preflight_sha256={KDS_STAGEB_REGRESSION_PREFLIGHT_SHA256} "
        f"kds_stageb_regression_preflight_receipt={KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_ID} kds_stageb_regression_preflight_receipt_sha256={KDS_STAGEB_REGRESSION_PREFLIGHT_RECEIPT_SHA256} "
        f"kds_stageb_regression_commit_authorization_request={KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_ID} kds_stageb_regression_commit_authorization_request_sha256={KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_REQUEST_SHA256} "
        f"kds_stageb_regression_commit_authorization={KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_ID} kds_stageb_regression_commit_authorization_sha256={KDS_STAGEB_REGRESSION_COMMIT_AUTHORIZATION_SHA256} "
        f"kds_stageb_regression_commit_receipt={KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_ID} kds_stageb_regression_commit_receipt_sha256={KDS_STAGEB_REGRESSION_COMMIT_RECEIPT_SHA256} "
        f"kds_stageb_openspec_preflight={KDS_STAGEB_OPENSPEC_PREFLIGHT_ID} kds_stageb_openspec_preflight_sha256={KDS_STAGEB_OPENSPEC_PREFLIGHT_SHA256} "
        f"kds_stageb_openspec_preflight_receipt={KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_ID} kds_stageb_openspec_preflight_receipt_sha256={KDS_STAGEB_OPENSPEC_PREFLIGHT_RECEIPT_SHA256} "
        f"kds_stageb_openspec_commit_request={KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_ID} kds_stageb_openspec_commit_request_sha256={KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_REQUEST_SHA256} "
        f"kds_stageb_openspec_commit_authorization={KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_ID} kds_stageb_openspec_commit_authorization_sha256={KDS_STAGEB_OPENSPEC_COMMIT_AUTHORIZATION_SHA256} "
        f"kds_stageb_openspec_commit_receipt={KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_ID} kds_stageb_openspec_commit_receipt_sha256={KDS_STAGEB_OPENSPEC_COMMIT_RECEIPT_SHA256} "
        f"kds_stageb_run_handoff_preflight={KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_ID} kds_stageb_run_handoff_preflight_sha256={KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_SHA256} "
        f"kds_stageb_run_handoff_preflight_receipt={KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_ID} kds_stageb_run_handoff_preflight_receipt_sha256={KDS_STAGEB_RUN_HANDOFF_PREFLIGHT_RECEIPT_SHA256} "
        f"kds_stageb_run_handoff_eof_baseline={KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_ID} kds_stageb_run_handoff_eof_baseline_sha256={KDS_STAGEB_RUN_HANDOFF_EOF_BASELINE_RECONCILIATION_SHA256} "
        f"kds_stageb_run_handoff_eof_execution={KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_ID} kds_stageb_run_handoff_eof_execution_sha256={KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_EXECUTION_SHA256} "
        f"kds_stageb_run_handoff_eof_receipt={KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_ID} kds_stageb_run_handoff_eof_receipt_sha256={KDS_STAGEB_RUN_HANDOFF_EOF_REWORK_RECEIPT_SHA256} "
        f"kds_stageb_run_handoff_commit_request={KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_ID} kds_stageb_run_handoff_commit_request_sha256={KDS_STAGEB_RUN_HANDOFF_COMMIT_REQUEST_SHA256} "
        f"kds_stageb_push_preflight={KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_ID} kds_stageb_push_preflight_sha256={KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_SHA256} "
        f"kds_stageb_push_preflight_receipt={KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_ID} kds_stageb_push_preflight_receipt_sha256={KDS_STAGEB_FOUR_COMMIT_PUSH_PREFLIGHT_RECEIPT_SHA256} "
        f"kds_stageb_push_request={KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_ID} kds_stageb_push_request_sha256={KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_REQUEST_SHA256} "
        f"kds_stageb_push_authorization={KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_ID} kds_stageb_push_authorization_sha256={KDS_STAGEB_FOUR_COMMIT_PUSH_AUTHORIZATION_SHA256} "
        f"kds_stageb_push_receipt={KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_ID} kds_stageb_push_receipt_sha256={KDS_STAGEB_FOUR_COMMIT_PUSH_RECEIPT_SHA256} "
        f"release0_current_state={RELEASE0_CURRENT_STATE_REVALIDATION_ID} release0_current_state_sha256={RELEASE0_CURRENT_STATE_REVALIDATION_SHA256} "
        f"release0_current_state_handoff={RELEASE0_CURRENT_STATE_HANDOFF_ID} release0_current_state_handoff_sha256={RELEASE0_CURRENT_STATE_HANDOFF_SHA256} "
        f"release0_current_state_review={RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_ID} release0_current_state_review_sha256={RELEASE0_CURRENT_STATE_REVIEW_CLOSURE_SHA256} "
        f"release0_kds_commit_request={KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_ID} release0_kds_commit_request_sha256={KDS_RELEASE0_PRODUCT_TEST_COMMIT_REQUEST_SHA256} "
        f"localization_boundary_repair={LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_ID} localization_boundary_repair_sha256={LOCALIZATION_FEATURE_EVIDENCE_BOUNDARY_REPAIR_SHA256} "
        f"release0_kds_commit_readiness_replay={KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_ID} release0_kds_commit_readiness_replay_sha256={KDS_RELEASE0_PRODUCT_TEST_COMMIT_READINESS_REPLAY_SHA256} "
        f"mmc_release0_policy_freshness_replay={MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_ID} mmc_release0_policy_freshness_replay_sha256={MMC_RELEASE0_POLICY_FRESHNESS_REPLAY_SHA256} "
        f"release0_consumer_freshness_replay={RELEASE0_CONSUMER_FRESHNESS_REPLAY_ID} release0_consumer_freshness_replay_sha256={RELEASE0_CONSUMER_FRESHNESS_REPLAY_SHA256} "
        "status=active/partial/not_complete dispatch_status=studio_frozen_brain_a10p1t4_passed_mmc_h1r3_verified_kds_stageb_four_commits_pushed_postpush_review_passed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
