---
doc_id: GPCF-DOC-EB9209D502
title: Headroom Runtime Adapter Dry-run Evidence
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.md
source_path: docs/harness/evidence/headroom-runtime-adapter-dry-run-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom Runtime Adapter Dry-run Evidence

## Evidence ID

`HEADROOM-RUNTIME-ADAPTER-DRY-RUN-20260621`

## 结论

本轮新增一个受控 adapter dry-run：先把 15 个项目/域的 Loop evidence 摘成结构化 tool payload，再调用 `headroom-ai==0.26.0` 的 `CompressionUnit` + `ContentRouter` runtime 路径压缩。

结果显示真实 Headroom runtime 可以压缩该结构化 tool payload，且项目名与 required marker gate 全部保留；但节省率只有 `0.022083`，低于 L2 阈值 `0.2`（below L2 threshold）。因此 `runtime_adapter_admission_gate | false`，不得升级 accepted、integrated 或 production_ready。

## 测量摘要

| 字段 | 当前值 |
|---|---|
| headroom_runtime_imported | true |
| headroom_runtime_used | true |
| headroom_version | 0.26.0 |
| python_version | 3.12.13 |
| adapter | project_group_evidence_json |
| project_count | 15 |
| tokens_before | 11049 |
| tokens_after | 10805 |
| tokens_saved | 244 |
| runtime_adapter_saving_rate | 0.022083 |
| minimum_saving_rate | 0.2 |
| strategy | mixed |
| transforms_applied | router:gpcf:headroom_runtime_adapter:project_group_evidence_json:mixed, mixed |
| all_marker_gates_pass | true |
| runtime_adapter_admission_gate | false |

## 安全边界

- `HEADROOM_TELEMETRY=off`。
- adapter 输入以 `input_sha256` 留痕，不保存原始敏感文本。
- source_path 保留在受控 metadata records 中，不要求 runtime 压缩结果逐字保留。
- 不启用跨项目 memory。
- 不写真实 KDS。
- 不执行真实外部 API 写入。
- 不生产代理、不部署、不提交、不推送。
- 不升级 accepted、integrated 或 production_ready。

## 与前序证据的关系

- `headroom-runtime-probe-20260621` 证明直接压缩项目 Markdown/Loop state 仍为 `router:noop`，saving rate 为 0。
- 本 adapter dry-run 证明结构化 tool 输出路径存在真实 runtime 压缩能力，但节省率低于 L2 阈值。
- `headroom-l2-project-group-dry-run-20260621` 的高节省率仍只代表 structured surrogate，不代表真实 runtime。

## 下一步

下一轮应扩大真实 tool-output payload 样本，按相同 marker gate 和 sensitive raw text gate 复放，并与 structured surrogate 逐项对比。真实 runtime saving_rate、marker gate 和安全门禁同时达标前，不得进入 L3.5/L4 runtime 使用。
