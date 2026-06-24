---
doc_id: PROJECT-DOC-REAL-EVIDENCE-RECORD-TEMPLATE
title: 真实证据记录模板
project: GPCF
related_projects: [WAES, GPCF]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/real-evidence-record-template.md
source_path: templates/real-evidence-record-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 真实证据记录模板

## 1. 证据基本信息

| 字段 | 内容 |
|---|---|
| evidence_id |  |
| project |  |
| evidence_type | `real_progress` / `real_development` / `runtime` / `integration` / `delivery` / `customer_acceptance` |
| status | `candidate` / `verified` / `ready_for_review` / `repair_required` |
| collected_at |  |
| collected_by |  |

## 2. 对应方案

| 对象 | 路径 |
|---|---|
| 项目总体方案 |  |
| 项目实施方案 |  |
| 项目群实施方案 | `01-architecture/GlobalCloud项目群实施方案.md` |
| 真实证据台账 | `09-status/globalcloud-core-chain-real-evidence-register.md` |

## 3. 执行命令

```bash
# command here
```

## 4. 原始输出摘要

记录命令结果、日志位置、失败信息或人工验收反馈。

## 5. 结论边界

本证据是否支持状态升级：

```text
supports_status =
does_not_support =
requires_user_confirmation =
```

不得把 candidate、mock、dry-run 或内部验证自动声明为 customer_accepted、accepted、integrated 或 production_ready。
