---
doc_id: GPCF-DOC-3FBC093145
title: ODF Phase 5 准入变更申请台账
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md
source_path: docs/harness/evidence/odf-phase5-change-request-ledger-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# ODF Phase 5 准入变更申请台账

日期：2026-06-17

## 机制结论

ODF Phase 5 建立准入变更申请机制。未来任何 ODF 样本扩展必须先登记申请，包含样本边界、人工确认、回滚提示和 KDS 定向同步清单。

当前状态：`phase5_change_request_closed`。

## 申请规则

| rule | value |
| --- | --- |
| request type | `odf_small_batch_admission` |
| max small batch samples | 5 |
| manual confirmation | required |
| rollback hints | required per sample |
| KDS sync paths | required |
| full rollout | forbidden |
| accepted / integrated | forbidden |

## 申请样例

| request_id | status | sample_count | result |
| --- | --- | ---: | --- |
| `ODF-CR-20260617-001` | `closed_after_audit` | 3 | Phase 4 小批量准入试运行已闭环 |

## Validator

```bash
python3 tools/kds-sync/validate_odf_change_request_gate.py
```

## 非范围

- 不新增 Phase 5 ODF 样本。
- 不全量导入 ODF。
- 不批量改写 Markdown 正文。
- 不写生产系统或真实外部 API。
- 不把文档验证写成业务完成。
- 不自动升级 `accepted` 或 `integrated`。
