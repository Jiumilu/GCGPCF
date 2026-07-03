---
doc_id: GPCF-DOC-04BF76145B
title: LOOP Execution Rules
project: WAES
related_projects: [WAES, GPCF]
domain: governance
status: controlled
version: v1.0
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
- output：严格遵守 `DO NOT send optional commentary`，只输出必要结论、阻塞项、授权确认请求、执行结果、验证证据和下一步必要动作。

## Output Boundary / 输出边界

整个项目群及 LOOP 正式运行输出必须遵守：

```text
DO NOT send optional commentary
```

可选过程性说明、无必要性的进度叙述、无证据支撑的解释性铺垫、情绪化说明、以及用 commentary 替代授权确认请求的表达，均不满足 LOOP 完成定义。需要用户授权或确认时，必须直接列出确认项并等待确认。

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
