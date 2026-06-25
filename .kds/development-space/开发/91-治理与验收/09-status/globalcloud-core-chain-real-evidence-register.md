---
doc_id: GPCF-DOC-CORE-CHAIN-REAL-EVIDENCE-REGISTER-20260624
title: GlobalCloud 核心链路真实证据台账
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-core-chain-real-evidence-register.md
source_path: 09-status/globalcloud-core-chain-real-evidence-register.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 核心链路真实证据台账

## 1. 台账定位

本文是 `GlobalCloud 项目群实施方案` 下的核心链路真实证据控制台账，用于登记从实施方案到真实研发、真实运行、真实集成、真实交付和客户验收的证据状态。

本文不替代项目实施方案，不把历史 evidence、README、mock、演示页面或脚本存在自动声明为真实运行完成。

项目群下一批真实执行任务、命令、证据、门禁、回滚边界和跨项目依赖由 `GlobalCloud 项目群真实执行治理总控板` 控制，受控文件为 `09-status/globalcloud-project-group-real-execution-governance-board.md`。

## 2. 核心链路范围

本阶段优先控制以下核心链路：

```text
WAES -> XWAIL -> AaaS -> GFIS/GPC/PVAOS -> KDS/Brain
```

控制对象：

- WAES 治理入口和模型/服务发布状态；
- XWAIL 模型契约、Schema、Profile、Validator；
- AaaS ServicePackage、Metering、SLA 和订阅状态；
- GFIS/GPC/PVAOS 业务事实、场景运行和运营状态；
- KDS/Brain 知识证据、候选推理和治理边界；
- GPCF 文档、门禁、LOOP 和证据台账。

## 3. 真实证据状态机

| 状态 | 含义 | 是否可声明完成 |
|---|---|---|
| `not_collected` | 尚未采集真实证据 | 否 |
| `declared` | 方案中已声明需要证据 | 否 |
| `command_defined` | 已明确运行/测试命令 | 否 |
| `candidate` | 已有候选证据，但未完成验证 | 否 |
| `verified` | 内部验证通过 | 仅限内部验证 |
| `ready_for_review` | 可进入人工审查 | 否 |
| `ready_for_uat` | 可进入 UAT | 否 |
| `customer_review` | 用户/客户验收中 | 否 |
| `customer_accepted` | 用户/客户确认通过 | 是，需人工确认 |
| `repair_required` | 证据不完整或验证失败 | 否 |

## 4. 证据最低标准

| 证据类型 | 最低要求 | 不接受 |
|---|---|---|
| 真实进度 | 任务、里程碑、阻塞、下一步、证据路径 | 口头描述 |
| 真实研发 | 代码/配置/脚本变更、测试命令、测试结果、回滚路径 | 只有文档 |
| 真实运行 | 启动命令、健康检查、日志、依赖、最近运行时间 | 只有 README 或截图 |
| 真实集成 | 调用方、被调用方、接口、数据对象、权限、测试结果 | 只有架构图 |
| 真实交付 | 交付包、部署说明、测试报告、已知问题、回滚说明 | 只有构建通过 |
| 客户验收 | 验收场景、验收人、验收结果、签收或退回 | 内部自评 |

## 5. 核心链路真实证据矩阵

