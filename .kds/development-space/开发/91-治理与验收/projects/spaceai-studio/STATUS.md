---
doc_id: GPCF-SpaceAIStudio-STATUS-20261010
title: SpaceAI Studio 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/spaceai-studio/STATUS.md
source_path: projects/spaceai-studio/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-10
supersedes: []
superseded_by: []
---

# SpaceAI Studio 状态

- 路径：`../GlobalCloud SpaceAI Studio`。
- 私有仓库目标：`https://github.com/Jiumilu/GCSpaceAIStudio`，main。
- 身份：独立客户端项目，external；2026-10-10 起**重定位为 GlobalCloud 空间智能工作台**（与 GlobalCloud Studio 平行，承担空间感知/设备/事件/可视化）；不等同于 Studio 或 SpaceAI，不合并。
- 由来：原为遗留 Windows 安防监控客户端（`UNISECManage` / UNISEC 平台，.NET Framework 4.5 WinForms），2026-10-10 纳入项目群。
- 工程角色（2026-10-10 定稿）：**宿主壳**（`OutputType=WinExe`，定义插件契约 `UnisecFunction.AbstractMng`）；姊妹项目 `SpaceAI` 的 `MB3000` 为**被加载模块库**（`OutputType=Library`，`MB3000/AbstractTDMng : AbstractMng`）。装配契约 = 本项目 `UnisecFunction/AbstractMng` + 5 接口。
- project_status: registered；overall_status: **partial**（P0–P5 已交付；等待人工验收与三平台产物）。
- authorization：2026-10-10 用户授权纳管与 Git 建立，确认敏感文件仅保留本地；同日授权提交并推送到私有远端。
- confirmation：业务验收与生产发布**尚未确认**；OpenSpec 归档**未执行**（前置条件未满足，见「归档前置条件核对」）。
- 验证边界：**TS 51 + Rust 5 测试全通过**；macOS 安装包已产出并校验自包含。缺口：Windows/Linux 产物（CI 进行中）与**实际运行启动证据**；远端有意排除 7 个敏感文件，不能独立构建。
- 证据：`../GlobalCloud SpaceAI Studio/docs/harness/onboarding-2026-10-10.md`；Harness run `.harness/runs/20261010-075917-spaceai-studio-multiplatform-refactor/`。
- 下一步：P6 桥接扩展（前端接入 Tauri 命令 / 旧 DLL 兼容桥 / 移动适配）——**按需**推进。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/spaceai-studio-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project spaceai-studio`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 重构路线

- 变更：`openspec/changes/spaceai-studio-multiplatform-refactor/`（2026-10-10 建立，status: draft）
- 目标：重定位为空间智能工作台；技术路线 Vue 3 + Naive UI + Tauri 2，目标端 Windows/macOS/Linux 桌面。
- 分期：P0 协议与素材固证 → P1 契约与领域层 → P2 通讯层 → P3 壳与插件宿主 → P4 首模块试点 → P5 三平台打包 → P6 桥接扩展。
- 方案文档：`../GlobalCloud SpaceAI Studio/docs/architecture/multiplatform-refactor-plan.md`；KDS `开发/15-SpaceAIStudio/`。
- 素材来源：非设备类接入组件均为我方资产——`RestFUL`（客户端 SDK，非后端）/`Unisec.Contracts`/`Unisec.Common`/`Utility`/`UNISEC_UserControls` 在姊妹项目 `GlobalCloud SpaceAI`（MB3000，1,313 cs）**有源码可复用**；`FlyUI`/`FlyUtil`/`SecSpeak` 无源码但可 **ilspycmd 逆向**（工具链已实测）；设备类为第三方，不逆向。仅功能模块 DLL（`Unisec_Video` 等 12 个）确实缺失，MB3000 单体实现可作业务参照。不宣称「功能等价迁移」。

## P0–P5 执行结果（2026-10-10）

| 期 | 交付 | 证据 |
| --- | --- | --- |
| P0 | 6 份规格（REST 20 端点 / Socket / 领域 / 契约 / 依赖处置 / 迁移面 245→A66·B149·C30） | `docs/specs/P0-0*.md` |
| P1 | `packages/domain` + `packages/plugin-sdk`（14 测试） | `docs/specs/P1-01-contract-domain-layer.md` |
| P2 | `packages/protocol` + mock 契约测试（19 测试） | `docs/specs/P2-01-transport-layer.md` |
| P3 | `packages/host` + `apps/desktop`（Vue 3 + Tauri 2）+ `apps/server`（Koa BFF）（10 测试） | `docs/specs/P3-01-shell-plugin-host.md` |
| P4 | `plugins/patrol` 端到端试点（8 测试） | `docs/specs/P4-01-patrol-pilot.md` |
| P5 | Rust 平台抽象（5 测试）+ 三平台 CI + macOS `.app` 8.17 MiB | `docs/specs/P5-01-platform-and-packaging.md` |

- 任务进度：**29/37**（`tasks.md`）；`openspec validate --strict` 通过；文档门禁 pass（missing_metadata=0）。
- 遗留 C# 业务源码本轮**零修改**。
- 凭据安全：7 个含口令/连接串的文件在 `.gitignore` 排除列表内，**未跟踪、未入库、未进历史**。
- 关键警示：**`MB3000/Func/FrmPatrolControl.cs` 是无人机（UAV）巡更控制**（`pbxFollow`/`pbxShowLine`/`pbxReturn`），与 Studio 的「巡更点/违规记录」**语义不同**——后续模块不得当作等价参照。

## 归档前置条件核对（8.3）

`openspec archive` **暂不执行**：

1. **任务未全部完成**（29/37；P6 与收口未闭合）→ 不满足归档的完整性前提；
2. `.harness/config.yaml` 要求 `archive.require_acceptance_first: true` 与 `require_confirmation: true` → 需**人工验收 + 人工确认**；
3. **运行态证据缺失**（未实际启动 GUI；三平台产物待 CI 落地）。

→ 维持 `partial`；待 P6 决策、CI 产物落地与人工验收后再议归档。
