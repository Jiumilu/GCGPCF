---
doc_id: GPCF-DOC-785AEA3125
title: GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md
source_path: 02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词

## 1. 方案定位

本文是 `GlobalCloud 项目群实施方案` 下的 WAS/Ontology 专项全量实施入口，用于把 WAS 顶层语义、Ontology 语义契约、XWAIL 机器契约、WAES 门禁、KDS 证据和 LOOP 运行控制闭环纳入同一实施链路。

本文不替代 `WAS世界资产体系总体方案`，不替代各项目当前有效实施方案，也不声明 WAS/Ontology 已经业务上线、客户交付完成、accepted、integrated 或 production_ready。

## 2. 继承链路

```text
WAS世界资产体系总体方案
  -> GlobalCloud 项目群实施方案
  -> GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词
  -> WAS / XWAIL / WAES / GFIS / GPC / PVAOS / KDS / Brain 项目实施方案
  -> LOOP round / Harness evidence / validator
```

本链路固定以下边界：

- WAS 定义资产世界、八维、八流、生命周期和治理原则。
- Ontology 只提供语义知识层和候选推理解释，不替代 XWAIL、GFIS、GPC、PVAOS 或 KDS source-of-record。
- XWAIL 负责机器契约、Profile、Schema、Validator 和迁移规则。
- WAES 负责注册、授权、发布、治理、证据审查和状态门禁。
- KDS 是受控知识与证据引用主存；Brain 输出默认是候选。
- GPCF 只负责 LOOP、Harness、文档治理、证据台账和门禁，不替代项目实现。

## 3. 当前监控状态

| 项 | 当前值 |
|---|---|
| latest_monitor_round | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100` |
| next_monitor_round | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101` |
| latest_precheck_execution | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-EXECUTION-015` |
| current_gate | `hold_required=1` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

当前 `docs/harness/intake` 仍只有模板，真实 P4 candidate 文件数为 0。任何测试数据、治理 validator、KDS 候选、用户口述、报价材料、合同审阅稿、Loop 文档或 mock evidence 都不得替代真实 source-of-record。

## 4. 实施分层

| 层级 | 实施对象 | 最低交付物 | 当前状态 |
|---|---|---|---|
| L0 体系控制 | WAS 总体语义和项目群实施主方案 | 总体方案、项目群实施方案、实施控制台账 | `controlled` |
| L1 语义契约 | Ontology / XWAIL profile | 术语、字段、crosswalk、validator | `candidate` |
| L2 Source Record 门禁 | GFIS/GPC/PVAOS 到 WAS/Ontology 的真实源记录 | intake checklist、negative fixtures、precheck | `hold_required` |
| L3 WAES 审查 | WAES review / runtime intake / review queue | 审查包、权限、回滚、审计 | `blocked_without_real_source_record` |
| L4 KDS/Brain 候选解释 | 受控 RAG、候选推理、知识回指 | KDS backlink candidate、Brain candidate explanation | `candidate_only` |
| L5 交付验收 | 客户/UAT/签收/发布 | UAT 记录、签收、发布批准 | `not_collected` |

## 5. LOOP 运行控制闭环

每次推进 WAS/Ontology 实施必须按以下结构登记，不得退回旧五段式作为唯一记录：

```yaml
run:
  input: 总体方案、项目群实施方案、当前 monitor evidence、真实 source-record 接收目录
  action: 执行 precheck、negative fixtures、crosswalk、profile mapping、WAS validator
  output: evidence、loop round、validator output、状态台账更新
stop:
  stop_type: authorization_boundary 或 blocker
  stop_evidence: 缺真实 P4 candidate、缺用户确认、缺 WAES 审查或门禁失败
verify:
  commands:
    - python3 tools/kds-sync/validate_project_group_implementation_plan.py
    - python3 tools/kds-sync/validate_project_implementation_register.py
    - python3 tools/kds-sync/validate_was_real_source_record_monitor_100.py
    - python3 tools/kds-sync/validate_was_status_matrix_control_board_refresh.py
recover:
  rollback: 回退本轮 evidence、loop round、validator 和状态台账；不涉及生产回滚
debug:
  next_round: GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101
  boundary: no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready
```

## 6. 全量执行提示词

```text
你正在执行 GlobalCloud 项目群 WAS/Ontology 全量实施链路。

先读取 AGENTS.md、WAS世界资产体系总体方案、GlobalCloud 项目群实施方案、实施方案控制台账、核心链路真实证据台账、LOOP_CONTROL_BOARD 和最新 WAS monitor evidence。

本轮目标只能是推进受控实施链路、真实 source-record 准备度、门禁 replay、证据台账或下一轮输入。不得把文档、模板、mock、测试数据、KDS 候选、用户口述或治理 validator 写成真实业务完成。

如果 docs/harness/intake 没有真实 P4 candidate，则必须保持 hold_required=1、real_source_records=0、valid_source_records=0、runtime_primary_key_ready=0、review_queue=0、runtime_intake=0、waes_review=0、verified=0、accepted=false、integrated=false、production_ready=false。

每轮输出必须包含 run、stop、verify、recover、debug，并说明下一轮是否进入 GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101 或后续 monitor。
```

## 7. 下一轮候选

| 优先级 | Round | 目标 | 边界 |
|---|---|---|---|
| P0 | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101` | 继续监控真实 P4 candidate 文件提交，并复核数字产品护照、公开披露、二维码/数据载体、追溯数据集、访问治理和检索回执边界 | 无真实输入时继续 hold |
| P0 | `WAS-IMPLEMENTATION-CHAIN-GATE-001` | 将 WAS/Ontology 全量实施方案纳入项目群实施方案门禁和台账 | 只做治理门禁，不升级验收状态 |
| P1 | `WAS-XWAIL-WAES-RUNTIME-CONTRACT-001` | 定义 XWAIL profile 到 WAES runtime contract 的最小验证清单 | 不写生产、不发布 |
| P1 | `WAS-KDS-BRAIN-CANDIDATE-EXPLANATION-001` | 建立 KDS/Brain 候选解释不越权规则 | Brain 输出仍为 candidate |

## 8. 非声明边界

本文不声明：

- 不声明真实 P4 source-record 已提交；
- 不声明 GFIS/GPC/PVAOS 真实业务事实已形成；
- 不声明 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact 已创建；
- 不声明 KDS 正式事实写入或 Brain 推理结果已进入主账；
- 不声明客户交付、UAT、签收、accepted、integrated 或 production_ready。
