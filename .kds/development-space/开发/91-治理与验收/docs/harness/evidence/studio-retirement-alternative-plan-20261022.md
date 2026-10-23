---
doc_id: GPCF-DOC-STUDIO-RETIREMENT-ALTERNATIVE-20261022
title: Studio 作废替代方案（2026-10-22）
project: GPCF
related_projects: [Studio, WAE, World, Project, GPCF, Hermes, PKC, Brain, PVAOS]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/studio-retirement-alternative-plan-20261022.md
source_path: docs/harness/evidence/studio-retirement-alternative-plan-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# Studio 作废替代方案（2026-10-22）

> 决策依据：老卢 2026-10-22「Studio 项目准备作废，要有替代方案」。
> 性质：替代方案草案，不删除任何项目、仓库或证据；不改任何项目状态；不 commit/push。

## 1. 为什么现在作废

- Studio HEAD `b02d837e` 存在运行时回归：删除 `gcworld.*` 路由但 `AppSidebar.vue:626` 仍引用，登录后整页空白；既有 E2E 2 failed。
- GCWorld 组织世界已于 2026-10-17 迁至独立项目 **World**，Studio 的差异化职责已减少。
- WAE 已立项为「项目群统一界面框架与统一入口」；Studio 继续维护会与 WAE 重复。
- 结论：**不再修 Studio 回归，冻结并迁出其剩余职责**。

## 2. Studio 现有职责与替代映射

| Studio 职责 | 替代方案 | 现状 |
|---|---|---|
| 统一工作台 UI / 工作台壳层 | **WAE**（主入口） | WAE 设计阶段，P0 四项未完成；需先落 M0 方案 |
| Agent 对话 / 技能 / 运行时入口 | **Hermes Web UI**（8648）+ WAE 内嵌 | 本机 8648 可启动（已验证 200）；对外 502 未恢复 |
| 项目 / 任务协作 | **PMC（Plane）** | 生产实例只读可达；本地实例不可用 |
| 治理 / 发布控制台 | **GPCF Console（F-018）** + WAE 治理视图 | F-018 已关闭，可承接只读治理视图 |
| GCWorld 组织世界 | **World** | 已于 2026-10-17 迁出 |
| Release workflows（5 个） | 迁 **GPCF** 或冻结 | 未迁移，需单独任务 |
| UI E2E / 截图证据 | **WAE**（F-010 新证据目标） | WAE a11y / evidence-overexposure 已 pass |

## 3. F-010 影响

- F-010 四项 UI gate：`accessibility_status=pass`、`evidence_overexposure_gate=pass`（WAE 登录首屏已实测）。
- `task_flow_e2e_status` 当前 fail 因 Studio 空白页；**替代后改用 WAE 登录→工作台→退出流程作为 E2E 目标**，不再依赖 Studio。
- `multi_user_usability` 仍需两个测试角色；WAE 若支持角色切换，可用本地 IdP；否则保持 pending。
- F-011 已关闭（2026-10-22），保留历史证据，不重开、不新增 Studio UI 工作。

## 4. 作废步骤（不删除）

1. **冻结**：Studio 不再接受新功能与回归修复；现有未提交改动保留原状，不清理。
2. **状态**：`projects/studio/STATUS.md` 标注 `deprecated`（建议），并写明替代入口与保留证据范围。
3. **职责迁移**：按 §2 表逐项迁出；F-015（gcworld 组织纵切，blocked）转 World 或登记历史例外。
4. **范围**：Studio 暂保留在 28 项目范围内但标记 deprecated；是否移出范围、是否把项目数改为 27，需老卢单独确认。
5. **证据**：全部历史证据保留；不删除仓库、不删测试、不改写历史闭环。

## 5. 风险

| 风险 | 处理 |
|---|---|
| WAE 尚未完成，短期无统一工作台 | 过渡期以 Hermes Web UI + PMC + GPCF Console 分担 |
| Studio release workflows 仍在 | 冻结前不触发；迁移需单独授权 |
| F-015 归属悬空 | 转 World 或历史例外，不自动关闭 |
| 证据引用指向 Studio | F-010 等只引用历史证据，不新增依赖 |

## 6. 已确认（2026-10-22）

1. **Studio 状态：`deprecated` 冻结**；保留在 28 项目范围内，不删除仓库/证据，暂不移出范围。
2. **替代主入口：WAE + Hermes + PMC**（WAE 管界面壳层、Hermes 管 Agent 对话、PMC 管项目协作；GPCF Console 承接治理视图）。
3. **F-015**：待裁定转 World 或登记历史例外，本轮不处置。
4. **F-010**：`task_flow_e2e_status` 改以 WAE 登录→工作台→退出流程为目标，不再依赖 Studio；`multi_user_usability` 待本地 IdP 账号授权。

## 7. 非声明

- 不声明 Studio 已删除或已归档（未执行）；
- 不声明 WAE 已承接 Studio 或已成为统一入口；
- 不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 不声明 F-010 四项 gate 已完成（task_flow 仍 fail、multi_user 仍 pending）。
