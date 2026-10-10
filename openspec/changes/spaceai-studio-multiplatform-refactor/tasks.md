---
doc_id: GPCF-OS-SPACEAI-STUDIO-MULTIPLATFORM-REFACTOR-TASKS-20261010
title: tasks
project: KDS
related_projects: [WAES, KDS, Studio, SpaceAIStudio, SpaceAI]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-studio-multiplatform-refactor/tasks.md
source_path: openspec/changes/spaceai-studio-multiplatform-refactor/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-10-10
supersedes: []
superseded_by: []
---

> 任务勾选不作为交付或验收证据；每项交付以 evidence 为准。

## 1. 治理与规格（本变更范围）

- [x] 1.1 建立本 OpenSpec 变更目录与四件套（proposal/design/tasks/spec）。
- [x] 1.2 把 SpaceAIStudio 的重定位（空间智能工作台，与 Studio 平行）写入 proposal 与 design。
- [x] 1.3 固定技术路线（Vue 3 + Naive UI + Tauri 2，三平台桌面）与资产处置结论。
- [x] 1.4 `projects/spaceai-studio/STATUS.md` 已含「重构路线」与证据指针（2026-10-10 升至 v1.1 复核）。
- [x] 1.5 已将 `SpaceAIStudio` 加入 `tools/kds-sync/document_control.py` 的 `PROJECTS` 映射（`15-SpaceAIStudio`；同时登记 `SpaceAI` → `16-SpaceAI`）。**并修正一处自引入错误**：KDS 目录初建误用 `14-` 前缀（与映射中的 `14-ICP` 冲突），已整体改为 `15-SpaceAIStudio`（31 个引用同步）。
- [x] 1.6 `loop_document_gate.py --check-only` 已运行并留存：**gate pass**（missing_metadata=0, missing_readme_dirs=0）。**期间发现并修复存量债务**：项目群扩至 21 项目后，37 份治理文档的 `related_projects` 未同步（config=21 vs 文档 18/14），门禁处于 `rework_required`；已批量同步 → 恢复 `pass`。
- [x] 1.7 `validate_project_group_openspec_coverage.py` 已运行：**status pass** —— 21 个项目，policy `required 9 / conditional 12 / waived 0`，`failures: []`。

## 2. P0 素材与协议固证（不改业务代码）

- [x] 2.1 《依赖处置表》→ `docs/specs/P0-05-dependency-disposition.md`（源码复用 7 / 逆向 7 / 设备类 10+ / 替换 5+ / 功能模块缺失 12 / 彻底缺失 4）。
- [x] 2.1b 归集 `SpaceAI` 源码依赖清单（`RestFUL` / `Unisec.Contracts` / `Unisec.Common` / `Utility` / `UNISEC_UserControls` / `WebS` / `Unisec_RegCode`）；版本兼容性核对留 P1。
- [x] 2.1c 逆向产物沿用既有 `SpaceAI.Recovered/`（7 组件 / 154,997 行，含 `_PROVENANCE.md` 溯源台账）；本仓未重复执行。
- [x] 2.2 《REST 协议规格书》→ `docs/specs/P0-01-rest-protocol.md`（20 端点、`ResultDS` 信封、Cookie 会话、`:8082` 回调）。**修正：`RestFUL` 是客户端 SDK，后端 `SqlService` 不在手 → 规格为客户端视角。**
- [x] 2.3 《Socket 协议规格书》→ `docs/specs/P0-02-socket-protocol.md`（UDP/TCP `:8888`、UTF-8 裸文本、80 字节缓冲、事件回调）。注：依据源码，报文格式待抓包补证。
- [x] 2.4 《领域模型规格》→ `docs/specs/P0-03-domain-model.md`（Studio 16 + SpaceAI 33 → 13 领域）。
- [x] 2.5 《迁移面清单》：245 个业务 cs 文件三分类完成 → **A 可迁移 66 / B 需重写 149 / C 不可用 30**（证据 `docs/specs/P0-06-migration-surface.md`）。
- [x] 2.6 技术债已登记（硬编码测试 IP、`Class/`+`Classes/` 重复目录、`.baiduyun` 残留）。
- [x] 2.7 《插件契约规格》→ `docs/specs/P0-04-plugin-contract.md`（`AbstractMng` + 6 扩展接口 → `plugin-sdk` 草案，含装配清单与 TS 草案）。

## 3. P1 契约与领域层

