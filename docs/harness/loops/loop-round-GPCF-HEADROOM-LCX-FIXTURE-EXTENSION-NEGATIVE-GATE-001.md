---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622
title: Loop Round GPCF Headroom LCX Fixture Extension Negative Gate 001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Fixture Extension Negative Gate 001

## 输入

建立扩展 fixture 负向样例门禁，验证越界声明和敏感字段会被拒绝。

## 动作

1. 生成 negative fixture boundary cases。
2. 覆盖 raw prompt、raw completion、敏感材料、生产测量、真实 KDS 写入、生产代理和状态升级声明。
3. 生成 evidence 和 validator。
4. 保持生产、验收、集成状态全部为 false。

## 输出

- `fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_fixture_extension_negative_gate.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_fixture_extension_negative_gate.py
```

## 反馈

本轮只证明负向边界样例可拒绝越界声明；不证明生产可用。

## 下一轮

建立脱敏 fixture 多轮稳定性门禁，检查连续 replay/comparison 输出是否稳定。
