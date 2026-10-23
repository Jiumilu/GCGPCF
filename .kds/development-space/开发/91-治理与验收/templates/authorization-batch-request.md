---
doc_id: GPCF-DOC-AUTHORIZATION-BATCH-REQUEST-TEMPLATE-20261022
title: 项目群批量授权请求模板 v1.0
project: GPCF
related_projects: [GPC, WAME, KDS, GPCF]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/templates/authorization-batch-request.md
source_path: templates/authorization-batch-request.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 项目群批量授权请求模板 v1.0

> 用途：把 `09-status/globalcloud-project-group-single-authorization-ledger-v1.0.md` 中的待授权项，以**老卢可直接回答**的形式提交。
> 规则：一次只提交 3–5 项；每项都有独立 `auth_id`；未获明确口令前不得登记授权。

## 1. 单仓最小授权口令（逐项）

```text
授权 <AUTH-ID>：只允许 <允许范围>；不允许 <禁止范围>。
```

示例：

```text
授权 AUTH-GPCF-SCHEME-REVIEW-20260626：只允许人工 review 和结论登记；不允许 stage、commit、push、delete、cleanup、deploy、真实 KDS API 同步、真实外部 API 写入或状态提升。
```

## 2. 批量授权口令（多项）

```text
授权 <批次ID> 的 <仓列表> 边界：只允许 <允许范围>；不允许 <禁止范围>。
```

## 3. 部分批准口令

```text
授权 A：<AUTH-ID-A>；授权 B：<AUTH-ID-B>；其余项暂不授权。
```

## 4. 驳回/暂缓口令

```text
暂不授权 <AUTH-ID>：原因 <一句话>。
```

## 5. 回执登记格式（append-only）

```yaml
- auth_id: AUTH-GPCF-SCHEME-REVIEW-20260626
  granted_at: "2026-10-22T00:00:00+08:00"
  granted_by: 老卢
  scope: "人工 review + 结论登记"
  actions_allowed: ["read", "review", "record_conclusion", "write_evidence"]
  actions_forbidden: ["stage", "commit", "push", "delete", "cleanup", "deploy", "status_promotion"]
  expires_at: "2026-11-05T00:00:00+08:00"
  evidence: "docs/harness/evidence/..."
  revoked_at: null
```

## 6. 禁止

- 禁止把"收到请求"当成"已授权"。
- 禁止在回执中扩大 scope。
- 禁止用一个 `auth_id` 覆盖清单外的动作。
- 禁止代替老卢填写 `granted_by`。
