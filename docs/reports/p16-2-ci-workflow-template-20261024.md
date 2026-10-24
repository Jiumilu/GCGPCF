---
doc_id: GPCF-DOC-A718A6E63A
title: P16-2 · test/build CI 模板（供 25 仓属主复制）
project: KDS
related_projects: [GFIS, GPC, WAME, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/p16-2-ci-workflow-template-20261024.md
source_path: docs/reports/p16-2-ci-workflow-template-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P16-2 · test/build CI 模板与覆盖实判（2026-10-24 更正）

- 日期：2026-10-24｜依据：P16-1+2 裁定（standards 强制、test/build 属主补齐）
- 实测覆盖（**按 workflow 步骤实际命令判定**，2026-10-24 更正）：standards **29/29**、test **10/29**、build **12/29**
- 本文件只给模板与判据，GPCF 不代写各仓 workflow（纪律⑤）

## 1. 模板（`.github/workflows/test-build.yml`，属主复制用）

```yaml
name: test-build
on:
  push: { branches: [main] }
  pull_request: {}
jobs:
  standards:
    runs-on: self-hosted            # 各仓既有 runner 口径为准
    steps:
      - uses: actions/checkout@v4
      - name: 项目群标准检查
        run: python3 "../../_governance/tools/gc_standard.py" check --repo "<仓库名>" --fail-on error
  test:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: 安装依赖
        run: |
          if [ -f package.json ]; then pnpm install --frozen-lockfile || npm ci; fi
          if [ -f pyproject.toml ] || [ -f requirements.txt ]; then uv sync || pip install -r requirements.txt; fi
      - name: 测试
        run: |
          if [ -f package.json ]; then pnpm test || npm test; fi
          if [ -f pyproject.toml ]; then uv run pytest -q; fi
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: 构建
        run: |
          if [ -f package.json ]; then pnpm build || npm run build; fi
          if [ -f pyproject.toml ]; then python3 -m compileall -q . || true; fi
```

## 2. 每仓改造判据（P16 验收口径）

1. `.github/workflows/` 中存在 `test` 与 `build` job（名称包含即可）；
2. 至少一次 **success** 运行：`gh run list --workflow=test-build.yml --limit 1 --json conclusion`；
3. `standards` job 固定存在（P16-1 已要求）；
4. 不要求覆盖率阈值、不要求 e2e/browser/a11y（属 P16-3）。

## 3. 覆盖与缺口（按步骤实判，2026-10-24 15:28 更新）

> 判定方式：解析 `steps[].run` 实际命令。本轮：PQC 新增 test-build 工作流（模型授权），test 11/29、build 14/29。

| 仓 | standards | test | build | test 依据 | build 依据 |
|---|---|---|---|---|---|
| GlobalCloud AAAS | ✓ | — | — | — | — |
| GlobalCloud Brain | ✓ | ✓ | ✓ | pnpm test | pnpm build |
| GlobalCloud WAS | ✓ | — | — | — | — |
| GlobalCloud XiaoC | ✓ | ✓ | ✓ | pnpm test | pnpm build |
| GlobalCloud WAME | ✓ | ✓ | ✓ | python3 -m unittest | npm run build |
| GlobalCloud GPC | ✓ | — | ✓ | — | compileall |
| GlobalCloud Studio | ✓ | — | ✓ | — | npm run build |
| GlobalCloud GPCF | ✓ | ✓ | ✓ | pytest | ast.parse |
| GlobalCloud XWAIL | ✓ | — | — | — | — |
| GlobalCloud GFIS | ✓ | — | ✓ | — | compileall |
| GlobalCloud MMC | ✓ | ✓ | — | pytest, vitest | — |
| GlobalCloud KDS | ✓ | — | — | — | — |
| GlobalCloud XiaoG | ✓ | — | ✓ | — | npm run build |
| GlobalCloud PVA | ✓ | ✓ | ✓ | npm test | npm run build |
| GlobalCloud SOP | ✓ | — | — | — | — |
| GlobalCloud PKC | ✓ | — | — | — | — |
| GlobalCloud XGD | ✓ | — | — | — | — |
| GlobalCloud ICP | ✓ | — | — | — | — |
| GlobalCloud PQC | ✓ | ✓ | ✓ | pytest | ast.parse |
| GlobalCloud SpaceAI Platform | ✓ | ✓ | — | vitest | — |
| GlobalCloud SpaceAI Studio | ✓ | ✓ | — | cargo test, pnpm test | — |
| GlobalCloud World | ✓ | — | ✓ | — | npm run build |
| GlobalCloud Mem | ✓ | — | — | — | — |
| GlobalCloud WAE | ✓ | ✓ | ✓ | pnpm test | pnpm build |
| GlobalCloud PMC | ✓ | ✓ | — | pytest | — |
| GlobalCloud PDC | ✓ | — | ✓ | — | npm run build |
| GlobalCloud SLC | ✓ | — | ✓ | — | npm run build |
| GlobalCloud DRC | ✓ | — | — | — | — |
| GlobalCloud FireQuote | ✓ | — | — | — | — |

缺口统计：**test 缺 18 仓、build 缺 15 仓**（standards 29/29）。

复跑：`python3 tools/kds-sync/scan_ci_coverage.py --markdown`

## 4. 优先级建议

1. **先补 3 个真实试点相关仓**：PQC、PVA、WAE；
2. 再补主链：WAME、GPC、GFIS、KDS；
3. 其余按属主排期。
