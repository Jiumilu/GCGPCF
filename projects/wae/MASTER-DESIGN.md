---
doc_id: GPCF-DOC-455691886F
title: 世界资产浏览器（WAE）统一界面框架总体设计
project: WAE
related_projects: [GPCF, WAME, WAS, PVAOS, PKC, Brain, GFIS, GPC, Studio, XiaoG, XGD, XiaoC, MMC, ICP, AAAS, SOP, PQC, SpaceAI, SpaceAIStudio]
domain: ui-delivery
status: controlled
version: v0.1
owner: WAE
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/wae/MASTER-DESIGN.md
source_path: projects/wae/MASTER-DESIGN.md
sync_direction: bidirectional
inherits:
  - GPCF:01-architecture/GlobalCloud 项目群总体方案.md
  - GPCF:04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md
  - GPCF:04-ui-delivery/WAME专业工作台母框架差距评估.md
  - GPCF:04-ui-delivery/WAME专业工作台母框架升级方案.md
last_reviewed: 2026-10-12
supersedes: []
superseded_by: []
---

# 世界资产浏览器（WAE）统一界面框架总体设计 v0.1

> **立项决策记录（2026-10-12，老卢裁定）**
> 1. 项目名：沿用「世界资产浏览器 / WAE」；原 WAME/WAES 系统合并为 **WAME（世界资产模型引擎）**。
> 2. **技术形态：已裁定为分步路线 C** —— ① 共享包 monorepo 打底 → ② 统一入口注册 + 异构项目受控 iframe 嵌入 → ③ 按需微前端试点。详见 `projects/wae/技术形态对比分析_v0.1.md`。
> 3. **命名：已裁定** —— `WAE` = World Asset Explorer·世界资产浏览器（本项目）；原「WAE/世界资产引擎」与「原 WAES」**合并为 WAME（World Asset Model Engine·世界资产模型引擎）**，`WAES` 缩写停用。
>    ⚠️ **本项反转了 WAS 总体方案 V1.2 的命名口径**（V1.2 曾定 WAE=引擎、WAME=浏览器）；WAS 仓已按本裁定同步修订。
> 4. 立项登记已执行：KDS `_meta/project-registry.yaml`（`WAS-WAE-BROWSER`）+ GPCF 项目群总体方案项目清单 + GPCF 文档控制台账。




日期：2026-10-12（周一）
状态：**draft（待老卢确认后转 controlled）**
定位：本项目总体设计第一版，回答"世界资产浏览器项目是什么、以 WAME 主框架为基础统一所有项目界面框架怎么落地"。

> **本文只建立设计基线，不声明任何项目已接入、已集成或已验收。**
> 所有"已建成"均为代码勘察事实；所有"目标"均为设计意图，未经实现验证。

---

## 一、项目定位

### 1.1 名称与身份

| 项 | 内容 |
|---|---|
| 中文名 | 世界资产浏览器 |
| 英文名 | WAE（World Asset Explorer） |
| 对外副标题 | Global Cloud AI 工作台 |
| 项目归属 | GlobalCloud 项目群 / `世界资产` 空间 |
| 现有登记 | KDS `_meta/project-registry.yaml` → `WAS-WAME-DEMO`（世界资产模型引擎/WAME，原 WAES 演示版开发；现称「世界资产模型引擎」） |
| 既有定义 | 《WAME 产品需求文档 v2.2》：WAE 世界资产浏览器 = WASOS / PVAOS / ISAOS 三层结构的全景仪表盘与 AI 规则编排工作台 |

### 1.2 本项目的重新定位（老卢 2026-10-12 指令）

把"世界资产浏览器"从**WAME 内部的一个模块/工作台**，升级为 **GlobalCloud 项目群统一界面框架与统一入口**：

1. **统一界面框架**——所有项目的界面外壳、页面骨架、状态语义、证据语义、AI 边界组件，统一到本项目维护的一套框架上。
2. **先单独运行**——本项目先作为一个可独立启动的框架/容器运行，不依赖任何业务项目即可打开。
3. **逐个项目纳入**——在独立框架稳定后，按批把各业务项目以受控方式接入。

### 1.3 一句话定义

> **世界资产浏览器是 GlobalCloud 项目群的统一界面框架与统一入口：以 WAME 主框架为母本，先独立运行，再把各项目界面逐个纳入同一套外壳、骨架与组件标准。**

### 1.4 边界（本项目不做什么）

