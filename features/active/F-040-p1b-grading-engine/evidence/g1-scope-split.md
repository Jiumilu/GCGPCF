---
doc_id: GPCF-DOC-F040-EVIDENCE-G1
title: F-040 G1 scope split（Lead/Recorder 证据）
project: GPCF
related_projects: [GPCF]
domain: governance
status: draft
version: v0.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-040-p1b-grading-engine/evidence/g1-scope-split.md
source_path: features/active/F-040-p1b-grading-engine/evidence/g1-scope-split.md
sync_direction: bidirectional
last_reviewed: 2026-10-26
supersedes: []
superseded_by: []
---

# F-040 G1 scope split（Lead/Recorder 证据）

本文件把 **F-040 引擎/pipeline 的代码/测试/fixtures** 与 F-039、Dispatcher 登记产物分开，避免把 F-039 或 runtime 变更误算作 F-040 越界。

## 1. F-040 交付文件（scope.in）

| 文件 | SHA-256 |
|---|---|
| `scripts/p1b_grading_engine.py` | `1068401a46327501efa81ddcf214734d3d69a08e9c2bf85a595d998b78331553` |
| `scripts/p1b_pipeline.py` | `dee99188b90c54de3dfbf58f546d03e0dd725ee2c7de53861201ad0208af92a0` |
| `tests/test_p1b_grading_engine.py` | `34fc702b355ba3f661dd985ebb338a017a23fd10139124bc1d3119bd68127f39` |
| `tests/test_p1b_pipeline.py` | `63dcc402a20d7b42f4640bd5604c65d62a9e0f0c79d1dcea425aae30e04b4b4f` |
| `tests/fixtures/p1b/demand_e1.json` | `58b5a2e98b6cf2341adb5db86c78c2e22aab60e215cd3966653b55d08b488e4f` |
| `tests/fixtures/p1b/demand_e2.json` | `52c9a9c1c93092cb0a4fe1bdf6eb8e41fbff07071d696fd7ab9d7dabcd11aaaa` |
| `tests/fixtures/p1b/defect_e1.json` | `23ecde863faf5232cb1997a1d5ed2d2bdc5b440258961c9d2273444f5c58e29f` |
| `tests/fixtures/p1b/defect_e2.json` | `3d390e8fabc861cc0022bf06f2dd1d85f57f39a46066bd4827038682c1f08727` |
| `tests/fixtures/p1b/demand_test.json` | `71421779d7906e776372faf5d3a5742461ba1b7cca8634ec5424acc04ea8cef8` |
| `tests/fixtures/p1b/demand_trial.json` | `73283a2673695a8a555b8472e583f012dadfa39fbeecc430b2c1b4228ea41c57` |

## 2. 依赖：F-039（C1 校验器）

- `scripts/p1b_pipeline.py` 在模块加载时 `from p1_sample_intake_validator import validate_document`；
- 该文件属于 F-039，不在 F-040 scope；
- F-040 `feature.yaml` 已声明 `depends_on: [F-039]`；
- 合并顺序：F-039 先，或 F-039+F-040 一起；否则 pipeline ImportError；
- 组合测试：`pytest tests/test_p1_sample_intake_validator.py tests/test_p1b_grading_engine.py tests/test_p1b_pipeline.py -q` → **90 passed**（F-039 55 + F-040 35）。

## 3. 非 F-040（同 worktree）

- F-039：`scripts/p1_sample_intake_validator.py`、`tests/test_p1_sample_intake_validator.py`、3 个 C1 fixture；属于 F-039。
- Dispatcher：`features/active/F-039/…`、`features/active/F-040/…` 登记文件、`runtime/queue.json`、`runtime/state.json`、`runtime/logs/F-039.jsonl`、`runtime/logs/F-040.jsonl`。
- 根因：F-039 未合并，F-040 为避 ID 冲突同 worktree；合并前需拆分/正式分支。

## 4. 验证

- 组合 pytest：**90 passed**（F-039 55 + F-040 35）
- F-040 Evidence Gate：tests/build/summary pass；screenshots/api waived；close_candidate=true
- `gpcf_check_evidence.py F-040 --check-only` → close_candidate=true，reasons=none
- 未 commit/push/merge；未接真实数据/网络/价格

## 5. Build/lint 限制

- 10 个交付文件均为 untracked；`git diff --check` 只覆盖 tracked 文件，不能单独证明新文件 lint。
- `py_compile` 覆盖语法；未做 whitespace/lint 全量检查。
- `summary.md` 的“lint 已通过 build 证据中的 git diff --check 覆盖”对 untracked 不成立；以本节为准。

## 6. 非声明

- 未合并/未发布/未接真实数据；不声明生产可用。
