---
doc_id: GPCF-DOC-5D0159ED7D
title: Evidence Index — GPCF
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/evidence-index.md
source_path: docs/harness/evidence/evidence-index.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Evidence Index — GPCF

## GPCF-L4-GFIS-TEST-SR-SYNC-001 GFIS test source-record submission gate sync

- GFIS test source-record validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_customer_requirement_test_source_record_submission.py`
- GFIS test data directory: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/test-data/customer-requirement-platform-order/`
- GFIS test gate evidence: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-test-source-record-submission-gate.json`
- GFIS validator output: `gfis_customer_requirement_test_source_record_submission=pass test_source_records=1 test_data_lane=pass real_business_lane=repair_required valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `test_source_record_submission_gate=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-DEV-READY-SYNC-001 GFIS development_ready goal audit sync

- GFIS development-ready validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_development_ready_goal.py`
- GFIS development-ready loop round: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-DEV-READY-001.md`
- GFIS validator output: `gfis_development_ready_goal=pass development_ready=pass synthetic_dev_lane=dev_closed synthetic_e2e_pass=1 synthetic_stage_count=12 synthetic_verified_artifacts=12 runtime_subject=GFIS运行层 demo_e2e=pass_demo_only real_business_lane=repair_required business_verification_pending=true real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0 accepted_integrated=0 production_ready=0 production_writes=0 real_external_api_writes=0`
- GPCF L4/self-correction validators now report `development_ready=pass` while keeping `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-007 GFIS verified artifact admission gate sync

- GFIS REAL-007 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/verified-artifact/README.md`
- GFIS REAL-007 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/verified-artifact/customer-requirement-platform-order-verified-artifact-gate.json`
- GFIS REAL-007 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_verified_artifact_gate.py`
- GFIS real-lane validator now reports `verified_artifact_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF L4/self-correction validators now report `verified_artifact_gate=pass` and keep `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-006 GFIS WAES review admission gate sync

- GFIS REAL-006 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/waes-review/README.md`
- GFIS REAL-006 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/waes-review/customer-requirement-platform-order-waes-review-gate.json`
- GFIS REAL-006 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_waes_review_gate.py`
- GFIS real-lane validator now reports `waes_review_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF L4/self-correction validators now report `waes_review_gate=pass` and keep `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-005 GFIS runtime intake admission gate sync

- GFIS REAL-005 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-intake/README.md`
- GFIS REAL-005 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-intake/customer-requirement-platform-order-runtime-intake-gate.json`
- GFIS REAL-005 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_intake_gate.py`
- GFIS real-lane validator now reports `runtime_intake_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF L4/self-correction validators now report `runtime_intake_gate=pass` and keep `project_group_score=78` / `repair_required`.

## GPCF-L4-GFIS-REAL-SYNC-003 GFIS runtime primary key gate sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS REAL-003 README | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-primary-key/README.md` | `CustomerRequirementOrPlatformOrder` runtime primary key gate 已定义；缺 valid source record 和人工业务核验时不得创建运行层主键 | controlled |
| GFIS REAL-003 gate JSON | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/runtime-primary-key/customer-requirement-platform-order-runtime-primary-key-gate.json` | `valid_source_records=0`、`runtime_primary_key_created=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0` | repair_required |
| GFIS REAL-003 validator | `python3 scripts/validate_gfis_runtime_primary_key_gate.py` in GFIS | `gfis_runtime_primary_key_gate=pass`；KDS 候选、报价、合同链、用户口述、Demo、mock、fixture、synthetic 均不能打开运行层主键 | pass |
| GFIS REAL-002 validator | `python3 scripts/validate_gfis_pending_business_verification.py` in GFIS | `gfis_pending_business_verification=pass`；pending 机制可机检，但真实提交仍为 0 | pass |
| GFIS REAL-001 validator | `python3 scripts/validate_gfis_real_source_record_intake_gate.py` in GFIS | `gfis_real_source_record_intake_gate=pass` 且真实业务计数仍为 0 | pass |
| GFIS real lane validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 runtime_primary_key_gate=pass real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0` | pass_as_repair_guard |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REAL-SYNC-003.md` | 总控同步 GFIS REAL-003，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=completed`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 下一步只能在真实 source-of-record 进入 pending_business_verification、通过人工业务核验并生成运行层主键后，推进 review queue gate。

