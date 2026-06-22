---
doc_id: GPCF-DOC-CA83191660
title: GlobalCloud 绿色供应链体系 Edge 接入与安全模型
project: GPCF
related_projects: [GPCF, GFIS, GPC, WAES]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud绿色供应链体系Edge接入与安全模型.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系Edge接入与安全模型.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系 Edge 接入与安全模型

日期：2026-06-07
状态：四流优化专项模型 v1
适用范围：现场设备、工业网关、OPC UA、Modbus、MQTT、SCADA、DCS、PLC、AGV、扫码枪、工位屏、边缘缓存、GFIS。

## 1. 模型定位

Edge 是现场与 GFIS 之间的边缘接入层，负责采集、协议转换、缓存、补传、去重和回执。Edge 不是业务主账，不决定工单、质量、库存、发货、签收、维修验收或治理状态。

当前架构更新口径：Edge 归属于 `GFIS` 执行侧，不属于绿链平台业务主线；宪法内容在 Edge 场景中体现为设备保护、授权边界、补传证据和高风险禁止接管。

## 2. 边界原则

1. Edge 默认只读采集。
2. Edge 产生的是遥测事实，不是业务主账事实。
3. 现场信号进入 GFIS 规则后，才可能触发业务流程。
4. AI 不得直接反控 PLC、DCS、急停、安全联锁、设备保护或环保排放控制。
5. 断网时 GFIS 本地运行优先，恢复后 Edge 缓存补传。

## 3. Edge 对象

| 对象 | 主责 | 用途 |
|---|---|---|
| EdgeNode | Edge / GFIS | 边缘节点、网关、工位终端 |
| DeviceSignal | Edge | 现场遥测事实 |
| EdgeBufferPolicy | Edge / WAES | 缓存、补传、去重、丢弃策略 |
| EdgeReplayRun | Edge / GFIS | 断网后补传运行记录 |
| Equipment | GFIS | 设备主数据 |
| MaintenanceOrder | GFIS | 维修工单 |
| EvidenceRecord | WAES | 现场证据引用 |

## 4. 采集分级

| 级别 | 数据 | 处理方式 |
|---|---|---|
| E1 | 普通状态、温度、速度、计数 | 可自动采集和上报 |
| E2 | 报警、停机、超限、AGV 异常 | 自动上报 GFIS 和 WAES |
| E3 | 影响质量、产量、库存的关键事件 | 进入 GFIS 规则确认 |
| E4 | 可能触发停线、质量隔离或维修 | 需 GFIS 内部流程和人工确认 |
| E5 | 安全联锁、急停、设备保护、环保排放控制 | AI 禁止接管，只允许确定性控制和授权人员 |

## 5. 缓存和补传

`EdgeBufferPolicy` 必须定义：

| 字段 | 说明 |
|---|---|
| bufferWindow | 缓存时长 |
| maxBufferSize | 最大缓存容量 |
| dedupKey | 去重键 |
| dropPolicy | 丢弃策略 |
| replayWindow | 补传窗口 |
| replayApprovalRequired | 是否需要治理确认 |
| orderingPolicy | 顺序保证 |
| evidencePolicy | 补传证据 |

补传状态：

```text
buffering -> reconnecting -> replaying -> replayed -> verified
buffering -> overflow -> discarded
```

## 6. 事件要求

Edge 必须使用以下事件：

```text
edge.node.online
edge.node.offline
edge.device_signal.received
edge.device_alarm.raised
edge.buffer.replayed
edge.buffer_policy.changed
edge.replay_run.completed
```

Edge 不得发布：

```text
gfis.work_order.released
gfis.quality_inspection.accepted
gfis.inventory_transaction.posted
gfis.factory_shipment.released
gpc.pod.signed
waes.governance_approval.approved
```

## 7. AI 安全边界

| AI 动作 | 是否允许 | 条件 |
|---|---:|---|
| 查询设备状态 | 是 | L1，只读 |
| 生成报警摘要 | 是 | L2，引用 DeviceSignal |
| 建议维修 | 是 | L3，GFIS/EAM 确认 |
| 建议停线 | 受限 | L4，只能建议，不能执行 |
| 质量放行 | 否 | GFIS/QMS 内部确认 |
| 反控 PLC/DCS | 否 | L5 禁止 |
| 急停和安全联锁 | 否 | L5 禁止 |

## 8. 验收要求

| 场景 | 判定 |
|---|---|
| Edge 节点上线 | EdgeNode online，GFIS/WAES 均可见 |
| 设备信号接收 | DeviceSignal 可回指设备、时间、trace |
| 报警触发 | edge.device_alarm.raised 进入 GFIS/WAES |
| 断网缓存补传 | EdgeReplayRun、去重、顺序和证据完整 |
| AI 禁止反控 | 越权动作生成 `ai.overreach.blocked` |
