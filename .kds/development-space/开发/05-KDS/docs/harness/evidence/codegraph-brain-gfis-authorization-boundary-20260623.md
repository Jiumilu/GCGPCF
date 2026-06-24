---
doc_id: GPCF-DOC-4E29A86D95
title: CodeGraph Brain/GFIS 授权边界复核
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-brain-gfis-authorization-boundary-20260623.md
source_path: docs/harness/evidence/codegraph-brain-gfis-authorization-boundary-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph Brain/GFIS 授权边界复核

本证据对应 `GPCF-CODEGRAPH-BRAIN-GFIS-AUTHORIZATION-BOUNDARY-018`。

## 结论

live 状态显示 Brain 仍有 1 项 Git dirty；KDS CodeGraph pending 为 0，但 KDS Git mirror 仍有 59 项漂移，进入 mirror watch；Studio 出现 post-clean drift；当前主要授权边界 watchlist 是 GFIS。

本轮只生成 GFIS 授权边界包，不执行 GFIS `codegraph sync`，不执行 clean reindex，不进入 GFIS 业务开发，不提交、不推送、不部署。

状态为 `gfis_authorization_boundary_with_kds_studio_watch`。

## 当前 watchlist

| repo | CodeGraph pending | Git dirty | 决策 |
| --- | --- | ---: | --- |
| Brain | added=0, modified=0, removed=0 | 1 | current_state_dirty_monitor_only |
| GFIS | added=0, modified=0, removed=0 | 1 | authorization_required_without_clean_reindex |
| KDS | added=0, modified=0, removed=0 | 59 | codegraph_git_mirror_drift_watch_no_write |
| Studio | added=0, modified=18, removed=0 | 20 | post_clean_drift_watch_no_sync |

## GFIS 授权问答

| 问题 | 建议 | 默认无回答 |
| --- | --- | --- |
| 是否授权 GFIS 执行只读 CodeGraph/Git scope review？ | 建议授权；只读分类 1 项 dirty 与 0 项 CodeGraph pending。 | 不授权 |
| 是否授权 GFIS 在 scope review 通过后执行 CodeGraph sync-only？ | 暂不建议直接授权；先做只读边界复核。 | 不授权 |
| 是否授权 GFIS clean reindex？ | 不建议授权；GFIS reindexRecommended=false，且用户此前明确暂不授权 clean reindex。 | 不授权 |
| 是否授权进入 GFIS 业务开发？ | 不建议授权；当前会话主线是 CodeGraph 项目群集成。 | 不授权 |

## 允许与禁止

若用户授权，只允许：

- GFIS Git dirty 只读分类
- GFIS CodeGraph status refresh
- GFIS policy exception 边界摘要
- scope review 后评估 sync-only 候选

禁止：

- clean reindex
- 业务开发
- bench migrate、schema sync
- 生产写入、外部 API 写入、真实 KDS API 写入
- commit、push、deploy
- accepted、integrated、production_ready 声明

## 五方向

### run

复核 Brain/GFIS/KDS/Studio live 状态，确认 GFIS 需要授权边界，KDS 仅保留 Git mirror drift watch。

### stop

`stop_type=authorization_boundary`。未获授权前不执行 GFIS scope review、sync、clean reindex 或业务开发。

### verify

回放：

```bash
python3 tools/kds-sync/validate_codegraph_brain_gfis_authorization_boundary.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

### recover

若用户不授权，保持 GFIS monitor_only；若授权范围不清，只重新生成问答，不执行 GFIS 仓动作。

### debug

Brain 仍有 1 项 Git dirty；KDS CodeGraph clean 但 Git mirror 仍有 59 项漂移；Studio 出现 post-clean drift；GFIS 是主要授权边界风险，且 clean reindex 继续禁止。

## 非声明

- 不声明 GFIS sync-only closure 完成。
- 不声明 GFIS clean reindex 已授权或已执行。
- 不声明 GFIS 业务实现完成。
- 不声明 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019`
