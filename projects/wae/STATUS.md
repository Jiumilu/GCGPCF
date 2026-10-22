---
doc_id: GPCF-DOC-420E49DB6F
title: WAE 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/wae/STATUS.md
source_path: projects/wae/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# WAE 状态

本文件只记录 WAE（世界资产浏览器）在 GPCF 2.0 下的项目级状态与阶段，不放过程说明。

## 基线

| 项 | 内容 |
|---|---|
| project_id | `WAS-WAE-BROWSER` |
| 立项日期 | 2026-10-12（老卢裁定） |
| 归属 | GlobalCloud 项目群 / 世界资产空间 |
| 定位 | GlobalCloud 项目群统一界面框架与统一入口；先独立运行，再逐项目纳入 |
| 基础 | WAME 主框架（外壳 / 骨架 / 组件 / 令牌 / 模块注册） |
| 项目级状态 | `active` / 设计阶段 |
| 总体设计 | `projects/wae/MASTER-DESIGN.md`（v0.1，controlled） |

## 当前阶段

- [x] 现状勘察（项目群界面载体全景 + WAME 主框架解剖）
- [x] 总体设计 v0.1 落盘并转受控
- [x] 立项登记（KDS registry + GPCF 项目群总体方案）
- [x] 技术形态已裁定：分步路线 C（共享包 → 统一入口+iframe → 按需微前端）
- [x] 命名已裁定：WAE=世界资产浏览器；原 WAE 引擎与原 WAES 合并为 WAME（WAES 缩写停用）
- [ ] P0：外壳解耦 / 令牌收口 / 侧栏统一 / 状态语义层
- [ ] 首批纳入（PKC / Brain / PVAOS）

## 非声明边界

本项目当前不得声明任一项目 `accepted` / `integrated` / `production_ready`；不得声明任一项目界面已纳入。门禁继承 GPCF《界面工程整体实施方案》。

## 项目群总体架构 v1.1 承接（2026-10-18）

WAE 只统一界面外壳、令牌、应用注册与入口导航，按“装配登记→统一导航→主流程迁移”渐进接入；不取得 WAME 治理、World 运行或业务主账。仓内唯一项目总体方案尚未确认，传导状态 `pending_unique_plan`；`MASTER-DESIGN_v0.3` 是设计输入，不等于项目群集成验收。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/wae-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project wae`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- 活跃 Feature：0（`features/active/` 无 `project: wae` 登记；项目群侧无 Feature 载体）。
- 当前阶段：设计阶段；唯一项目总体方案仍为 `candidate` / `pending_unique_plan`（`09-status/globalcloud-project-master-plan-control-register.md:85,116`）；实施台账交付状态 `planned`、边界 `ui_runtime_boundary`（`09-status/globalcloud-project-implementation-control-register.md:84,106`）。
- 阻塞：
  - 唯一总体方案未确认：WAE 仓根无 `GlobalCloud WAE 总体方案.md`/`实施方案.md`；`MASTER-DESIGN_v0.3` 为设计输入，不等同方案权威。
  - 无 Feature 载体与可回放 Evidence Gate，P0 无法按 GPCF 2.0 收口（0 active）。
  - P0 未收口：O1/O2/O4 在 WAE 仓有实现与自测记录（文档声明，未按 Feature 门禁复跑）；O3 仅框架侧完成，项目侧三套侧栏未归并；首批 PKC/Brain/PVAOS 未纳入。

## 已知证据

路径相对 `GlobalCoud GPCF` 仓根；`../GlobalCloud WAE/...` 为 WAE 仓路径。

- `projects/wae/MASTER-DESIGN.md`（v0.1）、`projects/wae/MASTER-DESIGN_v0.2.md`、`projects/wae/MASTER-DESIGN_v0.3.md`：设计迭代与 P0 四项（O1–O4）来源；`O3` 现状等见 v0.1 §四。
- `../GlobalCloud WAE/README.md`、`../GlobalCloud WAE/BASELINE.md`：母本直出基线、包结构（`ui-tokens`/`ui-kit`/`app-shell`/`app-registry`）、运行与门禁命令（`pnpm dev`/`typecheck`/`test`/`gate`）。
- `../GlobalCloud WAE/CONVERGENCE.md`：22 件组件收敛（20 件规范化后逐字节相同、2 件仅引号风格差异、0 件实现实质不同）。
- `../GlobalCloud WAE/VERIFICATION.md`：V6 令牌收口（76 令牌单源、4 份复制件逐字节相同；PKC 4 处、Brain 30 处+5 独有令牌偏离未裁定）、V7 外壳能力开关（默认全关）、V8 状态语义层（7 值字典，S1/S2 代码级）、V10 母本整块直出、V16 装配三阶段；「未执行」节明示项目侧侧栏归并与首批纳入未做。均为仓内自述（B 级），本轮未复跑。
- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`：上位总控，关键门禁 G1/G4/G5/G8/G9 与 Phase 0–3（Phase 1 以 WAME 为母框架；Phase 2 扩散序 `Studio → PKC → XGD → GPC → GFIS`）。
- `features/active/F-010-project-group-ui-engineering-coverage/feature.yaml`：项目群 UI 工程覆盖 Feature 载体（active；acceptance/scope.in 为空、Evidence Gate 不可关闭、UI gates 多为 pending）。
- `features/done/F-011-studio-workbench-ui-runtime-closure/evidence/verification-2026-10-22.txt`：单页 UI 证据收口样例（tests/build/UI/gate 写法），可作格式参考，不等同 WAE 纳入。
- `docs/harness/evidence/pj24-wae-p0-plan-20261022.md`：本轮 P0 实施计划（O1–O4 scope/依赖/验收/风险/回滚、首批接入顺序与门禁）。

