---
doc_id: GPCF-DOC-042A1FCA84
title: GPCF-KDS-DKS-011 数据对象最小落库与 API 契约草案 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-011.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-011.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-011 数据对象最小落库与 API 契约草案 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

上一轮 `GPCF-KDS-DKS-010` 已完成葛化 GFIS AI 助手内测运行记录模板，并建议本轮将 `GPCF-KDS-DKS-001` 至 `GPCF-KDS-DKS-010` 的对象收束为最小落库和 API 契约草案。

本轮读取并继承：

1. 绿色供应链分布式知识系统实施治理方案。
2. 对象字段与 KDS 11 池映射清单。
3. 葛化 GFIS AI 助手内测运行记录模板。
4. 当前 Loop 控制板关于 GFIS / GPCF `repair_required` 的状态边界。

## 2. 动作

本轮执行动作：

1. 建立受控契约草案：
   `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统数据对象最小落库与API契约草案.md`
2. 定义知识源、AI 建议、贡献积分、收益、悬赏、争议、AI 额度、葛化预运营、湖北磷材拓厂、AI 助手内测和 KDS 11 池挂接对象域。
3. 定义最小状态机、事件契约、API 路径草案、权限模型、幂等与审计字段。
4. 明确本轮不创建数据库、不实现 API、不写真实主账、不升级状态。

## 3. 输出

| 产物 | 路径 | 说明 |
|---|---|---|
| 数据对象最小落库与 API 契约草案 | `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统数据对象最小落库与API契约草案.md` | 定义最小表、事件、状态机、API、权限和 11 池挂接规则 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-011.md` | 记录本轮五段式治理微循环 |

## 4. 检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| 契约边界 | pass | 只定义草案，不声明实现 |
| API 写入边界 | pass | 所有写入默认 dry-run / 候选 / 人工确认 |
| 主账边界 | pass | 不写 GFIS / GPC / PVAOS 业务主账 |
| 权限边界 | pass | 合作单位默认 own_unit 可见 |
| 密级边界 | pass | DSR-L3 不进入开放问答 |
| 状态升级 | pass | 本轮不声明 accepted、complete 或 integrated |

## 5. 反馈

本轮结论：

1. 绿色供应链分布式知识系统最小数据对象和 API 契约草案已形成。
2. 前十轮对象已能被统一映射到表、事件、状态机、权限和 KDS 11 池。
3. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-012：
绿色供应链分布式知识系统权限与密级矩阵，把 DSR-L0 至 DSR-L3、合作单位可见范围、委员会可见范围、AI 助手可见范围、财务/质量/POD 特殊资料访问规则固化。
```

待用户回答：

1. DKS-011 的 API 是否先作为内部契约，不进入真实开发排期？
2. `dryRun` 是否作为所有写入 API 的默认值？
3. 合作单位是否默认只能看到 own_unit 范围，除非被邀请或参与悬赏？
4. DSR-L3 是否禁止进入开放问答和普通评测记录？
5. DKS-012 是否进入权限与密级矩阵？
