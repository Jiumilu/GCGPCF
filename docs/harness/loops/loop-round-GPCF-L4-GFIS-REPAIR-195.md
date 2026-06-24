---
doc_id: GPCF-DOC-7A56E22DB1
title: GPCF-L4-GFIS-REPAIR-195 GFIS 审阅授权负样本门禁
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-195.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-195.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-195 GFIS 审阅授权负样本门禁

## 轮次摘要

- round_id: `GPCF-L4-GFIS-REPAIR-195`
- gfis_round_id: `GFIS-RUNTIME-SOP-E2E-188`
- mode: L4 自纠偏与 GFIS 运行时修复
- subject: GFIS 运行层，不是 GFIS Demo
- business_positioning: GFIS 是葛化工厂建设期间现代精工 OEM 生产的运行系统，也是葛化自建工厂投产后的同一运行系统。
- target_object_family: `CustomerRequirementOrPlatformOrder`
- target_stage: `01_customer_requirement_platform_order`
- target_gap: 弱授权类材料不得创建 review authorization、review queue、runtime intake、WAES review 或 verified 状态。

## 已读取输入

- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/AGENTS.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/README.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/PROJECT_HARNESS_MANIFEST.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/loop-state.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/README.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/evidence/evidence-index.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_sop_e2e.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/gcfis_custom/gcfis_custom/api.py`

## GFIS 已落地变更

- 新增 `scripts/build_gfis_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard.py`。
- 新增 `scripts/validate_gfis_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard.py`。
- 新增 `docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-review-authorization-envelope-negative-fixture-guard.json`。
- 新增 `docs/harness/sop-e2e/gfis-customer-requirement-platform-order-review-authorization-envelope-negative-fixture-guard.md`。
- 新增 `docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-188.md`。
- 更新 `gcfis_custom/gcfis_custom/api.py`，增加只读 `get_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard`。
- 更新 `scripts/validate_gfis_runtime_sop_e2e.py`，运行新验证器并打印新的运行时状态行。
- 更新 GFIS loop-state、evidence index、loops README 和 SOP E2E README。

## 机器事实

| Fact | Value |
|---|---|
| negative_fixture_count | 6 |
| rejected_fixture_count | 6 |
| accepted_fixture_count | 0 |
| weak_authorization_count | 6 |
| submitted_envelopes | 0 |
| valid_envelopes | 0 |
| manual_authorized | 0 |
| recipient_identity_confirmed | 0 |
| dispatch_channel_confirmed | 0 |
| submitted_files_found | 0 |
| structure_valid_records | 0 |
| runtime_primary_key_ready | 0 |
| runtime_primary_key_missing | 1 |
| review_queue | 0 |
| manual_review | 0 |
| waes_review | 0 |
| runtime_intake | 0 |
| verified | 0 |
| state | `customer_requirement_platform_order_review_authorization_envelope_negative_fixtures_rejected` |
| runtime_sop_e2e | `repair_required` |

## 已拒绝负样本

- `reject_gfis_demo_state`
- `reject_kds_candidate_only`
- `reject_user_oral_note_only`
- `reject_weak_authorization_message`
- `reject_quotation_or_contract_draft`
- `reject_unverified_accepted_integrated_claim`

## 验证

| Check | Result |
|---|---|
| `python3 -m py_compile scripts/build_gfis_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard.py scripts/validate_gfis_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard.py scripts/validate_gfis_runtime_sop_e2e.py gcfis_custom/gcfis_custom/api.py` in GFIS | pass |
| `python3 scripts/build_gfis_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard.py && python3 scripts/validate_gfis_customer_requirement_platform_order_review_authorization_envelope_negative_fixture_guard.py` in GFIS | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | expected exit 2; `gfis_runtime_sop_e2e=repair_required` |
| `npm run test:e2e` in GFIS | 26 passed; `pass_demo_only` |
| `git diff --check -- .` in GFIS | pass |

## GPCF 回写

- 更新 `02-governance/loop/LOOP_CONTROL_BOARD.md`。
- 更新 `docs/harness/loop-state.md`。
- 更新 `docs/harness/evidence/evidence-index.md`。
- 更新 `docs/harness/minimum-closed-loop/l4-closure-score-matrix.md`。
- 更新 `09-status/gpcf-project-status-matrix.md`。
- 新增本 GPCF Loop 轮次记录。

## 不声明事项

- 未创建客户订单。
- 未创建平台订单。
- 未提交真实 source-of-record。
- 未提交审阅授权信封。
- 未创建运行时主键。
- 未创建 review queue 项。
- 未执行人工审阅。
- 未执行 WAES 审阅。
- 未执行 runtime intake。
- 未创建 verified 工件。
- 未设置 accepted 或 integrated 状态。
- 未执行生产写入、真实外部 API 写入、KDS 写入、WAES 写入、数据库迁移、schema sync、权限变更、ECS/Aliyun/Caddy/tunnel/Docker 变更、部署、Git push 或 merge。

## Real Round Accounting

- declared_rounds: `1/15`
- substantive_rounds: `1/15`
- generated_items: `7`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`

## 下一目标

`GFIS-RUNTIME-SOP-E2E-189`：构建 `CustomerRequirementOrPlatformOrder` 审阅授权信封提交目录扫描器，证明只有真实、结构化的授权信封提交才能进入审阅路径，并且在真实文件到达前当前 submitted/valid envelopes 继续为零。
