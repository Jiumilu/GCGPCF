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
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/summary.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-034 证据摘要（WAE 侧，2026-10-22）

> 与 `manifest.json` 一一对应（**18 项：16 pass、2 expected_diff**）。数字全部来自 `logs/` 原始输出。
> **不提升状态**：F-034 仍 `active/plan`；本摘要不是完成报告。

## 一、总账

| 判据组 | 结果 | 数字出处 |
|---|---|---|
| 框架全量单测 | **135 文件 / 1368 例 通过** | `logs/01-test-framework.log` |
| 框架 typecheck | exit 0 | `logs/02-typecheck.log` |
| WAME 全量单测 | **18 文件 / 110 例 通过** | `logs/03-wame-vitest.log` |
| WAME 生产构建 | 成功 | `logs/04-wame-build.log` |
| 双角色收敛 E2E | **6/6 通过** | `logs/05-e2e-dual-role.log` |
| PKC 候选页 dry-run E2E | **5/5 通过** | `logs/06-e2e-pkc-intake.log` |
| 落位/生成/对账/注册表 | 全绿（4 条） | `logs/07–10` |
| O2 跨仓令牌比对 | **expected_diff**（PKC 快照过期） | `logs/11-check-tokens-parity.log` |
| 框架包构建 | 6 包 + 声明 + CSS | `logs/12-build-packages.log` |
| **G8 无障碍/移动端矩阵** | **13 项断言通过** | `logs/13-e2e-a11y.log` |
| **G1 逐页视觉/结构基线** | **18 项断言通过** | `logs/14-e2e-visual.log` |
| **无机器字段暴露扫描** | **5 页 0 命中 + 金丝雀自检** | `logs/15-e2e-machine-fields.log` |
| **PKC 受控嵌入状态机** | **12 项断言通过** | `logs/16-e2e-pkc-states.log` |
| **O2 偏离登记表判定** | **expected_diff**（PKC 快照过期、Brain 待确认） | `logs/17-check-tokens-registry.log` |
| **像素级基线比对** | **4 页 ≤0.02% 差异**（噪声级） | `logs/18-e2e-pixel.log` |

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

## 三之二、M3 批次 0（Studio 例外演练）

| 项 | 状态 |
|---|---|
| 三件套材料（不适配对象/原因/影响范围/替代方案/不扩散承诺） | ✅ `docs/plan/Studio例外演练_三件套_20261022.md` |
| 只读核对 Studio 现状 | ✅ HEAD `6984c4a5`；`AppSidebar.vue:628` 引用 `gcworld.organizations` 但 router 无定义（回归仍在，未起服务复验）；无 `deprecated` 标记 |
| 三方审批（GPCF / WAE / Studio 属主） | ⏳ 待签（未签即不生效） |

## 三之三、UI gate 六件套（受控方案 §2.4/§7 要求）

| 件 | 位置 |
|---|---|
| 六件套全量（Tool route / Context package / Prompt profile / Design options / Selected option / WAME baseline reuse） | `docs/plan/F-034_UI_gate_六件套_20261022.md` |
| 关键门禁 G1/G4/G5/G8/G9 记录 | 同上 §7（G4/G5 组件级证据在 `packages/ui-templates/src/guards.dom.test.tsx`） |
| 待补 | G1 全量视觉回归、G8 无障碍/移动端矩阵 |

## 三之四、G1 逐页视觉/结构基线（2026-10-22）

| 项 | 内容 |
|---|---|
| 脚本 | `pnpm e2e:visual`（4 页 × 2 档：首页 / 应用壳 / 服务控制台 / PKC 候选页；1440×900 + 768×1024） |
| 结果 | **18 项断言全过**：关键区块存在、无横向溢出、pageerror=0；4 页均截图 |
| 基线 | `docs/evidence/F-034/visual/fingerprints.json`（结构指纹：mains/按钮数/色值/landmarks）+ 8 张截图 |
| 复比 | `pnpm e2e:visual --compare …` → 首次自比 0 漂移；**并发改动 `458a2e7`（入口收敛）后检出 6 项漂移**，a11y 复跑 12/12，基线已刷新（`6149f54`） |
| 限制 | 非像素级 diff（像素基线需固定字体/渲染环境）；G1 全量"逐页像素对照"仍为待补 |

## 三之五、ready_for_review 差距评估（2026-10-22）

见 `docs/plan/F-034_ready_for_review_差距评估_20261022.md`：**结论未达**——4 项实质阻塞（R1 O2 跨仓未回执 / R2 M2 真实多插件 / R3 M3 批次 / R4 像素级基线）+ 2 项流程项（R5 GPCF 归档滞后、R6 状态提升须老卢确认）。

## 四、未做 / 非声明

1. 未做：PKC/Brain 仓任何改动；GPCF 归档；M3 Studio 例外与 Brain/PVAOS 批次；视觉回归（他仓环境）；
2. 非声明：不声明 PKC 已接入/已集成/生产就绪/客户验收；不声明 O2 完成；F-034 不提升状态。

## 2026-10-24 O3 进展

- F-035（WAME 侧栏统一）已 closed：app-registry `sidebarContract` 消费、WAME b233438/ea8f321 已 push、E2E 冒烟 pageErrors=0。
- WAE 项目侧三套侧栏仍未归并；O3 仍为部分完成，F-034 不关闭。
