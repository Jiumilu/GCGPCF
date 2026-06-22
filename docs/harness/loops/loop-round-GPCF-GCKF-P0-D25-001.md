---
doc_id: GPCF-DOC-B4378BB296
title: GC-Knowledge Fabric P0-D25 Repair Path Workpack Dry-run LOOP evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D25-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D25-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0-D25 Repair Path Workpack Dry-run LOOP evidence

## 本轮目标

基于 D24 Harness decision template 建立 repair path workpack dry-run，将 `repair_required` 和 `scope_violation_found` 转为 KWE/LOOP 可追踪的候选补证或治理跟进工单。

## 本轮输入

- `fixtures/api/gckf-p0-harness-decision-template-dry-run-v0.1.json`
- `docs/gc-knowledge-fabric/harness-decision-template-dry-run-v0.1.md`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D24-001.md`

## 本轮输出

- `fixtures/api/gckf-p0-repair-path-workpack-dry-run-v0.1.json`
- `scripts/api/validate_gckf_p0_repair_path_workpack_dry_run.py`
- `docs/gc-knowledge-fabric/repair-path-workpack-dry-run-v0.1.md`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D25-001.md`

## 门禁命令

```bash
python3 scripts/api/validate_gckf_p0_repair_path_workpack_dry_run.py
python3 scripts/api/validate_gckf_p0_harness_decision_template_dry_run.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

## 受控边界

- 不创建真实 KWE work item。
- 不创建真实 LOOP follow-up。
- 不写正式 Harness evidence。
- 不写 KDS。
- 不连接数据库。
- 不启动 HTTP server。
- 不调用外部 API。
- 不写 GFIS、GPC 或其他业务系统。
- 不把状态升级为 `accepted`、`integrated` 或 `production_ready`。

## 下一轮建议

D26 建立 rejection archive path dry-run，把 `rejected` 结论转为拒绝归档、复审前置条件和新候选包重建规则。
