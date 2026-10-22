---
doc_id: GPCF-DOC-93941CDB
title: spaceai-panorama-operation-normalization
project: KDS
related_projects: [KDS, GPCF, SpaceAI]
domain: openspec
status: in_progress
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-panorama-operation-normalization/README.md
source_path: openspec/changes/spaceai-panorama-operation-normalization/README.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-panorama-operation-normalization

全景态势操作流程规范化：审计 → N1–N12 规范 → B0–B5f 落地（部分完成）。

| 项 | 内容 |
|---|---|
| 状态 | **in_progress（B0–B5f 已落地；B5 剩余四大块、i18n、人工验收未完成）** |
| 追溯补建 | 2026-10-22（工作已完成并本地提交 13 个提交，补建变更账） |
| 对应 Feature | `features/active/F-038-panorama-operation-normalization`（iteration 2） |
| 承接项目 | GlobalCloud SpaceAI Platform（独立 Git 仓） |
| 提交 | `6c9cf05` `25e73d0` `73b6f5c` `179a6bb` `4dd4c08` `8a88934` `85784a3` `54fc1c3` `b98c2be` `ea0b5ea` `b438c24` `39a55e6` `441f55c` |
| 关键证据 | `.harness/runs/20261022-panorama-ops/01–21`、`docs/全景态势_操作流程规范化与合理化方案_20261022.md` |
| 组件规模 | `PanoramaDeep.vue` 3955 → **3711 行**（含并行 L4 新增约 230 行） |
| 未完成 | B5 剩余四大块（卡片列 / 飞翔 / CWME / 控制器）；i18n 约 600 行；人工验收 |
| 边界 | 未 push、未部署、未提升验收状态；不改 schema |

## 文件

- `proposal.md`：Why / What / 三层对齐 / Impact
- `design.md`：操作契约、Esc 分层、键位与偏好、拆分边界、取舍
- `tasks.md`：B0–B5f 勾选与未完成项
- `specs/spaceai-panorama-operation-normalization/spec.md`：能力规格
