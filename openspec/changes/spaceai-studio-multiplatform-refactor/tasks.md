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
- [ ] 9.4 余项（按需）：旧 DLL 兼容桥（Windows 专用）、移动端适配、BFF↔Tauri 联调、桌面环境实际点击验证。