| 链路/项目 | 当前实施方案 | 真实进度 | 真实研发 | 真实运行 | 真实集成 | 真实交付 | 客户验收 | 下一步 |
|---|---|---|---|---|---|---|---|---|
| GPCF | `GlobalCloud GPCF 实施方案.md` | `verified` | `candidate` | `candidate` | `declared` | `not_collected` | `not_collected` | 建立 evidence schema 和真实运行记录 |
| WAES | `GlobalCloud WAES 实施方案.md` | `candidate` | `partial_verified` | `repair_required` | `declared` | `not_collected` | `not_collected` | `npm run lint` 失败已在 2026-06-25 复现；WAES 工作区 dirty 且 AGENTS 限制未授权实现，已形成授权包 `docs/harness/WAES/evidence/waes-lint-runtime-repair-authorization-20260625.md` |
| XWAIL | `GlobalCloud XWAIL 实施方案.md` | `candidate` | `candidate` | `repair_required` | `declared` | `not_collected` | `not_collected` | 建立最小 Validator/XAP 命令；证据见 `docs/harness/XWAIL/evidence/xwail-real-runtime-baseline-20260624.md` |
| AaaS | `docs/GlobalCloud AaaS 实施方案.md` | `candidate` | `candidate` | `repair_required` | `declared` | `not_collected` | `not_collected` | 建立最小 ServicePackage/Metering/SLA/EvidenceRequirement 命令；证据见 `docs/harness/AaaS/evidence/aaas-real-runtime-baseline-20260624.md` |
| GFIS | `GlobalCloud GFIS 实施方案.md` | `candidate` | `partial_verified` | `partial_verified` | `partial_verified` | `repair_required` | `not_collected` | 修复外部证据、中文映射、Playwright 浏览器和 ops drill；证据见 `docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md` |
| GPC | `GlobalCloud GPC 实施方案.md` | `candidate` | `partial_verified` | `partial_verified` | `partial_verified` | `repair_required` | `not_collected` | 修复 README 索引、外部证据和 Playwright 浏览器；证据见 `docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md` |
| PVAOS | `GlobalCloud PVAOS 实施方案.md` | `candidate` | `partial_verified` | `partial_verified` | `declared` | `repair_required` | `not_collected` | 修复 Vitest localStorage 环境与 release gate；证据见 `docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md` |
| KDS | `GlobalCloud KDS 实施方案.md` | `candidate` | `partial_verified` | `partial_verified` | `partial_verified` | `repair_required` | `not_collected` | 修复 RAG 准入导出缺失文件、哈希/大小不匹配和 allowlist 准入问题；证据见 `docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md` |
| Brain | `GlobalCloud Brain 实施方案.md` | `ready_for_review` | `verified` | `verified_with_authorization_boundary` | `verified_with_authorization_boundary` | `not_collected` | `not_collected` | A1/A2/A3 授权型闭包证据已在 local dev 范围执行并通过 completion/harness/loop；状态保持 `ready_for_review / authorization_boundary`，证据见 `docs/harness/Brain/evidence/brain-authorized-closure-refresh-execution-20260625.md` |

## 6. 运行命令登记

