---
doc_id: GPCF-DOC-GCWORLD-030
title: GCWORLD与KDS权威事实集成任务清单
project: GPCF
related_projects: [KDS, WAS, WAES, XWAIL]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-kds-authoritative-integration/tasks.md
source_path: openspec/changes/gcworld-kds-authoritative-integration/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## 1. 独立授权与准入

- [x] 1.1 批准本变更所属Release、F‑013或后继Feature、目标仓库、责任人、线程和有界文件范围。
- [ ] 1.2 清理或隔离KDS既存变化，验证F‑013准入为明确放行且记录提交、远端和工作树摘要。
- [x] 1.3 批准首批租户、项目、数据等级、S3处置、只读接口、凭据、有效期和撤销方式。
- [x] 1.4 复核身份候选、关系争议和S3例外的人工责任、SLA、双人复核与升级路径。

## 2. 只读集成与投影

- [ ] 2.1 先为准入快照缺失、过期、冲突和工作树变化编写失败测试。
- [ ] 2.2 实现只读KDS适配器，固定确定性排序、来源摘要、双时间、本体版本和零写入声明。
- [ ] 2.3 实现候选、例外和人工复核队列，证明同名身份及冲突关系不会自动合并。
- [ ] 2.4 实现可重建GCWORLD投影和差异检测，验证投影、索引与缓存不会成为第二事实账本。

## 3. 受控事实提升

- [ ] 3.1 在取得单独写入授权前保持提升通道硬禁用，并增加无授权、无确认和版本冲突负向测试。
- [ ] 3.2 定义并实现幂等提升请求、WAES裁决、人工确认、KDS执行回执和重新读取对账。
- [ ] 3.3 实现重复请求、部分失败、回执丢失、对账失败、撤销和补偿测试。
- [ ] 3.4 验证S3正文、未决候选、目标状态和模拟结果不能进入正式提升请求。

## 4. 验证、证据与回滚

- [ ] 4.1 执行适用的单元、集成、确定性、构建、格式和安全检查，记录不适用项及原因。
- [ ] 4.2 验证GKE‑001 Program与CodeGraph绑定；只有关系实际变化时才更新权威映射。
- [ ] 4.3 更新Feature日志、Evidence Index、验收矩阵和中文文档，并通过OpenSpec严格校验及项目群文档门禁。
- [ ] 4.4 演练停用凭据、冻结批次、撤销任务和从KDS事实重建投影的回滚流程。
- [ ] 4.5 将证据提交Harness独立复核；任务勾选不得作为已验收、已集成或生产就绪依据。
