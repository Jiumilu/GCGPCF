# GlobalCloud 智能体团队 Loop Engineering 全面改进方案

日期：2026-06-12
状态：v1.0
依赖：[gpcf-loop-engineering-spec-v1.md](../02-governance/gpcf-loop-engineering-spec-v1.md)、[gpcf-agent-architecture-six-elements.md](../02-governance/gpcf-agent-architecture-six-elements.md)
定位：将全部 11 个智能体纳入 Loop Engineering 运行机制，每个智能体的职责、evidence 产出、状态升级路径全部对齐到主规范。

---

## 1. 智能体与 Loop 三角色的映射

Loop Engineering 定义了三种角色（执行/审计/集成），每个智能体必须明确归属：

| 智能体 | 中文名 | Loop 角色 | 对应层级 | 说明 |
|---|---|---|---|---|
| 小即 | 总控 | 集成层 | 大循环 | 跨项目收口、状态升级申请、版本冻结 |
| 宪衡 | 治理架构 | 执行层 | 微循环+中循环 | 治理对象、证据门、状态机 |
| 链同 | 协同业务 | 执行层 | 微循环+中循环 | PVAOS/GPC 协同链路 |
| 厂行 | 工厂执行 | 执行层 | 微循环+中循环 | GFIS/Edge 执行链路 |
| 数枢 | 数据平台 | 执行层 | 微循环+中循环 | 数据底座、读模型、指标 |
| 仓图 | 资源仓库 | 执行层 | 微循环+中循环 | 资源池、映射总表 |
| 知源 | 知识体系 | 执行层 | 微循环+中循环 | 知识主存、知识引擎 |
| 灵策 | AI 服务 | 执行层 | 微循环+中循环 | Agent 分层、模型治理 |
| 接稳 | 连接器可靠性 | 执行层 | 微循环+中循环 | 连接器合同、DLQ/Replay |
| 评衡 | 评估审计 | 审计层 | 中循环 | 量化评分、差距识别、复评 |
| 证验 | 证据验收 | 审计层 | 中循环 | 证据完整性、可复现性判定 |

**关键约束**：
- 执行层可以修改业务文件、产出 evidence、自检，但**不得自行宣布状态升级**
- 审计层可以判定、评分、发现阻塞，但**不得修改业务文件、不得替执行层补证据**
- 集成层可以跨项目收口，但**不得绕过项目仓 evidence、不得在审计未完成时标记 integrated**

---

## 2. 每个智能体的 Evidence 责任清单

每个执行智能体在完成一轮微循环后，必须产出以下 evidence：

| evidence 类型 | 用途 | 产出者 | 存放位置 |
|---|---|---|---|
| `loop-round-{ID}.md` | 本轮完整执行记录 | 执行智能体 | 项目仓 `docs/harness/loops/` |
| diff evidence | 文件变更证据 | 执行智能体 | 项目仓 `docs/harness/evidence/` |
| command log | 关键命令执行记录 | 执行智能体 | 项目仓 `docs/harness/evidence/` |
| test result | 自查结果（如适用） | 执行智能体 | 项目仓 `docs/harness/evidence/` |
| loop-state.md 更新 | 当前循环状态 | 执行智能体 | 项目仓 `docs/harness/` |
| status-audit 报告 | 中循环审计报告 | 评衡 + 证验 | 项目仓 + GPCF 汇聚 |
| evidence-index 更新 | 证据完整性索引 | 证验 | 项目仓 `docs/harness/evidence/` |

**不满足最低 evidence 集合的循环轮次，在 Harness 判定中视为"本轮不可追溯"。**

---

## 3. 智能体状态标签迁移

所有智能体的状态标签必须从旧标签迁移到 Loop Engineering 统一状态机：

| 旧标签 | 新标签 | 使用场景 |
|---|---|---|
| `not_started` | `not_started` | 未进入循环机制 |
| `in_progress` | `loop_running` | 正在执行微循环 |
| `partial` | `partial` | 部分通过、部分未通过 |
| `blocked` | `blocked` | 存在阻塞且无解 |
| `pass_with_runtime_blockers` | `evidence_ready` | 本轮 evidence 齐全 |
| - | `audit_ready` | 审计完成，待 Harness 判定（新） |
| `ready_for_human_acceptance` | `harness_review` | 等待人工确认 |
| `accepted` | `accepted` | 人工确认通过 |
| `complete` | `integrated` | 小即跨项目收口完成（仅限项目级） |

