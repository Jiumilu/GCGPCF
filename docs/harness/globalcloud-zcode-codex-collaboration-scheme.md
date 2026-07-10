---
doc_id: GPCF-DOC-ZCODE-COLLAB-20260709
title: GlobalCloud 项目群 ZCode + Codex 协同工作方案
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/globalcloud-zcode-codex-collaboration-scheme.md
source_path: docs/harness/globalcloud-zcode-codex-collaboration-scheme.md
sync_direction: bidirectional
last_reviewed: 2026-07-09
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 ZCode + Codex 协同工作方案

## 1. 定位

本文定义 GlobalCloud 项目群在 ZCode 与 Codex 双工具并行场景下的工作区拓扑、配置分层、协同规则和无缝切换机制。本文不替代任何项目总体方案或实施方案，仅定义工具协同层。

## 2. 工作区拓扑

项目群内全部 18 个项目均为独立 ZCode 工作区，在 ZCode 左侧面板注册：

| 序号 | 工作区 | 角色 |
|---|---|---|
| 0 | GlobalCoud GPCF | 总控工作区（hooks + commands） |
| 1-18 | 其余 17 个项目 | 独立开发工作区 |

注册机制：`~/.zcode/v2/setting.json` 的 `recentProjects` + `lastWorkspaceSession` 数组，GPCF 在首位（默认激活）。

## 3. 配置三层拓扑

| 层 | 位置 | 作用域 | 内容 | Codex 可见 |
|---|---|---|---|---|
| 用户级 | `~/.zcode/AGENTS.md` | 所有工作区 | 身份路由 + 3 条最高禁令 + gbrain 检索习惯 + 无缝切换规则 | 否 |
| 用户级 | `~/.zcode/cli/config.json` | 所有工作区 | gbrain MCP（stdio，全局检索） | 否 |
| GPCF 工作区级 | `GlobalCoud GPCF/.zcode/` | 仅 GPCF | hooks（队列注入 + 状态门禁）+ 5 个 commands | 否 |
| 共享层 | 各项目 `AGENTS.md` + GPCF Markdown | 对应项目 | 治理规则、边界、技术栈 | **是** |

## 4. 双工具无缝切换（文档级共享）

### 4.1 共享层（单一来源）

- 各项目 `AGENTS.md` —— 治理规则、边界声明
- GPCF Markdown 文档 —— 总控方案、对齐矩阵、台账
- gbrain 本地 DB（`localhost:5432/gbrain`）—— 4835 页面共享索引

### 4.2 切换规则

Codex 和 ZCode 打开同一个项目目录时：
- 读到同一份 `AGENTS.md` + 同一套 GPCF 总控文档
- 产出都回写 Markdown source-of-record
- 切换工具时无需迁移上下文，靠共享文档对齐

### 4.3 防冲突

- 两工具不同时写同一文件（无 Git，靠 `_legacy/` 回滚）
- 按 Feature/项目划分工具边界，不按时间并发

### 4.4 总体方案继承

所有子项目 AGENTS.md 已引用项目群总体方案/实施方案。ZCode 打开任一子项目时自动加载其 AGENTS.md + 用户级桥梁层，继承链与 Codex 完全一致。

## 5. 协同分工

| 场景 | 推荐工具 | 理由 |
|---|---|---|
| 跨项目总控、Feature 队列推进、对齐矩阵复核 | Codex | 原生多 project + GPCF 总控模型 |
| 单项目深度开发、代码实现 | ZCode | workspace hooks/commands 强 |
| 项目群知识检索 | 两者皆可 | 共享 gbrain DB |
| 状态门禁校验 | ZCode | Stop hook 自动拦截 |
| KDS 同步台账维护 | Codex | 已有成熟脚本链 |

## 6. GPCF 工作区专属配置

### 6.1 Hooks

| 事件 | 脚本 | 作用 |
|---|---|---|
| SessionStart | `.zcode/hooks/session-start.sh` | 注入活跃 Feature 队列（runtime/queue.json） |
| Stop | `.zcode/hooks/stop-gate.sh` | 软门禁：拦截 accepted/production_ready 等禁止自动声明的状态 |

### 6.2 Commands

| 命令 | 作用 |
|---|---|
| `/loop` | 推进 Feature LOOP 闭环 |
| `/status` | 项目群状态快照（17 项目 + 活跃 Feature + 阻塞项） |
| `/propose` | 发起 Change Proposal（OpenSpec change） |
| `/sync-kds` | 同步文档到 KDS 开发空间台账 |
| `/evidence` | 生成真实证据记录 |

## 7. 生效方式

首次配置 user 级 MCP 需重启 ZCode。重启后：
- 左侧面板显示全部 18 个独立工作区
- 任意子项目独立打开 → 自动识别项目群身份 + gbrain 可用
- 打开 GPCF → 额外获得 hooks + commands
- Settings → MCP 可确认 gbrain server 已连接

## 8. 已落地清单

```
~/.zcode/AGENTS.md                                    ✅ 桥梁层（含无缝切换规则）
~/.zcode/cli/config.json                              ✅ gbrain MCP
~/.zcode/v2/setting.json                              ✅ 19 个工作区注册（GPCF 首位）
GlobalCoud GPCF/.zcode/config.json                    ✅ hooks 启用
GlobalCoud GPCF/.zcode/hooks/session-start.sh         ✅ 队列注入
GlobalCoud GPCF/.zcode/hooks/stop-gate.sh             ✅ 状态门禁
GlobalCoud GPCF/.zcode/commands/loop.md               ✅ LOOP 推进
GlobalCoud GPCF/.zcode/commands/status.md             ✅ 状态快照
GlobalCoud GPCF/.zcode/commands/propose.md            ✅ Change Proposal
GlobalCoud GPCF/.zcode/commands/sync-kds.md           ✅ KDS 同步
GlobalCoud GPCF/.zcode/commands/evidence.md           ✅ 证据记录
```
