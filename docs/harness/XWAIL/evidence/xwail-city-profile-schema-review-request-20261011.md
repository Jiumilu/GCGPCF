---
doc_id: GPCF-DOC-XWAIL-CITY-PROFILE-SCHEMA-REVIEW-REQUEST-20261011
title: XWAIL City/Spatial Profile Schema 候选评审请求 2026-10-11
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/XWAIL/evidence/xwail-city-profile-schema-review-request-20261011.md
source_path: docs/harness/XWAIL/evidence/xwail-city-profile-schema-review-request-20261011.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# XWAIL City/Spatial Profile Schema 候选评审请求 2026-10-11

## 1. 证据定位

本文登记 `XWAIL-CITY-PROFILE-SCHEMA-REVIEW-REQUEST-20261011`：工业绿链图谱（F-016）承接上游受理（`XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011`，accepted 2026-10-11），就其获准动作的产出——《XWAIL City/Spatial Profile 范围定义与 Schema 候选（草案）v0.1》与 V-CP 校验器 PoC——**提请 XWAIL 项目治理流程评审与裁定（schema 定版）**。

本文只提交请求：不写 XWAIL 仓、不声明通过、不声明 WAES 授权或发布、不声明生产就绪、不声明客户验收。决定权在 XWAIL 项目治理流程。

## 2. 请求内容

| 项 | 值 |
|---|---|
| requested_decision | review_and_settle_xwail_city_profile_schema_candidate |
| current_decision | pending_governance_review |
| requester | F-016 工业绿链业务图谱只读试点（`工业绿链/图谱/`）；KDS 侧工作件 |
| 上游 | `XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011`（accepted 2026-10-11） |

## 3. 附件（送审件）

| 件 | 位置 | 状态 |
|---|---|---|
| 范围定义与 Schema 候选草案 v0.1 | KDS `工业绿链/管理文件/方案与规划/2026-10-11_XWAIL_CityProfile范围定义与Schema候选草案_v0.1.md` | **定版送审** |
| V-CP 校验器 PoC | KDS `工业绿链/图谱/ontology/city-profile-poc/`（validator＋2 正 3 负＋实跑记录） | 实跑 5/5；core 对照：正例双过、负例分层拦截 |
| 读侧对照结论 | 同上 README | core 1.1.0：XWAIL-7001/5001；`additionalProperties` 兼容放行 |

## 4. 请求边界

允许（裁定为"通过"后）：`xwail-city-profile` schema **定版**（形式以本流程裁定为准）、validator 扩展定稿。
禁止：越过治理流程直接改 XWAIL 仓、WAES 发布声明、生产就绪声明、客户验收声明。

## 5. 门禁

| 项 | 值 |
|---|---|
| request_package_generated | true |
| submitted | true |
| governance_reviewed | false |
| waes_authorized | false |
| published | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 6. 前置（已核）

- 上游请求已受理（accepted；`decision_record` 留档）。
- 送审两件在位并已实测：草案（定版送审）＋ PoC（V-CP 5/5；core 对照矩阵）。
- 未修改 XWAIL 仓；候选边界保持（`waesStatus=Draft`）。

## 7. 下一步

XWAIL 治理流程评审本请求；裁定后按结论执行 schema 定版或退回修订（均不越 XWAIL 仓写权）。
