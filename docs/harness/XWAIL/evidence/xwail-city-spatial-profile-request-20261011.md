---
doc_id: GPCF-DOC-XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011
title: XWAIL City/Spatial Profile 立项请求 2026-10-11
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.md
source_path: docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# XWAIL City/Spatial Profile 立项请求 2026-10-11

## 1. 证据定位

本文登记 `XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011`：**工业绿链业务图谱（F-016）向 XWAIL 项目提交 City/Spatial Profile 立项请求**（源起《WAS语义基座与CWME及工业绿链应用协同关系与分工方案》M2，D-2 按推荐确认）。

本文只提交请求，不修改 XWAIL 仓，不声明 XWAIL 通过、不声明 WAES 授权或发布、不声明 AaaS 绑定、不声明业务交付或客户验收。决定权在 XWAIL 项目治理流程（Profile 审批）。

## 2. 请求内容

| 项 | 值 |
|---|---|
| requested_decision | initiate_xwail_city_spatial_profile |
| current_decision | accepted（2026-10-11 受理；见 §8） |
| requester | F-016 工业绿链业务图谱只读试点（`工业绿链/图谱/`） |
| 基线 | WAS semantic contract ／ Ontology `0.1.0` ／ XWAIL `1.1.0`（样例基线） |
| 同源申请 | 《域包登记申请草案》申请一（CWME 城市空间域扩展包 → WAS-Ontology 登记）另行独立推进 |
| 源材料 | KDS《域包登记申请草案 v0.1》《WAS×CWME 协同方案》《CWME 本体设计专题 v1.0》 |

## 3. Profile 范围（请求）

| 域 | 类（reference，不复制正文） | 映射目标 |
|---|---|---|
| 空间 | Site / Building / Floor / Space / Zone / Link | AssetGroup、Relations |
| 设备 | Asset / Device / Camera / Door / Sensor | AssetUnit（PhysicalAsset） |
| 事件 | Event / Observation / Alarm / Actuation / Command | Relations / FlowRelations（SOSA 对齐） |
| 回指字段 | wasBaseline / ontologyVersion / profile / ontologyRef / termVersion | 按《语义契约》§6 回指规则 |

## 4. 请求边界

允许（获准后）：Profile 范围定义、`xwail-city-profile` schema 候选起草、Validator 扩展规划。
禁止：越过治理流程直接改 XWAIL 仓、WAES 发布声明、生产就绪声明、客户验收声明。

## 5. 门禁

| 项 | 值 |
|---|---|
| request_package_generated | true |
| submitted | true |
| governance_reviewed | true |
| waes_authorized | false |
| published | false |
| accepted | true |
| integrated | false |
| production_ready | false |

## 6. 前置（已核）

- WAS-Ontology registry pass（43 项，2026-06-21）；XWAIL `mapping_candidate` 映射证据在位（2026-06-25）。
- 本图谱侧已产出可校验的一致样例（`工业绿链/图谱/ontology/exports/`，XWAIL 校验库只读导入 pass，2026-10-11）。
- 未修改 XWAIL 仓；候选边界保持（`waesStatus=Draft`）。

## 7. 下一步

XWAIL 治理流程裁定本请求；获准后进入 `xwail-city-profile` schema 候选起草，与 CWME B4-1/B4-2 初版件协同推进（CWME 编号 F-017，2026-10-11 已启动）。

## 8. 受理记录（2026-10-11）

- **已受理（accepted）**：授权来源＝老卢「按推荐执行」（2026-10-11）；材料复核通过（前置/边界齐备，见 §6）。
- 后续动作：`xwail-city-profile` schema 候选起草（仍不写 XWAIL 仓、不声明 WAES 发布，见 §4 边界）。
