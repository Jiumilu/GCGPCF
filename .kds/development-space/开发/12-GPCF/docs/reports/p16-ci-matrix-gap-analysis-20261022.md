---
doc_id: GPCF-DOC-5D1F7E0305
title: P16 · 跨项目 CI/验收矩阵 · 现状盘点与分阶段建议（2026-10-22）
project: GPCF
related_projects: [GPC, WAME, PKC, XiaoC, XiaoG, MMC, GPCF, Studio, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p16-ci-matrix-gap-analysis-20261022.md
source_path: docs/reports/p16-ci-matrix-gap-analysis-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P16 · 跨项目 CI/验收矩阵 · 现状盘点与分阶段建议（2026-10-22）

- 草案产物：`runtime/plan-20261022/ci-matrix-draft.yaml`（29 仓 × 六类 job，**未接门禁**）
- 纪律：接入门禁属治理变更，需 `gate(redline)` + 老卢授权；本文件只做盘点与建议

## 1. 实测覆盖（29 仓）

| job 类 | 已具备 | 缺失 | 说明 |
|---|---:|---:|---|
| standards | **29** | 0 | 项目群规范化已覆盖全仓 |
| test | 6 | **23** | 仅 XiaoC/MMC/XiaoG/SpaceAI Studio/PMC/PDC 有测试 job |
| build | 6 | **23** | 同上量级 |
| e2e | 2 | **27** | 仅 XiaoG/SLC |
| browser | 0 | **29** | 全缺 |
| a11y | 0 | **29** | 全缺 |

> 数据来源：各仓 `.github/workflows/*` 的 job 名关键词扫描（`runtime/plan-20261022/ci-matrix-draft.yaml` 含逐仓明细）。

## 2. 结论

**"统一验收门禁"当前不可直接全量接入**：若要求六类 job 全部存在，29 仓中 27+ 会在第一天就失败。P16 必须分阶段，否则会重演"门禁全红、无人可信"的老问题。

## 3. 建议的三阶段（每阶段有独立验收口径）

| 阶段 | 范围 | 验收口径 | 依赖 |
|---|---|---|---|
| **P16-1（可立即）** | 只把 `standards` 作为强制 job（29/29 已具备） | `gc_standard.py check --fail-on error` 在每仓 CI 中为 required | 无需新授权（已具备） |
| **P16-2（属主执行）** | `test`/`build` 逐仓补齐 | `ci-matrix.yaml` 中该仓 `test/build` 由 missing→present，且至少 1 次绿构建 | 各仓属主；GPCF 只出清单 |
| **P16-3（UI 仓专项）** | `e2e/browser/a11y` 仅对 UI 仓（WAE、PKC(经 WAE)、PDC、Studio、GPC、PQC） | 浏览器与无障碍基线取 WAE AppsShell；每仓 1 条用户任务 E2E | 需 WAE 属主先稳定壳 |

## 4. 建议的矩阵文件形态（待授权后落 `_governance/ci-matrix.yaml`）

```yaml
schema_version: "1.0"
repos:
  - {repo: "GlobalCloud GPCF", required_jobs: [standards], optional_jobs: [test]}
  - {repo: "GlobalCloud WAE", required_jobs: [standards, build, browser, a11y], optional_jobs: [test, e2e]}
  # …29 仓逐一登记；required_jobs 缺失即门禁失败
```

## 5. 需要老卢裁定（问答提交）

1. 是否先只落 **P16-1（standards 强制）**，test/build 交属主补齐（推荐）；
2. `e2e/browser/a11y` 的 UI 仓名单是否按 §3 的 6 个仓；
3. 矩阵文件放 `_governance/ci-matrix.yaml`（全群门禁组件）是否授权我落盘。
