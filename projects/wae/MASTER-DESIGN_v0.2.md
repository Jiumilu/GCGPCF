---
doc_id: GPCF-DOC-WAE-MASTER-DESIGN-V02
title: 世界资产浏览器（WAE）统一界面框架总体设计 v0.2
project: WAE
related_projects: [GPCF, WAME, WAS, PVAOS, PKC, Brain, GFIS, GPC, Studio, XiaoG, XGD, XiaoC, MMC, ICP, AAAS, SOP, PQC, SpaceAI]
domain: ui-delivery
status: controlled
version: v0.2
owner: WAE
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/wae/MASTER-DESIGN_v0.2.md
source_path: projects/wae/MASTER-DESIGN_v0.2.md
sync_direction: bidirectional
inherits:
  - GPCF:projects/wae/MASTER-DESIGN.md (v0.1)
  - GPCF:01-architecture/GlobalCloud 项目群总体方案.md
  - GPCF:04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md
last_reviewed: 2026-10-12
---

# 世界资产浏览器（WAE）统一界面框架总体设计 v0.2

日期：2026-10-12（周一）
状态：**controlled（2026-10-12 老卢「全部」授权转正；§5 两项已按建议裁定，见下）**
相对 v0.1 的定位：**v0.1 建立设计基线；v0.2 补齐「实盘数据」与「可施工契约」**——v0.1 的现状盘点是技术栈表，v0.2 把它换成实测数据，并把目标架构从"分层名词"落到"接口契约"。

> **本版不含任何"已接入/已集成/已验收"声明。** 所有实测数据均标注取得方式与日期；所有契约均为设计意图，未经实现验证。

---

## 〇、v0.2 相对 v0.1 的变更（差异表）

| # | 项 | v0.1 | v0.2 |
|---|---|---|---|
| 1 | 现状盘点 | 技术栈表（定性） | **实测矩阵**（令牌 hash / 组件同名同容 / 页规模 / 壳行数），附可复现命令 |
| 2 | 令牌同源问题（O2） | "未确认是否同源" | **已实测**：核心 shadcn 令牌三仓字节完全相同，但以"复制件"散落 → 结论与改造成本重估 |
| 3 | 组件层（O7 前置） | "有 22 个基础组件" | **已实测**：PKC/Brain/PVAOS 各 48 个同名组件，**仅 2 个字节相同** → "同名单、异实现" |
| 4 | 外壳耦合（O1） | "GlobalCloudShell 内嵌 WAME 专属能力" | **更正**：`GlobalCloudShell` 仅 **25 行**，是薄壳；真正的耦合在 `TitleBar`(218) / `RightAIAssistantPanel`(345) / `FunctionPanel`(1557) |
| 5 | 目标架构 | 五层分层名词 | **可施工契约**（AppModule / Shell Props / 令牌 schema / iframe 契约 / 状态字典 逐字段给出） |
| 6 | 待确认项 | 5 项全开 | **3 项已裁定**（立项载体/命名/技术形态），2 项给出建议与裁定入口 |
| 7 | 纳入路线 | B0–B8 表格 | 补**每批验收判据**，并给出与 GPCF 既定扩散序的对齐方案 |

---

## 一、项目定位（承 v0.1，无变更）

### 1.1 一句话定义

> **世界资产浏览器（WAE）是 GlobalCloud 项目群的统一界面框架与统一入口：以 WAME 主框架为母本，先独立运行，再把各项目界面逐个纳入同一套外壳、骨架与组件标准。**

### 1.2 已裁定事项（2026-10-12，老卢）

| 项 | 裁定 |
|---|---|
| 项目名 | **WAE = World Asset Explorer = 世界资产浏览器**（本项目） |
| 命名 | 原「WAE/世界资产引擎」与「原 WAES」**合并为 WAME = World Asset Model Engine = 世界资产模型引擎**；`WAES` 缩写停用 |
| 立项载体 | KDS `_meta/project-registry.yaml` → `WAS-WAE-BROWSER`（世界资产空间，active）+ GPCF 项目群总体方案项目清单 + 文档控制台账 |
| 技术形态 | **方案 C 分步路线**：① 共享包 monorepo 打底 → ② 统一入口注册 + 异构受控 iframe → ③ 按需微前端试点（第一阶段**不做**微前端） |

### 1.3 边界（本项目不做什么）

