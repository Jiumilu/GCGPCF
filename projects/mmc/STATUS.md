---
doc_id: GPCF-DOC-0CD635B751
title: MMC 状态
project: MMC
related_projects: [MMC]
domain: governance
status: controlled
version: v1.1
owner: MMC
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/mmc/STATUS.md
source_path: projects/mmc/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# MMC 状态

本文件只记录 MMC 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/mmc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project mmc`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- **活跃 Feature：0**。`features/active/` 下 23 个活跃 Feature 无一登记到 MMC（`runtime/queue.json` 无 `project: mmc` 条目）。
- **两套并存口径（都已记录，本轮未复跑）**：
  - L3 准入矩阵记 MMC **100 分 / `L3 Ready`**（`09-status/globalcloud-l3-admission-matrix.md`，`last_reviewed: 2026-06-12`），其正文自述「该矩阵是 L3 准入评估，不是业务验收结论」「不得因分数达到 L3 Ready 自动升级为 `accepted` 或 `integrated`」。
  - 2026-06-25 治理模板 smoke 记 `task_pack_ready / local_document_smoke_boundary`，且明确 `runtime_verified = false`、`integration_verified = false`。
  - 二者口径不同：前者为 2026-06 中旬的运行态测试结论，后者为 06-25 仅文档入口的 smoke。**当前有效口径以 smoke 的 `runtime_verified = false` 为保守值**。
- **当前阶段**：`task_pack_ready / local_document_smoke_boundary`（文档声明）。
- **阻塞：委派与人工确认契约未落地**。仍以 F-013 的 blocker 形式存在，MMC 侧没有自有 Feature 与授权/回执证据：
  - `mmc_delegation_and_human_confirmation_pending`
  - `mmc_a9_bounded_read_subset_technical_verified_global_policy_not_narrowed`

## 已知证据

| 证据 | 路径 | 一句话 |
|---|---|---|
| 治理模板 smoke 证据 | `docs/harness/MMC/evidence/mmc-governance-template-smoke-20260625.md` | 只验证 MMC 仓、`AGENTS.md`、唯一实施方案存在且受控；`runtime_verified = false`，未跑 runtime pytest / contract test / Gateway health check |
| smoke 校验脚本 | `tools/kds-sync/validate_mmc_governance_template_smoke.py` | 校验上述证据与登记一致，并把 `runtime_verified = true` 等列入**禁止声明**清单 |
| L3 准入矩阵 | `09-status/globalcloud-l3-admission-matrix.md` | MMC 100 / `L3 Ready`；列 `MMC_TEST_MODE=true python3 -m pytest runtime/tests -q` → 30 passed、`bash runtime/scripts/contract_test.sh` → pass（**文档声明，本轮未复跑**） |
| OpenAPI 契约文件 | `../GlobalCloud MMC/llm-wiki-openapi-schema.yaml` | `openapi: 3.0.0`，LLM Wiki API 契约；对应 `contract_test.sh` 在 MMC 证据索引中记为 pass |
| MMC 证据索引 | `../GlobalCloud MMC/docs/harness/evidence/evidence-index.md` | GPCF-MM-LR-007「OpenAPI policy contract」→ `contract_test.sh` → `pass` |
| 运行态测试目录 | `../GlobalCloud MMC/runtime/tests` | 30 passed 结论的测试载体（仅确认目录存在，未复跑） |
| 委派契约 blocker | `features/active/F-013-knowledge-asset-model-system/feature.yaml`（blockers 第 61–62 条） | `mmc_delegation_and_human_confirmation_pending`、`mmc_a9_..._global_policy_not_narrowed` |

证据分级：MMC 现有证据是**文档 smoke + L3 准入评估**，不是业务验收；`runtime_verified = false` 一轮明确未跑运行态。**未执行**真实外部 API 写入、数据库迁移、权限变更或部署。

## 到下一状态门的关键缺口

1. **无项目级 Feature 与 Evidence Gate 结果**：MMC 只有准入矩阵与文档 smoke，没有 GPCF 2.0 的 `feature.yaml` / `evidence/` / `gpcf_check_evidence.py` 可回放证据。
2. **运行态证据需重采收口**：06-25 smoke 记 `runtime_verified = false`，与 06-12 矩阵的「30 passed + contract_test pass」存在口径差，需重跑一次运行态与 OpenAPI 契约测试才能给出当前有效结论。
3. **委派与人工确认契约未落地**：仍挂在 F-013 blockers，MMC 侧无独立授权、人工确认与回执证据。
4. **A9 只读子集仅技术验证**，全局策略未收窄（同 F-013 blocker 第 61 条）。

## 本轮不做与非声明

- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。
- 不声明 MMC runtime 已通过、不声明下游项目已接入 MMC 模板（两条均为 smoke 证据的显式禁止声明项）。
- 不声明 `L3 Ready` 等于业务验收或运行验收。
- 不替代 MMC 项目实施方案，也不替代任何 Feature 的 `feature.yaml` / `evidence`。
- 本轮未运行 MMC 测试或服务，未 commit、未 push。
