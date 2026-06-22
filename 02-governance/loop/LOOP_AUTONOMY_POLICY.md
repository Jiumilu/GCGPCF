---

# LOOP_AUTONOMY_POLICY

## LOOP 运行控制闭环常驻接入规则

LOOP 运行控制闭环为所有 Loop 工作的默认工程接口，适用于 L1、L2、L3、L3.5、L4、L5。

旧五段式只能作为历史记录读取，不得替代运行控制闭环结构。任何未登记 run、stop、verify、recover、debug 的轮次，状态最高为 `partial`，不得升级 accepted、integrated 或 production_ready。

## 模式边界

- L3：只允许受控开发态证据闭环。
- L4：真实业务 lane 仍需保持 repair_required，直到 source-of-record、runtime primary key、review queue、runtime intake、WAES review 和 verified artifact 全部具备。
- L5：必须在 owner、WAES、Harness 全部确认后另行授权。
doc_id: GPCF-DOC-29E5B0AC17
title: LOOP_AUTONOMY_POLICY
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_AUTONOMY_POLICY.md
source_path: 02-governance/loop/LOOP_AUTONOMY_POLICY.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---
