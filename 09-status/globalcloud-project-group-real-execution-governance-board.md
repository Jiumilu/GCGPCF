---
doc_id: GPCF-DOC-PROJECT-GROUP-REAL-EXECUTION-GOVERNANCE-BOARD-20260625
title: GlobalCloud 项目群真实执行治理总控板
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-group-real-execution-governance-board.md
source_path: 09-status/globalcloud-project-group-real-execution-governance-board.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群真实执行治理总控板

## 1. 定位

本文承接 `GlobalCloud 项目群实施方案` 与 `GlobalCloud 核心链路真实证据台账`，用于把实施方案体系从文档治理推进到项目群真实执行治理。

本文不替代任何项目的唯一实施方案，也不替代项目群主方案。本文只控制下一批真实执行任务、证据、门禁、回滚边界和跨项目依赖。

## 2. 总体目标

```text
project_group_real_execution_governance = controlled
target = one master implementation system, multiple controlled projects, evidence-driven execution, LOOP continuous closure
status_upgrade_rule = no accepted / integrated / customer acceptance without explicit human confirmation
```

目标拆解：

| 目标 | 控制方式 |
|---|---|
| 对每个项目建立当前真实状态基线 | 以 `globalcloud-core-chain-real-evidence-register.md` 和项目 evidence 为基线 |
| 明确每个项目下一批可执行任务 | 本文第 5 节任务队列 |
| 每个任务绑定命令、证据、门禁、回滚边界 | 本文第 6 节任务控制字段和第 7 节任务执行控制矩阵 |
| 将项目间依赖纳入矩阵 | 本文第 8 节依赖矩阵 |
| 逐步推进到 `ready_for_review` | 只允许通过 evidence 与 gate 推进 |
| 人工确认后才允许 `accepted`、`integrated`、客户验收 | 本文第 8 节状态升级门禁 |

## 3. 当前真实状态基线

| 项目 | 当前状态 | 证据基线 | 当前推进边界 |
|---|---|---|---|
| WAES | `repair_required` | `docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md` | lint 解析错误阻断综合检查；不得声明治理运行闭环完成 |
| XWAIL | `repair_required` | `docs/harness/XWAIL/evidence/xwail-real-runtime-baseline-20260624.md` | Validator/XAP 命令缺失；不得声明工具链闭环完成 |
| AaaS | `repair_required` | `docs/harness/AaaS/evidence/aaas-real-runtime-baseline-20260624.md` | ServicePackage/Metering/SLA/EvidenceRequirement 命令缺失；不得声明客户可订阅 |
| GFIS | `partial_verified / repair_required` | `docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md` | 缺真实 source-of-record 与外部证据；不得用测试数据替代真实业务事实 |
| GPC | `partial_verified` | `docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md` | README、外部证据和浏览器依赖仍需修复；不得声明外部联调完成 |
| PVAOS | `partial_verified` | `docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md` | Vitest localStorage 与 release gate 仍需修复；不得声明发布完成 |
| KDS | `partial_verified / repair_required` | `docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md` | RAG 导出失败；不得声明 RAG 导出或真实交付完成 |
| Brain | `ready_for_review / authorization_boundary` | `docs/harness/Brain/evidence/brain-authorized-closure-refresh-execution-20260625.md` | A1/A2/A3 已通过，但不得升级 accepted、integrated、production_ready |
| GPCF | `repair_required` | `09-status/globalcloud-core-chain-real-evidence-register.md` | 作为总控仓需继续把真实执行治理传导到任务队列与依赖矩阵 |
| WAS | `semantic_foundation_candidate / not_accepted` | `09-status/gpcf-project-status-matrix.md` | 作为语义契约源，不替代 KDS 事实主存、GFIS 运行层或 WAES 裁决层 |

## 4. 下一阶段执行原则

| 原则 | 约束 |
|---|---|
| 真实优先 | 运行、集成、交付、验收必须绑定当前命令输出或外部事实证据 |
| 边界优先 | 任何 `partial_verified`、`ready_for_review` 都必须保留未完成边界 |
| 不越权 | 不执行生产写入、部署、权限变更、客户通知，除非用户另行明确授权 |
| 不混淆 | 设计文档、README、mock、fixture、测试数据不得替代真实运行事实 |
| 可回滚 | 每个执行任务必须有回滚或撤销路径 |
| 可传导 | 项目任务状态变化必须回写本总控板和核心链路真实证据台账 |

## 5. 下一批真实执行任务队列

