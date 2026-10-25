---
doc_id: GPCF-DOC-GROUP-ARCH-RECONSTRUCT-20261025
title: GlobalCloud 项目群总体架构重构（四层体系冻结版融合）
project: GPCF
related_projects: [WAE, WAME, WAS, XWAIL, KDS, GCMEM, MMC, PVA, AAAS, GFIS, GPC, SOP, PQC, SLC, PDC, PKC, XGD, XiaoG, XiaoC, World, ICP, SpaceAI, DRC, PMC, FireQuote, "GlobalCloud Token"]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud项目群总体架构重构_v1.0.md
source_path: 01-architecture/GlobalCloud项目群总体架构重构_v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群总体架构重构（四层体系冻结版融合）v1.0

日期：2026-10-25　状态：controlled v1.0（2026-10-25 老卢确认转正）
**输入**：session `5f142487-1887-49f7-9f2a-f7cc5e70b31f` **冻结基线 v1.0**（00–68 号文；权威入口 53 总纲、61 设计冻结、54 决策总台账 Q0–Q96、56 回写清单、48 第二批架构更新）
**性质**：群级架构重构分析。**不修改既有受控件**；回写按 CHG-14/15 由属主执行，须 G5。
**对 v0.1 的替代**：v0.1 基于会话中期（六基座版本）撰写，已被冻结版取代——本版按九基座/OPC/统一引擎/四业务/两形态重写。

---

## 0. 结论先行

1. **重构后的项目群总体架构 = 五面模型**：①架构层 L0–L7（供给，不变）②产品域四档（消费：个人 OPC/团队/企业/城市）③共享基座 B1–B9（九契约）④执行引擎与编排面（Hermes 统一主 runtime，不替换）⑤业务体系（四业务 × 两形态）。
2. **相对 v0.1 的五个实质变化**：基座 6→9（新增 B7 PMC 任务、B8 SOP 流程、B9 Token 模型供给）；个人层从「PKC+XGD」升级为 **OPC 一人公司**（六角色/双轮/远程 FDE/Paperclip）；新增**执行引擎面**；业务体系从「平台+交付」扩为**四业务×两形态**；项目计数 **29→30**（Studio 已退出、WAES 作废、Token 待登记）。
3. **三处结构性缺口**（会话 18 号文识别，重构必须处理）：SOP 未纳入四层授权/审批链；ICP 在城市层缺位；绿链业务系统（GFIS/GPC/PQC…）与企业层场景服务包接口未定义。
4. **回写责任明确**：群级方案回写=CHG-14（属主 GPCF）；AaaS 方案族=CHG-15（属主 AAAS）；10 个项目需改、15 个不需改（18 号文）。
5. **设计已冻结**：变更唯一通道=CHG（61 号文）；本文件的回写动作属执行项，不改变冻结设计。

---

## 1. 重新分析：相对 v0.1 的五个实质变化

| # | v0.1（会话中期） | 冻结版 v1.0 | 架构含义 |
|---|---|---|---|
| 1 | 六项基座 B1–B6 | **九项 B1–B9**（+B7 任务与工作单→PMC；+B8 流程与规则→SOP；+B9 模型供给→GlobalCloud Token） | 基座轴扩为九契约；新增「任务/流程/模型」三条跨层供给 |
| 2 | 个人层=PKC 主载体+XGD 内核 | **OPC 一人公司**：六角色（渠道/客户/伙伴/服务者/FDE 服务商/供应链服务商）、双轮（OPC 经营+PVA 商业接入）、远程 FDE、AI 员工编制（Paperclip） | 个人层从「工具」升级为「经营单元」；新增与 PVA 的外部商业关系（非 Membership） |
| 3 | 未定义统一执行引擎 | **Hermes Agent（gateway :8642）= 四层统一主 runtime，工作台可替换、引擎不替换**；DSH 并行；XiaoG/Multica/Paperclip 为壳与编排 | 架构新增**执行引擎面**；L6 AI 能力层语义从「三个 AI 项目」变为「能力供给 + 统一引擎」 |
| 4 | 业务=平台协同+商业交付 | **四业务**（平台买入口/供应链买交易/FDE 买时间/数据买资产）× **两形态**（形态 A 全域 SaaS / 形态 B 政府企业私有云，数据不出域） | 架构新增「业务体系面」与「部署形态」维度；城市层只走形态 B |
| 5 | 29 项登记、Studio 在册 | **30 项**：Token 新建（CHG-12 待登记）；Studio 退出（归档 `_archive/2026-10-25-studio-retired/`）；WAES 作废 | 注册表与架构图 §8 矩阵须回写（CHG-14） |

