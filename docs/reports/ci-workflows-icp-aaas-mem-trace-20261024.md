---
doc_id: GPCF-DOC-0F9C2C3BD9
title: ICP / AAAS / Mem CI test-build 工作流留痕（跨仓，模型逐仓裁决）
project: GPCF
related_projects: [GPCF, XGD, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/ci-workflows-icp-aaas-mem-trace-20261024.md
source_path: docs/reports/ci-workflows-icp-aaas-mem-trace-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# ICP / AAAS / Mem CI test-build 工作流留痕（跨仓，模型逐仓裁决）

- 时间：2026-10-24 15:50｜授权：逐仓 `decide_template(authorization_qa)`，**只采纳 verdict=yes**

| 仓 | 本地验证 | 模型 yes | 裁决 | 执行 |
|---|---|---:|---|---|
| GlobalCloud ICP | `pytest -q` → **33 passed** | 0.576 | yes | ✅ |
| GlobalCloud AAAS | `pytest -q` → **10 passed** | 0.640 | yes | ✅（该仓处置为 pause，仅补 CI 基线） |
| GlobalCloud Mem（GCMEM） | `pytest -q` → **649 passed** | 0.627 | yes | ✅ |

## 新增内容（各 1 文件，未提交跨仓）

`<repo>/.github/workflows/test-build.yml`：`test` = `python3 -m pytest -q`；`build` = AST 语法解析（无产物）；runner 沿用各仓 `standards.yml` 的 `[self-hosted, macOS]`。

## 覆盖实判变化

| 指标 | 本轮前 | 本轮后 |
|---|---:|---:|
| test 覆盖 | 21/29 | **24/29** |
| build 覆盖 | 17/29 | **20/29** |

## 扫描器口径改进（本轮）

新增 **npm/pnpm/yarn 脚本体展开**（递归 3 层）：`quality:ci` 这类封装脚本里的 test/build 命令现在能被识别，
XGD、SpaceAI Platform、SpaceAI Studio、PMC 等由误报缺失转为按实际判定（XGD/PMC 仍缺 build，属实）。

## 回滚

```bash
cd "GlobalCloud ICP" && rm .github/workflows/test-build.yml
cd "GlobalCloud AAAS" && rm .github/workflows/test-build.yml
cd "GlobalCloud Mem" && rm .github/workflows/test-build.yml
```
