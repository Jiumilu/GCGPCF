---
doc_id: GPCF-DOC-875CBA8392
title: tasks
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/integrate-gke001-openspec-codegraph/tasks.md
source_path: openspec/changes/integrate-gke001-openspec-codegraph/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

## 1. OpenSpec 项目群治理

- [x] 1.1 建立机器可读的 GKE-001 项目群绑定，关联 F-013、canonical manifest、应用路线图、Release 门禁和状态边界。
- [x] 1.2 扩展仓库 OpenSpec 上下文，强制声明 GKE-001 Program、Release、Feature、CodeGraph 影响、回滚和授权边界。

## 2. CodeGraph 工程域

- [x] 2.1 为 18 个受治理项目和 14 个索引仓库建立 GKE-001 工程域绑定，不改变真实仓库计数。
- [x] 2.2 在项目群 CodeGraph registry 中登记工程域绑定，并保留仓库级所有权。
- [x] 2.3 为 Program、Release、仓库、项目、canonical hash、授权和状态漂移增加确定性校验。

## 3. 受控入口与证据

- [x] 3.1 将 GKE-001 应用实施方案和长期调度提示词连接到 OpenSpec 与 CodeGraph 绑定。
- [x] 3.2 形成有界的 F-013 和 CodeGraph 证据，明确区分索引治理产物与真实跨仓集成。

## 4. 验证与回滚

- [x] 4.1 执行 OpenSpec 严格校验、GKE-001 绑定校验器、CodeGraph 同步/状态/查询及适用的项目群治理检查。
- [x] 4.2 执行文控、污染/TOKEN 检查、文档/readiness 门禁和差异检查，并如实保留 partial/rework 结果。
- [x] 4.3 将回滚限定为移除本轮未提交的 GPCF 治理增量，不修改产品仓库或外部事实。
