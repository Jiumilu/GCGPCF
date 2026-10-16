---
doc_id: GPCF-DOC-FCAE31EF6C
title: Design — was-flow-naming-migration
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/was-flow-naming-migration/design.md
source_path: openspec/changes/was-flow-naming-migration/design.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# Design — was-flow-naming-migration

## 决策记录

### D1 迁移执行策略：切净新名＋兼容窗口

- 契约本体（`was-flows.yaml`）与数据样例（examples）**切净至 V1.2 名**；旧名仅保留在「兼容定义」（`DEPRECATED_FLOWS`）与 schema 兼容枚举中，作为 deprecated 窗口，不阻断既有数据校验。
- 替代被否方案：①旧名长期双列并存（会拖延迁移、制造双主命名）——否；②一次性硬切（旧名直接报失败，会弄红他方在途数据）——否。
- 兼容窗口关闭条件：另行版本发布；关闭时旧名报失败（届时另案）。

### D2 校验器语义精准化（gfis profile）

- 原断言：「stages 覆盖全部 8 流」（旧世界里 12 个 stage 恰好覆盖旧 8 名）。
- 新世界问题：ValueFlow/CreditFlow 为 V1.2 新增流，本 profile（真实业务 12 阶段）**无对应实例**。
- 决定：`requiredFlows` 声明＝V1.2 全 8（框架声明，保持）；stage 覆盖断言＝**核心 6 流**（`CORE_FLOWS <= flows`）；Value/Credit **不编造实例**，如实记录。
- 被否方案：新增 S13/S14 stage 凑数——否（编造业务数据）。

### D3 schema 枚举双列

- flow enum＝V1.2 名（8）在前＋旧名（8）在后；语义：新数据必须用 V1.2 名；旧名仅兼容窗口内可过。
- `was-pilot-scope.schema.json` 的 `const: rule_flow` 同步放宽为 `enum: [ControlFlow, rule_flow]`（与 validator 特判一致）。

### D4 特殊归位（spacetime）

- `spacetime_flow` 不设一对一：维度侧＝`SpaceTimeDimension`（既有）；运行侧＝场景流（候选，随版本发布纳入）。
- 存量数据按「主导语义就近归位」：gfis profile S11（Delivery and POD）→ `LogisticsFlow`。

### D5 范围纪律

- 只动命名层；八维/三层资产/状态分离不动；XWAIL 代码不动；GPCF fixtures 与 KDS 存量引用留后续批次（迁移表 §5 列清单）。

## 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 他方在途数据用旧名 | 兼容窗口（不阻断）；迁移表列存量清单 |
| 迁移被误读为「V1.2 完成」 | 迁移表与 evidence 明示 §19 纪律：迁移执行 ≠ V1.2 发布/运行完成 |
| 校验器更新被误读为放水 | 精准化理由（新增流无实例）如实入档；核心 6 流仍强制 |
