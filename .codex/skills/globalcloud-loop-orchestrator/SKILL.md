---
name: globalcloud-loop-orchestrator
description: GlobalCloud Loop 编排入口。用于用户说“启动 Loop”“继续 Loop”“Loop 托管运行”“进入下一轮”“自动选择技能”“生成下一轮输入”时，读取项目群状态，选择相关技能，执行文档、Git、质量、可用性、客户满意、依赖、风险回滚和自我进化门禁检查，并给出受控下一步。不会替代人工确认、不会自动 accepted/integrated、不会绕过 KDS TOKEN、Git、质量或 evidence 门禁。
---

# GlobalCloud Loop Orchestrator

本技能是 Loop 启动与续跑入口。它只做编排：读取状态、选择技能、执行门禁、生成下一轮建议；实际文档治理、开发执行、验收判定仍由对应技能负责。

## 使用时机

当用户要求以下任一事项时使用本技能：

- 启动 Loop、继续 Loop、进入下一轮、托管运行
- 根据 `loop-state` 或状态矩阵判断下一步
- 自动选择应加载的技能
- 生成微循环输入、阻塞清单或状态升级建议
- 对项目群 Loop 准备度做阶段判断

## 核心规则

- 启动 Loop 前必须读取：
  - `AGENTS.md`
  - `02-governance/loop/LOOP_CONTROL_BOARD.md`
  - `02-governance/loop/LOOP_AUTONOMY_POLICY.md`
  - 最近一轮 `docs/harness/loops/loop-round-*.md`
  - 当前项目状态矩阵与 Git 状态
- 按需加载技能，不一次性加载全部技能。
- 不在无 evidence 时升级状态。
- 不自动标记 `accepted` 或 `integrated`。
- KDS TOKEN blocked 时，Loop 状态最高为 `blocked`。
- Git dirty、未提交、未推送或敏感文件未处理时，按 Git 门禁限制状态升级。
- 质量、可用性、客户满意、依赖、风险回滚、自我进化任一门禁 blocked 时，不得升级状态。
- 文档债务存在时，状态最高为 `partial`。
- GPCF 总控仓自身也必须参与 Loop，不是免审计例外。

## 编排流程

1. 读取当前项目群状态：
   - `AGENTS.md`
   - `02-governance/loop/LOOP_CONTROL_BOARD.md`
   - `02-governance/loop/LOOP_AUTONOMY_POLICY.md`
   - `09-status/gpcf-project-status-matrix.md`
   - `09-status/globalcloud-document-health-report.md`
   - 如存在项目仓 `docs/harness/loop-state.md`，一并读取。
2. 运行脚本获得建议：
   ```bash
   python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_orchestrator.py
   ```
   需要单独检查 Git 门禁时运行：
   ```bash
   python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_git_gate.py .
   ```
   需要检查完整运行门禁时运行：
   ```bash
   python3 .codex/skills/globalcloud-loop-orchestrator/scripts/loop_operational_gates.py .
   ```
3. 根据任务类型选择技能：

| 场景 | 技能 |
|---|---|
| 文档治理、KDS、污染、台账 | `globalcloud-document-governance` |
| 需求到实现到 evidence | `opsx-full-cycle` |
| 验收、状态裁决 | `globalcloud-harness-governance` |
| 多智能体并行开发 | `globalcloud-collaborative-dev` |
| 项目健康评估 | `software-project-assessment` |
| PDF/培训资料分析 | `pdf` |
| OpenSpec 变更 | `openspec-*` |

4. 生成本轮五段式微循环：
   ```text
   输入 → 动作 → 输出 → 检查 → 反馈
   ```
5. 把反馈转成下一轮候选输入，但只作为建议，不自动越权执行。

## 阶段门禁

需要判断状态升级、托管运行边界或停止条件时，读取：

- `references/stage-gates.md`
- `references/git-version-gates.md`
- `references/quality-gates.md`
- `references/usability-gates.md`
- `references/customer-satisfaction-gates.md`
- `references/dependency-gates.md`
- `references/risk-rollback-gates.md`
- `references/evolution-gates.md`

## 托管运行边界

托管模式必须声明：

- 范围：项目或项目集合
- 目标：最多推进到哪个状态
- 权限：是否允许改文件、提交、推送
- 停止条件：TOKEN、测试失败、跨项目冲突、人工确认点等

默认权限：允许读取和生成建议；只有用户明确授权时才修改文件。默认不提交、不推送、不发布。

若用户明确授权“自动提交并推送”，仍必须先通过 Git 敏感文件检查；`.env`、TOKEN、密钥、证书文件不得自动提交。

## L3 托管冲刺模式

只有当用户明确说“启动 Loop L3 托管冲刺模式”时，才进入 L3。

L3 规则：

- 最多连续推进 15 轮或 2 小时，以先到者为准。
- L3 启动后默认持续推进；未完成 15 轮、未满 2 小时、未触发硬停止、未收到用户暂停/停止、且任务队列不为空时，必须进入下一轮。
- 阶段性汇报、完成单轮、完成两轮、完成一个小任务或生成下一轮建议，都不是 L3 停止条件。
- 每轮结束必须报告 `L3 session`、已完成轮次、剩余轮次、已用时间、停止类型、停止证据和下一轮。
- 可自动执行文档治理、受控文档新增/修订、本地小范围代码修改、mock、dry-run、测试、校验脚本、evidence 归档和下一轮计划生成。
- 本地 commit 仅在用户明确允许、Git 状态清晰、变更范围受控且无敏感文件时允许。
- 禁止自动执行删除文件或大规模迁移、生产配置修改、真实 API 写入、真实 KDS TOKEN 写入、权限变更、部署、推送、合并主分支、`accepted` / `integrated` 状态升级、项目战略定位或架构主结论变更。
- 触发 P0 风险、测试无法局部修复、Git 冲突、密钥/TOKEN、生产写入、删除/迁移、业务判断或文档事实严重冲突时必须自动暂停。

## 连续运行默认继续原则

L3、L3.5、L4、L5 均属于连续运行模式。连续运行模式 active 后，阶段性汇报、完成单轮、完成两轮、完成一个局部任务、生成报告或生成下一轮建议，都不是停止条件。

连续运行模式未触发对应硬停止条件、未耗尽轮次/时间预算、任务队列或授权范围仍未闭合、且用户未明确暂停/停止时，必须继续下一轮。

每轮结束必须报告：

- `continuous session`：active / stopped。
- `continuous mode`：L3 / L3.5 / L4 / L5。
- 已完成轮次、剩余轮次、已用时间。
- 停止类型和停止证据。
- 是否符合停止规则。
- 未停止时的下一轮 Round ID 或任务。

## 高质量可用要求

每轮 Loop 结束时，至少需要说明：

- 本轮 Definition of Done 是否满足。
- 用户/客户是否可以真实使用或复现。
- 客户满意度反馈是否收集，若未收集需登记原因。
- 跨项目依赖是否明确且无未登记阻塞。
- 是否具备回滚或撤销方案。
- 本轮经验是否转化为下一轮约束、模板或技能改进建议。
