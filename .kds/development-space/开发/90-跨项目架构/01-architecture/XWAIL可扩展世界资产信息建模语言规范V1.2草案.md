---
doc_id: GPCF-DOC-XWAIL-V12-DRAFT-20260623
title: XWAIL可扩展世界资产信息建模语言规范V1.2草案
project: GPCF
related_projects: [GFIS, GPC, WAME, KDS, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/XWAIL可扩展世界资产信息建模语言规范V1.2草案.md
source_path: 01-architecture/XWAIL可扩展世界资产信息建模语言规范V1.2草案.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# XWAIL可扩展世界资产信息建模语言规范V1.2草案

> **文档状态**：draft（正文填充 2026-10-11，含 §2.1/§2.2/§2.3 资产·群组·关系建模模式与打包；此前为占位框架）
> **规范版本**：1.2.0-draft ｜ **工程化基线**：GCXWAIL 1.1（《XWAIL实施方案.md》）
> **固定关系（GPCF V1.2 口径）**：WAS 定义体系 · Ontology 定义语义 · **XWAIL 定义契约** · WAME 注册/授权/发布 · AaaS 服务包与运营
> **边界声明**：本草案不重定义 WAS 三层资产、八维、八流、生命周期与治理状态；不声明任何发布状态；任何 Schema、Profile、Validator、XAP、错误码或 CI 门禁进入正式发布前，必须补充版本兼容矩阵并通过 WAME 注册、授权与发布边界检查。

## 1. 定位

1.1 XWAIL（eXtensible World Asset Information Language）是 WAS 的**机器可读契约层**（Machine Contract）。

1.2 职责范围：把 WAS/Ontology 语义表达为**可验证**（Validator）、**可打包**（XAP）、**可治理**（版本兼容矩阵 + WAME 边界）的机器契约；提供 Schema、Profile、模板、迁移与一致性测试；配套**工具链：解析器 / 校验器 / 编辑器**（工程化实现=GCXWAIL；编辑器=建模工作台，见《XWAIL实施方案.md》阶段 2A）。

1.3 不承担：浏览器/市场/孪生平台/数据库实现（产品层）；注册、授权、发布（WAME）；服务包、订阅、计量、SLA、商业运营（AaaS）。

> 口径注：「工具处理文件，WAME 管状态」——解析器/校验器/编辑器为 XWAIL 侧工具链（处理 XWAIL 规范文件与数据源）；其在平台内的运行场景、以及数据（联网／数据库／规范文件）的调取与编辑治理，随 WAME 平台实现承载（与《WAS-Ontology-XWAIL 语义契约与映射机制》§1/§2 一致）。

## 2. 模型结构（JSON 形态）

XWAIL 模型为 JSON 文档，根对象 `kind = "XWAILModel"`。字段规范：

| 字段 | 必填 | 规范 |
|---|---|---|
| kind | ✓ | 固定 `"XWAILModel"` |
| xwailVersion | ✓ | 契约语言版本（`1.1.0`=当前样例基线；`1.2.0`=本草案目标版本） |
| wasBaseline | ✓ | WAS 统一语义基线版本（`1.1.0`） |
| ontologyVersion | ✓ | Ontology 版本 |
| wameStatus | ✓ | WAME 生命周期：`Draft / Registered / Authorized / Published / Deprecated / Archived` |
| wameEvidenceRef | 条件 | `wameStatus ∈ {Authorized, Published}` 时必填（WAME 门证据） |
| assets[] | ✓ | 资产列表；每项：`id`（唯一）/`category`/`ontologyRef`（`was:` 前缀）/`dimensions` |
| dimensions | ✓ | **八维齐全**：Physical / Rule / Intellectual / Data / Economic / Energy / Organization / SpaceTime（权威=WAS `was-dimensions.yaml`） |
| relations[] | ○ | `source`/`target` 须引用存在资产；禁止自环 |
| flowRelations[] | ○ | `flowType ∈ 八流`；`source`/`target` 存在（权威=WAS `was-flows.yaml`：LogisticsFlow / InformationFlow / FinancialFlow / EnergyFlow / ServiceFlow / ControlFlow / ValueFlow / CreditFlow） |
| lifecycle.states | ✓ | 状态机状态列表 |
| pilotScope | ○ | 试点范围契约（见 §4） |

### 2.1 资产与群组（AssetUnit / AssetGroup 模式）

- **单个资产**以 `assets[]` 条目表达（AssetUnit 模式）；**群组资产**（AssetGroup 模式）同为 `assets[]` 条目——**群组本身也是资产**。例：工厂、虚拟工厂等即以 AssetGroup 承载（《语义契约》§3 映射）；容器类对象（如项目，术语在审 T-1）同属此模式。
- 群组与其成员之间**不新增容器字段**：成员/组成统一经**关系**表达（见 2.2），保持「资产是资产、关系是关系」的正交结构。
- 群组可被更大群组包含（资产树）；成员可为任意资产类型（AssetGroup / AssetUnit）。

### 2.2 关系两分：结构关系与流关系（对齐 WAS V1.2「静态关系 + 八流行为」口径）

| 类 | 载体 | 表达 | 典型用途 |
|---|---|---|---|
| **结构关系**（静态） | `relations[]` | `type`（如 `composition`）＋ `source`/`target` | 组成/包含/层级（群组→成员、父→子） |
| **流关系**（行为） | `flowRelations[]` | `flowType ∈ 八流` ＋ `source`/`target`（＋动作/触发） | 物流/资金/信息等资产间作用 |

**建模约束**（校验项见规则清单）：
- `source`/`target` 必须引用存在资产（悬空引用禁；XWAIL-3004）；
- 禁自环（XWAIL-3001）；禁 composition 循环（XWAIL-3002，1.2 待实现）；嵌套层级限（XWAIL-6001，1.2 待实现）；
- 治理性绑定（池链等）与发布治理属 WAS/WAME 层，由 WAS 契约承载——XWAIL 只表达结构与行为的机器契约，不在核心内重复定义。

### 2.3 打包（XAP：资产包与请求包）

XAP＝可扩展资产包——XWAIL 契约的**打包/发布单位**（构建、签名、验证、回滚与证据目录约定见《XWAIL实施方案.md》阶段 4）。

- **两类包**（manifest 字段 `packageKind`）：
  - `asset`（**资产包**）：模型＋清单＋证据——承载模型交付（实例：KDS `工业绿链/图谱/ontology/xap-poc/` 五包，校验 0 issues）；
  - `request`（**请求包**）：信封＋请求体＋证据——**所有发往 WAME 的审核/注册/发布请示的统一封装**（请求类型学与信封字段见 GPCF《WAME统一审核请求机制_v0.1》§2.2/§2.3）。
- **识别与分流**：受理侧按 `packageKind` → `requestType` 分流；四级检验＝①信封（请求包必填）②包（XAP 校验）③模式（V1.2-06）④证据（引用可核验）。
- **回执**：`receipt{requestId, decision, decidedAt, authority, refs}`——`decision` 一律由治理方填写（留白纪律）。
- **规则**：V1.2-07（请求包检查，见规则清单）。

## 3. Profile 机制

3.1 内置 Profile：`supply-chain.basic`（1.1）。

3.2 扩展 Profile 登记制（在办清单——仅登记，不在此重复定义）：
- `industrial-green-chain.graph-evidence`（GPCF 受理 2026-10-11）
- `city-spatial`（XWAIL City/Spatial Profile：范围定义与 Schema 候选已受理；定版候选 v1.0 在办）
- 试点范围模型族（`industrial-green-chain.meeting-project-control`：meeting-project-control-pilot 样例）

3.3 Profile 约束规则：只可增约束、不得降低核心约束；不得重定义核心标签、八维、八流、生命周期枚举。

## 4. 试点范围契约（pilotScope）

4.1 必填字段（24）：`pilotScopeId / name / wasLayer / assetDimension / flowType / lifecycle / admissionStatus / projectRef / meetingPolicy / dataScope / evidencePolicy / approvalPolicy / receivingLedger / authorizedActorRefs / allowedActions / startAt / endAt / exitCriteria / sourceRefs / evidenceRefs / wameGateRefs / promotionBlockers / nextAction / staleSourceHash`。

4.2 受控位：`assetDimension = rule_asset`；`flowType = rule_flow`；`admissionStatus` 枚举 7 值；`allowedActions` 白名单 7 项（admit_meeting_asset / derive_minutes_candidate / derive_project_control_candidate / review_minutes_candidate / confirm_project_control_item / submit_write_intent / receive_ledger_receipt）。

4.3 Active 前置条件（校验强制）：`wameStatus ∈ {Authorized, Published}`；`promotionBlockers` 清零；`projectRef` / `receivingLedgerRef` 不得使用 candidate 占位。

4.4 口径注记（待评审）：WAS 契约侧 pilotScope 与 XWAIL 模型侧 pilotScope 为姐妹件（契约侧 / 模型侧；字段名差异属设计差异）；`admissionStatus` 枚举大小写两处不一致（WAS 小写 / XWAIL 1.1 大写），统一方向：以 WAS 契约为准（见《XWAIL-V1.2-Validator规则清单.md》V1.2-04）。

## 5. 回指与版本兼容

5.1 回指五件（模型 → 上游语义）：`wasBaseline` / `ontologyVersion` / `profile` / `ontologyRef`（`was:` 前缀）/ `termVersion`。

5.2 版本兼容矩阵（发布前置，强制）：**WAS × Ontology × XWAIL × Profile × AaaS ServicePackage × WAME status** 六维矩阵——Schema、Profile、Validator、XAP、错误码或 CI 门禁进入正式发布前必须补充。**不得以文档说明替代矩阵。**

5.3 版本策略：`1.1.x` = 工程化基线（迁移起点，非最终发布基线）；`1.2.x` = 本草案（增量：回指五件 + 兼容矩阵 + pilotScope 契约 + WAME 边界检查）。

## 6. 校验与符合性

6.1 Validator 规则清单见同目录《XWAIL-V1.2-Validator规则清单.md》（实现基线=GCXWAIL `scripts/xwail_common.py`）。

6.2 符合性三级：Core / Operational / Trusted（门禁定义见《XWAIL实施方案.md》阶段 5）。

6.3 阻断：`high` 严重度阻断发布；`medium` 默认阻断 Operational/Trusted（可豁免，须 `waiverRef` 入 policy）。

6.4 校验器成功 ≠ WAME 发布、AaaS 绑定、业务交付或客户验收（boundary 声明）。

## 7. 与既有实现的关系

7.1 GCXWAIL 仓（`Jiumilu/GCXWAIL`）1.1 工程化 = **迁移起点**；现有 `schemas-json/`、`models/`、`scripts/`、`packages/` 为 1.1 实现资产（`scripts/xwail_common.py` 为载体）。

7.2 1.2 增量以「补规则（规则清单 §2/§3）→ 补样例 → 兼容矩阵 → CI 扩展」推进，**不推倒重建**。

## 8. 收口待评审点

1. XML 通道是否纳入 1.2 —— 建议：不纳入（JSON 为现行实现；XML 250818V1 保持历史线）。
2. 版本兼容矩阵的载体格式（表格 / JSON 清单）待定。
3. Profile 白名单登记载体（GPCF registry 或 GCXWAIL `profiles/`）待定。
4. pilotScope 跨仓口径差（admissionStatus 大小写；WAS 侧 wasLayer 枚举含孤立值 `intelligence_asset_layer`）——统一方向：以 WAS 契约为准，1.2 对齐。
5. 首批实现范围：已实现 11 个 XWAIL 码 + 8 个 XAP 码；余码排期见规则清单 §2（另注：XWAIL-5001 在 1.1 实现中承载 WAME 门证据与 pilotScope 检查，与清单原定义「Integration 安全绑定」存在语义指派差异，待评审统一）。
