---
doc_id: GPCF-OS-ICP-REGISTRATION-PROPOSAL-20260712
title: proposal
project: KDS
related_projects: [GPC, WAES, KDS, GPCF, ICP]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/register-globalcloud-icp/proposal.md
source_path: openspec/changes/register-globalcloud-icp/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## Why

GC-ICP 已形成独立仓库、总体/实施方案、24×11契约、场景编排服务和验证证据，但尚未进入 GPCF 项目清单和控制台账。需要以候选状态完成项目群登记，才能建立正式传导关系，同时避免把本地开发误写为集成或验收完成。

## What Changes

- 将 GlobalCloud ICP 登记为项目群第18个独立项目。
- 在项目群总体方案中增加 ICP 的定位、职责和禁止边界。
- 在项目群实施方案中增加 ICP 的实施范围和候选链路。
- 在总体方案、实施方案控制台账中登记 ICP。
- 建立 `projects/icp` 状态、风险和路线图入口。
- 保持 ICP 为 `candidate/partial/human_required`，不改变 GPCF 当前门禁结论。

## Capabilities

### New Capabilities

- `project-group-icp-registration`: 控制 GC-ICP 作为独立项目的范围、职责、状态、台账和传导关系。

### Modified Capabilities

无。

## Impact

- 修改项目群总体方案、实施方案和两份项目控制台账。
- 新增 ICP 项目状态、风险和路线图入口。
- 不修改现有17项目职责，不执行部署、集成、KDS API 写回或状态晋升。