1. **不新建业务主账**——不接管 KDS 知识主存、GFIS 生产事实、GPC 订单事实、WAME 治理裁决权。
2. **不替代各项目后端**——只统一界面层（外壳/骨架/组件/令牌/接入协议），不统一各项目业务逻辑与数据源。
3. **不越权升级状态**——本项目不得自行声明任一项目 `accepted` / `integrated` / `production_ready`；沿用 GPCF 门禁。
4. **不另立标准**——界面标准继续以 GPCF《界面工程整体实施方案》为总控；本项目是其项下的**载体项目**，不替代总控文件。

### 1.5 与既有方案的关系（防止重复建设）

| 既有文件 | 状态 | 本项目的关系 |
|---|---|---|
| GPCF《GlobalCloud项目群界面工程整体实施方案》v1.0 | controlled | **上位总控**，本项目完全继承，不修改其分类模型与门禁 |
| GPCF《WAME专业工作台母框架差距评估》v1.0 | controlled | **直接输入**——本项目解决其指出的"母框架化封装能力不足" |
| GPCF《WAME专业工作台母框架升级方案》v1.0 | controlled | **直接输入**——本项目是其"三层目标"的工程载体化 |
| GPCF《统一体验骨架规范》《统一组件与设计令牌规范》 | controlled | **本项目实现这些规范**，不再另写一套 |
| WAME《总体方案 / 实施方案》 | controlled | WAME 继续作为治理执行主体；本项目只抽走其**壳与框架能力** |

**结论：本项目是既有方案的"工程载体化"落地，不是新体系，不产生第二套标准。**

---

## 二、现状盘点（事实源，2026-10-12 代码勘察）

### 2.1 项目群界面载体全景

| 项目 | 技术栈 | 入口/壳形态 | 与 WAME 同构度 | 纳入难度 |
|---|---|---|---|---|
| **WAME** | React18+Vite+TS+MUI7+Radix+Tailwind/shadcn | 状态机伪项目路由 + TitleBar/TopTabs/FunctionPanel + GlobalCloudShell | **母本** | — |
| **PKC** | React+Vite+TS+MUI7+Radix+Tailwind | react-router（createBrowserRouter）+ DashboardLayout + ProtectedRoute 权限 | **高**（同组件栈、同 shadcn 令牌） | 低 |
| **Brain** | React+Vite+TS+Radix+Tailwind（+react-resizable-panels） | 多面板可拖拽布局 + 空格选择器栏 | **高**（同组件栈，布局形态不同） | 低 |
| **PVAOS** | React+Radix+MUI（Figma Make 出身）+monaco | react-router + 双工作区/移动端适配 | **中**（同组件栈，历史文档堆积） | 中 |
| **SpaceAI Platform** | Vue3 monorepo（apps/desktop,server；packages/ui-kit,protocol,domain,plugin-sdk） | 已有 `@spaceai/ui-kit` 设计系统（深空指挥舱） | **低**（Vue，异构） | 高 |
| **Studio** | Node 后端 + web-ui（packages/client,desktop,server,esp32-c3,shared,skills） | 自带 client/desktop/server 体系 | **低**（异构） | 高 |
| **XiaoG** | 同上（hermes-web-ui 派生） | 移动/轻执行入口 | 低 | 高 |
| **XGD** | Electron + d3（ACUI Remix Library） | 桌面端长任务/重分析 | 低 | 高 |
| **XiaoC** | Electron（packages/ui,web,core,desktop,extension,mcp-server） | 模型路由/Agent 编排 | 低 | 高 |
| **PQC** | Next.js（frontend/，App Router） | 独立 Next 应用 | 低 | 中 |
| **GFIS / GPC** | Python 后端 + docs/openspec（无自有前端） | 无界面载体 | 无 | 待建页面时接入 |
| **MMC / AAAS / ICP / SOP** | Python 后端/契约 | 无界面载体 | 无 | 待建页面时接入（MMC 提供 `@globalcloud/kds-client` SDK） |

### 2.2 共享机制现状（重要）

1. **已有共享 SDK 先例**：`@globalcloud/kds-client` 位于 `GlobalCloud MMC/templates/sdks/kds-client`，被 PKC、Brain 以 `file:../GlobalCloud MMC/...` 方式依赖——**共享包模式在项目群已被采用**。
2. **已有设计系统先例**：SpaceAI Platform 的 `@spaceai/ui-kit`（令牌 `tokens.css`/`tokens.ts` + 基础组件 GcButton/GcPanel/GcKpiCard/GcTag/GcStatusDot）——**设计令牌 + 组件库模式已被采用**（但为 Vue，与 React 家族不通用）。
3. **WAME 内部已有统一外壳雏形**：`GlobalCloudShell`（Topbar + Sidebar + RightAIAssistantPanel + main）、`AppSwitcher`（WASOS/PVAOS/ISAOS 平台切换）、`platformModules.ts`（平台模块注册表）——**"统一容器 + 平台注册"机制已存在**。

