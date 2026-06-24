---
doc_id: GPCF-DOC-BRAIN-TEAM-AUTH-CONTRACT-DRIFT-20260624
title: Brain team 空间授权契约 C 口径确认证据 2026-06-24
project: Brain
related_projects: [GFIS, WAES, KDS, Brain, MMC]
domain: docs
status: controlled
version: v1.0
owner: Brain
kds_space: 开发
kds_path: 开发/06-Brain/docs/harness/Brain/evidence/brain-team-authorization-contract-drift-20260624.md
source_path: docs/harness/Brain/evidence/brain-team-authorization-contract-drift-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Brain team 空间授权契约 C 口径确认证据 2026-06-24

## 1. 证据定位

本文记录 Brain 浏览器证据刷新过程中发现的 `team` 空间授权契约漂移，以及用户确认后的 C 口径基线。

本文是授权口径确认证据，不声明 Brain 真实集成完成，不声明真实交付完成，不声明客户验收通过。

## 2. 当前事实

| 来源 | 当前事实 | 结论 |
|---|---|---|
| 当前 Chrome 页面观察 | `team` 空间显示 `总览 (team)`、`KDS API`、`totalPages=2709`、`graphNodes=132`、`graphEdges=192` | `team` 当前可读 KDS dashboard/graph |
| 当前 Chrome 搜索观察 | `team` 空间 Search 显示 `KDS GRAPH 浏览 team` 和 KDS graph 节点 | `team` 当前可读 KDS graph browse |
| 旧 `browser-runtime-smoke` validator | 期待 `team` Search/WikiPreview 为授权拒绝，且 `wikiPreviewSource` 为 `KDS 未授权` | 旧浏览器 smoke 契约仍按 team 未授权模型校验 |
| Brain loop-state / 历史证据 | 同时存在“team 未授权 no-mock 边界”和“七空间授权闭合”的历史描述 | 文档和运行证据之间存在口径漂移 |

## 3. 冲突判断

```text
brain_team_authorization_contract = confirmed_c_read_write_split
browser_runtime_smoke_status = pass_with_boundaries_after_c_alignment
current_chrome_visible_signals = confirmed
reason = user confirmed option C: team can read KDS dashboard/graph/search, while write, prompt, secret, and persistent operations remain authorization-controlled
```

确认 C 后，仍不能直接做两件事：

- 不能把 `browser-runtime-smoke` 通过扩展解释为 Brain 真实集成完成。
- 不能把 team 读权限扩展解释为写入、prompt、secret 或持久化操作授权。

## 4. 决策选项

| 选项 | 定义 | 后续动作 | 风险 |
|---|---|---|---|
| A | 确认 `team` 空间可读 KDS dashboard/graph/search 是新基线 | 更新 `browser-runtime-smoke`、read-closure、status-audit 和相关 evidence，将 team 从“拒绝态”改为“可读但仍受写入边界约束” | 需要同步所有旧 no-mock 授权拒绝描述，避免文档漂移 |
| B | 保持 `team` 空间应为未授权拒绝态 | 修复 Brain 当前运行或 MMC/KDS 授权配置，使 team Search/WikiPreview 回到拒绝态 | 可能影响当前多空间读取体验 |
| C | 区分读取和写入：`team` 可读 KDS graph/search，但写入、prompt、secret 和持久化操作继续受授权边界控制 | 更新 validator，把 read 权限和 write 权限拆开校验；保留 no-write/no-prompt 边界 | 需要重构多个 harness 断言，工作量比 A/B 稍大 |

## 5. 建议

用户已确认 C。

理由：

- 当前运行事实已经显示 `team` 可读 KDS dashboard/graph/search。
- team 空间可读 KDS dashboard/graph/search。
- 旧 validator 的“未授权拒绝”更像早期保护模型，不再完全匹配当前多空间读取能力。
- 对 Brain 这类知识工作台，读取能力和写入/LLM/secret 权限应分层治理：读可以扩展，写必须更严。

## 6. 用户确认结果

确认口径：

```text
C = team 空间可读，但写入、prompt、secret、持久化操作继续强授权控制
```

确认后，Brain 当前状态为：

```text
brain_team_authorization_contract = confirmed_c_read_write_split
browser_runtime_smoke_status = pass_with_boundaries_after_c_alignment
brain_integration_status = repair_required
```

说明：

- 已允许 Brain 将 `team` 的 KDS dashboard/graph/search 读取纳入只读授权边界。
- 写入、prompt、secret 和持久化操作继续受显式授权边界控制。
- `browser-runtime-smoke` 通过只代表浏览器只读 smoke 与 C 口径一致，不代表 `read-closure`、`status-audit`、`harness-evidence` 或整体集成闭合。
