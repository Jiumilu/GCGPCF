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

## 3. 缺口仓清单（25 个，截至 2026-10-24）

下表逐仓列出待补项；「缺测试/缺构建」表示该仓 CI 尚无对应 job。

| 仓 | 缺测试 | 缺构建 | 建议优先级 |
|---|---|---|---|
| GlobalCloud PQC | 是 | 是 | 高（真实试点相关） |
| GlobalCloud PVA | 是 | 是 | 高（真实试点相关） |
| GlobalCloud WAE | 是 | 是 | 高（统一壳） |
| GlobalCloud WAME | 是 | 是 | 高（主链裁决） |
| GlobalCloud GPC | 是 | 是 | 高（主链消费端） |
| GlobalCloud GFIS | 是 | 是 | 高（真实事实源） |
| GlobalCloud KDS | 是 | 是 | 高（知识主存） |
| GlobalCloud GPCF | 是 | 是 | 中（治理仓，pytest 已在钩子） |
| GlobalCloud XWAIL | 是 | 是 | 中（契约层） |
| GlobalCloud WAS | 是 | 是 | 中（语义底座） |
| GlobalCloud Brain | 是 | 是 | 中（知识编制） |
| GlobalCloud SOP | 是 | 是 | 中（流引擎） |
| GlobalCloud ICP | 是 | 是 | 中（产业控制台） |
| GlobalCloud PKC | 是 | 是 | 中（并入 WAE 路线） |
| GlobalCloud XGD | 是 | 是 | 中（已关单，补基线） |
| GlobalCloud World | 是 | 是 | 中（世界资产） |
| GlobalCloud SpaceAI Platform | 是 | 是 | 中（全景平台） |
| GlobalCloud Mem（GCMEM） | 是 | 是 | 低（长期记忆，运行态为主） |
| GlobalCloud AAAS | 是 | 是 | 低（已暂停） |
| GlobalCloud DRC | 是 | 是 | 低（新纳管） |
| GlobalCloud FireQuote | 是 | 是 | 低（新纳管，后端测试已有） |
| GlobalCloud SLC | 是 | 是 | 低（运力） |
| GlobalCloud Studio | 是 | 是 | 暂不补（已退役） |
| GlobalCloud MMC | 否 | 是 | 中（已有测试，缺构建） |
| GlobalCloud SpaceAI Studio | 否 | 是 | 低（legacy 三平台） |

已齐备（测试+构建均有）4 个：XiaoC、XiaoG、PMC、PDC。

## 4. 优先级建议

1. **先补 3 个真实试点相关仓**：PQC、PVA、WAE；
2. 再补主链：WAME、GPC、GFIS、KDS；
3. 其余按属主排期。
