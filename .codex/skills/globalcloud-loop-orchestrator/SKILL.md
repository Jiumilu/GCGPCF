---
doc_id: GPCF-DOC-2D8E4755AF
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
- LOOP 运行控制闭环为所有 Loop 工作的默认工程接口，历史别名为 LOOP 五方向。
- Governance Loop 使用 `run / stop / verify / recover / debug`。
- Delivery Loop 使用 `goal / changed / verified / risk / next`。
- 开发态默认 Delivery Loop；只有 guarded、blocked、状态提升、生产动作、阶段收口或触发 P0/P1 风险时才强制切换到 Governance Loop。
- `templates/loop-round-v2-five-direction.yaml` 仍是 Governance Loop 的标准模板；历史旧五段式 `输入 → 动作 → 输出 → 检查 → 反馈` 不得直接替代 Governance Loop 的 `run / stop / verify / recover / debug`。

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
   需要检查项目群 17 仓全量 Git clean 门禁时运行：
   ```bash
   python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py
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
| 项目群 17 仓 Git clean、全量 Git 收口、Loop Git clean 门禁 | `globalcloud-project-group-git-clean` |
| 项目健康评估 | `software-project-assessment` |
| UI 质量、产品界面、控制塔、工作台、证据页、异常页、AI 对话页、移动端/桌面端界面门禁 | `globalcloud-ui-quality-gate` |
| PDF/培训资料分析 | `pdf` |
| OpenSpec 变更 | `openspec-*` |

4. 根据当前模式生成本轮 LOOP 运行控制闭环：
   - Delivery Loop：
     ```text
     goal → changed → verified → risk → next
     ```
   - Governance Loop：
     ```text
     run → stop → verify → recover → debug
     ```
   Delivery Loop 只用于开发态；Governance Loop 只用于 guarded、blocked、状态提升、生产动作、阶段收口或 P0/P1 风险。
   对进入 Governance Loop 的轮次，仍必须按 `templates/loop-round-v2-five-direction.yaml` 覆盖 `run`、`stop`、`verify`、`recover`、`debug`，不得退回只记录“输入 → 动作 → 输出 → 检查 → 反馈”的旧五段式。
5. 把 `debug` 与 `recover` 的结论转成下一轮候选输入，但只作为建议，不自动越权执行。

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

若本轮涉及 UI、界面交互、控制塔、工作台、证据页、异常页、AI 对话页、移动端或桌面端展示，必须同时读取并执行：

- `.codex/skills/globalcloud-ui-quality-gate/SKILL.md`
- `.codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md`
- `.codex/skills/globalcloud-ui-quality-gate/references/quality-checklist.md`
- `.codex/skills/globalcloud-ui-quality-gate/references/evidence-output.md`

UI Quality Gate 的输出只作为 `ui_evidence_candidate`，不得替代 Harness/WAES/GPCF 状态判定。

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
- 每轮结束必须报告 LOOP 运行控制闭环结果：`run` 的输出、`stop` 的停止类型、`verify` 的门禁结果、`recover` 的恢复点、`debug` 的当前阻塞或下一授权。
- 可自动执行文档治理、受控文档新增/修订、本地小范围代码修改、mock、dry-run、测试、校验脚本、evidence 归档和下一轮计划生成。
- 本地 commit 仅在用户明确允许、Git 状态清晰、变更范围受控且无敏感文件时允许。
- 禁止自动执行删除文件或大规模迁移、生产配置修改、真实 API 写入、真实 KDS TOKEN 写入、权限变更、部署、推送、合并主分支、`accepted` / `integrated` 状态升级、项目战略定位或架构主结论变更。
- 触发 P0 风险、测试无法局部修复、Git 冲突、密钥/TOKEN、生产写入、删除/迁移、业务判断或文档事实严重冲突时必须自动暂停。

### L3 final answer guard

当 `L3 session` 为 `active` 且已完成轮次小于 15 时，最终收口回答只能在以下停止类型之一成立时发送：

- `hard_stop`
- `user_stop`
- `budget_exhausted`
- `time_exhausted`
- `task_queue_empty`
- `authorization_boundary`

若停止类型为 `none`，且下一轮存在，则不得把阶段性汇报、3 轮小结、5 轮小结、10 轮小结、单轮完成、局部任务完成或“下一轮建议”当成停止。此时只能发送进度更新，并必须继续下一轮。

L3 每轮结束前必须运行或等价检查：

```bash
python3 tools/kds-sync/validate_l3_continuation_guard.py
```

## 连续运行默认继续原则

L3、L3.5、L4、L5 均属于连续运行模式。连续运行模式 active 后，阶段性汇报、完成单轮、完成两轮、完成一个局部任务、生成报告或生成下一轮建议，都不是停止条件。

连续运行模式未触发对应硬停止条件、未耗尽轮次/时间预算、任务队列或授权范围仍未闭合、且用户未明确暂停/停止时，必须继续下一轮。

## 连续运行真实性门禁

L3、L3.5、L4、L5 的轮次预算只能按 `substantive_rounds` 计数，不能按文件数量、模板数量、脚本生成数量或声明轮次数计数。

每轮必须检查：

- 独立输入。
- 独立判断。
- 独立输出。
- 独立验证。
- 独立反馈。

至少满足 4/5 才能计为 `substantive_round=1`。同一脚本、同一时间窗口、同一模板批量生成多个 Round 文档时，整批默认最多计 1 个实质轮次。

若 `declared_rounds` 达到上限但 `substantive_rounds` 未达到上限，不得使用 `budget_exhausted` 收口；必须更正为 `authorization_boundary`，并说明继续推进需要真实任务队列、独立输入或更高授权。

连续运行 final answer 前必须运行或等价检查：

```bash
python3 tools/kds-sync/validate_continuous_round_substance.py
```

每轮结束必须报告：

- `continuous session`：active / stopped。
- `continuous mode`：L3 / L3.5 / L4 / L5。
- declared_rounds、substantive_rounds、generated_items、batch_generated、substance_gate。
- 剩余实质轮次、已用时间。
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
