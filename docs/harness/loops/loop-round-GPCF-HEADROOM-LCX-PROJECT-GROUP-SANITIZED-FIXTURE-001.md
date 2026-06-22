---
doc_id: GPCF-DOC-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622
title: Loop Round GPCF Headroom LCX Project Group Sanitized Fixture 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Project Group Sanitized Fixture 001

## 输入

用户选择补全 15 项目域 sanitized fixture，再做全项目域 replay/comparison/stability。

## 动作

1. 生成 15 项目域、3 场景、45 条 sanitized metadata fixture。
2. 保持 token 字段为 fixture 元数据，不声明生产实测。
3. 生成 evidence 和 validator。

## 输出

- `fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- `docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- `docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_project_group_sanitized_fixture.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_project_group_sanitized_fixture.py
```

## 反馈

本轮只证明全项目域 sanitized fixture coverage 已建立；不证明生产可用。

## 下一轮

执行全项目域 fixture replay/comparison/stability。
