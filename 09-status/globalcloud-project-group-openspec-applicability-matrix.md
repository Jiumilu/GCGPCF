---
doc_id: GPCF-DOC-OPEN-SPEC-18-PROJECT-MATRIX-20260712
title: GlobalCloud 项目群 OpenSpec 适用性矩阵
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAME, WAE, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio, GCMEM, Project, PDC, SLC]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-group-openspec-applicability-matrix.md
source_path: 09-status/globalcloud-project-group-openspec-applicability-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 OpenSpec 适用性矩阵

当前项目集合事实源：`config/project-group-projects.yaml`。统一中央入口：`openspec/config.yaml`；change 命名使用 `<project-slug>-<change>`。`conditional` 表示需求、架构、契约、安全或迁移类变更触发时必须使用，不是豁免。

| 项目 | slug | 策略 | OpenSpec 入口或豁免 | Feature 映射 | 默认 Loop | Evidence | Harness |
|---|---|---|---|---|---|---|---|
| AAAS | aaas | conditional | `openspec/changes/aaas-<change>/` | `gpcf_new_feature --project aaas` | Delivery | required | required |
| Brain | brain | conditional | `openspec/changes/brain-<change>/` | `gpcf_new_feature --project brain` | Delivery | required | required |
| WAS | was | conditional | `openspec/changes/was-<change>/` | `gpcf_new_feature --project was` | Governance | required | required |
| XiaoC | xiaoc | conditional | `openspec/changes/xiaoc-<change>/` | `gpcf_new_feature --project xiaoc` | Delivery | required | required |
| WAME | wame | required | `openspec/changes/wame-<change>/` | `gpcf_new_feature --project wame` | Governance | required | required |
| GPC | gpc | required | `openspec/changes/gpc-<change>/` | `gpcf_new_feature --project gpc` | Governance | required | required |
| Studio | studio | conditional | `openspec/changes/studio-<change>/` | `gpcf_new_feature --project studio` | Delivery | required | required |
| GPCF | gpcf | required | `openspec/changes/gpcf-<change>/` | `gpcf_new_feature --project gpcf` | Governance | required | required |
| XWAIL | xwail | conditional | `openspec/changes/xwail-<change>/` | `gpcf_new_feature --project xwail` | Delivery | required | required |
| GFIS | gfis | required | `openspec/changes/gfis-<change>/` | `gpcf_new_feature --project gfis` | Governance | required | required |
| MMC | mmc | conditional | `openspec/changes/mmc-<change>/` | `gpcf_new_feature --project mmc` | Governance | required | required |
| KDS | kds | required | `openspec/changes/kds-<change>/` | `gpcf_new_feature --project kds` | Governance | required | required |
| XiaoG | xiaog | conditional | `openspec/changes/xiaog-<change>/` | `gpcf_new_feature --project xiaog` | Delivery | required | required |
| PVAOS | pvaos | conditional | `openspec/changes/pvaos-<change>/` | `gpcf_new_feature --project pvaos` | Delivery | required | required |
| SOP | sop | conditional | `openspec/changes/sop-<change>/` | `gpcf_new_feature --project sop` | Governance | required | required |
| PKC | pkc | conditional | `openspec/changes/pkc-<change>/` | `gpcf_new_feature --project pkc` | Delivery | required | required |
| XGD | xgd | conditional | `openspec/changes/xgd-<change>/` | `gpcf_new_feature --project xgd` | Delivery | required | required |
| ICP | icp | required | `openspec/changes/icp-<change>/` | `gpcf_new_feature --project icp` | Governance | required | required |

| SpaceAIStudio | spaceai-studio | required | `openspec/changes/spaceai-studio-<change>/` | `gpcf_new_feature --project spaceai-studio` | Governance | required | required |
| PQC | pqc | required | `openspec/changes/pqc-<change>/` | `gpcf_new_feature --project pqc` | Governance | required | required |

| SpaceAI | spaceai | required | `openspec/changes/spaceai-<change>/` | `gpcf_new_feature --project spaceai` | Governance | required | required |

| World | world | required | `openspec/changes/world-<change>/` | `gpcf_new_feature --project world` | Governance | required | required |
| GCMEM | gcmem | conditional | `openspec/changes/gcmem-<change>/` | `gpcf_new_feature --project gcmem` | Governance | required | required |
| WAE | wae | conditional | `openspec/changes/wae-<change>/` | `gpcf_new_feature --project wae` | Governance | required | required |
| Project | project | required | `openspec/changes/project-<change>/` | `gpcf_new_feature --project project` | Governance | required | required |
| PDC | pdc | conditional | `openspec/changes/pdc-<change>/` | `gpcf_new_feature --project pdc` | Delivery | required | required |
| SLC | slc | conditional | `openspec/changes/slc-<change>/` | `gpcf_new_feature --project slc` | Delivery | required | required |
| DRC | drc | required | `openspec/changes/drc-<change>/` | `gpcf_new_feature --project drc` | Governance | required | required |
| FireQuote | firequote | required | `openspec/changes/firequote-<change>/` | `gpcf_new_feature --project firequote` | Delivery | required | required |
| GCToken | gctoken | required | `openspec/changes/gctoken-<change>/` | `gpcf_new_feature --project gctoken` | Governance | required | required |

## 状态边界

- 当前 30 个注册记录均有中央入口，`waived=0`；因此无豁免债务。
- 中央入口不表示已向各独立项目仓安装 OpenSpec。
- apply 前必须创建或绑定 Feature；归档前必须通过 Evidence 与文档门禁。
- Harness 保留最终裁决权；未经人工确认不得提升验收或生产状态。
