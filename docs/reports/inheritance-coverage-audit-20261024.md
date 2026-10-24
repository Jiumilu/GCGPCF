---
doc_id: GPCF-DOC-4531130BE2
title: 跨仓方案继承覆盖审计（29 仓全量，2026-10-24）
project: KDS
related_projects: [GPC, WAME, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/inheritance-coverage-audit-20261024.md
source_path: docs/reports/inheritance-coverage-audit-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 跨仓方案继承覆盖审计（29 仓全量，2026-10-24）

- 依据校验器：`validate_project_plan_inheritance.py`（门禁内，2026-10-24 纳入）
- 口径：①文件存在 ②含控制 token `GPCF:01-architecture/GlobalCloud 项目群总体方案.md` ③11 个必备章节齐全

## 1. 结论

| 状态 | 仓数 | 说明 |
|---|---:|---|
| ✅ 合规（token + 11 节） | 16 | 校验器当前覆盖的仓全部在此列 |
| ⚠️ 部分缺失 | 8 | 有文件但缺 token 或缺章节 |
| ❌ 无总体方案文件 | 5 | PQC / SpaceAI / SpaceAI Studio / SLC / FireQuote |

## 2. 部分缺失明细

| 项目 | 仓 | 文件 | 有 token | 章节数/11 |
|---|---|---|---:|---:|
| GPC | GlobalCloud GPC | GPC-绿色供应链公共服务平台-总体方案.md | — | 0 |
| ICP | GlobalCloud ICP | GlobalCloud ICP 总体方案.md | — | 1 |
| World | GlobalCloud World | GlobalCloud World 总体方案.md | ✓ | 6 |
| GCMEM | GlobalCloud Mem | GlobalCloud GCMEM 总体方案.md | — | 0 |
| WAE | GlobalCloud WAE | GlobalCloud WAE 总体方案.md | — | 0 |
| Project | GlobalCloud PMC | GlobalCloud Project 总体方案.md | — | 0 |
| PDC | GlobalCloud PDC | GlobalCloud PDC 总体方案.md | — | 10 |
| DRC | GlobalCloud DRC | GlobalCloud DRC 总体方案.md | — | 0 |

## 3. 无总体方案文件的 5 仓

| 项目 | 仓 | 建议 |
|---|---|---|
| PQC | GlobalCloud PQC | 属主补总体方案（含 11 节） |
| SpaceAI | GlobalCloud SpaceAI Platform | 确认是否保留；若保留需补总体方案 |
| SpaceAIStudio | GlobalCloud SpaceAI Studio | 确认是否保留；若保留需补总体方案 |
| SLC | GlobalCloud SLC | 确认是否保留；若保留需补总体方案 |
| FireQuote | GlobalCloud FireQuote | 属主补总体方案（含 11 节） |

## 4. 与校验器覆盖的关系

`validate_project_plan_inheritance.py` 目前只校验**固定 10 个文件**（GPCF/WAME/PVA/SOP/KDS/Brain/Studio/MMC/PKC/XGD/XiaoC/XiaoG 中的一部分），
因此上表 13 个非合规仓**不会**导致门禁失败。若要把该不变量扩展到 29 仓，需：
1. 属主补章节（大部分仓缺 8–11 节，工作量在属主侧）；
2. 校验器文件清单扩到 29（GPCF 侧一次性改，但会让门禁转红直到属主补齐）。

**建议**：先按本表派单给属主补「项目定位 + 与项目群主方案的继承关系 + 不声明边界」三节和 token（最小集），再考虑扩覆盖。

## 5. 边界

本审计只读，未改任何仓内容；不构成状态提升。
