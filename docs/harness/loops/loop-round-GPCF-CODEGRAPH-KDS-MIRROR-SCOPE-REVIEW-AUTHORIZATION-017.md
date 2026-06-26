---
doc_id: GPCF-DOC-7272ECE5C1
title: Loop Round - CodeGraph KDS mirror scope review 授权复核
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph KDS mirror scope review 授权复核

## run

- 输入：`GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016` 中 KDS dirty 增长事实。
- 范围：KDS mirror / WorkWiki scope review 授权必要性。
- 动作：复核 KDS live CodeGraph 与 Git 状态，发现当前 pending 已清零但 Git dirty 仍非零。
- 输出：
  - `docs/harness/evidence/codegraph-kds-mirror-scope-review-authorization-20260622.json`
  - `docs/harness/evidence/codegraph-kds-mirror-scope-review-authorization-20260622.md`
  - `tools/kds-sync/validate_codegraph_kds_mirror_scope_review_authorization.py`

## stop

- stop_type：`authorization_boundary`
- 停止证据：KDS 当前 CodeGraph pending=0，但 Git dirty=1；需要保留 scope review 授权边界，不能执行 sync、真实 KDS API 写入、mirror overwrite 或 clean reindex。
- 状态上限：不得升级 accepted、integrated 或 production_ready。

## verify

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_kds_mirror_scope_review_authorization.py
```

同时保留：

```bash
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

## recover

- 最后安全状态：`GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016`
- 可重试动作：重新只读采集 KDS status；若 KDS 后续再次清零，可重新评估是否取消 scope review。
- 不可重试动作：未授权 sync、真实 KDS API 写入、mirror overwrite、clean reindex、业务开发、commit、push、deploy。
- 恢复轮次：`GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017`

## debug

- 当前阻塞：KDS mirror / WorkWiki 仍有 dirty，Brain、GFIS、Studio 继续保持 monitor_only。
- 下一轮：`GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018`
- 真实 lane：未进入业务开发，真实业务计数不变。
- 写入计数：生产写入 0，外部 API 写入 0，真实 KDS API 写入 0，commit 0，push 0，deploy 0。
