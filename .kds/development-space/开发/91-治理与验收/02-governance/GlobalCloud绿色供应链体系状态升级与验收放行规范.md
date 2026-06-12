---
doc_id: GPCF-DOC-5D55FFB7D9
title: GlobalCloud 绿色供应链体系状态升级与验收放行规范
project: WAES
related_projects: [GPC, WAES, XiaoC]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系状态升级与验收放行规范.md
source_path: 02-governance/GlobalCloud绿色供应链体系状态升级与验收放行规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系状态升级与验收放行规范

日期：2026-06-08
状态：状态升级与验收放行规范 v1
用途：把 Harness 状态纪律落实到团队执行层，防止虚假完成和状态漂移。

## 1. 可用状态

只允许使用以下状态：

- `not_started`
- `in_progress`
- `partial`
- `blocked`
- `pass_with_runtime_blockers`
- `ready_for_human_acceptance`
- `accepted`
- `complete`

## 2. 升级原则

1. 状态升级必须有证据。
2. 状态升级必须有交付物完成判定支持。
3. 状态升级必须有验证结果支持。
4. 证据不足时，必须维持或退回较低状态。

## 3. 小即权限

1. 小即是唯一可以升级总体状态的人。
2. 各专项负责人只能提交升级建议，不能自行升级总体状态。
3. 评衡与证验可以驳回升级建议。

## 4. 当前阶段升级边界

在首轮实施前验证准备阶段：

1. 可以写：
   - 已完成正式只读预检
   - 可进入首轮实施前验证准备
2. 不可以写：
   - `ready_for_human_acceptance`
   - `complete`
   - 已联调完成
   - 已试运行完成

## 5. 放行条件

### 5.1 进入 `ready_for_human_acceptance`

至少要求：

1. 关键交付物完成
2. 关键验证通过
3. 阻塞项已关闭或已受控
4. 人工验收只剩最终确认，不剩工程级未解问题

### 5.2 进入 `complete`

至少要求：

1. 已通过人工验收
2. 所有必需运行证据存在
3. 无关键阻塞
4. 状态、证据、交付物三者一致

## 6. 退回条件

以下情况必须退回：

1. 证据不成立
2. 验证失败
3. 发现交付物与设计不一致
4. 发现无授权仓库改动
5. 发现 AI 结论被误写成业务事实
