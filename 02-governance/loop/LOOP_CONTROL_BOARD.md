---
doc_id: GPCF-DOC-0DF6AA8647
title: Loop Control Board
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CONTROL_BOARD.md
source_path: 02-governance/loop/LOOP_CONTROL_BOARD.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Control Board

## 当前运行状态

| 字段 | 当前值 |
|---|---|
| 当前 Loop 模式 | L4 自我纠错与 GFIS 运行层修复 |
| 本轮最新校准 | `GPCF-L4-GFIS-REPAIR-251` 已回写：已将 `CustomerRequirementOrPlatformOrder` pending business verification manual completion release-ready package release override approval request dispatch confirmation hold release negative fixture guard 落入 GFIS 真项目仓运行层 API 与主 validator，输出 `source_hold_release_precheck_items=1 source_blocked=1 source_blocked_reasons=6 source_release_allowed_items=0 weak_release_attempt_count=6 rejected_release_attempt_count=6 accepted_release_attempt_count=0 confirmation_files_found=0 valid_confirmations=0 missing_confirmations=1 owner_response_allowed=0 submission_package_allowed=0 dispatch_allowed=0 request_items_dispatched=0 release_override_allowed=0 release_allowed_items=0 hold_items=1 open_holds=1 hold_release_allowed=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 runtime_sop_e2e=repair_required`。本轮只证明 GFIS Demo、KDS candidate-only、用户口述、Loop 文档、缺 hash/KDS backlink 或缺 WAES candidate 的弱放行声明不得释放 open hold；不得升级 accepted/integrated |
| 可升级模式 | L4 repair active；L5 暂停，必须等 GFIS 运行层证据与完整 SOP E2E 修复后再评估 |
| 当前主线项目 | GFIS / GPCF |
| 当前轮次 | `GPCF-L4-GFIS-REPAIR-251`：GFIS pending business verification manual completion release-ready package release override approval request dispatch confirmation hold release negative fixture guard |
| 当前阶段 | L4 repair；GFIS 运行层仍是唯一 SOP 主体。本轮完成 pending_business_verification manual completion release-ready package release override approval request dispatch confirmation hold release negative fixture guard，同步确认 `source_hold_release_precheck_items=1`、`source_blocked=1`、`source_blocked_reasons=6`、`source_release_allowed_items=0`、`weak_release_attempt_count=6`、`rejected_release_attempt_count=6`、`accepted_release_attempt_count=0`、`confirmation_files_found=0`、`valid_confirmations=0`、`missing_confirmations=1`、`hold_release_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`；本轮未执行删除、reset、checkout、提交、推送或生产配置变更 |
| 当前目标 | 以 GFIS 运行层为唯一 SOP 主体，把辽宁远航报价来源、合同链、现代精工 OEM 当前运行层定位、未来葛化自建工厂运行层定位、签章完成件接收门禁、真实回执接收目录、KDS backlink receipt、KDS 候选发现、客户商业补证、authorization envelope、review/runtime/WAES 阻断全部纳入完整 runtime SOP E2E 主门禁；本轮不证明真实 KDS 写入回执、签章完成、客户确认函、采购订单/合同、客户规格/封样、PP/改性料规格、上机窗口、首批 1 吨闭环验收、出厂全检、客户验收/POD、生产写入、物流 API、资金事实、人工验收或 accepted/integrated 完成 |
| 当前涉及项目 | GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、GPCF |
| 当前状态判定 | `partial_repair`；GFIS 运行层 SOP E2E 仍为 `repair_required`。本轮只证明 `CustomerRequirementOrPlatformOrder` dispatch confirmation open hold 不得被 GFIS Demo、KDS candidate-only、用户口述、Loop 文档、缺 hash/KDS backlink 或缺 WAES candidate 的弱放行声明释放；仍无真实 pending 文件、合规人工核验完成文件、有效 release-ready package、有效 source-of-record、有效派发确认、运行层主键、review queue、runtime intake、WAES review 或 verified artifact；不得升级 accepted/integrated |
| 本轮新增事实 | GFIS 真项目仓新增 pending business verification manual completion release-ready package release override approval request dispatch confirmation hold release negative fixture guard JSON/Markdown evidence、builder、validator、只读 API，并在 `scripts/validate_gfis_runtime_sop_e2e.py` 接入主门禁。输出 `source_hold_release_precheck_items=1 source_blocked=1 source_blocked_reasons=6 source_release_allowed_items=0 weak_release_attempt_count=6 rejected_release_attempt_count=6 accepted_release_attempt_count=0 confirmation_files_found=0 valid_confirmations=0 missing_confirmations=1 owner_response_allowed=0 submission_package_allowed=0 dispatch_allowed=0 request_items_dispatched=0 release_override_allowed=0 release_allowed_items=0 hold_items=1 open_holds=1 hold_release_allowed=0 runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 runtime_sop_e2e=repair_required`。本轮不创建业务凭证、人工批准事实、人工核验完成事实、有效 release-ready package、外部通知发送事实、dispatch confirmation 或运行层主键 |
| KDS TOKEN | 已配置于本机私有文件；`validate_kds_token.py` pass，fingerprint=`bfd9553d`；不得写入 Git/文档/evidence/log |
| L3 上限 | 最多 15 轮或 2 小时，以先到者为准 |
| L3 session | stopped |
| L3 已完成轮次 | 1/15 |
| L3 剩余轮次 | 14 |
| L3 已用时间 | 未做统一分钟级计时；仍未达到 2 小时上限 |
| L3 stop_type | authorization_boundary |
| L3 stop_evidence | 全项目提交推送后重新运行 `python3 tools/kds-sync/assess_l3_admission.py`，11 个业务项目均为 L3 Ready；GPCF 保持 governance_hub；所有仓库 `git status --short --branch` clean/up-to-date；本轮只做总控证据校准，不执行生产写入、权限变更、部署、真实外部 API、Docker 部署、设备 OTA 或 accepted/integrated 升级 |
| L3 final answer guard | stopped；`stop_type=authorization_boundary` 是允许 final 收口条件 |
| 连续运行真实性门禁 | pass |
| continuous declared_rounds | 17/30 |
| continuous substantive_rounds | 17/30 |
| continuous generated_items | 101 |
| continuous batch_generated | false |
| continuous substance_gate | pass |
| continuous substance_evidence | `GPCF-L4-001` 建立项目群控制面；`MMC-L4-002`、`KDS-L4-003`、`Brain-L4-004`、`PKC-L4-005`、`PVAOS-L4-006`、`GPC-L4-007`、`XiaoC-L4-009`、`XGD-L4-010`、`XiaoG-L4-011` 保持各自 L4 dry-run/mock/read-only evidence；`GFIS-L4-008` 被纠偏为 repair_required，因为其核心 fixture 来自 `gcfis_demo`；`GFIS-RUNTIME-SOP-E2E-001/002` 证明 Demo E2E pass 不等于运行层 SOP pass，KDS source path 当前真实缺口为 2，当前仍缺 5 项 KDS 葛化真实业务输入；`GPCF-L4-012` 原 100/100 被 `GPCF-L4-CORR-001` 降级，当前随 KDS source path 修复校准为 78/100 L4 repair；当前不执行生产写入、真实外部 API、权限变更、部署、数据库迁移、设备 OTA 或 accepted/integrated 升级 |
| corrected stop_type | authorization_boundary |
| 连续运行默认继续规则 | L3/L3.5/L4/L5 active 时未触发硬停止、用户停止、预算耗尽、时间耗尽、授权边界或任务队列为空，必须继续下一轮 |
| 连续运行阶段性汇报 | 不是停止条件；只能作为 evidence 或进度说明 |
| 连续运行停止记录要求 | 必须记录模式、停止类型、停止证据、已完成轮次、剩余轮次、已用时间和下一步 |
| L3.5 状态 | executable / requires explicit activation；最多 5 轮或 1 小时 |
| L4 状态 | active；最多 30 轮或 4 小时 |
| L5 状态 | executable / not activated；完全生产自治；最多 10 轮或 2 小时 |

