---
doc_id: GPCF-DOC-BF9AA5F60D
title: Headroom LCX 运行模型
project: WAES
related_projects: [WAES]
domain: general
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/loop/context/headroom/docs/operating-model.md
source_path: loop/context/headroom/docs/operating-model.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX 运行模型

## LCX-Proxy

`start-proxy.sh` 只允许 dev/test/dry-run，本地脚本拒绝 `HEADROOM_PRODUCTION_PROXY=true`。

## LCX-SDK

SDK 接入只用于受控应用、RAG、Harness 和 Agent runtime 的脱敏上下文。每次调用必须形成 Harness evidence。

## LCX-MCP

`headroom_compress` 和 `headroom_stats` 可见；`headroom_retrieve` 受限，必须满足 WAES retrieve gate。

## LCX-Agent-Wrap

Agent wrap 只能通过 Loop 启动器或等价受控入口调用。`wrap-codex.sh` 默认关闭 telemetry 和 output shaper，不允许 learn apply。

## LCX-CCR

CCR 可以恢复原文，但恢复动作必须记录任务、调用者、理由、内容类型、敏感检查和 evidence 引用。

## LCX-Learn

`learn-preview.sh` 只运行 preview。候选经验必须经过 Harness evidence、WAES pass 和 Owner 审核后才能进入工作记忆。

## LCX-Output-Shaper

开发和日志调试可按 profile 开启。正式验收、合规、合同和财务场景必须关闭。
