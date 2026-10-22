---
doc_id: GPCF-DOC-748674198C
title: P16-2 · test/build 属主补齐清单（29 仓实测）
project: KDS
related_projects: [GFIS, GPC, WAME, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio, Project]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/p16-test-build-owner-checklist-20261022.md
source_path: docs/reports/p16-test-build-owner-checklist-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P16-2 · test/build 属主补齐清单（29 仓实测）

- 依据：老卢 2026-10-22 22:21 裁定「P16-1+2」；矩阵 `_governance/ci-matrix.yaml`
- 现状：`standards` 29/29 已具备（CI 中已是 required）；`test` 6/29、`build` 6/29
- 本单只列缺口与判据，GPCF 不代写各仓 workflow

## 1. 已具备（无需动作，6 仓）

| 仓 | 已有 job |
|---|---|
| GlobalCloud XiaoC | test / build |
| GlobalCloud MMC | test |
| GlobalCloud XiaoG | test / build / e2e |
| GlobalCloud SpaceAI Studio | test |
| GlobalCloud PMC | test / build |
| GlobalCloud PDC | test / build |

## 2. 缺口（23 仓，需属主补 workflow）

AAAS、Brain、WAS、WAME、GPC、Studio、GPCF、XWAIL、GFIS、KDS、PVA、SOP、PKC、XGD、ICP、PQC、
SpaceAI Platform、World、Mem(GCMEM)、WAE、SLC、DRC、FireQuote

## 3. 补齐判据（每仓）

```bash
# 1) 存在 test 与 build job
grep -lE "^\s{2,}(test|build):" .github/workflows/*.yml
# 2) 至少一次绿构建（Actions 页面或 gh run list --limit 1）
gh run list --workflow=<file> --limit 1 --json conclusion | jq '.[0].conclusion=="success"'
# 3) 门禁只查"存在 + 最近一次绿"，不查覆盖率
```

## 4. 非声明

- 补齐 workflow ≠ 产品验收通过；不得据此声明 accepted/integrated/production_ready；
- UI 仓的 e2e/browser/a11y 属 P16-3，本轮不强制。