**迁移规则**：现有智能体的状态标签应立即切换。当前处于 `partial` 的智能体（宪衡、链同、厂行、知源）保持 `partial`；处于 `in_progress` 的（小即、数枢、灵策）切换为 `loop_running`。

---

## 4. 智能体工作流：从"专项执行版包"到 Loop Round

### 4.1 旧工作流（专项执行版包）

```
专项回报 → 只读预检 → 实施准入 → 追踪表 → 交付判定 → 验证清单 → 状态申请
```

### 4.2 新工作流（Loop Round 五段式）

```
输入 → 动作 → 输出 → 检查 → 反馈
  │      │      │      │      │
  │      │      │      │      └── 更新 loop-state.md
  │      │      │      └── 自检/评衡评分/证验验证
  │      │      └── loop-round-{ID}.md + diff + command log
  │      └── 文件变更（新增/修改/删除）
  └── 来自上一轮反馈或总控分派
```

### 4.3 专项执行版包与新工作流的融合

旧版包是"设计-实现追踪的静态文件"，新版工作流是"动态循环的运行机制"。融合方式：

| 专项执行版包字段 | Loop Round 对应段 | 说明 |
|---|---|---|
| 当前基线 | `loop-round-{ID}.md` 第1节"输入" | 基线信息从 loop-state.md 读取 |
| 实施准入检查表 | `loop-round-{ID}.md` 第1节"入口条件" | 准入判断前置到输入段 |
| 设计-实现追踪表 | `loop-round-{ID}.md` 第2节"动作" | 动作段记录文件变更 |
| 交付物完成判定表 | `loop-round-{ID}.md` 第3节"输出" | 输出段记录产物清单 |
| 测试与验证清单 | `loop-round-{ID}.md` 第4节"检查" | 检查段记录自查结果 |
| 状态升级申请表 | `loop-round-{ID}.md` 第5节"反馈" | 反馈段提出状态建议 |

---

## 5. 五项目试点期的智能体调度

### 5.1 试点项目与智能体对应

> **v1.1 更新**：试点项目 MMC/KDS/Brain/PKC/GFIS 已纳入 [12个交付包责任分解表](GlobalCloud智能体团队12个交付包责任分解表.md) 作为正式交付包，对应关系从"借用"升级为"正式绑定"；GFIS 试点由厂行牵头。

| 试点项目 | 代号 | 牵头智能体 | 协同智能体 | 审计智能体 |
|---|---|---|---|---|
| MMC | MM | 宪衡 | 链同 | 评衡、证验 |
| KDS | KD | 数枢 | 知源、灵策 | 评衡、证验 |
| Brain | BR | 灵策 | 知源、数枢 | 评衡、证验 |
| PKC | PK | 链同 | 灵策 | 评衡、证验 |
| GFIS | GF | 厂行 | 数枢、接稳 | 评衡、证验 |
| XiaoG | XG | 接稳 | 厂行 | 证验 |（非试点，预激活准备）

### 5.2 试点期智能体执行优先级

| 优先级 | 智能体 | 状态 | 试点期任务 |
|---|---|---|---|
| P0 | 小即 | 集成层 | 总控协调、启动 P1 初始化、验证 GPCF 汇聚 |
| P0 | 评衡 | 审计层 | 就绪待命中循环审计 |
| P0 | 证验 | 审计层 | 就绪待命中循环审计 |
| P1 | 宪衡 | 执行层 | MMC 模板基线、证据制度化 |
| P1 | 数枢 | 执行层 | KDS 数据指标、evidence 结构化 |
| P1 | 灵策 | 执行层 | Brain 知识UI闭环、KDS↔Brain 联邦 |
| P1 | 链同 | 执行层 | PKC 用户闭环、状态同步接口 |
| P1 | 厂行 | 执行层 | GFIS 工厂主链试点、工单/质量/库存闭环 |
| P2 | 知源 | 执行层 | 协同 KDS 知识主存 evidence |
| P2 | 接稳 | 执行层 | XiaoG ESP32 接入规范预研、连接可靠性基线 |
| P3 | 仓图 | 执行层 | 等待推广阶段再激活 |

