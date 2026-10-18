---
doc_id: GPCF-DOC-F009-OPEN-SPEC-COVERAGE-SUMMARY-20260712
title: 证据摘要
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-009-project-group-openspec-coverage/evidence/summary.md
source_path: features/done/F-009-project-group-openspec-coverage/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# 证据摘要

## 2026-10-18 追溯复核

原 `tests.txt` 只有 18 项目 Feature 工作区校验，没有运行 `validate_project_group_openspec_coverage.py`；原 `build.txt` 只编译 GPCF 脚本。当前事实源为 24 项目，原 18 项目输出不能证明现行覆盖。现行 `gpcf_check_evidence.py F-009 --check-only` 返回 `close_candidate=false`，Feature 专属测试和构建命令未声明，故当前 `tests/build=fail`。截图与真实 API 不属本地治理矩阵范围，逐项豁免原因见 `feature.yaml`。

保留原始 18 项目关闭记录；当前 24 项目覆盖由独立项目群校验判定，不用历史记录替代。

## 原始关闭记录（未经现行门禁回放）

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: waived
- api: waived
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升。
