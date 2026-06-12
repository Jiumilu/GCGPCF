---
doc_id: GPCF-DOC-8C2AA8996B
title: Status Audit — {YYYY-MM-DD}
project: GPCF
related_projects: [GPC, WAES, XiaoC, GPCF]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/loop-audit-template.md
source_path: templates/loop-audit-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Status Audit — {YYYY-MM-DD}

> 中循环审计报告模板。由评衡 + 证验联合填写。
> 存放位置：项目仓 `docs/harness/status-audit-YYYY-MM-DD.md` 和 GPCF `08-evidence-samples/{项目}/status-audit-YYYY-MM-DD.md`。

## 1. 基本信息

| 字段 | 值 |
|---|---|
| 项目 | {项目名} |
| 项目代号 | {项目代号} |
| 审计日期 | {YYYY-MM-DD} |
| 审计范围 | 第 {N} 轮至第 {M} 轮微循环 |
| 审计人 | 评衡 / 证验 |

## 2. 审计项

| # | 审计项 | 判定 | 证据引用 | 备注 |
|---|---|---|---|---|
| 1 | 是否完成 ≥3 轮微循环 | yes/no | loop-round-{ID}.md | |
| 2 | 每轮输入输出是否对应 | pass/partial/fail | | |
| 3 | evidence 是否完整 | {百分比} | evidence-index.md | |
| 4 | 阻塞项是否全部登记 | yes/no | blockers.md | |
| 5 | 是否存在越权状态升级 | yes/no | loop-state.md | |
| 6 | 是否可进入 harness_review | yes/no | | |

## 3. 评衡量化评分

| 维度 | 得分 | 扣分项 |
|---|---|---|
| evidence 完整度 | /100 | |
| 规范合规度 | /100 | |
| 循环推进效率 | /100 | |
| 阻塞消解率 | /100 | |
| **加权总分** | **/100** | |

## 4. 证验证据审计

| evidence 类型 | 应有 | 实有 | 完整 | 可复现 |
|---|---|---|---|---|
| loop record | | | yes/no | yes/no |
| diff evidence | | | yes/no | yes/no |
| command log | | | yes/no | yes/no |
| audit report | | | yes/no | - |

## 5. 阻塞项清单

| # | 阻塞项 | 责任归属 | 建议动作 | 紧急程度 |
|---|---|---|---|---|
| | | | | 高/中/低 |

## 6. 审计结论

| 字段 | 值 |
|---|---|
| 总体判定 | pass / partial / fail / blocked |
| Harness 状态建议 | evidence_ready / audit_ready / blocked / rework_required |
| 可进入下一轮 | yes / no |
| 需要人工确认 | yes / no |

## 7. 建议

- 对执行层的建议：
- 对 Harness Governance 的建议：
- 对小即的建议：