## GPCF-L4-GFIS-REAL-SYNC-002 GFIS pending_business_verification sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS REAL-002 README | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/pending-business-verification/README.md` | `CustomerRequirementOrPlatformOrder` pending_business_verification 顶层接收入口已定义；禁止报价单-only、合同审阅稿-only、KDS candidate-only、用户口述-only、Loop 文档-only、GFIS Demo、mock、fixture、synthetic/dev-only 直接进入真实业务链路 | controlled |
| GFIS REAL-002 schema | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/pending-business-verification/customer-requirement-platform-order.schema.json` | 12 个必填字段、5 类待人工核验等效来源、2 类最终有效来源；强制 manual verification before release | controlled |
| GFIS REAL-002 precheck | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/pending-business-verification/customer-requirement-platform-order-precheck.json` | `real_business_lane=repair_required`、`business_verification_pending=true`、`valid_source_records=0`、`real_runtime_primary_keys=0`、`real_review_queue_items=0`、`real_runtime_intake_items=0`、`real_waes_reviews=0`、`real_verified_artifacts=0` | repair_required |
| GFIS REAL-002 validator | `python3 scripts/validate_gfis_pending_business_verification.py` in GFIS | `gfis_pending_business_verification=pass`；KDS 候选可作为 pending 线索，弱凭证不会进入真实业务链路 | pass |
| GFIS REAL-001 gate | `python3 scripts/validate_gfis_real_source_record_intake_gate.py` in GFIS | `gfis_real_source_record_intake_gate=pass` 且真实业务计数仍为 0 | pass |
| GFIS real lane validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0` | pass_as_repair_guard |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REAL-SYNC-002.md` | 总控同步 GFIS REAL-002，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=completed`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 下一步只能在真实客户订单、平台订单回执、采购订单、客户确认、客户签样或等效正式确认进入 pending_business_verification 并通过人工核验后推进 `REAL-003`。

## GPCF-L4-GFIS-REAL-SYNC-001 GFIS real source-of-record intake gate sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS REAL-001 gate doc | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/gfis-real-source-record-intake-gate.md` | `CustomerRequirementOrPlatformOrder` 真实 source-of-record intake gate 已定义；禁止 synthetic/dev-only/mock/demo/fixture/KDS candidate-only/Loop document-only/口述-only 替代真实 source-of-record | controlled |
| GFIS REAL-001 evidence | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-real-source-record-intake-gate.json` | `source_record_files_found=0`、`pending_business_verification_files_found=0`、`valid_source_records=0`、`real_runtime_primary_keys=0`、`real_review_queue_items=0`、`real_runtime_intake_items=0`、`real_waes_reviews=0`、`real_verified_artifacts=0` | repair_required |
| GFIS REAL-001 validator | `python3 scripts/validate_gfis_real_source_record_intake_gate.py` in GFIS | `gfis_real_source_record_intake_gate=pass real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0 real_business_lane=repair_required business_verification_pending=true stop_type=completed` | pass |
| GFIS real lane validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0` | pass_as_repair_guard |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | 先因 Playwright webServer 15 秒启动超时失败；手动按同一配置启动 `python3 -m http.server 4173 --bind 127.0.0.1` 后复跑 `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REAL-SYNC-001.md` | 总控同步 GFIS REAL-001，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=4`、`batch_generated=false`、`substance_gate=pass`、`stop_type=blocked_missing_real_source_record`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 下一步只能在真实客户订单、平台订单回执、采购订单、客户确认或等效正式确认进入 `pending_business_verification` 后推进 REAL-002。

## GPCF-L4-GFIS-DEV-SYNC-001 GFIS dual-lane dev sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS DEV-001 synthetic master | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/synthetic-fixtures/synthetic-gehu-sop-e2e-master.json` | 覆盖 12 个 GFIS SOP 阶段；标记 `synthetic=true`、`dev_only=true`、`dry_run=true`、`not_source_of_record=true`、`not_business_verified=true` | pass |
| GFIS DEV-002 dry-run | `python3 scripts/run_gfis_runtime_sop_e2e_dev_dry_run.py` in GFIS | `synthetic_dev_lane=dev_closed`、`synthetic_e2e=synthetic_e2e_pass`、`synthetic_stage_count=12`、`synthetic_verified_artifacts=12`、`real_business_lane=repair_required`、`business_verification_pending=true` | pass |
| GFIS DEV-003 dev validator | `python3 scripts/validate_gfis_runtime_sop_e2e_dev.py` in GFIS | `gfis_runtime_sop_e2e_dev=pass`、`synthetic_dev_lane=dev_closed`、`synthetic_e2e_pass=1`、`business_verification_pending=true`、`runtime_sop_e2e_real=repair_required` | pass |
| GFIS DEV-003 real validator | `python3 scripts/validate_gfis_runtime_sop_e2e_real.py` in GFIS | `gfis_runtime_sop_e2e_real=repair_required`、`synthetic_rejected_by_real_lane=1`、`synthetic_pollution_files=0`、`real_source_records=0`、`real_runtime_primary_keys=0`、`real_review_queue_items=0`、`real_runtime_intake_items=0`、`real_waes_reviews=0`、`real_verified_artifacts=0` | pass_as_repair_guard |
| GPCF control status | `GPCF-L4-GFIS-DEV-SYNC-001` | `synthetic_dev_lane=dev_closed`、`real_business_lane=repair_required`、`business_verification_pending=true`；不恢复 100/100，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=8`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 source-of-record、真实运行层主键、真实 review queue、真实 runtime intake、真实 WAES review、真实 KDS/WAES 写入或真实 verified artifact。
- 真正业务闭环仍等待真实 source-of-record：`real source record -> runtime primary key -> review queue -> runtime intake -> WAES review -> verified artifact`。

## GPCF-L4-GFIS-REPAIR-278 GFIS CustomerRequirementOrPlatformOrder owner reminder dispatch authorization negative fixture guard sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 268 validator | `python3 scripts/validate_gfis_sop_e2e_268.py` in GFIS | `source_receiving_scan_items=1`、`negative_fixture_count=6`、`rejected_fixture_count=6`、`accepted_fixture_count=0`、`dispatch_authorization_files_found=0`、`valid_dispatch_authorizations=0`、`recipient_confirmations_found=0`、`channel_confirmations_found=0`、`kds_backlinks_found=0`、`dispatch_allowed=0`、`owner_reminders_dispatched=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-268.md` | 记录 6 类弱派发授权声明均被拒收，不能派发或重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-278.md` | 总控同步 GFIS 268，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、外部通知、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步进入 `GFIS-RUNTIME-SOP-E2E-269`，把缺有效派发授权转换为 post-scan hold/action queue。

