---
doc_id: GPCF-DOC-GSCROLEVIEWLOOP001
title: loop-round-GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001
project: GPCF
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001.md
sync_direction: bidirectional
last_reviewed: 2026-07-01
supersedes: []
superseded_by: []
---

# loop-round-GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001

日期：2026-07-01
状态：`controlled_local_entity_recorded`
目标：把绿色供应链角色视图从方案落成 KDS 实体产物，并纳入知识工程体系。

## 1. 本轮输入

| 输入 | 路径 |
|---|---|
| 角色初始化来源 | `03-data-ai-knowledge/GlobalCloud绿色供应链合作单位接入与组织空间初始化清单.md` |
| 对象字段与 11 池来源 | `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md` |
| no-write API 契约来源 | `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统数据对象最小落库与API契约草案.md` |
| KDS 对象模型 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/_schemas/object-model.yaml` |
| KDS 全局对象注册表 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/_registries/global-object-registry.yaml` |

## 2. 本轮产物

| 产物 | 路径 | 状态 |
|---|---|---|
| GPCF 受控说明 | `03-data-ai-knowledge/GlobalCloud绿色供应链角色视图KDS实体产物.md` | `controlled` |
| KDS 实体页 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/entities/green-supply-chain-role-view-entity.md` | `controlled_candidate` |
| KDS 注册表入口 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/_registries/global-object-registry.yaml` | `governance_index_only` |
| 局部校验脚本 | `tools/kds-sync/validate_green_supply_chain_role_view_kds_entity_20260701.py` | `local_gate` |

## 3. LOOP 运行控制闭环

### run

执行本地实体化：读取受控方案，把角色、ACL、11 池、no-write 边界和知识工程挂接固化为 KDS 实体页与注册表入口。

### stop

触发以下任一条件必须停止升级：

1. 缺少人工授权或 WAES 规则记录。
2. 实体页出现真实账号创建、真实 KDS API 写入、生产权限配置或业务验收完成声明。
3. 出现 `accepted`、`integrated`、`production_ready`、`customer_accepted` 等未经人工确认的状态提升。

### verify

本轮必须通过：

1. `python3 tools/kds-sync/validate_green_supply_chain_role_view_kds_entity_20260701.py`
2. `python3 tools/kds-sync/document_control.py` 或限定范围等价同步检查
3. `python3 tools/kds-sync/check_document_pollution.py`
4. `python3 tools/kds-sync/validate_kds_token.py`
5. `python3 tools/kds-sync/loop_document_gate.py --check-only`

### recover

若校验失败，保持实体状态为 `controlled_candidate` 或 `repair_required`，回退到受控文档和 KDS 注册表入口复核，不做真实 API 同步。

### debug

优先排查：

1. frontmatter 与 `source_path / kds_path` 不一致。
2. KDS 实体页缺少 `entity_id`、`source_refs`、`acl_scope_tags`、`pool_bindings` 或禁止升级口径。
3. 注册表入口与实体页 ID 不一致。
4. 文档污染或 KDS token 门禁异常。

## 4. 真实边界

本轮只完成本地受控实体登记和知识工程挂接证据，不代表 KDS API 已真实同步，不代表合作单位账号、权限、积分、收益、额度或悬赏已完成配置。
