---
doc_id: GPCF-DOC-58DD3BDFFC
title: P08 / P09 属主执行包（31–60 天：统一壳 + 首条接入）
project: GPCF
related_projects: [GPC, WAME, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p08-p09-owner-execution-packets-20261022.md
source_path: docs/reports/p08-p09-owner-execution-packets-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P08 / P09 属主执行包（31–60 天：统一壳 + 首条接入）

- 日期：2026-10-22｜依据：Q3 裁定（WAE 落仓方案为真源、PKC 首接入）
- 边界：跨项目仓改动由属主执行；GPCF 只出动作与判据（群级纪律⑤）
- 现状：F-035 / F-036 证据六类均 pass/waived，但因**真实集成未完成**不能关单（close_candidate=false 的唯一原因是 governance blockers）

## 1. F-035（WAME 三套侧栏归并）— 属主：WAME

| # | 动作 | 判据 |
|---|---|---|
| 1 | 在 `wame/architecture-contracts` 分支正式应用 app-registry 依赖（`app-registry` sidebarContract 纯类型，13.1KB 已重打包） | `pnpm install --ignore-scripts` exit 0；`tsc --noEmit` exit 0 |
| 2 | `layout/GlobalCloudSidebar` 改为消费 app-registry 契约；`components/Sidebar` 变兼容 re-export（无第二套实现） | `grep -rln "components/Sidebar" src` 仅剩 re-export；DOM 测试守护默认 4 项标签/路径/激活判定 |
| 3 | 补 task-flow E2E + 多用户/无障碍实测（现 screenshots/a11y waived、task_flow_e2e pending） | `ui_product_first_control` 六门中 task_flow_e2e 由 pending → pass |
| 4 | 生产消费路径（私有 registry）作为独立事项立项 | 未立项前不得声明"生产已消费" |

**GPCF 侧验收**：`python3 scripts/gpcf_check_evidence.py F-035 --check-only` 的 blockers 前缀消失后再走解除流程。

## 2. F-036（PKC 首接入 WAE）— 属主：WAE（不改 PKC 仓）

| # | 动作 | 判据 |
|---|---|---|
| 1 | 配置 `VITE_PKC_EMBED_URL`（受控嵌入地址，映射到 PKC 运行态） | 嵌入页加载成功且 `ui_gate C10 有效=0`（默认不发起请求） |
| 2 | 正式接入评审（现 `review_status=conditional`） | 评审记录落 `docs/assembly-spec/` 或 F-036 evidence；评审人签认 |
| 3 | 菜单按角色收敛实测（system-admin/operator/strategist/studio 可见；viewer/auditor 不可见） | 单测 + 双角色 DOM 用例 pass |
| 4 | 登记清单 `manifests/pkc-intake.yaml` 的来源/适配 L2/回滚/非声明补全 | 文件字段齐全 |

**GPCF 侧验收**：同上，`gpcf_check_evidence.py F-036 --check-only`；在正式评审通过前**不得**声明"PKC 已接入"。

## 3. 两包共同的非声明边界

- 不得声明 accepted / integrated / production_ready / customer_accepted；
- PKC 个人数据写入保持关闭（`real_personal_data_write=false`）；
- 令牌一律 mock，禁读生产凭据。