## GPCF-L4-GFIS-REPAIR-277 GFIS CustomerRequirementOrPlatformOrder owner reminder dispatch authorization receiving scan sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 267 validator | `python3 scripts/validate_gfis_sop_e2e_267.py` in GFIS | `source_dispatch_preflight_items=1`、`dispatch_authorization_files_found=0`、`valid_dispatch_authorizations=0`、`invalid_dispatch_authorizations=0`、`missing_dispatch_authorizations=1`、`unexpected_files=0`、`recipient_confirmations_found=0`、`channel_confirmations_found=0`、`dispatch_allowed=0`、`owner_reminders_dispatched=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-267.md` | 记录派发授权接收目录为空，无有效授权、收件方确认或通道确认，不能派发或重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-277.md` | 总控同步 GFIS 267，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、外部通知、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步进入 `GFIS-RUNTIME-SOP-E2E-268`，在授权接收目录仍为空时建立授权缺口 hold/action queue 或下一步受控补证机制。

## GPCF-L4-GFIS-REPAIR-276 GFIS CustomerRequirementOrPlatformOrder owner reminder dispatch authorization preflight sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 266 validator | `python3 scripts/validate_gfis_sop_e2e_266.py` in GFIS | `dispatch_authorization_files_found=0`、`valid_dispatch_authorizations=0`、`recipient_confirmations_found=0`、`channel_confirmations_found=0`、`dispatch_allowed=0`、`owner_reminders_dispatched=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-266.md` | 记录派发授权预检已建立，但无人工授权、收件方确认或通道确认，不能派发或重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-276.md` | 总控同步 GFIS 266，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、外部通知、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步扫描 owner reminder dispatch authorization 接收目录。

## GPCF-L4-GFIS-REPAIR-275 GFIS CustomerRequirementOrPlatformOrder valid source-record index owner reminder escalation action package sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 265 validator | `python3 scripts/validate_gfis_sop_e2e_265.py` in GFIS | `owner_action_items=3`、`owner_reminders_prepared=3`、`owner_reminders_dispatched=0`、`dispatch_authorizations_found=0`、`external_notifications_sent=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-265.md` | 记录三类责任方补证动作已准备但未派发，不能重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-275.md` | 总控同步 GFIS 265，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实提醒派发、valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步建立 owner 补证动作派发授权预检。

