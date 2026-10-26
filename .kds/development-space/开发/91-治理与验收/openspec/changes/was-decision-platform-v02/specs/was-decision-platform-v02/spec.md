---
doc_id: GPCF-WAS-DECISION-PLATFORM-V02-SPEC-20261024
title: 能力规格 — WAS 决策能力平台 v0.2（was-decision-platform-v02）
project: WAS
related_projects: [WAS, WAES, WAME, GPCF, XWAIL]
domain: openspec
status: draft
version: v0.2
owner: WAS
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/was-decision-platform-v02/specs/was-decision-platform-v02/spec.md
source_path: openspec/changes/was-decision-platform-v02/specs/was-decision-platform-v02/spec.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/WAS世界资产体系总体方案.md
---

# 能力规格：WAS 决策能力平台 v0.2

本规格只登记能力要求与验收口径，不实现、不冻结 schema、不授权执行。

## ADDED Requirements

### Requirement: 治理登记与变更门禁

WAS 决策能力平台相关变更 SHALL 通过 GC 项目治理入口 `openspec/changes/was-<change>/` 登记，MUST 声明能力边界、跨仓影响矩阵、人工决策项、验收方式与回滚方式；MUST NOT 以文档登记替代平台获批或架构提升。

#### Scenario: 登记完备性
- **WHEN** 任一检查方读取本变更包
- **THEN** proposal/design/tasks/spec 四件齐备，影响矩阵覆盖 WAS/WAES/WAME/GPCF/XWAIL，四项人工决策逐条有形，且「非声明边界」段完整

#### Scenario: 未登记不得进入实现
- **WHEN** 任一实现任务缺少已登记的 Change 与 Feature 绑定
- **THEN** 该任务 MUST 被判定为 blocked，不得派发

### Requirement: WAS v0.2 契约冻结门

平台 MUST 在 WAS v0.2 八个最小契约对象（DecisionProfile、DecisionContextSnapshot、DecisionAssessment、DecisionRecord、AuthorizationRecord、ExecutionRecord、OutcomeRecord、FeedbackRecord）完成逐对象评审前，MUST NOT 进入实现或冻结 schema。

#### Scenario: 对象评审
- **WHEN** 评审八个契约对象
- **THEN** 每个对象具备目的、归属层、必需字段、不变量、状态机与非法转移、引用键与版本、证据要求、负例

#### Scenario: 顺序与状态冲突
- **WHEN** 冻结 `DecisionRecord` 或 `AuthorizationRecord`
- **THEN** 必须满足「先裁定后授权再执行」，且裁定/授权/执行/评估状态不得混写；存在 `authorizationRef` 顺序倒置或三世界归属冲突时 MUST 阻塞冻结

#### Scenario: 反馈不覆盖历史
- **WHEN** 反馈产生新版本
- **THEN** MUST 生成新版本/替代关系，MUST NOT 覆盖历史输入、历史推演或历史决策

### Requirement: 能力验收合同

pilot MUST 以可量化能力目标验收，MUST 包含决策问题、目标与约束、no-action 基线、候选行动、Outcome 时间窗、损失矩阵与人工复核成本、当前基线、晋级/停止/回滚条件；MUST NOT 以「增加模型」「一致率更高」等替代能力目标。

#### Scenario: pilot 合同齐备
- **WHEN** 评审首个 pilot（任务优先级建议，shadow + no-write）
- **THEN** 上述八项逐项有形，且 Outcome 使用实际延期、返工、完成质量

#### Scenario: 无合同不得验收
- **WHEN** 缺少 loss matrix 或 Outcome 时间窗
- **THEN** 任何「能力提升」结论 MUST 被拒绝

### Requirement: 独立金标与锁定评测集

评测 MUST 使用独立金标：两人独立盲标 + 第三人仲裁；MUST NOT 使用 StartLux/JEV 输出、预审标签、规则标签或已曝光样本作为 gold；开发集/校准集/锁定测试集/时间外测试集 MUST 隔离，并按项目、事件、时间分组防泄漏。

#### Scenario: 指标覆盖
- **WHEN** 评测结果发布
- **THEN** MUST 至少覆盖 FN/FP、Brier、ECE、risk-coverage、OOD、鲁棒性、期望损失、人工复核量

#### Scenario: 样本量门槛
- **WHEN** 声称红线初步安全评估完成
- **THEN** MUST 至少使用 300 个独立正例与 500 个高相似负例；50–100 条仅可用于 smoke test

### Requirement: 许可与商业边界

平台 MUST 按未来商业服务规划；StartLux 权重（CC BY-NC 4.0）MUST NOT 进入商业交付，商用 MUST 取得 StartLux Labs 书面授权或替换为可商用模型；MUST NOT 复制权重或推理正文到其它项目。

