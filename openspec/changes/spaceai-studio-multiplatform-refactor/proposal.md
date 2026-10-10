---
doc_id: GPCF-OS-SPACEAI-STUDIO-MULTIPLATFORM-REFACTOR-PROPOSAL-20261010
title: proposal
project: SpaceAIStudio
related_projects: [SpaceAIStudio, SpaceAI, Studio, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: 老卢
kds_space: 开发
kds_path: 开发/14-SpaceAIStudio/openspec/changes/spaceai-studio-multiplatform-refactor/proposal.md
source_path: openspec/changes/spaceai-studio-multiplatform-refactor/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-10-10
supersedes: []
superseded_by: []
---

## Why

GlobalCloud SpaceAI Studio（`UNISECManage` 遗留安防监控客户端）于 2026-10-10 纳入项目群，治理角色 `external`、状态 `partial`。经全量勘察确认三项事实，决定了「不做代码移植、只做平台重建」，并澄清了素材的实际分布：

1. **素材分散（2026-10-10 修正）**：本项目自身仅有主框架（`UNISECManage`）与契约库（`UnisecFunction`）；其余依赖**并未丢失，而是分散在同日的姊妹项目 `GlobalCloud SpaceAI`（`MB3000.sln`，1,313 个 .cs）中**。按用户口径，**非设备类接入组件均为我方资产**：`Unisec.Contracts` / `Unisec.Common` / `Utility` / `UNISEC_UserControls` / `RestFUL`（后端 REST 服务）**有源码，可源码级复用**；`FlyUI` / `FlyUtil` / `SecSpeak` **无源码，但可用已安装的 `ilspycmd` 逆向恢复**；设备类（视频播放/厂商 SDK）为第三方，**不逆向**。**仅功能模块 DLL**（`Unisec_Video` / `Unisec_Alarm` / `UNISEC_TalkBack` / `UNISEC_DPControl_DH` / `Unisec_Bayonet` / `Unisec_Operation` / `Unisec_Patrol` / `Unisec_DoorAccess` / `UniSec_Map2D` / `UNISEC_SysConfigManagement` / `Unisec_AlarmWindow` / `Unisec_HomePage`）确实在 Projects + Desktop 范围内无源码、无 DLL，但 MB3000 模块库（1,313 cs）与 MB2000 逆向产物（147,059 行）可作业务逻辑参照。

**宿主/模块关系（v1.3 工程证据定稿）**：本项目（`UNISECManage`）`OutputType=WinExe` 且定义插件契约 `UnisecFunction.AbstractMng`，是**宿主壳**；姊妹项目 `GlobalCloud SpaceAI` 的 `MB3000.csproj` 为 `OutputType=Library`，其 `MB3000/AbstractTDMng : AbstractMng`（`using UnisecFunction;`）证明它是**被宿主加载的业务模块库**。两者是「宿主 + 模块」装配关系，治理身份仍各自独立登记、不合并。
2. **深 Windows 耦合**：WinForms 142 文件、WPF 引用、DevExpress v18.1（商业控件、仅 Windows）、Win32 P/Invoke 22 文件、注册表/WMI 7 文件、`DataSet`/`DataTable`/XML 数据交换 23 文件。
3. **体系技术栈不一致**：GlobalCloud 体系现有技术栈为 Web/Python 系（Studio = Vue 3 + Naive UI + Koa 2 + Socket.IO + SQLite；PQC = FastAPI + Next.js；GPC = ERPNext；KDS = Markdown + Python），无 .NET 技术栈。

同时，项目名称与体系定位指向的并非「复原旧安防客户端」，而是与 GlobalCloud Studio 平行的一条业务线。

## What Changes

- **重定位**：把本项目从「遗留安防监控客户端」重定位为 **GlobalCloud SpaceAI Studio — 空间智能工作台**，与 GlobalCloud Studio（知识层 × AI 能力层 × 供应链层）平行，承担**空间层**（空间感知、空间设备、空间事件、空间可视化）。身份、slug（`spaceai-studio`）与 `external` 角色不变，不并入 Studio 或 SpaceAI。
- **技术路线**：采用 **Web 优先**——Vue 3 + Naive UI（对齐 Studio）+ **Tauri 2 桌面壳** + Node/Koa BFF + Socket.IO；目标端为 **Windows / macOS / Linux 桌面**（单一前端代码库，经 Tauri 打包三平台）。
- **资产处置**：把遗留资产按「可迁移/需重写/不可用」三类处置——领域模型（`Model/` 16 类）转 TypeScript 类型；REST/Socket 协议面固证为 `protocol` 包；插件契约（`AbstractMng` + 5 接口）重设计为平台无关的 `plugin-sdk`；窗体 UI（17,189 行）与自定义控件（7,363 行）作交互需求输入后重写。
- **素材获取**：非设备类依赖优先**源码级复用**（`SpaceAI`/MB3000 项目），无源码者用已装 `ilspycmd` **逆向恢复**；设备类不逆向，按新定位重新设计接口。工具链已实测（`DOTNET_ROOT=/opt/homebrew/opt/dotnet@8/libexec` + `DOTNET_ROLL_FORWARD=LatestMajor` + `ilspycmd 8.2.0`）。
- **分期实施**：P0 素材与协议固证 → P1 契约与领域层 → P2 通讯层 → P3 壳与插件宿主 → P4 首模块试点 → P5 平台抽象与三平台打包 → P6 旧资产桥接与扩展。
- **治理接入**：本变更绑定 GPCF Feature 与 Harness 六层，每期产出 evidence 到 `.harness/runs/`。

## Non-Goals

- 不声明「功能等价迁移」——功能模块 DLL 无源码；虽可凭 MB3000 与后端源码提高还原度，仍不承诺等价复刻。
- 不逆向设备类组件（视频播放 / 厂商 SDK）。
- 不声明跨项目集成、真实业务接入或生产就绪；状态天花板维持 `partial`。
- 不改写历史 17/19 项目基线与其他项目既有文档范围。
- 不在本变更内提交或推送 GPCF 共享工作区中与本变更无关的在途改动。
- 不引入新的 .NET 技术栈孤岛（已评估并否选 .NET + Avalonia 主线）。

## Impact

- 受影响仓库：`GlobalCloud SpaceAI Studio`（项目仓库）、`GlobalCoud GPCF`（治理与规格）、`GlobalCloud KDS`（知识沉淀）。
- 受影响文档：新增本 change 目录；`projects/spaceai-studio/STATUS.md` 追加重构路线；KDS 新增 `开发/14-SpaceAIStudio/`。
- 受影响自动化：需把 `SpaceAIStudio` 加入 `tools/kds-sync/document_control.py` 的 `PROJECTS` 映射，使 KDS 镜像可归类。
- 回滚边界：本变更只新增文档与规格，不改业务源码；回滚使用 `git revert`，禁止 `reset`/`clean`/`force push`。