### 5.3 未激活智能体的处理

仓图在当前试点期内保持 `not_started`，接稳已进入 XiaoG 预激活准备（P2），但必须：
1. 补齐本域的 `PROJECT_HARNESS_MANIFEST.md`（如尚未补齐）
2. 准备本域的首轮输入材料
3. 在推广阶段（P5）作为第二批激活
4. 接稳额外要求：产出 XiaoG ESP32 接入规范首版、WebSocket 可靠性基线文档

---

## 6. 智能体 Loop 周报增强

在现有控制塔与周报机制基础上，每个智能体的周报增加以下 Loop 字段：

### 6.1 执行智能体周报新增字段

| 新增字段 | 来源 |
|---|---|
| 当前 Round ID | `loop-state.md` |
| 本周完成轮次 | `loops/` 目录 |
| 本轮 evidence 完整率 | `evidence-index.md` |
| 本轮阻塞项 | `loop-state.md` blockers |
| 本轮门禁结果 | `loop-state.md` gate_result |
| 是否需要中循环审计 | 累计 ≥3 轮时标记 |

### 6.2 审计智能体周报新增字段

| 新增字段 | 来源 |
|---|---|
| 审计覆盖项目数 | `status-audit-*.md` |
| 审计通过率 | 审计结论汇总 |
| 证据缺口清单 | `evidence-index.md` 差异 |
| 状态越权检测结果 | 自动化检查输出 |

### 6.3 小即周报新增字段

| 新增字段 | 来源 |
|---|---|
| 试点项目状态矩阵 | `09-status/gpcf-project-status-matrix.md` |
| GPCF 汇聚 evidence 总数 | `08-evidence-samples/evidence-index.md` |
| 跨项目阻塞汇总 | 各项目 `blockers.md` |
| 整体 Loop 健康度 | 红黄绿指标汇总 |

---

## 7. 显性智能体名录 Loop 字段补充

现有名录 `GlobalCloud智能体团队显性智能体名录与可见机制.md` 增加以下列：

| 新增列 | 含义 | 示例 |
|---|---|---|
| Loop 角色 | 执行/审计/集成 | 执行层 |
| 当前 Round ID | 最近的 loop-round 编号 | GPCF-MM-LR-001 |
| evidence 完整率 | 当前证据完整率 | 85% |
| 阻塞登记 | 阻塞项是否已登记 | 是/否 |

---

## 8. 改进后的智能体执行铁律

以下规则覆盖全部 11 个智能体，不得例外：

1. **不产 evidence = 不算完成**。任何一轮推进，没有 `loop-round-{ID}.md` + diff + command log，不视为有效推进。
2. **状态升级必须经 Harness 判定**。执行智能体不得自行将状态标记为 `accepted` 或 `integrated`。
3. **每 3 轮触发中循环审计**。累计 3 轮微循环后，必须由评衡+证验完成审计才能继续。
4. **阻塞项必须登记**。任何阻塞必须在 `loop-state.md` 和 `blockers.md` 中显式记录。
5. **不得绕过小即做跨项目收口**。跨项目状态变更、统一命名、版本冻结均须经小即确认。
6. **AI 建议不得直接写入业务事实**。遵循 SUGG → WAES → 业务确认链路。

---

## 9. 版本记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.0 | 初始发布：智能体 Loop 角色映射、evidence 责任清单、状态标签迁移、工作流融合、五项目试点调度、周报增强、执行铁律 |
| 2026-06-12 | v1.1 | 试点项目交付包正式化：MMC/Brain/PKC 从"借用"升级为正式绑定，XiaoG 纳入预激活调度，接稳从 P3 升至 P2 |
| 2026-06-12 | v1.2 | 试点扩展至五项目：新增 GFIS（厂行牵头），厂行从 P3 升至 P1 |
