---
doc_id: GPCF-DOC-C6440B6B
title: spaceai-l4-precision-model
project: KDS
related_projects: [KDS, GPCF, SpaceAI]
domain: openspec
status: implemented
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-l4-precision-model/README.md
source_path: openspec/changes/spaceai-l4-precision-model/README.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-l4-precision-model

三维地图 L4 精模：资产口径、清单契约、加载/切换/回落、接入工具链、一键验收与 CI。

| 项 | 内容 |
|---|---|
| 状态 | **implemented（链路）/ partial（真实资产未接入）** |
| 追溯补建 | 2026-10-22（工作已完成并本地提交 6 个提交，补建变更账） |
| 对应 Feature | `features/active/F-037-map-3d-l4-precision-model` |
| 承接项目 | GlobalCloud SpaceAI Platform（独立 Git 仓） |
| 提交 | `3880c18` `577c15b` `30cefd2` `d6c83b1` `f42aac0` `65738fc` |
| 关键证据 | `harness/l4-acceptance/`（PASS ×2）、`harness/l4-evidence/sim-drill/`、`docs/3d/l4-*.md` |
| 未完成 | 真实 L4 资产（采购/自采/外部源均待授权）；几何精度验收 |
| 边界 | 未 push、未部署、未提升验收状态；不改 schema |

## 文件

- `proposal.md`：Why / What / 三层对齐 / Impact
- `design.md`：口径、清单、切换回落、工具链、验收与取舍
- `tasks.md`：任务勾选与未完成项
- `specs/spaceai-l4-precision-model/spec.md`：能力规格（Requirement / Scenario）
