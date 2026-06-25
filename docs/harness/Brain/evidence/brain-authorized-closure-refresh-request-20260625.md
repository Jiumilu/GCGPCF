---
doc_id: GPCF-DOC-BRAIN-AUTHORIZED-CLOSURE-REFRESH-REQUEST-20260625
title: Brain 授权型闭包证据刷新请求 2026-06-25
project: Brain
related_projects: [GPC, WAES, KDS, Brain, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: Brain
kds_space: 开发
kds_path: 开发/06-Brain/docs/harness/Brain/evidence/brain-authorized-closure-refresh-request-20260625.md
source_path: docs/harness/Brain/evidence/brain-authorized-closure-refresh-request-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Brain 授权型闭包证据刷新请求 2026-06-25

## 1. 请求定位

本文把 Brain 当前剩余的 `completion-matrix` 阻塞拆成可授权执行的真实证据刷新窗口。

当前状态：

```text
brain_authorized_closure_refresh = authorization_required
brain_completion_matrix = repair_required
brain_harness_evidence = repair_required
brain_loop_harness = repair_required
```

本文不是执行结果，不表示真实写入、真实 bulk-fix execution 或真实 LLM prompt 已执行。

## 2. 已完成前置证据

| 前置项 | 当前状态 |
|---|---|
| `npm run validate:runtime-health` | pass，`brain_status=200`，`kds_total_pages=2732` |
| `npm run validate:browser-runtime-smoke` | pass |
| `npm run validate:browser-user-flow` | pass |
| `npm run validate:read-closure-matrix` | pass，`read_closure_workflow_count=17` |
| `npm run validate:chinese-gates` | pass |
| `npm run format:check` | pass |

## 3. 待授权动作

| 编号 | 动作 | 目的 | 涉及真实能力 | 当前状态 |
|---|---|---|---|---|
| A1 | 刷新 `backend-write-closure-20260621.json` | 让 `projects.write` 和 `settings.save` 的当前写入闭包证据重新有效 | KDS 写入、更新、读回、redacted secret ack | `authorization_required` |
| A2 | 刷新 `bulk-fix-acceptance-execution` | 让 BulkFix confirm/execution/readback 证据重新有效 | KDS bulk-fix confirm 与 execution readback | `authorization_required` |
| A3 | 刷新 `chat-llm-prompt-20260621.json` | 让 ChatPanel 授权 prompt 证据重新有效 | MMC LLM connector 真实 prompt 调用 | `authorization_required` |

## 4. 授权范围

| allow | value |
|---|---|
| allowed_projects | Brain, KDS, MMC, GPCF |
| allowed_environment | local dev only |
| allowed_write_scope | Brain harness 专用测试对象与 evidence 文件 |
| allowed_prompt_scope | 一次低风险中文 prompt，用于验证 ChatPanel 真实 LLM 调用边界 |
| allowed_evidence_outputs | `backend-write-closure-20260621.json`、`bulk-fix-acceptance-readback-20260622.json`、`chat-llm-prompt-20260621.json`、派生 validator 输出 |
| allowed_status_after_success | `ready_for_review / authorization_boundary` |

## 5. 禁止范围

| forbid | value |
|---|---|
| production_write | true |
| permission_change | true |
| deployment | true |
| secret_plaintext_capture | true |
| customer_acceptance_claim | true |
| accepted_or_integrated_upgrade | true |
| broad_data_migration | true |
| external_customer_notification | true |

## 6. 执行前门禁

执行前必须满足：

- Brain dev server 明确启动并通过 `npm run validate:runtime-health`。
- KDS TOKEN 检查通过，但不得写入或展示真实 TOKEN。
- 所有写入仅限 harness 测试对象、测试配置或受控 evidence。
- LLM prompt 仅允许一次，必须记录 model、space、prompt 授权标签、response 非空和 token usage。
- 每个动作必须保留 readback 或 negative boundary，不允许只记录请求发送。

## 7. 用户确认语句

执行本授权窗口需要用户明确回复：

```text
我确认执行 Brain 授权型闭包证据刷新 2026-06-25，允许 A1、A2、A3 在 local dev 范围内执行。
```

如果只授权部分动作，需要明确写出：

```text
我确认执行 Brain 授权型闭包证据刷新 2026-06-25，仅允许 A1。
```

## 8. 非声明边界

即使 A1、A2、A3 全部通过，仍不得自动声明：

- 不声明 Brain 真实集成完成。
- 不声明 Brain 真实交付完成。
- 不声明客户验收通过。
- 不声明 `accepted`、`integrated`、`production_ready`。

通过后最多只能进入：

```text
brain_completion_matrix = candidate_or_ready_for_review
brain_harness_evidence = candidate_or_ready_for_review
```

是否升级仍需 Harness/GPCF 后续裁决。
