---
doc_id: GPCF-DOC-GSCROLEVIEWKDSENTITY20260701
title: GlobalCloud 绿色供应链角色视图 KDS 实体产物
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链角色视图KDS实体产物.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链角色视图KDS实体产物.md
sync_direction: bidirectional
last_reviewed: 2026-07-01
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链角色视图 KDS 实体产物

日期：2026-07-01
轮次：`GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001`
状态：`controlled_local_entity`

## 1. 定位

本文把绿色供应链角色视图从方案口径落成 KDS 知识工程实体产物，并建立 GPCF 受控说明、KDS 实体页、全局对象注册表入口和 LOOP 证据之间的引用关系。

本次落地是本地受控实体登记，不创建真实账号，不写真实 KDS API，不配置生产权限，不确认合作单位接入完成，不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

## 2. 实体产物

| 项 | 值 |
|---|---|
| KDS 实体 ID | `KDS-GSC-ROLE-VIEW-20260701` |
| 对象类型 | `Entity / kds_role_view` |
| KDS 实体页 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/entities/green-supply-chain-role-view-entity.md` |
| KDS 注册表入口 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/_registries/global-object-registry.yaml` |
| GPCF 受控说明 | `03-data-ai-knowledge/GlobalCloud绿色供应链角色视图KDS实体产物.md` |
| LOOP 证据 | `docs/harness/loops/loop-round-GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001.md` |
| 写入边界 | `no_write / candidate_only / controlled_document` |

## 3. 来源继承

本实体继承以下受控方案：

| 来源 | 继承内容 |
|---|---|
| `GlobalCloud绿色供应链合作单位接入与组织空间初始化清单.md` | 角色初始化、组织空间、权限矩阵、接入状态和 LOOP 证据要求 |
| `GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md` | 统一编号、通用必填字段、KDS 11 池、状态机和禁止升级口径 |
| `GlobalCloud绿色供应链分布式知识系统数据对象最小落库与API契约草案.md` | P0 no-write、candidate_only、metadata_only 和 API 响应边界 |
| `docs/gc-knowledge-fabric/object-numbering-rule-v0.1.md` | 对象编号治理入口 |
| `docs/gc-knowledge-fabric/status-machine-policy.md` | 状态机治理入口 |
| `docs/gc-knowledge-fabric/object-relationship-policy.md` | 对象关系治理入口 |

## 4. 角色视图

| 角色代码 | 角色 | 默认可见范围 | KDS 主责池 | 当前状态 |
|---|---|---|---|---|
| `GSC-ROLE-UNIT-OWNER` | 单位负责人 | `own_unit + invited` | 人才池、场景池 | `candidate` |
| `GSC-ROLE-PROJECT-OWNER` | 项目负责人 | `project_group + own_unit` | 人才池、场景池、数据池 | `candidate` |
| `GSC-ROLE-MATERIAL-CURATOR` | 资料管理员 | `own_unit` | 数据池、政策池、场景池 | `candidate` |
| `GSC-ROLE-AI-QUOTA-ADMIN` | AI 额度管理员 | `own_unit` | 资金池、数据池、人才池 | `candidate` |
| `GSC-ROLE-POINTS-ADMIN` | 积分管理员 | `own_unit` | 人才池、数据池、场景池 | `candidate` |
| `GSC-ROLE-BOUNTY-ADMIN` | 悬赏管理员 | `own_unit + invited` | 数据池、人才池、场景池 | `candidate` |
| `GSC-ROLE-FINANCE-CONTACT` | 财务联系人 | `finance_private + own_unit` | 资金池、数据池 | `candidate` |
| `GSC-ROLE-QUALITY-POD-CONTACT` | 质量 / POD 联系人 | `own_unit + invited` | 订单池、运力池、数据池 | `candidate` |
| `GSC-ROLE-GFIS-OPERATOR` | GFIS 操作人 | `gfis_operator` | 订单池、产能池、数据池、场景池 | `candidate` |
| `GSC-ROLE-WAES-LIAISON` | WAES 对接人 | `waes_boundary` | 数据池、人才池、政策池 | `candidate` |
| `GSC-ROLE-KDS-RECORDER` | KDS 记录人 | `kds_operator` | 数据池、人才池、场景池 | `candidate` |

所有角色必须保留授权来源、授权范围、生效日期、复核日期和撤销条件。缺少人工授权或 WAES 规则记录时，只能保持 `candidate`、`repair_required` 或 `blocked`。

## 5. 知识工程挂接

| 知识工程层 | 挂接方式 | 边界 |
|---|---|---|
| 对象模型 | 注册为 `Entity / kds_role_view`，主键 `entity_id` | 不替代真实账号或 IAM |
| 全局对象注册表 | 以 `KDS-GSC-ROLE-VIEW-20260701` 建立对象入口 | 只做跨空间治理索引 |
| 11 池 | 角色映射到人才池、数据池、场景池，并按业务角色挂接资金、订单、运力、政策等池 | 不确认业务事实 |
| RAG 准入 | 默认 `limited / repair_required`，敏感角色和 DSR-L3 仅元数据 | 不把 LLM 输出写成事实 |
| ACL | 使用 `own_unit`、`invited`、`finance_private`、`gfis_operator`、`waes_boundary`、`kds_operator` 等范围标签 | 不配置生产权限 |
| LOOP | 通过 `GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001` 形成 evidence | 不代表合作单位接入验收完成 |

## 6. 禁止升级口径

1. 角色视图实体存在，不等于真实账号已创建。
2. KDS 注册表存在，不等于 KDS API 已真实同步。
3. 角色字段完整，不等于授权已确认。
4. 11 池挂接存在，不等于业务事实、积分、收益、额度或悬赏已确认。
5. 缺少人工确认或委员会备案时，禁止声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

## 7. 当前下一步

1. 由 KDS 记录人复核实体字段和注册表入口。
2. 由 WAES 对接人复核 ACL、DSR-L2 / DSR-L3 和禁止升级口径。
3. 若后续需要真实 KDS API 同步，必须另行形成授权窗口、请求包、回执和回滚证据。
