---
doc_id: GPCF-DOC-D2DDB9FD6E
title: Loop Round GPCF-HEADROOM-RUNTIME-PROBE-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-PROBE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-PROBE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-RUNTIME-PROBE-001

## 输入

- 用户目标：全面在项目群实施 Headroom 接入与应用，纳入 Loop 工程体系，并建立成本评估模型。
- 上轮产物：structured surrogate L2 项目群 dry-run 已通过，saving_rate 为 0.989466。
- 当前缺口：本机系统 Python 3.9.6 不满足 `headroom-ai` 的 Python 版本要求；需用隔离 Python 3.12 环境探测真实 runtime。

## 动作

1. 使用 Codex bundled Python 3.12.13 在 `/tmp/gpcf-headroom-runtime-probe` 建立隔离 venv。
2. 安装 `headroom-ai==0.26.0`。
3. 以 `HEADROOM_TELEMETRY=off` 执行 `tools/kds-sync/probe_headroom_runtime.py`。
4. 使用同一 `fixtures/headroom/headroom-l2-project-group-sources.json` 覆盖 15 个项目/域样本。
5. 记录 runtime import、version、token before/after、transforms、marker gate 和 runtime admission gate。

## 输出

- `tools/kds-sync/probe_headroom_runtime.py`
- `docs/harness/evidence/headroom-runtime-probe-20260621.json`
- `docs/harness/evidence/headroom-runtime-probe-20260621.md`
- `docs/harness/loops/loop-round-GPCF-HEADROOM-RUNTIME-PROBE-001.md`
- `tools/kds-sync/validate_headroom_runtime_probe.py`

## 检查

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/probe_headroom_runtime.py
python3 tools/kds-sync/validate_headroom_runtime_probe.py
python3 tools/kds-sync/validate_headroom_l2_project_group_dry_run.py
python3 tools/kds-sync/validate_headroom_project_group_admission.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

真实 `headroom-ai==0.26.0` runtime 可安装、可 import、可执行，但当前项目群样本全部 `router:noop`，runtime_saving_rate=0.0，runtime_admission_gate=false。

下一轮应排查 Headroom 支持的 transform path、CLI/proxy/MCP 路径或低层 SmartCrusher/ContentRouter API。未形成真实 runtime 正向节省前，不进入 L3.5/L4 runtime 使用。
