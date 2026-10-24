---
doc_id: GPCF-DOC-3D2E0797B1
title: 校验器笔误修复：external loop gate delegates（2026-10-24）
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/validator-typo-fix-20261024.md
source_path: docs/reports/validator-typo-fix-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 校验器笔误修复：external loop gate delegates（2026-10-24）

- 授权：`decide_template(authorization_qa)` → **yes 0.93**
- 现象：门禁报 `hard_failure:project_group_external_loop_gate_delegates`，仅 AAAS 等仓失败
- 根因：校验器要求被委托仓脚本包含 `GPCF_ROOT = ROOT.parent / "GlobalCoud GPCF"`——**少一个 l 的错误拼写**

## 1. 实测分布（29 仓扫描）

| 拼写 | 仓数 |
|---|---:|
| 正确 `"GlobalCloud GPCF"` | **21** |
| 错拼 `"GlobalCoud GPCF"` | **0** |
| 无该行（无委托 gate） | 8 |

→ 校验器的期望值是笔误，被检查方全部正确。

## 2. 修法

- 新增 `GPCF_ROOT_TOKENS`（正确拼写优先、兼容历史错拼写）；
- 从 `REQUIRED_TOKENS` 移除笔误项；
- 改为 `require(any(t in text for t in GPCF_ROOT_TOKENS), "missing GPCF_ROOT 声明")`。

**不放宽任何实质约束**：其余 5 个委托 token 与 7 个 forbidden token 不变。

## 3. 验证

```bash
python3 tools/kds-sync/validate_project_group_external_loop_gate_delegates.py   # exit 0
python3 tools/kds-sync/loop_document_gate.py --check-only                       # gate=pass
```

## 4. 回滚

```bash
cd "GlobalCloud GPCF" && git checkout -- tools/kds-sync/validate_project_group_external_loop_gate_delegates.py
```
