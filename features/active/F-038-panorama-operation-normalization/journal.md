---
doc_id: GPCF-DOC-316BCCD3
title: F-038 panorama-operation-normalization
project: GPCF
related_projects: [SpaceAI, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-038-panorama-operation-normalization/journal.md
source_path: features/active/F-038-panorama-operation-normalization/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-038 panorama-operation-normalization

## 账实说明（2026-10-22 补建）

- 本 Feature 为**治理账实补齐时追溯建立**：全景态势操作流程规范化 2026-10-22 已执行到 B5e 并本地提交 12 个提交，
  原会话（`session-e35aea3e…`）按老卢选择「部分完成，收口本轮」收口，但当时没有 GPCF Feature 记账。
- 本次补建只做**记账与证据归位**，不改产品代码、不重跑改造、不提升任何验收状态。
- B5 剩余五大块、i18n、人工验收明确留在下一轮，Feature 保持 active。

## LOOP 日志

### Iteration 0（追溯建账）

1. 这轮做什么？
   - 追溯建立 Feature Workspace，把已收官的全景态势操作规范化工作纳入中央账。
2. 改了什么？
   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。
3. 怎么验证？
   - 关闭前运行 gpcf_check_evidence.py。
4. 发现什么问题？
   - 账实缺口：工作已提交、方案已成文，但无 Feature 记录；且收口时工作目录改名导致旧会话多轮启动失败（见收口记录 §五）。
5. 是否可以提交？
   - 否，Evidence Gate 待 Iteration 1 补齐。

### Iteration 1（2026-10-22 证据归位）

1. 这轮做什么？
   - 把 12 个已提交的全景态势操作规范化提交对应到本 Feature，补齐证据并复测当前 HEAD。
2. 改了什么？
   - 提交链（主项目 `../GlobalCloud SpaceAI Platform`，均本地提交未 push）：
     - `6c9cf05` test(pano): B0 操作契约护栏（6 例，红-绿验证）
     - `25e73d0` feat(pano): B1 六组 P0 修复——假成功 / 反馈通道 / 派单门禁 / CWME 回投门禁 / 驾驶 Esc / AI 结果可见
     - `73b6f5c` merge: 全景态势 B0 护栏 + B1 六组 P0 + B2 规范骨架（pano-ops/b0b1，--no-ff）
     - `179a6bb` feat(pano): B2 规范骨架（Esc 分层 / 演示互斥 / 持续能力胶囊 / 键位帮助 / 共享组件可选契约）
     - `4dd4c08` feat(pano): B3 入口收敛 / 死代码清理 / ⌘K 命令面板
     - `8a88934` feat(pano): B4 持久化收口 / 审计待补 / 导出脱敏 / 可访问性
     - `85784a3` feat(pano): B4b 偏好合并冲突保护 + 偏好键登记表
     - `54fc1c3` feat(pano): B5a 组件切片 + B3b/B4b 清理（i18n/aria/术语/恢复默认）
     - `b98c2be` feat(pano): B5b 组合式外提（反馈/审计、卡片配置）+ i18n 菜单批次
     - `ea0b5ea` feat(pano): B5c 相机接管模式外提（useCameraModes）
     - `b438c24` feat(pano): B5d 卡片顺序/拖拽外提（useCardOrder）
     - `39a55e6` feat(pano): B5e 演示态外提（useDemoModes）
   - 证据目录：`.harness/runs/20261022-panorama-ops/`（01–04 审计、06 索引、07 文档复核、08–15 批次执行、16–20 B5 验收、21 收口）。
   - 方案：`docs/全景态势_操作流程规范化与合理化方案_20261022.md`（v2.3，含 N1–N12 与 20 项决策模型判定）。
3. 怎么验证？
   - 相关测试 26 例通过：panorama-operate 14 / camera-modes 3 / card-order 4 / audit-privacy 3 / demo-modes 2。
   - 全仓：`npx vitest run` → 135 文件 / 1242 例通过（2026-10-22 19:04）；`pnpm typecheck` → 0。
   - e2e：`e2e/panorama-operate.spec.ts` 5/5 通过（2026-10-22 18:35，真实 Chrome，见 16-acceptance-b5a.md）。
   - 接口：`/healthz` 200（263 端点，SIMULATED 39 表）。
4. 发现什么问题？
   - **B5 剩余五大块**（卡片列 / 气泡 / 飞翔 / CWME / 控制器）仍在 `PanoramaDeep.vue` 内；组件 3955 行（含并行 L4 新增约 230 行），script 目标 <800 行未达。
   - **i18n 欠账**：约 600 行中文硬编码，仅工具栏与卡片标题走 `T()`。
   - **人工验收缺口**：派单确认/失败保留、CWME 回投确认/30s 幂等未被自动 e2e 覆盖。
   - 收口期间工作目录改名（`GlobalCloud SpaceAI` → `GlobalCloud SpaceAI Platform`）导致旧会话第 15/16 轮启动失败；收口动作在新路径会话补齐。
5. 是否可以提交？
   - 证据齐备可提交（治理产物独立提交）；Feature 保持 active，状态 partial / 待验收，不提升。
