---
doc_id: GPCF-DOC-GROUP-GAP-ADR-20261025
title: GlobalCloud 项目群结构性缺口分析与 ADR 草案（SOP 补链 / ICP 城市层 / 场景包接口）
project: GPCF
related_projects: [SOP, WAME, WAE, PMC, ICP, KDS, AAAS, XWAIL, GFIS, GPC, World, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud项目群结构性缺口分析与ADR草案_v1.0.md
source_path: 01-architecture/GlobalCloud项目群结构性缺口分析与ADR草案_v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群结构性缺口分析与 ADR 草案

日期：2026-10-25　状态：controlled v1.0（2026-10-25 老卢确认「全按推荐」）
**输入**：session 5f14 冻结基线（53 总纲 / 54 台账 / 61 冻结 / 18 号文缺口识别 / 22 号文 SOP 定位）
**性质**：缺口分析与三份 ADR 草案。设计基线冻结（61 号），本文件为**实施期发现的结构缺口补充设计**，须经 CHG 流程纳入基线。**不改既有受控件**。

---

## 0. 结论先行

| 缺口 | 模型推荐方案 | 概率 |
|---|---|---|
| ① SOP 未纳入四层授权/审批链 | **A：SOP=审批流实例编排者，WAME 仍是唯一裁决方，WAE 执行写门禁** | **0.951**（B 0.039 / C 0.010） |
| ② ICP 城市层缺位 | **A：维持 ICP pause；城市层 S5 前不含 ICP，仅以 KDS 产线投影只读引用** | **0.670**（B 0.221 / C 0.108） |
| ③ 绿链业务系统↔企业层场景包接口未定义 | **A：XWAIL Schema + 只读事实投影 + 事件合同；写回走 XAP 治理** | **0.947**（B 0.023 / C 0.030） |

三项均以「不新增项目、不夺既有主账、不绕治理」为原则，与冻结基线一致。

---

## 1. ADR-B8-01：SOP 以「流程编排者」身份接入四层授权链（草案）

### 背景
四层授权链现状：`身份(WAE idp) → WAME 裁决 → WAE 写门禁 → L3 人工确认`。SOP 虽是项目群唯一流引擎中心（2026-10-17 裁定），但不在链上；四层审批流（个人豁免/团队 2 级/企业 3 级/城市 4 级会签）无处落地。

### 决策
1. **职责三分不变**：WAME=唯一裁决方（合不合规）；SOP=流程定义与流程实例编排（按什么顺序、谁审、怎么收口）；WAE=写门禁执行（能不能写）；PMC=任务执行状态（做到哪了）。
2. SOP 在授权链中的位置：**L3 人工确认环节的流程承载者**——SOP 输出「流程实例 + 步骤状态 + 审批人序列」，WAME 依据其裁决，WAE 依据裁决放行写操作。
3. SOP **不持**：业务主账、事实、证据状态、总控；其过程证据与 WAME Evidence Ledger 互补（SOP 管流程过程，WAME 管动作证据）。

### 接口（草案）
| 接口 | 方向 | 语义 |
|---|---|---|
| `flowdef:get` | WAME/WAE → SOP | 取审批流定义（层/场景/版本） |
| `flowinst:create` | WAME → SOP | 为一次授权请求开流程实例（关联 authz_id） |
| `step:advance` | SOP → WAME | 步骤推进与审批人回执（幂等） |
| `flowinst:close` | SOP → WAME/PMC | 会话收口 + 过程证据引用 |

### 数据模型（草案）
`FlowDef(flowId, tier, scenario, steps[], version, status)`；`FlowInstance(instanceId, authzId, flowId, state, currentStep, approvalRefs[], openedAt, closedAt)`；`StepState(stepId, assignee, decision, decidedAt, evidenceRef)`。

### 门禁与纪律
- 流程定义变更须版本化 + SOP 会话收口；审批裁决仍以 WAME 记录为准；
- AI 只能发起流程与起草，**不得代替审批人**（L3 人工确认位）；
- 城市层 4 级会签为 S5 前增量，不阻塞 S1 审批流。

### 落地
S1：审批流（团队 2 级/企业 3 级）最小闭环；S4：业务流规则包接入场景包；S5：跨组织会签流。**CHG 需求：CHG-16（B8 补链）**，属主 SOP/WAME 双签。

### 风险
流程与裁决双写不一致 → 以 WAME 裁决为唯一状态源，SOP 只读回挂；SOP P1 基线能力不足 → 分层推进（22 号文 Q23）。

---

## 2. ADR-ICP-01：城市层暂不含 ICP，仅保留 KDS 投影只读引用（草案）

### 背景
ICP（24 字产业模型 / 十一池只读投影 / 决策候选）处置为 `pause`（2026-10-22，preconditions：真实业务源到位 或 SOP 需新版 ICP 规则包）。18 号文识别「ICP 在城市层缺位」：城市层需要产业语义支撑，但 ICP 未纳入四层依赖。

### 决策
1. **维持 pause**，不解除；城市层 S5 前**不以 ICP 为强依赖**。
2. 城市层所需产业语义，以 **KDS 只读投影**（十一池视图）与 WAS/Ontology 语义基座承载；ICP 的产业匹配建议作为**可选旁路**（只读、人工参考），不进入授权链与证据链。
3. **前置条件不变**：真实业务源到位或 SOP 需新版 ICP 规则包时，再走 CHG 解除 pause 并评估城市层接入。

### 接口（草案，只读）
`projection:read`（KDS）→ 城市层视图；ICP `match_suggest` 保持 candidate 语义，不产生写回与状态。

### 落地
S5 城市层启动前完成一次 ICP 接入评估（含 pause 解除与否），评估单随城市项目立项走 G5。

### 风险
城市层产业语义不足 → 以 WAS/Ontology + KDS 投影兜底；ICP 模型漂移 → pause 状态不对外承诺。

---

## 3. ADR-PKG-01：场景服务包与绿链业务系统的接口契约（草案）

### 背景
企业层场景服务包（AAAS ServicePackage，19 顶层键/required 9 项）需消费 GFIS/GPC 事实（订单、库存、质量、发货、签收），但二者接口未定义；直接调用业务 API 会绕过治理与证据链。

### 决策
1. **契约层**：以 **XWAIL Schema/Profile** 定义「场景包 ↔ 业务系统事实契约」（只读事实投影 + 事件引用），AAAS 服务包通过 `xwailBinding` 绑定版本。
2. **读**：事实一律只读投影（GFIS 单厂事实、GPC 协同事实），经 KDS/事件合同引用，**不直连业务库**。
3. **写**：任何回写/状态变化走 **XAP 治理**（WAME 受理 → 裁决 → 发布制品），场景包自身不写业务事实。
4. **事件**：依赖 O6「GFIS→GPC 单向事件合同 v0.1」交付；缺事件时以只读查询兜底并在证据中标注。

### 接口（草案）
| 接口 | 方向 | 语义 |
|---|---|---|
| `fact:query` | AAAS/场景包 → GFIS/GPC（经 KDS 投影或只读 API） | 按包声明的 factRefs 取数 |
| `event:subscribe` | 事件合同（O6） | 订单/库存/质量/发货/签收事件 |
| `xap:intake` | 场景包 → WAME | 回写/状态变更走 XAP 请求包 |

### 数据模型（草案）
`ServicePackage.xwailBinding{schemaVersion, profileVersion, factRefs[]}`；`FactRef{sourceSystem, objectType, keyFields[], asOfPolicy}`；`EvidenceRequirement` 引用 B4 强度档。

### 门禁
包发布前须过 WAME 注册与 XWAIL 校验（`validate_aaas_binding.py` 缺失项先补，implementation_pending）；事实只读红线（GFIS/GPC 唯一写）；无真实 source-of-record 时不得声明真实 E2E。

### 落地
S1：Schema 草案 + `validate_aaas_binding` 补建；S4：企业层首个场景包接入（SKU-07 客户）。**CHG 需求：CHG-17（场景包契约）**，属主 AAAS/XWAIL。

### 风险
事件合同未就绪 → 只读兜底 + 证据标注；场景包字段膨胀 → Profile 特化，不改基础语义。

---

## 4. 三缺口的关系

```text
SOP（流程编排） ──提供审批流与业务流规则包──▶ 场景包（企业层）
KDS/WAS（产业语义与只读投影） ──兜底──▶ 城市层（ICP pause 期间）
场景包（AAAS） ──只读事实 + XAP 写回──▶ GFIS/GPC 业务事实
```

顺序建议：PKG 契约（S1 可先行，与 O6 并行）→ B8 补链（S1 审批流）→ ICP 评估（S5 前）。

## 5. 模型依据

| 决策点 | 模型 | 概率 |
|---|---|---|
| B8 补链方式 | StartLux priority_rank（dual-v1@0.3.0） | A 0.951 / B 0.039 / C 0.010 |
| ICP 城市层 | 同上 | A 0.670 / B 0.221 / C 0.108 |
| 场景包接口 | 同上 | A 0.947 / B 0.023 / C 0.030 |

### 5.1 决策记录（2026-10-25 老卢「全按推荐」）

- 三项裁决：①A（SOP 流程编排者/WAME 唯一裁决）②A（ICP 维持 pause，城市层 S5 前不含）③A（XWAIL Schema+只读投影+XAP 写回）。
- 已出单：`runtime/four-layer-workbench-20261025/S1-exec/CHG-16-18-缺口ADR变更申请单.md`（属主执行后纳入冻结基线 v1.1）。
- 本文件已转 controlled v1.0 并登记台账（2026-10-25 老卢「确认」）。

## 6. 非声明边界

本文为缺口分析与 ADR 草案：不声明任何缺口已修复；三份 ADR 须经 CHG-16/17/18 纳入冻结基线（61 号文变更流程）后方可作为实施依据；不改既有受控件与项目仓。
