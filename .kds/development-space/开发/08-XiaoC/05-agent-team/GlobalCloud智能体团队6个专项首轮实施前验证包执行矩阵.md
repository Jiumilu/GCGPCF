---
doc_id: GPCF-DOC-B66EC338E9
title: GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵
project: XiaoC
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, XiaoG]
domain: agent-team
status: controlled
version: v1.0
owner: XiaoC
kds_space: 开发
kds_path: 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵.md
source_path: 05-agent-team/GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵

日期：2026-06-08
状态：专项验证包执行矩阵 v1
用途：把固定 10 个专项在首轮实施前验证阶段的环境、工具、技能、方法、效率要求、成本上限、证据清单和状态上限统一固定下来。

## 1. 使用口径

1. 本矩阵只适用于“首轮实施前验证准备”阶段。
2. 本矩阵建立在 6 个先导专项正式只读预检已完成，4 个侧线会话已建但尚未全部启动的前提上。
3. 本矩阵不用于联调完成、试运行完成或生产完成判定。
4. 所有专项同时受环境门、工具门、过程门、证据门和状态门约束。

## 2. 10 个专项执行矩阵

| 专项 | 当前阶段 | 当前目标 | 主责成员 | 工作环境 | 推荐工具 | 推荐技能 | 推荐方法 | 效率要求 | 成本上限 | 证据清单 | 状态上限 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 宪衡 / WAES | 首轮实施前验证准备 | 抽取治理对象、证据对象、授权对象和连接器治理样本要求 | 宪衡 | 项目仓库环境 + 设计控制环境 | Shell、Git、文档工具 | `globalcloud-harness-governance` | 治理对象落点法、证据样本设计法 | 中速、高准确性 | 中等 token；禁止大面积翻仓 | `EvidenceRecord` 样本要求、`StatusAudit` 样本要求、`AgentToolGrant` 样本要求、连接器治理样本要求 | `partial` |
| 链同 / PVAOS + GPC | 首轮实施前验证准备 | 收敛协同主链运行前样本要求，区分 PVAOS 入口事实和 GPC 原型样本 | 链同 | 项目仓库环境 + 设计控制环境 | Shell、Git、文档工具 | `repo branch gate`, `globalcloud-harness-governance` | 协同主链样本法、原型-目标边界法 | 高效率、强证据化 | 低到中等 token | 组织/项目/伙伴入口样本、订单/ASN/预约/运输/POD 样本要求、GPC 缺口清单 | `partial` |
| 厂行 / GFIS + Edge | 首轮实施前验证准备 | 收敛工厂主链回执、LES/EAM 样本、Edge 事实转换样本要求 | 厂行 | 项目仓库环境 + 设计控制环境 | Shell、Git、文档工具 | `repo branch gate`, `globalcloud-harness-governance` | 工厂主链样本法、联合预检法 | 高效率、低返工 | 低到中等 token | 工单样本、质量样本、库存样本、发货回执样本、LES/EAM 样本要求、Edge 转换与回执样本要求 | `partial` |
| 数枢 / AI 与数据底座 | 首轮实施前验证准备 | 收敛数据库权限、读模型只读、DLQ/Replay、Trace/Evidence 样本要求 | 数枢 | 项目仓库环境 + 设计控制环境 | Shell、Git、文档工具 | `globalcloud-harness-governance` | 边界样本法、异常回放样本法 | 中速、高结构化 | 中等 token | 数据库权限样本要求、读模型只读样本要求、DLQ/Replay 样本要求、Trace/Evidence 回指样本要求 | `partial` |
| 灵策 / Brain（知源协同） | 首轮实施前验证准备 | 关闭 Brain remote 缺口，收敛 ingest / 引用回指 / 失效拦截样本要求 | 灵策（知源协同） | 项目仓库环境 + 设计控制环境 | Shell、Git、文档工具 | `globalcloud-harness-governance` | 知识治理样本法、引用回指样本法 | 中速、证据优先 | 中等 token | remote 证据、ingest 样本要求、引用回指样本要求、失效拦截样本要求 | `partial` |
| 灵策 / XiaoC（蚁后）+ Hermes/XGD（大象）+ XiaoG | 首轮实施前验证准备 | AI 服务域运行前样本化：AgentToolGrant、AISuggestion、`ai.overreach.blocked`、主账无变化样本 | 灵策 | 项目仓库环境 + 本地运行环境 + 设计控制环境 | Shell、Git、Browser、Computer Use、文档工具 | `computer-use:computer-use`, `browser:control-in-app-browser`, `globalcloud-harness-governance` | 反向验证法、权限样本法、回执样本法 | 低速但高确定性 | 时间成本高于 token 成本 | AI 服务闭环样本要求 | `partial` |
| 评衡 / XiaoC（蚁后）+ Hermes/XGD（大象）+ XiaoG | 首轮实施前验证准备 | 评估口径、评分闭环、阻塞与偏差闭环样本化 | 评衡 | 项目仓库环境 + 设计控制环境 | Shell、Git、文档工具 | `globalcloud-harness-governance` | 指标清单法、差距闭环法、签核前置法 | 中速 | 时间成本中等 | 运行样本驱动评分闭环与偏差追踪 | `not_started` |
| 证验 / XiaoC（蚁后）+ Hermes/XGD（大象）+ XiaoG | 首轮实施前验证准备 | A7/A9/A13/A19/A20 关键事件的证据分级与签核就绪检查 | 证验 | 项目仓库环境 + 设计控制环境 | Shell、文档工具 | `globalcloud-harness-governance` | 证据分层法、签核闭环法、状态门控法 | 中速 | 时间成本中等 | 证验看板与签核时间窗闭环要求 | `not_started` |
| 仓图 / 资源仓库 | 首轮实施前验证准备 | 11池对象映射、池边界、扩展机制执行样本化 | 仓图 | 设计控制环境 + 项目仓库环境 | Shell、文档工具 | `globalcloud-harness-governance` | 对象拆解法、规则样本法 | 中速 | 时间成本中等 | 池映射对象与扩展边界样本闭环 | `not_started` |
| 接稳 / 连接器可靠性 | 首轮实施前验证准备 | DLQ/Replay、补偿、降级恢复和连接器可观测闭环 | 接稳 | 项目仓库环境 + 设计控制环境 | Shell、文档工具 | `globalcloud-harness-governance` | 重试闭环法、恢复时效法 | 中速 | 时间成本中等 | DLQ/Replay 与连接器恢复闭环样本 | `not_started` |

