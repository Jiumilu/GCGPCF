---
doc_id: GPCF-DOC-4F77004DF4
title: WAME 状态
project: WAME
related_projects: [WAME, XiaoG, XGD, MMC]
domain: governance
status: controlled
version: v1.1
owner: WAME
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/wame/STATUS.md
source_path: projects/wame/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: [WAES]
superseded_by: []
---

# WAME 状态

本文件只记录 WAME 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## 项目群总体架构 v1.1 承接（2026-10-18）

WAME 应承接资产/模型引擎主账、XAP 治理受理、授权发布及审计；World 线 A 只共建 E1 分期规划，不取得 WAME/人工裁决权。仓内总体方案传导状态为 `pending_branch_binding`：架构目标分支 `wame/architecture-contracts`，当前检出 `wame/world-asset-studio`，本轮未跨分支写入。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/wame-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project wame`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- 活跃 Feature：0（项目群侧无 Feature 载体；F-033 仅在 XiaoC 侧以 PoC 覆盖 WAME 受理）
- 当前阶段：lint / typecheck / check 已 green；引擎面 E1 未落（`not_implemented`）
- 阻塞：架构目标分支 `wame/architecture-contracts` 未检出；仓内承接状态 `pending_branch_binding`

## 已知证据

- `GlobalCloud WAME/docs/harness/evidence/wame-lint-runtime-fix-20261022.md`：lint 280 files / 0 findings、typecheck / check 全绿、runtime smoke 2/2；0 源码改动
- `GlobalCoud GPCF/docs/harness/evidence/wave1-review-pack-20261022.md`：Wave1 WAME review 结论 `review_ready_lint_pass_no_code_change`

## 到下一状态门的关键缺口

- 建立并检出 `wame/architecture-contracts` 分支，完成架构承接
- 引擎面 E1 最小集（资产主账 + 模型注册）落地
- XWAIL / AaaS 发布门禁预检

## 2026-10-22 承接 WAES 动作授权与执行服务

- 依据：2026-10-12 老卢裁定（原 WAES 并入 WAME、缩写停用）+ 2026-10-22 作废决策（D1=路径 B：不立项，仅标识符退役 + 资产归并）
- 承接内容：契约 v1.0.3、参考实现（57 py / 23,864 行）、141 契约安全测试（2026-10-22 复跑全绿）、23 目录 386 文件验收证据、部署与运维脚本
- 来源仓：`GlobalCloud WAES` 冻结于 `76ec565` / tag `waes-final-20261022`；证据包 `runtime/waes-decision/handover-evidence-20261022/`
- 下游：XiaoG main 已合入适配器（1426 行 / 21 文件，未推送，D2=keep-dormant）；XGD 仅只读镜像（D-005）；MMC 身份 I1–I5 待答
- **边界：承接治理身份与资产，不等于生产运行接管**；WAME 引擎 E1 未落，运行体以独立子服务 `wame-authz` 保留，不并入本仓前端
- 继承缺陷：P1 用例数口径不一致（docs/05 唯一编号 7 个 vs 自称 103/104 vs 实测 141）、P3 policy_signature 文档与实现不一致
- 过渡：90 天双签 owner（WAME 负责人 + 原 WAES 接口负责人），到期上收或降级冻结；审计保留（在线≥180d / 归档≥3y）责任转 WAME owner 待签认（D3）

## 本轮不做与非声明

- 不声明 accepted / integrated / production_ready / customer_accepted；
- 不声明引擎面已实现或正式发布；
- 不替代项目实施方案与 Feature 证据。

## 2026-10-23 刷新（长期目标 Round 21）

- F-035（三套侧栏归并）pass：`src/app/layout/GlobalCloudSidebar.tsx` 成为唯一导航侧栏（契约同源 `@globalcloud/app-shell`）；`src/app/components/Sidebar.tsx` 改为兼容 re-export；FunctionPanel 定性为内容面板不并入。
- 验证：tsc pass、vitest 39 files/189 pass、build pass（2026-10-22 记录）。
- 残留：`@globalcloud/app-shell` 未发布 npm（直接消费需发布/并入 workspace）；FunctionPanel 重构另立项；无视觉/E2E 证据。
- 不声明状态提升。

