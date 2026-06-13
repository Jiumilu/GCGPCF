---
doc_id: GPCF-DOC-8D5147AC17
title: Loop Risk Gate
project: WAES
related_projects: [WAES]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_RISK_GATE.md
source_path: 02-governance/loop/LOOP_RISK_GATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Risk Gate

## 风险分级

| 等级 | 定义 | 处理 |
|---|---|---|
| P0 | 可能造成数据丢失、权限泄露、未授权生产写入、战略口径错误或不可逆变更 | 立即暂停，等待用户确认 |
| P1 | 影响项目主线、跨项目边界、质量门禁或 evidence 真实性 | 可局部修复；无法修复则暂停 |
| P2 | 文档、模板、索引、局部测试或镜像一致性问题 | 自动修复并复验 |
| P3 | 格式、命名、轻微链接或 README 清单问题 | 自动修复并复验 |

## P0 自动暂停项

- 发现密钥、TOKEN、证书、权限配置泄露风险。
- 准备执行未授权真实生产写入或外部写入。
- 准备删除文件、大规模移动文件或迁移目录。
- 准备执行 `bench migrate`、schema sync、运行态写 API。
- 准备未授权 Git push、合并主分支、发布或部署。
- 准备将状态标记为 `accepted` 或 `integrated`。
- 发现文档与事实严重冲突且无法局部修复。

## 回滚与撤销要求

| 变更类型 | 最低要求 |
|---|---|
| 文档新增/修订 | 可通过 Git diff 审查；不得删除旧依据 |
| 本地脚本新增/修订 | 需要 validator 或 dry-run 输出 |
| mock / fixture | 必须说明不是真实业务数据 |
| dry-run 写入 | 必须有创建物、清理、残留核查 evidence |
| L3.5 真实接口验证 | 必须满足白名单、可回滚、可审计、测试数据标识、残留核查 evidence |
| L4 运营写入 | 必须在白名单内，禁止默认生产写入和生产部署 |
| L5 生产自治 | 必须有强授权口令、监控指标、回滚策略、incident/postmortem evidence |
| 未授权生产或外部写入 | 不得自动执行 |

## 风险记录字段

每次触发 P0/P1 风险，必须在 loop record 或 evidence 中记录：

| 字段 | 说明 |
|---|---|
| risk_id | 风险编号 |
| severity | P0/P1/P2/P3 |
| trigger | 触发条件 |
| affected_projects | 影响项目 |
| decision | 自动修复 / 暂停 / 请求确认 |
| rollback_path | 回滚或撤销路径 |
| owner | 责任方 |
