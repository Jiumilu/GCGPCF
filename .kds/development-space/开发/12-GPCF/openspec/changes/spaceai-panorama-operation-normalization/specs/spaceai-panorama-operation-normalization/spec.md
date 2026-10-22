---
doc_id: GPCF-DOC-5FDFC3B2
title: spec
project: GPCF
related_projects: [GPCF, SpaceAI]
domain: openspec
status: in_progress
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-panorama-operation-normalization/specs/spaceai-panorama-operation-normalization/spec.md
source_path: openspec/changes/spaceai-panorama-operation-normalization/specs/spaceai-panorama-operation-normalization/spec.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-panorama-operation-normalization · Spec

## ADDED Requirements

### Requirement: 操作不得假成功

每个用户动作 SHALL 以三种终局之一结束：成功（有可见结果且数据已落）、失败（给出原因且可恢复）、
被门禁拦下（说明缺什么）；数据未落库、回投未确认或 AI 无结果时 SHALL NOT 提示成功。

#### Scenario: 派单缺必填
- **WHEN** 派单确认时缺少必填项
- **THEN** 操作被门禁拦下并说明缺项，不出现「派单成功」

#### Scenario: CWME 回投未确认
- **WHEN** CWME 回投未获确认
- **THEN** 不得提示回投成功；提供重试或取消

### Requirement: Esc 分层单一契约

Esc SHALL 逐层退出（面板 → 卡片配置 → 帮助），每层只处理本层；帮助内容 SHALL 由键位注册表渲染。

#### Scenario: 多层叠加时按 Esc
- **WHEN** 帮助与卡片配置同时打开时按 Esc
- **THEN** 只关闭最上层，再次 Esc 关闭下一层

#### Scenario: 输入框聚焦
- **WHEN** 输入框有焦点时按快捷键
- **THEN** 不劫持输入，仅 Esc 按分层规则处理

### Requirement: 演示态互斥

大屏、巡演、回放、驾驶四种演示态 SHALL 互斥：开启其一 SHALL 自动停止其他，并保持可退出。

#### Scenario: 开启回放
- **WHEN** 巡演进行中开启回放
- **THEN** 巡演自动停止，回放启动，状态提示明确

#### Scenario: 驾驶模式退出
- **WHEN** 驾驶模式开启
- **THEN** 出现常驻退出胶囊，Esc 或胶囊均可退出

### Requirement: 偏好键命名与合并保护

偏好键 SHALL 统一前缀 `gc.pano.*` 并登记；读取时 SHALL 对非法值回落默认并兼容旧键。

#### Scenario: 非法值
- **WHEN** localStorage 中 `gc.pano.*` 的值非法
- **THEN** 回落默认值，界面不崩溃

#### Scenario: 导出脱敏
- **WHEN** 导出偏好或配置
- **THEN** 敏感字段被脱敏，不含凭据

### Requirement: 组件拆分不改变行为

视图拆分 SHALL 先有行为基线测试；拆分前后模板结构与视觉语义 SHALL 保持一致，且组件必须可挂载渲染。

#### Scenario: 拆分后回归
- **WHEN** 完成一次组件/组合式外提
- **THEN** 相关单测与组件测试全绿，e2e 无新增错误

## 未纳入本变更（下一轮）

- B5 剩余四大块（卡片列 / 飞翔 / CWME / 控制器）外提；
- i18n 约 600 行中文硬编码；
- 人工验收项（派单确认/失败保留、CWME 回投 30s 幂等）。
