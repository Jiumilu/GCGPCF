---
doc_id: GPCF-F-018-ARTIFACTS-GPCF-GOVERNANCE-CONSOLE
title: F-018 artifacts（指针说明）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-018-gpcf-governance-console/artifacts/README.md
source_path: features/done/F-018-gpcf-governance-console/artifacts/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# F-018 artifacts（指针说明）

本 Feature 的交付工件不在本目录（保持工作区轻量），实际工件位置：

| 工件 | 位置 |
|---|---|
| 模块包（八视图组件） | `GlobalCloud WAE/packages/modules/module-gpcf-console/`（package.json/manifest.yaml/src/CHANGES.md） |
| WAE 装配点 | `apps/wame`：WorkbenchModule（路由/context）＋GlobalCloudSidebar（第 6 项）＋vite.config（只读代理/别名）＋domain/platform.ts（platformId） |
| 装配清单（WAE 侧） | `GlobalCloud WAE/docs/assembly-spec/manifests/gpcf-console.yaml`＋`_三方对账表.md`（v0.6） |
| 应用库登记 | `GlobalCloud KDS/世界资产/应用库/registry.yaml`（v0.6·gpcf-console available） |
| 规划件 | `GlobalCloud KDS/体系/GPCF治理控制台_全量规划_v0.1.md` |
| 契约件 | `GlobalCloud KDS/世界资产/应用库/GPCF控制台_数据卡与接口契约_v0.1.md` |
| 数据面导出物 | `runtime/evidence/`（governance-state/ledger-index/governance-probe·gitignore 生成物） |
