---
doc_id: GPCF-OS-OPEN-SPEC-COVERAGE-PROPOSAL-20260712
title: proposal
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/enable-project-group-openspec-coverage/proposal.md
source_path: openspec/changes/enable-project-group-openspec-coverage/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## Why

OpenSpec 当前仅在 GPCF 总控仓形成规则入口，18 个项目尚无逐项适用结论、入口或豁免、Feature/Loop 映射；同时部分门禁仍固定使用历史 17 项目集合，导致当前 18 项目事实与校验口径冲突。

## What Changes

- 为 AAAS、Brain、WAS、XiaoC、WAES、GPC、Studio、GPCF、XWAIL、GFIS、MMC、KDS、XiaoG、PVAOS、SOP、PKC、XGD、ICP 建立 OpenSpec 适用性矩阵。
- 为适用项目登记受控 OpenSpec 入口；为暂不适用项目登记有理由、有复核条件的豁免。
- 将每个项目映射到 GPCF Feature、Delivery/Governance Loop、Evidence 和 Harness 交接边界。
- 将当前项目门禁从历史 17 项目集合修复为 18 项目集合，同时保留历史证据的 17 项目时间口径。
- 增加可回放验证，防止项目遗漏、无入口无豁免、Feature/Loop 映射缺失及 17/18 口径回归。

## Capabilities

### New Capabilities

- `project-group-openspec-coverage`: 控制 18 项目 OpenSpec 适用性、入口/豁免、Feature/Loop/Evidence/Harness 映射和当前项目集合门禁。

### Modified Capabilities

无。

## Impact

- Program：GlobalCloud 项目群；Project：全部 18 项目；Feature：F-009。
- 影响 GPCF 总控仓的 OpenSpec 配置、项目状态入口、Loop 编排、文档台账及当前项目元数据校验器。
- 不向 18 个独立代码仓写入实现代码，不执行部署、真实 API 或 KDS API 写入。
- 非目标：不把 OpenSpec 纳入等同业务完成，不提升 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
- 回滚边界：删除新增矩阵/验证器/映射入口并恢复本 change 修改的校验器；不得回滚 ICP 已登记的第 18 项目事实。
