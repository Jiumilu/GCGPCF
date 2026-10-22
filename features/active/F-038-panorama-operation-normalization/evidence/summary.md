---
doc_id: GPCF-DOC-790BC588
title: F-038 panorama-operation-normalization 证据摘要
project: spaceai
related_projects: [SpaceAI, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-038-panorama-operation-normalization/evidence/summary.md
source_path: features/active/F-038-panorama-operation-normalization/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: waived
- api: pass
- acceptance_declared: false
- risk: 本轮为部分完成（B0–B5e）；B5 剩余五大块、i18n 与人工验收未完成，不得据此宣告验收。
<!-- GPCF_EVIDENCE_GATE_END -->

## 交付摘要（2026-10-22，partial）

全景态势操作流程规范化执行到 B5e，12 个本地提交，方案与 21 份证据归档。

| 项 | 结果 |
|---|---|
| 审计 | 4 份（地图工具 M01–M31 / 卡片数据 C01–C39 / 导航对象处置 OP / CWME）共 143 项操作、106 条问题；索引 `06-ops-index.md` |
| 方案 | `docs/全景态势_操作流程规范化与合理化方案_20261022.md` v2.3：N1–N12 规范 + B0–B5 批次 + 20 项决策模型判定 + Q1–Q8 授权问答 |
| B0 | 操作契约护栏 6 例（先红后绿，防「假成功」回归） |
| B1 | 六组 P0：假成功 / 反馈通道 / 派单门禁 / CWME 回投门禁 / 驾驶 Esc / AI 结果可见 |
| B2 | Esc 分层单一契约、键位注册表 + ? 帮助、键盘作用域、演示态互斥、持续能力胶囊、共享组件可选契约 |
| B3 | 入口收敛 D1–D7、死代码与假字段清理、⌘K 命令面板（28 条） |
| B4 | 偏好键收口 `gc.pano.*` + 22 键登记表、审计待补队列、导出脱敏、卡片可访问性 |
| B5a–B5e | help/palette 组件切片；useFeedback / useCardConfig / useCameraModes / useCardOrder / useDemoModes 外提（11 个 use* 组合式） |
| 测试 | 本 Feature 26 例；全仓 135 文件 / 1242 例；typecheck 0 |
| e2e | `panorama-operate.spec.ts` 5/5（真实 Chrome） |
| 接口 | `/healthz` 200（263 端点） |

## 未完成边界（如实记录）

1. **B5 剩余五大块**：卡片列、气泡、飞翔、CWME、控制器仍在 `PanoramaDeep.vue` 内；组件 3955 行
   （含并行 L4 新增约 230 行、本轮外提约 460 行逻辑），script 目标 <800 行未达。
2. **i18n**：约 600 行中文硬编码未迁（仅工具栏与卡片标题走 `T()`）。
3. **人工验收**：派单确认/失败保留、CWME 回投确认/30s 幂等未被自动 e2e 覆盖。
4. **收口事故**：工作目录改名（`GlobalCloud SpaceAI` → `GlobalCloud SpaceAI Platform`）导致原会话第 15/16 轮启动失败，收口在新路径会话补齐；产品代码未受影响。
5. 状态保持 partial / 待验收；未 push、未部署。
