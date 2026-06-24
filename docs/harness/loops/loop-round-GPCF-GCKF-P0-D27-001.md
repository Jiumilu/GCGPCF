---
doc_id: GPCF-DOC-4F5857B240
title: GC-Knowledge Fabric P0-D27 正式 evidence 批准预检 dry-run LOOP 证据
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D27-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D27-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0-D27 正式 evidence 批准预检 dry-run LOOP 证据

## 本轮目标

基于 D24 Harness decision template 建立 approval-to-formal-evidence preflight dry-run，将 `approved_for_formal_harness_evidence` 结论转为正式 Harness evidence 写入前的预检清单。

## 本轮输入

- `fixtures/api/gckf-p0-harness-decision-template-dry-run-v0.1.json`
- `docs/gc-knowledge-fabric/harness-decision-template-dry-run-v0.1.md`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D24-001.md`

## 本轮输出

- `fixtures/api/gckf-p0-approval-formal-evidence-preflight-dry-run-v0.1.json`
- `scripts/api/validate_gckf_p0_approval_formal_evidence_preflight_dry_run.py`
- `docs/gc-knowledge-fabric/approval-formal-evidence-preflight-dry-run-v0.1.md`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D27-001.md`

## 门禁命令

```bash
python3 scripts/api/validate_gckf_p0_approval_formal_evidence_preflight_dry_run.py
python3 scripts/api/validate_gckf_p0_harness_decision_template_dry_run.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 受控边界

- 不写正式 Harness evidence。
- 不写 KDS。
- 不连接数据库。
- 不启动 HTTP server。
- 不调用外部 API。
- 不写 GFIS、GPC 或其他业务系统。
- 不提升 lifecycle。
- 不把 P0 标记为 accepted 或 production ready。

## 下一轮建议

D28 建立 formal evidence write action guard dry-run，定义正式 evidence 写入动作本身的权限、输入、幂等、防重复和回滚前置条件，但仍不执行真实写入。