1. **不新建业务主账**——不接管 KDS 知识主存、GFIS 生产事实、GPC 订单事实、WAME 治理裁决权。
2. **不替代各项目后端**——只统一界面层（外壳/骨架/组件/令牌/接入协议）。
3. **不越权升级状态**——不得自行声明任一项目 `accepted` / `integrated` / `production_ready`。
4. **不另立标准**——界面标准以 GPCF《界面工程整体实施方案》为总控；本项目是其**载体项目**。

---

## 二、实盘盘点（v0.2 核心新增，2026-10-12 实测）

### 2.1 技术栈与界面载体实测矩阵

| 项目 | 框架 | UI 基座 | 关键版本（实测） | 路由机制 | 页规模* | 接入档次 |
|---|---|---|---|---|---|---|
| **WAME**（母本） | React 18 + Vite + TS | MUI7 + Radix + Tailwind/shadcn | `@mui/material@7.3.5`、`tailwindcss@4.1.12` | **状态机路由**（`activeProject.type` 分支） | 124 | — |
| **PKC** | React 18 + Vite + TS | 同上 + zustand | 同上 + `zustand@^5.0.14` | react-router | 63 | A |
| **Brain** | React 18 + Vite + TS | 同上 + react-resizable-panels | 同上 | react-router | 125 | A |
| **PVAOS** | React 18 + Vite + TS | 同上 + monaco | 同上 + `react-router-dom@^7.17.0` | react-router | **416** | A |
| **PQC** | **Next 15 + React 19** | Tailwind | `next@^15.5.0`、`react@^19.1.0` | Next App Router | 28 | B（例外） |
| **Studio** | **Vue 3.5 + Vite** | 自研 | `vue@^3.5.32`、`pinia@^3.0.4` | vue-router | 34 | B（例外） |
| **XiaoG** | **Vue 3.5**（同 Studio 派生） | 自研 | 同上 | vue-router | — | B（例外） |
| **XiaoC** | **Electron 41 + Vue** | `packages/ui`（130 组件） | `electron@^41.1.0` | 状态机/主进程驱动 | — | B（例外） |
| **XGD** | **Electron 40** | d3 | `electron@^40.10.2` | — | — | B（例外） |
| GFIS / GPC / MMC / AAAS / ICP / SOP | Python 后端 / 契约 | **无自有前端** | — | — | 0 | A（新建页面直建在框架上） |

\* 页规模＝`pages|views|screens|app` 目录下 `.tsx/.vue` 文件数（近似量级，用于排批次，不作精确指标）。

**结论**：React 同构家族 = **WAME / PKC / Brain / PVAOS（4 家，页量占比 >80%）**；异构 = PQC(Next) / Studio+XiaoG(Vue) / XGD+XiaoC(Electron)。**方案 C 的"共享包"能覆盖 4 家同构 + 6 家无前端的全部新页面，即项目群绝大多数界面量。**

### 2.2 设计令牌实测（**修正 v0.1 的"未确认"**）

实测文件与内容哈希：

| 文件 | 字节 | 变量数 | SHA-256 前 12 位 |
|---|---|---|---|
| `WAME: src/styles/default_theme.css` | 4,319 | 76 | `54729cdf634f` |
| `Brain: default_shadcn_theme.css` | 4,319 | 76 | `54729cdf634f` ← **与上者完全相同** |
| `PVAOS: default_shadcn_theme.css` | 4,319 | 76 | `54729cdf634f` ← **与上者完全相同** |
| `WAME: src/styles/globals.css` | 6,618 | 79 | `b6e71d70874e` |
| `PVAOS: src/styles/globals.css` | **57,750** | 121 | `9d255e241262` ← 已分叉（外加大段业务样式） |
| `Brain: src/styles/globals.css` | **0** | 0 | `e3b0c44298fc` ← **空文件** |
| `PKC: src/styles/theme.css` | 5,527 | 76 | `e1791a879106` |
| `Brain: src/styles/theme.css` | 5,525 | 81 | `16184f5baa37` |

令牌交集分析：

| 对比 | 交集 | 仅左 | 仅右 | Jaccard |
|---|---|---|---|---|
| WAME.default_theme ↔ PVAOS.default_theme | 76 | 0 | 0 | **1.00** |
| PKC.theme ↔ Brain.theme | 76 | 0 | 5 | 0.94 |
| WAME.globals ↔ PVAOS.globals | 74 | 5 | 47 | 0.59 |

**实测结论（三点，直接决定 O2 的做法）**：

