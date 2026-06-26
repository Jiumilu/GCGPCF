---
doc_id: GPCF-DOC-PROJECT-GROUP-REVIEW-PACKAGES-20260625
title: GlobalCloud 项目群提交前 Review 分组证据 2026-06-25
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-review-packages-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-review-packages-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群提交前 Review 分组证据 2026-06-25

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-REVIEW-PACKAGE-001` |
| 前置证据 | `docs/harness/evidence/globalcloud-project-group-dirty-classification-20260625.md` |
| 执行日期 | 2026-06-25 |
| 执行边界 | 只做 review 分组，不 stage、commit、push、stash、reset、clean 或删除文件 |
| 分组结论 | `project_group_review_packages = controlled` |
| 状态建议 | `commit_ready = false`、`push_ready = false`，等待人工确认各包范围 |

## 2. Review 包总览

| 包 ID | 范围 | 当前建议 | 人工确认 |
|---|---|---|---|
| `PKG-GPC-EVIDENCE-BROWSER-20260625` | `GlobalCloud GPC` 的 README、`docs/26`、E2E 断言修复 | 可进入 review | 需要 |
| `PKG-PVAOS-RELEASE-GATE-20260625` | `GlobalCloud PVAOS` 的 Vitest setup、`dompurify` override、lockfile | 可进入 review | 需要 |
| `PKG-GPCF-GOVERNANCE-EVIDENCE-20260625` | GPCF 总控板、核心台账、证据、validator、Git clean skill | 可进入 review | 需要 |
| `PKG-GPCF-KDS-MIRROR-20260625` | `.kds/development-space/**`、`.kds/local-mirror-ledger.jsonl`、自动索引 README | 只可随治理包审查，不代表真实 KDS API 同步 | 需要 |
| `HOLD-WAS-SYSTEM-NOISE-20260625` | `WAS世界资产体系/.DS_Store` | hold，等待清理/忽略规则确认 | 需要 |
| `HOLD-KDS-FUNDING-REPORT-20260625` | KDS 资金追踪报告刷新及其镜像索引影响 | hold，等待业务/数据 owner 确认 | 需要 |
| `HOLD-SOP-WUHAN-SCENARIO-20260625` | SOP 武汉城市圈绿色供应链方案与输出文件 | hold，等待方案 owner 确认 | 需要 |

## 3. 可 Review 包

### 3.1 `PKG-GPC-EVIDENCE-BROWSER-20260625`

仓库：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC`

文件：

```text
README.md
docs/26-gcfis-100-external-evidence-register.md
tests/e2e/gcfis-core-flow.spec.js
```

证据：

```text
docs/harness/GPC/evidence/gpc-evidence-browser-repair-20260625.md
tools/kds-sync/validate_gpc_evidence_browser_repair.py
npm run quality:repo = pass
npm run test:e2e = pass, 20 passed
```

边界：

```text
npm run quality:100 = failed_external_evidence_required
npm run quality:ops = failed_runtime_surface_required
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

### 3.2 `PKG-PVAOS-RELEASE-GATE-20260625`

仓库：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS`

文件：

```text
vitest.config.ts
package.json
package-lock.json
```

证据：

```text
docs/harness/PVAOS/evidence/pvaos-release-gate-repair-20260625.md
tools/kds-sync/validate_pvaos_release_gate_repair.py
npm run release:gate:local = pass
npm run test:e2e = pass, 50 passed, 4 skipped
npm audit --audit-level=moderate --registry=https://registry.npmjs.org = pass, found 0 vulnerabilities
```

边界：

```text
remote_ci = not_verified
pr_created = false
merged = false
production_release = false
customer_accepted = false
```

### 3.3 `PKG-GPCF-GOVERNANCE-EVIDENCE-20260625`

仓库：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF`

范围：

```text
.codex/skills/globalcloud-project-group-git-clean/**
09-status/globalcloud-project-group-real-execution-governance-board.md
09-status/globalcloud-core-chain-real-evidence-register.md
docs/harness/GPC/evidence/gpc-evidence-browser-repair-20260625.md
docs/harness/PVAOS/evidence/pvaos-release-gate-repair-20260625.md
docs/harness/evidence/globalcloud-project-group-git-clean-20260625.*
docs/harness/evidence/globalcloud-project-group-dirty-classification-20260625.md
docs/harness/evidence/globalcloud-project-group-review-packages-20260625.md
tools/kds-sync/validate_gpc_evidence_browser_repair.py
tools/kds-sync/validate_pvaos_release_gate_repair.py
tools/kds-sync/validate_project_group_git_clean_evidence.py
tools/kds-sync/validate_project_group_dirty_classification.py
tools/kds-sync/validate_project_group_review_packages.py
tools/kds-sync/validate_project_group_real_execution_governance_board.py
```

证据：

```text
validate_project_group_git_clean_evidence.py = pass
validate_project_group_dirty_classification.py = pass
validate_project_group_real_execution_governance_board.py = pass
validate_core_chain_real_evidence_register.py = pass
validate_core_chain_runtime_claims.py = pass
loop_document_gate.py = pass
```

边界：

```text
project_group_git_clean = partial
commit_ready = false
push_ready = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

### 3.4 `PKG-GPCF-KDS-MIRROR-20260625`

范围：

```text
.kds/development-space/**
.kds/local-mirror-ledger.jsonl
docs/**/README.md auto index changes
09-status/globalcloud-document-control-register.md
09-status/kds-development-space-sync-register.md
09-status/globalcloud-document-health-report.md
```

说明：

- 该包是 `document_control.py` 的本地镜像和文档台账输出。
- 只能证明本地 KDS 开发空间镜像已更新。
- 不能证明真实 KDS API 已同步。
- 不能替代业务 owner 对 KDS/SOP 内容的确认。

## 4. Hold 包

### 4.1 `HOLD-WAS-SYSTEM-NOISE-20260625`

```text
WAS世界资产体系/.DS_Store
```

处理建议：等待人工确认后删除或加入忽略规则。本轮不自动删除。

### 4.2 `HOLD-KDS-FUNDING-REPORT-20260625`

```text
GlobalCloud KDS/工业绿链/reports/合同资金追踪报告.md
```

处理建议：等待业务/数据 owner 确认报告来源、金额口径、逾期判断和是否纳入 KDS 正式提交。本轮不混入治理包。

### 4.3 `HOLD-SOP-WUHAN-SCENARIO-20260625`

```text
GlobalCloud SOP/docs/standardization/document-index.md
GlobalCloud SOP/docs/operations/wuhan-city-circle-green-supply-chain-operating-system.md
GlobalCloud SOP/output/.DS_Store
GlobalCloud SOP/output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.md
GlobalCloud SOP/output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.pdf
```

处理建议：等待方案 owner 确认后单独 review；`output/.DS_Store` 不应进入业务提交。

## 5. 提交前门禁

任一 review 包进入提交前，必须满足：

| 门禁 | 要求 |
|---|---|
| Git status | 只包含该包文件，或明确说明其它文件 hold |
| Sensitive path | 无 token、secret、证书、私钥、生产 `.env` |
| diff check | `git diff --check -- .` 通过 |
| Evidence | 有对应 evidence 和 validator |
| Boundary | 禁止声明 accepted/integrated/production/customer accepted |
| Human confirmation | 用户确认包范围后才允许 stage/commit/push |

## 6. 当前结论

```text
project_group_review_packages = controlled
review_package_count = 7
review_ready_packages = 4
hold_packages = 3
commit_ready = false
push_ready = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

当前不得声明：

- 不声明项目群可提交；
- 不声明项目群可推送；
- 不声明项目群可验收；
- 不声明真实 KDS API 已同步；
- 不声明 KDS/SOP hold 包业务内容已确认；
- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。
