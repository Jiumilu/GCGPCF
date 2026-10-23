---
doc_id: GPCF-PROJECT-PLANE-PROPOSAL-20261018
title: GlobalCloud Project Plane 与 GPCF 对接提案
project: GPCF
related_projects: [GPCF, Project]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/project-plane-gpcf-integration/proposal.md
source_path: openspec/changes/project-plane-gpcf-integration/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

## Why

项目群已有 GPCF Feature、Evidence 和 Loop 控制链，但缺少面向团队的统一任务协作入口。用户决定新增 GlobalCloud Project，基于 Plane 开源社区版定制，首期优先对接 GPCF Feature 与证据状态。

## What Changes

- 将 GlobalCloud Project 作为第 25 个独立项目纳入项目群，并建立项目级总体、实施与状态入口。
- 固定 Plane 社区版上游基线，保留许可证与来源信息。
- 增加 GPCF Feature／Evidence 的只读投影，展示来源、状态、证据链接与更新时间；不从 Plane 回写 GPCF 裁决状态。
- 将项目群中央登记、Feature 与 OpenSpec 入口对应到新项目。

## Capabilities

### New Capabilities

- `project-plane-onboarding`: GlobalCloud Project 独立纳管、上游源码基线与许可可追溯。
- `project-gpcf-readonly-projection`: GPCF Feature／Evidence 只读同步和展示。

### Modified Capabilities

无。

## Impact

Program：GlobalCloud Platform Group。Project：GlobalCloud Project。Feature：F-028。影响仓库：新建 `GlobalCloud Project` 和 GPCF；依赖 Plane 社区版源码、GPCF 运行队列与证据结果。KDS 仅受控镜像文档，不建立第二证据主账。回滚边界为移除新项目投影与本次登记，保留原 GPCF Feature、Evidence 和历史快照。授权范围为本地建仓与开发；业务验收、生产部署、对外发布和状态提升仍需人工确认。