1. **核心 shadcn 令牌事实上已经同源**——`default_shadcn_theme.css` 在 WAME/Brain/PVAOS **三份字节完全相同**。v0.1 的"未确认是否同源"**可以销项**。
2. **但同源是靠"复制文件"维持的**：同一份文件存在于三个仓，**没有单一来源**，任何一方改动都不会传导。这正是 `@globalcloud/ui-tokens` 要解决的问题——**不是"统一分叉的令牌"，而是"把复制件收成单一来源"**。
3. **两个真实缺陷**：`Brain/src/styles/globals.css` 是 **0 字节空文件**；`PVAOS/src/styles/globals.css` 膨胀到 **57,750 字节 / 121 变量**（历史业务样式堆积）。这两处是收口时的**首个清理对象**。

补充：令牌存在**双命名**（`--accent` 与 `--color-accent` 并存，Tailwind v4 约定）——schema 设计需同时容纳两套名，不能只取其一。

### 2.3 组件层实测（**v0.2 新发现：同名单、异实现**）

对 `src/app/components/ui/` 目录做文件名 + 内容哈希比对：

| 项目 | 组件数 |
|---|---|
| WAME | **23** |
| PKC | **48** |
| Brain | **48** |
| PVAOS | **48** |

| 指标 | 实测 |
|---|---|
| PKC/Brain/PVAOS **三家共有**同名组件 | **48 个** |
| 其中**内容字节完全相同**的 | **仅 2 个**（`skeleton.tsx`、`utils.ts`） |
| 因此**同名但实现不同** | **46 / 48** |
| WAME 独有组件 | **0 个** |
| WAME **缺失**而三家都有 | **25 个**（`accordion` `alert-dialog` `aspect-ratio` `breadcrumb` `calendar` `carousel` `chart` `command` `drawer` `form` `hover-card` `input-otp` `menubar` `navigation-menu` `pagination` `popover` `radio-group` `resizable` `sheet` `sidebar` `sonner` `table` `toggle-group` `toggle` `use-mobile`） |

**实测结论（对 v0.1 的重要修正）**：

1. **组件层"看起来统一、实际各写各的"**——48 个同名组件里 46 个实现不同。**统一组件库不是"抄母本"，而是"逐组件收敛"**，需按 diff 分类处置（弃用 / 取一 / 并集）。
2. **母本反而最不全**——WAME 只有 23 个，**缺 25 个**（含 `table` `form` `sidebar` `navigation-menu` 这些高频件）。所以 `ui-kit` 的**基线应取"三家 48 的超集"，而非 WAME 的 23**。这一条直接改写 v0.1 的 O7 前置假设。
3. `sidebar.tsx` / `navigation-menu.tsx` 三家的实现分歧，正对应 §2.4 的"三套侧栏并存"。

### 2.4 外壳层实测（**修正 v0.1 的耦合判断**）

母本 `/src/app/layout/` 与相关壳件行数（实测）：

| 文件 | 行数 | 说明 |
|---|---|---|
| `GlobalCloudShell.tsx` | **25** | **薄壳**：props 仅 `{ children, context }`，只做容器 + 上下文注入 |
| `GlobalCloudTopbar.tsx` | 30 | 顶栏容器 |
| `GlobalCloudSidebar.tsx` | 49 | 侧栏（新） |
| `AppSwitcher.tsx` | 74 | 应用切换器（三平台） |
| `TitleBar.tsx` | **218** | 标题栏（返回首页/搜索/模式） |
| `RightAIAssistantPanel.tsx` | **345** | 右侧 AI 面板（WAME 专属语义） |
| `FunctionPanel`（侧栏） | **1,557** | 功能面板（真正的重件） |

**实测结论**：v0.1 说"GlobalCloudShell 内嵌 WAME 专属能力，直接抽会被一起带走"——**该判断不准确**。真实情况是：

- `GlobalCloudShell` 本身**已经是干净的薄壳**，可直接作为抽取起点（无需大改）。
- 真正的耦合集中在 **`FunctionPanel`(1557) / `RightAIAssistantPanel`(345) / `TitleBar`(218)** 三件，O1 的依赖清单应从这三件开始逐项判定"下沉 / 插件化 / 剔除"。
- **三套侧栏并存属实**：`FunctionPanel`(1557) / `components/Sidebar.tsx` / `layout/GlobalCloudSidebar.tsx`(49)。

### 2.5 应用注册表实测

