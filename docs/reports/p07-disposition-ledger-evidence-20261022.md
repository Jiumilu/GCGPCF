---
doc_id: GPCF-DOC-0D0FBC993C
title: P07 · 29 项目处置台账 · 完成证据（2026-10-22）
project: GPCF
related_projects: [GPCF, WAME, PKC, XiaoG, Studio, ICP]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p07-disposition-ledger-evidence-20261022.md
source_path: docs/reports/p07-disposition-ledger-evidence-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P07 · 29 项目处置台账 · 完成证据（2026-10-22）

- 依据：Q6 裁定「15 项目整批授权」+ Q1「分母 29 纳入 FireQuote」
- 台账文件：`runtime/plan-20261022/decisions.yaml`（29 项）+ `runtime/audit/decision-ledger-20261022.jsonl`

## 1. 台账断言（实测）

```bash
python3 -c "import yaml;d=yaml.safe_load(open('runtime/plan-20261022/decisions.yaml'));p=d['projects'];
assert len(p)==29 and len({x['project'] for x in p})==29;
assert all(x['disposition'] in {'continue','merge','pause','exit'} for x in p);
assert all(x.get('decided_at') and x.get('auth_id') for x in p);print('decisions.yaml ok')"
jq -s '[.[]|select(.kind=="dispose")]|length' runtime/audit/decision-ledger-20261022.jsonl
```

结果：`decisions.yaml ok`；dispose 台账行 **16 条**（15 项目处置 + 1 批次行），满足 P07 的 ≥15 要求。

## 2. 处置分布

| disposition | 数量 | 项目 |
|---|---:|---|
| continue | 22（8 启动 + 14 retain） | 见 decisions.yaml |
| merge | 2 | XWAIL→WAME、PKC→WAE |
| pause | 4 | AAAS、XiaoG、ICP、World |
| exit | 1 | Studio（**保留在 29 分母**，`denominator_retained: true`） |

## 3. 合并/退出执行前清单（不随台账自动执行）

- XWAIL→WAME：受理域归属裁定 → 影子合并 → 3 消费方回放 → 注册表恢复行可回滚；
- PKC→WAE：F-036 注册完成 → `pnpm check:apps` pass → PKC 57 测试仍 pass；
- Studio 退出：F-015 已随退役结项 → GKE-001 STAGE-03 owner 改 WAE → 注册表标 deprecated（**不改 current_project_count**）。

## 4. 状态边界

台账是"处置登记"，不等于执行完成；合并/退出在执行时仍需逐项清单 + 回滚 + `gate(rule=redline)` 复核 + 回执。
