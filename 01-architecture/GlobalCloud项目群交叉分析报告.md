# GlobalCloud V0.0.1 项目群交叉分析报告

日期：2026-06-10  
基线：GPCF 00-index/README.md 0.0 节统一定义  
用途：对 GlobalCloud V0.0.1 下 11 个项目做全覆盖交叉分析，识别冗余、遗漏、边界冲突和治理缺口

## 一、项目群全景

| # | 项目 | 定位 | 仓库 | 治理状态 | Harness评分 |
|---|------|------|------|---------|------------|
| 1 | GlobalCloud Brain | 知识主存/LLM Wiki | [GCBrain](https://github.com/Jiumilu/GCBrain) | 基础 Manifest | - |
| 2 | GlobalCloud GFIS | 工厂执行系统 | [GCGFIS](https://github.com/Jiumilu/GCGFIS) | ready_for_human_acceptance | 96/100 |
| 3 | GlobalCloud GPC | 供应链公共服务平台 | [GCGPC](https://github.com/Jiumilu/GCGPC) | not_started | - |
| 4 | GlobalCloud PVAOS | 运营与门户底座 | [GCPVAOS](https://github.com/Jiumilu/GCPVAOS) | not_started | - |
| 5 | GlobalCloud WAES | 治理/证据/AI越权控制 | [GCWAES](https://github.com/Jiumilu/GCWAES) | not_started | - |
| 6 | GlobalCloud WIKI | 知识库(Wiki空间) | [GCWIKI](https://github.com/Jiumilu/GCWIKI) | not_started | - |
| 7 | GlobalCloud XGD | 数字意识框架(AI Agent) | [GCXGD](https://github.com/Jiumilu/GCXGD) | 无 Manifest | - |
| 8 | GlobalCloud XiaoC | 提示词工程服务 | [GCXiaoC](https://github.com/Jiumilu/GCXiaoC) | partial | 78/100 |
| 9 | GlobalCloud XiaoG | 本地语音助手 | [GCXiaoG](https://github.com/Jiumilu/GCXiaoG) | 无 Manifest | - |
| 10 | GlobalCloud开发控制台 | Harness Engineering 控制台 | [GCPCT](https://github.com/Jiumilu/GCPCT) | 无 Manifest(模板来源) | - |
| 11 | GlobalCoud GPCF | 体系文档工作区 | [GCGPCF](https://github.com/Jiumilu/GCGPCF) | not_started | - |

## 二、关键发现

### 2.1 严重冗余：Brain 与 WIKI 并存

**现状**：`GlobalCloud Brain` 与 `GlobalCloud WIKI` README.md 元数据完全一致（title: "GlobalCloud LLM Wiki"、space: GLOBAL、type: wiki_readme、status: canonical、authority_level: A0），目录结构相同（世界资产、个人、体系、工业绿链等），`SPACE_REGISTRY.yaml` 字段一致。差异为 Brain 多出 `GBRAIN_MIGRATION.md`、`docker-compose.yml`、`_legacy/`、`scripts/` 等。

**体系口径冲突**：GPCF 0.0 统一定义第7条——"Brain / LLM Wiki 是企业知识主存 / 知识编制与引擎候选"，体系只认一个企业知识主存。

**建议**：
- `GlobalCloud Brain` 保留为企业知识主存（GBrain），具备迁移和容器化基础
- `GlobalCloud WIKI` 降级为镜像/归档，README 标注 canonical source 为 GCBrain

### 2.2 文档混用：GPC 仓库含大量 GFIS 品牌文档

**现状**：`GlobalCloud GPC` 的 `docs/` 目录下 10 个文件（01-gcfis-constitution-extension.md ~ 10-gcfis-v0.2-cn-baseline-report.md）命名含 GCFIS 前缀。同时 GPC 有自己的核心文档（GPC-Native-实施规划.md、GPC-项目全面分析报告.md、继续开发路线.md）。

**影响**：GPC(供应链协同平台) 与 GFIS(工厂执行系统) 文档归属混淆。GPCF 0.0 统一定义第4条明确 gcfis_custom、ERPNext 资产归为 GFIS 历史实现资产/适配器资产。

**建议**：
- `docs/01~10-gcfis-*.md` 标注为 "historical reference，主源见 GFIS 仓库"
- GPC README 区分两类文档
- GPC 的 CHANGELOG.md 标题修正为 GPC（当前标题仍为 GFIS）

### 2.3 治理缺口：XGD、XiaoG 缺少 Harness Manifest

**现状**：XGD(v2.1.184, Electron 数字意识框架) 和 XiaoG(v6.0, ESP32 语音助手) 均无 PROJECT_HARNESS_MANIFEST.md，未纳入项目群治理体系。

**建议**：为 XGD、XiaoG 建立基础 Manifest；开发控制台作为模板来源保留无 Manifest 状态。

### 2.4 治理成熟度不均

| 等级 | 数量 | 项目 |
|------|------|------|
| ready_for_human_acceptance (96分) | 1 | GFIS |
| partial (78分) | 1 | XiaoC |
| not_started | 5 | PVAOS、WAES、WIKI、GPC、GPCF |
| 无完整 Manifest | 4 | Brain、XGD、XiaoG、开发控制台 |

### 2.5 技术栈分布

| 技术栈 | 项目 |
|--------|------|
| Node.js/TypeScript (Vite+React) | PVAOS、WAES |
| Python (Frappe/ERPNext + FastAPI) | GFIS、GPC(gpc_sop_engine) |
| Node.js (Electron) | XGD |
| ESP32 + Python (WebSocket) | XiaoG |
| Next.js (pnpm monorepo) | XiaoC |
| 纯文档 Markdown | Brain、WIKI、GPCF、开发控制台 |

PVAOS 与 WAES 同为 Vite+React+TS，可共享组件库（GPCF 04-ui-delivery 已定义统一组件规范）。

### 2.6 跨项目依赖关系

```
GPCF(文档体系) ─── 0.0节统一定义约束 ────┐
                                          ├── GPC(协同平台) ──CON── GFIS(工厂执行)
Brain(知识主存) ─── LLM Wiki服务 ────────┤                         │
                                          ├── WAES(治理) ────CON──┤
XiaoC(提示词工程) ─── MCP服务 ───────────┤                         │
                                          ├── PVAOS(运营门户) ────┘
XGD(Agent框架) ─── AI编排 ───────────────┤
                                          └── XiaoG(语音助手)
```

5根连接器约束了 GPC↔GFIS↔WAES↔Edge 的事实流，但 XiaoC/XGD/XiaoG 的 MCP/Agent 服务调用仍需纳入连接器治理。

## 三、行动清单

| # | 行动 | 优先级 | 目标项目 |
|---|------|--------|---------|
| 1 | Brain/WIKI 收口：WIKI 标注为 Brain 镜像 | P0 | WIKI |
| 2 | GPC 文档分类：GFIS 历史文档标注 + CHANGELOG 修正 | P0 | GPC |
| 3 | XGD 补充 PROJECT_HARNESS_MANIFEST.md | P1 | XGD |
| 4 | XiaoG 补充 PROJECT_HARNESS_MANIFEST.md | P1 | XiaoG |
| 5 | GPCF Manifest 从占位升级为详细配置 | P1 | GPCF |
| 6 | PVAOS/WAES/WIKI Manifest 补齐详细配置 | P2 | PVAOS、WAES、WIKI |
| 7 | XiaoC UI测试阻塞消解 + Wrangler安装 | P2 | XiaoC |
| 8 | 全项目 AGENTS.md 补齐（当前仅4/11有） | P2 | 各项目 |
| 9 | GPC CHANGELOG 标题从 GFIS 修正为 GPC | P2 | GPC |
| 10 | Brain SPACE_REGISTRY 更新项目群引用 | P2 | Brain |

## 四、与 GPCF 0.0 统一定义的对照

| 条款 | 核心要求 | 对照状态 |
|------|---------|---------|
| 1 | GPCF 是公共服务与治理体系 | OK：11个项目分布体现体系化 |
| 2 | GPC-Native 是平台本体 | 警告：GPC 仓库含 GFIS 文档混淆 |
| 3 | PVAOS 是运营门户底座 | OK：定位正确，治理待启动 |
| 4 | GFIS 是工厂事实主账 | OK：治理最成熟(96分) |
| 5 | WAES 是治理/证据/门控 | 警告：治理 not_started，remote 为本地 |
| 6 | Edge 优先服务 GFIS | 无独立 Edge 项目，需确认归属 |
| 7 | Brain 是知识主存 | 违规：Brain/WIKI 并存违反唯一真源 |
| 8 | 不得越权写入 | 警告：XiaoC/XGD/XiaoG AI写入边界未入连接器合同 |
