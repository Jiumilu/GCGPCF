---
doc_id: GPCF-DOC-429E306B5F
title: ODF Phase 4 小批量准入试运行方案
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase4-small-batch-admission-plan.md
source_path: 09-status/odf-phase4-small-batch-admission-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# ODF Phase 4 小批量准入试运行方案

日期：2026-06-17

## 目标

在 Phase 3 schema gate 已通过的基础上，对 3 个新增受控文档执行 ODF 小批量准入试运行，验证 ODF metadata envelope 从模板化检查走向受控小批量准入的可行性。

当前阶段目标：`phase4_small_batch_closed`。

## 样本范围

| category | source_path |
| --- | --- |
| status-governance | `09-status/gpcf-project-status-matrix.md` |
| loop-harness-evidence | `docs/harness/evidence/loop-governance-dashboard-20260617.md` |
| kds-knowledge | `03-data-ai-knowledge/GlobalCloud项目群与分布式KDS关系总图.md` |

## 证据

| artifact | path |
| --- | --- |
| Phase 4 ledger Markdown | `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.md` |
| Phase 4 ledger JSON | `docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.json` |
| Phase 4 envelopes | `docs/harness/evidence/odf-samples/phase4/*.json` |
| Phase 4 closure evidence | `docs/harness/evidence/odf-phase4-small-batch-closure-20260617.md` |

## 门禁

1. Phase 3 schema gate 仍通过。
2. Phase 4 ledger 纳入 `validate_odf_schema_gate.py`。
3. 3 个新增样本哈希均可复算。
4. 文档污染检查通过。
5. KDS TOKEN 检查通过。
6. Loop 文档门禁通过。
7. KDS 冲突检查通过。
8. Phase 4 相关 KDS 待同步项为 0。

## 非范围

- 不全量导入 ODF。
- 不批量改写 Markdown 正文。
- 不写生产系统或真实外部 API。
- 不替代 Git、KDS、OKF 或 Loop evidence。
- 不自动升级 `accepted` 或 `integrated`。
- 不将其它并行工作线的 KDS create/update 混入本批次。
