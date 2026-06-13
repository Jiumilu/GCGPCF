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
| 可升级模式 | L4 repair active；L5 暂停，必须等 GFIS 运行层证据与 SOP E2E 修复后再评估 |
| 当前主线项目 | GPCF / WAES / 全项目 |
| 当前轮次 | `GPCF-L4-CORR-001`：GFIS 主体错位与 SOP E2E failed 自我纠错 |
| 当前阶段 | L4 repair；纠正此前 100/100 假阳性，建立自我发现和自我纠偏门禁 |
| 当前目标 | 在 GPCF 总控仓记录 GFIS Demo 错误主体、SOP E2E failed、L4 降级结论和 GFIS-runtime-repair 下一轮输入 |
| 当前涉及项目 | GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、GPCF |
| 当前状态判定 | `repair_required`；此前 `GPCF-L4-012` 的 `100/100` 与 `L4 closed` 结论已失效 |
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
| continuous declared_rounds | 12/30 |
| continuous substantive_rounds | 12/30 |
| continuous generated_items | 68 |
| continuous batch_generated | false |
| continuous substance_gate | pass |
| continuous substance_evidence | `GPCF-L4-001` 建立项目群控制面；`MMC-L4-002`、`KDS-L4-003`、`Brain-L4-004`、`PKC-L4-005`、`PVAOS-L4-006`、`GPC-L4-007`、`XiaoC-L4-009`、`XGD-L4-010`、`XiaoG-L4-011` 保持各自 L4 dry-run/mock/read-only evidence；`GFIS-L4-008` 被纠偏为 repair_required，因为其核心 fixture 来自 `gcfis_demo` 且 SOP E2E failed；`GPCF-L4-012` 原 100/100 被 `GPCF-L4-CORR-001` 降级为 78/100 L4 repair；当前不执行生产写入、真实外部 API、权限变更、部署、数据库迁移、设备 OTA 或 accepted/integrated 升级 |
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
| `bench migrate` / schema sync / 运行态写 API | GFIS 当前仍未取得迁移授权 |
| 标记 `accepted` / `integrated` | 必须用户人工确认且满足状态门禁 |

## 最近门禁状态

| 门禁 | 最近结果 | 说明 |
|---|---|---|
| Git 门禁 | pass | 提交推送后全项目状态 clean/up-to-date；本轮校准变更需再次通过 diff check 后提交 |
| 文档污染检查 | pass | `check_document_pollution.py` 最近通过 |
| KDS 镜像冲突 | pass | `kds_conflict_guard.py` 最近通过 |
| Loop 运行门禁 | pass | `loop_operational_gates.py` 最近通过 |
| GFIS 质量门禁 | blocked | GFIS `test-results/.last-run.json` 为 `status=failed`；SOP E2E 未通过前不得以 Demo 或局部 validator 代替运行层验收 |
| XiaoC L4 门禁 | pass | `node scripts/validate_xiaoc_l4_agent_orchestration.mjs`、`node scripts/validate_xiaoc_loop_harness.mjs`、`pnpm test:repo`、`git diff --check -- .` 均通过 |
| XGD L4 门禁 | pass | `node scripts/validate_xgd_l4_risk_analysis.mjs`、`npm run harness:validate`、`npm test`、`git diff --check -- .` 均通过 |
| XiaoG L4 门禁 | pass | `python3 scripts/validate_xiaog_l4_readonly_audit_mock.py`、legacy L3 validators/smoke/test、`git diff --check -- .` 均通过 |
| GPCF L4 收口门禁 | repair_required | `validate_loop_self_correction_gate.py` 与 `validate_l4_minimum_closed_loop.py` 必须输出 78/100 repair，直到 GFIS 运行层证据和 SOP E2E 修复 |
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
| P0 | GFIS-runtime-repair | 以 GFIS 运行层替换 Demo 主体证据，修复 SOP E2E，补齐运行态 DocType/工作流/API/evidence validator | 保护 GFIS dirty 工作区；不生产写入、不 bench migrate、不部署、不升级 accepted/integrated |

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
