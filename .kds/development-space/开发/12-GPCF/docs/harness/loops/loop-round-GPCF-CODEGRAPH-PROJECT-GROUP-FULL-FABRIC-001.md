---
doc_id: GPCF-DOC-55CEA573A4
title: GPCF CodeGraph Project Group Full Fabric 001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-FULL-FABRIC-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-FULL-FABRIC-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Project Group Full Fabric 001

## 输入

- 用户要求严格按 GlobalCloud 项目群 CodeGraph / Loop 集成方案执行。
- 范围为当前项目群全部 14 项目，不再采用 Brain/Harness 双仓试点口径。
- GlobalCloud Studio 与 WAS 必须纳入项目群、代码图谱与 LOOP 工程体系。

## 动作

- 建立 14 项目 CodeGraph registry。
- 建立 CodeGraph 六层授权模型。
- 建立 Loop CodeGraph schema。
- 建立 Harness impact report 与 evidence bundle 模板。
- 建立 WAES high-risk gate policy。
- 建立 KDS/OKF candidate fact mapping。
- 采集 14 仓 `codegraph status --json .` 与 `git status --short -- .codegraph`。
- 固化 5 个 validator。

## 输出

- `docs/harness/evidence/codegraph-project-group-full-coverage-20260621.json`
- `docs/harness/evidence/codegraph-project-group-full-coverage-20260621.md`
- `tools/kds-sync/validate_codegraph_project_group_full_coverage.py`
- `tools/kds-sync/validate_codegraph_authorization_model.py`
- `tools/kds-sync/validate_codegraph_loop_schema.py`
- `tools/kds-sync/validate_codegraph_waes_gate_policy.py`
- `tools/kds-sync/validate_codegraph_kds_candidate_policy.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_project_group_full_coverage.py`
- `python3 tools/kds-sync/validate_codegraph_authorization_model.py`
- `python3 tools/kds-sync/validate_codegraph_loop_schema.py`
- `python3 tools/kds-sync/validate_codegraph_waes_gate_policy.py`
- `python3 tools/kds-sync/validate_codegraph_kds_candidate_policy.py`
- `python3 tools/kds-sync/document_control.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

本轮把 CodeGraph 固化为项目群 Code Intelligence Fabric 的治理层、证据层和门禁输入层。当前状态为 `review_required`；不声明 accepted、integrated 或 production_ready。下一轮进入 `GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004`，继续检查 steady-state、GFIS policy exception 与 GPCF 本轮新增治理文件引发的 pending sync。
