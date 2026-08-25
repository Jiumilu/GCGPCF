---
doc_id: GPCF-DOC-GCWORLD-045
title: GCWORLD与KDS权威事实集成能力规格
project: GPCF
related_projects: [KDS, WAS, WAES, XWAIL]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-kds-authoritative-integration/specs/gcworld-kds-authoritative-integration/spec.md
source_path: openspec/changes/gcworld-kds-authoritative-integration/specs/gcworld-kds-authoritative-integration/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: KDS保持权威事实主存
系统 SHALL 仅从经过确认的KDS事实和证据生成GCWORLD投影，MUST NOT 将GCWORLD投影、缓存、索引、候选或模拟分支作为与KDS并列的事实主账。

#### Scenario: 投影与KDS事实冲突
- **WHEN** GCWORLD投影内容与绑定版本的KDS正式事实不一致
- **THEN** 系统以KDS事实为准，标记投影失效并阻断该投影参与真实行动

### Requirement: 集成批次绑定准入快照
每个集成批次 SHALL 记录KDS提交、远端关系、工作树摘要、F‑013准入结果、授权摘要、来源分级、本体版本、投影版本和有效期。任一必要状态未知、过期或冲突时 MUST 拒绝打开正文或执行集成。

#### Scenario: KDS工作树在准入后发生变化
- **WHEN** 批次执行前发现KDS工作树摘要与批准快照不同
- **THEN** 系统使批次失效并要求重新执行准入，不沿用旧授权继续读取

### Requirement: 候选身份和关系由人工复核
系统 SHALL 将未决身份、重复候选、关系争议和S3例外保存在独立队列中，MUST NOT 根据名称、相似度或智能体判断自动合并权威资产。S3记录只能保存不透明标识和受控指针。

#### Scenario: 两个来源出现同名人员
- **WHEN** 自动评估认为两个同名提及可能属于同一人员但缺少权威证据
- **THEN** 系统保留两个候选及各自来源并进入人工复核，不生成正式合并

### Requirement: 事实提升使用受控请求
任何从GCWORLD候选向KDS事实的提升 SHALL 使用包含命令标识、幂等键、预期事实版本、证据摘要、WAES裁决和人工确认的受控请求。GCWORLD MUST NOT 直接修改KDS存储。

#### Scenario: 提升请求缺少人工确认
- **WHEN** 候选具有充分证据但缺少规定的人工确认
- **THEN** 系统保持候选状态，不调用KDS写入接口并记录阻断原因

### Requirement: 写入回执与双向对账
KDS责任系统执行受控写入后 SHALL 返回不可变回执，记录实际版本、结果、错误、证据和责任主体；GCWORLD MUST 通过重新读取KDS确认事实后才能更新投影。

#### Scenario: KDS返回成功但重新读取不一致
- **WHEN** 写入接口返回成功而后续KDS读取未出现预期事实版本
- **THEN** 系统将批次标记为对账失败，冻结投影提升并启动人工调查或补偿

### Requirement: 独立授权先于实施
在Release、Feature、目标仓库、责任人、接口范围、凭据、数据范围、回滚和Harness门禁获得独立批准前，系统 MUST 将本能力保持为规划状态，禁止实施、部署和状态提升。

#### Scenario: OpenSpec规划产物全部完成
- **WHEN** 本变更的提案、设计、规格和任务均通过结构校验但独立授权尚未签发
- **THEN** 系统只记录规划就绪，不开始KDS集成实现，也不改变F‑013或GCWORLD状态