## GPCF-L4-GFIS-REPAIR-274 GFIS CustomerRequirementOrPlatformOrder valid source-record index change listener sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 264 validator | `python3 scripts/validate_gfis_sop_e2e_264.py` in GFIS | `source_record_index_files_found=0`、`new_source_record_index_files=0`、`changed_source_record_index_files=0`、`valid_source_records=0`、`runtime_primary_key_recheck_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-264.md` | 记录 valid source-record index 接收目录无新增或变更文件，不能重新打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-274.md` | 总控同步 GFIS 264，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步继续监听真实 source-record index，并形成 owner 补证提醒/升级动作。

## GPCF-L4-GFIS-REPAIR-273 GFIS CustomerRequirementOrPlatformOrder runtime primary key negative/pollution guard sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 263 validator | `python3 scripts/validate_gfis_sop_e2e_263.py` in GFIS | `weak_primary_key_open_attempts=6`、`rejected_primary_key_open_attempts=6`、`accepted_primary_key_open_attempts=0`、`runtime_primary_key_created=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | scoped `git diff --check -- ...` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-263.md` | 记录 GFIS Demo、KDS candidate-only、报价单、Loop 文档、口述事实、mock/fixture/培训资料均不能打开运行层主键门禁 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-273.md` | 总控同步 GFIS 263，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步建立 valid source-record 接收目录的下一轮监听/变更检测。

## GPCF-L4-GFIS-REPAIR-272 GFIS CustomerRequirementOrPlatformOrder runtime primary key gate sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 262 validator | `python3 scripts/validate_gfis_sop_e2e_262.py` in GFIS | `valid_source_records=0`、`runtime_primary_key_gate_blocked=1`、`runtime_primary_key_created=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-262.md` | 记录缺 valid source record 时 runtime primary key gate 必须阻断 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-272.md` | 总控同步 GFIS 262，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=5`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步建立 runtime primary key gate 的负例/污染拒收。

## GPCF-L4-GFIS-REPAIR-271 GFIS CustomerRequirementOrPlatformOrder valid source record index receiving scan sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 261 validator | `python3 scripts/validate_gfis_sop_e2e_261.py` in GFIS | `source_record_index_files_found=0`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-261.md` | 记录真实 source-of-record 脱敏索引接收目录为空，不能打开 runtime primary key gate | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-271.md` | 总控同步 GFIS 261，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步只有在真实 source-record index 出现并通过校验后才允许打开 runtime primary key gate。

## GPCF-L4-GFIS-REPAIR-270 GFIS CustomerRequirementOrPlatformOrder valid source record eligibility sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 260 validator | `python3 scripts/validate_gfis_sop_e2e_260.py` in GFIS | `pending_business_verification_candidates=1`、`formal_quotation_candidates=1`、`customer_confirmations=0`、`purchase_orders=0`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS KDS harvester | `python3 scripts/harvest_gfis_kds_gehu_inputs.py` in GFIS | categories `8/8`，missing live business inputs `5`，controlled missing sources `4` | partial |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | failed on `KDS coverage must not have missing controlled sources`；状态保持 `repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-260.md` | 记录报价单与 KDS 受控数据只能进入 pending_business_verification，不能升级 valid source record | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-270.md` | 总控同步 GFIS 260，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=4`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；下一步必须接收真实客户确认、平台订单回执、采购订单或等效正式确认原件的脱敏索引。

## GPCF-L4-GFIS-REPAIR-269 GFIS CustomerRequirementOrPlatformOrder KDS candidate mapping sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 259 validator | `python3 scripts/validate_gfis_sop_e2e_259.py` in GFIS | `kds_candidate_sources=1`、`quotation_sources=1`、`customer_confirmations=0`、`purchase_orders=0`、`valid_source_records=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增输出 `runtime_customer_requirement_platform_order_kds_candidate_source_record_mapping_gate=customer_requirement_platform_order_kds_candidate_mapped_customer_source_record_missing:...`；整体仍为 `gfis_runtime_sop_e2e=repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS diff hygiene | `git diff --check -- .` in GFIS | pass | pass |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-259.md` | 记录报价单 KDS 候选只能作为 pending_business_verification 种子，不能升级 valid source record | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-269.md` | 总控同步 GFIS 259，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有 valid source record、dispatch confirmation、运行层主键、review queue、runtime intake、WAES review、KDS write receipt 或 verified artifact。
- 真正最小闭环仍未形成；只有至少一个阶段打通 `source record -> runtime primary key -> review queue -> runtime intake -> WAES review -> verified artifact` 后才能进入闭环判定。

