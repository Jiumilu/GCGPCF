---
doc_id: GPCF-DOC-GCWORLD-021
title: GCWORLD 工程与治理规格
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, KWE, MMC, GFIS, Brain, Studio]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-engineering-governance/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-engineering-governance/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 七层数据分层
系统 SHALL 将数据划分为来源层、候选层、KDS 事实层、世界投影层、运行状态层、模拟分支层、证据与审计层。每条记录 MUST 标明所属层级、来源、生命周期和允许的提升路径；候选、运行状态和模拟数据不得伪装成正式事实。

#### Scenario: 会议纪要解析出新联系人
- **WHEN** 来源层的会议纪要解析出尚未确认的联系人
- **THEN** 该记录进入候选层并关联原始证据，不直接进入 KDS 事实层或正式世界投影

### Requirement: 世界投影可重建且不形成第二事实账本
世界投影 SHALL 由 KDS 正式事实、WAS 权威语义、规则版本和投影版本确定性生成，并可从这些输入完整重建。投影服务 MUST NOT 成为与 KDS 并列的第二事实账本；重建结果差异必须被检测、报告和阻断提升。

#### Scenario: 投影存储损坏后重建
- **WHEN** 运维人员从已确认事实和指定版本重新生成世界投影
- **THEN** 系统得到相同对象标识和语义结果，或输出可定位到输入与版本的差异报告

### Requirement: 存储职责按数据性质分工
系统 SHALL 按责任选择存储：KDS 保存事实与证据索引，图存储承载关系投影，关系型存储承载事务状态与授权对象，事件存储承载不可变事件和回执，对象存储承载原始材料，大模型检索索引承载可重建语义索引，缓存仅保存短期派生结果。任何缓存、索引或图投影丢失后必须可恢复，不得被视为权威事实源。

#### Scenario: 语义索引与 KDS 事实冲突
- **WHEN** 检索索引中的摘要与 KDS 当前正式事实不一致
- **THEN** 系统以 KDS 事实和有效版本为准，标记索引过期并触发重建，不使用旧摘要扩大权限或驱动真实动作

### Requirement: 统一标识与版本字段
每个世界对象 SHALL 使用稳定的 `worldAssetId`，并按对象类型记录 `sourceSystemId`、`sourceRecordId`、`tenantId`、`assetDimension`、`ontologyVersion`、`schemaVersion`、事实有效时间、系统记录时间和证据引用。标识合并或拆分 MUST 保留别名、前后映射和审计链。

#### Scenario: 两个候选组织被确认同一主体
- **WHEN** 人工依据证据批准身份合并
- **THEN** 系统保留原标识映射、批准记录和生效时间，并使历史引用仍可追溯

### Requirement: 领域接口与可靠事件
系统 SHALL 提供世界查询、上下文、身份、智能体、行动、模拟、治理和事件流接口。所有写命令与事件 MUST 携带 `commandId`、`idempotencyKey`、`eventId`、`causationId`、`correlationId` 和 `schemaVersion` 中适用的标识，并采用事务消息、收件去重、可控重试、死信和补偿机制保证可追溯的一致性。

#### Scenario: 外部系统重复提交同一行动命令
- **WHEN** 执行系统因网络重试再次提交相同 `idempotencyKey` 的命令
- **THEN** 行动运行时返回同一处理结果或当前状态，不重复产生业务副作用

### Requirement: 安全与秘密隔离
系统 SHALL 实施租户隔离、最小权限、运行身份、短期凭证、传输与静态加密、审计、防提示注入和连接器白名单。密码、令牌、私钥及其他秘密 MUST NOT 写入 KDS 正文、世界投影、智能体提示词、长期记忆或执行回执；只允许保存受控引用和必要的非敏感元数据。

#### Scenario: 来源文档包含访问令牌
- **WHEN** 采集器在来源文档中检测到疑似访问令牌
- **THEN** 系统隔离并遮蔽秘密，只记录安全事件和受控引用，不把明文传播到检索索引或智能体上下文

### Requirement: 可观测性与分阶段退出门禁
系统 SHALL 监测来源覆盖率、身份未决率、事实冲突率、投影延迟、快照构造时间、裁决延迟、动作成功与补偿率、越权阻断率、智能体候选采纳率和证据完整率。P0 至 P7 每一阶段 MUST 具有量化退出条件、风险复核和独立授权；前一阶段通过不得自动提升下一阶段权限。

#### Scenario: 只读运行时指标未达标
- **WHEN** P2 的投影一致性或证据完整率未达到批准阈值
- **THEN** 阶段状态保持返工或部分完成，不进入 P3 内部辅助智能体阶段

### Requirement: 四级验收状态与证据真实性
Harness SHALL 区分 `structural_compliance`、`validation_readiness`、`ready_for_human_acceptance` 和 `complete` 四级状态。只有独立验证证据和必要人工确认均满足时才能逐级提升；演示、桩件、固定样例、截图或仅文档声明 MUST NOT 单独作为完整运行证据，也不得自动标记 `complete`。

#### Scenario: 演示环境全部页面可访问
- **WHEN** GCWORLD 演示环境展示十二个工作中心但没有真实数据链和执行证据
- **THEN** Harness 最多记录结构或验证准备状态，不宣称已验收、已集成、生产就绪或完整运行
