---
doc_id: GPCF-DOC-FEC2988B71
title: AAAS 状态
project: AAAS
related_projects: [AAAS]
domain: governance
status: controlled
version: v1.1
owner: AAAS
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/aaas/STATUS.md
source_path: projects/aaas/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# AAAS 状态

本文件只记录 AAAS 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/aaas-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project aaas`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- 活跃 Feature：0（项目群侧无 Feature 载体；`F-020-aaas-service-console` 已关闭，`status: done`，位于 `features/done/`）。
- 当前阶段：模板桩（判定见 `runtime/plan-20261022/project-state.md`；仓内无 README）。
- 阻塞：
  - GPCF 侧无活跃 Feature 与项目级验收登记，功能级证据只落在已关闭的 F-020。
  - WAME 绑定仅有本地前置预检：`aaas_wame_binding_precheck = controlled`，WAME 侧状态 `Draft`、结论 `candidate_only_not_published`。
  - AAAS 仓工作树 dirty 16 条、ahead 1（`runtime/plan-20261022/constraints.md` §c-1，2026-10-22 实测）。

## 已知证据

路径相对 `GlobalCoud GPCF` 仓根；标注 `GlobalCloud AAAS/...` 的为跨仓路径。

- `docs/harness/AaaS/evidence/aaas-wame-binding-precheck-20260625.md`：AaaS-WAME 绑定前置预检；四项本地校验器 pass，WAME 为 Draft/未发布，`accepted/integrated/production_ready/customer_accepted` 均为 false。
- `docs/harness/AaaS/evidence/aaas-service-runtime-20260625.md`：最小 ServicePackage/Metering/SLA/EvidenceRequirement 本地运行证据；仅本地、Draft 边界。
- `docs/harness/AaaS/evidence/aaas-real-runtime-baseline-20260624.md`：首轮运行基线采集；当时判定为文档型仓库，四个验证脚本均不存在。
- `features/done/F-020-aaas-service-console/feature.yaml`：已关闭；evidence `tests/build/screenshots/summary=pass`、`api=waived`（一期只读导出物模式）。
- `GlobalCloud AAAS/research/aaas-business-evidence.md`、`GlobalCloud AAAS/research/benchmark-fde-platform-ops.md`：业务事实底稿与对标分析（2026-10-21 提取，明示不构成商业结论）。
- `GlobalCloud AAAS/review/fde-plan-review.md`、`GlobalCloud AAAS/review/red-team-report.md`、`GlobalCloud AAAS/review/red-team-addendum.md`：评审类文档（文档态，非运行证据）。
- `GlobalCloud AAAS/docs/` 下 6 份业务专项方案：`GlobalCloud AaaS 总体方案.md`、`GlobalCloud AaaS 实施方案.md`、`GlobalCloud AaaS FDE 业务专项方案_v1.0.md`、`AaaS总体方案_GPCF对齐版.md`、`GlobalCloud AaaS DoDAF架构规划_v0.1.md`、`GlobalCloud AaaS 平台+运营+FDE 业务模式分析_v1.1.md`（均为文档态）。

## 到下一状态门的关键缺口

- 建立项目级 README 与首个活跃 Feature 载体，并在其中声明专属 tests/build 命令（当前 0 active）。
- 将 `aaas-wame-binding-precheck` 推进到 WAME 正式注册/授权审查（依赖 WAME 侧裁定，非 AAAS 单方可控）。
- 补项目级验收登记与运行证据：现有运行证据均为 local dev / 本地脚本边界，无外部联调、无客户验收。
- 归因并清理 AAAS 仓 dirty 16 条，登记 Git 基线。

## 本轮不做与非声明

- 本文件不声明 accepted / integrated / production_ready / customer_accepted；
- 本文件不替代项目实施方案与 Feature 证据；
- 真实业务验证/客户验收未发生。
