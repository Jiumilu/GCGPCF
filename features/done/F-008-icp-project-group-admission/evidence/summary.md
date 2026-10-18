---
doc_id: GPCF-DOC-C3B0435AFB
title: 证据摘要
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-008-icp-project-group-admission/evidence/summary.md
source_path: features/done/F-008-icp-project-group-admission/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# 证据摘要

## 2026-10-18 追溯复核

原 `tests.txt` 只有 18 项目 Feature 工作区校验，未记录验收要求中的 `validate_icp_project_registration.py`；原 `build.txt` 只编译 GPCF 脚本。现行 `gpcf_check_evidence.py F-008 --check-only` 返回 `close_candidate=false`，其中还指出验收要求保持 active candidate，与历史 `done` 状态冲突。Feature 专属测试和构建命令未声明，故当前 `tests/build=fail`。截图与真实 API 不属本地项目登记范围，逐项豁免原因见 `feature.yaml`。

当前 `projects/icp/STATUS.md` 仍声明 `candidate/partial/human_required`。保留原始关闭记录；它不证明当前项目群口径、业务集成或人工验收。

## 原始关闭记录（未经现行门禁回放）

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: waived
- api: waived
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升。
