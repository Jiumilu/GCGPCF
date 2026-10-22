---
doc_id: GPCF-DOC-58D9EB15
title: spec
project: GPCF
related_projects: [GPCF, SpaceAI]
domain: openspec
status: implemented
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-l4-precision-model/specs/spaceai-l4-precision-model/spec.md
source_path: openspec/changes/spaceai-l4-precision-model/specs/spaceai-l4-precision-model/spec.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-l4-precision-model · Spec

## ADDED Requirements

### Requirement: L4 资产口径与来源标注

系统 SHALL 在清单中对每个资产标注 `source`（`real` / `placeholder`）与 `license`，且 `placeholder` 必须带 `sourceNote`；
UI、文档、验收证据三处 SHALL 标注「占位/真实」。

#### Scenario: 占位资产
- **WHEN** 清单中某资产 `source = "placeholder"`
- **THEN** 资产信息面板与图层菜单显示占位标注，验收报告写明「不验证几何精度」

#### Scenario: 真实资产缺许可
- **WHEN** 资产 `source = "real"` 但 `license` 为空
- **THEN** 校验脚本报 error，导入被拒绝

### Requirement: 清单可用性与回落

三维视图 SHALL 以 `data/rebuild/l4/manifest.json` 为唯一资产来源；当清单不可用、无已发布资产或覆盖不足时，
SHALL 自动回落白盒模式且不出现白屏或未捕获错误。

#### Scenario: 清单 500
- **WHEN** `GET /RestFul/Rebuild/Tileset` 返回 500
- **THEN** 前端 `mode = whitebox`，显示可见提示，页面 / 控制台错误为 0

#### Scenario: 无已发布资产
- **WHEN** 清单存在但 `published = false`
- **THEN** 默认白盒

### Requirement: 精度切换与贴地

用户 SHALL 能在「L4 精模」与「白盒」间切换，选择被 localStorage 记忆；L4 模型底部 SHALL 贴地，偏移 ≤0.2m。

#### Scenario: 切换三态
- **WHEN** 用户在图层菜单切换 L4 → 白盒 → L4
- **THEN** 三态均可用，3D Tiles 与白盒三园区批次可见性互斥，L4↔白盒画面差异 ≥1%

#### Scenario: 模型悬空
- **WHEN** 验收测量到底部与地面偏移 >0.2m
- **THEN** 验收 fail，需人工确认 heightOffset 或模型精度

### Requirement: 资产接入与回滚

资产接入 SHALL 可脚本化复现：校验 → 导入（未发布）→ 复检 → 发布；任一失败 SHALL 可回滚到上一版 manifest。

#### Scenario: 导入失败
- **WHEN** `import-asset --apply` 复检失败
- **THEN** 自动恢复备份 manifest，资产保持未发布，平台不受影响

### Requirement: 一键验收

SHALL 提供一条命令产出可归档证据（含清单/加载/切换/回落/贴地/画面差异/FPS/错误），退出码 0/1/2 区分通过/失败/前置不满足。

#### Scenario: 占位资产验收
- **WHEN** 对 placeholder 或 SIMULATED 资产执行 `pnpm l4:acceptance`
- **THEN** 报告 0 fail 且显式写明「不验证几何精度」
