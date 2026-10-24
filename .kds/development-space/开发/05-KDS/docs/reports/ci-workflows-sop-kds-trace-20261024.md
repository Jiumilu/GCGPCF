---
doc_id: GPCF-DOC-13707BF76C
title: SOP / KDS CI test-build 工作流留痕（跨仓，模型授权分批裁决）
project: KDS
related_projects: [WAME, KDS, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/ci-workflows-sop-kds-trace-20261024.md
source_path: docs/reports/ci-workflows-sop-kds-trace-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# SOP / KDS CI test-build 工作流留痕（跨仓，模型授权分批裁决）

- 时间：2026-10-24 15:40｜授权方式：`decide_template(authorization_qa)` 逐仓出概率，**只采纳 verdict=yes 的仓**

## 1. 三仓裁决与执行

| 仓 | 本地验证 | 模型 yes 概率 | verdict | 是否执行 |
|---|---|---:|---|---|
| GlobalCloud SOP | `python3 -m pytest -q` → **19 passed** | 0.610 | yes | ✅ 已新增 |
| GlobalCloud KDS | `python3 -m pytest tests -q` → **exit 0** | 0.542 | yes | ✅ 已新增 |
| GlobalCloud PKC | `npm test` → 151 passed | 0.455 | **no** | ❌ 未执行（交属主） |

> 说明：PKC 虽然本地测试通过，但模型判 no（0.455 < 0.5），按"只采纳推荐"的授权边界**不执行**，留清单给属主。

## 2. 新增内容（各 1 文件，未提交跨仓）

`<repo>/.github/workflows/test-build.yml`：
- `test` job：Python 仓直接 `python3 -m pytest`（KDS 指定 `tests` 子目录）；
- `build` job：AST 语法解析（无产物，规避超长文件名 `.pyc` 问题）；
- runner 沿用各仓 `standards.yml` 的 `[self-hosted, macOS]`。

## 3. 覆盖实判变化

| 指标 | 本轮前 | 本轮后 |
|---|---:|---:|
| test 覆盖 | 18/29 | **20/29** |
| build 覆盖 | 14/29 | **16/29** |

## 4. 回滚

```bash
cd "GlobalCloud SOP" && rm .github/workflows/test-build.yml
cd "GlobalCloud KDS" && rm .github/workflows/test-build.yml
```

## 5. 边界

仅新增 CI 文件，未改业务代码；不构成任何状态提升。

> **激活状态（2026-10-24 16:25 更正）**：本文件所述为**工作区口径**（文件已准备）。该文件在属主仓内仍是未跟踪状态、尚未在 CI 生效；激活与回滚步骤见 `ci-activation-checklist-20261024.md`。