| 优先级 | 任务 ID | 项目 | 目标 | 当前状态 | 执行入口 |
|---|---|---|---|---|---|
| P0 | `GFIS-REAL-SOR-001` | GFIS | 获取或登记真实 source-of-record，形成 pending_business_verification 输入 | `authorization_or_business_input_required` | 等待真实客户订单、平台订单回执或等效正式确认 |
| P0 | `WAES-LINT-RUNTIME-001` | WAES | 修复 lint 解析错误并恢复综合 `npm run check` | `repair_required` | WAES 仓本地质量门禁 |
| P0 | `KDS-RAG-EXPORT-001` | KDS | 修复 RAG 导出缺失文件、哈希/大小和 allowlist 问题 | `repair_required` | KDS `validate_rag_export.py` |
| P1 | `XWAIL-MIN-VALIDATOR-001` | XWAIL | 建立最小 Validator/XAP 命令，使规划命令有真实执行入口 | `command_missing` | `scripts/validate_xwail.py`、`scripts/build_xap.py`、`scripts/verify_xap.py` |
| P1 | `AAAS-SERVICE-RUNTIME-001` | AaaS | 建立 ServicePackage、Metering、SLA、EvidenceRequirement 最小验证命令 | `command_missing` | `scripts/validate_service_package.py` 等 |
| P1 | `PVAOS-RELEASE-GATE-001` | PVAOS | 修复 Vitest localStorage 环境与 local release gate | `repair_required` | `npm run test`、`npm run release:gate:local` |
| P1 | `GPC-EVIDENCE-BROWSER-001` | GPC | 修复 README 索引、外部证据和浏览器依赖 | `repair_required` | `npm run quality:repo`、`npm run quality:100`、`npm run test:e2e` |
| P1 | `BRAIN-REVIEW-HANDOFF-001` | Brain | 将 Brain 从授权边界证据转为人工审查包 | `ready_for_review / authorization_boundary` | Brain harness evidence 与 GPCF 执行结果文档 |
| P2 | `GPCF-EXECUTION-CONTROL-001` | GPCF | 维护项目群真实执行总控板、依赖矩阵和状态传导验证器 | `in_progress` | 本文与 `validate_project_group_real_execution_governance_board.py` |

## 6. 任务控制字段

每个任务进入执行前必须补齐以下字段：

| 字段 | 必填要求 |
|---|---|
| `task_id` | 与第 5 节一致 |
| `project` | 项目名和仓库路径 |
| `baseline_evidence` | 当前基线证据文件 |
| `commands` | 至少一个可复现命令 |
| `expected_evidence` | 预期新增或更新的 evidence 文件 |
| `gate` | 对应 validator 或质量门禁 |
| `rollback` | 文件回滚、配置撤销或状态降级方式 |
| `dependency_impact` | 影响哪些上游/下游项目 |
| `human_confirmation_required` | 是否需要用户或业务方确认 |
| `forbidden_claims` | 禁止声明的状态 |

## 7. 任务执行控制矩阵

