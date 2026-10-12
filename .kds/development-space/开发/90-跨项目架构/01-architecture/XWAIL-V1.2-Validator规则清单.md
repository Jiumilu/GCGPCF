---
doc_id: GPCF-DOC-XWAIL-V12-VALIDATOR-RULES-20260623
title: XWAIL-V1.2-Validator规则清单
project: GPCF
related_projects: [GPC, PVAOS, WAME, KDS, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/XWAIL-V1.2-Validator规则清单.md
source_path: 01-architecture/XWAIL-V1.2-Validator规则清单.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# XWAIL-V1.2-Validator规则清单

> **文档状态**：draft（正文填充 2026-10-11；此前为占位框架）
> **依据**：《XWAIL可扩展世界资产信息建模语言规范V1.2草案》
> **实现基线**：GCXWAIL `scripts/xwail_common.py`（1.1 工程化）
> **本清单双重用途**：①对 1.1 已实现规则的**如实对账**；②1.2 补规则的**唯一排期表**。
> **输出格式**：`ValidationIssue{code, severity, path, message}`；门禁报告含 `status / checked / issue_count / high_count / boundary`。

## 1. 已实现规则（1.1 工程化基线 · 实可运行）

| 码 | 严重度 | 检查内容 |
|---|---|---|
| XWAIL-1001 | high | JSON 解析失败；`kind ≠ XWAILModel`；`xwailVersion` 缺失；资产/关系结构非法；资产 ID 重复 |
| XWAIL-2001 | high | `assets` 为空或非列表 |
| XWAIL-2004 | high | 资产缺 `id` |
| XWAIL-2005 | medium | 资产缺 `category` |
| XWAIL-2201 | high | 资产 `dimensions` 为空 |
| XWAIL-3001 | high | 关系自环（source = target） |
| XWAIL-3004 | high | 悬空引用（relations / flowRelations 的 source / target 不存在；结构非法） |
| XWAIL-5001 | high | `Authorized/Published` 缺 WAME 门证据（`wameEvidenceRef`）；pilotScope：授权对象/动作缺失或越权、promotionBlockers 规则、Active 前置条件（WAME 状态 / blockers 清零 / 非 candidate 引用） |
| XWAIL-6002 | high | `wameStatus` 非 WAME 生命周期枚举；pilotScope `admissionStatus` 非法 |
| XWAIL-7001 | high | `wasBaseline` / `ontologyVersion` 缺失；资产 `ontologyRef` 缺失；八维缺失；`lifecycle.states` 缺失；pilotScope 必填字段缺失 / `ontologyRef` 非 `was:` 前缀 |
| XWAIL-9001 | high | `flowType` 非八流枚举；`flowRelations` 结构非法 |
| XAP-1001 | high | manifest 必填字段（packageId / version / wasBaseline / ontologyVersion / xwailVersion / wameStatus / decision） |
| XAP-1002 | high | manifest `wameStatus` 非枚举 |
| XAP-1003 | high | manifest `decision` 非枚举（compatible / migration_required / deprecated / blocked） |
| XAP-2001 | high | manifest `models` 为空或非列表 |
| XAP-2002 | high | 模型项缺 `path` |
| XAP-2003 | high | 模型文件不存在 |
| XAP-2004 | high | 模型摘要（sha256）不一致 |
| XAP-5001 | high | `Authorized/Published` XAP 缺 WAME 门证据 |

（合计运行码：XWAIL 11 个 + XAP 8 个 = **19 个**。）

## 2. 目标规则（规范首批 22 码清单 · 未实现部分对账）

| 码 | 严重度 | 检查 | 状态 |
|---|---|---|---|
| XWAIL-3002 | high | composition 循环 | 未实现（阶段 2 图语义） |
| XWAIL-4004 | medium | 状态机缺 EventPriority | 未实现 |
| XWAIL-4101 | medium | Transition 缺事件或超时 | 未实现 |
| XWAIL-4102 | medium | SideEffect action 未登记 | 未实现（需 action registry） |
| XWAIL-4103 | medium | scope 非法或不存在 | 未实现（需 scope registry） |
| XWAIL-6001 | high | 嵌套层级超限 | 未实现 |
| XWAIL-6006 | medium | 模板依赖过深 | 未实现（需模板机制） |
| XWAIL-6007 | high | 局部覆盖违反组织策略 | 未实现（需 org-policy） |
| XWAIL-8001 | high | 快照缺模型或策略版本 | 未实现（阶段 6 Trusted） |
| XWAIL-8002 | high | 证据引用不可解析 | 未实现（阶段 6 Trusted） |
| XWAIL-9002 | medium | 单位 / 货币 / 坐标 / 时区非法 | 未实现 |
| XWAIL-9502 | high | 模板 / 作用域 / 跨文档引用不存在 | 未实现 |

（对账注记：清单原 22 码中，`XWAIL-5001` 原定义为「Integration 未绑定 SecurityProfile」，1.1 实现将其承载为「WAME 门证据 + pilotScope 检查」——语义指派变化待评审统一；实现另含清单外语义（pilotScope 系列）。）

## 3. V1.2 增量规则（规划 —— 正式编号发布时分配）

| 规划项 | 严重度（建议） | 检查 | 依赖 |
|---|---|---|---|
| V1.2-01 回指完整性 | high | `wasBaseline / ontologyVersion / profile / ontologyRef / termVersion` 五件回指齐全 | 规范 §5.1；**PoC 参考实现**：KDS `工业绿链/图谱/ontology/xwail-v12-poc/`（2026-10-11，5/5 实证） |
| V1.2-02 兼容矩阵前置 | high | 发布候选附六维版本兼容矩阵（WAS × Ontology × XWAIL × Profile × ServicePackage × WAME status） | 规范 §5.2；**PoC 参考实现**：KDS `工业绿链/图谱/ontology/xwail-v12-poc/`（compatcheck.py ＋ compat-matrix.yaml 格式提案，6/6 实证，2026-10-11） |
| V1.2-03 Profile 白名单 | high | 模型 `profile` 必须位于登记白名单 | 规范 §3.2；登记载体待定；**PoC 参考实现**：KDS `工业绿链/图谱/ontology/xwail-v12-poc/`（profilecheck.py ＋ profiles-registry.yaml 载体提案，6/6 实证，2026-10-11） |
| V1.2-04 pilotScope 口径对齐 | high | `admissionStatus` 大小写统一（**以 WAS 契约为准：小写 7 值** draft/candidate/authorized/active/closed/archived/blocked）；wasLayer 枚举对齐（三层 world/industry/scenario） | **WAS 侧已完成（2026-10-11）**；GCXWAIL 侧待其流程（现值=大写 7 值；落点：`xwail-pilot-scope.schema.json` ＋ `xwail_common.py` PILOT_ADMISSION_STATUSES） |
| V1.2-05 WAME 边界扩展 | high | WAME 边界检查扩展到 Profile / XAP 全族（部分已实现：XWAIL-5001 / XAP-5001） | 规范 §6；**PoC 参考实现**：KDS `工业绿链/图谱/ontology/xwail-v12-poc/`（wamecheck.py 三族四规则统一截面，7/7 实证，2026-10-11） |
| V1.2-06 导入模式检查 | medium | 三种导入模式包侧预检：M1 `packageId` 唯一性／M2 对象级比对（新增/跳过/**冲突挂起不自动合并**）／M3 只读零写断言 | **PoC 参考实现**：KDS `工业绿链/图谱/ontology/xwail-v12-poc/`（modecheck.py ＋ 目标状态样本，5/5 实证，2026-10-11）；接口语境＝WAS《接入点_WAME包登记_v0.1》§二 |
| V1.2-07 请求包检查 | medium | 请求包（`packageKind=request`）：信封 6 规则（含**留白纪律全字段扫描**——跳过 traceability 引述区）＋**R07 引用格式/存在性**＋**R08 包级分流**（纯请求包：资产包字段 N/A；混合包：追加资产包校验） | **PoC 参考实现 v2**：KDS `xwail-v12-poc/requestcheck.py`（12/12 实证含 2 新负例，2026-10-11；含 Codex 审计 P0/P1 修复）；机制＝GPCF《WAME统一审核请求机制_v0.1》§三；规范 §2.3 |

## 4. 严重度与阻断策略

- `high`：阻断生产发布（CI fail）。
- `medium`：默认阻断 Operational 与 Trusted 发布；经 policy 豁免须显示 `waiverRef`。
- 豁免与规则变更：保留 changelog 与兼容说明（见《XWAIL实施方案.md》§9 回滚方案）。

## 5. 运行入口

```bash
python3 scripts/validate_xwail.py <model.xwail.json>
python3 scripts/build_xap.py <pkg> --lock
python3 scripts/verify_xap.py <pkg>
```

## 6. 边界

校验器成功 ≠ WAME 发布、AaaS 绑定、业务交付或客户验收。

## 7. 对账方法注记

§1 系 2026-10-11 对 `scripts/xwail_common.py`（286 行）的逐码对照；§2 / §3 为实现排期项。实现状态一律以 GCXWAIL 仓实际输出为准，本清单不替代运行结果。
