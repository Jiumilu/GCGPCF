---
doc_id: GPCF-DOC-6C2F2CC1ED
title: CodeGraph Impact Report Dry-run Evidence
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-impact-report-dry-run-20260621.md
source_path: docs/harness/evidence/codegraph-impact-report-dry-run-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph Impact Report Dry-run Evidence

本轮执行 `GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005`，用低风险 GPCF 治理 validator 作为 dry-run 对象，验证 CodeGraph impact report 是否能形成 Loop/Harness/WAES/KDS 可用证据。

## Dry-run 对象

| 字段 | 值 |
|---|---|
| repo | GlobalCoud GPCF |
| change_type | governance_validator_and_evidence_dry_run |
| target_file | `tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py` |
| business_development | false |
| commit_or_push | false |
| deploy | false |

## CodeGraph 查询结果

| 查询 | 作用 | 结果 |
|---|---|---|
| `codegraph query codegraph_project_group_steady_state_verify --json` | 定位 validator 与证据常量 | 4 results |
| `codegraph node tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py` | 读取目标文件和 indexed dependents | 129 lines / 9 symbols / 0 dependents |
| `codegraph affected tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py --json` | 选择受影响测试 | 0 affected tests / 0 traversed dependents |
| `codegraph explore validate_codegraph_project_group_steady_state_verify REPOS evidence` | 找相邻 validator 模式 | 8 symbols / 8 files |
| `codegraph impact main --depth 2` | 宽泛符号负例 | 101 affected symbols，不能作为门禁证据 |

## rg 基线

同等关键词用 `rg` 扫描得到 16 个 matched files / 31 个 matched lines。rg 能定位文本，但不能直接给出符号、依赖、受影响测试或宽泛查询噪声判断。

## Impact Report

| 项 | 结论 |
|---|---|
| changed_files | `tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py` |
| impacted_symbols | file + `EVIDENCE_JSON`、`EVIDENCE_MD`、`LOOP_ROUND`、`REPOS`、`require`、`read`、`run`、`main` |
| impacted_tests | none |
| impacted_docs | steady-state JSON、Markdown、Loop round |
| risk_level | low |
| waes_required | false |
| committee_required | false |

## 实际作用

- CodeGraph 把影响分析从文本命中转成文件、符号、测试和依赖判断。
- CodeGraph 明确证明目标 validator 无 indexed dependents、无 affected tests。
- CodeGraph 也暴露了宽泛 `main` 查询的噪声风险，因此后续门禁必须使用限定文件或限定符号查询。
- 本轮只是 impact report dry-run，不证明业务完成、不升级 accepted/integrated/production_ready。

## 下一轮

`GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006`
