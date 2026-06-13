---
doc_id: GPCF-DOC-0DF6AA8647
title: Loop Control Board
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, MMC, GPCF]
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
| 当前 Loop 模式 | L3 托管冲刺模式 |
| 可升级模式 | L3 托管冲刺模式；L3.5/L4/L5 可执行但必须显式或强授权启动 |
| 当前主线项目 | GFIS |
| 当前轮次 | `GPCF-GF-LR-030` 已完成；下一轮候选 `GPCF-GF-LR-031` |
| 当前阶段 | 本地受控开发与文档治理 |
| 当前目标 | 建立签收证据接收后的审计准备规则 |
| 当前涉及项目 | GFIS、GPC、Finance、WAES、KDS、GPCF |
| 当前状态判定 | `partial` |
| KDS TOKEN | 本开发机阶段暂缓；不得声明真实 KDS API 双向同步完成 |
| L3 上限 | 最多 15 轮或 2 小时，以先到者为准 |
| L3 默认继续规则 | active 时未触发硬停止、用户停止、预算耗尽、时间耗尽或任务队列为空，必须继续下一轮 |
| L3 阶段性汇报 | 不是停止条件；只能作为 evidence 或进度说明 |
| L3 停止记录要求 | 必须记录停止类型、停止证据、已完成轮次、剩余轮次、已用时间和下一步 |
| L3.5 状态 | executable / requires explicit activation；最多 5 轮或 1 小时 |
| L4 状态 | executable / not activated；最多 30 轮或 4 小时 |
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
| 真实 KDS API 双向同步 | KDS TOKEN 暂缓 |
| 未授权真实外部 API 写入 | 必须人工确认；L3.5/L4/L5 只按专项政策与显式授权执行 |
| 生产配置修改或部署 | 必须人工确认 |
| `bench migrate` / schema sync / 运行态写 API | GFIS 当前仍未取得迁移授权 |
| 标记 `accepted` / `integrated` | 必须用户人工确认且满足状态门禁 |

## 最近门禁状态

| 门禁 | 最近结果 | 说明 |
|---|---|---|
| Git 门禁 | partial | 工作区 dirty；`git diff --check` 最近通过 |
| 文档污染检查 | pass | `check_document_pollution.py` 最近通过 |
| KDS 镜像冲突 | pass | `kds_conflict_guard.py` 最近通过 |
| Loop 运行门禁 | pass | `loop_operational_gates.py` 最近通过 |
| GFIS 质量门禁 | pass | `npm run quality:repo` 已纳入 LR-030 validator 并通过 |
| KDS TOKEN 检查 | blocked/deferred | 本开发机阶段暂缓 |

## 当前待确认项

| 项 | 状态 | 下一步 |
|---|---|---|
| 现场真实样本 | 未收到 | 建立样本回收跟踪台账 |
| UAT 签收 | 未收到 | 建立问题分级与签收跟踪模板 |
| GPC/Finance 边界确认 | 未收到 | 保持金融事实 L4 阻断 |
| WAES 门禁语义确认 | 未收到 | 保持 fixture/contract 层 |
| KDS TOKEN | 暂缓 | 不进入真实 API 同步 |
| L3.5/L4/L5 启动 | 未启动 | 已形成可执行方案，但除非出现明确启动口令或强授权口令，否则不得进入 |
| L3 连续推进偏差 | 已修正规则 | 阶段性收口汇报不得导致 L3 停止；未触发停止条件时继续下一轮 |

## 下一轮候选任务队列

| 优先级 | Round | 任务 | 自动化边界 |
|---|---|---|---|
| P1 | `GPCF-GF-LR-031` | 建立签收证据接收后的审计准备规则 | 可自动执行，不替代人工签收 |
| P1 | `GPCF-GF-LR-032` | 建立现场样本进入 evidence 前的审计队列 | 可自动执行，不接收伪造样本 |
| P2 | `GPCF-CF-LR-002` | 将 Loop 三件套纳入 GPCF 自身 loop record | 可自动执行，本地文档范围 |
| P2 | 后续 | 试点补齐 MMC/KDS/Brain/PKC 的 Manifest/loop-state/evidence-index | 可自动执行，项目仓写入前需确认边界 |

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
