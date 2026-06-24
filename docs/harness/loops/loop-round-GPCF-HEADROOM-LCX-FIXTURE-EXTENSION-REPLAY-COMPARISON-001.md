---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622
title: Loop Round GPCF Headroom LCX Fixture Extension Replay Comparison 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Fixture Extension Replay Comparison 001

## 输入

将 `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json` 输入 metadata replay 和 marker/retrieval miss comparison gate。

## 动作

1. 读取 5 项目域、3 场景、15 条 sanitized fixture 元数据。
2. 复用 LCX field map 生成 replay records。
3. 比对 marker、redaction、retrieval miss 和 answer equivalence 元数据。
4. 保持所有生产、验收、集成状态为 false。

## 输出

- `docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_fixture_extension_replay_comparison.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_fixture_extension_replay_comparison.py
```

## 反馈

本轮只证明扩展 fixture 的 metadata replay/comparison 可回放；不证明真实生产 token 节省或生产可用。

## 下一轮

建立扩展 fixture 的负向样例，验证原文、敏感材料、生产测量、跨项目事实写入和生产状态升级声明会被拒绝。
