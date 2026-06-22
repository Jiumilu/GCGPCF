---
doc_id: GPCF-DOC-D63AEEB17D
title: Loop 治理运行边界
project: WAES
related_projects: [GFIS, WAES, KDS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop 治理运行边界

本文定义实施主进程与治理进程之间的边界。

## 进程分工

| Process | Responsibility | Boundary |
|---|---|---|
| implementation main process | 产生真实 GFIS source records、runtime primary keys、review queue entries、runtime intake records、WAES reviews、verified artifacts，以及任何 accepted/integrated 证据。 | 业务状态升级前必须提供真实业务证据。 |
| governance process | 检查 Loop 质量、文档控制、债务可见性、验证覆盖和自我提升门禁。 | 不得创建或替代真实业务事实。 |

## 治理规则

1. 治理进程可以新增 validators、review plans、evidence indexes 和 status ceilings。
2. 治理进程可以标记缺失证据、历史债务或 review required 状态。
3. 治理进程不得创建 source-of-record、runtime primary key、review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated 状态。
4. 治理进程不得用 synthetic、demo、mock、fixture、KDS candidate-only、Loop document-only 或 oral-only 材料替代真实业务证据。
