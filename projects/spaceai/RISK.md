---
doc_id: GPCF-DOC-40D3030FDC
title: SpaceAI 风险
project: GPCF
related_projects: [SpaceAI, GPCF]
domain: governance
status: controlled
version: v1.3
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/spaceai/RISK.md
source_path: projects/spaceai/RISK.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# SpaceAI 风险

**项目定位**：空间智能平台（`GlobalCloud SpaceAI Platform` 为唯一正本）；CWME 本地应用已随 Legacy 归档（2026-10-22）。

## 当前风险

| ID | 风险 | 等级 | 说明 |
|---|---|---|---|
| R-01 | 占位资产被当成真实 L4 精模 | 高 | L4 链路已通，但演练/验收资产为 placeholder / SIMULATED，只能证明加载/切换/回落/贴地，**不能证明平面/高程 ≤0.3m 精度** |
| R-02 | 库无上限增长 | 中高 | `data/spaceai.db` **2.17GB**；`EXT_ObolObservation` 527,570 / `IngestEvent` 142,097 / `EXT_SceneAsset` 50,179 追加表无保留策略（D-10） |
| R-03 | 30+ 个提交只在本地 | 中 | `main` 领先 `origin/main` **34 提交**（19:04 为 30，随并行会话增长）；单点磁盘故障即丢失，推送需授权（D-13） |
| R-04 | 并行会话 WIP 混入 | 中 | 工作区有他方未提交改动（`apps/desktop/src/main.ts`、`vite.config.ts`、`pnpm-workspace.yaml` 等），误提交会把未验收改动带入账 |
| R-05 | KDS 镜像不同步 | 中 | 镜像树与源码有上千条未提交差异；若以镜像为准读账会得到过期事实（D-11） |
| R-06 | 人工验收缺口 | 中 | 派单确认/失败保留、CWME 回投确认/30s 幂等未被自动 e2e 覆盖，自动断言不能替代人工验收 |
| R-07 | 合成数据被写成真实运行 | 高（既有） | 不得把合成样例库、局部浏览器验证、占位三维模型写成真实城市/设备运行或平台集成 |
| R-08 | OpenSpec 变更缺口 | **低（2026-10-22 关闭）** | F-037 / F-038 已补建 `openspec/changes/spaceai-l4-precision-model`（implemented）与 `.../spaceai-panorama-operation-normalization`（in_progress），三层对齐表门禁通过 |

## 控制动作

- **L4**：三处标注（图层菜单 / 资产信息 / 文档）+ 验收报告显式写明「不验证几何精度」；真实资产到位后重跑 `pnpm l4:acceptance` 并要求供应商质检。
- **数据**：保留策略按时间窗非删除归档（D-10），先出只读容量报告再动手，不做 DELETE。
- **推送 / 镜像**：均需单独授权、单独操作，不与功能改动混做（D-11 / D-13）。
- **并行会话**：提交前逐文件核对，不 `git add -A`；WIP 由各自会话收口。
- **Feature 复核**：以 `projects/spaceai/STATUS.md` 与 F-017 / F-024 / F-037 / F-038 证据复核；缺失证据标待补，不以文档登记替代。

## 状态上限

人工验收与生产发布未确认，保持 **partial / rework**；不得提升 accepted / integrated / production_ready / customer_accepted。
