---
doc_id: GPCF-DOC-GKE001-OPENSPEC-CODEGRAPH-EVIDENCE-20260811
title: GKE-001 OpenSpec 与 CodeGraph 纳管证据
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/features/F-013/evidence/gke-001-openspec-codegraph-binding-20260811.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-openspec-codegraph-binding-20260811.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

# GKE-001 OpenSpec 与 CodeGraph 纳管证据

## 结论

GKE-001 已作为跨仓知识工程域纳入 GPCF OpenSpec 和 CodeGraph 治理。它不是新增 Git 仓库：项目群治理范围保持 18 个项目，CodeGraph 仓库注册表保持 14 个真实仓库。当前分类仅为 `governance_binding_verified`，整体仍为 `active / partial / not_complete`。

## 受控关系

- OpenSpec Program：`governance/openspec/gke001-program-binding.yaml`
- OpenSpec change：`openspec/changes/integrate-gke001-openspec-codegraph/`
- CodeGraph domain：`governance/codegraph/gke001-engineering-domain-binding.yaml`
- CodeGraph registry：`governance/codegraph/repo-codegraph-registry.yaml`
- canonical：F-013、revision `v0.1`、manifest SHA-256 `8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de`
- application roadmap SHA-256：`32f00e131b0dab667fa7403dbd6d6a79c865f517959c5d6b227f82340534ad9f`

## 回放结果

| 检查 | 结果 |
|---|---|
| OpenSpec strict validation | pass |
| GKE-001 Program/CodeGraph validator | pass |
| representative drift self-test | pass |
| project-group OpenSpec coverage | pass，18/18 |
| knowledge asset model | pass |
| GPCF 2.0 Feature workspace | pass |
| F-013 Evidence Gate | pass，保留 11 个治理 blocker |
| F-013 KDS apply admission | pass，`blocked_dirty_worktree`，KDS changed entries 166 |
| scoped document control | pass，仅本地 KDS 开发空间镜像 |
| document pollution / KDS token | pass / pass |
| LOOP document gate | `rework_required`，既有 `localization_debt` |
| project-group gate readiness | `watch_required`，0/17，既有 `localization_debt` 扇出 |
| CodeGraph sync/status | pass，记录时 pending 0 |
| CodeGraph `validate_program` / `PROGRAM_BINDING` query | pass |
| CodeGraph 两个 binding file node | pass |
| project-group full CodeGraph coverage | fail：KDS live pending 13，与本轮 GPCF 域绑定无关，仍须治理收口 |

机器证据位于 `docs/harness/evidence/gke001-openspec-codegraph-binding-20260811.json`。

## 事实边界

CodeGraph 证据只证明 GKE-001 治理文件已经建立关系、进入本地索引并可查询；不证明 KDS、MMC、Studio、Brain 已完成真实网络集成、客户任务闭环或生产部署。OpenSpec 变更完成也不等于 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

本轮未修改任何产品仓源码，未执行真实 KDS/MMC 写入、提交、推送、部署、客户发布或状态提升。回滚仅移除本轮未提交的 GPCF OpenSpec、CodeGraph、校验器、入口引用和证据增量，不涉及外部数据回滚。
