---
doc_id: GPCF-DOC-260DDD94E9
title: Headroom LCX Rollout 计划
project: WAES
related_projects: [WAES, KDS, Brain]
domain: general
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/04-WAES/loop/context/headroom/docs/rollout.md
source_path: loop/context/headroom/docs/rollout.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Rollout 计划

## P0：OSS / License / Security / Runtime

建立隔离安装、telemetry off、许可证登记、安全边界和 runtime probe。

## P1：LCX-Proxy dry-run

为 Codex、Claude、Cursor、LiteLLM 建立 dev/test/dry-run proxy。禁止生产代理。

## P2：LCX-SDK 与 LCX-MCP

为 KDS、Brain、Harness、Agent runtime 建立 SDK/MCP 受控配置。`headroom_retrieve` 必须通过 WAES gate。

## P3：LCX-Learn 与工作记忆

`headroom learn` 只允许 preview。候选经验必须经 Owner 审核后才能应用。

## P4：LCX-Output-Shaper

开发和日志调试可开启；正式验收、合规、合同、财务场景关闭。

## P5：生产准入申请包

只生成申请包，不自动进入生产。P5 需要授权窗口、脱敏生产 token 账本、真实价格输入、连续观测 evidence 和 WAES/Harness 裁决。