## GPCF-L4-GFIS-REPAIR-268 GFIS runtime 12-stage input gap convergence queue sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS 12-stage queue validator | `python3 scripts/validate_gfis_sop_e2e_258.py` in GFIS | `runtime_sop_stages=12`、`kds_controlled_stages=12`、`blocked_stages=12`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；新增输出 `runtime_12_stage_input_gap_convergence_queue=runtime_12_stage_input_gap_convergence_queue_open_missing_real_inputs:...`；整体仍为 `gfis_runtime_sop_e2e=repair_required` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-258.md` | 记录 12 阶段均 blocked，review/runtime/WAES/verified 全部保持 0 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-268.md` | 总控同步 GFIS 258，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=6`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 source-of-record、客户签样、转量产批准、生产订单、质检、库存、发货、POD、WAES review、KDS write receipt、运行层主键或 verified artifact。
- 下一步进入 `GFIS-RUNTIME-SOP-E2E-259`：从 12 阶段队列中选择一个阶段建立真实输入接收门禁。

## GPCF-L4-GFIS-REPAIR-267 GFIS source owner response release remediation evidence intake scanner sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS remediation evidence intake scanner validator | `python3 scripts/validate_gfis_sop_e2e_257.py` in GFIS | `remediation_evidence_intake_scanner_items=1`、`remediation_evidence_files_found=0`、`valid_remediation_evidence_files=0`、`missing_remediation_evidence_files=1`、`remediation_evidence_intake_blocked=1`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；`gfis_runtime_sop_e2e=repair_required`、`missing_inputs=5 missing_kds_source_paths=2` | repair_required |
| GFIS Demo E2E | `npm run test:e2e` in GFIS | `26 passed`；仅作为 demo/frontend 回归，不作为 SOP 真实业务凭证 | pass_demo_only |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-257.md` | 记录真实补证材料接收目录为空，release/review/runtime/WAES/verified 全部保持 0 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-267.md` | 总控同步 GFIS 257，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=7`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 remediation evidence、source-of-record、pending submission、人工核验完成、有效 release-ready package、有效 dispatch confirmation、运行层主键、review/runtime/WAES 或 verified artifact。
- 下一步进入 `GFIS-RUNTIME-SOP-E2E-258`：继续收敛完整 12 阶段 SOP 的 KDS/GFIS 输入差距。

## GPCF-L4-GFIS-REPAIR-266 GFIS remediation action recheck sync

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| GFIS remediation action recheck validator | `python3 scripts/validate_gfis_sop_e2e_256.py` in GFIS | `remediation_action_recheck_items=1`、`remediation_actions_required=8`、`remediation_actions_satisfied=0`、`remediation_actions_unsatisfied=8`、`remediation_recheck_blocked=1`、`runtime_sop_e2e=repair_required` | pass |
| GFIS runtime SOP validator | `python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2；GFIS 运行层仍为 `repair_required`，未形成真实业务闭环 | repair_required |
| GFIS loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-256.md` | 记录 8 项 remediation action 均未满足，release/dispatch/review/runtime/WAES/verified 全部保持 0 | partial |
| GPCF loop round | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-266.md` | 总控同步 GFIS 256，不升级 accepted/integrated | partial |

- 本轮真实计数：`declared_rounds=1/15`、`substantive_rounds=1/15`、`generated_items=7`、`batch_generated=false`、`substance_gate=pass`、`stop_type=authorization_boundary`。
- 本轮没有真实 source-of-record、pending submission、人工核验完成、有效 release-ready package、有效 dispatch confirmation、运行层主键、review/runtime/WAES 或 verified artifact。
- 下一步进入 `GFIS-RUNTIME-SOP-E2E-257`：建立 source owner response release remediation evidence intake scanner。

## Base Knowledge / ODF Evidence Registry

## GPCF-L4-GFIS-REAL-SYNC-004 GFIS review queue admission gate sync

