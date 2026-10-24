---
doc_id: GPCF-DOC-7A1535F943
title: F-032 / PQC 对外服务 · M0 设计评审裁定（2026-10-24）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/f032-m0-review-ruling-20261024.md
source_path: docs/reports/f032-m0-review-ruling-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-032 / PQC 对外服务 · M0 设计评审裁定（2026-10-24）

- 裁定人：老卢（问答 + 决策模型）｜时间：2026-10-24 11:26
- 范围：PQC 对外服务（询价/测算/报价/订单，经 PVA PVAAI 服务桥承载）
- 非声明：本裁定只批准设计基线与契约版本；**不声明** production_ready / customer_accepted，也不改变 `C_real`（真实客户试点仍未启动）

## 1. 四项裁定

| # | 议题 | 决策模型 | 裁定 |
|---|---|---|---|
| 1 | M0 设计评审 | `gate` go 0.259（模型认为不触红线） | **通过 M0**，契约 `pqc-external-openapi.v1.yaml` 由 `1.0.0-draft` **冻结为 v1.0**；后续真实试点字段增补走 **v1.1** |
| 2 | 异议 O-1（BFF 路径） | 按实施现状 92.2% / 按基线 4.7% / 共存 3.1% | **按实施现状**：BFF 在 `src/app/supabase/functions/server/pqc.bridge.tsx`，由同目录 `index.tsx` 挂载；00 基线路径仅作历史表述 |
| 3 | 异议 O-2（卡片类型） | 合并 5 类 93.3% / 保留 6 类 6.1% / 先不定 0.5% | **合并为 5 类**（`pqc-quote` 内含 `pending_accept` 态） |
| 4 | 契约登记 GPCF | `gate` stop 0.905（需确认） | **登记为 controlled**：新增 `CONTRACT-PQC-PVA-EXTERNAL-SERVICE` + 关闭型冲突 `CONFLICT-09` |

## 2. GPCF 侧已完成（本文件提交内）

- `runtime/contract-matrix.yaml`：新增契约集合 `ext`、契约条目 1 条（controlled）、冲突 CONFLICT-09（closed）；
- 校验：`validate_contract_matrix.py` **exit 0**（schema/contract_sets/unique_id/schema_paths/evidence_paths/version/consumers/conflict_links/themes/sensitive 全 pass；9 条冲突 high 5 / medium 4）；
- 回执：`AUTH-PG-F032-M0-20261024`。

## 3. PQC / PVA 属主待执行（跨仓，GPCF 不代改）

| # | 动作 | 位置 | 判据 |
|---|---|---|---|
| 1 | 契约版本 `1.0.0-draft` → `1.0`，正文“状态：draft/待评审”改为“M0 通过（2026-10-24）” | `GlobalCloud PQC/docs/architecture/external-service/contracts/pqc-external-openapi.v1.yaml` | 文件内 `version: 1.0` |
| 2 | 设计分册 02 同步 O-1/O-2 裁定（BFF 路径、5 类卡片） | `.../02-PVAAI对话与应用接入设计.md` | 文档内 O-1/O-2 标注“已裁定” |
| 3 | 契约测试基线保持 ≥68 passed | `backend/tests/test_ext_*.py` | `bash scripts/verify_external_service.sh --fast` |
| 4 | 真实客户试点按 A1–A4 另行执行 | 见 `pqc-pilot-intake-checklist` | `data_class: real` + 回执 |

## 4. 与目标的关系

- 本裁定**不改变**目标第二判据：`C_real` 仍需真实客户一单（A1–A4）才能破 0；
- 本裁定补齐了 P13 的“跨项目契约登记”缺口（原 3 条契约 → 4 条）。
