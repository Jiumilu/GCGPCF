---
doc_id: GPCF-DOC-EAB78E119A
title: F-034 运行时证据（task_flow_e2e_status / evidence_overexposure_gate，2026-10-25）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: 已补（两项 gate 的运行时证据落盘）
version: v1.0
owner: WAE（受权执行）
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/runtime-evidence-20261025.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/runtime-evidence-20261025.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
created: 2026-10-25
---

# F-034 运行时证据补充

> 背景：`feature.yaml` 的 `ui_product_first_control.gates` 中 `task_flow_e2e_status` / `evidence_overexposure_gate` 早已标 `pass`，但对应**可回放运行时证据**此前未落盘（blockers 记为待补）。本文件补上两项证据与回放方式。

## 一、task_flow_e2e_status

| 项 | 内容 |
|---|---|
| 命令 | `cd "../GlobalCloud WAE" && pnpm e2e:task-flow` |
| 结果 | **8/8 步通过**（登录 → 统一工作台 → PKC 候选页 → 服务控制台 → 回 PKC 候选页 → 全流程 pageerror=0） |
| 证据 | WAE `docs/evidence/F-034/logs/21-e2e-task-flow.log`（退出码 0）+ `.e2e-task-flow-report.md` |
| 实现 | `scripts/e2e-task-flow.mts`（真实 dev + 临时身份目录；不依赖 mock 页面） |
| 判据 | 真实用户任务流可走通、步骤可回放；失败会如实列出分步明细 |

## 二、evidence_overexposure_gate

| 项 | 内容 |
|---|---|
| 命令 | `cd "../GlobalCloud WAE" && pnpm e2e:machine-fields` |
| 结果 | **通过**：5 页（首页/应用壳/服务控制台/PKC 候选页/设置）可见文本 **0 命中** 机器字段模式；**金丝雀自检 6/6 可命中**（证明扫描器没有空转） |
| 证据 | WAE `docs/evidence/F-034/logs/15-e2e-machine-fields.log`（退出码 0）+ `.e2e-machine-fields-report.md` |
| 实现 | `scripts/e2e-no-machine-fields.mts`（`doc_id` / `evidence:` / JSON / 内部 ID / digest 等模式） |

## 三、与 feature.yaml 的对应

- `ui_product_first_control.gates.task_flow_e2e_status: pass` ⇒ 证据见 §一；
- `ui_product_first_control.gates.evidence_overexposure_gate: pass` ⇒ 证据见 §二；
- 本次仅补证据与移除对应 blocker，不改任何状态（F-034 仍 `ready_for_review`）。

## 四、非声明

不声明 UI 全量验收通过；两项以外（多用户可用性、无障碍）仍按各自记录（waived/pass）处理，不在本文件范围。