- GFIS REAL-004 README: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/review-queue/README.md`
- GFIS REAL-004 gate JSON: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/review-queue/customer-requirement-platform-order-review-queue-admission-gate.json`
- GFIS REAL-004 validator: `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_review_queue_admission_gate.py`
- GFIS real-lane validator now reports `review_queue_gate=pass` while keeping `real_business_lane=repair_required`.
- GPCF validators: `tools/kds-sync/validate_loop_self_correction_gate.py` and `tools/kds-sync/validate_l4_minimum_closed_loop.py`
- Truth counts: `declared_rounds=1/15`, `substantive_rounds=1/15`, `generated_items=5`, `batch_generated=false`, `substance_gate=pass`, `stop_type=completed`.
- Non-claim: this evidence does not create source record, runtime primary key, review queue, runtime intake, WAES review, KDS/WAES write receipt, verified artifact, accepted, integrated, production write, external API write, schema sync, bench migrate, deployment, or permission change.

This registry connects evidence already listed in `docs/harness/evidence/README.md`
to the main evidence index. It is a discoverability registry only; it does not
claim real KDS writeback, RAG admission, settlement, production write,
accepted, or integrated status.

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| Base Knowledge closure score dry-run summary | `docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md` | dry-run scoring evidence; uses fixtures and hard-stop checks only | dry_run_evidence_only |
| Base Knowledge writeback candidate ledger | `docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md` | candidate ledger for controlled review; not a real writeback receipt | candidate_only |
| Base Knowledge committee review queue | `docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md` | committee review queue for human-controlled decisions | review_queue_only |
| Base Knowledge committee review schema | `docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md` | schema for controlled committee review records | controlled_schema |
| Base Knowledge committee review template | `docs/harness/evidence/base-knowledge-committee-review-template-20260619.md` | template for future committee review entries | controlled_template |
| Base Knowledge human confirmation queue | `docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md` | human confirmation queue; does not prove confirmation completed | confirmation_queue_only |
| Base Knowledge human confirmation schema | `docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md` | schema for human confirmation records | controlled_schema |
| Base Knowledge human confirmation template | `docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md` | template for future human confirmation entries | controlled_template |
| KDS MD/OKF/ODF full closure report | `docs/harness/evidence/kds-md-okf-odf-full-closure-report-20260619.md` | governance closure report; not a production KDS API write receipt | controlled_report |
| KDS Phase 10 backlog triage report | `docs/harness/evidence/kds-phase10-backlog-triage-20260619.md` | backlog triage report for continued KDS governance; not accepted/integrated proof | controlled_report |
| KDS Phase 10 self-refresh stabilization workpack | `docs/harness/evidence/kds-phase10-self-refresh-stabilization-workpack-20260619.md` | self-refresh stabilization workpack; not a production write or remote sync receipt | controlled_workpack |
| ODF phase 2 expansion closure report | `docs/harness/evidence/odf-phase2-closure-report-20260617.md` | closure evidence for phase 2 expanded sample governance | controlled_closure |
| ODF phase 2 sample ledger | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.md` | sample ledger for phase 2 ODF governance | controlled_ledger |
| ODF phase 3 schema gate evidence | `docs/harness/evidence/odf-phase3-schema-gate-20260617.md` | schema gate evidence for ODF governance | controlled_gate |
| ODF phase 4 small-batch closure | `docs/harness/evidence/odf-phase4-small-batch-closure-20260617.md` | closure evidence for phase 4 small-batch governance | controlled_closure |
| ODF phase 4 small-batch ledger | `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.md` | small-batch ledger for phase 4 ODF governance | controlled_ledger |
| ODF phase 5 change request closure | `docs/harness/evidence/odf-phase5-change-request-closure-20260617.md` | closure evidence for phase 5 change-request governance | controlled_closure |
| ODF phase 5 change request ledger | `docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md` | change-request ledger for phase 5 ODF governance | controlled_ledger |
| ODF phase 6 manual confirmation workbench | `docs/harness/evidence/odf-phase6-manual-confirmation-workbench-20260618.md` | manual confirmation workbench evidence; confirmation remains controlled by human review | controlled_workbench |
| ODF phase 6 manual confirmation closure | `docs/harness/evidence/odf-phase6-manual-confirmation-workbench-closure-20260618.md` | closure evidence for phase 6 governance workflow | controlled_closure |
| ODF phase 7 small-batch ledger | `docs/harness/evidence/odf-phase7-small-batch-ledger-20260619.md` | small-batch governance ledger; not business completion evidence | controlled_ledger |
| ODF phase 7 small-batch closure | `docs/harness/evidence/odf-phase7-small-batch-closure-20260619.md` | closure evidence for phase 7 small-batch governance workflow | controlled_closure |
| ODF phase 8 drift monitoring report | `docs/harness/evidence/odf-phase8-drift-monitoring-report-20260619.md` | drift monitoring evidence; does not upgrade runtime business status | controlled_report |
| ODF phase 8 drift monitoring closure | `docs/harness/evidence/odf-phase8-drift-monitoring-closure-20260619.md` | closure evidence for phase 8 drift monitoring workflow | controlled_closure |
| ODF phase 9 dynamic source stabilization report | `docs/harness/evidence/odf-phase9-dynamic-source-stabilization-report-20260619.md` | dynamic source stabilization report; not a remote sync or accepted/integrated proof | controlled_report |
| ODF phase 9 dynamic source stabilization closure | `docs/harness/evidence/odf-phase9-dynamic-source-stabilization-closure-20260619.md` | closure evidence for phase 9 dynamic source stabilization workflow | controlled_closure |

### Non-Claims

- This registry does not perform or prove real KDS API writeback.
- This registry does not admit any item into production RAG, settlement,
  runtime business flow, accepted, or integrated status.
- This registry does not authorize production write, external API write, schema
  sync, bench migrate, deployment, commit, or push.

## Current Control Gates

| 门禁 | 命令 | 当前结论 |
|---|---|---|
| KDS sync plan | `python3 tools/kds-sync/kds_sync_plan.py --allow-unconfigured-remote` | pass |
| KDS token guard | `python3 tools/kds-sync/validate_kds_token.py` | pass，token 未写入 Git 文档 |
| Loop document gate | `python3 tools/kds-sync/loop_document_gate.py` | pass |
| Loop engineering integrity | `python3 tools/kds-sync/validate_loop_engineering_integrity.py` | pass，GFIS subject remains runtime layer |
| Loop self-correction gate | `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | expected blocked，GFIS runtime repair still required |
| L4 minimum closed loop | `python3 tools/kds-sync/validate_l4_minimum_closed_loop.py` | repair，GFIS runtime SOP blocks final closure |

