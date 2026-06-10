# GlobalCloud 智能体团队首轮实施前验证包总表

日期：2026-06-08  
状态：首轮实施前验证包总表 v1  
用途：把固定 10 个专项的首轮实施前验证推进到统一可执行状态。

## 1. 总体结论

当前 6 个先导专项已完成正式只读预检，其余 4 个显性会话已建并进入待启动准备。
下一阶段统一进入“首轮实施前验证准备”。

本轮验证包只解决两类问题：

1. 运行前样本和实现落点是否存在
2. 是否具备进入首轮联调准备的前置条件

本轮验证包不解决：

1. 联调完成
2. 试运行完成
3. 生产运行完成

## 2. 专项验证包清单

| 专项 | 验证包 | 当前目标 | 当前状态 |
|---|---|---|---|
| 宪衡 | [宪衡专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/宪衡专项首轮实施前验证包.md:1) | 治理对象、证据对象、授权对象运行前样本 | `in_progress` |
| 链同 | [链同专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/链同专项首轮实施前验证包.md:1) | PVAOS/GPC 协同对象与运行前样本 | `in_progress` |
| 厂行 | [厂行专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/厂行专项首轮实施前验证包.md:1) | GFIS 主链回执与 Edge 事实转换样本 | `in_progress` |
| 数枢 | [数枢专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/数枢专项首轮实施前验证包.md:1) | 数据权限、读模型、DLQ/Replay、Trace/Evidence 样本 | `in_progress` |
| 知源 | [知源专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/知源专项首轮实施前验证包.md:1) | Brain remote、ingest、回指、失效拦截样本 | `in_progress` |
| 灵策 | [灵策专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/灵策专项首轮实施前验证包.md:1) | AI 服务域样本要求与越权、主账隔离闭环 | `in_progress` |
| 仓图 | [仓图专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/仓图专项会话状态报告.md:1) | 资源池对象与扩展边界执行化 | `not_started` |
| 接稳 | [接稳专项会话状态报告.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/接稳专项会话状态报告.md:1) | 连接器可靠性与 DLQ/Replay 样本闭环 | `not_started` |
| 评衡 | [评衡专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/评衡专项首轮实施前验证包.md:1) | 评分复评与偏差闭环（运行样本驱动） | `not_started` |
| 证验 | [证验专项首轮实施前验证包.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/证验专项首轮实施前验证包.md:1) | 证据分级、签核闭环与关键事件验收 | `not_started` |

## 3. 统一执行纪律

1. 全部验证先走只读或局部安全命令。
2. 任何可能触发真实写入、部署、外部调用、长期运行状态变化的动作，都必须先保留为“待人工确认”。
3. 所有验证结果都必须回写到专项验证包和总控周报。
4. 没有样本，不得把“已设计”升级成“已验证”。

## 4. 统一输出要求

每个专项验证包最终都要产出：

1. 已执行命令清单
2. 已取得证据清单
3. 未取得证据清单
4. 当前阻塞
5. 是否允许进入联调前准备

## 5. 模型治理专项验证入口

`A21-A24` 统一由灵策牵头，评衡、证验协同，宪衡、数枢配合：

1. `A21` 模型授权变更与生效验证：核对 `ModelAuthorizationGrant` 变更后调用结果是否切换。
2. `A22` 模型路由、降级与回退验证：核对 `ModelRouteDecision`、fallback 和人工覆盖证据。
3. `A23` 模型使用计量与统计回指验证：核对 `ModelUsageRecord`、`ModelMeterSnapshot` 和 trace 回指。
4. `A24` 模型越权或超预算拦截验证：核对 `ai.model_overreach.blocked` 和无未授权调用落地。