母本契约位于 `src/app/domain/platform.ts`：

```ts
export type PlatformId = 'wasos' | 'pvaos' | 'isaos';

export interface PlatformRoute { id; label; path; moduleId: PlatformId; componentKey }
export interface PlatformNavGroup { id; label; items: PlatformRoute[] }
export interface PlatformModule {
  id: PlatformId; name; shortName; description;
  basePath; icon; navGroups: PlatformNavGroup[]; routes: PlatformRoute[]; enabled: boolean;
}
```

`AppSwitcher.tsx`(74 行) 将 **`moduleIcons` / `platformPositioning` / `platformStatus` 三张映射表按 `PlatformId` 硬编码在组件内**，并全部为三平台固定值。

**实测结论**：泛化为全项目群注册表，需做两件事——① `PlatformId` 联合类型 → 开放 `string`；② 把三张硬编码映射**外置到注册表条目**（每个 AppModule 自带 `icon` / `positioning` / `status`）。道路清晰，改动面小。

---

## 三、契约设计（v0.2 核心新增，可施工）

> 原则承 GPCF §6：**先统一语义，后统一装饰；先统一高风险组件，后统一展示风格。**

### 3.1 `@globalcloud/ui-tokens`（令牌单一来源）

**目标**：把现有"三份复制件"收成单一来源，且**不改变任何现有项目的外观**（零视觉回归）。

```
packages/ui-tokens/
├─ src/tokens.css        # 单一来源：基础令牌（保留双命名 --x 与 --color-x）
├─ src/tokens.ts         # TS 导出（供 JS 侧消费，如图表主题）
├─ src/semantic.css      # 语义层：状态色 / 证据色 / 危险色
└─ src/index.css         # 汇总入口
```

**迁移判据（逐项可验证）**：

| 判据 | 验收 |
|---|---|
| T1 零视觉回归 | 引用前后，各项目关键页截图逐像素比对（PVAOS/WAME/PKC/Brain 各 ≥3 页） |
| T2 单一来源 | 仓内不再存在 `default_shadcn_theme.css` 复制件；改为 `import '@globalcloud/ui-tokens'` |
| T3 双命名兼容 | `--accent` 与 `--color-accent` 两套名均可用（迁移期不强制收敛） |
| T4 缺陷清理 | `Brain/src/styles/globals.css` 空文件与 `PVAOS` 57KB 业务样式**移出令牌层**（分别处理，不混入 tokens） |

### 3.2 `@globalcloud/ui-kit`（组件层：**收敛**，非复制）

**基线**：取 **PKC/Brain/PVAOS 三家 48 个同名单的超集**（已含 WAME 缺失的 25 个），**不取 WAME 的 23**。

**收敛流程（逐组件）**：
1. 对每个同名组件做三方 diff → 归入四类：**①三家一致（2 个，直接采用）②细微差异（取一 + 记差异）③实质分歧（需裁定）④一方独有（并入）**
2. 每个组件产出：`ui-kit/src/<component>/` + `CONVERGENCE.md`（记录分歧与裁定）
3. 首批优先级：`button` `card` `table` `dialog` `dropdown-menu` `tabs` `badge` `input` `form` `sidebar`（高频 + 高风险）

**五组编排（母框架级，v0.1 的 O5/O6 落地为具体组）**：

| 组 | 内容 | 服务的门禁 |
|---|---|---|
| **状态语义组** | `StatusBadge` `StatePill` `StateTransition` —— 统一状态字典渲染 | 状态语义统一 |
| **证据审计组** | `EvidenceCard` `SourceRef` `AuditItem` `VerdictPanel` `CitationBlock` | G4 Evidence And Governance |
| **AI 边界组** | `AISuggestion` `AIProvenance` `AdoptReject` `HumanTakeoverNotice` `ForbiddenActionNotice` | G5 AI Fact Separation |
| **表格筛选组** | `DataTable` `FilterBar` `SavedView` `BulkAction` | 主列表母模板 |
| **危险确认组** | `DangerConfirm` `ScopeNotice` `ImpactPreview` | G9 Scope Control |

### 3.3 `@globalcloud/app-shell`（外壳 + 骨架层）

**抽取起点（实测证明可行）**：以现有 25 行的 `GlobalCloudShell` 为雏形，逐步把 `GlobalCloudTopbar`(30) / `GlobalCloudSidebar`(49) / `TitleBar`(218) 纳入；`FunctionPanel`(1557) 与 `RightAIAssistantPanel`(345) 作为**可选插件**（WAME 侧继续使用，框架只提供插槽）。