- [x] 3.0 《迁移面清单》（承接 P0-2.5）→ `docs/specs/P0-06-migration-surface.md`（245 文件：A 可迁移 66 / B 需重写 149 / C 不可用 30）。
- [x] 3.1 建立 monorepo 骨架（`apps/` / `packages/` / `plugins/` + pnpm workspace + `tsconfig.base.json` + `.gitignore` 补充）。
- [x] 3.2 `packages/domain`：13 领域类型（字段沿用遗留原名）+ 领域纯函数。
- [x] 3.3 `packages/plugin-sdk`：装配契约（替代 `AbstractMng`，6 项能力）+ `isAssemblable` 可装配校验。
- [x] 3.4 单元测试：**14/14 通过、零外部依赖**（Node 26 原生 TS 剥离 + `node --test`）。命令 `pnpm test`。证据 → `docs/specs/P1-01-contract-domain-layer.md`。

## 4. P2 通讯层

- [x] 4.1 `packages/protocol`：协议类型（`ApiResult<T>` 替代 `ResultDS`）+ **20 个端点常量**（唯一权威）。
- [x] 4.2 REST 客户端（`RestClient`：登录/查询/增改/删除/心跳/登出 + Token/Cookie 双模式）与 Socket 语义（编解码、80 字节约束、通道识别、WS 转换）。
- [x] 4.3 **mock server 契约一致性测试通过**：`pnpm test` → **33/33**（P1 14 + P2 19），零外部依赖。证据 → `docs/specs/P2-01-transport-layer.md`。

## 5. P3 壳与插件宿主

- [x] 5.1 Tauri 2 桌面壳骨架：`Cargo.toml` / `tauri.conf.json` / `build.rs` / `main.rs` / `lib.rs` + **项目级 `rust-toolchain.toml`（1.95.0，不动全局默认）**。
- [x] 5.2 Vue 3 + Naive UI 壳（登录 / 主框架 / 菜单 / 插件宿主）+ **`packages/host` 插件宿主核心**（注册/菜单排序/权限过滤/路由汇总/能力路由/生命周期/报警分发，**10 测试**）。`vite build` 成功：2667 模块 → 140.01 kB（gzip 51.02 kB）。
- [x] 5.3 BFF（Koa 2 + Socket.IO）骨架，**实测**：`/healthz` → `{"ok":true}`；`/` → `endpoints:20`；`/ws` socket.io 握手返回 sid。
- [x] 5.4 构建产物证据：**前端产物 ✅**（`apps/desktop/dist/`，140 kB）；**macOS 桌面二进制 ✅**（`apps/desktop/src-tauri/target/debug/spaceai-studio`，**25.2 MB，Mach-O arm64 可执行**）；**Windows / Linux ❌ 本机无法构建 → 改由 CI matrix 产出**。

## 6. P4 首模块试点

- [x] 6.1 选定 **巡更（patrol）**——遗留系统中数据耦合最低（通用端点、无设备 SDK 依赖）。
- [x] 6.2 **端到端链路跑通**：`plugins/patrol` 模块 + `ModuleHost` 装配 + `PatrolService` + `RestClient` + 真实 HTTP（mock server 断言 method/path/body）。测试 **8 用例**，`pnpm test` → **51/51**。
- [x] 6.3 **行为比对**：与 `BAL/BAL.cs` 查询模式逐项比对（同端点、同分页语义；去 XML/去 UI 耦合为有意变更）；并记录 **MB3000 巡更为 UAV 语义、与 Studio 不同**的警示。证据 → `docs/specs/P4-01-patrol-pilot.md`。

## 7. P5 平台抽象与打包

- [x] 7.1 Rust 侧平台抽象：`apps/desktop/src-tauri/src/platform.rs` —— TCP 设备探测 `probe_tcp` + `#[tauri::command] probe_device / common_device_ports` + 常见安防端口表；**`cargo test` 5/5 通过**。原则：设备类为第三方，**只做标准协议探测**（ONVIF/RTSP/GB28181 均基于 TCP），不引入厂商 SDK。
- [x] 7.2 三平台 CI：`.github/workflows/build.yml`（test job + bundle matrix：macOS arm64 / macOS x64 / Linux / Windows），tag 时自动建 draft release。**配置就绪，待推送后运行验证**（本机只能产出 macOS）。
- [x] 7.3 macOS 打包与校验：`SpaceAI Studio.app`（**8.17 MiB**；`Contents/MacOS/spaceai-studio` 8.1 MB + icns + Info.plist；`otool -L` 无本地路径依赖=**自包含**）。**实际启动未做**（需 GUI 会话）；Windows / Linux 依赖 CI 产物。

