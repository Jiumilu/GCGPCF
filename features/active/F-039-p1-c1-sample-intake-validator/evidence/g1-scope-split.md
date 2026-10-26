---
doc_id: GPCF-DOC-F039-EVIDENCE-G1
title: F-039 G1 scope split（Lead/Recorder 证据）
project: GPCF
related_projects: [GPCF]
domain: governance
status: draft
version: v0.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-039-p1-c1-sample-intake-validator/evidence/g1-scope-split.md
source_path: features/active/F-039-p1-c1-sample-intake-validator/evidence/g1-scope-split.md
sync_direction: bidirectional
last_reviewed: 2026-10-26
supersedes: []
superseded_by: []
---

# F-039 G1 scope split（Lead/Recorder 证据）

本文件用于把 **Dispatcher 建 Feature 的登记产物** 与 **coder-01 的代码 diff** 分开，避免把 `runtime/queue.json`、`runtime/state.json`、`features/F-039` 登记文件误算作 coder 越界。

## 1. Dispatcher 前置产物（19:29，非 coder）

- `features/active/F-039-p1-c1-sample-intake-validator/feature.yaml`
- `features/active/F-039-p1-c1-sample-intake-validator/journal.md`
- `features/active/F-039-p1-c1-sample-intake-validator/evidence/.gitkeep`
- `features/active/F-039-p1-c1-sample-intake-validator/artifacts/.gitkeep`
- `runtime/queue.json`（新增 F-039 条目）
- `runtime/state.json`（current_feature=F-039）
- `runtime/logs/F-039.jsonl`

## 2. coder-01 代码/测试/fixture（19:31–19:51）

首轮：
- `scripts/p1_sample_intake_validator.py`
- `tests/test_p1_sample_intake_validator.py`
- `tests/fixtures/p1_sample_intake_valid.yaml`
- `tests/fixtures/p1_sample_intake_missing_field.yaml`
- `tests/fixtures/p1_sample_intake_unauthorized.yaml`

条件返修（19:51）：
- 同 2 个代码/测试文件；新增枚举、敏感覆盖（+86/分隔手机号、身份证、姓名/地址键、JWT/Base64）、`--allow-sensitive FIELD=REASON` 审计、approved_by 不回显；测试 18→55。
- 3 个 fixture 内容未改。

以上 5 个文件均在 `scope.in` / `allowed_files` 内；未改既有 `gpcf_*.py` / `config/**`；未 commit/push。

## 3. 验证

- `pytest tests/test_p1_sample_intake_validator.py -q` → **55 passed**（reviewer/tester 独立复跑）
- 3 fixture → 0 / 1 / 1
- 条件项：枚举负例、+86/分隔手机号、身份证、姓名/地址键、JWT/Base64、豁免 reason、approved_by 无原值均闭合
- F11 仍开：coder/reviewer/tester 均 deepseek-flash；需人工/异模型复核
- 证据文件归属：`evidence/*`（tests/build/screenshots/api/summary/g1-scope-split）为 Lead/Recorder 生成，不属于 coder diff；`evidence/.gitkeep` 为 Dispatcher 前置

## 4. Build/lint 证据限制

- `build.txt` 的 `git diff --check` 只覆盖 **tracked** 文件；本 Feature 5 个交付文件均为 untracked，因此该行不能单独证明新文件 lint 已过。
- 新文件由 `py_compile` 覆盖语法；未做 whitespace/lint 全量检查。
- `summary.md` 中“lint 已通过 build 证据中的 git diff --check 覆盖”对 untracked 新文件不成立；以本节为准。

## 5. 非声明

- 未合并/未发布/未接真实数据；不声明生产可用。
