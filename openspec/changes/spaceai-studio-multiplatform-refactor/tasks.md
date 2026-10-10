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
- [ ] 10.5 待修：① 窗口位置偏差（-60,39，左导航被屏幕裁切——无边框窗口初始位置，待调）；② 巡更 `Xg`/设置 active 图标缺失（fallback）；③ 模块内容区——报警（10.6）、设备（10.7）已补，余：首页/视频/对讲/大屏/车辆/门禁/地图/巡更；④ ~~登录未真调 `/User/Login`~~（→ 10.21 已完成）。
- [x] 10.6 **R3 报警模块还原**（`ucAlarmInfo` + `FrmAlarmNoticeList`）：按原 Designer 还原 4 列行（时间 128 / 级别 60 / 名称 75 / 资产 88，底 `RGB(37,47,93)`，1px 分隔线）+ 级别配色（紧急红/重要黄/一般蓝）+ 「更多」链接；数据经 BFF `/api/Alarm/Info/Page`（**内置模拟上游**，无需真实后端）。**实机截图验证**：5 条报警、「共 5 条 · 未处理 3」、无错误。
- [x] 10.7 **R4 设备模块还原**（`menustruct no=19`）：字段沿用遗留 `Model/DataAssert.cs`（`AssetID`/`AssetName`/`AssetTypeID`/`AssetBrand`/`AssetOwner`/`address`/`StatusID`/`CanControl` + 环境温湿度光照）；列表 + 详情面板（`/DeviceAccess`、`/Asset/AssetInfo/AssetID/{id}`）。**实机截图验证**：5 台设备、「共 5 台 · 在线 4 · 离线 1」、无错误。
- [x] 10.8 **真机验证暴露并修复两处深链缺陷**（Node 测试盲区）：① `packages/protocol/src/rest.ts` 默认 `fetch` 未绑定 `globalThis` → WebView 抛 `Can only call Window.fetch on instances of Window`（已绑定 + 新增「浏览器严格 this」回归测试）；② BFF 缺 CORS → WebView（origin `tauri://localhost`）跨源请求报 `Load failed`（已加 CORS 中间件：回显 Origin + OPTIONS 204 + credentials）。`pnpm test` **79/79**。证据：实机截图 2 张（报警 / 设备）。
- [x] 10.9 **主窗体自适应屏幕**：`lib.rs` setup 显式 `maximize()`（此前固定 1920×1080 窗口在小屏溢出：位置 -60,39、左导航被裁）；配置改 1440×900 + 显式 `label`；新增 `viewport.ts`（`computeStageScale` contain 语义 + 7 项单测），登录页改为 **1920×1080 设计舞台 + 原始像素坐标**（134/408/459/465/895/465/1809/1877…）等比缩放 → 任意分辨率不裁切不错位。**实机验证**：窗口 `0,39 1800×1074`（铺满屏宽），12 导航项完整可见。`pnpm test` **86/86**。
- [x] 10.10 **R5 门禁模块还原**（`menustruct no=20` `mjmng`）：字段取自遗留 `Class/ADoorAccessMng.cs` 注释的 `strDoor[]` 十项（`AssetID`/`AssetName`/`CardID`/`UserID`/`UserName`/`Department`/`InOutTypeName`/`IODatetime`/`Satff`/`InType`）；实现刷卡记录表（进/出配色）+ 右侧门控制（`icon_doorcontrol_normal`，远程开门）。端点 `/Door/Record/Info/Page`、`/Door/Info`、`/Door/Open` 属**新架构约定**（遗留 DLL 缺失），代码内已标注待与真实 DLL 核对。**实机截图验证**：5 条记录（进 3 / 出 2）+ 3 扇门 + 开门按钮，无错误。
- [x] 10.11 **R6 巡更模块还原**（`menustruct no=22` `xgmng`）：字段取自遗留 `Model/PatrolViolationRecordcs.cs`（30+ 字段，含 `PrisonDepot*` 监所字段——该系统原面向监所场景）+ `Model/PatrolCell.cs`（巡更点）+ `Model/PatrolType.cs`（类型）。实现违规记录表（类型按级别配色：一般蓝/重要橙/紧急红；处理状态红绿）+ 巡更点按 `OrderIndex` 排序列表 + 全字段详情面板。**注**：`Xg_*` 导航图标在遗留 `Resources/`（430 图）中缺失（原在缺失的 `Unisec_Patrol.dll` 资源里），暂用 MB3000 `icon-patrol.png` 替代（视图头注释已标注）。**实机截图验证**：4 条违规（待处理 2）+ 4 个巡更点，无错误。
- [x] 10.12 **R7 地图模块还原**（`menustruct no=21` `mapmng`）：遗留控件 **GMap.NET**（第三方开源，Windows 专用）→ 按处置矩阵「**第三方替换**」，重构版以 **SVG 平面图 + 画布坐标**渲染（本机模拟）。实现 4 区域轮廓 + 5 设备点位（按类型配色：视频/门禁/巡更/照明）+ 图例 + 类型过滤 + 点位详情。端点 `/Map/Layout`。**实机截图验证**：5 点位渲染正确、图例与统计（点位 5 / 显示 5）正常，无错误。
- [x] 10.13 **R8 对讲模块还原**（`menustruct no=15` `talkbackmng`，`alarm=true`）：字段取自遗留 `Model/TalkBack.cs`（`DeviceName`/`DeviceId`/`CustomID`/`DeviceType`/`DeviceTypeCode`）与 `BLL/BllTalkcall.cs`（`InsTalkcallHistory`/`UpdTalkcallHistoryToHandle` → `Caller`/`StartTime`/`EndTime`/`Result`/`IsHandled`/`Handler`）；**处理弹层按 `FrmTalkcallHandle.Designer.cs` 还原**（标题「对讲通话处理」/发生时间/处理人员/`btnHandleLater` 93×25 稍后处理/`btnSure` 93×25 确定）。端点 `/TalkBack/Device/Info`、`/Talkcall/History/Info/Page`、`/Talkcall/Handle`（DLL 缺失，端点名为新架构约定）。**实机截图验证**：5 条通话记录（未处理 2）+ 4 台对讲设备 + 处理弹层可用，无错误。注：`alarm=true`（对讲与报警联动）在报警事件接入 Socket 阶段补。
- [x] 10.14 **R9 车辆/卡口模块还原**（`menustruct no=18` `bayonetmng`，`alarm=true`）：字段取自遗留 `Classes/VehicleInfo.cs`（21 字段：`captureNo`/`roadwayNo`/`directionNo`/`hostNo`/`roadCode`/`alarmType`/`plateCode`/`PlateColor`/`vehicleType`/`vehicleSpeed`/`violationCode`/`captureTime`/`pic*`/`vehicleTypeName`/`PlatColorName`/`roadCaption`）+ `Classes/BayonetInfo.cs`（`id`/`code`/`caption`/`enabledkk`/`description`/`latitude`/`longitude`/`locate`/`parentId`）+ `Class/ABayonetMng.cs`（`strVehicle[]` 十二项）。实现过车记录表（方向与牌色配色、报警红字）+ 卡口侧栏（启停状态）+ 全字段详情。端点 `/Bayonet/Info`、`/Vehicle/Pass/Info/Page`（含卡口/报警过滤）。**实机截图验证**：5 条过车（报警 2）+ 3 卡口，无错误。
- [x] 10.15 **R10 视频模块还原**（`menustruct no=11` `videomng`，`config=true`）：**播放器属设备类**（`playerHW`/`playerVS300` 厂商 DLL）→ 不逆向、按「第三方替换」以 Web 播放器（HLS/WebRTC/flv）承接，**本机模拟**下每格显示模拟画面。字段取自遗留 `Model/Camera.cs`（`ID`/`CameraName`/`CameraNumber`/`StoreType`/`VideoBrand`/`CameraType`/`Available`/`LockStatus`/`AIOverlayEnabled`/`PlayBackTime`/`VideoLink`/`CustomerID`/`DeviceType`/`DeviceTypeCode`）。实现摄像机列表（在线/品牌/类型/AI/锁定）+ **2×2 分屏预览**（OSD 叠加：名称·编号/品牌机型/时间戳/AI 状态）+ 点击上墙与清格。端点 `/Video/Camera/Info`。**实机截图验证**：4/5 在线、4 格全播放模拟流带 OSD，无错误。
- [x] 10.16 **R11 大屏模块还原**（`menustruct no=16` `dpmng`，`config=true`）：模块 DLL **`UNISEC_DPControl_DH.dll`** 为大华拼接屏 SDK 封装 → **设备类不逆向**，新架构以「拼接屏网格 + 信号源分配 + 场景预案」Web 控制台承接（本机模拟）。字段取自遗留 `Model/LEDScreen.cs`（`DeviceName`/`DeviceId`/`CustomID`/`DeviceType`/`DeviceTypeCode`）。实现大屏设备选择 + **布局 1×1/2×2/3×3/4×4** + **场景预案**（全景/重点监控(监区)/全量上墙/清空）+ 拼接墙逐窗信号源分配（复用 `/Video/Camera/Info`）。端点 `/Screen/Info`。**实机截图验证**：3×3 拼接墙渲染、控件齐全，无错误。
- [x] 10.17 **R12 首页还原（业务总览）**（`menustruct no=00` `home`）：聚合 5 个 BFF 端点做**统计卡片**（报警 5/未处理 3、设备 5/在线 4、车辆 5/报警 2、巡更 4/待处理 2、门禁 5/进 3 出 2）+ **最近报警**（级别配色 + 处理状态）+ **9 项快捷入口**（点击直达模块）；替换原 P3 插件演示面板。**实机截图验证**：5 卡数据正确、最近报警 3 条、快捷入口 9 键，无错误。
- [x] 10.18 **R 系列收官**：`menustruct.xml` **12 个可见模块全部还原并实机验证** —— 首页 ✅ 视频 ✅ 报警 ✅ 对讲 ✅ 大屏 ✅ 车辆 ✅ 设备 ✅ 门禁 ✅ 地图 ✅ 巡更 ✅ 配置 ✅（BFF/平台面板）报警弹窗 ✅（复用报警视图）。累计 12 张实机截图存 `~/Desktop/Hermes文档/2026-10-10_SpaceAIStudio_*.png`；KDS `specs/R3-汇总.md`~`R12` 同步。`pnpm test` **86/86**。
- [x] 10.19 **R13 报警实时推送 + 弹窗联动**（还原遗留分发链路）：遗留「报警服务 → Socket（UDP 广播 + TCP :8888 裸文本，P0-02）→ `A*Mng.Notify` → `AbstractXxxMng.AlarmLD` → `FrmAlarmNoticeList` 弹窗」→ 重构版用 BFF 已挂载的 **Socket.IO（/ws）主题订阅**承接：BFF 周期广播 `alarm` 频道（`MOCK_ALARM_INTERVAL_MS`，默认 45000ms，0 关闭）；前端 `socket.ts`（`connectRealtime`/`toSocketIoUrl`，非浏览器安全降级）+ **`AlarmNoticePopup.vue`（还原 `FrmAlarmNoticeList`：362×210 / 透明度 0.9 / 级别配色 / 「更多」）**；ShellView 挂载订阅 + WebAudio 提示音 + 状态栏「实时通道已连接」+ 底部「报警通知」开关。新增 4 条 socket 单测 → `pnpm test` **90/90**。**实机截图验证**：弹窗收到 6 条实时报警（级别配色正确），无错误。
- [x] 10.20 **R14 专属联动窗（AlarmLD 分派）**：按 `AlarmCode`/名称分派 **门禁 / 车辆 / 巡更 / 通用** 四类处理（还原 `Class/ADoorAccessMng.cs`、`Class/ABayonetMng.cs` 等 `alarm=true` 模块的 `AlarmLD` 联动）：`AlarmLinkageDialog.vue` 显示报警四要素（名称/时间/设备/编号）+ 动作（**门禁类附「远程开门」**，复用 `/Door/Open`；通用「打开XX模块 / 标记已处理 / 忽略」）。**紧急报警自动弹出**；通知弹窗条目可点击唤起。**实机截图验证**：紧急报警自动弹出「报警处理」窗（含四要素 + 三按钮），「更多」跳转与弹窗开关均正常。
- [x] 10.21 **R15 登录真调 `/User/Login`**（完成 10.5-④）：`App.vue` 的 `onLogin` 先真调 `RestClient.login()`（还原 `Pub.Login`：`Name`/`PWD`/`LoginIP`/`CallBackUrl`）——**失败**显示服务端 `errmsg` 并停留登录页，**成功**才初始化宿主；同时修复由 REST 基址推导实时通道地址的 bug（`http://host:port/api` → `ws://host:port/ws`）。BFF `/User/Login` 增加凭据校验（沿用遗留默认 `admin`/`123456`，来源 `FrmLogin.designer.cs` 硬编码默认值），错误口令返回失败信封。**验证**：curl 双路径（正确 → Token 信封；错误 → 「用户名或密码错误」）+ 实机重登录直达主界面（截图）。`pnpm test` **90/90**。
- [x] 10.22 **R16 BFF 常驻服务化（launchd）**：BFF 以 **LaunchAgent** 常驻（`ai.globalcloud.spaceai-bff`，命名对齐现有 `ai.globalcloud.*` 习惯）：**RunAtLoad 开机自启 + KeepAlive 崩溃自愈**，日志落 `~/Library/Logs/spaceai-bff*.log`；plist 模板与操作手册入仓库 `docs/deploy/`（含 `MOCK_ALARM_INTERVAL_MS` / `UPSTREAM_BASE` 配置说明与 kickstart/bootout/日志/健康检查命令表）。**验证**：`launchctl list` → `state=running`；**杀进程后 launchd 秒级自动拉起**（新 pid + `/healthz` 恢复）。
- [x] 10.23 **R17 报警处理窗对齐 `FrmAlarmHandle`**：将联动窗由「语义简化版」**重写为对齐遗留 Designer**（`FrmAlarmHandle.Designer.cs`，**866×540 无边框居中**）：标题栏 22px「报警处理」+ `btnClose`；**左栏 248px**（「报警消息」+ `check1/2/3`「一级/二级/三级」筛选 + `dgvAlarmList` 报警列表 + `cmbPCL/btnPCL` 预案行 + `label3`「视频查看」缩略）；**右栏**（`pnlAlarmVideo1` **报警视频 300px** + `lblAlarmMsg`「XX发生XX报警!」+ `pbAlarm` 图标 + `panel10` 处理区：「报警地点/报警内容/**处理说明(cmbCL)**/其他(txtCustomCL)」+「报警时间/类型/处理人」+ **`btnCL` 处理**按钮）；保留 AlarmLD 分派（门禁类附「远程开门」）。ShellView 传 `liveAlarms` 列表 + `@select` 切换查看报警（对齐 `dgvAlarmList` 选中联动右侧）。**实机截图验证**：紧急报警自动弹出 866×540 处理窗，各遗留区块齐全，无错误。
- [x] 10.24 **R18 配置模块「报警设置」还原 `FrmConfig` + 设置生效**：盘点遗留 Designer 发现 `FrmConfig`（492×389）实为**报警设置窗**；还原为 `AlarmSettingPanel.vue`（视频回放时间 + 秒（30~600）/ 文件保存位置 / **自动弹出设置**（一/二/三级）/ **自动刷新设置** / **程序运行设置**（弹窗/扩展屏/独立运行）/ 取消·保存），接入**配置模块**（BFF/平台面板之上）。新增 `alarm-settings.ts`（localStorage 持久化 + 范围校验 + `shouldAutoPopup`）——**自动弹出处理窗的级别改为按设置判定**（原硬编码「紧急」，对齐遗留 `checkBoxAlertAlarmLevel*` 语义）。新增 4 条单测 → `pnpm test` **94/94**。**实机截图验证**：配置页渲染还原面板（60s / `D:\AlarmVideo` / 弹出=一级 / 刷新=一二级 / 弹窗），无错误。
- [x] 10.25 **R19 账户体系还原（`FrmAccountSetting` + `FrmChangePassword`）**：顶栏用户区（显示登录名）点击弹出**账户下拉**，还原 `FrmAccountSetting`（129×146：修改密码 / 报警接收[开关] / 注销用户 / 分隔线 / 版本号）；「修改密码」打开 `ChangePasswordDialog.vue`，还原 `FrmChangePassword`（332×262：标题栏 + 分隔线 + **原始密码/新的密码/确认密码** + 取消·确定），校验链逐条对齐 `btnOK_Click`（空值 / 6~10 位 / 两次一致 /「确认要修改密码吗？」/「修改成功，重新登录生效！」）。BFF 新增 **`/User/UpdatePassword`**（旧密码与长度二次校验，更新内存凭据 → **改密真实生效**；登录端点改查可变凭据）。「注销用户」调 `/User/LogOut` 回登录页；成功后可一键**重新登录**。**实机端到端验证**：菜单 → 改密（校验+确认）→ 修改成功 → 重新登录 → **以新密码登录成功**（旧密码被后端拒绝；演示后凭据复位）。`pnpm test` **94/94**。
- [x] 10.26 **R20 报警弹窗还原 `AlarmWindows`（1300×880）+ `openType` 真实生效**：新增 `AlarmWindowsView.vue` 还原遗留 `AlarmWindows`（报警弹窗模块 no=33 的真实形态）：标题栏 50px「报警消息」+ **全部/一级/二级/三级筛选** + ⚙/⛶/✕；左区（`panel5` 消息条「XX发生XX报警!」RGB(31,36,41) + `pnlAlarmVideo1` **957×710** 报警视频 + `panelButtom` 52px 回放控制「上一页/实时/回放/1-4-7/下一页」）；右区 322px（`label10`「报警列表」+ `dgvAlarmList` 列**报警时间/报警设备** + `labPageAndCount` **1/N** 分页 + `label3`「报警处理」：报警类型/报警内容/处理说明/其它/处理人 + `labelPlan`「暂无预案」+ 处理按钮）。**接入**：菜单 no=33 由简化列表改为该窗（⚙ → 配置模块）；**报警打开方式真正消费 `openType`**（对齐 `InitAlarmWindow` 的 `WindowOpenType`）：弹窗 → `FrmAlarmHandle` 式处理窗；扩展屏/独立运行 → 打开报警消息窗（无第二屏时降级内容区全窗）。**实机截图验证**：1300×880 全要素呈现（筛选/消息条/视频/列表[选中联动]/分页/处理区），无错误。`pnpm test` **94/94**。
- [x] 10.27 **R21 遗留端点缺口补齐（接口面完整性审计）**：对遗留全解决方案 `HttpRequest(...)` 路径**逐一审计**（`BAL`/`Class/Global`/`FrmMain`），与 BFF 模拟上游比对后**补齐 5 个缺失端点**：`POST /Alarm/statistics/Count`（还原 `BAL.GetEventAlarmAll`：总数+未处理+日期）、`GET /Alarm/statistics/AlarmCount`（还原 `FrmMain`：按级别汇总）、`GET /User`（列表）+ **`PUT /User`**（改密，还原 `Global` 的 `UserParameter{UserID,Password}` 语义）、`GET /License`（还原 `Global.GetAuthorizationCode`：本机模拟授权）、`GET /Limit/Module`（还原 `Global.getUserFunction`：12 个可见模块权限）。**`/Test/SQL` 明确不实现**（安全红线）。新增 `mock.test.ts` 6 条用例 → `pnpm test` **100/100**；**curl 逐一验证** 5 端点信封正确（含按级别统计 紧急1/重要2/一般2）。
