---
doc_id: GPCF-DOC-40640A40
title: design
project: GPCF
related_projects: [GPCF, SpaceAI]
domain: openspec
status: implemented
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-l4-precision-model/design.md
source_path: openspec/changes/spaceai-l4-precision-model/design.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-l4-precision-model · Design

## 1. 口径先写死（避免把占位当真实）

- **L4 定义**：单体建筑真实几何（外轮廓/层高/女儿墙/屋面设备/雨棚/台阶/门窗洞口级）+ PBR 材质；平面/高程误差 ≤0.3m；底部贴地不悬空。不含室内。
- **source 必填**：`real` 或 `placeholder`；placeholder 必须写 `sourceNote`，UI/文档/证据三处标注。
- **license 必填**：真实资产写数据许可；占位写「内部演示数据」。
- 三园区优先；其余 OSM 楼群保持白盒（8614 栋）。

## 2. 清单与加载（单一事实源）

- `data/rebuild/l4/manifest.json` 是唯一事实源；BFF `GET /RestFul/Rebuild/Tileset` 返回 `rows`（清单 + 内存登记合并）与 `manifest`（路径/时间/条数）。
- 前端不写死 URL：按 manifest 加载；无已发布资产或覆盖不足 → 默认白盒。
- 二进制资产不入 git（`data/rebuild/` 忽略），清单与生成脚本入库。

## 3. 切换与回落（可用性优先）

| 状态 | 触发 | 行为 |
|---|---|---|
| L4 就绪 | manifest 有已发布真实/占位资产 | 显示 L4，隐藏白盒三园区批次 |
| 白盒 | 用户切换 / localStorage 记忆 | 显示白盒，隐藏 3D Tiles |
| 回落 | 清单 500 / 无已发布资产 / 加载失败 | 自动回落白盒 + 可见提示，不白屏 |

- 贴地：`region[4]`（minHeight）或清单 `heightOffset`；引擎 `tilesetGroundClamp` 校准，验收阈值 ≤0.2m。
- 切换判据不只靠文案：验收用**画面差异 ≥1%** + `data-status=ready` + 白盒批次 `show=false`。

## 4. 接入工具链（可复现，不手工拷贝）

`validate-tileset`（结构/坐标/文件/清单）→ `import-asset --unpublished`（校验 + 备份 manifest）→ 复检 → `switch-asset --publish` → `pnpm l4:acceptance` → 归档证据。
失败路径：任一步 error 即停，`published=false`，前端回落白盒。

## 5. 验收方法（20 项检查）

清单有已发布资产 / 覆盖三园区 / ready / 资产数 ≥1 / tileset.json 200 / 首屏 ≤90s / show=true / 内容就绪 / 视口内（warn）/ 白盒隐藏 / 贴地 ≤0.2m / 切白盒 / 回切 L4 / 画面差异 ≥1% / 清单 500 回落 / whitebox / 页面错误 0 / 控制台错误 0 / FPS ≥12 / 目标 ≥30。
**不验证几何精度**：精度需供应商质检或实测（≥20 特征点）。

## 6. 已知取舍

- 占位资产用程序化生成（162 栋 SIMULATED 演练 + 三园区占位），只证明链路；不得作为精度验收依据。
- 重建算力（WorldMirror/3DGS）为 stub，不做真实重建。
- 真实资产三路径（采购 / 自采 / 合规外部源）均暂停或未授权，blocker 记录在 F-037。

## 7. 三层对齐

见 proposal.md「三层对齐（契约 → 工具链 → 应用链）」一节（契约层 = manifest + BFF 端点；工具链 = tools/l4 + CI；应用链 = 精度模型 + 图层菜单 + 回落）。
