---
doc_id: GPCF-DOC-F034-TOKEN-REQUEST-20261024
title: O2 跨仓令牌整改请求（2026-10-24）
project: GPCF
related_projects: [WAE, PKC, Brain, PVAOS]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/token-consolidation-request-20261024.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/token-consolidation-request-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# O2 跨仓令牌整改请求

## 权威来源

- `GlobalCloud WAE/packages/ui-tokens/src/tokens.css`
- 76 个令牌；sha256 前 16 位 `54729cdf634fadd5`
- 复核命令：`python3 tools/verify-token-sources.py`（WAE 仓）

## 当前偏离

| 仓/文件 | 结果 |
|---|---|
| WAE apps/wame default_theme / globals | 薄壳，零重复声明 ✓ |
| Brain default_shadcn_theme.css | 与权威逐字节相同 ✓ |
| PKC src/styles/theme.css | 值不同 34 处 |
| Brain src/styles/theme.css | 值不同 30 处 + 独有令牌 5 |
| PVAOS 目标路径 | 不存在（需属主确认落点） |

## 请求

1. PKC 属主：以 WAE ui-tokens 为准替换/收敛 34 处差异，或登记受控例外。
2. Brain 属主：收敛 30 处差异；5 个独有令牌逐一裁定（迁入权威或登记例外）。
3. PVAOS 属主：确认令牌落点路径，补薄壳或登记例外。
4. 整改后重跑 WAE `verify-token-sources.py`，期望「逐字节相同」或登记例外清零。

## 非声明

- 不声明已整改；不声明 F-034 可关闭。
