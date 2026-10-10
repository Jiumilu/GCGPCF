---
doc_id: GPCF-OS-SPACEAI-STUDIO-MULTIPLATFORM-REFACTOR-DESIGN-20261010
title: design
project: SpaceAIStudio
related_projects: [SpaceAIStudio, SpaceAI, Studio, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: 老卢
kds_space: 开发
kds_path: 开发/14-SpaceAIStudio/openspec/changes/spaceai-studio-multiplatform-refactor/design.md
source_path: openspec/changes/spaceai-studio-multiplatform-refactor/design.md
sync_direction: bidirectional
last_reviewed: 2026-10-10
supersedes: []
superseded_by: []
---

## Context

现状是一套 .NET Framework 4.5 / VS2013 的 WinForms 遗留客户端，采用「壳框架 + 反射加载插件」架构：

```
UNISECManage.exe（壳：登录 FrmLo → 主框架 FrmMain → 菜单）
  ├─ AMngClassSystem.LoadModularForm()  反射加载插件 DLL（返回 WinForms Form）
  │    └─ 插件统一继承 UnisecFunction.AbstractMng
  ├─ 通讯：REST（http://<DBUrl>/RestFul，XML/DataSet 交换）+ Socket（UDP 广播 :8888 / TCP）
  ├─ 数据：System.Data.SqlClient 直连（8 文件）、DataTable 贯穿（23 文件）
  └─ UnisecFunction（项目内源码，11,493 行）= 插件契约 + 自定义控件 + 日志 + 多语言
```

已知 REST 端点（代码提取，需 P0 补全）：`/User/Login`、`/User/LogOut`、`/User/Info`、`/User/KeepAlive`、`/License`、`/ServerDateTime`、`/Limit/Module`、`/Alarm/AlarmType/Info`、`/Alarm/statistics/Count`、`/Alarm/statistics/AlarmCount`、`/Log`、`/DeviceAccess`、`Asset/AssetInfo/AssetID/{id}`、`/sendMessages?templateId=`；HttpRequest 调用点 35 处。

**宿主/模块关系（v1.3 工程证据定稿）**：本项目（`UNISECManage`）`OutputType=WinExe` 且定义插件契约 `UnisecFunction.AbstractMng`，是**宿主壳**；姊妹项目 `GlobalCloud SpaceAI` 的 `MB3000.csproj` 为 `OutputType=Library`，其 `MB3000/AbstractTDMng : AbstractMng`（`using UnisecFunction;`）证明它是**被宿主加载的业务模块库**。两者是「宿主 + 模块」装配关系，治理身份仍各自独立登记、不合并。

## Goals / Non-Goals

**Goals:**

- 建立与 GlobalCloud Studio 平行的**空间智能工作台**产品线，技术栈与体系一致。
- 以单一前端代码库交付 **Windows / macOS / Linux 桌面**三端。
- 把遗留资产中可迁移的部分（领域模型、协议语义、插件契约思想）正式化为受控规格。
- 每期产出可运行、可验证的交付物，全程保持可运行版本（绞杀者模式）。

**Non-Goals:**

- 不恢复原安防功能等价性（无源码）。
- 不新增 .NET 技术栈。
- 不在本项目内承载业务事实写入或治理批准（经 MMC Gateway，知识沉淀到 KDS）。

## Decisions

### D1 技术选型：Web 优先（Vue 3 + Tauri 2），否选 .NET + Avalonia

| 方案 | 体系一致 | C# 复用 | 三平台桌面 | 结论 |
| --- | --- | --- | --- | --- |
| **Vue 3 + Naive UI + Tauri 2** | ✅ 与 Studio 同栈 | ~0% | ✅ | **采用** |
| .NET 8 + Avalonia 11 | ✗ 孤立 | ~35% | ✅ | 否选 |
| .NET MAUI | ✗ | ~25% | ✗ 无 Linux | 否选 |

理由：体系一致可复用 Studio 的 UI 体系与 MMC 网关；Tauri 复用系统 WebView（Windows=WebView2 / macOS=WKWebView / Linux=WebKitGTK），打包体量小；Rust 侧可承载本地能力（串口/USB/进程/托盘），弥补 Web 技术栈的设备集成短板。

### D2 目标架构

```
SpaceAIStudio/
├─ apps/
│  ├─ desktop/           Tauri 2 应用
│  │   ├─ src-tauri/      Rust 侧：本地设备适配、文件、进程、托盘、系统集成
│  │   └─ src/            Vue 3 + Naive UI 前端
│  └─ server/            BFF：Koa 2 / Node + Socket.IO（对齐 Studio）
├─ packages/
│  ├─ protocol/          REST OpenAPI + Socket 消息 schema（唯一权威）
│  ├─ domain/            领域模型（TypeScript 类型）
│  ├─ plugin-sdk/        插件契约（Web 版，平台无关）
│  └─ ui-kit/            组件库
└─ plugins/              空间智能模块（视频/报警/门禁/巡更/地图/大屏…）
```

### D3 插件契约重设计（对应原 `AbstractMng`）

原契约 6 属性（`StrWebServiceUrl`/`StrParam`/`StrUserID`/`StrUserName`/`StrDBConnect`/`StrDBUrl`）+ 方法（`ShowForm`/`ShowModelConfigFrom`/`AlarmLD`/`Dispose`/`ClossAllVideo`）。
新契约三条铁律：① **不返回 UI 类型**（去掉 `Form`，改为视图注册）；② **全异步**；③ **可脱离 UI 单测**。`StrDBConnect` 与 `StrDBUrl` 语义合并为 `IEndpointProvider`。

### D4 迁移策略：契约先行 + 绞杀者

每模块「提取四步法」：UI 剥离 → 逻辑提取 → 接口抽象 → 新 UI 实现。新壳并行运行，模块逐个替换。

**素材获取优先级**（每模块统一遵循）：① 有源码 → 直接读 `SpaceAI`（MB3000）项目源码；② 无源码但我方组件 → `ilspycmd` 逆向恢复；③ 设备类 → 按新定位重新设计接口，不逆向。

### D5 分期与验收

| 期 | 可验证交付物 | 验收门 |
| --- | --- | --- |
| P0 | 协议规格书、领域模型规格、迁移面清单 | 端点/报文与原客户端抓包逐条核对一致 |
| P1 | 契约 + 领域层库 + 单测 | 测试通过率 100%，零 Windows 依赖 |
| P2 | 通讯层（对接 mock server） | 契约测试与 P0 规格书一致 |
| P3 | 三平台可启动的壳 | 三平台构建产物 |
| P4 | 首模块端到端链路 | 端到端 + 与原客户端行为比对 |
| P5 | 三平台安装包 | 干净环境安装可运行 |
| P6 | 旧资产桥接 / 扩展 | 按需 |

**P0 不依赖选型**，无论后续路线如何调整，P0 产出全额有效。

## Risks / Trade-offs

| 风险 | 严重度 | 缓解 |
| --- | --- | --- |
| 功能模块 DLL 缺失（视频/报警/门禁等插件） | 中 | MB3000 单体源码（1,313 cs）作实现参照，按新定位重新实现 |
| 协议理解偏差 | 低（已降级） | `RestFUL` 后端源码在手，可直接读实现；辅以抓包核对 |
| 逆向产物质量与边界 | 中 | 仅逆向**我方**非设备类组件；核对行为一致性；设备类不逆向 |
| Linux WebKitGTK 视频解码能力不足 | 中 | Rust 侧集成 ffmpeg 或走服务端 WebRTC 流 |
| DevExpress 观感差异与重做成本 | 中 | 用 Naive UI 体系替代，接受视觉差异 |
| KDS 镜像未覆盖新项目 | 低 | 把 SpaceAIStudio 加入 document_control.py PROJECTS |

## Migration / Rollback

- 迁移：本变更仅新增文档与规格；实施阶段每期独立 Feature 与 evidence。
- 回滚：`git revert` 本变更提交；禁止 `reset`/`clean`/`force push`。
- 状态：全过程维持 `partial`；accepted/integrated/production_ready/customer_accepted 均需人工确认。
