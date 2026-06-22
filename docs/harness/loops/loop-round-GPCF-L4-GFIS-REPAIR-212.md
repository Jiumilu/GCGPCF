---
doc_id: GPCF-DOC-B64CED7E7D
title: GPCF-L4-GFIS-REPAIR-212
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-212.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-212.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-212

## 轮次定位

本轮按用户指定推荐顺序执行第一项：先清理 Git 风险，但只做分类，不删除、不 reset、不 checkout、不提交、不推送。

本轮不修复 GFIS runtime SOP E2E，也不补真实业务凭证；目标是把 GPCF/GFIS 当前工作区的 dirty 状态转成可治理、可审计、可分批提交的分类清单。

## 输入

- GPCF 真实仓库：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF`
- GFIS 真实仓库：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS`
- 真实命令：`git -c core.quotePath=false status --porcelain=v1`
- 治理要求：只分类、不删除、不 reset、不 checkout；高风险项默认不得进入提交候选。

## 产出

| 类型 | 路径 | 说明 |
|---|---|---|
| classifier | `tools/kds-sync/classify_git_risk.py` | 读取 GPCF/GFIS 真实 Git 状态并输出分类报告 |
| JSON evidence | `docs/harness/evidence/git-risk-classification-20260617.json` | 机器可读分类账 |
| Markdown evidence | `docs/harness/evidence/git-risk-classification-20260617.md` | 人工审阅报告 |
| evidence index | `docs/harness/evidence/evidence-index.md` | 登记本轮证据 |
| loop state | `docs/harness/loop-state.md` | 回写当前轮次与下一步 |
| control board | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 回写 Git 门禁状态 |
| status matrix | `09-status/gpcf-project-status-matrix.md` | 回写项目群总控状态 v3.81 |

## 分类结果

| 仓库 | total | modified | untracked | deleted_or_missing | high_risk |
|---|---:|---:|---:|---:|---:|
| GPCF | 476 | 41 | 435 | 0 | 2 |
| GFIS | 486 | 21 | 465 | 0 | 3 |

## GPCF 分类

| 分类 | 数量 | 处置 |
|---|---:|---|
| `gpcf_governance_and_control_sync` | 28 | 可作为总控同步提交候选复核 |
| `kds_local_mirror_and_ledger` | 234 | 需确认属于 KDS 开发空间镜像与审计流水 |
| `legacy_or_prior_loop_round_artifacts` | 211 | 只能作为历史轮次证据，不能计为新实质轮次 |
| `project_documentation` | 1 | 复核是否为主体定位或治理文档更新 |
| `sensitive_config_review` | 1 | 必须人工复核，默认不得提交 |
| `unclassified_requires_manual_review` | 1 | 必须人工判定归属 |

GPCF 高风险项：

- `.codex/config.toml`
- `scripts/`

## GFIS 分类

| 分类 | 数量 | 处置 |
|---|---:|---|
| `gfis_runtime_repair` | 265 | 可作为 runtime repair 提交候选复核 |
| `legacy_or_prior_loop_round_artifacts` | 203 | 只能作为历史轮次证据，不能计为新实质轮次 |
| `project_documentation` | 12 | 复核是否为 GFIS 主体定位或治理文档更新 |
| `gfis_demo_regression` | 3 | 只作为 `pass_demo_only` 展示层回归候选 |
| `unclassified_requires_manual_review` | 3 | 必须人工判定归属 |

GFIS 高风险项：

- `gcfis_custom/gcfis_custom/install/doctypes.py`
- `scripts/harvest_gfis_kds_gehu_inputs.py`
- `scripts/run_gfis_runtime_sop_e2e_dry_run.py`

## 真实性计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 边界

本轮没有执行：

- 删除文件
- `git reset`
- `git checkout`
- Git commit
- Git push
- 生产写入
- 真实外部 API 写入
- 数据库迁移
- 权限变更
- accepted/integrated 状态升级

## 下一步

从 KDS 候选中提取 5 类真实凭证的责任方回执任务，优先补 `CustomerRequirementOrPlatformOrder` 的真实 source-of-record 与 dispatch confirmation，再推进 WAES confirmation、KDS write receipt、runtime primary key。
