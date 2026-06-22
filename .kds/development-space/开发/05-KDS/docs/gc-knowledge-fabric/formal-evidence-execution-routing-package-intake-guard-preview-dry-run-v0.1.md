---
doc_id: GPCF-DOC-4BA0188069
title: GC-Knowledge Fabric P0 正式证据执行路由包受理门禁预览 dry-run v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-execution-routing-package-intake-guard-preview-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-execution-routing-package-intake-guard-preview-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 正式证据执行路由包受理门禁预览 dry-run v0.1

## 1. 定位

本文档定义 P0-D66 的 routing package intake guard 预览 dry-run。

D66 承接 D65 reviewer acceptance acknowledgement routing package preview，只预览候选路由包进入 intake guard 前需要具备的包完整性、ACL 边界、委员会可见性、阻断码、保持条件、冻结保持、WAES 负向门禁和 Harness no-write 边界。

## 2. 输入

| 输入 | 路径 |
|---|---|
| D66 fixture | `fixtures/api/gckf-p0-formal-evidence-execution-routing-package-intake-guard-preview-dry-run-v0.1.json` |
| D66 validator | `scripts/api/validate_gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_dry_run.py` |
| D65 reviewer acceptance acknowledgement routing package preview | `fixtures/api/gckf-p0-formal-evidence-execution-reviewer-acceptance-acknowledgement-routing-package-preview-dry-run-v0.1.json` |
| D65 Loop evidence | `docs/harness/loops/loop-round-GPCF-GCKF-P0-D65-001.md` |

## 3. 禁止动作

- 不执行 intake guard。
- 不执行 routing package。
- 不执行正式 routing。
- 不执行 committee reentry。
- 不开启委员会事项。
- 不执行委员会裁决。
- 不执行人工确认。
- 不释放冻结或执行 unfreeze。
- 不写 KDS、GFIS、GPC 或业务系统。
- 不写 Harness evidence 或 formal evidence。
- 不写收益分配或贡献积分。
- 不覆盖 WAES 门禁。
- 不提升 lifecycle。
- 不标记 accepted / integrated / production_ready。

## 4. 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_dry_run.py
```

预期输出必须包含：

```text
gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_dry_run=pass
status=candidate_preview
execution_mode=dry_run_no_write
executes_intake_guard=0
executes_routing_package=0
executes_routing=0
executes_committee_reentry=0
writes_harness_evidence=0
no_write=covered
```

## 5. 结论

D66 仍是 candidate_preview，不是正式 intake、正式路由包执行、正式路由、委员会再进入、委员会立案、委员会裁决、人工确认、冻结释放、收益/贡献确认或正式 evidence 写入。后续若进入 D67，应继续只做 committee acceptance acknowledgement precheck 或 intake guard return path 的 no-write 预演。
