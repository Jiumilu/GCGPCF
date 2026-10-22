---
doc_id: GPCF-DOC-2B1D05FA
title: tasks
project: GPCF
related_projects: [GPCF, SpaceAI]
domain: openspec
status: in_progress
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-panorama-operation-normalization/tasks.md
source_path: openspec/changes/spaceai-panorama-operation-normalization/tasks.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-panorama-operation-normalization · Tasks

> `[x]` = 已交付并本地提交（未 push）；`[ ]` = 未完成（下一轮）。
> 追溯补建：按 2026-10-22 实际提交回填，不新增工作。

## 1. 审计与方案

- [x] 1.1 四域审计（地图工具 M01–M31 / 卡片数据 C01–C39 / 导航对象处置 / CWME）：143 项操作、106 条问题。
- [x] 1.2 操作总索引（`.harness/runs/20261022-panorama-ops/06-ops-index.md`）。
- [x] 1.3 方案 v2.3：N1–N12 规范、B0–B5 批次、20 项决策模型判定、Q1–Q8 授权问答（`docs/全景态势_操作流程规范化与合理化方案_20261022.md`）。

## 2. B0–B4（语义、规范、入口、持久化）

- [x] 2.1 B0 操作契约护栏 6 例（先红后绿）——`6c9cf05`。
- [x] 2.2 B1 六组 P0：假成功 / 反馈通道 / 派单门禁 / CWME 回投门禁 / 驾驶 Esc / AI 结果可见——`25e73d0`。
- [x] 2.3 B2 规范骨架：Esc 分层 / 键位注册表 + ? 帮助 / 键盘作用域 / 演示互斥 / 持续能力胶囊 / 共享组件可选契约——`179a6bb`。
- [x] 2.4 B3 入口收敛 D1–D7 / 死代码与假字段清理 / ⌘K 命令面板 28 条——`4dd4c08`。
- [x] 2.5 B4 偏好键收口 `gc.pano.*` / 审计待补队列 / 导出脱敏 / 卡片可访问性——`8a88934`。
- [x] 2.6 B4b 偏好合并冲突保护 + 22 键登记表——`85784a3`。
- [x] 2.7 合并回 main（--no-ff，冲突仅 import 1 处）——`73b6f5c`。

## 3. B5 外提

- [x] 3.1 B5a 组件切片（PanoramaHelp / PanoramaPalette）+ i18n 工具栏/aria/术语——`54fc1c3`。
- [x] 3.2 B5b useFeedback / useCardConfig 外提——`b98c2be`。
- [x] 3.3 B5c useCameraModes（3 例）——`ea0b5ea`。
- [x] 3.4 B5d useCardOrder（4 例）——`b438c24`。
- [x] 3.5 B5e useDemoModes（2 例）——`39a55e6`。
- [x] 3.6 B5f PanoramaBubbles + bubbleState（9 例），组件 3955 → 3711 行——`441f55c`。

## 4. 验证

- [x] 4.1 本变更相关 35 例单测；全仓 136 文件 / 1251 例；typecheck 0。
- [x] 4.2 e2e `panorama-operate.spec.ts` 5/5（真实 Chrome，2026-10-22 18:35）。
- [x] 4.3 证据归档 `.harness/runs/20261022-panorama-ops/01–21`。

## 5. 未完成（下一轮）

- [ ] 5.1 B5 剩余四大块外提：卡片列、飞翔、CWME、控制器（script 目标 <800 行未达）。
- [ ] 5.2 i18n：约 600 行中文硬编码迁 `T()`。
- [ ] 5.3 人工验收：派单确认/失败保留、CWME 回投确认/30s 幂等（需真实气泡与面板状态）。
- [ ] 5.4 推送：0 推送（本地领先 34 提交，需授权）。
