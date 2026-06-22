---
doc_id: GPCF-DOC-1B5550FF05
title: Loop L3.5 Real API Verification Policy
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_L3_5_REAL_API_VERIFICATION.md
source_path: 02-governance/loop/LOOP_L3_5_REAL_API_VERIFICATION.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop L3.5 Real API Verification Policy

## 定位

L3.5 = Controlled Real-API Verification Mode / 受控真实接口验证模式。

L3.5 用于补齐 L3 dry-run 与真实系统之间的验证缺口。它不承担全自动运营，不承担生产自治，只在严格白名单、可回滚、可审计的前提下验证真实 API 可用性。

## 状态

| 字段 | 值 |
|---|---|
| 模式状态 | executable / requires explicit activation |
| 默认是否启用 | 否 |
| 是否可由 L3 自动升级 | 否 |
| 运行上限 | 最多 5 轮或 1 小时，以先到者为准 |
| 默认继续 | 授权范围内仍有待验证接口、未触发接口/回滚/污染停止条件时，必须继续下一轮 |

## 启动口令

最小口令：

```text
启动 Loop L3.5 受控真实接口验证模式。
```

合格口令必须同时包含：

| 字段 | 示例 |
|---|---|
| 授权项目 | GPC / GlobalCoud GPCF |
| 授权环境 | staging / sandbox / 指定测试环境 |
| 授权 API | KDS sync validate-only / GFIS runtime health / 指定接口 |
| 授权时间窗 | 2026-06-13 20:00 至 2026-06-13 21:00，Asia/Shanghai |
| 允许动作 | 真实 API 读、真实鉴权、validate-only、sandbox 写入、单条白名单测试写入 |
| 禁止动作 | 批量写入、删除、权限变更、生产部署、不可回滚写入 |
| 回滚策略 | 删除测试记录或恢复到验证前状态 |
| 验收指标 | API 返回成功、响应结构符合契约、无新增错误、测试记录可回滚 |

## 允许动作

- 真实 API 读取。
- 真实鉴权检查。
- 真实 endpoint 连通性测试。
- validate-only 请求。
- dry-run 请求。
- sandbox 写入。
- staging 写入。
- 单条白名单测试写入。
- 读取写入后的真实结果。
- 执行回滚或清理验证。
- 记录请求摘要、响应结构、状态码和时间戳。
- 生成 evidence。
- 更新接口契约文档。
- 更新 Loop 控制板。

## 禁止动作

- 批量生产写入。
- 删除真实生产数据。
- 修改权限。
- 修改 Token。
- 修改密钥。
- 生产部署。
- 修改生产配置。
- 不可回滚写入。
- 跨项目真实写入。
- 自动扩大 API 授权范围。
- 标记 production accepted。
- 标记 integrated。

## 启动前门禁

| 门禁 | 要求 |
|---|---|
| 授权项目 | 明确 |
| 授权环境 | 明确，且不得默认 production |
| 授权 API | 明确到接口或接口组 |
| 时间窗 | 明确 |
| 允许动作 | 明确 |
| 禁止动作 | 明确 |
| 回滚策略 | 明确且可执行 |
| 验收指标 | 明确 |
| 凭证来源 | 可控，不写入文档、日志、Git 或 evidence |
| 测试数据 | 必须有 `loop-test-*` 或等价标识 |
| Git 状态 | 可解释 |

## 自动暂停条件

- API 返回权限错误。
- API 返回非预期 4xx/5xx。
- 响应结构与契约不一致。
- 写入后无法验证。
- 回滚或清理失败。
- 出现真实数据污染风险。
- 凭证异常。
- 触及未授权 API。
- 触及生产批量写入。
- 触及删除动作。
- 用户发出暂停、停止或降级指令。

## 连续推进与停止规则

L3.5 active 后，完成一次接口验证、生成一次 evidence 或完成一次阶段性汇报都不是停止条件。只有满足以下任一条件时才能停止：

1. 已连续完成 5 轮。
2. 已运行满 1 小时。
3. 触发 API 权限错误、非预期 4xx/5xx、响应契约不一致、回滚失败、真实数据污染风险或凭证异常。
4. 触及未授权 API、生产批量写入或删除动作。
5. 用户明确暂停、停止或降级。
6. 授权接口清单已全部验证，回滚/清理/残留核查完成，且已生成下一步建议。

## 真实性计数门禁

L3.5 的轮次预算只能按 `substantive_rounds` 计数。一次接口记录、一次 evidence 生成、一个批量脚本输出或多个模板化 API 验证文档，不能自动计为多个实质轮次。

每个 L3.5 实质轮次必须至少满足 4/5：独立接口输入、独立验证判断、独立响应/清理输出、独立验证命令或真实返回证据、独立反馈或回滚结论。

若 `declared_rounds` 达到 5/5 但 `substantive_rounds` 未达到 5/5，不得使用 `budget_exhausted` 收口，必须更正为 `authorization_boundary`，并运行：

```bash
python3 tools/kds-sync/validate_continuous_round_substance.py
```

## Evidence 要求

每次 L3.5 验证必须记录：

| 字段 | 要求 |
|---|---|
| endpoint | 可记录路径，不记录密钥和完整敏感查询串 |
| request_summary | 记录字段结构和测试数据标识 |
| status_code | 必填 |
| response_schema | 必填，敏感值脱敏 |
| timestamp | 必填 |
| cleanup_result | 如有写入则必填 |
| residual_check | 如有写入则必填 |

## 与其他等级的关系

| 模式 | 真实 API 读 | 真实 API 写 | 部署 | 定位 |
|---|---:|---:|---:|---|
| L3 | 否 | 否 | 否 | 开发闭环与 dry-run |
| L3.5 | 是 | 有限、白名单、可回滚 | 否 | 真实接口验证 |
| L4 | 是 | 白名单内可允许 | 默认否 | 全自动运营 |
| L5 | 是 | 授权内允许 | 授权内允许 | 完全生产自治 |