| 项目 | 已登记命令 | 状态 |
|---|---|---|
| GPCF | `validate_project_group_implementation_plan.py`、`loop_document_gate.py` | `candidate` |
| WAES | `npm run lint`、`npm run check`、`npm run typecheck`、`npm run test`、`npm run build`、`npm run check:wasm`、`validate_waes_lint_runtime_repair_authorization.py` | `authorization_required / repair_required`，`npm run lint` 当前仍因 `AppLazyImports.ts` JSX 解析和 `PluginManager.tsx` import type 解析失败；修复需用户确认 WAES dirty workspace 接管边界 |
| XWAIL | 规划命令 `python scripts/validate_xwail.py --all`、`python scripts/build_xap.py --check`、`python scripts/verify_xap.py --all` 已检查，当前脚本缺失 | `repair_required` |
| AaaS | 规划命令 `python scripts/validate_service_package.py --all`、`python scripts/validate_metering.py --all`、`python scripts/validate_sla.py --all`、`python scripts/verify_evidence_requirements.py --all` 已检查，当前脚本缺失 | `repair_required` |
| GFIS | `npm run check:js`、`npm run quality:100`、`npm run quality:repo`、`npm run test:e2e`、`npm run test:coverage`、`npm run quality:ops` | `partial_verified`，运行态可达、接口/核心流部分通过；外部证据、中文映射、浏览器依赖和 ops drill 仍需修复 |
| GPC | `npm run check:js`、`npm run quality:repo`、`validate_gpc_l3_harness.py`、`validate_gpc_l4_platform_contract.py`、`npm run quality:100`、`npm run test:e2e`、`npm run quality:ops` | `partial_verified`，运行态、ops drill、runtime API、L3/L4 和核心流片段通过；README、外部证据和浏览器依赖仍需修复 |
| PVAOS | `npm run lint`、`npm run validate:modules`、`npm run typecheck`、`npm run test`、`npm run release:gate:local`、`npm run check:production-domain`、`npm run build` | `partial_verified`，lint/modules/typecheck/build/domain 通过；test 与 release gate 仍需修复 |
| KDS | `python3 -m pytest tests/test_api_smoke.py`、`validate_kds_loop_harness.py`、`validate_kds_l4_sample_knowledge_index.py`、`validate_evidence_gates.py`、`validate_rag_export.py`、`gbrain doctor --json --fast`、`gbrain search`、`gbrain query` | `partial_verified`，API smoke、Loop harness、L4 样本索引、evidence gate 与 GBrain 检索通过；`kds_rag_export` 失败，RAG 准入导出仍为 `repair_required` |
| Brain | `npm run lint`、`npm run typecheck`、`npm run test`、`npm run build`、`npm run dev:local`、`npm run validate:runtime-health`、`npm run validate:browser-runtime-smoke`、`npm run validate:browser-user-flow`、`npm run validate:read-closure-matrix`、`npm run validate:chinese-gates`、`npm run validate:projects-write-boundary`、`npm run validate:settings-write-boundary`、`npm run validate:bulk-fix-acceptance-execution`、`npm run validate:chat-llm-boundary`、`npm run validate:completion-matrix`、`npm run validate:harness-evidence`、`npm run validate:loop-harness`、`npm run validate:local-action-boundaries`、`npm run format:check` | `ready_for_review / authorization_boundary`，A1/A2/A3 已按用户授权在 local dev 范围执行；`brain_status=200`、`kds_total_pages=2732`、`test_count=208`、`test_passed=208`、`requirements=11 achieved=11 blockers=0`、`brain_harness_evidence=pass`、`brain_loop_harness=pass` |

## 7. 非声明边界

当前不得声明：

- 不声明任何核心链路项目真实研发完成；
- 不声明任何核心链路项目真实运行完成；
- 不声明任何跨项目接口真实集成完成；
- 不声明任何项目真实交付完成；
- 不声明任何客户验收通过；
- 不声明 accepted、integrated 或 production_ready。

当前可以声明：

```text
core_chain_real_evidence_governance = baseline_controlled
reason = core-chain real evidence register and evidence standards are established; real runtime and integration evidence remain pending
```

## 8. 本轮 WAES 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 采集结论 | `waes_runtime_evidence = partial_verified` |
| 阻塞状态 | `waes_repair_required = lint_parse_errors` |
| 已通过命令 | `npm run typecheck`、`npm run test`、`npm run build`、`npm run check:wasm` |
| 未通过命令 | `npm run check`，失败于 `npm run lint` |
| 边界 | 不声明 WAES 真实运行闭环完成，不声明跨项目真实集成完成，不声明真实交付完成，不声明客户验收通过 |

## 8.1 本轮 WAES lint runtime 授权包登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/WAES/evidence/waes-lint-runtime-repair-authorization-20260625.md` |
| 采集日期 | 2026-06-25 |
| 当前分支 | `waes/integration-release` |
| 工作区状态 | dirty，存在未跟踪 WAES 方案文档和 `tools/` |
| 预检结论 | `git diff --check` pass、`git ls-files -u` pass、lock 检查无输出 |
| 失败命令 | `npm run lint` |
| 失败点 | `src/app/components/AppLazyImports.ts` JSX 位于 `.ts` 文件；`src/app/plugin/PluginManager.tsx` 存在不完整 `import type` |
| 授权状态 | `waes_lint_runtime_repair_authorization = required` |
| 边界 | 未修改 WAES 源码，未提交，未推送，未部署，未升级 WAES 状态 |

