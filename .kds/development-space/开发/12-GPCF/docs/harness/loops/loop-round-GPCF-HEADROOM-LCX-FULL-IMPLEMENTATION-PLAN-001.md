---
doc_id: GPCF-DOC-5FF130412D
title: Loop Round GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001

## 输入

- 用户提供的 Headroom 纳入方案。
- 用户补充要求：根据项目群范围差异，必须覆盖整个项目群。
- 既有 Headroom evidence：admission、L2 dry-run、runtime probe、项目覆盖矩阵、成本敏感性模型、生产 token 授权包和行动队列。

## 动作

1. 读取用户方案全文。
2. 复核 GPCF 文档治理、Loop 编排、防污染和 KDS TOKEN 规则。
3. 复核当前项目群状态矩阵中的项目范围。
4. 将 Headroom 定位为 `LCX / LOOP Context Optimization Layer`。
5. 把方案从单项目/示例口径扩展为 15 个项目/域的全量实施蓝图。
6. 生成全量实现提示词，作为后续 Agent 执行合同。

## 输出

- `02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md`
- `docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001.md`

## 检查

预期检查：

```bash
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
git diff --check -- 02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FULL-IMPLEMENTATION-PLAN-001.md
```

## 反馈

本轮只输出全量实施方案和执行提示词，不执行生产代理、不启用跨项目 memory、不运行 `headroom learn --apply`、不写真实 KDS、不处理未脱敏生产材料、不升级 accepted、integrated 或 production_ready。

下一轮可按本方案进入 `GPCF-HEADROOM-LCX-P0-CONTROLLED-PACKAGE-001`，创建 `loop/context/headroom/` 受控能力包、WAES policy、Harness schema、KDS registry 和安装/代理/学习脚本。
