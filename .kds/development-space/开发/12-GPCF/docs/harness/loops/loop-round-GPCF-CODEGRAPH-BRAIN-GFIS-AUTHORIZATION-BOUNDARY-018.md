---
doc_id: GPCF-DOC-D1B5B8B030
title: Loop Round - CodeGraph Brain/GFIS 授权边界复核
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph Brain/GFIS 授权边界复核

## run

- 输入：`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017` 后的 watchlist。
- 范围：Brain、GFIS、KDS、Studio live CodeGraph/Git 状态。
- 动作：只读复核四仓，生成 GFIS 单独授权边界包。
- 输出：
  - `docs/harness/evidence/codegraph-brain-gfis-authorization-boundary-20260623.json`
  - `docs/harness/evidence/codegraph-brain-gfis-authorization-boundary-20260623.md`
  - `tools/kds-sync/validate_codegraph_brain_gfis_authorization_boundary.py`

## stop

- stop_type：`authorization_boundary`
- 停止证据：Brain 已 clean；KDS CodeGraph clean 但 Git mirror 有 4 项漂移；Studio 出现 post-clean drift；GFIS 仍有 pending 与 dirty，且 clean reindex 未授权。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_brain_gfis_authorization_boundary.py
```

同时保留：

```bash
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017`
- 可重试动作：重新只读采集四仓 status。
- 不可重试动作：未授权 GFIS scope review、sync、clean reindex、业务开发、commit、push、deploy。
- 恢复轮次：`GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018`

## debug

- 当前阻塞：GFIS 仍需只读 scope review 授权；KDS mirror drift 仅 watch，不执行 KDS 写入或覆盖。
- 下一轮：`GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019`
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，commit 0，push 0，deploy 0。
