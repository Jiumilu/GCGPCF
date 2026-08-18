---
doc_id: GPCF-DOC-42FE6A63EF
title: proposal
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/integrate-gke001-openspec-codegraph/proposal.md
source_path: openspec/changes/integrate-gke001-openspec-codegraph/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

## Why

GKE-001 已具有受控知识工程规范、应用实施方案、F-013 canonical 契约和跨仓协调记录，但尚未形成 OpenSpec capability contract，也没有在 CodeGraph 中建立一级工程域到仓库、契约、Release、证据和状态边界的机器可查询关系。现在纳管可以让后续 KDS、MMC、Studio、Brain 及 18 项目的变更共享同一规格入口和影响图谱，避免仅靠文档或会话记忆调度。

## What Changes

- 将 GKE-001 注册为 OpenSpec Program 级工程域，并绑定 F-013、canonical revision/manifest、Release 0 至 Release 3、OpsX、Harness 和人工状态提升边界。
- 新增 GKE-001 CodeGraph engineering-domain binding，映射 GPCF、KDS、MMC、Studio、Brain、业务权威系统和能力消费项目。
- 在现有 14 仓 CodeGraph registry 中登记 GKE-001 工程域引用，不改变真实仓库计数。
- 提供确定性 validator，验证 OpenSpec change、实施方案、机器路线图、CodeGraph binding、registry 引用和状态上限保持一致。
- 生成 CodeGraph 同步、状态和受控查询证据；只证明本地代码图谱纳管，不证明真实 KDS、客户 E2E、集成或生产就绪。

## Capabilities

### New Capabilities

- `gke001-program-governance`: 定义 GKE-001 在 OpenSpec 中的 Program、Feature、Release、跨仓派工、handoff、独立验收和状态提升要求。
- `gke001-codegraph-binding`: 定义 GKE-001 工程域在 CodeGraph 中的仓库、契约、能力、证据、依赖边和查询要求。

### Modified Capabilities

无。当前 `openspec/specs/` 尚无需要修改的 GKE-001 主规格。

## Impact

- Program：GKE-001 / GlobalCloud Knowledge Engineering。
- Project：GPCF、KDS、MMC、Studio、Brain 以及 AAAS、WAS、XiaoC、WAES、GPC、XWAIL、GFIS、XiaoG、PVAOS、SOP、PKC、XGD、ICP。
- Feature：`F-013-knowledge-asset-model-system`。
- 仓库：仅修改 GPCF 的 OpenSpec、CodeGraph 治理映射、validator、文档和 evidence；不修改外部产品仓源码。
- 依赖：canonical manifest SHA-256 `8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de`、应用路线图 SHA-256 `32f00e131b0dab667fa7403dbd6d6a79c865f517959c5d6b227f82340534ad9f`、现有 CodeGraph CLI 和 14 仓 registry。
- 非目标：不新增虚构仓库，不执行真实 KDS/MMC 写入，不启动客户 E2E，不提交、推送、部署或提升状态。
- 回滚：删除本 change、GKE-001 CodeGraph binding、registry 工程域引用、validator 和本轮 evidence；不影响现有 14 仓 CodeGraph 数据或产品运行时。
