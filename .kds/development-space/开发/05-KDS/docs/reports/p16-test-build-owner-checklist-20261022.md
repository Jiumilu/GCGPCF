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

> ⚠️ **已被取代**（2026-10-24）：本文件保留备查，最新口径见 `docs/reports/INDEX.md` 第 8 节。


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

下表逐仓列出待补项，`缺 test` 表示该仓 CI 中尚无 test job，`缺 build` 表示尚无 build job；两列同时标注即为两项都要补。

| 仓 | 缺 test | 缺 build | 备注 |
|---|---|---|---|
| GlobalCloud AAAS | 是 | 是 | 服务包与运营类，补最小单测与构建 |
| GlobalCloud Brain | 是 | 是 | 知识编制，前端构建已有本地脚本 |
| GlobalCloud WAS | 是 | 是 | 语义底座，补规则校验单测 |
| GlobalCloud WAME | 是 | 是 | 裁决引擎，E1 启动后同步补 |
| GlobalCloud GPC | 是 | 是 | 消费端已有仓内单测，仅缺 CI job |
| GlobalCloud Studio | 否 | 是 | 已退役项目，仅补构建或登记豁免 |
| GlobalCloud GPCF | 是 | 是 | 治理仓，pytest 已在 pre-commit，需补 CI job |
| GlobalCloud XWAIL | 是 | 是 | 契约层，补 schema 校验 |
| GlobalCloud GFIS | 是 | 是 | 工厂事实源，补集成单测 |
| GlobalCloud KDS | 是 | 是 | 知识主存，补只读索引校验 |
| GlobalCloud PVA | 是 | 是 | 门户底座，补身份上下文单测 |
| GlobalCloud SOP | 是 | 是 | 流引擎，补规则包校验 |
| GlobalCloud PKC | 是 | 是 | 个人工作台，已并入 WAE 路线 |
| GlobalCloud XGD | 是 | 是 | 常驻智能体，F-031 已关单 |
| GlobalCloud ICP | 是 | 是 | 产业控制台，补契约单测 |
| GlobalCloud PQC | 是 | 是 | 真实试点项目，优先补齐 |
| GlobalCloud SpaceAI Platform | 是 | 是 | 全景平台，本地有 vitest |
| GlobalCloud World | 是 | 是 | 世界资产纳管 |
| GlobalCloud Mem（GCMEM） | 是 | 是 | 长期记忆，补运行态单测 |
| GlobalCloud WAE | 是 | 否 | 统一壳，已有构建 job |
| GlobalCloud SLC | 是 | 否 | 运力，已有构建 job |
| GlobalCloud DRC | 是 | 是 | 数据资源目录 |
| GlobalCloud FireQuote | 是 | 是 | 消防定额，已有 89 项后端测试可接 CI |

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
