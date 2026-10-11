---
doc_id: GPCF-DOC-CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-20261011
title: CWME 城市空间域扩展包登记请求 2026-10-11
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.md
source_path: docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# CWME 城市空间域扩展包登记请求 2026-10-11

## 1. 证据定位

本文登记 `CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-20261011`：**申请将 CWME 城市空间域扩展包登记入 WAS-Ontology registry**（域包＝本地化扩展本体；与《WAS×CWME 协同方案》R1「域扩展包登记制」一致）。

本文只提交登记请求：不改 WAS/Ontology 主术语、不改任何 registry 条目本体、不声明受理/通过；不声明 WAES 授权或发布；不声明生产就绪。

## 2. 请求内容

| 项 | 值 |
|---|---|
| requested_decision | register_cwme_city_space_domain_extension_pack |
| current_decision | pending_governance_review |
| 申请对象 | CWME 城市空间域扩展包（本地化扩展；`cwme-ext.ttl` 初版） |
| 载体 | KDS `世界资产/世界模型引擎/ontology/`（F-017 工作区） |
| 基线 | WAS semantic contract ／ Ontology `0.1.0` ／ XWAIL `1.1.0`（样例基线） |
| 并列 | 申请二（XWAIL City/Spatial Profile）已提交（2026-10-11）；本条为其语义侧配套 |

## 3. 扩展包内容（初版件）

| 附件 | 内容 | 验证 |
|---|---|---|
| `ontology/cwme-ext.ttl` | 扩展本体初版：核心类骨架 ＋ 我方特色扩展类（巡更/航线/围栏/预案/联动链/定位记录）＋ 22 对象属性 | **199 triples／33 类**（rdflib 7.6.0 实跑） |
| `ontology/cwme-mapping-v1.yaml` | B4-1 映射表 v1：国际词表 ↔ spaceai.db **40 表**（全量处置）↔ 特色扩展点；含关系数据线索 | 40 表盘点（只读，2026-10-11） |
| `ontology/cwme-shapes-min.ttl` ＋样例外 | 最小 SHACL（4 形状） | 合规样例 conforms=True；违规样例 **5 项全检出**（pyshacl 0.40.1） |

## 4. 与绿链侧对照（联评材料初稿）

| CWME 类（域包） | 绿链图谱对象类型 | crosswalk 概念组 |
|---|---|---|
| Site / Building / Zone | facility / project（空间锚） | space |
| Device / Camera / Door | facility（E01—E08 台账） | device |
| Alarm / Observation | event | event |
| Person / Org | person / organization | agent |
| Task / Plan | task_candidate（候选边界） | task |
| —（仿真/回放） | —（永不作为业务证据） | evidence（隔离规则沿用） |

> 联评状态：绿链侧对照已列（上表）；CWME 侧评审与正式联评记录为后续动作（不阻塞登记受理）。

## 5. 请求边界

禁止：修改 WAS 主术语、registry 既有条目本体、越过治理流程修改 XWAIL/WAS 仓、WAES 发布声明、生产就绪声明。

## 6. 门禁

| 项 | 值 |
|---|---|
| request_package_generated | true |
| submitted | true |
| registry_entry_added | false |
| governance_reviewed | false |
| waes_authorized | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 7. 下一步

registry admission 裁定；受理后按域扩展包登记制登记（不触碰既有条目）。CWME 侧后续：B4-3 生成器 → B4-4 Neo4j → B4-5 SHACL 进 CI。