**Shell Props 契约（草案）**：

```ts
export interface ShellProps {
  /** 应用注册表（框架据此渲染切换器与导航） */
  registry: AppRegistry;
  /** 当前应用 id；受控模式由外部给定 */
  activeAppId?: string;
  onActiveAppChange?: (id: string) => void;
  /** 应用内容；非受控模式由框架按 registry 渲染 */
  children?: ReactNode;
  /** 可选插槽：侧栏 / 右侧面板 / 标题栏扩展 */
  slots?: {
    sidebar?: ReactNode;
    rightPanel?: ReactNode;
    titleBarExtra?: ReactNode;
  };
  /** 壳级能力开关：默认全关，WAME 侧显式打开（避免把 WAME 专属能力带进框架） */
  capabilities?: {
    wasmMonitor?: boolean;
    performanceMonitor?: boolean;
    projectPersistence?: boolean;
  };
  /** 接入档次：A=框架提供壳；B=iframe 受控嵌入 */
  mountMode?: 'A' | 'B';
}
```

**骨架模板族（v0.1 的 O7 落地为 6 类，每类给出接口而非仅名词）**：

| 模板 | 契约要点 | 首批实例 |
|---|---|---|
| 主列表 | 表头/筛选/分页/批量操作/空态/加载态 | WAS 资产目录 |
| 详情 | 头部摘要/分区/关联引用/变更历史 | 资产详情 |
| 异常 | 原因/影响/建议/升级路径/责任方 | 门禁失败页 |
| 证据审计 | 证据卡列表/来源回指/裁决面板 | 治理看板 |
| 操作工作台 | 步骤/校验/回滚/留证 | 发布流程 |
| AI 对话 | 建议/引用/采纳驳回/接管 | 统一 AI 区 |

### 3.4 `@globalcloud/app-registry`（接入契约）

**`AppModule` 契约（由实测的 `PlatformModule` 泛化而来，逐字段标注来源）**：

```ts
export interface AppModule {
  // ——— 承 PlatformModule（字段名与语义不变，降低迁移成本）———
  id: string;                    // 原 PlatformId 联合 → 开放 string
  name: string;
  shortName: string;
  description: string;
  basePath: string;              // 档次 A：框架内路由前缀；档次 B：外部 URL
  icon: string | ComponentType;  // 外置（原硬编码在 AppSwitcher 的 moduleIcons）
  navGroups: AppNavGroup[];
  routes: AppRoute[];
  enabled: boolean;

  // ——— v0.2 新增 ———
  positioning?: string;          // 外置（原 platformPositioning）
  statusLabel?: string;          // 外置（原 platformStatus）
  status?: AppStatus;            // 统一状态字典取值
  mount: 'A' | 'B';              // 接入档次
  entry: { kind: 'route' | 'iframe'; target: string };
  tokenProfile?: string;         // 令牌档（默认 'globalcloud-default'）
  maturity: 'candidate' | 'pilot' | 'adopted';  // 纳入成熟度（≠ 项目验收状态）
}

export type AppStatus = 'running' | 'blocked' | 'partial' | 'review'
                      | 'complete' | 'candidate' | 'human_required';
```

**接入档次判定表（机械可判，替代 v0.1 的定性描述）**：

| 条件 | 判定 |
|---|---|
| React 18/19 + Radix/Tailwind + 可改源码 | **A**（框架提供壳） |
| 非 React（Vue/Next）或不可改源码 | **B**（iframe 受控嵌入） |
| Electron 桌面端 | **B**（仅统一入口） |
| 无前端（纯后端项目） | **A**（新页面直建在框架上） |

**档次 B 的 iframe 受控嵌入契约（v0.1 只说"受控"，v0.2 给出条款）**：

| # | 条款 |
|---|---|
| B1 | 目标应用必须声明 `postMessage` 协议版本与支持事件集 |
| B2 | 令牌映射：宿主通过 `?gcTokens=<url>` 或 postMessage 注入令牌覆盖，目标页面须支持（否则记例外） |
| B3 | 导航一致性：面包屑/返回由宿主提供；目标应用不得自开顶层跳转 |
| B4 | 状态上报：目标应用以 `gc:status` 事件上报 `AppStatus`，宿主据此渲染统一状态条 |
| B5 | 沙箱：`sandbox` 属性白名单化；禁止同源直连业务库 |
| B6 | 例外登记：不满足 B1–B5 者按 GPCF 例外机制三方审批（GPCF+WAE+目标项目） |

