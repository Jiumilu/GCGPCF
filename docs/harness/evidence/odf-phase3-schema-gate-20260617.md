---
doc_id: GPCF-DOC-146EB71EF5
title: ODF Phase 3 Schema Gate Evidence
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/odf-phase3-schema-gate-20260617.md
source_path: docs/harness/evidence/odf-phase3-schema-gate-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ODF Phase 3 Schema Gate Evidence

日期：2026-06-17

## 结论

ODF Phase 3 已建立可执行 schema gate，用于在小批量准入前检查 Phase 1 与 Phase 2 ODF metadata envelope。

当前结论：`phase3_schema_gate_ready`。

下一阶段允许：`yes_with_gate`。

## 输入

| input | path |
| --- | --- |
| Phase 1 sample ledger | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.json` |
| Phase 2 sample ledger | `docs/harness/evidence/odf-phase2-sample-ledger-20260617.json` |
| Phase 3 evidence JSON | `docs/harness/evidence/odf-phase3-schema-gate-20260617.json` |

## Validator

```bash
python3 tools/kds-sync/validate_odf_schema_gate.py
```

## 准入规则

| gate | required |
| --- | --- |
| ledger JSON parseable | yes |
| ledger status controlled | `pilot_closed` or `phase2_closed` |
| required sample fields | 12 |
| source hash reproducible | yes |
| markdown hash reproducible | yes |
| ODF hash reproducible | yes |
| envelope matches ledger | yes |
| duplicate sample id / ODF path | forbidden |
| cross-phase source overlap | counted and disclosed |
| boundary flags | required |
| rollout/accepted/integrated claims | forbidden |

## 预期输出

```text
odf_schema_gate=pass ledgers=2 samples=13 ledger_statuses=pilot_closed,phase2_closed categories=business-import,governance,kds-knowledge,loop-harness-evidence,okf-navigation,pilot source_hash=pass markdown_hash=pass odf_hash=pass source_overlaps=2 duplicate_sample_ids=0 duplicate_odf_paths=0 forbidden_rollout=0
```

## 最终审计结果

| check | result |
| --- | --- |
| ODF schema gate | pass |
| ledgers | 2 |
| samples | 13 |
| ledger statuses | `pilot_closed`、`phase2_closed` |
| source hash | pass |
| markdown hash | pass |
| ODF hash | pass |
| source overlaps | 2 |
| duplicate sample ids | 0 |
| duplicate ODF paths | 0 |
| forbidden rollout claims | 0 |
| KDS sync plan | pass |
| remote documents | 723 |
| conflicts | 0 |
| missing local | 0 |
| Phase 3 related pending writes | 0 |

## 非范围

- 不全量导入 ODF。
- 不批量改写 Markdown 正文。
- 不写真实业务系统。
- 不替代 Git、KDS、OKF 或 Loop evidence。
- 不自动升级 `accepted` 或 `integrated`。
- 不将其它并行工作线混入本阶段 KDS 同步。
