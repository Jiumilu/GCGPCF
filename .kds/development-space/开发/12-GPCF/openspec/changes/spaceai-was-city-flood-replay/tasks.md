---
doc_id: GPCF-SPACEAI-FLOOD-TASKS-20261016
title: tasks
project: GPCF
related_projects: [WAME, GPCF]
domain: openspec
status: implemented
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-was-city-flood-replay/tasks.md
source_path: openspec/changes/spaceai-was-city-flood-replay/tasks.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## 1. 模型与契约
- [x] 1.1 创建逐片标注 synthetic 的内涝网络，复用已批准 XWAIL Schema，校验零错误零警告。
- [x] 1.2 记录 sourceRefs、规则引用、指纹与晚到修订，保持三世界身份。

## 2. 回放与视图
- [x] 2.1 先编写时间、修订、幂等、过期、关系和范围过滤测试，再实现纯投影函数。
- [x] 2.2 从投影结果生成中文动态切片网络，验证时间与口径切换及证据详情。
- [x] 2.3 运行单元测试、构建与语法检查；浏览器验证成功或明确记录阻塞。

## 3. 证据与治理
- [x] 3.1 独立代码审查，保存本轮变更 patch、验收矩阵和 evidence-index。
- [x] 3.2 回读文档门禁与项目群 readiness，追加 F-017 journal/evidence，不提升状态。
- [x] 3.3 完成 Harness audit_only，记录回滚边界；正式 spec sync/归档待后续验收，不在本轮执行。

## 4. CWME 应用落地
- [x] 4.1 在 apps/city-model 形成独立本地应用与可复跑构建入口，保持模型单一来源。
- [x] 4.2 修正当前项目 CWME 定位，增加应用入口及使用说明，不覆盖旧工程与已有CWME文档。
- [x] 4.3 执行模型回归、独立网页真实浏览器验证及独立审查，保存证据。
- [x] 4.4 完成本轮门禁与 Harness audit_only，保持 partial，不发布或归档。
