---
doc_id: GPCF-SPACEAI-PANORAMA-TASKS-20261016
title: tasks
project: GPCF
related_projects: [GPCF, WAME]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-platform-panorama-convergence/tasks.md
source_path: openspec/changes/spaceai-platform-panorama-convergence/tasks.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## 1. 前置：基线与治理入口

- [x] 1.1 建立抽取前基线：1600×900 与 1600×1000 截图、DOM 节点数、JS 堆、FPS（有头/无头各一次）、14 接口状态，归档到 `harness/runs/<run-id>/evidence/`。
- [x] 1.2 记录抽取前函数清单（410 项）与分段清单（60 项），作为后续逐域核对的对照表。
- [x] 1.3 打通中央 Feature 入口：`gpcf_new_feature.py` 的项目白名单缺 `spaceai`（事实源 `config/project-group-projects.yaml` 已注册）。已修 `scripts/gpcf_feature_lib.py` 的 PROJECTS 白名单（补 `spaceai`，与事实源对齐），创建 F-024。

## 2. 纯模块域（先做，收益最高、风险最低）

- [x] 2.1 为域 1 `cards.ts` 先写行为基线测试（卡片列计算、分类体系、内容面清单），再抽取；断言公开契约。
- [x] 2.2 为域 2 `cardLayout.ts` 先写布局不变量测试（每场景两列铺满、左一=实时事件大卡、重点卡靠前、卡组折叠、拼图并排），再抽取。
- [x] 2.3 核对该两域的提取未改变模板可见行为：结构指标一致（DOM 1503 / 接口 27）；域 2 另做定向验证——注入卡组配置后组标签渲染正常，点击折叠仅组首可见（21→20，risk 隐藏、index 保留）。

## 3. 状态与持久化域

- [x] 3.1 域 3 持久化安全读取：先测（19 项，含坏形状守卫），再抽取为 `prefRead.ts`；并在 6 个读取点接入守卫——**修复了 D-4 整屏崩溃**（旧代码 DOM 239/卡片 0/地图无 → 修复后 1477/21/有）。底图与透明度为直接 localStorage 写入（键 `gc.pano.base` 等），未纳入本轮抽取，留待后续。
- [x] 3.2 域 4 回放：先测（26 项：窗口过滤/排序/密度直方图/截断含最小可见 4 条/历史模式/时间文案），再抽取为 `replay.ts` 并接线 5 处。真实浏览器验证：双击事件卡进入回放，密度柱 20 条、游标 max=200、拖到中段时间文案更新、21 个历史角标、0 错误。
- [x] 3.3 域 7 收藏与飞翔：先测（26 项：收藏形状守卫/幂等增删含根节点拒绝/三条快捷航线编排/分享载荷剔除内部 id/导入解析容错），再抽取为 `favorites.ts` 并接线 8 处。真实浏览器验证收藏守卫：4 条存储（1 有效 + 3 坏）→ 界面只用 1 条有效、0 错误。**资产层级导航的下钻与层级固定未纳入本轮**（依赖 navPath 状态机与地图飞行回调，属域 7 余量，留待后续）。

## 4. 表现与地图域

- [x] 4.1 域 5 表现层：先测（17 项：关联高亮有向映射与自洽性、色带三档阈值、卡片放大、场景强调色含回退、巡演取焦含越界回绕与空列表保护），再抽取为 `presentation.ts` 并接线 6 处。真实浏览器验证四项可观测信号（色带渐变/悬停点亮 forces+events/巡演 .tour-on=scene/仅 events 带 .grow），0 错误。**大屏态切换与单卡投放未纳入本轮**（涉及 window.open 与 requestFullscreen 副作用，属域 5 余量，留待后续）。
- [x] 4.2 域 6 地图交互：先测（31 项：视域几何/视频点位与最近点位/POI 网格聚合/地图接管态/空间检索三类与限额/底图枚举），再抽取为 `mapInteraction.ts` 并接线 8 处。真实浏览器检索「烟感」→ 地标+设备+事件三类且命中限额 30，0 错误。**气泡系统与点选映射未纳入本轮**（依赖 Cesium 事件与 DOM 锚定，属域 6 余量，留待后续）。
- [x] 4.3 域 8 动效音效：先测（20 项：闪光方向/心跳速率含单调性与封顶/音效三档参数/副作用注册表 7 项），再抽取为 `effects.ts`。**聚焦放大与 A3 悬停联动未纳入本轮**（前者的单击/双击区分逻辑已随 click 定时器接入注册表，后者依赖引擎 markerAdd）。

## 5. 副作用收口

- [x] 5.1 全量排查裸 `setInterval`/`setTimeout`/`addEventListener`/`requestAnimationFrame`/Web Audio 节点，纳入域 5/6/8 的 `onScopeDispose` 回收。
- [x] 5.2 新增"活跃副作用计数"导出，并写挂载→卸载后归零的测试。
- [x] 5.3 核对组件卸载后无回调继续触发（真实浏览器进/出全景态势 3 次，观察 console 与堆回落）。

## 6. 验证与交付

- [x] 6.1 全量门禁：`pnpm typecheck && pnpm -r build && pnpm exec vitest run` 通过，且包含本轮新增测试。
- [x] 6.2 抽取后对照：两档截图逐张比对、DOM 节点数变化 ≤5%、无新增 console/page error、14 接口全 200。
- [x] 6.3 交付性能基线表（抽取前后可比），明确其为后续优化输入而非本轮验收条件。
- [x] 6.4 归档证据到 `harness/runs/<run-id>/`，更新本变更 tasks 勾选状态与验收矩阵。
- [x] 6.5 回滚演练说明：逐域独立提交，可按单域 revert；不 reset/clean/force push。

## 7. 发现但不修（记账，留待后续轮次）

- [x] 7.1 记录既有缺陷（不改）交用户排期：**D-4 坏数据整屏崩溃（本轮已修）**；**D-5 `gc-prefs-loaded` 无监听者→跨机偏好同步对界面无效**；D-1 db.test.ts 全量并行下偶发失败（DB_PATH import 期冻结 + skipIf 只查文件存在）；D-2 favicon 404 噪声。
- [x] 7.2 无 GPU 环境性能要点已记录于 `iteration-summary.json` 的 `performance_baseline_for_next_iteration`：有头 61 FPS / 堆 373–401MB vs 无头 SwiftShader 3 FPS / 堆 290MB（相差约 20 倍）；用户确认虚拟机/远程桌面为实际部署环境，方向 B 立项可直接引用。