### 2.3 WAME 主框架解剖（母本）

```
App（ErrorBoundary → AppContextProvider → LoadingProvider → AnimationProvider）
└─ AppContent
   ├─ TitleBar          标题栏（返回首页/搜索/模式）
   ├─ TopTabs           多项目标签栏（打开/切换/关闭项目）
   ├─ PageTransition    页面过渡
   │   └─ 按 activeProject.type 分支渲染（状态机路由，非 react-router）：
   │      MainContent │ AIWorkbench │ AgentDesktop │ GlobalCloudWorkbench
   │      │ WorldAssetStudio │ SystemSettings │ WaeEditor（默认）
   ├─ NotificationSystem / ShortcutFeedback / KeyboardShortcutsHelp
   ├─ PerformanceMonitor / WasmPerformanceMonitor
   ├─ ProjectManager（项目管理）
   └─ SmartRecommendations（智能推荐）
```

**四层可复用资产**：
1. **外壳层**：TitleBar / TopTabs / FunctionPanel（侧栏，1557 行）/ GlobalCloudShell / AppSwitcher / RightAIAssistantPanel
2. **骨架层**：MainContent + modules/*（每个模块一个页面族）
3. **组件层**：`components/ui/`（22 个 shadcn 组件：button/dialog/tooltip/dropdown-menu/tabs/table…）
4. **令牌层**：`styles/default_theme.css` + `globals.css`（Tailwind + CSS 变量令牌）

**模块系统**：`modules/` 下已有 6 个模块（agent-desktop / global-cloud-workbench / isaos / pvaos / wasos / wasset）——**"模块化挂载"模式已在本项目群运行**。

### 2.4 现状问题（差距，承接 GPCF 母框架升级方案）

1. **外壳层未封装**——GlobalCloudShell 只服务 `/global-cloud-workbench` 路由，不是全局壳；`components/Sidebar.tsx`、`layout/GlobalCloudSidebar.tsx` 新旧两套并存（改错文件无效果）。
2. **骨架层无模板族**——GPCF 要求的 5 类母模板（主列表/详情/异常/证据/操作工作台）在代码中无统一实现。
3. **组件层无组织法**——有 22 个基础组件，但缺"状态语义组/证据审计组/AI 边界组/危险确认组/分屏上下文组"的母框架级编排。
4. **接入无协议**——项目如何"被纳入"没有定义（无模块清单、无注册契约、无隔离边界）。
5. **设计令牌未收口**——WAME 令牌与 PKC/Brain 令牌是否同源未确认，`@spaceai/ui-kit` 另起一套。
6. **外壳与业务耦合**——WAME 壳内嵌 WASM、性能监控、项目持久化等 WAME 专属能力，直接抽会被一起带走。

---

## 三、目标架构

### 3.1 分层模型（五层，自下而上）

```
L5 接入层   项目适配器（Adapter）——把各项目挂进框架的统一接入协议
L4 外壳层   Shell——TitleBar / TopTabs / 侧栏 / 应用切换器 / 全局搜索 / 通知
L3 骨架层   页面模板族——主列表 / 详情 / 异常 / 证据审计 / 操作工作台 / AI 对话
L2 组件层   统一组件库——状态 / 证据审计 / AI 边界 / 表格筛选 / 危险确认 / 分屏上下文
L1 令牌层   设计令牌——颜色 / 间距 / 字体 / 圆角 / 阴影 / 状态色 / 暗色模式
```

**统一原则（继承 GPCF §6）：先统一语义，后统一装饰；先统一高风险组件，后统一展示风格。**

### 3.2 核心机制

1. **应用注册表（泛化 platformModules）**
   `PlatformModule` → `AppModule`：每个纳入的项目登记一个模块条目（id / 名称 / 入口 / 图标 / 导航组 / 路由 / 状态）。`AppSwitcher` 由三平台扩展为全项目群切换器。

2. **模块挂载（两种接入档次）**
   - **档次 A（同构项目，首选）**：项目在自己的仓内实现"框架适配层"，复用统一令牌与组件，壳由本项目提供。适用于 PKC / Brain / PVAOS。
   - **档次 B（异构项目，受控例外）**：Vue（SpaceAI Platform）/ Next（PQC）/ Electron（XGD/XiaoC）/ web-ui（Studio/XiaoG）保留自有壳，只接入**统一入口注册 + 令牌映射**，不强行换壳（按 GPCF §6.2 / 例外机制走审批）。

3. **状态机路由保留**——沿用 WAME 现有 `activeProject.type` 分支模式，避免引入 react-router 造成双路由体系。

4. **状态与证据语义层**——统一状态字典（running / blocked / partial / review / complete / candidate / human_required）与证据组件（证据卡 / 来源回指 / 审计项 / 裁决面板 / 引用块）。

5. **AI 边界组件组**——AI 建议区 / 引用区 / 采纳-驳回区 / 人工接管区 / 禁止动作提示区，强制"AI 建议 ≠ 业务事实"。

### 3.3 "先单独运行"的形态定义

本项目先以 **独立可启动的框架工程** 运行，具备：
1. 独立 `npm run dev` 可打开（不依赖任何业务项目后端）。
2. 自带演示模块（如 WAS 资产浏览 / 治理看板样例），证明外壳与骨架可用。
3. 框架自身可构建、可测试、可发布为版本化包，供各项目引用。

### 3.4 目标工程形态（已裁定：分步路线 C）

**已裁定（方案 C 第一步）：把框架抽为 monorepo 包，先独立运行，再逐项目引用；第二步做统一入口注册 + 异构 iframe；第三步按需微前端。**
- `@globalcloud/ui-tokens`（令牌层）
- `@globalcloud/ui-kit`（组件层，React 版；与 `@spaceai/ui-kit` 做映射而非合并）
- `@globalcloud/app-shell`（外壳层 + 骨架层）
- `@globalcloud/app-registry`（应用注册表 + 接入契约）
- 本项目仓 = 该 monorepo + 独立运行入口（演示/自检）

> 备选形态（**第一阶段不做**，留作第三步按需试点）：统一微前端容器（Module Federation / wujie）。风险：各项目技术栈差异大、Electron 与 Next 项目无法纳入、改造面过大。**先不做微前端**，用"共享包 + 统一入口注册"实现 80% 收益。

---

## 四、深度优化清单（对 WAME 主框架）

| # | 优化项 | 现状 | 目标 | 优先级 |
|---|---|---|---|---|
| O1 | 外壳解耦 | GlobalCloudShell 仅局部路由可用，内嵌 WAME 专属能力 | 抽出纯壳，WAME 专属能力下沉为可选插件 | P0 |
| O2 | 令牌收口 | WAME/PKC/Brain 令牌未验证同源 | 单一份 `ui-tokens`，各项目引用 | P0 |
| O3 | 侧栏统一 | 三套侧栏并存（FunctionPanel / Sidebar / GlobalCloudSidebar） | 保留一套，其余下线 | P0 |
| O4 | 状态语义层 | 代码中无统一状态字典 | 建立并接入骨架 | P0 |
| O5 | 证据/审计组件组 | 有零散实现（IntakeLedger 等） | 抽为统一组件组 | P1 |
| O6 | AI 边界组件组 | RightAIAssistantPanel 为 WAME 专属 | 泛化为可复用组件组 | P1 |
| O7 | 5 类页面模板族 | 无 | 建立母模板并至少各有一个实例 | P1 |
| O8 | 应用注册表 | platformModules 硬编码三平台 | 扩展为全项目群注册表 + 契约 | P1 |
| O9 | 接入协议 | 无 | 定义 Adapter 契约 + 接入检查表 | P1 |
| O10 | 外壳性能/可测 | 壳内 WASM/性能监控耦合初始加载 | 壳可独立测试、按需加载 | P2 |

---

## 五、纳入路径（分批）

**原则**：先同构、后异构；先轻、后重；每批必须有真实运行证据（UI gate）。

| 批次 | 纳入对象 | 接入档次 | 说明 |
|---|---|---|---|
| **B0** | 本项目自运行 | — | 框架独立运行 + 演示模块，通过 G1/G4/G5/G8/G9 门禁 |
| **B1** | WAS 资产浏览 / 治理演示 | A | 用框架自身能力做首个真实页面族（对齐 GPCF 首批样板） |
| **B2** | PKC | A | 同构度最高，验证"同栈继承" |
| **B3** | Brain | A | 验证"不同布局形态（多面板）继承" |
| **B4** | PVAOS | A | 验证"历史仓继承 + 迁移" |
| **B5** | 无前端项目（GFIS/GPC/MMC/AAAS/ICP/SOP） | A | 新页面直接建在框架上 |
| **B6** | Studio / XiaoG（web-ui） | B（例外评估） | 异构，只纳入统一入口 |
| **B7** | PQC（Next）/ SpaceAI Platform（Vue） | B（例外评估） | 异构，只纳入统一入口 + 令牌映射 |
| **B8** | XGD / XiaoC（Electron） | B（例外评估） | 桌面端，仅统一入口 |

> 与 GPCF 既定扩散序（`Studio → PKC → XGD → GPC → GFIS`）的关系：GPCF 序针对"专业工作台类"；本批次序按"技术同构度"排，二者不冲突——**B1/B2/B3 是 GPCF 序的工程化前置**。此差异作为待确认项（见第九章）。

---

## 六、治理与门禁（继承，不新立）

1. **分类模型**：沿用 GPCF 7 类一级分类 + 2 类二级约束。
2. **关键门禁**：G1 Surface Structure / G4 Evidence And Governance / G5 AI Fact Separation / G8 Runtime Verification / G9 Scope Control 不得失败。
3. **UI gate**：涉及界面改动的每轮必须留证（Tool route / Context package / Prompt profile / Design options / Selected option / WAME baseline reuse）。
4. **例外机制**：档次 B 项目走受控例外（不适配对象 / 原因 / 影响范围 / 替代方案 / 不扩散承诺 + 三方审批 GPCF+WAE+目标项目）。
5. **非声明边界**：本项目不得声明任何项目 `accepted` / `integrated` / `production_ready`。

---

## 七、分期实施

| 阶段 | 目标 | 交付物 | 完成标准 |
|---|---|---|---|
| **P0 框架立项与抽取** | 立项；外壳/令牌/侧栏解耦 | 立项登记、框架 monorepo 骨架、O1–O4 完成 | 框架独立 `dev` 可打开；令牌单源；门禁通过 |
| **P1 组件与模板族** | 组件组 + 5 类母模板 | O5–O8 + 模板族实例 | 至少 3 类母模板跑通并留证 |
| **P2 首批纳入** | B1–B4 接入 | 接入协议 + PKC/Brain/PVAOS 适配 | 至少 1 个跨项目真实 UI gate 通过 |
| **P3 全面纳入与例外治理** | B5–B8 | 例外清单 + 回归 | 例外受控且有限；月度评审确认 |

---

## 八、风险

| 风险 | 影响 | 缓解 |
|---|---|---|
| 壳内 WAME 专属能力耦合过深 | 抽取工期超预期 | O1 先做依赖清单，逐项判定"下沉/插件化/剔除" |
| 各项目技术栈分裂（Vue/Next/Electron） | 无法真正统一 | 明确档次 B 例外边界，只统一入口与令牌 |
| 抽取后 WAME 回归风险 | 破坏现有可用功能 | 抽取前后跑 WAME 全量测试（tsc/vitest/Playwright） |
| 令牌不统一导致视觉分裂 | 统一感失败 | O2 先验证同源再扩散 |
| 与 GPCF 扩散序冲突 | 治理口径不一致 | 列为待确认项，请 GPCF 裁定 |

---

## 九、待确认项（请老卢 / GPCF 裁定）

1. **立项载体**：是在 GPCF 项目群（`01-architecture/GlobalCloud 项目群总体方案.md` 项目清单 + KDS registry）新增独立项目，还是在现有 `WAS-WAME-DEMO` 上重新定位？是否建飞书项目群、是否新建独立仓？
2. **命名冲突**：`世界资产浏览器 = WAE = WAME 对外产品名`，与现有 WAME 项目同名。新项目是否沿用 WAE 名（与 WAME 同源但分工），还是另立名（如"GlobalCloud 统一界面框架 / GC-UI-Frame"）？
3. **技术形态**：确认采用"共享包 monorepo（推荐）"还是"微前端容器"？
4. **扩散序**：与 GPCF 既定序（Studio→PKC→XGD→GPC→GFIS）如何对齐——按同构度（本设计）还是按 GPCF 序？
5. **WAME 本体处置**：WAME 是否也会被纳入本框架（作为其中一个应用），还是保留独立壳？

---

## 十、下一步动作（待确认后执行）

1. 立项登记：KDS `_meta/project-registry.yaml` + GPCF 项目群总体方案项目清单。
2. 落盘受控：本文转 `controlled` 并登记 GPCF `09-status/globalcloud-document-control-register.md`。
3. 建仓：按确认形态建立框架仓/monorepo 骨架。
4. P0 执行：外壳解耦（O1）+ 令牌收口（O2）+ 侧栏统一（O3）+ 状态语义层（O4）。
5. 每步留 UI gate 证据。
