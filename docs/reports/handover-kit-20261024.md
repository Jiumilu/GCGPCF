---
doc_id: GPCF-DOC-9281B3C521
title: "待外部动作清单（2026-10-24 19:10 刷新）"
project: KDS
related_projects: [GFIS, GPC, WAME, KDS, Brain, PKC, XGD, MMC, GPCF, Studio, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/handover-kit-20261024.md
source_path: docs/reports/handover-kit-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 待外部动作清单（2026-10-24 19:10 刷新）

> 这份清单是 GPCF 侧"已就绪但必须由他人执行"的全部事项。每项都写了：
> **为什么必须你做 / 需要什么 / 做完后我接着做什么**。

## 0. 当前事实（实测）

| 项 | 值 |
|---|---|
| 分母 / 项目数 | 29 |
| C_dev / **C_real** | 41.53% / **0.00%** |
| blocked | 1（F-013） |
| done Feature | 23（19 可关单 + 4 受控例外） |
| 门禁 | pass |
| 治理覆盖 | 本地门禁 29/29；继承「不合规」0；CI 远端 standards 29 / test 24 / build 21 |

## 1. 唯一能让 C_real 破 0：PQC 真实客户一单

- **为什么必须你做**：纪律②禁止用 fixture/PoC/dry-run/合成数据；只有真实客户数据能让 VU 进 S4。
- **已就绪**：A1–A4 授权（`AUTH-PG-PQC-REAL-PILOT-20261022`）、M0 评审通过、契约已登记（`CONTRACT-PQC-PVA-EXTERNAL-SERVICE` controlled）、执行手册、一键收口脚本 `gpcf_pqc_pilot_close.py`（dry-run 不写台账，六项强校验拒绝模板/合成数据）。
- **需要什么**：客户代号 / 单据类型 / 脱敏确认（去姓名去联系方式）/ 预计执行日 / 复核人。
- **收到后我做**：`--dry-run` 预检 → 属主填证据 → `--apply` 推 VU 到 S4 → 复算 C_real → 台账/回执/计划状态同步。

## 2. F-013 剩余 13 条治理/授权（派单表已出）

详见 `docs/reports/f013-blocker-dispatch-20261024.md`。摘要：

| 归属 | 条数 | 其中"技术已验证、只差治理"的 |
|---|---:|---|
| KDS | 4 | `kds_stage_b_read_admission_technical_verified_governance_blocked` |
| Brain | 2 | — |
| Studio | 4 | — |
| MMC | 2 | `mmc_a9_bounded_read_subset_technical_verified_global_policy_not_narrowed` |
| 跨仓复核 | 1 | — |

**需要你**：①对上述 2 条"技术已验证"项做治理放行或明确否决；②把其余 11 条派给对应属主。

## 3. F-036（WAE ↔ PKC 首接入）：部署 / 正式 SSO / 属主签字

- 已验证：生产构建、CSP frame-ancestors、401/403 双端消息链、embed/embed-auth 证据
- 未满足：生产部署、正式 SSO、属主签字（正式评审为 conditional，不批准关闭）
- **为什么必须你做**：部署=生产红线；SSO 需 IdP 配置；签字是人工动作。

## 4. GCMEM / GCPQC 的 CI：两条路都需要人

| 路线 | 现状 | 需要谁 |
|---|---|---|
| 启动 `gc-macmini-GCMem` / `gc-macmini-GCPQC` self-hosted runner | 两者 **offline**，且**不在本机**（launchctl/plist/进程/docker 均无） | 运维（runner 实际所在主机） |
| 改用 GitHub 托管 runner | 实测被拒：**账户计费/支出上限**（job 未启动，注解已存档） | 你（Billing & plans） |

## 5. GFIS 生产栈部分宕机（发现项，未处置）

- `gcfis-backend-1` 7 天前退出 → `gcfis-frontend-1` nginx 解析 `backend:8000` 失败而崩溃循环
- `gcfis-queue-long-1` 连不上 `redis-queue:6379`
- **阻碍**：容器标签指向 compose 目录 `/private/tmp`，**该目录无 compose 文件**，无法安全重建缺失服务
- **为什么必须你做**：生产变更红线（`gate(rule=production)` → stop 0.771）
- **需要**：授权 + GFIS 部署仓的 compose 定义（或让属主自行恢复）

## 6. 我已能自动执行、但要等你一句话的

| 项 | 一句话即可 |
|---|---|
| KDS 重构成果取回 | 快照分支 `wip/kds-restructure-snapshot-full-20261024`（5ce9f69），说"取回"我就按目录恢复 |
| P16-2 CI 剩余 6 仓 | WAS/XWAIL/DRC 无测试套件、XGD/SpaceAI Studio 无构建、PKC 模型否决 → 需属主补或你给豁免 |
| 8 仓无总体方案 | PQC/SpaceAI/SpaceAI Studio/SLC/FireQuote 等需属主新建（我不代写正文） |
