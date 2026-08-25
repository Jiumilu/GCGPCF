---
doc_id: GPCF-DOC-GCWORLD-042
title: GCWORLD受控运行时集成任务清单
project: GPCF
related_projects: [XWAIL, WAES, KWE, MMC, KDS, GFIS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-controlled-runtime-integration/tasks.md
source_path: openspec/changes/gcworld-controlled-runtime-integration/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## 1. 运行授权与责任边界

- [ ] 1.1 批准所属Release、后继Feature、目标仓库、运行责任人、安全责任人、线程和有界文件范围。
- [ ] 1.2 批准首个R0/R1纵向切片、测试环境、服务边界、数据范围、凭据、网络和保留期限。
- [ ] 1.3 明确XWAIL、WAES、KWE、MMC、KDS、GFIS及业务系统的接口责任和禁止替代事项。
- [ ] 1.4 建立阶段开关、紧急冻结、撤销、停机和回滚的人工责任与确认矩阵。

## 2. 镜像与建议闭环

- [ ] 2.1 先为跳过快照、裁决、确认、取证或回执的路径编写失败测试。
- [ ] 2.2 实现真人会话、智能体调用、运行身份、连接器凭据和业务动作的身份分离。
- [ ] 2.3 实现世界快照、有效权限交集、默认拒绝、短期裁决和提交前复核。
- [ ] 2.4 实现无外部连接器的R0镜像与R1建议闭环，验证真实执行和外部写入均为0。

## 3. 可靠命令、回执与补偿

- [ ] 3.1 实现命令标识、幂等键、因果标识、关联标识、契约版本和失效时间校验。
- [ ] 3.2 实现收件去重、事务发件、受控重试、死信、部分失败和不可变责任回执。
- [ ] 3.3 为重复命令、裁决过期、连接器超时、回执丢失、补偿失败和撤销传播编写测试。
- [ ] 3.4 验证没有目标系统结果证据的动作不能标记成功。

## 4. 分阶段真实执行

- [ ] 4.1 为R2内部测试写入另行取得Feature、数据、凭据、确认和Harness授权后再启用阶段开关。
- [ ] 4.2 为每类R3外部动作分别批准目标、用途、责任人、双重确认、补偿和审计，不使用通用放行。
- [ ] 4.3 为R4重大行动实施不可绕过硬门禁、多人治理、紧急冻结和事后复核。
- [ ] 4.4 验证低阶段授权、技术能力或缓存裁决均不能扩大高阶段权限。

## 5. 验证、证据与回滚

- [ ] 5.1 执行单元、状态机、集成、故障注入、构建、格式、类型、安全和零副作用检查。
- [ ] 5.2 验证GKE‑001 Program与CodeGraph绑定；只有真实服务或事件关系变化时才更新权威映射。
- [ ] 5.3 更新Feature日志、Evidence Index、验收矩阵和中文文档，并通过OpenSpec严格校验及项目群文档门禁。
- [ ] 5.4 演练关闭阶段开关、撤销身份与凭据、停止任务、处置未完成回执和恢复只读模式。
- [ ] 5.5 将真实服务、真实裁决、真实确认、真实连接器和目标系统回执分项提交Harness独立复核。
