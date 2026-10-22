---
doc_id: GPCF-DOC-7DBC7397B6
title: 目标判据证据：「≥3 个项目解除门禁阻塞」已达成（可审计）
project: KDS
related_projects: [GPC, WAME, KDS, XGD, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/goal-criterion-evidence-unblocked-20261022.md
source_path: docs/reports/goal-criterion-evidence-unblocked-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 目标判据证据：「≥3 个项目解除门禁阻塞」已达成（可审计）

- 目标判据原文：`≥3 个项目解除门禁阻塞`（90 天绝对量目标之一）
- 结论：**达成，去重后 5 个项目**（要求 ≥3）
- 审计方式：每条给出 Feature → 项目 → 前态 → 现态 → 证据（台账行 / 提交 / 队列可回读）

## 1. 逐条证据

| # | Feature | 项目 | 前态 | 现态 | 证据 |
|---|---|---|---|---|---|
| 1 | F-031 xgd-dot-alignment | **XGD** | blocked（六类证据齐但欠人工确认） | **closed / Recorder** | 决策台账 d021；提交 `403fa9cd4`；`features/done/F-031-*` |
| 2 | F-026 gcmem-governance-onboarding | **GCMEM** | blocked（理由：中央门禁 rework_required） | **closed / Recorder** | 台账 d022（unblock）；提交 `d4ea653eb` |
| 3 | F-027 governance-remediation | **GPCF** | blocked（方案未核验 + 历史 done 不合规） | **closed / Recorder** | 台账 d023 前置；提交 `d4ea653eb` |
| 4 | F-030 pdc-project-group-onboarding | **PDC** | blocked（tests/summary fail，根因是全群门禁） | **closed / Recorder** | 提交 `ab1212ba1`；属主重采后闭环 |
| 5 | F-015 org-readonly-vertical-slice | **Studio** | blocked（证据 pending） | **closed / Recorder**（随 Studio 退役结项） | 台账 d023；提交 `20bf4674b` |
| 6 | F-014 meeting-to-project-control | GPCF（同项目） | blocked（4 条授权类阻塞） | **evaluated**（授权已批，仅剩 B3 配置边界） | 提交 `9053ad6b2`/`f50f63924` |

**去重项目数**：XGD、GCMEM、GPCF、PDC、Studio = **5 个 ≥ 3 ✅**
（F-014 与 F-027 同属 GPCF，不重复计数）

## 2. 回读命令

```bash
# 当前队列态（应只看到 F-013 / F-021 仍为 blocked）
jq -r '[.queue[]|select(.status=="blocked")|[.id,.project]|@tsv]|.[]' runtime/queue.json

# 台账变更行
jq -r 'select(.kind=="close" or .kind=="unblock")|[.id,.kind,.answer]|@tsv' runtime/audit/decision-ledger-20261022.jsonl

# 证据文件存在性
ls features/done/{F-026,F-027,F-030,F-031,F-015}*
```

## 3. 仍然 blocked 的 2 项（不影响本判据）

| Feature | 项目 | 阻塞原因 | 需要谁 |
|---|---|---|---|
| F-013 | GPCF | KDS 脏工作树 + 4 文件 delta 待独立复核 | KDS 属主（请求函已出） |
| F-021 | World | Ontology 版本冲突（0.2.x vs 0.2.0） | WAS 属主裁定（函件已出） |

## 4. 非声明

- 本文件只证明"门禁阻塞解除"，**不证明**这些项目产品验收通过；
- 不得据此声明 accepted/integrated/production_ready/customer_accepted。
