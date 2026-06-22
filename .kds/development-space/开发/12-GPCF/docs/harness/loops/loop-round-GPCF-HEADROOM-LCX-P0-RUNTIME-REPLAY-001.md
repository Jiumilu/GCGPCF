---
doc_id: GPCF-DOC-AD82144FCE
title: Loop Round GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001

## 输入

- 上一轮输出：`loop/context/headroom/` LCX 受控能力包。
- 用户要求：进入下一轮，继续执行 Headroom LCX 全量实施。
- 本轮边界：只做隔离 runtime replay 和脚本 smoke，不启动生产 proxy，不写真实 TOKEN，不处理未脱敏材料。

## 动作

1. 使用隔离 Headroom runtime 执行 `headroom --help` smoke。
2. 对 `loop/context/headroom/scripts/*.sh` 执行 `bash -n` 语法检查。
3. 回放既有 Headroom 成本模型样例。
4. 对 LCX 受控 package payload 执行 Headroom runtime compression replay。
5. 记录 marker gate、生产非声明和下一轮 P1 proxy dry-run smoke。

## 输出

- `tools/kds-sync/run_headroom_lcx_p0_runtime_replay.py`
- `tools/kds-sync/validate_headroom_lcx_p0_runtime_replay.py`
- `docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.json`
- `docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md`

## 检查

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_lcx_p0_runtime_replay.py
python3 tools/kds-sync/validate_headroom_lcx_p0_runtime_replay.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

本轮只证明 P0 runtime replay 和脚本 smoke 可执行，不证明生产代理、生产 token 节省、真实外部 API、真实 KDS 写入、accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001`：在不启动生产服务的前提下，验证 proxy dry-run 配置、端口策略和禁止生产代理门禁。
