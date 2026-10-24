---
doc_id: GPCF-DOC-DONE-FEATURE-AUDIT-20261022
title: 项目群历史 done Feature 证据审计（2026-10-22）
project: GPCF
related_projects: [GPCF]
domain: status
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-done-feature-audit-20261022.md
source_path: 09-status/globalcloud-done-feature-audit-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 项目群历史 done Feature 证据审计（2026-10-22）

> 任务：PG-08（关闭规则冻结的配套审计）。口径：`GCPF-EVIDENCE-RULE-1.0`。
> 非声明：本审计不重开、不关闭任何 Feature，不提升任何项目状态。

## 1. 结果总览

```text
done_feature_count = 22
pass_count = 18
exception_count = 4
fail_count = 0
audit_rule_version = GCPF-EVIDENCE-RULE-1.0
auto_close = false
updated_at = 2026-10-24T11:45:00+08:00
update_basis = 老卢 2026-10-22 21:24 裁定「P17 现在做：能补的补验，不能补的登受控例外」
```

## 2. 逐项结果

| # | Feature | close_candidate | 失败原因（摘要） | 建议处置 |
|---:|---|---|---|---|
| 1 | `F-001-supplier-onboarding` | false | acceptance 空；scope.in 空；tests/build 未声明 | 补 acceptance/scope 或历史例外 |
| 2 | `F-002-project-group-feature-queue` | false | tests/build 未声明；screenshots/api waiver 无专属理由 | 低成本的补验：补命令+理由 |
| 3 | `F-003-evidence-gate-profile` | false | tests/build 未声明；screenshots/api waiver 无专属理由 | 低成本的补验 |
| 4 | `F-006-knowledge-e2e-flow` | false | acceptance 空；scope.in 空；tests/build 未声明 | 补 acceptance/scope 或历史例外 |
| 5 | `F-007-reports-data-flow` | false | acceptance 空；scope.in 空；tests/build 未声明 | 补 acceptance/scope 或历史例外 |
| 6 | `F-008-icp-project-group-admission` | false | acceptance 要求本 Feature 保持 active；tests/build 未声明；waiver 无理由 | 历史例外（保留 active 语义） |
| 7 | `F-009-project-group-openspec-coverage` | false | tests/build 未声明；screenshots/api waiver 无专属理由 | 低成本的补验 |
| 8 | `F-018-gpcf-governance-console` | false | tests/build 未声明；api waiver 无专属理由 | 低成本的补验 |
| 9 | `F-020-aaas-service-console` | false | tests/build 未声明；api waiver 无专属理由 | 低成本的补验 |
| 10 | `F-028-plane-gpcf-feature-evidence-integration` | **true** | 无 | 保持 done |

## 3. 处置建议

| 处置 | Feature | 理由 |
|---|---|---|
| 补验（低成本） | F-002、F-003、F-009、F-018、F-020 | 只缺专属命令与 waiver 理由，补采后可重新判定 |
| 补 acceptance/scope | F-001、F-006、F-007 | 缺验收定义，需 owner 补语义 |
| 历史例外 | F-008 | 其 acceptance 要求保持 active，与"关闭"语义冲突 |
| 保持 | F-028 | 当前规则下 pass |

> 补验与例外均需逐项登记；不得批量改写历史 done 记录，不得自动重新关闭。

## 2.1 P17 复跑结果（2026-10-22 21:30，分母 10→16）

| # | Feature | close_candidate | 处置 |
|---:|---|---|---|
| 1 | `F-001-supplier-onboarding` | false | **受控例外** EXC-DONE-F-001（acceptance/scope.in 历史缺失） |
| 2 | `F-002-project-group-feature-queue` | **true** | 补验通过（补 tests/build 声明 + waiver 理由） |
| 3 | `F-003-evidence-gate-profile` | **true** | 补验通过 |
| 4 | `F-006-knowledge-e2e-flow` | false | **受控例外** EXC-DONE-F-006 |
| 5 | `F-007-reports-data-flow` | false | **受控例外** EXC-DONE-F-007 |
| 6 | `F-008-icp-project-group-admission` | false | **受控例外** EXC-DONE-F-008（acceptance 要求保持 active） |
| 7 | `F-009-project-group-openspec-coverage` | **true** | 补验通过 |
| 8 | `F-018-gpcf-governance-console` | **true** | 补验通过 |
| 9 | `F-020-aaas-service-console` | **true** | 补验通过 |
| 10 | `F-028-plane-gpcf-feature-evidence-integration` | true | 保持 |
| 11 | `F-010-project-group-ui-engineering-coverage` | true | 保持 |
| 12 | `F-011-studio-workbench-ui-runtime-closure` | true | 保持 |
| 13 | `F-015-gcworld-organization-readonly-vertical-slice` | true | 2026-10-22 随 Studio 退役结项 |
| 14 | `F-019-icp-industry-console` | true | 保持 |
| 15 | `F-031-xgd-dot-alignment` | true | 2026-10-22 P0 六项人工验收通过后关单 |
| 16 | `F-034-wae-p0-shell-and-role-convergence` | true | 保持 |

> 受控例外登记于 `runtime/exceptions.yaml`（approved_by=laolu，until=2027-01-20，到期转 warn，不得自动续期）。
> 补验只补"命令与豁免理由"声明，未改写任何历史证据本体。

## 2.2 P17 复检（2026-10-24 11:45，分母 22）

| 结果 | 数量 | Feature |
|---|---:|---|
| close_candidate=true | **18** | F-002/003/004/009/010/011/015/018/019/020/021/024/026/027/028/030/031/**035** |
| 受控例外（不变） | **4** | F-001 / F-006 / F-007 / F-008（`runtime/exceptions.yaml`，until 2027-01-20） |
| 合计 | **22** | 与 `features/done` 实际数量一致 |

复跑命令与判据：`for f in $(ls features/done | grep -oE '^F-[0-9]+'); do python3 scripts/gpcf_check_evidence.py $f --check-only; done`
—— 18 项 `close_candidate=true`，4 项仍 false 且全部落在已登记的受控例外内（无未登记例外项）。

## 4. 复跑命令

```bash
for d in features/done/*/; do
  fid=$(basename "$d")
  python3 scripts/gpcf_check_evidence.py --check-only "$fid"
done
```

## 5. 非声明

- 不声明 9 个 fail 的 Feature 已修复；
- 不声明任何 Feature 已重新关闭；
- 不声明任何项目状态提升。
