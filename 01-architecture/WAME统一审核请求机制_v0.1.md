---
doc_id: GPCF-DOC-WAME-UNIFIED-REQUEST-MECHANISM-20261011
title: GlobalCloud 项目群 · WAME 统一审核请求机制 v0.1
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAME, KDS, Brain, GPCF, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/WAME统一审核请求机制_v0.1.md
source_path: 01-architecture/WAME统一审核请求机制_v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 · WAME 统一审核请求机制 v0.1

- 日期：2026-10-11 ｜ 性质：**机制设计件**（项目群级）——提交侧（WAS/XWAIL）产出；WAME/PVAOS 实现随其流程
- 提出：老卢（2026-10-11 表述核验与机制化）｜实施：WAS/XWAIL 契约线
- 依据：《XWAIL 可扩展世界资产信息建模语言规范 V1.2 草案》§2.3（本次同步补）、XWAIL V1.2-07 规则（本次登记）

## 一、问题陈述（核验结果：阻点风险成立）

**老卢表述核验**：
1. 「WAME 承担注册、审核、发布」→ ✅ 既有职责（《WAME 总体方案》§4：承接 XWAIL 模型注册、授权、发布和证据展示）；
2. 「其它系统的审核请示不能被识别 → WAME 成为阻点」→ ✅ **现实证据充分**：GPCF `docs/harness/evidence/` 现有 **≥15 份风格各异的请求件**，无一具备统一封套：

| 类 | 既有样本（节选） | 格式 |
|---|---|---|
| 执行授权请求 | agent-reach P7／P8／P9×2（2026-06） | 各自定制 JSON |
| 准入/受理 | codegraph-dev-admission；cognee-full-run-admission | 各自定制 |
| 域登记请求 | IGL-graph-domain（2026-10-11）；CWME-space-domain（2026-10-11） | 各自定制 JSON |
| 修复请求链 | GCKF P0 repair-request 链 d174→d181 | 长链专用格式 |
| 词表请求 | registry_vocab_review（state×1＋term×8） | MD 清单 |
| 发布物登记 | XAP 包族 5 份（本次） | XAP manifest |

**结论**：**没有统一识别机制**——WAME 侧面对 N 种格式无法通用受理、无法自动分流、无法回执闭环——**阻点风险成立，须建立统一机制**。

## 二、机制设计（统一请求原则）

> **凡发往 WAME 的审核/注册/发布请示，一体封装为符合 XWAIL XAP 规范的「请求包」（Request XAP）**。

### 2.1 两类包（XAP 包族统一）

| 包类型 | `packageKind` | 内容 | 现有实例 |
|---|---|---|---|
| **资产包** | `asset` | 模型 + manifest + 证据（既有 5 包模式） | gehua-e01／gehua-full／city-spatial-wenbo／huangmei-01／pva-bmw |
| **请求包** | `request` | 请求信封 + 请求体 + 证据（本次新增） | 见 §三 样本（由既有请求改造） |

### 2.2 请求类型学（`requestType` 枚举 · 映射既有请求）

| requestType | 用途 | 既有样本映射 |
|---|---|---|
| `asset_registration` | 资产/域包注册（含模型） | XAP 5 包；域切片登记请求 |
| `domain_registration` | 域/域切片登记 | IGL-graph；CWME-space-domain |
| `term_request` | 术语/词表增补 | registry_vocab_review（term×8） |
| `state_request` | 状态词表增补 | 同上（state×1：rejected） |
| `authorization` | 执行授权 | agent-reach P7-P9×4；codegraph；cognee |
| `repair_request` | 修复请求 | GCKF P0 链 d174-181 |
| `other` | 兜底（须显式说明） | — |

### 2.3 请求信封（统一识别字段）

```text
XAPRequestEnvelope v0.1（最小必填）：
  packageId          唯一包标识（前缀 xap.request.*）
  packageKind        "request"
  requestType        §2.2 枚举
  from               提交方系统（枚举：kds｜cwme｜gfis｜pvaos｜studio｜brain｜gpc｜pqc｜xwail｜其他登记值）
  to                 "wame"（固定）
  subject            请求对象（描述＋refs：对象/域/术语 id）
  requestedDecision  期望裁定（如 admit_xap_import_interface_candidate）
  evidenceRefs[]     证据引用（可核验路径/摘要）
  constraints{}      scope 绑定／限域声明／non-claims
  createdAt          日期
```

**回执（Receipt）**：`receipt{requestId, decision, decidedAt, authority, refs}`——**decision 一律由治理方填写**（留白纪律）。