### 3.5 状态字典与证据语义（统一语义层）

**统一状态字典（7 值）**：`running` / `blocked` / `partial` / `review` / `complete` / `candidate` / `human_required`

| 约束 | 内容 |
|---|---|
| S1 | 各项目自有状态词必须映射到该 7 值之一；未映射者不得进入统一外壳 |
| S2 | `complete` ≠ 项目验收；`accepted` / `integrated` / `production_ready` **不属本字典**（属 GPCF 门禁） |
| S3 | 证据语义：任何 AI 产出在统一外壳中**必须**携带来源回指；无来源不得渲染为事实 |

---

## 四、分批纳入路线（v0.2：补验收判据）

| 批次 | 对象 | 档次 | **本批验收判据（v0.2 新增）** |
|---|---|---|---|
| **B0** | 本项目自运行 | — | 框架独立 `dev` 可开；令牌单一来源生效（T2 判据）；`ui-kit` ≥10 组件收敛完成并有 `CONVERGENCE.md`；壳可独立测试 |
| **B1** | WAS 资产浏览 / 治理演示 | A | ≥3 类母模板有实例；状态字典 S1 全量映射；G1/G4/G5 门禁通过 |
| **B2** | PKC | A | 同栈继承成立：壳替换后 PKC 全量测试（tsc+vitest）通过；零视觉回归（≥3 页比对） |
| **B3** | Brain | A | 多面板布局继承成立：`resizable` 语义在框架侧可配；回归通过 |
| **B4** | PVAOS | A | 历史仓继承成立：416 页量下的**分批迁移路径**成文并跑通首批；回归通过 |
| **B5** | GFIS/GPC/MMC/AAAS/ICP/SOP | A | 新页面 100% 建在框架上（不得另起壳） |
| **B6** | Studio / XiaoG | B（例外） | B1–B5 条款满足或例外三方审批完成；统一入口可达 |
| **B7** | PQC / SpaceAI Platform | B（例外） | 同上 + 令牌映射验证 |
| **B8** | XGD / XiaoC | B（例外） | 同上（仅入口） |

### 与 GPCF 既定扩散序的对齐（v0.1 待确认项 #4 的解法）

GPCF 序：`Studio → PKC → XGD → GPC → GFIS`（面向"专业工作台类"）；本序按**技术同构度**。

**对齐方案（建议）**：两者**不冲突**——GPCF 序中的首个 `Studio` 是**档次 B 的例外演练**（先碰最难的异构，验证例外机制），本序把同构的 PKC/Brain/PVAOS 前置是为了**先把共享包打稳**。建议裁定为：

> **B0/B1（打基础）→ GPCF 序的 `Studio` 例外演练（并入 B6 首位）→ 回到本序 B2/B3/B4 → 余下按 GPCF 序。**

---

## 五、待确认项收敛（v0.1 五项 → 现状）

| # | v0.1 待确认项 | 现状 | 处置 |
|---|---|---|---|
| 1 | 立项载体 | ✅ **已裁定** | KDS registry `WAS-WAE-BROWSER` + GPCF 清单 + 台账（已执行） |
| 2 | 命名冲突 | ✅ **已裁定** | WAE 沿用；WAES→WAME；WAES 缩写停用（已全链传导） |
| 3 | 技术形态 | ✅ **已裁定** | 方案 C 分步路线（微前端留第三步） |
| 4 | 扩散序 | ✅ **已裁定（2026-10-12）** | **采纳对齐方案**：`B0/B1 打基础 → GPCF 序的 Studio 例外演练（并入 B6 首位）→ 回到同构序 B2/B3/B4 → 余下按 GPCF 序`。复核入口：GPCF 可在月度评审中提出异议。 |
| 5 | WAME 本体处置 | ✅ **已裁定（2026-10-12）** | **WAME 纳入为首个档次 A 应用**（同时是框架母本）；`FunctionPanel`/`RightAIAssistantPanel`/WASM/性能监控等专属能力**下沉为插件**（由 `ShellProps.capabilities` 显式开启，默认全关）。**不保留独立壳**——否则"统一界面框架"不成立。 |

---

## 六、风险（v0.2 更新）

