---
doc_id: GPCF-DOC-C10C271958
title: GlobalCloud 项目文档完整度与 Loop 成熟度量化矩阵
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-document-loop-maturity-matrix.md
source_path: 09-status/globalcloud-project-document-loop-maturity-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 项目文档完整度与 Loop 成熟度量化矩阵

日期：2026-06-13

用途：将 12 个项目的基本文档体系、Loop 覆盖情况和量化成熟度收口到同一张表，作为下一轮 Loop 初始化和补债顺序依据。

## 评分规则

| 指标 | 说明 | 分值 |
|---|---|---:|
| Manifest | 项目 Manifest 已建立或已有基础 | 14 |
| loop-state | `docs/harness/loop-state.md` 或等价状态记录已建立 | 14 |
| 项目主线/架构边界 | 有项目级主线、架构或边界文档 | 14 |
| evidence/证据目录 | 有项目级 evidence 或样本输入 | 14 |
| 验收/状态审计 | 有验收、状态审计或 Harness 证据 | 14 |
| 项目文档数量 | 直接归属文档数，最多 10 分 | 10 |
| KDS 空间落位 | KDS 项目空间已有镜像文档 | 10 |

成熟度：L0 未进入 Loop；L1 有基础但未 loop_ready；L2 已进入微循环；L3 证据接近可审计；L4 已进入审计/验收；L5 已通过验收或集成。

## 12 项目量化矩阵

| 项目 | 代号 | 文档数 | KDS文档 | Manifest | loop-state | 架构边界 | evidence | 验收审计 | 完整度分 | Loop成熟度 | 当前状态 | 主要缺口 | 下一步 |
|---|---|---:|---:|---|---|---|---|---|---:|---|---|---|---|
| GFIS | GF | 14 | 14 | 是 | 是 | 是 | 是 | 否 | 76 | L3：证据接近可审计 | partial | 验收/状态审计；现场真实样本尚未提交；业务 UAT 尚未由工厂/生产/质量/仓储/GPC/WAES 角色签收；生产环境确认和外部联调仍缺；`127.0.0.1:8080` 被本机 Python/uvicorn 占用；迁移窗口未授权；所有 received/signed/confirmed 均为 false | 建立签收证据接收后的审计准备规则；仍不执行 `bench migrate`、schema sync、写 API 或外部联调 |
| GPC | GP | 27 | 22 | 否 | 否 | 是 | 是 | 是 | 62 | L1：已有基础但未 loop_ready | not_started | Manifest；loop-state；目标平台骨架尚未形成可验收实现 | 补齐 Manifest 与一期蓝图 |
| PVAOS | PV | 0 | 0 | 否 | 否 | 否 | 否 | 否 | 0 | L0：未进入 Loop | not_started | 项目级文档；Manifest；loop-state；项目主线/架构边界；evidence/证据目录；验收/状态审计 | 补齐 Manifest（P2） |
| WAES | WA | 117 | 8 | 否 | 否 | 是 | 是 | 是 | 62 | L1：已有基础但未 loop_ready | not_started | Manifest；loop-state | 补齐 Manifest（P2） |
| KDS | KD | 37 | 37 | 是 | 否 | 是 | 是 | 否 | 62 | L1：已有基础但未 loop_ready | not_started | loop-state；验收/状态审计 | 试点项目，P1 初始化 |
| Brain | BR | 0 | 0 | 是 | 否 | 否 | 否 | 否 | 14 | L1：已有基础但未 loop_ready | not_started | 项目级文档；loop-state；项目主线/架构边界；evidence/证据目录；验收/状态审计 | 试点项目，P1 初始化 |
| PKC | PK | 0 | 0 | 否 | 否 | 否 | 否 | 否 | 0 | L0：未进入 Loop | not_started | 项目级文档；Manifest；loop-state；项目主线/架构边界；evidence/证据目录；验收/状态审计 | 试点项目，P1 初始化 |
| XiaoC | XC | 58 | 58 | 是 | 否 | 是 | 是 | 是 | 76 | L1：已有基础但未 loop_ready | partial | loop-state；UI 测试 / Wrangler / loop-state 缺口 | 补齐 loop-state.md |
| XGD | XD | 0 | 0 | 否 | 否 | 否 | 否 | 否 | 0 | L0：未进入 Loop | not_started | 项目级文档；Manifest；loop-state；项目主线/架构边界；evidence/证据目录；验收/状态审计；Manifest 缺口 | 补齐 Manifest（P1） |
| XiaoG | XG | 0 | 0 | 否 | 否 | 否 | 否 | 否 | 0 | L0：未进入 Loop | not_started | 项目级文档；Manifest；loop-state；项目主线/架构边界；evidence/证据目录；验收/状态审计；Manifest 缺口 | 补齐 Manifest（P1） |
| MMC | MM | 0 | 0 | 否 | 否 | 否 | 否 | 否 | 0 | L0：未进入 Loop | not_started | 项目级文档；Manifest；loop-state；项目主线/架构边界；evidence/证据目录；验收/状态审计；Manifest 缺口 | 试点项目，P1 初始化 |
| GPCF | CF | 102 | 59 | 是 | 是 | 是 | 是 | 是 | 90 | L2：已进入微循环 | partial | KDS TOKEN 暂缓为上线同步门禁；Git dirty；多项目文档体系待补齐 | 监督 GFIS 数据字典与接口契约生成，并补 GPCF command log / Git clean evidence |

## 总体判定

- 12 项目平均文档完整度：36.8/100。
- 文档完整度 >=80 的项目数：1/12。
- Loop 成熟度 L0 项目数：5/12。
- Loop 成熟度 L1 项目数：5/12。
- Loop 成熟度 L2 及以上项目数：2/12。

## 执行结论

1. KDS 项目空间已经建立，但项目级基本文档体系尚未全量完善。
2. Loop 机制已经在总控矩阵层覆盖 12 个项目，但项目仓级 loop-state 和 evidence 尚未全量落地。
3. 当前量化体系已经具备可计算指标，下一步必须按本矩阵逐项目补齐，而不能只更新总控文档。

## 下一轮补齐顺序

1. GFIS：已完成 `GPCF-GF-LR-030` UAT 问题处置闭环和豁免复核规则，金融事实保持 L4 阻断，下一步建立签收证据接收后的审计准备规则。
2. GPCF：继续补 command log、Git clean evidence 与 KDS TOKEN 上线同步门禁。
3. MMC、KDS、Brain、PKC：作为试点项目补齐 Manifest、loop-state、evidence-index。
4. XiaoC：从 partial 推进到 loop_ready，补齐测试、部署和模型路由证据。
5. GPC、PVAOS、WAES、XGD、XiaoG：补 Manifest 和首轮输入，防止主线空转。
