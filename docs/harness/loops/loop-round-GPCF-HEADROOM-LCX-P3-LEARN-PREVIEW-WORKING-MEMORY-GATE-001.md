---
doc_id: GPCF-DOC-8161B0C039
title: Loop Round GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001

## 输入

- 上轮输出：P2 MCP/SDK dry-run smoke 通过。
- 本轮目标：建立 `headroom learn` preview 与工作记忆治理门禁。
- 本轮边界：不扫描真实会话、不执行 LLM failure analysis、不执行 `headroom learn --apply`、不自动写入 memory、不把 Headroom memory 作为 KDS 正式事实源。

## 动作

1. 修正 `loop/context/headroom/scripts/learn-preview.sh`，移除当前 Headroom CLI 不支持的 `--preview` 参数，保持默认 dry-run。
2. 使用空白临时项目执行 `headroom learn` dry-run smoke。
3. 验证 `apply-approved-memory.sh` 缺审批文件拒绝，合成审批包仅输出 `apply_manually=true`。
4. 检查 policy、WAES policy 与 KDS component 中的工作记忆边界。

## 输出

- `loop/context/headroom/scripts/learn-preview.sh`
- `tools/kds-sync/run_headroom_lcx_p3_learn_preview_working_memory_gate.py`
- `tools/kds-sync/validate_headroom_lcx_p3_learn_preview_working_memory_gate.py`
- `docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.json`
- `docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md`

## 检查

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_lcx_p3_learn_preview_working_memory_gate.py
python3 tools/kds-sync/validate_headroom_lcx_p3_learn_preview_working_memory_gate.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

本轮只建立 learn preview 和工作记忆治理门禁。未扫描真实会话、未调用真实业务材料、未执行 LLM failure analysis、未执行 `--apply`、未写 KDS、未外部 API 写入、未升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001`：验证 LCX-Output-Shaper profile，并确保验收、合规、合同、财务场景关闭。
