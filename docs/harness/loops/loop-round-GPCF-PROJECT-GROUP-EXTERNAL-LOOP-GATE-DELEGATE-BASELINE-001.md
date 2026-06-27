---
doc_id: GPCF-DOC-LOOP-ROUND-PROJECT-GROUP-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-001
title: loop-round-GPCF-PROJECT-GROUP-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# loop-round-GPCF-PROJECT-GROUP-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-001

## run

- 输入：`globalcloud-project-group-live-status-snapshot-20260626.md`、`globalcloud-project-group-current-state-baseline-refresh-20260626.md`、三仓 delegated `tools/kds-sync/loop_document_gate.py`。
- 动作：建立三仓 delegated loop gate wrapper 的统一基线证据，并绑定 review replay 的命令、门禁、证据和回滚边界。
- 输出：`docs/harness/evidence/globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md` 和 `tools/kds-sync/validate_project_group_external_loop_gate_delegate_baseline_20260627.py`。

## stop

- 不执行 AAAS/XWAIL/SOP 仓内 stage、commit、push、delete、deploy、真实 KDS API 同步或真实业务写入。
- 未得到人工确认前，不生成任何 delegated wrapper review receipt。

## verify

- `python3 tools/kds-sync/validate_project_group_external_loop_gate_delegates.py`
- `python3 tools/kds-sync/validate_project_group_external_loop_gate_delegate_baseline_20260627.py`
- `python3 tools/kds-sync/validate_project_group_live_status_snapshot_20260626.py`
- `python3 tools/kds-sync/loop_document_gate.py`

## recover

- 若三仓 wrapper 不再只委托到 GPCF canonical gate，或 dirty 基线不再为 `1/1/1`，则回滚本文结论并重新采集 live 状态。

## debug

- 当前 delegated wrapper 本身不是业务完成证据；它只证明项目群 loop gate 纳入边界已落到外部仓。
- 当前 REVIEW-AUTH 仍受 `GlobalCloud KDS/.env.production.example` sensitive_path、GFIS `repair_required` 和人工确认边界阻塞。
