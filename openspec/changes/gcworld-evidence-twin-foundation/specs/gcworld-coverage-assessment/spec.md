---
doc_id: GPCF-DOC-GCWORLD-005
title: GCWORLD 覆盖评估规格
project: GPCF
related_projects: [KDS, WAES]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-coverage-assessment/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-coverage-assessment/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 只读来源清单评估
系统 SHALL 接受经过明确批准的本地 KDS 来源清单，并 SHALL 在不修改来源文件、KDS 元数据、KDS API 或业务系统的情况下进行评估。来源清单应覆盖会议纪要、合同、方案、报告、邮件、通讯记录、业务系统记录和项目资料。评估 SHALL 为每条被检查记录保存清单版本、确定性文件顺序、来源路径、来源哈希、扫描状态、提取版本、覆盖率和失败原因。

#### Scenario: 基于批准清单执行评估
- **WHEN** 操作人员使用经批准的本地清单执行覆盖评估
- **THEN** 评估仅生成本地派生证据产物，并报告来源文件修改数为零

### Requirement: 覆盖率与例外报告
系统 SHALL 生成可复核报告，包含来源扫描覆盖率、实体提及识别率、资产引用提取数、身份归一率、未决同名数量、重复候选数、孤立资产数、无证据关系数、时间冲突数、项目参与方覆盖率、智能体与组织职能绑定率、排除项和数据质量例外。每条例外 MUST 关联来源证据或明确的排除原因。

#### Scenario: 被提及组织缺少已归一资产
- **WHEN** 评估发现某个组织提及没有经过验证的权威资产链接
- **THEN** 报告将其列为未决引用并附来源位置，不得宣称组织覆盖完整

### Requirement: 未完成显式闭环不得宣称完整覆盖
除非清单中的每条记录均已关联到验证资产，或进入明确的例外与排除处置，并且最终闭环报告已获得人工批准，否则系统 MUST NOT 声称覆盖了全部人员或组织。

#### Scenario: 仍存在未决引用
- **WHEN** 评估报告中仍有未归一或未复核的身份引用
- **THEN** 报告状态为部分完成，并禁止给出完整覆盖声明

### Requirement: 每份来源完成五类对象提取处置
每份纳入清单的来源 SHALL 对实体、关系、事件、行动和承诺五类对象分别记录已提取、无此类内容、失败或待复核状态。系统 MUST NOT 仅因未识别到对象就将该类对象标记为不存在。

#### Scenario: 某合同未识别出承诺对象
- **WHEN** 自动提取未从合同中识别出承诺
- **THEN** 系统将承诺提取标记为待复核或明确无此类内容，不得把“尚未发现”当作“不存在”
