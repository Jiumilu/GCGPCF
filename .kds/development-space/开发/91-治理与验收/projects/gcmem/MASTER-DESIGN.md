---
doc_id: GPCF-DOC-2252D3D171
title: GCMEM 总体设计（v1.0 · 2026-10-16）
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gcmem/MASTER-DESIGN.md
source_path: projects/gcmem/MASTER-DESIGN.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# GCMEM 总体设计（v1.0 · 2026-10-16）

## 1. 背景

mem0（云记忆）于 2026-10-16 因配额耗尽与数据主权考量退役。跨会话长期记忆需要**本地、单一主存、可审计、可自动迭代**的承载；KDS 已是知识事实主存、gbrain 已提供语义检索——长期记忆并入同一体系，不另立系统。

## 2. 定位

GCMEM ＝ 基于 KDS 的长期记忆服务：跨会话记忆的**唯一主存与迭代通道**。

## 3. 架构（四层一体）

| 层 | 载体 | 说明 |
|---|---|---|
| 记忆主存 | `KDS/_meta/hermes-memory-log.md` | append-only 账本；类型 fact / decision / correction / preference / entity |
| 语义检索 | gbrain（KDS 索引） | 定向 `import _meta --no-embed --include-gitignored` + `embed --stale`（≈3 秒） |
| 服务接口 | `~/.hermes/scripts/gcmem.py` | `add` / `search` / `sync` / `stats` / `candidates` / `import-candidates` |
| 自动迭代 | 夜间对话挖掘（23:00） | 当日对话 → 高置信记忆自动入账（≤8条/日、去重）→ 报告留存全量候选供人工/agent 复核 |

## 4. 数据流

对话（Hermes 全部会话，含小G 通道）→ 夜间挖掘 → 记忆提炼 → 账本（+来源标注）→ gbrain 索引 → 检索注入（会话 / 小G / 周报指标）

## 5. 迭代机制

1. **每夜**：挖掘提炼 → 自动入账（高置信：明确决策/纠正/偏好句式；去重、限量）→ 定向同步索引。
2. **每周**：体系进化周报统计「KDS 记忆条目数」。
3. **人工**：老卢或 agent 随时 `gcmem add` 补录、`import-candidates` 复核导入。

## 6. 验收与指标

- 检索可用：`gcmem search` 命中账本条目（2026-10-16 首验 0.91 ✓）。
- 自动迭代：连续 3 日挖掘产出 ≥1 条有效记忆（待验）。
- 索引时效：账本写入后 24h 内可被 gbrain 检索（由 sync 保证）。

## 7. 边界与风险

- 不建立第二套记忆主账；mem0 / cognee / local-jsonl 旧栈均为退役或降级对象（容器侧见 §9）。
- 记忆条目为 working 级，不改变业务事实与状态；噪声风险由去重、置信过滤与人工复核控制。

## 8. 与既有件关系

- **继承**：KDS 记忆迭代首版（账本＋脚本，2026-10-16）；Hermes 技能库 `hermes-agent → references/multi-session-contention.md`。
- **替代**：mem0（云记忆，已卸载）。
- **关联**：GKE-001 知识工程 —— 长期记忆条目受其上位规范约束，不得建立平行记忆主账。

## 9. 小G 记忆迁移（进行中）

容器侧 `xiaoji_memory_backend.py` / `xiaoji_mem0_memory.py` / `xiaoji_memory_patrol.py` 现依赖 mem0_local / cognee 旧栈。迁移目标：记忆读写走 GCMEM（账本＋gbrain）。迁移步骤与验收另行登记；迁移完成前不得声明小G 长期记忆已切换。
