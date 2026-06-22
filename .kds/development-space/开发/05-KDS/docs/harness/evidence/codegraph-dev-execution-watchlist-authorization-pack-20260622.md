---
doc_id: GPCF-DOC-2B8C8B68C2
title: CodeGraph watchlist 授权包
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph watchlist 授权包

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014`。

## 结论

本轮只生成问答式授权包，不执行 Brain、GFIS、KDS、Studio 任一 watchlist 仓的 `codegraph sync`，不执行 clean reindex，不进入业务开发，不提交、不推送、不部署。

状态为 `authorization_pack_ready`。下一步建议优先选择 Studio 作为低风险 `sync-only precheck` 候选；Brain、GFIS、KDS 继续保持授权边界。

## 授权问答

| 问题 | 建议 | 默认无回答 |
| --- | --- | --- |
| 是否授权 Studio 先进入低风险 CodeGraph sync-only precheck？ | 建议授权；范围最小，dirty 总量 12，适合作为 watchlist sync-only 试点。 | 不授权 |
| 是否授权 Brain 进入独立 sync-only precheck？ | 建议暂缓；Brain 有 203 项 dirty 且含 deleted openspec archive，需要 owner 先确认。 | 不授权 |
| 是否授权 GFIS 进入 sync-only precheck，并继续禁止 clean reindex？ | 建议只在 GFIS policy exception 复核后授权；clean reindex 仍不建议授权。 | 不授权 |
| 是否授权 KDS 先做 mirror / WorkWiki scope review？ | 建议先复核镜像与 WorkWiki 同步边界，再考虑 CodeGraph sync-only closure。 | 不授权 |
| 是否授权任一 watchlist 仓执行 clean reindex？ | 建议不授权；当前四仓 reindexRecommended=false，clean reindex 没有必要且风险更高。 | 不授权 |

## 生成时基线

| repo | CodeGraph pending | Git dirty | 分类 | 下一轮候选 |
| --- | --- | ---: | --- | --- |
| Brain | added=4, modified=54, removed=0 | 203 | broad_active_development_drift_with_deleted_openspec_archive | `GPCF-CODEGRAPH-BRAIN-SYNC-ONLY-PRECHECK-015` |
| GFIS | added=1, modified=2, removed=0 | 239 | broad_runtime_sop_e2e_governance_drift_with_policy_exception | `GPCF-CODEGRAPH-GFIS-SYNC-ONLY-PRECHECK-015` |
| KDS | added=0, modified=1, removed=0 | 1652 | broad_kds_mirror_workwiki_content_drift | `GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-015` |
| Studio | added=2, modified=9, removed=0 | 12 | bounded_studio_session_binding_and_kds_governance_drift | `GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015` |

以上 Git dirty 为授权包生成时基线。Brain、GFIS、KDS、Studio 属于活动 watchlist；后续验证只要求当前 dirty 不低于基线并保持 `.codegraph/` Git 隔离，不把持续漂移误判为本轮授权包失败。

## 允许与禁止

Studio 若被明确授权，只允许：

- read-only status refresh
- sync-only precheck
- 当 pending 范围仍匹配 session binding 与 KDS governance 时执行 CodeGraph sync

Studio 禁止：

- release、deployment、workflow release write
- 业务开发
- commit、push
- accepted、integrated、production_ready 声明

Brain、GFIS、KDS 在未取得独立授权前，只允许继续只读监控。GFIS clean reindex 继续不授权。

## 五方向

### run

把 Brain/GFIS/KDS/Studio 的活动漂移分诊转成问答式授权包，列出每仓允许动作、禁止动作和下一轮候选。

### stop

`stop_type=authorization_boundary`。本轮只生成授权包，不执行 watchlist sync、clean reindex、commit、push、deploy 或业务开发。

### verify

回放：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_watchlist_authorization_pack.py
python3 tools/kds-sync/validate_codegraph_dev_execution_watchlist_drift_triage.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

### recover

若用户不授权，恢复为 `watchlist monitor_only`；若授权范围不清，只允许重新生成授权问题，不执行仓内动作。

### debug

当前最小可执行授权建议是 Studio sync-only precheck；Brain/GFIS/KDS 仍需独立边界复核。

## 非声明

- 不声明业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 watchlist sync-only closure 完成。
- 不声明 GFIS clean reindex 已执行。
- 不声明生产写入、外部 API 写入、commit、push 或 deploy。

## 下一轮

`GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015`