#### Scenario: pilot 能力模型
- **WHEN** 选定 pilot 能力模型
- **THEN** 必须通过许可审查，且不得依赖 CC BY-NC 权重证明能力

#### Scenario: 输出数据
- **WHEN** 模型输出进入商业交付
- **THEN** 必须给出输出数据许可与法务结论

### Requirement: 数据边界与远端外发

系统 MUST 默认禁止内部架构、代码、客户数据、凭据、未脱敏业务数据发送远端；仅脱敏后的合成/样例数据可用于评测；当前出境实现仅 L0，L1/L2 MUST 一律拒绝。

#### Scenario: 外发判定
- **WHEN** 任一调用准备把数据发往远端端点
- **THEN** 必须完成数据分级与三列判定（允许原样发 / 脱敏后发 / 禁止发），并登记端点

#### Scenario: 客户数据
- **WHEN** 数据包含客户数据
- **THEN** MUST 在出境评估完成前禁止入模

### Requirement: 失败态与 fail-closed

系统 MUST 统一枚举失败态（ok / unavailable / refusal / ood / missing_evidence / timeout / invalid_input / low_confidence / disputed / policy_blocked）；红线场景任一非 ok MUST fail-closed（stop + 人工）；`unavailable` MUST NOT 被当作放行。

#### Scenario: 本地影子不可用
- **WHEN** 本地模型闸口不可用
- **THEN** 结论 MUST 标记 `unavailable`，且不得引用远端结论冒充本地结论、不得放行

#### Scenario: 高风险输出留痕
- **WHEN** 输出涉及高风险判定
- **THEN** MUST 保留结构化证据与规则命中记录（输入摘要、模型版本、规则命中、置信度、时间戳、调用链）

### Requirement: 权限排除

模型与模型适配器 MUST NOT 取得裁定、授权、生产写入、状态提升、读取凭据、修改规则或自动扩权的权限；上述权限只属于人工/治理主体，并 MUST 保留审计与复核记录。

#### Scenario: 越权阻断
- **WHEN** 模型建议试图直接改变任务状态或触发生产写入
- **THEN** MUST 被阻断并记录越权事件

### Requirement: 工具链单一事实源与门禁诚实

StartLux 红线模板 MUST 与生产 `GATE_RULES` 单一事实源一致，并重建可校验基线；21 个仓的门禁代理路径错误 MUST 修复且与 GPCF 校验器同步；门禁结论 MUST 诚实：`gate=pass` 且 `status_ceiling=partial` MUST NOT 表述为 Green，MUST NOT 通过批量修改 `last_reviewed` 伪造复核。

#### Scenario: 漂移检测
- **WHEN** 模板注册表与生产规则不一致
- **THEN** 必须报错并阻断基线发布，而不是静默通过

#### Scenario: 代理修复
- **WHEN** 修复门禁代理路径
- **THEN** 修复后代理输出 MUST 与 GPCF 正本一致，且状态上限仍为 `partial`

### Requirement: 状态诚实与 No-Go 维持

本变更包与平台 MUST NOT 声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；MUST 保持 `No-Go / partial`，直到老卢确认的 Go 条件全部满足。

#### Scenario: 状态查询
- **WHEN** 任一检查方查询平台状态
- **THEN** 返回 `no_go_partial / draft`，不包含任何完成级声明

### Requirement: 跨仓任务包与执行隔离

跨仓任务 MUST 以完整字段任务包表达（含 target_branch、touches、acceptance、validation、cost/模型档位、验收/验证级别、worktree、resource_lock、reviewer、serial_integration_order、kill_switch、rollback）；No-Go 阶段所有任务 MUST 保持 `pending` 且 `blocked_by` 非空；`touches` MUST 互不重叠。

#### Scenario: 未 Go 不得开工
- **WHEN** No-Go 未解除
- **THEN** MUST NOT 创建 worktree/分支/锁，MUST NOT 派发实现 agent

#### Scenario: 执行隔离
- **WHEN** 任务获授权开工
- **THEN** 必须在独立 clean worktree、从正确基线、按锁与串行顺序执行，并可一键停止与回滚

### Requirement: 运行承接与资产边界

平台运行 MUST 由 WAME 承接治理运行时；WAES 资产 MUST 作为退役归档只读引用，MUST NOT 表述为复活，除非老卢明确批准并走 WAME 变更流程。

#### Scenario: WAES 引用
- **WHEN** 文档引用 WAES 资产
- **THEN** 必须标注退役状态与时点，且不得写入 WAES 仓