| 风险 | 影响 | 缓解（v0.2 实测后更新） |
|---|---|---|
| 组件层 46/48 实质分歧 | 收敛工作量被低估 | 按四类分流（§3.2），细微差异类先行；实质分歧类进裁定清单 |
| 抽取后 WAME 回归 | 破坏现有可用功能 | 抽取前后跑 WAME 全量测试；`capabilities` 开关默认全关（§3.3） |
| PVAOS 416 页体量 | 迁移工期不可控 | B4 单列"分批迁移路径"判据；不以一次性迁移为目标 |
| 令牌双命名长期并存 | schema 复杂化 | 迁移期双命名，收敛期（B4 之后）再议 |
| 与 GPCF 序冲突 | 治理口径不一致 | §4 对齐方案，请上级裁定 |

---

## 七、下一步动作（v0.2 落盘后）

1. 本文转 `controlled` 并登记 GPCF `09-status/globalcloud-document-control-register.md`。
2. 请老卢/GPCF 裁定 §5 的第 4、5 项。
3. 建框架仓（monorepo 骨架：`ui-tokens` / `ui-kit` / `app-shell` / `app-registry`）。
4. 执行 P0：令牌单一来源（§3.1 T1–T4）+ 组件收敛首批 10 件（§3.2）+ 壳抽取（§3.3）。
5. 每步留 UI gate 证据。

---

## 附：实测命令（可复现）

```bash
# 令牌内容比对（§2.2）
shasum -a 256 <各项目>/default_shadcn_theme.css
grep -oE '\-\-[a-z0-9-]+' <各项目>/src/styles/*.css | sort -u

# 组件同名/同容比对（§2.3）
ls <各项目>/src/app/components/ui/ | wc -l
for f in <各项目>/src/app/components/ui/*; do shasum -a 256 "$f"; done

# 壳件规模（§2.4）
wc -l <WAME>/src/app/layout/*.tsx <WAME>/src/app/components/TitleBar.tsx

# 注册表契约（§2.5）
sed -n '1,30p' <WAME>/src/app/domain/platform.ts
```


---

## 附录 A：P0 第一步 工程进展（2026-10-12 落地）

框架仓已建立并**实测通过**：`GlobalCloud WAE/`（monorepo，4 包 + 1 应用，50 文件，首提交 `ab3da35`）。

| 包 | 落地内容 |
|---|---|
| `@globalcloud/ui-tokens` | 令牌单一来源（基线＝三仓字节相同的 `default_shadcn_theme.css`，SHA-256 前 12 位 `54729cdf634f`）+ 语义层（状态/证据/AI 边界）|
| `@globalcloud/ui-kit` | 组件收敛**首批 10 件** + `CONVERGENCE.md`（含实测矩阵、决策规则、待裁定清单、母本缺失 25 件）|
| `@globalcloud/app-registry` | `AppModule`/`AppStatus`/`AppRegistry` 契约 + `decideMountMode` 机械判定 |
| `@globalcloud/app-shell` | `Shell`（slots + capabilities + mountMode）/ `AppSwitcher` 泛化 / `StatusPill` |
| `apps/wae-console` | **独立运行入口**（Vite+React，五类母模板实例 + 自检页）|

**实测验证**（证据见该仓 `VERIFICATION.md`）：`tsc --noEmit` exit 0（4 包 + 1 应用全图）｜`vitest` 4/4 通过｜`vite build` 1694 模块 → 265KB JS + 4.5KB CSS｜`vite dev` 启动后 `localhost:4300` **HTTP 200**。

**诚实标注**：本仓**未触达任何现有项目**（WAME/PKC/Brain/PVAOS 一行未改）；`npm/pnpm install` 与 E2E 的执行状态见 `VERIFICATION.md`。

## 附录 B：命名卫生待决（新仓与旧目录易混）

新仓目录 `GlobalCloud WAE` 与现有目录 `GlobalCloud WAES`（其实已正名为 WAME）**只差一个字母**且同处一个父目录。

| 选项 | 说明 | 状态 |
|---|---|---|
| A | 新仓保留 `GlobalCloud WAE`；旧目录 `GlobalCloud WAES` **择机**改为 `GlobalCloud WAME` | 新仓已按此命名；旧目录改名**待影响评估**（涉及 5 个 Codex 工作树的 gitdir 绝对路径引用） |
| B | 新仓改叫 `GlobalCloud WAE-Browser` | 未采纳 |
| C | 维持现状，靠文档区分 | 当前实际状态 |
