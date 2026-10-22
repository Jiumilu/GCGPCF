---
doc_id: GPCF-DOC-0B5EA78915
title: F-034 证据摘要（WAE 侧，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/summary.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/summary-active-residue-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-034 证据摘要（WAE 侧，2026-10-22）

> **历史残留（2026-10-22）**：本文件是回滚前生成的摘要；**以同目录 `summary.md` 为准**（现行摘要）。


> 与 `manifest.json` 一一对应（12 项：11 pass、1 expected_diff）。数字全部来自 `logs/` 原始输出。
> **不提升状态**：F-034 仍 `active/plan`；本摘要不是完成报告。

## 一、总账

| 判据组 | 结果 | 数字出处 |
|---|---|---|
| 框架全量单测 | **129 文件 / 1353 例 通过** | `logs/01-test-framework.log` |
| 框架 typecheck | exit 0 | `logs/02-typecheck.log` |
| WAME 全量单测 | **17 文件 / 106 例 通过** | `logs/03-wame-vitest.log` |
| WAME 生产构建 | 成功 | `logs/04-wame-build.log` |
| 双角色收敛 E2E | **6/6 通过** | `logs/05-e2e-dual-role.log` |
| PKC 候选页 dry-run E2E | **5/5 通过** | `logs/06-e2e-pkc-intake.log` |
| 落位/生成/对账/注册表 | 全绿（4 条） | `logs/07–10` |
| O2 跨仓令牌比对 | **expected_diff**（PKC 快照过期） | `logs/11-check-tokens-parity.log` |
| 框架包构建 | 6 包 + 声明 + CSS | `logs/12-build-packages.log` |

## 二、M1 判据逐项对账（受控方案 v1.1）

| 任务包 | v1.1 判据 | 证据 | 判定 |
|---|---|---|---|
| **O1**（v1.1 改述） | 产品壳内壳能力可关可回退；默认零变化 | `screens/m2-plugin-on-20261022.png`、`screens/m2-plugin-off-20261022.png`；单测 4+4；WAME 106 例 | **pass** |
| **O2** 令牌收口 | TOKEN_NAMES≡tokens.css、default_theme 零声明 | `logs/01` 内 tokens 用例；比对脚本 P1–P3 | **partial**（仓内 pass；跨仓 PKC 快照过期、Brain 偏离待属主裁定） |
| **O3** 侧栏统一 | 唯一侧栏、无同屏双栏 | 死代码已归档（`_superseded/`）；`WameSidebarPlugin` 注册表 + `hasSidebarPlugin()` 装配点；单测 4 例 | **pass（WAME 首例）** |
| **O4** 状态语义层 | 7 值 / S1 / S2 / S3 | 字典 14 + 状态件 5 + **G4/G5 守卫 5** | **pass** |
| 角色收敛 | viewer 不见受限入口、接口 403 一致 | `screens/dual-role-{admin,viewer}-20261022.png`；E2E 6/6 | **pass** |

## 三、跨仓（不在 WAE 仓内，WAE 只取证）

| 项 | 现状 |
|---|---|
| PKC 令牌快照 | **过期**（WAE `c02954c9…` vs PKC `9b7dd014…`，缺 12 个新令牌、值 0 差异）→ PKC 属主重新快照 |
| Brain 令牌 | **5 独有令牌** + **28 个令牌字面值差异**（自有深色+紫主题）→ Brain 属主 + 老卢裁定 |
| PKC 侧 B 表 7 项 | 待 PKC 属主（origin/身份模式/全量测试/视觉回归/偏离裁定/状态词） |
| GPCF 官方归档 | **待授权**（跨仓写入）：本包作待复制源 |

## 四、未做 / 非声明

1. 未做：PKC/Brain 仓任何改动；GPCF 归档；M3 Studio 例外与 Brain/PVAOS 批次；视觉回归（他仓环境）；
2. 非声明：不声明 PKC 已接入/已集成/生产就绪/客户验收；不声明 O2 完成；F-034 不提升状态。
