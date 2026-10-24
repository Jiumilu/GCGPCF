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

# P16-2 · test/build CI 模板（供 25 仓属主复制）

- 日期：2026-10-24｜依据：P16-1+2 裁定（standards 强制、test/build 属主补齐）
- 实测覆盖：29 仓中 test 仅 6、build 仅 6（截至 2026-10-24），缺口 25 仓
- 本文件只给模板与判据，GPCF 不代写各仓 workflow（纪律⑤）

## 1. 模板（`.github/workflows/test-build.yml`）

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

## 3. 缺口仓清单（25，截至 2026-10-24）

AAAS、Brain、WAS、WAME、GPC、Studio、GPCF、XWAIL、GFIS、KDS、PVA、SOP、PKC、XGD、ICP、PQC、
SpaceAI Platform、World、Mem(GCMEM)、WAE、SLC、DRC、FireQuote、MMC（仅 test）、SpaceAI Studio（仅 test）

> 6 仓已具备：XiaoC、XiaoG、PMC、PDC（test+build）、MMC、SpaceAI Studio（仅 test）

## 4. 优先级建议

1. **先补 3 个真实试点相关仓**：PQC、PVA、WAE；
2. 再补主链：WAME、GPC、GFIS、KDS；
3. 其余按属主排期。
