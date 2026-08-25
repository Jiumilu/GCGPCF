---
doc_id: GPCF-DOC-GCWORLD-028
title: GCWORLD与KDS权威事实集成变更提案
project: GPCF
related_projects: [KDS, WAS, WAES, XWAIL]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-kds-authoritative-integration/proposal.md
source_path: openspec/changes/gcworld-kds-authoritative-integration/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## 变更原因

GCWORLD已经形成证据孪生、只读普查和候选台账，但KDS当前仍有工作树准入阻塞，身份候选与S3例外也尚未完成最终人工处置。需要先定义一套不复制KDS主账、默认只读、可逐项授权的权威事实集成契约，作为未来真实连接的前置规划。

## 变更内容

- 定义KDS事实、证据、候选、例外与GCWORLD世界投影之间的单向读取和受控提升边界。
- 要求每次集成运行绑定KDS提交、工作树、授权、来源分级、本体和投影版本快照。
- 建立身份候选与关系争议人工复核、幂等提升请求、写入回执、失败补偿和可重放对账要求。
- 将KDS工作树干净、F‑013准入明确放行、独立写入授权和人工确认设为任何真实写入的硬前置条件。
- 当前只创建GPCF规划产物，不修改KDS或其他责任仓库，不执行API、写入、部署或状态提升。

## 能力范围

### 新增能力

- `gcworld-kds-authoritative-integration`：定义GCWORLD从KDS读取正式事实、保留候选与例外、受控提出事实提升并完成回执对账的权威集成契约。

### 修改能力

无。

## 影响范围

- **Program / Release：** GKE‑001；`release_0`后续规划候选，任何实现前必须重新分配并批准Release阶段。
- **Feature：** 绑定F‑013 `knowledge-asset-model-system`；F‑013当前状态与上限保持不变。
- **当前目标仓库与责任方：** GPCF / GPCF，仅限本OpenSpec目录。
- **未来依赖：** KDS、WAS、WAES、XWAIL；对应仓库、接口和责任人均待独立授权。
- **基线：** `gcworld-evidence-twin-foundation` Harness结论为 `pass_with_runtime_blockers`；KDS准入为 `blocked_dirty_worktree`。
- **CodeGraph：** 仅声明未来 `KDS事实→GCWORLD投影` 与 `GCWORLD候选→KDS受控提升请求` 关系，不修改当前权威绑定。
- **非目标：** 不处理全部身份争议，不读取S3正文，不建立第二事实账本，不直接写KDS，不授权运行时集成。
- **回滚：** 删除本次未提交的规划目录即可，不改变来源、运行状态或外部系统。
