---
doc_id: GPCF-DOC-6F5B2A27CF
title: GlobalCloud 智能体团队显性智能体名录与可见机制
project: XiaoC
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: agent-team
status: controlled
version: v1.0
owner: XiaoC
kds_space: 开发
kds_path: 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队显性智能体名录与可见机制.md
source_path: 05-agent-team/GlobalCloud智能体团队显性智能体名录与可见机制.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 智能体团队显性智能体名录与可见机制

日期：2026-06-12
状态：显性化执行补充版 v2
适用范围：GlobalCloud 绿色供应链体系小即智能体团队全部角色。

## 1. 显性化定义

“显性智能体”是指：

1. 有固定中文名字，不是角色别名。
2. 有固定主责/协同/审计边界。
3. 有固定回报入口和固定周报来源。
4. 每轮状态变化、主要困难、阻塞项都可在统一文档里追溯。
5. 未获会话或汇报确认前，不允许当作已执行状态给用户下结论。

## 2. 全量显性智能体名录

| 智能体 | 中文名字 | Loop角色 | 会话可见性 | 绑定交付包 | 当前Round ID | 当前会话状态 | evidence完整率 | 固定回报入口 |
|---|---|---|---|---|---|
| 总负责人 | 小即 | 集成层 | 已建固定主控会话 | 团队总控 | - | - | `in_progress` | [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) |
| 治理架构 | 宪衡 | 执行层 | 已建专项会话 | WAES 治理与控制塔包、MMC 管理配置中心包 | - | - | `partial` | [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) |
| 协同业务 | 链同 | 执行层 | 已建专项会话 | PVAOS 生态入口包、GPC 运营协同包、PKC 个人知识工作台包 | - | - | `partial` | [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) |
| 工厂执行 | 厂行 | 执行层 | 已建专项会话 | GFIS 工厂执行包、Edge 边缘接入包 | - | - | `partial` | [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) |
| 数据平台 | 数枢 | 执行层 | 已建专项会话 | AI 与数据底座包 | - | - | `in_progress` | [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) |
| 资源仓库 | 仓图 | 执行层 | 已建专项会话（待启动） | 资源仓库域、11 池映射、扩池能力 | - | - | `not_started` | [仓图专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/仓图专项会话状态报告.md) |
| 知识体系 | 知源 | 执行层 | 已建专项会话 | 企业级知识主存与知识引擎包 | - | - | `partial` | [GlobalCloud智能体团队专项回报汇总台账.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队专项回报汇总台账.md) |
| AI 服务 | 灵策 | 执行层 | 已建专项会话 | XiaoC（蚁后）+ Hermes/XGD（大象）+ XiaoG AI 服务包、Brain 智能知识平台包 | - | - | `in_progress` | [灵策专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策专项会话状态报告.md) |
| 连接器可靠性 | 接稳 | 执行层 | 已建专项会话（待启动） | XiaoG 本地语音助手包、连接器与可靠性（横向） | - | - | `not_started` | [接稳专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/接稳专项会话状态报告.md) |
| 评估审计 | 评衡 | 审计层 | 已建专项会话（待启动） | 全局审计与评分 | - | - | `not_started` | [评衡专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/评衡专项会话状态报告.md) |
| 证据验收 | 证验 | 审计层 | 已建专项会话（待启动） | 全局证据与验收 | - | - | `not_started` | [证验专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/证验专项会话状态报告.md) |

> 已建会话不代表可见合格。只有在状态更新、困难、阻塞和下一步均同步到台账后才视为显性成立。

## 3. 会话源和已知来源映射

| 智能体 | 来源会话 |
|---|---|
| 宪衡 | `019ea0b3-f7ab-74f3-b5c4-70da363bca54` |
| 链同 | `019ea0b3-f8e2-79b3-949f-8d7bcea39249` |
| 厂行 | `019ea0b3-fa29-78d0-84d9-dd6281d070a4` |
| 数枢 | `019ea0b3-fca9-7e61-9161-fac4c3cafd50` |
| 知源 | `019ea0b3-feac-7f51-8d58-f718c09ace6d` |
| 灵策 | `019e9fa8-9d1c-73c0-8fc5-b45571eb4e5d` |
| 仓图 | 已建（会话文件：仓图专项会话状态报告.md） |
| 接稳 | 已建（会话文件：接稳专项会话状态报告.md） |
| 评衡 | 已建（会话文件：评衡专项会话状态报告.md） |
| 证验 | 已建（会话文件：证验专项会话状态报告.md） |

## 4. 显性化汇报流程（统一）

1. 每个智能体必须每天至少更新“当前阻塞项/是否可继续”到小即台账。
2. 每周至少一次提交标准周报项：完成、进行中、下一步、困难、阻塞、需协调。
3. 任何状态升级前，必须先在总控会话形成可追溯证据与门禁判断，不得直接对外输出完成。
4. 若智能体未有固定会话，状态仅限于“待建”；小即必须优先补齐会话再纳入评分。

## 5. 显性化检查点

| 检查项 | 强制要求 |
|---|---|
| 名字是否固定中文 | 是 |
| 角色边界是否有文档 | 是 |
| 回报入口是否可见 | 是 |
| 会话 ID 是否可追溯 | 是 |
| 每轮阻塞项可追溯 | 是 |
| 是否有状态停留理由 | 是 |
| Loop 角色是否明确 | 是 |
| 当前 Round ID 是否可追溯 | 是 |
| evidence 完整率是否可查 | 是 |

## 6. 下一步建议

以下建议已按 Loop Engineering 全面改进方案（`05-agent-team/GlobalCloud智能体团队Loop Engineering全面改进方案.md`）更新：

1. 完成“仓图/接稳/评衡/证验/数枢/宪衡/灵策”的独立会话状态报表首轮同步，并逐步推进固定字段补齐。
2. 每个新会话形成首次状态提交，补齐到 `GlobalCloud智能体团队专项回报汇总台账.md`。
3. 小即在下一次“总控阶段报告”前再次核验“全量显性条目=11 行全部可见”。