---

## 2. 重构后的总体架构（五面模型）

```text
┌── 面1 产品域轴（四档 · 消费方 · 不进 L1–L7）────────────────────────────────┐
│ 个人 OPC（六角色/双轮/远程 FDE）· 团队 XiaoG · 企业 PVA+WAME · 城市 World 联邦 │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │ 经 WAE 壳装配 → Hermes 统一引擎执行
┌── 面2 执行引擎与编排（工作台可替换、引擎不替换）───────────────────────────┐
│ Hermes Agent :8642（统一主 runtime）· DSH（并行）· XiaoG（团队载体）          │
│ · Paperclip（AI 员工编排：个人本地 + 中心多公司两实例）· Multica（补充）     │
│ · StartLux（决策 gate/decide/rate）· WAE（唯一壳）                          │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │ 调用九项基座契约
┌── 面3 共享基座轴（B1–B9 · 契约不新造项目）─────────────────────────────────┐
│ B1 身份租户 · B2 记忆知识 · B3 授权链 · B4 证据链 · B5 壳装配                │
│ B6 计量分档 · B7 任务工作单 · B8 流程规则 · B9 模型供给（Token）             │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │ 落点：既有项目承载
┌── 面4 架构层轴（L0–L7 + 横切 A/B · 供给方 · 既有分层不变）──────────────────┐
│ L0 宪法 → L1 入口(WAE) → L2 治理(WAME/GPCF/MMC/SOP/ICP) → L3 平台(GPC/PVA/    │
│ PQC/SLC/AAAS) → L4 执行(GFIS/Edge) → L5 知识(KDS/GCMEM/Brain/PKC) →          │
│ L6 AI(XiaoC/XiaoG/XGD) → L7 工程(PMC/Harness 规范·Studio 退出)               │
│ 横切 A WAS 语义契约 · 横切 B WAS 运行时链                                     │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │ 支撑
┌── 面5 业务体系（四业务 × 两形态）────────────────────────────────────────────┐
│ 平台（买入口）· 供应链（买交易）· FDE（买时间）· 数据（买资产）               │
│ 形态 A 全域 SaaS（多租户）｜形态 B 政府/企业私有云（单租户、数据不出域）      │
│ 界面：WAE 三版工作方式（列表/操作/证据中心）+ DESIGN v2 产品界面体系          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 九基座（B1–B9）与落点

| # | 基座 | 落点（既有项目） | 重构后要求 |
|---|---|---|---|
| B1 | 身份与租户 | WAE idp-kit（身份权威）/ PVA（租户/组织主账）/ MMC（服务令牌/scope） | Identity/Membership/Grant 三分；Tenant→Org→Workspace 谱系；禁止各自签发会话 |
| B2 | 记忆与知识 | GCMEM（唯一写口）/ KDS（知识正本） | 四级命名空间 personal/team/org/city；meta v3；本地库降级为缓存 |
| B3 | 授权链 | WAME（裁决）+ WAE 写门禁 + MMC + StartLux（红线） | 一条链；L4 恒拒；AI 只到 L1–L3 |
| B4 | 证据链 | WAME Evidence Ledger（唯一运行证据主账）+ GPCF（只判门禁） | S1–S4 证据强度分档 + hash + 互链 |
| B5 | 壳与装配 | WAE（app-registry + assembly 加 tier） | 不建 app-shell；`apps/wame` 收口先于任何 tier 装配 |
| B6 | 计量与分档 | AAAS（四档 ServicePackage + SKU-07 + AIWorkUnit） | 四档包；个人免费/团队 seat/企业 license+计量/城市项目制 |
| B7 | 任务与工作单 | **PMC**（四层任务中枢） | 每 Tier 一 workspace；只写任务状态，不写业务事实/交付验收/知识正本 |
| B8 | 流程与规则 | **SOP**（审批流/业务流/会话治理/规则装配/过程审计） | Q20=C 分阶段（S1 审批流 → S4 全流程）；**须补入四层授权链**（缺口①） |
| B9 | 模型供给 | **GlobalCloud Token**（聚合网关：多模型接入/路由降级/限流/计量/凭据托管/本地模型；LiteLLM MIT 基座 + 薄自研） | 成本中心+加价；与 MMC 分工（Token 不持模型主账）；项目 29→30 待登记 |

### 2.2 四层 × 架构层消费矩阵（九基座版）

| 产品域 | 强依赖架构层/项目 | 强依赖基座 | 定价口径 |
|---|---|---|---|
| 个人 OPC | L1 壳(WAE) · L5(PKC/KDS/GCMEM) · L6(XGD) | B1/B2/B5（+B9 模型供给） | 不单独收费（BYO-Key/个人额度） |
| 团队 | L1 壳 · L6(XiaoG) · L2(WAME 审批/证据) · L5(GCMEM team) | B1/B2/B3/B5/B7/B8 | seat 订阅（SKU-01 子档） |
| 企业 | L1 · L2(WAME/MMC/GPCF) · L3(PVA/AAAS) · L5 · 横切 A | B1–B9 全量 | license + 计量（SKU-01/02/03/04）+ SKU-07 |
| 城市 | L1 · L2 · 横切 A/B · L3(PVA 联邦) · L5 | B1–B9 全量（证据极强档） | 项目制 + 运营分成（SKU-05 冻结） |

### 2.3 项目重定位（30 项登记）

| 角色 | 项目 |
|---|---|
| 壳（唯一） | WAE |
| 内核/主载体 | PKC（个人主载体）、XGD（个人内核）、XiaoG（团队主载体+内核）、PVA（企业主载体）、WAME（企业/城市内核）、World（城市内核） |
| 基座组件 | GPCF（门禁）、MMC（令牌）、KDS（知识）、GCMEM（记忆）、PMC（任务）、SOP（流程）、AAAS（计量）、Token（模型供给） |
| 业务支撑/被消费 | GFIS、GPC、PQC、SLC、PDC、FireQuote、Brain、XiaoC、DRC、ICP、SpaceAI、SpaceAIStudio |
| 横切 | WAS、XWAIL（语义契约） |
| 退出/作废 | Studio（exit）、WAES（作废） |

**需改 10 项**（18 号文）：KDS/GCMEM/MMC/AAAS/PVA/WAME/GPCF/WAE/WAS-XWAIL/PMC；**不需改 15 项**；Token 新建。

---

## 3. 九基座数据流（重构后）

```text
身份流：Identity(WAE idp) → Membership(PVA Org/Workspace) → Grant(资源域) → 会话/令牌(MMC scope)
记忆流：四层 → GCMEM 唯一写口(ns: personal/team/org/city) → KDS 知识正本；本地库=缓存
授权流：身份 → 角色写上限 → 总闸(默认关) → 点名 → L3 人工 → 幂等；L4 恒拒；StartLux 红线
证据流：运行事实 → WAME Ledger(hash+authz_id/usage_id 互链) → 对账/SLA；GPCF 只判
任务流：四层任务/工作单 → PMC(每 Tier 一 workspace) → 只写任务状态
流程流：SOP 审批流/业务流/会话治理/规则装配 → 挂 WAME 授权与证据（缺口①待补）
装配流：WAE app-registry + assembly(tier) → module-kit → 四层工作台（同壳不同装配）
计量流：ServicePackage(四档) → AIWorkUnit 采样 → UsageRecord → 账单/对账；Token 计量加价
模型流：Hermes/各层 runtime → Token 聚合网关(多模型/路由/降级/限流) → 云 provider 或本地模型
```

---

## 4. 结构性缺口与重构动作

### 4.1 三处结构性缺口（18 号文识别）

| # | 缺口 | 影响 | 重构动作 |
|---|---|---|---|
| S1 | **SOP 未纳入四层授权/审批链**（授权链=MMC→WAME→WAE→L3，SOP 不在链上） | 四层审批流与治理链脱节 | B8 补入授权链（ADR-B8），S1 先审批流 |
| S2 | **ICP 在城市层缺位**（24 字产业模型/十一池投影未纳入城市层） | 城市层缺产业语义支撑 | 城市层前置评估（ICP 处置=pause 须裁） |
| S3 | **绿链业务系统与企业层场景服务包接口未定义**（GFIS/GPC/PQC…） | 企业层场景包无法引用绿链事实 | 定义场景包接口契约（挂 XWAIL/AAAS） |

### 4.2 回写清单（56 号文 → CHG）

| CHG | 属主 | 内容 | 本重构对应 |
|---|---|---|---|
| CHG-14 | GPCF | 群级总体方案回写：①项目计数 30 ②四层产品域章节 ③B9 ④四业务 ⑤两形态 ⑥界面体系；架构图加边界声明 | M1–M3 |
| CHG-15 | AAAS | AaaS 方案族回写（四业务/四档服务包/SKU-07/Token 加价/两形态/FDE 分层） | M5 |
| CHG-01/03/06 | GPCF/WAE | 边界声明、命名收口、WAE PRODUCT.md 重写 | M1/M4 |
| CHG-04/07/08/11/12/13 | AAAS/PMC/SOP/PVA/Token/WAE | 四档包、任务中枢、流程支撑、PVA 清理、Token 登记、DESIGN v2 | M5/M6 |

### 4.3 本文件的变更清单（M1–M6，均待 G5）

| # | 受控件 | 变更 |
|---|---|---|
| M1 | `GlobalCloud项目群系统架构图.md`（controlled） | §1 前加边界声明（四层不参与分层）+ §8 矩阵补 30 项 |
| M2 | `config/project-group-projects.yaml` | 29→30（Token 登记）、Studio 移除、WAES 标注 |
| M3 | `GlobalCloud 项目群总体方案.md` | 新增四层产品域/四业务/两形态/B9 章节 |
| M4 | 命名正名（文档层） | XGD 标题纠错、WAE/WAME 收口、PVA 命名统一 |
| M5 | AAAS 方案族 | 四档 ServicePackage + SKU-07 + Token 计量 |
| M6 | 六→九份基座 ADR | B1–B9（含 B7/B8/B9），挂 F-025 |

---

## 5. 实施路线与冻结变更控制

| 阶段 | 内容 | 门禁 |
|---|---|---|
| S0（已完成） | 设计冻结 v1.0 + S0 验证报告（60 号）+ MVP 实施清单（63 号）+ 实施准备（58 号） | 已过 |
| S1 | 口径与基座契约：边界声明、ADR B1–B9、命名正名、四档 ServicePackage + SKU-07、Token 登记 | G5；`gc_standard.py check` 0 error |
| S2 | 个人层 OPC 试点（PKC 承接体/WAE 个人装配/XGD 内核/GCMEM personal；Paperclip 个人实例） | Feature 立项；KDS 写入授权 |
| S3 | 团队层（XiaoG 限范围解冻、BSL 许可评估、成员/角色/隔离/审计四件、PMC 任务中枢） | Q5 授权；BSL 结论 |
| S4 | 企业层商业切片（PVA 组织 + WAE 企业装配 + WAME 证据 + AAAS SKU-07 + Hermes/Token） | 商业授权（G5） |
| S5 | 城市层（World + PVA 联邦 + 多中心 Hermes；只走形态 B） | 每单独立 G5 |

**冻结纪律（61 号文）**：设计变更走 CHG（白名单除外）；实施发现阻塞按执行协议先决策模型辅助再问答。

---

## 6. 风险与待办（执行项，非设计项）

| # | 事项 | 属主 | 风险 |
|---|---|---|---|
| R1 | Token 四件套 + 注册表 29→30（CHG-12） | GPCF | 不登记则架构图与注册表失配 |
| R2 | WAME 引擎/Evidence Ledger 落地（B4 前置） | WAME | 证据主账缺位 |
| R3 | PVA 组织树主数据 + 个人级接口（35 号文） | PVA | 企业层主账缺表 |
| R4 | SOP 入授权链（缺口①） | SOP/WAME | 审批流脱链 |
| R5 | ICP 城市层缺位评估（处置=pause） | ICP/GPCF | 城市层缺产业语义 |
| R6 | 绿链业务系统 ↔ 企业层场景包接口 | GPC/GFIS/AAAS | 场景包无法消费事实 |
| R7 | 性能验证 V1–V7（39 号文） | 平台 | 部署性能未实测 |
| R8 | 两形态客户归属口径（销售） | 老卢/销售 | 定价与交付边界 |

## 7. 图与资产

- 会话冻结版 4 图（archify v4/v5）：`runtime/four-layer-workbench-20261025/four-layer-{architecture,deployment,deployment-saas,deployment-private}.html`
- 本重构群级总览图：`.archify/architecture-reconstructed-overview-*/reconstructed-overview.html`（本版更新为五面模型）
- 一页纸总纲：53 号文；决策总台账：54 号文；冻结清单：61 号文

## 8. 非声明边界

本文为群级架构重构分析草案：不声明任何设计已实现、已计价、已上线或已验收；不修改既有受控件；所有回写与执行动作须经 G5；设计基线以 61 号冻结清单为准。