| task_id | project | baseline_evidence | commands | expected_evidence | gate | rollback | dependency_impact | human_confirmation_required | forbidden_claims |
|---|---|---|---|---|---|---|---|---|---|
| `GFIS-REAL-SOR-001` | GFIS | `docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md` | `validate_gfis_was_source_record_submission_precheck.py`、GFIS 真实 source-of-record 接收目录扫描、人工核验记录检查 | `docs/harness/GFIS/evidence/gfis-real-source-record-intake-*.md`、真实订单或平台订单回执索引、人工核验结论 | GFIS source-record validator、GPCF core-chain register gate、WAES review gate | 不写入 GFIS runtime；若输入不合格，保持 `repair_required` 并登记 rejected reason | 解锁 `GFIS/GPC/PVAOS -> SCaaS`，影响 WAS profile、KDS backlink、WAES review | 是，需要订单 owner 或等效正式确认 | 不声明真实 SOP E2E 完成、不声明生产写入、不声明客户验收、不声明 `accepted`/`integrated`/`production_ready` |
| `WAES-LINT-RUNTIME-001` | WAES | `docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md` | `npm run lint`、`npm run check`、`npm run typecheck`、`npm run test`、`npm run build`、`npm run check:wasm` | `docs/harness/WAES/evidence/waes-lint-runtime-repair-*.md`、命令输出 JSON 或日志摘要 | WAES quality gate、GPCF core-chain register gate | 回滚 lint 修复相关文件；若 `npm run check` 失败，保持 `repair_required` | 影响 `WAES -> XWAIL -> AaaS` 和 Brain/KDS 证据裁决链 | 否，除非需要修改权限、部署或外部服务 | 不声明 WAES 治理运行闭环完成、不声明发布、不声明权限变更 |
| `KDS-RAG-EXPORT-001` | KDS | `docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md` | `python3 -m pytest tests/test_api_smoke.py`、`python3 scripts/validate_rag_export.py`、`python3 scripts/validate_evidence_gates.py`、`gbrain search`、`gbrain query` | `docs/harness/KDS/evidence/kds-rag-export-repair-*.md`、RAG export error diff、allowlist/hash/size 修复证据 | KDS RAG export gate、evidence gate、GPCF core-chain register gate | 回滚导出清单、allowlist 或生成物；失败时保留失败 evidence | 影响 `KDS -> Brain`、Brain 检索与 RAG 上下文可信度 | 否，除非需要真实 TOKEN、生产索引或外部写入 | 不声明 RAG 导出完成、不声明真实交付、不声明客户验收 |
| `XWAIL-MIN-VALIDATOR-001` | XWAIL | `docs/harness/XWAIL/evidence/xwail-real-runtime-baseline-20260624.md` | `python scripts/validate_xwail.py --all`、`python scripts/build_xap.py --check`、`python scripts/verify_xap.py --all` | `docs/harness/XWAIL/evidence/xwail-min-validator-runtime-*.md`、最小 schema/profile/XAP 验证输出 | XWAIL validator gate、WAS-XWAIL-AaaS alignment gate、GPCF register gate | 回滚新增脚本或样例模型；失败时保持 `validator_commands_missing` | 影响 `WAS -> Ontology -> XWAIL` 和 `WAES -> XWAIL -> AaaS` | 否 | 不声明完整 XWAIL 工具链完成、不声明 WAES 发布完成、不声明 AaaS 绑定完成 |
| `AAAS-SERVICE-RUNTIME-001` | AaaS | `docs/harness/AaaS/evidence/aaas-real-runtime-baseline-20260624.md` | `python scripts/validate_service_package.py --all`、`python scripts/validate_metering.py --all`、`python scripts/validate_sla.py --all`、`python scripts/verify_evidence_requirements.py --all` | `docs/harness/AaaS/evidence/aaas-service-runtime-*.md`、ServicePackage/Metering/SLA/EvidenceRequirement 验证输出 | AaaS service runtime gate、XWAIL binding gate、GPCF register gate | 回滚新增服务包样例或计量规则；失败时保持 `service_package_metering_sla_commands_missing` | 影响 SCaaS 服务化交付、GFIS/GPC/PVAOS 服务订阅边界 | 否，除非涉及真实计费、客户订阅或生产 SLA | 不声明客户可订阅、不声明商业交付完成、不声明真实计费完成 |
| `PVAOS-RELEASE-GATE-001` | PVAOS | `docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md` | `npm run test`、`npm run release:gate:local`、`npm run lint`、`npm run typecheck`、`npm run build` | `docs/harness/PVAOS/evidence/pvaos-release-gate-repair-*.md`、localStorage 环境修复证据、release gate 输出 | PVAOS release local gate、GPCF register gate | 回滚测试环境或 release gate 配置；失败时保持 `repair_required` | 影响 `GFIS/GPC/PVAOS -> SCaaS` 门户与运营入口 | 否，除非触发发布、外部 API 或权限变更 | 不声明发布完成、不声明客户验收、不声明 AaaS 运营闭环完成 |
| `GPC-EVIDENCE-BROWSER-001` | GPC | `docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md` | `npm run quality:repo`、`npm run quality:100`、`npm run test:e2e`、`npm run quality:ops` | `docs/harness/GPC/evidence/gpc-evidence-browser-repair-*.md`、README 索引、外部证据、浏览器依赖修复输出 | GPC quality repo gate、browser/e2e gate、GPCF register gate | 回滚 README 索引或浏览器依赖改动；失败时保持 `partial_verified` | 影响 SCaaS 场景展示、GFIS/GPC/PVAOS 业务链路 | 否，除非需要真实外部联调或客户环境 | 不声明外部联调完成、不声明真实交付、不声明客户验收 |
| `BRAIN-REVIEW-HANDOFF-001` | Brain | `docs/harness/Brain/evidence/brain-authorized-closure-refresh-execution-20260625.md` | `npm run validate:completion-matrix`、`npm run validate:harness-evidence`、`npm run validate:loop-harness`、GPCF 执行结果验证器 | `docs/harness/Brain/evidence/brain-review-handoff-*.md`、人工审查包、边界确认清单 | Brain harness gate、GPCF Brain execution gate、human review gate | 不改 Brain 运行证据；若人工未确认，保持 `ready_for_review / authorization_boundary` | 影响 `KDS -> Brain` review、项目群 ready_for_review 样板 | 是，需要人工确认才能升级 | 不声明 `accepted`、`integrated`、`production_ready`、客户验收 |
| `GPCF-EXECUTION-CONTROL-001` | GPCF | `09-status/globalcloud-core-chain-real-evidence-register.md` | `python3 tools/kds-sync/validate_project_group_real_execution_governance_board.py`、`python3 tools/kds-sync/validate_core_chain_real_evidence_register.py`、`python3 tools/kds-sync/loop_document_gate.py` | `09-status/globalcloud-project-group-real-execution-governance-board.md`、项目群真实执行任务变更记录 | GPCF execution governance board gate、document control gate、Loop document gate | 回滚总控板对应状态变更；若门禁失败，最高状态为 `partial/rework` | 影响所有项目状态传导、依赖矩阵和下一轮任务选择 | 否，除非要升级项目状态或执行跨仓真实写入 | 不声明项目群完成、不声明全部 ready_for_review、不声明客户验收 |

