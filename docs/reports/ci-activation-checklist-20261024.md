---
doc_id: GPCF-DOC-C4E8E450FB
title: 已准备 CI 工作流：激活前检查与激活步骤（2026-10-24）
project: KDS
related_projects: [GPC, KDS, GPCF, ICP]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/ci-activation-checklist-20261024.md
source_path: docs/reports/ci-activation-checklist-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 已准备 CI 工作流：激活前检查与激活步骤（2026-10-24）

- 背景：前几轮为 7 个仓准备了 `.github/workflows/test-build.yml`，但**均为未跟踪文件、尚未生效**
- 本文件是激活前的最后检查清单；**激活 = 由各仓属主提交并 push**（GPCF 不代提交，纪律⑤）

## 1. 逐仓检查（2026-10-24 16:25 实测）

| 仓 | 文件 | runner 与仓内 standards.yml 一致 | 本地等价验证 | 依赖风险 |
|---|---|---|---|---|
| GlobalCloud PQC | `test-build.yml`（test+build） | ✅ `[self-hosted, macOS]` | `uv run pytest tests/test_ext_contract_*.py` → 39 passed | uv 路径：**已加 fallback**（`~/.local/bin/uv`） |
| GlobalCloud SOP | 同上 | ✅ | `pytest -q` → 19 passed | 仅需系统 python3 |
| GlobalCloud KDS | 同上（test 指定 `tests`） | ✅ | `pytest tests` → exit 0 | 仅需系统 python3 |
| GlobalCloud ICP | 同上 | ✅ | `pytest -q` → 33 passed | 仅需系统 python3 |
| GlobalCloud AAAS | 同上 | ✅ | `pytest -q` → 10 passed | 仅需系统 python3 |
| GlobalCloud Mem | 同上 | ✅ | `pytest -q` → 649 passed | 仅需系统 python3 |
| GlobalCloud FireQuote | 同上 | ✅ | `uv run pytest -q` → 89 passed / 1 skipped | uv 路径：**已加 fallback** |

build job 统一为 AST 语法解析（无产物），规避超长文件名导致的 `.pyc` 失败。

## 2. 激活步骤（逐仓执行，属主）

```bash
cd "GlobalCloud <仓>"
git add .github/workflows/test-build.yml
git commit -m "ci: 新增 test-build 工作流（P16-2）"
git push
gh run list --workflow=test-build.yml --limit 1 --json conclusion   # 期望 success
```

## 3. 回滚

```bash
cd "GlobalCloud <仓>"
git rm .github/workflows/test-build.yml && git commit -m "revert: 移除 test-build 工作流" && git push
```

## 4. 生效后的口径变化

| 口径 | 现在 | 全部激活后 |
|---|---|---|
| 已跟踪（真正进 CI） | test 18/29、build 16/29 | test 25/29、build 23/29 |

## 5. 边界

- 本清单不代表已生效；未激活前 P16-2 的"已跟踪口径"数字不会变化；
- 首次运行若失败（如 runner 缺 uv），按第 1 节依赖风险处置，不要直接删除工作流。