## Governance Evidence Registry

| 证据 | 路径/命令 | 结果 | 状态 |
|---|---|---|---|
| Loop governance dashboard evidence | `docs/harness/evidence/loop-governance-dashboard-20260617.md` | 登记 `LOOP-GOV-DASHBOARD-20260617`，维持 `partial_repair` 状态上限、`repair_required` 业务事实和 accepted/integrated 禁止升级边界 | active_governance_dashboard |
| Loop governance current window disposition evidence | `docs/harness/evidence/loop-governance-current-window-disposition-20260619.md` | 登记 `LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619`，记录 `LEDB-001-RD-005` 与 `LEDB-002-RD-004`；区分 shell exceptions 与 targeted annotation candidates，不批量改写历史 | review_required |
| Loop governance current window review evidence | `docs/harness/evidence/loop-governance-current-window-review-20260619.md` | 登记 `LOOP-GOV-CURRENT-WINDOW-REVIEW-20260619`，记录当前 audit window 的 `truth_records=2`、`five_segment_records=7`、duplicate/similarity review 信号，不批量改写历史 | review_required |
| Loop governance phase goal evidence | `docs/harness/evidence/loop-governance-phase-goal-20260617.md` | 登记 `LOOP-GOV-PHASE-20260617`，限定治理进程服务于实施主进程质量提升，维持 `partial_repair` 状态上限且不创建业务事实 | active_governance |
| Loop governance efficiency debt backlog evidence | `docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.md` | 登记 `LOOP-GOV-EFF-DEBT-20260617`，覆盖 `LEDB-001` 至 `LEDB-004` 的受控 review disposition 队列，不升级业务状态 | review_required |
| Loop governance efficiency debt locator evidence | `docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md` | 登记 `LOOP-GOV-EFF-DEBT-LOCATOR-20260617`，用于定位 `LEDB-001` / `LEDB-002` 当前审计窗口债务，不批量改写历史 | review_required |
| Loop governance round review plan evidence | `docs/harness/evidence/loop-governance-round-review-plan-20260617.md` | 登记 `LOOP-GOV-ROUND-REVIEW-PLAN-20260617`，绑定 `LOOP-GOV-EFF-DEBT-LOCATOR-20260617`，保持 `no_bulk_rewrite=true` 与 `business_status_impact=none` | review_required |
| Loop governance truth-field review evidence | `docs/harness/evidence/loop-governance-truth-field-review-20260617.md` | 登记 `LOOP-GOV-TRUTH-FIELD-REVIEW-20260617` 与 `LEDB-001-RD-003`，保留 shell 例外和已注释历史记录的区分 | review_required |
| Loop governance five-segment review evidence | `docs/harness/evidence/loop-governance-five-segment-review-20260617.md` | 登记 `LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617` 与 `LEDB-002-RD-002`，区分 targeted annotation candidate 与 index-level exception | review_required |
| Loop governance sequence checkpoint evidence | `docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.md` | 记录 `LEDB-003-RD-002`：每 25 个 `GPCF-L4-GFIS-REPAIR-*` 轮次做一次长序列 checkpoint，下一次到 sequence length 200 或 hard-window debt 复现时触发 | watch |
| Loop governance sequence checkpoint validator | `python3 tools/kds-sync/validate_loop_governance_sequence_checkpoint.py` | 校验 checkpoint cadence、hard-window 清洁、不批量改写历史和不升级业务状态 | pass |