## 8. 项目间依赖矩阵

| 依赖链 | 当前状态 | 风险 | 下一步 |
|---|---|---|---|
| `WAES -> XWAIL -> AaaS` | `declared / repair_required` | XWAIL/AaaS 缺最小运行命令，WAES 综合检查受 lint 阻断 | 先修 WAES lint，再补 XWAIL/AaaS 最小 validator |
| `KDS -> Brain` | `partial_verified -> ready_for_review` | Brain 已通过授权型闭包，KDS RAG export 仍 repair_required | 保持 Brain review 包；并行修复 KDS RAG export |
| `GFIS/GPC/PVAOS -> SCaaS` | `partial_verified / repair_required` | GFIS 缺真实 source-of-record；GPC/PVAOS 仍有证据和 release gate 缺口 | 优先 GFIS 真实业务输入，其次修 GPC/PVAOS 门禁 |
| `WAS -> Ontology -> XWAIL` | `semantic_foundation_candidate` | WAS 是语义契约源，但不能替代事实主存或运行层 | 将 WAS 术语和 profile 映射为 XWAIL validator 输入 |
| `GPCF -> all projects` | `controlled / in_progress` | 总控台账已存在，但任务队列与传导验证需要持续更新 | 本文建立后由 validator 守住任务、依赖和禁止声明 |

## 9. 状态升级门禁

| 目标状态 | 必要条件 |
|---|---|
| `candidate` | 有实施方案、命令或证据入口，但尚未通过完整门禁 |
| `partial_verified` | 至少一个真实命令或真实运行片段通过，并明确剩余边界 |
| `ready_for_review` | 项目内关键门禁通过，GPCF 侧证据台账已更新，禁止声明已保留 |
| `ready_for_uat` | 有可复现用户场景、数据、环境、回滚方案和人工审查结论 |
| `accepted` | 用户明确确认 |
| `integrated` | 依赖项目均通过相应集成门禁，且用户明确确认 |
| `customer_accepted` | 客户验收人、验收场景、验收结果和签收证据齐备 |

任何项目不得仅凭以下内容升级：

- README 或方案存在；
- mock、fixture、synthetic/dev-only 数据；
- 单一截图；
- 仅构建通过；
- 仅本地 UI 可见；
- 旧 evidence 未刷新；
- 未经授权的生产、权限或部署动作。

## 10. 回滚与恢复

| 场景 | 恢复动作 |
|---|---|
| 项目命令失败 | 保持原状态，新增 `repair_required` 证据，不覆盖历史通过证据 |
| 证据口径漂移 | 建立 drift 文档，更新 validator，禁止直接提升状态 |
| 跨项目依赖冲突 | 将上游/下游均标记为 `dependency_review_required` |
| 误声明完成 | 回滚状态文本，补充禁止声明验证器 |
| TOKEN 或权限问题 | 立即停止执行，状态最高为 `blocked` 或 `authorization_required` |

## 11. 本轮结论

```text
project_group_real_execution_board = established
next_execution_mode = project_by_project_real_gate_repair
first_priority = GFIS real source-of-record, WAES lint/runtime gate, KDS RAG export
brain_status = ready_for_review / authorization_boundary
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```