## 当前允许动作

| 动作 | 是否允许 | 条件 |
|---|---|---|
| 读取和分析本地文档 | 是 | 必须保护用户已有工作 |
| 新增/修订受控文档 | 是 | 必须有 front matter，并进入文档控制台账 |
| 新增/修订本地校验脚本 | 是 | 不得写入真实 TOKEN 或生产配置 |
| 运行本地质量、文档、污染、KDS 镜像检查 | 是 | 只读或本地镜像范围 |
| dry-run / mock / fixture / validator | 是 | 不触达生产和真实外部写入 |
| L3.5 真实接口验证 | 受限 | 仅显式启动，且满足白名单、可回滚、可审计、时间窗和 evidence 要求 |
| L4 全自动运营 | 受限 | 仅显式启动，默认不触达生产部署和真实生产写入 |
| L5 完全生产自治 | 强授权 | 仅 L5 强授权口令完整时可启动 |
| 本地 commit | 受限 | 仅 L3 且 Git 状态清晰、变更范围受控、无敏感文件；默认不自动提交 |

## 当前禁止动作

| 动作 | 禁止原因 |
|---|---|
| Git push / 合并主分支 | 需要用户明确授权 |
| 删除文件或大规模迁移 | 需要用户明确授权和回滚方案 |
| 写入真实 KDS TOKEN | 安全边界未授权 |
| 真实 KDS API 双向同步 | `开发` 空间 read/write/edit 已跑通；非 `开发` 空间访问 403；仍需按工具链留审计流水 |
| 未授权真实外部 API 写入 | 必须人工确认；L3.5/L4/L5 只按专项政策与显式授权执行 |
| 生产配置修改或部署 | 必须人工确认 |
| ECS / 阿里云 / Caddy / 隧道 / Docker 运行配置修改 | Hermes 永远只读；Loop 不得自动执行；仅 Codex 当前会话在明确授权、回滚和审计条件满足时可作为变更入口；控制规则见 `02-governance/ops/ecs-access-control-and-network-boundary.md` |
| `bench migrate` / schema sync / 运行态写 API | GFIS 当前仍未取得迁移授权 |
| 标记 `accepted` / `integrated` | 必须用户人工确认且满足状态门禁 |

