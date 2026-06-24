---
doc_id: GPCF-DOC-CGNC001
title: Loop Round - CodeGraph 常态化归一清单
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-NORMALIZATION-CHECKLIST-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-NORMALIZATION-CHECKLIST-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph 常态化归一清单

## 输入

当前目标是把 CodeGraph 的常态化要求固定成长期受控清单，并用现有门禁证明它可重放。

## 动作

- 建立 `02-governance/loop/LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST.md`
- 建立 `docs/harness/evidence/codegraph-normalization-checklist-20260623.json`
- 建立 `docs/harness/evidence/codegraph-normalization-checklist-20260623.md`
- 建立 `tools/kds-sync/validate_codegraph_normalization_checklist.py`

## 输出

- CodeGraph 常态化清单有固定位置
- 准入字段、验收字段、量化字段和稳态字段被一次性列出
- 现有门禁被串到清单验证里

## 检查

- `python3 tools/kds-sync/validate_codegraph_normalization_checklist.py`
- `python3 tools/kds-sync/document_control.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

下一轮输入：`GPCF-CODEGRAPH-NORMALIZATION-WATCH-002`

清单只定义和验证常态化要求，不声明业务完成、不声明 accepted/integrated/production_ready。
