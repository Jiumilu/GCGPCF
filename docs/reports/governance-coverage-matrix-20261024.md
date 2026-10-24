---
doc_id: GPCF-DOC-2F9FFC0B41
title: "28/29 仓治理覆盖总矩阵（2026-10-24 17:40）"
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAME, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/governance-coverage-matrix-20261024.md
source_path: docs/reports/governance-coverage-matrix-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 28/29 仓治理覆盖总矩阵（2026-10-24 17:40）

一份表把此前的三项审计合到一起：**总体方案继承 / 本地门禁委托 / CI（standards·test·build，均取远端生效口径）**。

## 1. 覆盖矩阵（由脚本生成，可复跑）

复跑：`python3 scripts/gpcf_governance_matrix.py`（加 `--json` 取机器可读）

| 项目 | 总体方案继承 | 本地门禁 | standards | test(远端) | build(远端) |
|---|---|---|---|---|---|
| AAAS | 无文件 | 委托 | ✓ | ✓ | ✓ |
| Brain | 合规 | 委托 | ✓ | ✓ | ✓ |
| WAS | 无文件 | 委托 | ✓ | — | — |
| XiaoC | 合规 | 委托 | ✓ | ✓ | ✓ |
| WAME | 合规 | 委托 | ✓ | ✓ | ✓ |
| GPC | 不合规 | 委托 | ✓ | ✓ | ✓ |
| Studio | 合规 | 委托 | ✓ | ✓ | ✓ |
| GPCF | 合规 | 正本 | ✓ | ✓ | ✓ |
| XWAIL | 合规 | 委托 | ✓ | — | — |
| GFIS | 合规 | 委托 | ✓ | ✓ | ✓ |
| MMC | 合规 | 委托 | ✓ | ✓ | — |
| KDS | 合规 | 委托 | ✓ | ✓ | ✓ |
| XiaoG | 合规 | 委托 | ✓ | ✓ | ✓ |
| PVAOS | 合规 | 委托 | ✓ | ✓ | ✓ |
| SOP | 合规 | 委托 | ✓ | ✓ | ✓ |
| PKC | 合规 | 委托 | ✓ | — | — |
| XGD | 合规 | 委托 | ✓ | ✓ | — |
| ICP | 部分 | 无 | ✓ | ✓ | ✓ |
| PQC | 无文件 | 委托 | ✓ | ✓ | ✓ |
| SpaceAI | 无文件 | 委托 | ✓ | ✓ | ✓ |
| SpaceAIStudio | 无文件 | 委托 | ✓ | ✓ | — |
| World | 部分 | 无 | ✓ | ✓ | ✓ |
| GCMEM | 不合规 | 无 | ✓ | ✓ | ✓ |
| WAE | 无文件 | 委托 | ✓ | ✓ | ✓ |
| Project | 不合规 | 委托 | ✓ | — | — |
| PDC | 部分 | 无 | ✓ | ✓ | ✓ |
| SLC | 无文件 | 无 | ✓ | ✓ | ✓ |
| DRC | 不合规 | 无 | ✓ | — | — |
| FireQuote | 无文件 | 无 | ✓ | ✓ | ✓ |

## 2. 统计

```
继承:  {'合规': 14, '部分': 3, '不合规': 4, '无文件': 8}
门禁: {'委托': 21, '正本': 1, '无': 7, '自实现/缺': 0}
CI 远端: standards 29/29 · test 24/29 · build 21/29
```

- 继承口径：根目录 `*总体方案.md` + token + 11 节齐全 = 合规
- 门禁口径：`tools/kds-sync/loop_document_gate.py` 含两个委托 token = 委托
- CI 口径：**远端生效**（`origin/main` workflow 内容）

## 3. 多维度同时缺失的仓（优先处置）

| 仓 | 缺项 | 建议 |
|---|---|---|
| DRC | 继承不合规 + 无门禁 + 无 test/build | 新纳管仓：四件套补齐（属主） |
| FireQuote | 无总体方案 + 无门禁（CI 已绿） | 补总体方案 + 委托脚本（属主） |
| GCMEM | 无总体方案 + 无门禁 | 补总体方案 + 委托脚本（属主） |
| World / PDC / ICP | 无门禁（其余尚可） | 补 17 行委托脚本即可 |
| SLC | 无总体方案 + 无门禁 | 按处置排期（当前 continue/support） |

## 4. 说明与口径

- 「继承」以根目录 `*总体方案.md` 为准（不含 `docs/` 下同义文件）；
- 「门禁」看 `tools/kds-sync/loop_document_gate.py` 是否含两个委托 token；
- 「test/build」取**远端生效**（`origin/main` 上的 workflow 内容），因此本地已提交未推送的不计；
- 本表是**只读审计**，未修改任何仓；不构成状态提升。

## 5. 与门禁的关系

当前门禁只校验：方案继承（固定 ~12 个文件）、门禁委托（3 个仓）。
因此本表中多数缺口**不会**让门禁转红；若要扩大覆盖，需先把缺口补齐再扩展校验清单，否则会立刻阻断全群提交。
