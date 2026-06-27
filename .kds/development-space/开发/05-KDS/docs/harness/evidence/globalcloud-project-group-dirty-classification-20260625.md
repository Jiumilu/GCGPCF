---
doc_id: GPCF-DOC-PROJECT-GROUP-DIRTY-CLASSIFICATION-20260625
title: GlobalCloud 项目群 Dirty 变更分类证据 2026-06-25
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dirty-classification-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-dirty-classification-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Dirty 变更分类证据 2026-06-25

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-GIT-DIRTY-CLASSIFY-001` |
| 前置证据 | `docs/harness/evidence/globalcloud-project-group-git-clean-20260625.md` |
| 执行日期 | 2026-06-25 |
| 执行边界 | 只读分类，不 clean、stash、reset、commit、push 或删除文件 |
| 分类结论 | `project_group_dirty_classification = controlled` |
| 状态建议 | `project_group_git_clean = blocked`，等待人工确认提交范围与 sensitive-path 处置 |

## 2. 分类总览

本文件保留 2026-06-25 的历史分类结论；当前 authoritative live baseline 已在 2026-06-28 重放为 7 仓 dirty + `GlobalCloud KDS/.env.production.example` sensitive-path blocked，引用时必须同时结合 `globalcloud-project-group-live-status-snapshot-20260626.md` 与 `globalcloud-project-group-current-state-baseline-refresh-20260626.md`。

| 仓库 | 变更类型 | 归因 | 当前建议 |
|---|---|---|---|
| `WAS世界资产体系` | 未跟踪 `.DS_Store` | 系统噪声 / 非业务变更 | 不纳入业务提交；需要人工确认后清理或加入忽略规则 |
| `GlobalCloud GPC` | 3 个 tracked 文件 | 本轮 GPC evidence/browser 修复 | 可作为 `GPC-EVIDENCE-BROWSER-001` 单独审查包 |
| `GlobalCoud GPCF` | 总控、证据、validator、KDS 镜像与技能门禁变更 | 本轮真实执行治理与文档治理生成物，混有前序 codegraph/KDS 镜像调整 | 需要拆分为 GPCF governance/evidence 包与 KDS mirror 生成物包 |
| `GlobalCloud KDS` | 1 个 tracked 报告文件 | 非本轮主题的资金追踪报告刷新 | 需要业务/数据 owner 确认，不纳入本轮治理提交 |
| `GlobalCloud PVAOS` | 3 个 tracked 文件 | 本轮 PVAOS release gate 修复 | 可作为 `PVAOS-RELEASE-GATE-001` 单独审查包 |
| `GlobalCloud SOP` | 1 个 tracked 索引 + 4 个 untracked 输出文件 | 非本轮主题的武汉城市圈绿色供应链 SOP 方案生成物 | 需要方案 owner 确认，不纳入本轮治理提交 |

## 3. 本轮可归因变更包

### 3.1 GPC evidence/browser 修复包

| 文件 | 归因 |
|---|---|
| `README.md` | 补充 `docs/18` 到 `docs/26` 的 GFIS/GPC 证据入口，修复 `quality:repo` README 索引缺口 |
| `docs/26-gcfis-100-external-evidence-register.md` | 增加 `当前最高可证明状态仍为 96/100` 明文边界，满足 delivery readiness gate |
| `tests/e2e/gcfis-core-flow.spec.js` | 修复标题、指标、工厂质量、工单号、`L4_blocked` 浏览器断言漂移 |

验证结果：

```text
npm run quality:repo = pass
npm run test:e2e = pass, 20 passed
npm run quality:100 = failed_external_evidence_required
npm run quality:ops = failed_runtime_surface_required
```

### 3.2 PVAOS release gate 修复包

| 文件 | 归因 |
|---|---|
| `vitest.config.ts` | 增加 `setupFiles: ['./src/app/tests/setup.ts']`，修复 jsdom/localStorage 测试环境 |
| `package.json` | 将 `dompurify` override 从 `3.4.2` 调整为 `3.4.11` |
| `package-lock.json` | 跟随依赖修复更新 |

验证结果：

```text
npm run release:gate:local = pass
npm run test:e2e = pass, 50 passed, 4 skipped
npm audit --audit-level=moderate --registry=https://registry.npmjs.org = pass, found 0 vulnerabilities
```

### 3.3 GPCF 真实执行治理包

| 类别 | 文件/目录 | 归因 |
|---|---|---|
| Git clean 技能 | `.codex/skills/globalcloud-project-group-git-clean/**` | 新增项目群 17 仓 Git clean 只读门禁技能 |
| 总控与台账 | `09-status/globalcloud-project-group-real-execution-governance-board.md`、`09-status/globalcloud-core-chain-real-evidence-register.md` | 纳入 GPC、PVAOS、Git clean 和 dirty 分类状态 |
| 证据 | `docs/harness/GPC/evidence/gpc-evidence-browser-repair-20260625.md`、`docs/harness/PVAOS/evidence/pvaos-release-gate-repair-20260625.md`、`docs/harness/evidence/globalcloud-project-group-git-clean-20260625.*`、本文 | 本轮真实执行证据 |
| validator | `tools/kds-sync/validate_gpc_evidence_browser_repair.py`、`tools/kds-sync/validate_pvaos_release_gate_repair.py`、`tools/kds-sync/validate_project_group_git_clean_evidence.py`、`tools/kds-sync/validate_project_group_real_execution_governance_board.py` | 本轮门禁和总控强制项 |
| KDS 本地镜像 | `.kds/development-space/**`、`.kds/local-mirror-ledger.jsonl` | `document_control.py` 生成的受控镜像和台账 |

## 4. 非本轮提交候选

### 4.1 WAS 系统噪声

```text
?? .DS_Store
```

分类：`system_noise / not_business_change`。

处理边界：不由本轮自动删除；需要人工确认后清理或加入 `.gitignore`。

### 4.2 KDS 资金追踪报告刷新

文件：

```text
工业绿链/reports/合同资金追踪报告.md
```

变更摘要：

- 从空报告变为 2026-06-25 自动生成资金追踪报告。
- 包含 22 个项目概览、逾期行动项、合同金额缺口、资金节点索引状态和优先级建议。

分类：`external_business_report_update / owner_confirmation_required`。

处理边界：需要业务/数据 owner 确认，不纳入本轮项目群治理提交。

### 4.3 SOP 武汉城市圈方案生成物

文件：

```text
docs/standardization/document-index.md
docs/operations/wuhan-city-circle-green-supply-chain-operating-system.md
output/.DS_Store
output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.md
output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.pdf
```

分类：`scenario_plan_generated_output / owner_confirmation_required`。

处理边界：需要方案 owner 确认；`output/.DS_Store` 属系统噪声，不应进入业务提交。

## 5. 提交前控制建议

| 包 | 建议状态 | 需要人工确认 | 禁止事项 |
|---|---|---|---|
| GPC evidence/browser 修复包 | 可进入 review | 是 | 不声明外部联调、生产确认或客户验收 |
| PVAOS release gate 修复包 | 可进入 review | 是 | 不声明远程 CI、PR、merge、生产发布或客户验收 |
| GPCF 真实执行治理包 | 可进入 review | 是 | 不把 KDS 镜像生成物误当成外部 API 同步 |
| WAS `.DS_Store` | 待清理确认 | 是 | 不自动删除 |
| KDS 资金追踪报告 | 待业务 owner 确认 | 是 | 不混入治理提交 |
| SOP 武汉城市圈方案 | 待方案 owner 确认 | 是 | 不混入治理提交 |

## 6. 当前边界

```text
project_group_dirty_classification = controlled
project_group_git_clean = blocked
historical_project_group_git_clean_20260625 = partial
live_recheck_gate_20260628 = blocked
commit_ready = false
push_ready = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

当前不得声明：

- 不声明项目群 Git 全量 clean；
- 不声明项目群可提交；
- 不声明项目群可推送；
- 不声明项目群可验收；
- 不声明非本轮 KDS/SOP 业务内容已确认；
- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。
