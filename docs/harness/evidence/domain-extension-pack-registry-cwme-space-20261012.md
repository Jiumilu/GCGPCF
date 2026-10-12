---
doc_id: GPCF-DOC-DOMAIN-EXTENSION-PACK-REGISTRY-CWME-SPACE-20261012
title: 域扩展包登记（CWME 城市空间域扩展包）· 2026-10-12
project: KDS
related_projects: [WAME, CWME, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/domain-extension-pack-registry-cwme-space-20261012.md
source_path: docs/harness/evidence/domain-extension-pack-registry-cwme-space-20261012.md
sync_direction: bidirectional
last_reviewed: 2026-10-12
supersedes: []
superseded_by: []
---

# 域扩展包登记（CWME 城市空间域扩展包）· 2026-10-12

## 1. 登记定位

本文登记 `GPCF-DOMAIN-EXTENSION-PACK-REGISTRY-CWME-SPACE-20261012`：按 WAS 项目群 registry `future_project_policy`（admission_required／scope binding／六类目映射／不绕 KDS-WAME loop），将 **CWME 城市空间域扩展包**（本地化扩展本体，`cwme-ext.ttl` 初版）登记为域扩展包条目（候选），与 IGL 业务域切片（2026-10-11）并列。

- 上游：`cwme-space-domain-extension-registration-request-20261011`（**已受理 accepted，2026-10-12**）。
- 基础 registry：`was-project-group-ontology-registry-20260621.json`（**既有 43 条一字未动**）。
- 登记状态：`domain_extension_pack_registered_candidate`（候选：零写回、零运行状态提升）。

## 2. 域扩展包条目

| 项 | 值 |
|---|---|
| 名称 | `CWME 城市空间域扩展包`（CWME City Space Domain Extension Pack） |
| 载体 | `世界资产/世界模型引擎/ontology/`（F-017 工作区） |
| 内容 | `cwme-ext.ttl`（199 triples／33 类／22 对象属性）｜`cwme-mapping-v1.yaml`（spaceai.db 40 表全量处置）｜`cwme-shapes-min.ttl`（4 形状，正例 conforms=True／负例 5 项检出） |
| scope 绑定 | 世界资产（CWME/F-017）＋ KDS |
| 六类目映射 | object=33 类｜relationship=22 对象属性｜event=Alarm/Observation（SOSA 方向）｜evidence=实跑记录+mapping-v1｜state=P2-2/P2-3 候选态｜interface=exports/city+city-api（MMC 已注册） |
| 并列 | IGL 业务域切片（GreenChainGraphBusinessDomain，2026-10-11）｜F-015（组织域） |
| crosswalk | `工业绿链/图谱/ontology/crosswalk-工业绿链×CWME_v0.1.yaml`（待双方联评，不阻塞本登记） |

## 3. 边界（候选保持）

| 项 | 值 |
|---|---|
| real_source_records | 0 |
| wame_review | 0 |
| accepted | false |
| integrated | false |
| production_ready | false |
| runtime_write | false |
| kds_api_write | false |

## 4. 非声明

- 本登记为**域扩展包条目（候选）**：不是运行授权、不是知识库、不替代 KDS source-of-record。
- 不修改 `20260621` registry 既有 43 条；不改写任何来源；零写回、零运行状态提升。
- 与 XWAIL City/Spatial Profile（申请二）分别为语义侧与契约侧，互不阻塞。

## 5. 复核

```bash
python3 tools/kds-sync/validate_cwme_space_domain_extension_registration_request.py
```