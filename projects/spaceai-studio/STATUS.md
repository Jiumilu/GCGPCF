---
doc_id: GPCF-SpaceAIStudio-STATUS-20261010
title: SpaceAIStudio 状态
project: GPCF
related_projects: [SpaceAIStudio, GPCF]
domain: governance
status: controlled
version: v1.0
owner: 老卢
kds_space: 开发
kds_path: 开发/SpaceAIStudio/projects/spaceai-studio/STATUS.md
source_path: projects/spaceai-studio/STATUS.md
sync_direction: local_only
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
- project_status: registered；overall_status: partial。
- authorization：2026-10-10 用户授权纳管与 Git 建立，确认敏感文件仅保留本地。
- confirmation：业务验收与生产发布尚未确认。
- 验证边界：工程 XML 可解析；缺 Windows/.NET Framework 构建与设备运行证据；远端有意排除7个敏感文件，不能独立构建。
- 证据：`../GlobalCloud SpaceAI Studio/docs/harness/onboarding-2026-10-10.md`。
- 下一步：执行重构变更 `spaceai-studio-multiplatform-refactor` 的 P0（素材与协议固证，不改业务代码）。

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
- 方案文档：`../GlobalCloud SpaceAI Studio/docs/architecture/multiplatform-refactor-plan.md`；KDS `开发/14-SpaceAIStudio/`。
- 素材来源：非设备类接入组件均为我方资产——`RestFUL`（后端）/`Unisec.Contracts`/`Unisec.Common`/`Utility`/`UNISEC_UserControls` 在姊妹项目 `GlobalCloud SpaceAI`（MB3000，1,313 cs）**有源码可复用**；`FlyUI`/`FlyUtil`/`SecSpeak` 无源码但可 **ilspycmd 逆向**（工具链已实测）；设备类为第三方，不逆向。仅功能模块 DLL（`Unisec_Video` 等 12 个）确实缺失，MB3000 单体实现可作业务参照。不宣称「功能等价迁移」。