## 9. 本轮 XWAIL 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/XWAIL/evidence/xwail-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 治理结论 | `xwail_governance_evidence = verified` |
| 运行结论 | `xwail_runtime_evidence = repair_required` |
| 阻塞状态 | `xwail_repair_required = validator_commands_missing` |
| 已通过命令 | `validate_project_implementation_inheritance.py`、`validate_project_terms_consistency.py`、`validate_project_version_compatibility.py`、`validate_was_xwail_aaas_plan_alignment.py` |
| 缺失命令 | `scripts/validate_xwail.py`、`scripts/build_xap.py`、`scripts/verify_xap.py` |
| 边界 | 不声明 XWAIL Validator 已实现，不声明 XWAIL 工具链闭环完成，不声明 WAES 发布完成，不声明 AaaS 绑定完成 |

## 10. 本轮 AaaS 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/AaaS/evidence/aaas-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 治理结论 | `aaas_governance_evidence = verified` |
| 运行结论 | `aaas_runtime_evidence = repair_required` |
| 阻塞状态 | `aaas_repair_required = service_package_metering_sla_commands_missing` |
| 已通过命令 | `validate_project_implementation_inheritance.py`、`validate_project_terms_consistency.py`、`validate_project_version_compatibility.py`、`validate_was_xwail_aaas_plan_alignment.py` |
| 缺失命令 | `scripts/validate_service_package.py`、`scripts/validate_metering.py`、`scripts/validate_sla.py`、`scripts/verify_evidence_requirements.py` |
| 边界 | 不声明 AaaS 服务包已实现，不声明计量/SLA 已真实运行，不声明客户可订阅状态达成，不声明商业交付完成 |

## 11. 本轮 GFIS 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 运行结论 | `gfis_runtime_evidence = partial_verified` |
| 接口结论 | `gfis_interface_evidence = partial_verified` |
| 阻塞状态 | `gfis_repair_required = external_evidence_branding_browser_ops_drill` |
| 已通过命令/片段 | `npm run check:js`；`quality:repo` 中 API contract、core flow、external contract smoke、work-order API、WAES gate event 等片段通过；`quality:ops` 中 operational preflight 通过 |
| 未通过命令 | `npm run quality:100`、`npm run quality:repo`、`npm run test:e2e`、`npm run test:coverage`、`npm run quality:ops` |
| 边界 | 不声明 GFIS 真实交付完成，不声明外部联调完成，不声明客户验收通过，不声明 production_ready |

## 12. 本轮 GPC 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 运行结论 | `gpc_runtime_evidence = partial_verified` |
| 接口结论 | `gpc_interface_evidence = partial_verified` |
| L3/L4 结论 | `gpc_l3_l4_evidence = verified` |
| 阻塞状态 | `gpc_repair_required = readme_external_evidence_browser` |
| 已通过命令/片段 | `npm run check:js`、`validate_gpc_l3_harness.py`、`validate_gpc_l4_platform_contract.py`、`npm run quality:ops`；`quality:repo` 中 smoke、API contract、core flow、external contract smoke 等片段通过 |
| 未通过命令 | `npm run quality:repo`、`npm run quality:100`、`npm run test:e2e` |
| 边界 | 不声明 GPC 真实交付完成，不声明外部联调完成，不声明客户验收通过，不声明 production_ready |

## 13. 本轮 PVAOS 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 构建结论 | `pvaos_build_evidence = verified` |
| 域名结论 | `pvaos_domain_evidence = verified` |
| 运行结论 | `pvaos_runtime_evidence = partial_verified` |
| 阻塞状态 | `pvaos_repair_required = localstorage_test_environment_release_gate` |
| 已通过命令 | `npm run lint`、`npm run validate:modules`、`npm run typecheck`、`npm run check:production-domain`、`npm run build` |
| 未通过命令 | `npm run test`、`npm run release:gate:local` |
| 边界 | 不声明 PVAOS 发布完成，不声明客户验收通过，不声明 AaaS 运营闭环完成，不声明 production_ready |

