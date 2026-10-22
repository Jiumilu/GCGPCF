---
doc_id: GPCF-DOC-88EC26FE57
title: PKC 状态
project: PKC
related_projects: [PKC]
domain: governance
status: controlled
version: v1.1
owner: PKC
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/pkc/STATUS.md
source_path: projects/pkc/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# PKC 状态

本文件只记录 PKC 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/pkc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project pkc`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- **活跃 Feature：0**。`features/active/` 下 23 个活跃 Feature 无一登记到 PKC（`runtime/queue.json` 无 `project: pkc` 条目）。
- **当前阶段**：`task_pack_ready / local_dev_dryrun_boundary`，`pkc_kds_brain_workflow_dryrun = controlled`（文档声明）。
- **已通过的本地能力**：`npm run lint`、`npm run typecheck`、`npm run test` 三条均 pass；`test_files = 10 passed`、`tests = 57 passed`。
- **阻塞一：真实集成未验证**——同批证据自述 `real_kds_integration_verified = false`、`real_brain_integration_verified = false`；本结论为**本地 dry-run 边界**，PKC 侧未连接真实 KDS/Brain。
- **阻塞二：无 Feature 载体**——PKC 未进入 GPCF 2.0 Feature 队列，无 `gpcf_check_evidence.py` 可回放结果。
- **注**：F-033（xiaoc）把 PKC 列为待联调消费方，属 PoC scope，**不等于** PKC 集成已验证。

## 已知证据

| 证据 | 路径 | 一句话 |
|---|---|---|
| workflow dry-run 证据 | `docs/harness/PKC/evidence/pkc-kds-brain-workflow-dryrun-20260625.md` | lint/typecheck/test 全 pass，`test_files = 10 passed`、`tests = 57 passed`；同时记 `real_kds_integration_verified = false`、`real_brain_integration_verified = false`、`real_personal_data_write = false`、`accepted = false` |
| dry-run 一致性校验脚本 | `tools/kds-sync/validate_pkc_kds_brain_workflow_dryrun.py` | 校验上述证据与总控板/状态矩阵口径一致（本次未复跑） |
| PKC 仓 L4 证据 | `../GlobalCloud PKC/docs/harness/evidence/kds-retrieval-PKC-L4-005.json` | PKC 侧 KDS retrieval L4-005 证据（仅确认文件存在，本轮未复核其内容结论） |
| PKC 证据索引 | `../GlobalCloud PKC/docs/harness/evidence/evidence-index.md` | PKC 仓内证据索引入口 |
| F-033 待联调消费方 | `features/active/F-033-r1-ecosystem-integration/feature.yaml` | 消费方接入任务包列 XiaoG/XGD/PKC/飞书，PoC scope、非正式验收 |

证据分级：上表为**本地 dry-run / mock 边界**，非真实业务运行；证据自述「真实运行 `not_verified_this_round`，未启动 dev server 或浏览器 smoke」。

## 到下一状态门的关键缺口

1. **真实 KDS/Brain 集成未验证**：当前仅本地 dry-run 与 mock，`real_kds_integration_verified = false`，需真实只读接入并形成新证据才能离开 `local_dev_dryrun_boundary`。
2. **无项目级 Feature 与 Evidence Gate 结果**：PKC 缺 `feature.yaml` / `evidence/` / 可回放门禁结果，项目级节奏只能由 dry-run 证据支撑。
3. **运行态未采集**：未启动 dev server、未做浏览器 smoke，真实运行列为 `not_verified_this_round`。
4. **真实个人数据仍受禁**：`real_personal_data_write = false`，一旦涉及真实个人数据必须先取得人工确认。

## 本轮不做与非声明

- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。
- 不声明 PKC 端到端用户闭环完成、不声明真实 KDS 集成完成、不声明真实 Brain 集成完成、不声明真实个人数据写入完成（均为 dry-run 证据的「禁止声明」项）。
- 不替代 PKC 项目实施方案，也不替代任何 Feature 的 `feature.yaml` / `evidence`。
- 本页只记项目级节奏与缺口；上表命令结果来自受控证据，未在本轮复跑。
- 本轮未运行 PKC 命令，未 commit、未 push。

## 2026-10-23 刷新（长期目标 Round 21）

- P4 令牌：新增 `src/styles/gc-tokens.css`（WAE 令牌只读快照）+ theme.css 34 处 `var(--gc-*)`；ui_gate C6 `--gc-*` 0→117。
- P5 状态：`status-badge.tsx` 7 值字典 + S1/S2；已迁移 TasksPage、AgentRunsPage、ProjectPackagePage、BulkFixPage、HomePage；ui_gate C5 未发现→存在。
- 验证：typecheck pass、test 29 files/147 pass、build pass（2026-10-22 记录）。
- 残留：非真实包消费（快照过渡）、部分页面/徽章未迁移、C1/C4/C10 既有项、未视觉差分、真实受控嵌入未联调。
- 不声明 PKC 已接入 WAE / 已验收 / production_ready。