## 8. 收口与归档

- [x] 8.1 证据归档到 `.harness/runs/20261010-075917-spaceai-studio-multiplatform-refactor/`（`run.yaml` + `validation-summary.yaml` + `evidence-index.yaml`）；**YAML 语法校验通过**，文档门禁 pass。
- [x] 8.2 状态复核：`projects/spaceai-studio/STATUS.md` 升 **v1.1**，**维持 `overall_status: partial`**；补录 P0–P5 执行结果、凭据安全结论、UAV 巡更语义警示与证据指针。
- [x] 8.3 归档前置条件核对：**不满足** → ① ~~任务 29/37 未闭合~~ → **已解除（37/37）**；② `.harness/config.yaml` 要求 `archive.require_acceptance_first` 与 `require_confirmation`（需人工验收+确认）；③ 缺运行态与三平台产物证据。**`openspec archive` 暂不执行**，维持 `partial`。

## 9. P6 桥接扩展（前端平台能力接入）

- [x] 9.1 **前端平台桥** `apps/desktop/src/platform.ts`：Tauri 环境检测（`__TAURI_INTERNALS__`）+ `invokeTauri`（**非 Tauri 环境安全降级、不抛错**）+ `probeDevice` / `commonDevicePorts` 封装；依赖 `@tauri-apps/api ^2.12.2`（**动态 import** → 独立分包 `core-*.js` 2.49 kB，Web 场景不加载）。
- [x] 9.2 **设备探测面板** `apps/desktop/src/views/DeviceProbeView.vue`（主机/端口输入、可达性与延迟显示、常见安防端口表），挂载于 `ShellView` 的「平台能力（Tauri）」区。
- [x] 9.3 **测试与构建**：新增 **6 个测试**（降级行为 / 接口形状 / 环境恢复）→ `pnpm test` **57/57**；`vite build` 2673 模块 → 143.45 kB（gzip 52.55 kB）。证据 `docs/specs/P6-01-frontend-platform-bridge.md`。
- [x] 9.4 **BFF 连通性联调**：`apps/desktop/src/bff.ts`（`checkBff`）+ `BffStatusView.vue` + **6 测试**；**真实端到端验证**（启动 `apps/server` → `checkBff` → `{ok:true, endpoints:20, version:"0.1.0"}`，验证后已停止服务）→ `pnpm test` **63/63**。
- [x] 9.5 **REST 代理** `apps/server/src/proxy.ts`：`/api/*` → 上游（`UPSTREAM_BASE`，未配置不挂载），含前缀剥离、查询串/请求体/**`Set-Cookie` 会话透传**、逐跳头过滤、**不静默失败**（上游不可达 → `502` + 统一信封）、超时保护；**9 个测试** + **真实集成验证**（起 BFF+上游，`curl /api/User/Info?x=1` → 上游收到 `/User/Info?x=1`）→ `pnpm test` **72/72**。
- [x] 9.6 **业务链路（三段打通）**：`apps/desktop/src/api.ts`（前端 `RestClient` 经 BFF `/api/*` 访问上游，**不直连**）+ **6 测试** + **真实三段验证**（desktop → BFF → 上游，上游确收 `/ServerDateTime`）；UI 加「业务通道自检」按钮 → `pnpm test` **78/78**。
- [x] 9.7 **桌面实际启动验证**：`open -g` 启动 `.app` → **System Events 报告 1 个窗口**（界面真实渲染）→ 运行健康（CPU 0.1% / 内存 0.4% / STAT=S）→ **优雅退出**（响应 `quit` 事件）→ **无残留**。**「能构建」升级为「能启动、有界面、能正常退出」**。
- [ ] 9.8 余项（按需）：真实遗留后端的**字段级适配**、旧 DLL 兼容桥（Windows 专用）、移动端适配。

## 10. UI 还原（老卢 2026-10-10 方向：「重构后应还原原有 UI 和功能；外部连接可本机模拟」）

- [x] 10.1 **素材与依据盘点**：`menustruct.xml`（**12 个可见模块**：首页/视频/报警/对讲/大屏/车辆/设备/门禁/地图/巡更/配置/报警弹窗）+ `FrmLogin/FrmMain/FrmMenu` Designer（原始坐标）+ `Resources/`**430 个界面 PNG（21MB）**。
- [x] 10.2 **登录页还原**（`FrmLogin`）：按原坐标还原（`login_bg` 背景 / 双标题 / 双输入框 430×64 + `user`/`mima` 图标 / 记住用户名 / 登录按钮 / 右上角窗口按钮）；**33 个素材**入 `public/ui/`。
- [x] 10.3 **主界面壳还原**（`FrmMain`+`FrmMenu`）：左导航 **100px**（`NavBG` + `logooo` Logo + **12 模块** `ucMenu` 94×62）+ 顶部 **45px**（`TopBG`）+ 内容区 + 底部状态栏（`bg_screen_bottom`，红字状态）；窗口改**无边框最大化**（还原 `FormBorderStyle=None`+`Maximized`）。
- [x] 10.4 **验收**：`pnpm test` **78/78**；`vite build` 85.55 kB；**实机启动 + 截图核对**（登录页、主界面各一张，元素齐全、无破图无错位）。证据 `docs/specs/UI-R1-login-and-shell.md`。
- [ ] 10.5 待修：① 窗口位置偏差（-60,39，左导航被屏幕裁切——无边框窗口初始位置，待调）；② 巡更 `Xg`/设置 active 图标缺失（fallback）；③ 模块内容区——报警（10.6）、设备（10.7）已补，余：首页/视频/对讲/大屏/车辆/门禁/地图/巡更；④ 登录未真调 `/User/Login`（本机模拟登录为下一批）。
- [x] 10.6 **R3 报警模块还原**（`ucAlarmInfo` + `FrmAlarmNoticeList`）：按原 Designer 还原 4 列行（时间 128 / 级别 60 / 名称 75 / 资产 88，底 `RGB(37,47,93)`，1px 分隔线）+ 级别配色（紧急红/重要黄/一般蓝）+ 「更多」链接；数据经 BFF `/api/Alarm/Info/Page`（**内置模拟上游**，无需真实后端）。**实机截图验证**：5 条报警、「共 5 条 · 未处理 3」、无错误。
- [x] 10.7 **R4 设备模块还原**（`menustruct no=19`）：字段沿用遗留 `Model/DataAssert.cs`（`AssetID`/`AssetName`/`AssetTypeID`/`AssetBrand`/`AssetOwner`/`address`/`StatusID`/`CanControl` + 环境温湿度光照）；列表 + 详情面板（`/DeviceAccess`、`/Asset/AssetInfo/AssetID/{id}`）。**实机截图验证**：5 台设备、「共 5 台 · 在线 4 · 离线 1」、无错误。
- [x] 10.8 **真机验证暴露并修复两处深链缺陷**（Node 测试盲区）：① `packages/protocol/src/rest.ts` 默认 `fetch` 未绑定 `globalThis` → WebView 抛 `Can only call Window.fetch on instances of Window`（已绑定 + 新增「浏览器严格 this」回归测试）；② BFF 缺 CORS → WebView（origin `tauri://localhost`）跨源请求报 `Load failed`（已加 CORS 中间件：回显 Origin + OPTIONS 204 + credentials）。`pnpm test` **79/79**。证据：实机截图 2 张（报警 / 设备）。
- [x] 10.9 **主窗体自适应屏幕**：`lib.rs` setup 显式 `maximize()`（此前固定 1920×1080 窗口在小屏溢出：位置 -60,39、左导航被裁）；配置改 1440×900 + 显式 `label`；新增 `viewport.ts`（`computeStageScale` contain 语义 + 7 项单测），登录页改为 **1920×1080 设计舞台 + 原始像素坐标**（134/408/459/465/895/465/1809/1877…）等比缩放 → 任意分辨率不裁切不错位。**实机验证**：窗口 `0,39 1800×1074`（铺满屏宽），12 导航项完整可见。`pnpm test` **86/86**。
- [x] 10.10 **R5 门禁模块还原**（`menustruct no=20` `mjmng`）：字段取自遗留 `Class/ADoorAccessMng.cs` 注释的 `strDoor[]` 十项（`AssetID`/`AssetName`/`CardID`/`UserID`/`UserName`/`Department`/`InOutTypeName`/`IODatetime`/`Satff`/`InType`）；实现刷卡记录表（进/出配色）+ 右侧门控制（`icon_doorcontrol_normal`，远程开门）。端点 `/Door/Record/Info/Page`、`/Door/Info`、`/Door/Open` 属**新架构约定**（遗留 DLL 缺失），代码内已标注待与真实 DLL 核对。**实机截图验证**：5 条记录（进 3 / 出 2）+ 3 扇门 + 开门按钮，无错误。
