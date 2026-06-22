---
doc_id: GPCF-DOC-535BF5C0CA
title: GlobalCloud V0.0.1 项目群交叉分析报告
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud项目群交叉分析报告.md
source_path: 01-architecture/GlobalCloud项目群交叉分析报告.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud V0.0.1 项目群交叉分析报告

日期：2026-06-11
基线：GPCF 00-index/README.md 0.0 节统一定义
用途：对 GlobalCloud V0.0.1 下 12 个项目做全覆盖交叉分析，识别冗余、遗漏、边界冲突和治理缺口

## 一、项目群全景

| # | 项目 | 定位 | 仓库 | 治理状态 | Harness评分 |
|---|------|------|------|---------|------------|
| 1 | GlobalCloud Brain | 智能知识平台（WiIKI） | [GCBrain](https://github.com/Jiumilu/GCBrain) | 基础 Manifest | - |
| 2 | GlobalCloud GFIS | 工厂执行系统 | [GCGFIS](https://github.com/Jiumilu/GCGFIS) | ready_for_human_acceptance | 96/100 |
| 3 | GlobalCloud GPC | 供应链公共服务平台 | [GCGPC](https://github.com/Jiumilu/GCGPC) | not_started | - |
| 4 | GlobalCloud PVAOS | 运营与门户底座 | [GCPVAOS](https://github.com/Jiumilu/GCPVAOS) | not_started | - |
| 5 | GlobalCloud WAES | 治理/证据/AI越权控制 | [GCWAES](https://github.com/Jiumilu/GCWAES) | not_started | - |
| 6 | GlobalCloud KDS | 知识中心（LLM Wiki） | [GCKDS](https://github.com/Jiumilu/GCKDS) | 基础 Manifest | - |
| 7 | GlobalCloud PKC | 个人知识工作台 | [GCPKC](https://github.com/Jiumilu/GCPKC) | 无 Manifest | - |
| 8 | GlobalCloud XGD | 大象：长程 Agent、重分析、多端交互与运行承载 | [GCXGD](https://github.com/Jiumilu/GCXGD) | 无 Manifest | - |
| 9 | GlobalCloud XiaoC | 蚁后：AI 能力生产、Prompt/MCP、模型路由、任务拆解与结果汇总 | [GCXiaoC](https://github.com/Jiumilu/GCXiaoC) | partial | 78/100 |
| 10 | GlobalCloud XiaoG | 本地语音助手 | [GCXiaoG](https://github.com/Jiumilu/GCXiaoG) | 无 Manifest | - |
| 11 | GlobalCloud MMC | 管理配置中心 | [GCMMC](https://github.com/Jiumilu/GCMMC) | 无 Manifest(模板来源) | - |
| 12 | GlobalCoud GPCF | 体系文档工作区 | [GCGPCF](https://github.com/Jiumilu/GCGPCF) | not_started | - |

## 二、关键发现

### 2.1 已解决：Brain / WIKI 冗余

**2026-06-10 状态**：KDS（原 GCBrain 代码项目）与 WIKI 内容完全相同，存在企业知识主存不唯一的严重冲突。已收口：KDS 为企业知识主存唯一真源。

**2026-06-11 结论**：WIKI 已移出项目群。知识职能拆分为：
- `GlobalCloud KDS`（知识中心）：承接 LLM Wiki canonical source，四空间体系长期记忆
- `GlobalCloud Brain`（智能知识平台）：面向用户的 AI 驱动知识管理与协作 UI（WiIKI）

**风险**：需确认 KDS 与 Brain 之间的同步机制和数据流向，避免新的分歧。

### 2.2 文档混用：GPC 仓库含大量 GFIS 品牌文档

**现状**（未变化）：`GlobalCloud GPC` 的 `docs/` 目录下含 GFIS 前缀历史文档。GPC README 已添加 docs/ 目录说明，标注为 GFIS 历史参考。

**建议**：继续修正 CHANGELOG 标题（当前仍为 GFIS）。

### 2.3 治理缺口：XGD、XiaoG、PKC 缺少 Harness Manifest

**现状**：XGD(v2.1.184)、XiaoG(v6.0) 和 PKC 均无 PROJECT_HARNESS_MANIFEST.md，未纳入项目群治理体系。

**建议**：为 XGD、XiaoG、PKC 建立基础 Manifest。

### 2.4 治理成熟度不均

| 等级 | 数量 | 项目 |
|------|------|------|
| ready_for_human_acceptance (96分) | 1 | GFIS |
| partial (78分) | 1 | XiaoC |
| not_started | 4 | PVAOS、WAES、GPC、GPCF |
| 基础 Manifest | 2 | Brain、KDS |
| 无完整 Manifest | 4 | XGD、XiaoG、PKC、MMC |

### 2.5 技术栈分布

| 技术栈 | 项目 |
|--------|------|
| Node.js/TypeScript (Vite+React) | PVAOS、WAES、Brain、PKC |
| Python (Frappe/ERPNext + FastAPI) | GFIS、GPC(gpc_sop_engine) |
| Node.js (Electron) | XGD |
| ESP32 + Python (WebSocket) | XiaoG |
| Next.js (pnpm monorepo) | XiaoC |
| 纯文档 Markdown | KDS、GPCF、MMC |
| Python (Brain Platform) | KDS(gbrain-platform/server) |

Brain、PKC、PVAOS、WAES 同为 Vite+React+TS，可共享组件库。

### 2.6 跨项目依赖关系

```
GPCF(文档体系) ─── 0.0节统一定义约束 ────┐
                                          ├── GPC(协同平台) ──CON── GFIS(工厂执行)
Brain(智能知识平台) ─── UI/WiIKI ────────┤
KDS(知识中心) ─── LLM Wiki服务 ─────────┤                         │
                                          ├── WAES(治理) ────CON──┤
XiaoC(蚁后) ─── Prompt/MCP/模型路由/任务拆解 ─┤                         │
                                          ├── PVAOS(运营门户) ────┘
XGD(大象) ─── 长程Agent/重分析/多端交互 ─────┤
PKC(个人工作台) ─── 个人仪表盘 ──────────┤
                                          └── XiaoG(语音助手)
```

**新增依赖**：KDS 作为 canonical source 为 Brain 提供知识数据；Brain 作为 UI 层面向用户。两者需保持单向数据流（KDS→Brain）。

## 三、行动清单

| # | 行动 | 优先级 | 目标项目 |
|---|------|--------|---------|
| 1 | GPC 文档分类：CHANGELOG 标题修正 | P0 | GPC |
| 2 | KDS↔Brain 数据流同步机制定义 | P0 | KDS、Brain |
| 3 | XGD 补充 PROJECT_HARNESS_MANIFEST.md | P1 | XGD |
| 4 | XiaoG 补充 PROJECT_HARNESS_MANIFEST.md | P1 | XiaoG |
| 5 | PKC 补充 PROJECT_HARNESS_MANIFEST.md | P1 | PKC |
| 6 | GPCF Manifest 从占位升级为详细配置 | P1 | GPCF |
| 7 | PVAOS/WAES Manifest 补齐详细配置 | P2 | PVAOS、WAES |
| 8 | XiaoC UI测试阻塞消解 + Wrangler安装 | P2 | XiaoC |
| 9 | 全项目 AGENTS.md 补齐 | P2 | 各项目 |
| 10 | GPC CHANGELOG 标题从 GFIS 修正为 GPC | P2 | GPC |
| 11 | KDS SPACE_REGISTRY 更新项目群引用 | P2 | KDS |

## 四、与 GPCF 0.0 统一定义的对照

| 条款 | 核心要求 | 对照状态 |
|------|---------|---------|
| 1 | GPCF 是公共服务与治理体系 | OK：12个项目分布体现体系化 |
| 2 | GPC 是平台本体 | 警告：GPC 仓库含 GFIS 文档混淆 |
| 3 | PVAOS 是运营门户底座 | OK：定位正确，治理待启动 |
| 4 | GFIS 是工厂事实主账 | OK：治理最成熟(96分) |
| 5 | WAES 是治理/证据/门控 | 警告：治理 not_started，remote 为本地 |
| 6 | Edge 优先服务 GFIS | 无独立 Edge 项目，需确认归属 |
| 7 | 企业知识主存唯一 | 已解决：KDS 承接 canonical source，Brain 为 UI 层，WIKI 移除 |
| 8 | 不得越权写入 | 警告：XiaoC/XGD/XiaoG AI写入边界未入连接器合同 |


## 五、项目群领域分类

| 领域 | 项目 |
|------|------|
| 治理层 | GCMMC（管理配置中心）、GCPCF（文档工作区） |
| 知识层 | GCBrain（智能平台）、GCKDS（知识中心）、GCPKC（个人工作台） |
| 供应链层 | GCGFIS（工厂信息化）、GCGPC（绿色公链）、GCPVAOS（价值联盟） |
| AI 能力层 | GCXiaoC（蚁后：AI 能力生产与编排路由）、GCXGD（大象：长程 Agent 与重分析承载）、GCXiaoG（蚂蚁：轻量执行入口/语音助手） |
| 视窗层 | GCWAES（世界浏览器） |