## LOOP-GOV-DASHBOARD-20260617 Loop governance dashboard

- Dashboard evidence is registered in the Governance Evidence Registry table above.
- It links `LOOP-GOV-PHASE-20260617`, keeps `efficiency_risk=review_required`, and enforces `status_ceiling=partial_repair`.
- It does not prove GFIS runtime SOP E2E passed and does not allow accepted/integrated status.

## LOOP-GOV-CURRENT-WINDOW-REVIEW-20260619 Loop governance current window review

- Current-window review evidence is registered in the Governance Evidence Registry table above.
- It records `LEDB-001-RD-004` and `LEDB-002-RD-003` for current live audit-window review targets.
- It keeps `no_bulk_rewrite=true`, `business_status_impact=none`, and does not prove GFIS runtime SOP E2E passed.

## LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619 Loop governance current window disposition

- Current-window disposition evidence is registered in the Governance Evidence Registry table above.
- It records `LEDB-001-RD-005` and `LEDB-002-RD-004` for affected records `252`, `254`, and `269` through `273`.
- It distinguishes index-level shell exceptions from targeted annotation candidates, keeps `no_bulk_rewrite=true`, and does not prove GFIS runtime SOP E2E passed.

## LOOP-GOV-PHASE-20260617 Loop governance phase goal

- Phase goal evidence is registered in the Governance Evidence Registry table above.
- It keeps Loop governance bound to quality, efficiency, and self-improvement support for the implementation main process.
- It does not create real business facts or allow accepted/integrated status.

## LOOP-GOV-EFF-DEBT-20260617 Loop governance efficiency debt backlog

- Efficiency debt backlog evidence is registered in the Governance Evidence Registry table above.
- It records `LEDB-001`, `LEDB-002`, `LEDB-003`, and `LEDB-004`; it does not rewrite historical records in bulk or change GFIS/GPCF business status.

## LOOP-GOV-ROUND-REVIEW-PLAN-20260617 Loop governance round review plan

- Round review plan evidence is registered in the Governance Evidence Registry table above.
- It binds review packages to `LOOP-GOV-EFF-DEBT-LOCATOR-20260617` and keeps `no_bulk_rewrite=true`.
- It has `business_status_impact=none` and does not prove GFIS runtime SOP E2E passed.

## LOOP-GOV-TRUTH-FIELD-REVIEW-20260617 Loop governance truth-field review

- Truth-field review evidence is registered in the Governance Evidence Registry table above.
- It records `LEDB-001-RD-003`; shell records remain index-level exceptions unless a separate historical migration plan is authorized.

## LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617 Loop governance five-segment review

- Five-segment review evidence is registered in the Governance Evidence Registry table above.
- It records `LEDB-002-RD-002`; targeted annotation candidates and index-level exceptions remain separated.

## LOOP-GOV-SEQUENCE-CHECKPOINT-20260619 Loop governance sequence checkpoint

- Sequence checkpoint evidence is registered in the Governance Evidence Registry table above.
- It records `LEDB-003-RD-002`; it does not close `LEDB-003`, rewrite historical records in bulk, or change GFIS/GPCF business status.
