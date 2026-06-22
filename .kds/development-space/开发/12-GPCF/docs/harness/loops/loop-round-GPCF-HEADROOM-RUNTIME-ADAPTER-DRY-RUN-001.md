---
doc_id: GPCF-DOC-AAD319F327
title: LOOP Round GPCF Headroom Runtime Adapter Dry-run 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-ADAPTER-DRY-RUN-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-ADAPTER-DRY-RUN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Headroom Runtime Adapter Dry-run 001

## 输入

- `fixtures/headroom/headroom-l2-project-group-sources.json`
- `headroom-ai==0.26.0`
- `HEADROOM_TELEMETRY=off`
- 前序 runtime probe 结论：直接压缩项目群 Markdown 样本为 `router:noop`。

## 动作

1. 执行 `HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_runtime_adapter_dry_run.py`。
2. 将项目群 evidence 摘要转为 `project_group_evidence_json` tool payload。
3. 调用 Headroom `CompressionUnit` + `ContentRouter` runtime 路径。
4. 执行 `python3 tools/kds-sync/validate_headroom_runtime_adapter_dry_run.py`。

## 输出

- `docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.json`
- `docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.md`
- `tools/kds-sync/run_headroom_runtime_adapter_dry_run.py`
- `tools/kds-sync/validate_headroom_runtime_adapter_dry_run.py`

## 检查

| 检查项 | 结果 |
|---|---|
| 真实 Headroom runtime import | pass |
| 真实 Headroom runtime used | pass |
| adapter payload compression | pass |
| required marker gate | pass |
| telemetry off | pass |
| raw sensitive text not stored | pass |
| runtime adapter saving rate >= 0.2 | fail |
| runtime_adapter_admission_gate | false |

## 反馈

adapter dry-run 证明了真实 Headroom runtime 对结构化 tool 输出存在可执行压缩路径，但当前节省率不足以进入 L2/L3.5/L4。下一轮必须扩大 tool-output 样本并复核成本模型，不得据此升级 accepted、integrated 或 production_ready。
