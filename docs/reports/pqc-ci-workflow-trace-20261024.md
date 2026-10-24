---
doc_id: GPCF-DOC-F63BAE8881
title: PQC CI test/build 工作流留痕（跨仓，模型授权）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/pqc-ci-workflow-trace-20261024.md
source_path: docs/reports/pqc-ci-workflow-trace-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# PQC CI test/build 工作流留痕（跨仓，模型授权）

- 时间：2026-10-24 15:28｜授权：`decide_template(authorization_qa)` → **probability_yes 0.839 / verdict yes**
- 依据：老卢 2026-10-24 授权「自动按决策模型推荐选择确认」；P16-2 优先级第 1 档（真实试点相关仓）

## 1. 改动（跨仓新增 1 文件，未提交）

`GlobalCloud PQC/.github/workflows/test-build.yml`：

| job | 内容 | 本地等价验证 |
|---|---|---|
| `test` | `cd backend && uv sync && uv run pytest -q tests/test_ext_contract_*.py` | **39 passed**（3.64s） |
| `build` | AST 语法解析（无产物，避免超长文件名导致的 `.pyc` 失败） | **128 文件，0 失败** |

runner 沿用仓内 `standards.yml` 既有约定 `[self-hosted, macOS]`，`concurrency` 与 `permissions` 同口径。

## 2. 覆盖变化（实判扫描器）

| 指标 | 改前 | 改后 |
|---|---:|---:|
| test 覆盖 | 10/29 | **11/29** |
| build 覆盖 | 13/29 | **14/29** |

## 3. 回滚

```bash
cd "GlobalCloud PQC"
rm .github/workflows/test-build.yml
```

## 4. 边界

- 只新增 CI 文件，未改任何业务代码；
- 若属主希望改为 `[self-hosted, linux]` 或加缓存，可自行调整；
- 不构成任何状态提升（不声明 accepted/integrated/production_ready）。
