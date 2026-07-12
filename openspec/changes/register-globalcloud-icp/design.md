---
doc_id: GPCF-OS-ICP-REGISTRATION-DESIGN-20260712
title: design
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF, ICP]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/register-globalcloud-icp/design.md
source_path: openspec/changes/register-globalcloud-icp/design.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## Context

项目群当前登记17个项目。GC-ICP 已在独立仓库完成首期开发闭环，但 GPCF 的项目清单、职责矩阵和控制台账尚无该项目，因此项目群无法正式追踪其状态、风险和传导关系。

## Goals / Non-Goals

**Goals:**

- 以第18个独立项目登记 GC-ICP。
- 明确产业控制平面与 GPCF、WAS、WAES、KDS、GPC、GFIS、PVAOS 的边界。
- 把总体状态固定为 `candidate/partial/human_required`。
- 建立控制台账与项目状态入口。

**Non-Goals:**

- 不声明跨项目集成、真实业务接入或生产就绪。
- 不将 GC-ICP 计入既有17项目已完成基线。
- 不改动其它项目的当前状态和证据。

## Decisions

1. 直接扩展项目群主方案、实施方案和既有控制台账，避免另建平行登记体系。
2. 项目代码统一使用 `ICP`，目录统一使用 `GlobalCloud ICP`，产品名为 `GlobalCloud Industry Control Plane`。
3. 项目只以候选状态进入清单，GPCF 当前 `rework_required` 门禁保持不变。
4. 项目状态、风险和路线图使用既有 `projects/<project>` 三文件模式。

## Risks / Trade-offs

- [第18项目导致既有17项目计数失真] → 明确新旧基线时间，新增计数不得回写旧证据。
- [本地开发被解释为已集成] → 台账明确 `integration_not_started` 和人工确认边界。
- [与 WAES/GPC/KDS 职责重叠] → 在总体方案中登记禁止边界。
