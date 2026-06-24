---
doc_id: GPCF-DOC-DEE39184F1
title: GC-Knowledge Fabric P0 正式证据执行修复请求受理完整性预检查预览 dry-run v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-execution-repair-request-intake-completeness-precheck-preview-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-execution-repair-request-intake-completeness-precheck-preview-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 正式证据执行修复请求受理完整性预检查预览 dry-run v0.1

## 1. 定位

本文档定义 P0-D75 的 repair request intake completeness precheck 预览 dry-run。

D75 承接 D74 aggregation precheck repair request intake preview，只预览补正请求接收候选的完整性预检，包括所需材料清单、缺失材料矩阵、提交方身份边界、ACL 边界、保持条件、阻断码、WAES 负向门禁和 Harness no-write 边界。

## 2. 输入

| 输入 | 路径 |
|---|---|
| D75 fixture | `fixtures/api/gckf-p0-formal-evidence-execution-repair-request-intake-completeness-precheck-preview-dry-run-v0.1.json` |
| D75 validator | `scripts/api/validate_gckf_p0_formal_evidence_execution_repair_request_intake_completeness_precheck_preview_dry_run.py` |
| D74 repair request intake preview | `fixtures/api/gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-dry-run-v0.1.json` |
| D74 Loop evidence | `docs/harness/loops/loop-round-GPCF-GCKF-P0-D74-001.md` |

## 3. 禁止动作

- 不执行 completeness precheck preview。
- 不执行正式完整性预检。
- 不创建补正请求。
- 不执行正式补正接收。
- 不执行 aggregation completeness precheck。
- 不开启委员会事项。
- 不执行委员会裁决或人工确认。
- 不写 KDS、GFIS、GPC 或业务系统。
- 不写 Harness evidence 或 formal evidence。
- 不写收益分配或贡献积分。
- 不覆盖 WAES 门禁。
- 不提升 lifecycle。
- 不标记 accepted / integrated / production_ready。

## 4. 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_execution_repair_request_intake_completeness_precheck_preview_dry_run.py
```

## 5. 结论

D75 仍是 candidate_preview，不是正式完整性预检、正式补正请求、委员会立案、委员会裁决、人工确认、收益/贡献确认或正式 evidence 写入。
