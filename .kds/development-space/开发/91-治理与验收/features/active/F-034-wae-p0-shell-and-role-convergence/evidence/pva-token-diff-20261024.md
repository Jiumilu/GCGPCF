---
doc_id: GPCF-DOC-F034-PVA-TOKEN-DIFF-20261024
title: PVA/PVAOS 令牌路径与差异（2026-10-24）
project: GPCF
related_projects: [WAE, PVA]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/pva-token-diff-20261024.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/pva-token-diff-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# PVA/PVAOS 令牌路径与差异

## 路径

- verifier 期望：`GlobalCloud PVAOS/src/styles/default_theme.css`
- 实际仓：`GlobalCloud PVA/src/styles/default_theme.css`
- 结论：PVAOS 与 PVA 为同一平台仓的不同称谓；verifier 路径需按实际仓名映射。

## 差异

- 共同变量 76；仅 **1 处**不同：
  - `--muted-foreground`：WAE `oklch(0.708 0 0)` / PVA `oklch(0.78 0 0)`
- PVA 独有变量 0。

## 处置

- 路径映射登记进 token 例外；1 处差异交 PVA 属主裁定（对齐或例外）。

## 非声明

- 不声明差异已消除；不声明 F-034 可关闭。