## 三、受理流程（识别 → 分流 → 裁定 → 回执）

```text
提交方（各系统）→ 封装请求包（工具/模板）→【WAME 受理器】识别（packageKind=request → requestType 分流）
→ 四级检验：①信封（本机制）②包（XAP 校验）③模式（V1.2-06 modecheck）④证据（引用可核验）
→ 分流（登记/词表/授权/修复各归其道）→ 治理裁定 → 回执回写（requestId 关联）→ 归档
```

**四级检验实现分工**：①③④ 提交侧工具已就绪（本次：`requestcheck.py`＋`modecheck.py`＋校验链）；②**按 `packageKind` 分流**——**纯请求包**（无 models）：资产包字段（version／三维基线／models 等）**不适用**（分流 N/A）；**混合包**（含 models）追加 `validate_xap_manifest` 校验——已实证（requestcheck v2 R08；**修复 2026-10-11 Codex 审计 P0**：「旧 XAP 校验器对请求包报 9 项」的串联断裂）；**WAME 受理器**＝其实现侧（本机制给规范与工具，实现随其立项）。

## 四、实施规划（四阶段）

> **路线映射（2026-10-11）**：本表 S1-S4 ＝《XAP统一治理交换协议_Codex提案采纳意见_v0.1》**P0-P4 基准路线**的子集（S1≈P0 部分已完成；S2≈P0-P1 间；S3＝P3 预置；S4＝P1-P2 的受理器部分）。后续按 **P0-P4** 口径陈述推进。

| 阶段 | 内容 | 责任侧 | 就绪度 |
|---|---|---|---|
| **S1 规范与工具**（本轮） | 规范 §2.3＋V1.2-07 规则；`requestcheck.py`；两样本改造（既有请求→请求包） | WAS/XWAIL（我们） | ✅ 本轮完成 |
| **S2 试点** | 既有请求分批改造为标准请求包：①IGL 域登记（追溯）②CWME 空间域（在审）③registry 词表 ④GCKF repair 链（d174-d181 段）——**4 件齐**（KDS `工业绿链/图谱/ontology/requests/`，requestcheck 4/4 过）；覆盖 3 种 requestType（domain_registration×2／term_request／repair_request） | 提交方＋我们 | **✅ S2 完成（2026-10-11）** |
| **S3 各系统接入** | 分批：KDS/CWME → PVAOS/Studio → GFIS/Brain/GPC → 其余（26 成员目录） | 各系统（用我们工具） | **🔧 工具包就绪（2026-10-11）**：《请求包制作指南》＋`mkrequest.py`（制作→自检闭环实证）；待各系统陆续使用 |
| **S4 受理器实现** | WAME 侧统一受理器（识别/分流/裁定/回执/发布） | **WAME 项目**（其流程） | **✅ 参考实现可用（2026-10-11）**：`server/xap-intake`（受理器＋33 项验收＋WAE 内「受理台账」UI）；生产化随 WAME 上线流程 |

## 五、边界与不声明

- 本机制**不改 WAME/PVAOS/GCXWAIL 仓**；为提交侧机制设计＋规范建议；
- 受理器**参考实现**已可用（`GlobalCloud WAES/server/xap-intake`：P1 受理闭环＋P2 资产交付闭环＋WAE 受理台账 UI；33 项验收全过）——**不声明**已生产化、已由任何真实系统上线治理；**不声明**任何请求已裁定（decision 留白纪律在受理器中代码级强制）；
- 「所有系统」范围以项目群成员目录为准（26 项——**分批接入**，不搞一刀切）；
- 轻量请求（term/state）允许**最小请求包**（无 models，仅信封＋请求体）——**均符合 XAP 规范**（「均应」的落地口径）。

## 六、随附产物（本轮）

| 产物 | 位置 |
|---|---|
| 规范增量 §2.3（打包 XAP：asset／request 两类） | GPCF `01-architecture/XWAIL…规范V1.2草案.md` |
| V1.2-07 规则行（请求包检查） | GPCF `01-architecture/XWAIL-V1.2-Validator规则清单.md` |
| `requestcheck.py`（信封检查器）＋两样本 | KDS `工业绿链/图谱/ontology/xwail-v12-poc/` |
| XAP 受理器（参考实现）＋WAE 受理台账 UI | WAME `server/xap-intake/`（分支 `waes/world-asset-studio`） |
| 本机制文件 | GPCF `01-architecture/WAME统一审核请求机制_v0.1.md` |
