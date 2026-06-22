---
doc_id: GPCF-DOC-A5BB39D841
title: Headroom Runtime Probe Evidence
project: KDS
related_projects: [KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-runtime-probe-20260621.md
source_path: docs/harness/evidence/headroom-runtime-probe-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom Runtime Probe Evidence

## Evidence ID

`HEADROOM-RUNTIME-PROBE-20260621`

## 结论

本轮已在隔离环境探测真实 `headroom-ai==0.26.0` runtime。runtime 可以安装、import 并执行 `headroom.compress()`，但对当前 15 个项目/域样本全部返回 `router:noop`，token saving 为 0。因此当前真实 runtime 准入门禁为 false。

该结果不推翻 L2 structured surrogate dry-run；它说明 surrogate 只能证明测量链路和成本模型可执行，不能替代真实 Headroom runtime 接入。

## 探测摘要

| 字段 | 当前值 |
|---|---|
| headroom_runtime_imported | true |
| headroom_runtime_used | true |
| headroom_version | 0.26.0 |
| python_version | 3.12.13 |
| project_count | 15 |
| tokens_before | 313533 |
| tokens_after | 313533 |
| tokens_saved | 0 |
| runtime_saving_rate | 0.0 |
| all_marker_gates_pass | true |
| all_runtime_compressions_positive | false |
| all_transforms_noop | true |
| runtime_admission_gate | false |

## 安全边界

- `HEADROOM_TELEMETRY=off`。
- 不保存原始敏感文本。
- 不启用跨项目 memory。
- 不写真实 KDS。
- 不执行真实外部 API 写入。
- 不生产代理、不部署、不提交、不推送。
- 不升级 accepted、integrated 或 production_ready。

## 下一步

下一轮应排查 Headroom 对项目群 Markdown/Loop state 样本返回 `router:noop` 的原因，确认是否需要 CLI/proxy/MCP 路径、SmartCrusher/ContentRouter 低层 API、或专门 adapter 配置。真实 runtime 形成正向 saving_rate 前，不得进入 L3.5/L4 runtime 使用。
