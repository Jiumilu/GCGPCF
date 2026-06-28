---
doc_id: GPCF-DOC-04BF76145B
title: LOOP Execution Rules
project: WAES
related_projects: [WAES]
domain: governance
status: controlled
version: v1.0
doc_schema_version: v1.0
policy_version: v1.1
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_EXECUTION_RULES.md
source_path: 02-governance/loop/LOOP_EXECUTION_RULES.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Execution Rules

## Definition of Done / 完成定义

每轮 LOOP 的完成定义不是“生成了文档”，而是满足以下最小条件：

- run：本轮目标、输入、范围和授权边界已明确。
- stop：硬停止条件已检查，未越过人工确认、生产写入、真实 API、schema migrate、deploy、commit/push 授权边界。
- verify：本轮修改有本地命令、validator、diff-check 或等价证据。
- recover：失败或暂停时可回到上一个安全状态。
- debug：当前阻塞、下一步和需要人工确认的问题已登记。

## v1.1 Delivery Default

开发态默认 Delivery Loop。普通本地开发不要求完整展开治理审计，只需保留当前切片的目标、变更、验证、风险和下一步。Governance Loop 只在 guarded、blocked、状态提升、生产动作、阶段收口或 P0/P1 风险触发时进入。

Delivery Loop 不强制展开 `run / stop / verify / recover / debug`。Delivery Loop 只使用以下 5 字段：

```text
goal / changed / verified / risk / next
```

Delivery Loop 的 `risk` 字段必须显式声明是否触发 P0/P1。一旦触发 P0/P1，或进入 guarded、blocked、状态提升、生产动作、阶段收口，必须停止 Delivery Loop 并切换到 Governance Loop。

Governance Loop 才强制展开：

```text
run / stop / verify / recover / debug
```

边界：

```text
accepted = false
integrated = false
production_ready = false
customer_accepted = false
real_business_lane=repair_required
runtime_primary_key_ready=0
review_queue=0
runtime_intake=0
waes_review=0
verified=0
```