## 14. 本轮 KDS 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| API 结论 | `kds_api_smoke = verified` |
| Loop 结论 | `kds_loop_harness = verified` |
| 索引结论 | `kds_l4_sample_knowledge_index = ready_for_review` |
| 检索结论 | `kds_gbrain_search = partial_verified` |
| 阻塞状态 | `kds_rag_export = repair_required` |
| 已通过命令 | `python3 -m pytest tests/test_api_smoke.py`、`validate_kds_loop_harness.py`、`validate_kds_l4_sample_knowledge_index.py`、`validate_evidence_gates.py`、`gbrain search`、`gbrain query` |
| 未通过命令 | `validate_rag_export.py`，失败于 185 个错误和 1 个 warning |
| 边界 | 不声明 KDS 真实运行闭环完成，不声明 RAG 导出完成，不声明真实交付完成，不声明客户验收通过 |

## 15. 本轮 Brain 证据登记

| 项 | 内容 |
|---|---|
| 证据文件 | `docs/harness/Brain/evidence/brain-real-runtime-baseline-20260624.md` |
| 采集日期 | 2026-06-24 |
| 研发结论 | `brain_static_check/typecheck/unit_tests/build = verified` |
| 运行结论 | `brain_runtime_health = verified`，但整体运行闭环仍为 `partial_verified` |
| 集成结论 | `brain_harness_evidence = repair_required` |
| 阻塞状态 | `brain_repair_required = status_audit_backend_write_closure_bulk_fix_execution_authorized_prompt_harness_evidence` |
| 已通过命令 | `npm run lint`、`npm run typecheck`、`npm run test`、`npm run build`、`npm run dev:local`、`npm run validate:runtime-health`、`npm run validate:target-panel-runtime-matrix`、`npm run validate:target-panel-data-quality`、`npm run format:check` |
| 候选浏览器证据 | `Chrome Playwright live browser observation` 看到 `总览 (personal)`、`KDS API`、`totalPages=2732`、`graphNodes=280`、`graphEdges=1085`、`8 个结果 · personal · KDS 关键词搜索 · KDS API`、`MMC LLM · 8` |
| 授权契约漂移证据 | `docs/harness/Brain/evidence/brain-team-authorization-contract-drift-20260624.md` |
| 浏览器授权状态 | `brain_chrome_browser_visible_signals = confirmed`；用户已确认 C，`team authorization` 采用读写分层：team 可读 KDS dashboard/graph/search，写入、prompt、secret、持久化操作继续强授权控制，`brain_team_authorization_contract = confirmed_c_read_write_split` |
| 授权刷新请求 | `docs/harness/Brain/evidence/brain-authorized-closure-refresh-request-20260625.md`；用户已确认 A1/A2/A3 local dev 授权 |
| 授权执行结果 | `docs/harness/Brain/evidence/brain-authorized-closure-refresh-execution-20260625.md`；`brain_authorized_closure_refresh_result = verified_with_authorization_boundary` |
| 已通过结果 | `21 test files / 208 tests`、Vite build `2100 modules transformed`、`brain_status=200`、`kds_total_pages=2732`、`projects_write_boundary=pass`、`settings_write_boundary=pass`、`bulk_fix_execution_id=bulk-fix-exec-01249afa30ff`、`chat_llm_prompt_invoked=true`、`completion_matrix requirements=11 achieved=11 blockers=0`、`brain_harness_evidence=pass`、`brain_loop_harness=pass` |
| 当前未通过命令 | 本轮授权范围内未保留未通过 Brain 闭包命令 |
| 关键边界 | 仍不声明生产写入、权限变更、部署、真实交付、客户验收、`accepted`、`integrated` 或 `production_ready` |
| 边界 | Brain 当前最高状态为 `ready_for_review / authorization_boundary`，需后续人工裁决才能升级 |
