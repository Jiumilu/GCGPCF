---
doc_id: GPCF-DOC-165FB00EF6
title: Loop Round GPCF XWAIL City Spatial Profile Request 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-XWAIL-CITY-SPATIAL-PROFILE-REQUEST-001.md
source_path: docs/harness/loops/loop-round-GPCF-XWAIL-CITY-SPATIAL-PROFILE-REQUEST-001.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# Loop Round GPCF XWAIL City Spatial Profile Request 001

## 输入

- 老卢点名执行（2026-10-11）："1、提交"——提交域包登记申请（XWAIL City/Spatial Profile 立项先行）。
- 前置已核：WAS-Ontology registry pass；`mapping_candidate` 映射证据在位；图谱 XWAIL 导出物校验 pass（O-2，同日）。

## 动作

- 建 `docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.json` / `.md`（request 包）。
- 保证：不修改 XWAIL 仓；`current_decision` 留 `pending_governance_review`（决定权在 XWAIL 治理流程）。

## 输出

- `docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.md`
- `docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.json`

## 检查

- `python3 tools/kds-sync/validate_xwail_city_spatial_profile_request.py`
- `python3 tools/kds-sync/validate_was_project_group_ontology_registry.py`（回归）
- `python3 tools/kds-sync/document_control.py`（本目录新增 Markdown 必跑）

## 反馈

- 请求包已提交（submitted=true）；`governance_reviewed=false`、`waes_authorized=false`、`accepted=false`、`integrated=false`、`production_ready=false`。
- 获准后将进入 `xwail-city-profile` schema 候选起草（与 F-017 CWME B4-1/B4-2 协同）。

## 下一轮

XWAIL 治理裁定；如获准，建立 profile 候选草稿与 validator 扩展清单（仍不改 XWAIL 仓，走治理交换）。
