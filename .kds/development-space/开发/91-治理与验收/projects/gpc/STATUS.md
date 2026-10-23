---
doc_id: GPCF-DOC-B35947A669
title: GPC 状态
project: GPC
related_projects: [GPC]
domain: governance
status: controlled
version: v1.1
owner: GPC
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gpc/STATUS.md
source_path: projects/gpc/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GPC 状态

本文件只记录 GPC 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/gpc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project gpc`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- 活跃 Feature：0（GPCF 侧无 Feature 载体）。
- 当前阶段：模板桩（判定见 `runtime/plan-20261022/project-state.md`）；仓 README 记 2026-10-17 定位变更为「流规则包消费执行点」，流引擎统一归 `GlobalCloud SOP` 仓（文档声明，非验收）。
- 阻塞：
  - 无项目级状态登记与活跃 Feature 载体；GPCF 侧仅有核心链路证据台账 1 行。
  - 2026-10-17 定位变更后，尚未建立对应「流规则包消费执行点」的 Feature 验收。
  - 外部 runtime 证据缺：`quality:100` 因生产确认/外部联调失败；`quality:ops` 因 GCFIS desk/runtime language asset 不可达失败（2026-06-25 台账口径）。

## 已知证据

路径相对 `GlobalCoud GPCF` 仓根；标注 `GlobalCloud GPC/...` 的为跨仓路径。

- `09-status/globalcloud-core-chain-real-evidence-register.md`（GPC 行，第 112、126 行）：GPC 结论 `partial_verified / external_runtime_evidence_required`；`quality:repo`、`test:e2e` 已通过；真实集成与客户验收均为 `not_collected`。
- `docs/harness/GPC/evidence/gpc-evidence-browser-repair-20260625.md`：README 索引与 Playwright 浏览器 E2E 修复证据。
- `docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md`：首轮本地运行基线；当轮 `quality:repo` fail（README 缺索引），`validate_gpc_l3_harness.py`、`validate_gpc_l4_platform_contract.py` pass。
- `GlobalCloud GPC/README.md`：2026-10-17 定位变更声明（文档声明）。
- `GlobalCloud GPC/tests/e2e/gcfis-core-flow.spec.js`：Playwright E2E 用例文件（存在性证据，非本轮 pass 结果）。
- `GlobalCloud GPC/playwright-report/`：E2E 报告目录（本轮未复核内容）。

## 到下一状态门的关键缺口

- 按 2026-10-17 新定位建立首个活跃 Feature 与专属验收命令（当前 0 active）。
- 补外部 runtime 证据：GCFIS desk/runtime 可达性、生产确认与外部联调，解除 `quality:100`、`quality:ops` 失败。
- 在 GPCF 侧补项目级状态登记与真实集成/客户验收采集方案（当前 `not_collected`）。
- 归因 GPC 仓 dirty 1 条并纳入 Git 基线（`runtime/plan-20261022/constraints.md` §c-1）。

## 本轮不做与非声明

- 本文件不声明 accepted / integrated / production_ready / customer_accepted；
- 本文件不替代项目实施方案与 Feature 证据；
- 真实业务验证/客户验收未发生。