## 3. 专项统一效率要求

### 3.1 必须高效率推进的项

1. 样本要求收敛
2. 仓库落点抽取
3. 台账更新

要求：

1. 优先复用现有只读预检结果
2. 优先复用既有文档与 shell 输出
3. 避免重复扫描整个仓库

### 3.2 必须慢一点但要准的项

1. 越权拦截样本设计
2. 主账无写入样本设计
3. 知识失效拦截样本设计
4. 数据库权限和读模型只读样本设计

要求：

1. 证据优先于速度
2. 不允许为了快而降低证据质量

## 4. 专项统一成本要求

### 4.1 token 成本控制

1. 每个专项验证包优先在既有只读预检基础上扩展，不重新做全量分析。
2. 优先局部落点抽取，不做整仓全文重写。

### 4.2 时间成本控制

1. 先形成样本要求，再做运行前验证。
2. 没有样本要求，不进入高成本运行验证。

### 4.3 返工成本控制

1. 禁止在样本未定义前直接进入 Browser 或 Computer Use 大量验证。
2. 禁止同一专项在未收口边界前反复改写验证包。

## 5. 专项统一证据要求

每个专项首轮实施前验证包都必须至少包含：

1. 当前目标
2. 当前边界
3. 当前工作环境
4. 当前推荐工具与技能
5. 样本要求清单
6. 阻塞清单
7. 下一步验证入口
8. 状态上限

## 6. 当前正式结论

当前下一步不再是抽象推进，而是按这张矩阵逐专项推动 10 个固定专项的“首轮实施前验证包”闭环（其中 4 个侧线会话目前偏向样本准备与启动前状态）。