## 最近门禁状态

| 门禁 | 最近结果 | 说明 |
|---|---|---|
| Git 门禁 | partial | GPCF/GFIS dirty 状态已分类：GPCF high_risk=2、GFIS high_risk=3；无 deleted/missing。高风险项需人工复核后才可进入提交候选；本轮不提交不推送 |
| 文档污染检查 | pass | `check_document_pollution.py` 最近通过 |
| KDS 镜像冲突 | pass | `kds_conflict_guard.py` 最近通过 |
| Loop 运行门禁 | pass | `loop_operational_gates.py` 最近通过 |
| GFIS 质量门禁 | partial | GFIS Demo E2E 只允许作为 `pass_demo_only` 展示层回归；GFIS 运行层 SOP E2E validator 输出 `repair_required`。本轮新增并接入 GFIS 真项目仓 pending business verification manual completion release-ready package release attempt hard-stop audit；当前 `source_open_holds=1`、`release_attempt_audit_items=1`、`attempted_release=1`、`hard_stops=1`、`hard_stop_reasons=8`、`blocked=1`、`release_ready_files_found=0`、`schema_valid_release_ready_files=0`、`release_ready_packages=0`、`release_allowed_items=0`、`manual_business_verification_completed=0`、`valid_source_records=0`、`hold_items=1`、`open_holds=1`、`hold_release_allowed=0`、`manual_completion_release_allowed=0`、`runtime_primary_key_ready=0`、`review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`。完整 SOP E2E 未通过前不得升级验收 |
| XiaoC L4 门禁 | pass | `node scripts/validate_xiaoc_l4_agent_orchestration.mjs`、`node scripts/validate_xiaoc_loop_harness.mjs`、`pnpm test:repo`、`git diff --check -- .` 均通过 |
| XGD L4 门禁 | pass | `node scripts/validate_xgd_l4_risk_analysis.mjs`、`npm run harness:validate`、`npm test`、`git diff --check -- .` 均通过 |
| XiaoG L4 门禁 | pass | `python3 scripts/validate_xiaog_l4_readonly_audit_mock.py`、legacy L3 validators/smoke/test、`git diff --check -- .` 均通过 |
| GPCF L4 收口门禁 | repair_required | `validate_loop_self_correction_gate.py` 与 `validate_l4_minimum_closed_loop.py` 已纳入 GFIS 运行层 SOP validator；当前必须输出 78/100 repair，直到 GFIS 运行层证据和 SOP E2E 修复 |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d`；私有 env 不入库 |

## 当前待确认项

| 项 | 状态 | 下一步 |
|---|---|---|
| 现场真实样本 | 未收到 | 建立样本回收跟踪台账 |
| UAT 签收 | 未收到 | 建立问题分级与签收跟踪模板 |
| GPC/Finance 边界确认 | 未收到 | 保持金融事实 L4 阻断 |
| WAES 门禁语义确认 | 未收到 | 保持 fixture/contract 层 |
| KDS TOKEN | 已完成 | 本机私有 env 已配置，真实 `开发` 空间 API 同步已跑通；继续禁止泄露 Token |
| L3.5/L4/L5 启动 | 未启动 | 已形成可执行方案，但除非出现明确启动口令或强授权口令，否则不得进入 |
| 连续运行偏差 | 已修正规则 | 阶段性收口汇报不得导致 L3/L3.5/L4/L5 停止；未触发停止条件时继续下一轮 |
| L3 三轮误停止 | 已建立防复发门禁 | `validate_l3_continuation_guard.py` 拦截 `3/15` 阶段性 final 收口 |
| 第二轮 L3 15/15 收口 | 已完成 | `GPCF-GF-LR-046` 至 `GPCF-GF-LR-060` 已跑满第二轮 L3 15/15，stop_type 为 budget_exhausted |
| GPCF 本轮 L3 15/15 收口 | 已完成 | `GPCF-CF-LR-002` 至 `GPCF-CF-LR-016` 已跑满 GPCF 主线 L3 15/15，stop_type 为 budget_exhausted |
| GPCF 项目准备度 L3 15/15 收口 | 已完成 | `GPCF-CF-LR-017` 至 `GPCF-CF-LR-031` 已跑满 12 项目准备度 L3 15/15，stop_type 为 budget_exhausted |
| KDS Token 完成登记 | 已完成 | `GPCF-CF-LR-032` 登记本机私有 Token、fingerprint=`bfd9553d`、真实 `开发` 空间 API 同步与审计流水 |
| 连续运行真实性规则 | 已建立 | L3/L3.5/L4/L5 均必须区分 `declared_rounds`、`generated_items` 与 `substantive_rounds`；批量生成默认最多计 1 个实质轮次 |
| 批量生成纠偏 | 已登记 | `GPCF-CF-LR-017` 至 `GPCF-CF-LR-031` 更正为 declared_rounds=15、substantive_rounds=1、substance_gate=partial、corrected stop_type=authorization_boundary |
| MMC 初始化 | 已完成 | `GPCF-MM-LR-001` 完成 MMC Manifest、loop-state、evidence-index、loop record 和 validator；本次计为 1 个实质轮次 |
| KDS 初始化 | 已完成 | `GPCF-KD-LR-001` 完成 KDS loop-state、evidence-index、loop record 和 validator；本次累计 2 个实质轮次 |
| Brain 初始化 | 已完成 | `GPCF-BR-LR-001` 完成 Brain loop-state、evidence-index、loop record 和 validator；本次累计 3 个实质轮次 |
| PKC 初始化 | 已完成 | `GPCF-PK-LR-001` 完成 PKC loop-state、evidence-index、loop record 和 validator；本次累计 4 个实质轮次 |
| XiaoC 初始化 | 已完成 | `GPCF-XC-LR-001` 完成 XiaoC loop-state、evidence-index、loop record 和 validator；本次累计 5 个实质轮次 |
| XGD 初始化 | 已完成 | `GPCF-XD-LR-001` 完成 XGD loop-state、evidence-index、loop record 和 validator；本次累计 6 个实质轮次 |
| GPC 初始化 | 已完成 | `GPCF-GP-LR-001` 完成 GPC loop-state、evidence-index、loop record 和 validator；不改一期蓝图，本次累计 7 个实质轮次 |
| XiaoG 初始化 | 已完成 | `GPCF-XG-LR-001` 完成 XiaoG loop-state、evidence-index、loop record 和 validator；本次累计 8 个实质轮次 |
| PVAOS 初始化 | 已完成 | `GPCF-PV-LR-001` 完成 PVAOS loop-state、evidence-index、loop record 和 validator；本次累计 9 个实质轮次 |
| WAES 初始化 | 已完成 | `GPCF-WA-LR-001` 完成 WAES loop-state、evidence-index、loop record 和 validator；本次累计 10 个实质轮次 |
| L3 二轮验证清单 | 已完成 | `GPCF-WA-LR-002` 至 `GPCF-MM-LR-002` 完成 5 个二轮专项验证清单；本次累计 15 个实质轮次 |
| PKC 真实项目仓最小 Loop harness | 已完成 | `PKC-LR-001` 在真实 PKC 项目仓落地 docs/harness、loop-state、evidence-index、round record 和 validator，并修复测试/typecheck 缺口；declared_rounds=1/15、substantive_rounds=1/15、generated_items=9、batch_generated=false |
| KDS 真实项目仓最小 Loop harness | 已完成 | `KDS-LR-001` 在真实 KDS 项目仓落地 docs/harness、loop-state、evidence-index、round record 和 validator；declared_rounds=1/15、substantive_rounds=1/15、generated_items=6、batch_generated=false |
| XGD 真实项目仓最小 Loop harness | 已完成 | `XGD-LR-001` 在真实 XGD 项目仓落地 docs/harness、loop-state、evidence-index、round record 和 validator；declared_rounds=1/15、substantive_rounds=1/15、generated_items=6、batch_generated=false |
| XGD L3 任务队列与自我进化门禁 | 已完成 | `XGD-LR-002` 在真实 XGD 项目仓落地 `.codex/tasks` 结构化队列、自我进化 checklist、LR-002 轮次记录、`harness:validate` 和 validator 覆盖；declared_rounds=1/15、substantive_rounds=1/15、generated_items=4、batch_generated=false |
| XiaoG L3 风险回滚与自我进化门禁 | 已完成 | `XiaoG-LR-002` 在真实 XiaoG 项目仓落地 `.codex/tasks` 结构化队列、risk rollback runbook、自我进化 checklist、LR-002 轮次记录和 operational-control validator；declared_rounds=1/15、substantive_rounds=1/15、generated_items=5、batch_generated=false |
| XiaoG GFIS/WAES trigger dry-run | 已完成 | `XiaoG-LR-003` 在真实 XiaoG 项目仓落地 `dry_run_xiaog_gfis_waes_triggers.py`，用本地 fixture 验证 GFIS suggestion payload 与 WAES ready_for_review gate request；declared_rounds=1/15、substantive_rounds=1/15、generated_items=6、batch_generated=false |
| XiaoG dashboard/voice usability smoke | 已完成 | `XiaoG-LR-004` 在真实 XiaoG 项目仓落地 `smoke_xiaog_dashboard_voice_usability.py`，验证 Web dashboard 路由、voice feature switches、mobile pages 与 README/Deployment_all 可用性线索；declared_rounds=1/15、substantive_rounds=1/15、generated_items=7、batch_generated=false |
| 全项目提交推送 | 已完成 | XGD `840b70f0`、XiaoG `a6494b33`、GPCF `3c578ec` 已推送；最终全项目 `git status --short --branch` clean/up-to-date |
| XiaoC 真实项目仓最小 Loop harness | 已完成 | `XiaoC-LR-001` 在真实 XiaoC 项目仓落地 docs/harness、loop-state、evidence-index、round record 和 validator；declared_rounds=1/15、substantive_rounds=1/15、generated_items=6、batch_generated=false |
| Brain 真实项目仓敏感文件门禁与最小 Loop harness | 部分完成 | `Brain-LR-001` 在真实 Brain 项目仓补齐 `.env` gitignore 门禁、docs/harness、loop-state、evidence-index、round record 和 validator；declared_rounds=1/15、substantive_rounds=1/15、generated_items=7、batch_generated=false、substance_gate=partial |
| Brain ESLint 9 flat config | 部分完成 | `Brain-LR-002` 在真实 Brain 项目仓补齐 `eslint.config.js`，使 `pnpm lint` 从配置缺失恢复为 0 errors / 16 warnings；declared_rounds=1/15、substantive_rounds=1/15、generated_items=6、batch_generated=false、substance_gate=partial |
| PVAOS D4 L3 harness bootstrap | 已完成 | `PVAOS-LR-001` 在真实 PVAOS D4 分支补齐 Manifest、docs/harness、loop-state、evidence-index、round record、任务元数据和 validator；已提交推送，当前评分 100/L3 Ready |
| WAES integration-release L3 harness bootstrap | 已完成 | `WAES-LR-001` 在真实 WAES integration-release 分支补齐 Manifest、docs/harness、loop-state、evidence-index、round record、任务元数据、validator 和 Vitest localStorage 测试环境；已提交推送，当前评分 100/L3 Ready |
| GPC main L3 harness bootstrap | 已完成 | `GPC-LR-001` 在真实 GPC main 分支补齐 Manifest 命名纠偏、docs/harness、loop-state、evidence-index、round record、任务元数据和 validator；已提交推送，当前评分 97/L3 Ready |
| XiaoC L4 任务拆解与模型路由 dry-run | 已完成 | `XiaoC-L4-009` 在真实 XiaoC 项目仓落地 TaskBreakdown、ModelRoute、AgentDispatchPlan、AgentResultAggregation fixture、KDS retrieval、validator、loop record；计为第 9 个 L4 实质轮次；95/100；未真实模型调用、未 XiaoG runtime、未 WAES API 写入、未升级 accepted/integrated |
| XGD L4 重分析与风险建议 dry-run | 已完成 | `XGD-L4-010` 在真实 XGD 项目仓落地 RiskAnalysis、BottleneckProjection、ReliabilityAssessment、RecommendationPacket fixture、KDS retrieval、validator、loop record；计为第 10 个 L4 实质轮次；95/100；未 live LLM、未桌面运行态、未 WAES API、未升级 accepted/integrated |
| XiaoG L4 只读查询与审计 mock | 已完成 | `XiaoG-L4-011` 在真实 XiaoG 项目仓落地 ReadOnlyQueryResult、PkcNotificationCandidate、WaesAuditWriteMock、ExecutionTrace fixture、KDS retrieval、validator、loop record；计为第 11 个 L4 实质轮次；95/100；未 live API、未设备 OTA、未 Docker、未生产写入、未升级 accepted/integrated |
| GPCF L4 项目群收口 | 已纠偏为修复态 | `GPCF-L4-012` 原 100/100 与 L4 closed 结论失效；`GPCF-L4-CORR-001` 记录 GFIS Demo 主体错位、SOP E2E failed 和 78/100 repair；未生产写入、未真实外部 API、未设备 OTA、未部署、未升级 accepted/integrated |

## 下一轮候选任务队列

| 优先级 | Round | 任务 | 自动化边界 |
|---|---|---|---|
| P1 | 后续授权 | 收集真实现场样本、UAT 签收、WAES/GPC/Finance 确认 | 需要人工输入或显式授权 |
| P1 | 后续授权 | 新 L3/L4 继续 GFIS、转真实样本/UAT/WAES/GPC/Finance 收集，或转 GPCF 自身治理轮次 | 需要用户重新授权 |
| P1 | 后续授权 | 各项目真实项目仓、运行态验证、GPC 一期蓝图、WAES 门禁语义、accepted/integrated 升级 | 需要人工确认或更高授权，L3 不自动改主结论 |
| P1 | WAES-LR-001 | 先解决 WAES 分支绑定，再落地真实 WAES harness、validator 和 evidence | 不生产写入、不部署、不越权裁决 |
| P1 | L5-preparation | 起草 L5 强授权包：客户/UAT 样本、live read API、WAES runtime endpoint、监控、回滚和验收指标 | 只起草授权包；不生产写入、不真实外部 API、不升级 accepted/integrated |
| P0 | GFIS-real-receipt-empty-directory-hold-register | 在 5 个正式真实回执接收目录仍无文件时，建立空状态 hold register / 责任方补证提醒门禁；不得伪造真实回执、责任方响应、签章完成件、客户确认函、采购订单/合同、KDS write receipt 或 WAES confirmation | 不生产写入、不真实外部 API、不 bench migrate、不 schema sync、不真实 KDS/WAES 写入、不升级 accepted/integrated；KDS context 和用户事实只能作为候选和采集方向 |
| P0 | GFIS-original-proof-collection-checklist | 将 `LiaoningYuanhangProofCollectionPackage` 的 4 项开放请求持续转成业务方可执行的原始凭证采集清单：样箱测试签收/反馈、江西委托生产单或完工记录、客户确认函、现代精工转量产批准或 WAES evidence ref | 需要真实业务输入或明确授权；未授权前不 bench migrate、不 schema sync、不生产写入、不真实外部 API、不部署、不升级 accepted/integrated |
| P0 | GFIS-runtime-real-pod-receipts | 补齐真实 POD 签收、WAES evidence confirmation 与 KDS backlink receipt，复测 `get_runtime_pod_gate` 是否从 blocked 收敛 | 需要真实业务输入或明确授权；未授权前不 bench migrate、不 schema sync、不生产写入、不真实外部 API、不部署、不升级 accepted/integrated |
| P0 | GFIS-runtime-gap-resolution-plan | 按 `get_runtime_sop_gap_resolution_plan` 输出的 `gfis_runtime_actionable_count=7` 优先选择 GFIS 可行动缺口，继续补最小运行层能力并复测 | 不生产写入、不真实外部 API、不 bench migrate、不 schema sync、不升级 accepted/integrated |
| P0 | GFIS-runtime-real-production-execution | 补齐真实作业卡、投料、开始/完工、过程记录和 WAES execution evidence，复测 `get_runtime_production_execution_gate` 是否从 blocked 收敛 | 需要真实业务输入或明确授权；未授权前不 bench migrate、不 schema sync、不生产写入、不真实外部 API、不部署、不升级 accepted/integrated |
| P0 | GFIS-runtime-schema-and-real-input-repair | 在明确授权后执行候选 DocType schema sync / migrate，并补齐 KDS 葛化真实业务输入；继续复测 sample candidate、runtime evidence candidate 与 runtime handoff candidate API，补齐样品、ProductionExecution、QualityInspection、InventoryBatch、DeliveryNote、POD、WAES/KDS 回执的本机受控运行层 runner 或真实 UAT evidence | 保护 GFIS dirty 工作区；未授权前不 bench migrate、不 schema sync、不生产写入、不真实外部 API、不部署、不升级 accepted/integrated |
| P0 | GFIS-customer-requirement-platform-order-source-record-submission | 从 `GPC_or_Liaoning_Yuanhang_order_owner` 取得真实客户订单原件或平台订单回执 JSON，并提交到 GFIS 指定 source-of-record 接收目录；不得把请求包、报价单、合同审阅稿、KDS 候选、用户口述、Loop 文档、GFIS Demo 或未核验 accepted/integrated 声明转成运行层主键、review queue 或有效 source-of-record | 不生产写入、不真实外部 API、不 bench migrate、不 schema sync、不真实 KDS/WAES 写入、不升级 accepted/integrated；真实源记录提交前只允许请求包和校验门禁 |
| P0 | GFIS-pending-business-verification-manual-completion-release-ready-schema | 建立人工核验完成 release-ready schema；定义未来真实 completion release 文件的严格字段和 readiness 条件 | 不生产写入、不真实外部 API、不 bench migrate、不 schema sync、不真实 KDS/WAES 写入、不升级 accepted/integrated；schema 仅定义规则，不等于人工核验完成或 hold release |

## 最近 evidence 链接

| 类型 | 路径 |
|---|---|
| GFIS loop-state | `08-evidence-samples/GFIS/loop-state.md` |
| GFIS evidence-index | `08-evidence-samples/GFIS/evidence-index.md` |
| GPCF 状态矩阵 | `09-status/gpcf-project-status-matrix.md` |
| GPCF Loop 编排器 | `.codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py` |
| 本控制板 | `02-governance/loop/LOOP_CONTROL_BOARD.md` |
| L3.5 真实接口验证政策 | `02-governance/loop/LOOP_L3_5_REAL_API_VERIFICATION.md` |
| L4 全自动运营政策 | `02-governance/loop/LOOP_L4_AUTONOMOUS_OPERATIONS.md` |
| L5 完全生产自治政策 | `02-governance/loop/LOOP_L5_FULL_PRODUCTION_AUTONOMY.md` |
| GFIS runtime SOP E2E precheck | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/README.md` |
| GFIS runtime SOP E2E runner evidence | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dry-run-result.json` |
| GFIS runtime KDS Gehua input register | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/kds-gehu-data-input-register.md` |
| GFIS runtime SOP E2E failure analysis | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/e2e-failure-analysis.md` |
| Loop Engineering self-correction | `02-governance/loop/LOOP_ENGINEERING_SELF_CORRECTION.md` |
