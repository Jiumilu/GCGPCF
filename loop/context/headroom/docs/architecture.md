---
doc_id: GPCF-DOC-8749FB9903
title: Headroom LCX 架构说明
project: WAES
related_projects: [WAES, KDS]
domain: general
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/loop/context/headroom/docs/architecture.md
source_path: loop/context/headroom/docs/architecture.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX 架构说明

Headroom LCX 位于 Agent Runtime 与 LLM provider 之间，是上下文优化层，不是事实层、治理层或验收层。

```text
KDS      -> 知识事实主存与受控镜像
WAES     -> 授权、风险、门禁和裁决
Harness  -> 执行、证据、回放、指标和验收准备
Loop     -> 微循环、中循环和大循环编排
LCX      -> 压缩、恢复、成本观测、候选工作记忆
Agents   -> Codex、Claude、Cursor、LiteLLM、LangChain、项目自研运行体
```

## 数据流

```text
tool output / log / RAG chunk / file / conversation
  -> WAES sensitive check
  -> LCX compress or passthrough
  -> Harness evidence
  -> LLM provider
  -> optional CCR retrieve request
  -> WAES retrieve gate
  -> Harness retrieve evidence
```

## 非声明

- LCX 输出不是 KDS 正式事实。
- LCX memory 不是业务事实。
- LCX evidence 不能替代原始 source path、doc_id、validator output 或 Harness evidence。
- LCX dry-run 通过不等于 accepted、integrated 或 production_ready。
