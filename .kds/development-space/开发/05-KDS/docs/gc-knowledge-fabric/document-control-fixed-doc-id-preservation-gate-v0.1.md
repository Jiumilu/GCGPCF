---
doc_id: GPCF-DOC-GCKFDOCUMENTCONTROLFIXEDDOCIDPRESERVATIONGATEV01
title: GC-Knowledge Fabric P0 文档控制固定 doc_id 保留门禁 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/document-control-fixed-doc-id-preservation-gate-v0.1.md
source_path: docs/gc-knowledge-fabric/document-control-fixed-doc-id-preservation-gate-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 文档控制固定 doc_id 保留门禁 v0.1

## 定位

本文件记录 D83 对文档控制脚本的机制修复：`document_control.py` 必须优先保留 Markdown frontmatter 中已有的 `doc_id`，不得在重建台账、README 或 KDS 本地镜像时把固定受控 ID 回写为路径哈希短 ID。

## 修复内容

- 新增 `controlled_doc_id(source_path, existing_frontmatter)`。
- `build_records` 读取已有 frontmatter。
- 当已有 `doc_id` 非空时直接沿用。
- 只有缺失 `doc_id` 的文档才回退到原路径哈希策略。

## 受控边界

- 本修复只影响文档控制 ID 生成逻辑。
- 不写入真实 KDS API。
- 不生成正式业务事实。
- 不确认 GFIS/GPC 写回。
- 不形成正式收益、积分或委员会裁决。

## 验证命令

```bash
DOCUMENT_CONTROL_SCOPE='docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-completeness-precheck-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-intake-acknowledgement-preview-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-preview-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-preview-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-preview-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-dry-run-v0.1.md,docs/gc-knowledge-fabric/formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-completeness-precheck-dry-run-v0.1.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D75-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D76-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D77-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D78-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D79-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D80-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D81-001.md,docs/harness/loops/loop-round-GPCF-GCKF-P0-D82-001.md' python3 tools/kds-sync/document_control.py
python3 scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py
```

## 验证结果

```text
gckf_p0_document_control_preserves_fixed_doc_id=pass
frontmatter_doc_id_preservation=covered
old_short_doc_ids_present=0
fixed_doc_ids_present=16
execution_mode=read_only_validation
```

## 下一步

D84 可以继续补齐文档控制脚本的单元级 fixture，覆盖“已有固定 ID”“缺失 ID”“外部 frontmatter”三类路径，降低后续治理脚本再次引入 ID 漂移的风险。
