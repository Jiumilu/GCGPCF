---
doc_id: GPCF-DOC-D86BB8E18F
title: Loop Round - CodeGraph Studio sync-only precheck
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph Studio sync-only precheck

## run

- 输入：用户对 `GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015` 的授权。
- 范围：仅 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio` 的 CodeGraph 索引。
- 动作：执行 `codegraph sync`，采集 sync 前后 status 和 `.codegraph/` Git 隔离。
- 输出：
  - `docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.json`
  - `docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.md`
  - `tools/kds-sync/validate_codegraph_studio_sync_only_precheck.py`

## stop

- stop_type：`sync_only_pass_with_residual_watch`
- 停止证据：Studio CodeGraph sync-only 已执行；最终仍观测到小幅 modified residual watch；Studio 工作树仍有 12 项既有 dirty，且本轮没有业务开发授权。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_studio_sync_only_precheck.py
```

同时保留：

```bash
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014`
- 可重试动作：重新采集 Studio CodeGraph status；如出现新 pending，重新请求授权。
- 不可重试动作：业务开发、release、deployment、workflow release write、commit、push、生产写入、外部 API 写入。
- 恢复轮次：`GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015`

## debug

- 当前阻塞：Brain、GFIS、KDS 仍未授权；Studio 仅完成 CodeGraph 索引闭合。
- 下一轮：`GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016`
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。
