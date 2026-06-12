---
doc_id: GPCF-DOC-DB96D52951
title: Loop Integration Policy
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/loop-integration-policy.md
source_path: .codex/skills/globalcloud-document-governance/references/loop-integration-policy.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Integration Policy

## 纳入点

文档治理嵌入 Loop Engineering 的三层循环：

| Loop 阶段 | 文档治理要求 |
|---|---|
| 微循环开始 | 明确输入文档、目标文档和本轮不处理范围 |
| 微循环结束 | 更新文档或登记文档债务，并同步 KDS 开发空间 |
| 中循环审计 | 检查受控、同步、真实性和污染风险 |
| 大循环收口 | 生成文档健康报告，作为状态升级证据 |

## 状态门禁

- 无文档记录：不得进入 `evidence_ready`。
- 有文档债务：最高 `partial`。
- KDS 同步失败：最高 `partial` 或 `blocked`。
- 污染检查失败：必须 `rework_required`。
- TOKEN 检查失败：必须 `blocked`。

## Evidence 要求

每轮 Loop 至少保留：

- 本轮输入文档列表
- 本轮输出文档列表
- 文档控制检查结果
- KDS 同步检查结果
- 污染检查结果
- 如有文档债务，必须列明 due_loop
