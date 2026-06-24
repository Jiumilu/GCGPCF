---
doc_id: GPCF-DOC-6AAF1F40B0
title: Loop Round GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001

## 输入

- 用户目标：全面在项目群实施 Headroom 接入与应用，纳入 Loop 工程体系，并建立成本评估模型。
- 上轮产物：Headroom admission evidence、成本公式、成本计算器和 measurement template。
- 当前边界：本机未安装 `headroom` Python runtime；本轮只能做结构化 surrogate dry-run，不声明真实 Headroom runtime 接入。

## 动作

1. 建立 `fixtures/headroom/headroom-l2-project-group-sources.json`，覆盖 15 个项目/域的受控样本来源。
2. 建立 `tools/kds-sync/generate_headroom_l2_project_group_dry_run.py`，生成项目群 L2 token/cost 测量 evidence。
3. 建立 `tools/kds-sync/validate_headroom_l2_project_group_dry_run.py`，检查 coverage、saving_rate、marker 保真、安全边界和非声明。
4. 更新 Headroom 接入治理文档与 admission evidence 索引。

## 输出

- `fixtures/headroom/headroom-l2-project-group-sources.json`
- `tools/kds-sync/generate_headroom_l2_project_group_dry_run.py`
- `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json`
- `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md`
- `docs/harness/loops/loop-round-GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001.md`
- `tools/kds-sync/validate_headroom_l2_project_group_dry_run.py`

## 检查

```bash
python3 tools/kds-sync/generate_headroom_l2_project_group_dry_run.py
python3 tools/kds-sync/validate_headroom_l2_project_group_dry_run.py
python3 tools/kds-sync/validate_headroom_project_group_admission.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

本轮将 Headroom 从 L1 准入和模板成本模型推进到 L2 项目群样本测量。当前仍为 `structured_surrogate_no_headroom_runtime`，不能替代真实 `headroom-ai` runtime 验证。

下一轮输入：在隔离环境安装或引入真实 `headroom-ai` runtime，保持 `HEADROOM_TELEMETRY=off`，使用同一 source fixture 复跑并比较真实压缩器结果。
