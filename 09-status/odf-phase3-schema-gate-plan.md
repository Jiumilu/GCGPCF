---
doc_id: GPCF-DOC-E360D5C8BC
title: ODF Phase 3 受控模板化与准入门禁计划
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-phase3-schema-gate-plan.md
source_path: 09-status/odf-phase3-schema-gate-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ODF Phase 3 受控模板化与准入门禁计划

日期：2026-06-17

## 目标

在 Phase 1 `pilot_closed` 和 Phase 2 `phase2_closed` 的基础上，将 ODF metadata envelope 的人工准入规则固化为可执行门禁，形成小批量准入前的自动检查能力。

当前阶段目标：`phase3_schema_gate_ready`。

## 范围

| item | scope |
| --- | --- |
| validator | `tools/kds-sync/validate_odf_schema_gate.py` |
| input ledgers | Phase 1 与 Phase 2 ODF sample ledgers |
| evidence | `docs/harness/evidence/odf-phase3-schema-gate-20260617.md` |
| evidence JSON | `docs/harness/evidence/odf-phase3-schema-gate-20260617.json` |
| OKF navigation | `.okf/governance/index.md`、`.okf/kds/index.md` |

## 准入门禁

1. ODF ledger JSON 必须可解析。
2. ledger status 只能为 `pilot_closed` 或 `phase2_closed`。
3. 每个 sample 必须具备 12 个准入字段。
4. `source_hash` 必须匹配源 Markdown。
5. `markdown_hash` 必须匹配源 Markdown。
6. `odf_hash` 必须匹配 ODF envelope JSON。
7. ODF envelope 与 ledger 字段必须一致。
8. ODF envelope 必须声明不替代 Git、KDS、OKF、Loop evidence。
9. 不允许重复 sample id 或 ODF path；跨阶段重复 source path 必须计数披露。
10. 不允许出现 `full_rollout`、`accepted`、`integrated` 状态声明。

## 非范围

- 不全量导入 ODF。
- 不批量改写现有 Markdown 正文。
- 不新增真实业务完成声明。
- 不替代 Git、KDS、OKF 或 Loop evidence。
- 不自动升级 `accepted` 或 `integrated`。
- 不混入其它并行 KDS 同步项。

## 下一阶段出口

Phase 3 仅在以下条件同时满足后，才允许进入 Phase 4 小批量准入：

1. `validate_odf_schema_gate.py` 通过。
2. 文档污染检查通过。
3. KDS TOKEN 检查通过。
4. Loop 文档门禁通过。
5. KDS 冲突检查通过。
6. Phase 3 相关 KDS 待同步项为 0。
7. 人工确认小批量样本范围。