## 到下一状态门的关键缺口

1. 确认唯一项目总体方案：在 WAE 仓建立 `GlobalCloud WAE 总体方案.md` + `实施方案.md`，核验继承链，并更新 master-plan 台账（解除 `pending_unique_plan`，需人工确认）。
2. 建立首个 WAE Feature 载体并声明专属 tests/build 命令（当前 0 active），使 P0 有可回放 Evidence Gate。
3. P0 收口：O1/O2/O4 复跑并入 Feature evidence；O3 项目侧三套侧栏归并（WAME 先行，需目标项目授权）。
4. 首批纳入 PKC/Brain/PVAOS：先立接入协议与检查表，按 `PKC → Brain → PVAOS` 批次判据通过 G1/G4/G5/G8/G9；PVAOS 需先绑定 `pvaos/architecture-contracts` 分支。
5. 未决偏离裁定：PKC 令牌 4 处值偏离、Brain 独立深色主题（30 处 + 5 独有令牌）。

## 本轮不做与非声明

- 本文件不声明 accepted / integrated / production_ready / customer_accepted；
- 不声明唯一总体方案已存在、P0 已完成、任一项目界面已纳入、WAE 达到 `项目群基线态`；
- 本文件不替代项目总体方案/实施方案与 Feature 证据；
- 本轮未改 WAE 代码、未启动前端、未运行测试/门禁、未 commit/push；真实业务验证/客户验收未发生。

## 2026-10-23 刷新（长期目标 Round 21）

- 唯一方案已落仓：`../GlobalCloud WAE/docs/GlobalCloud WAE 总体方案.md` 与 `实施方案.md`（controlled v1.0）；master-plan register 已由 candidate→authoritative，`pending_unique_plan` 已移除 WAE。
- F-034（WAE P0 + AppsShell 角色收敛）已关闭；AppsShell requires 修复 + main landmark/TopTabs aria 已提交（WAE 557db8e / ef7b36f）。
- F-036（PKC 接入 WAE）当前 **conditional**：六门 pass；PKC P4/P5 已最小接入（C6 `--gc-*` 0→117、C5 存在）；真实受控嵌入/其他页面/正式评审未完成。
- F-035（WAME 侧栏归并）pass：GlobalCloudSidebar 唯一导航侧栏，Sidebar 兼容别名。
- 仍不声明：WAE 已承接 Studio、任一项目界面已纳入、P0 完成、`accepted/integrated/production_ready`。

