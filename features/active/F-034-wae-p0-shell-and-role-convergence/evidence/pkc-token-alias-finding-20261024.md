---
doc_id: GPCF-DOC-F034-PKC-TOKEN-ALIAS-20261024
title: PKC 令牌差异实为语义别名层（2026-10-24）
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# PKC 令牌差异实为语义别名层

## 发现

`verify-token-sources.py` 报 PKC `theme.css` 34 处不同；逐项检查发现 PKC 并非硬编码另一套值，而是通过 `--gc-*` 语义变量别名：

| 变量 | WAE ui-tokens | PKC theme.css |
|---|---|---|
| `--background` | `oklch(0.145 0 0)` | `var(--gc-bg-canvas)` |
| `--foreground` | `oklch(0.985 0 0)` | `var(--gc-fg-primary)` |
| `--primary` | `oklch(0.985 0 0)` | `var(--gc-accent-default)` |
| `--border` | `oklch(0.269 0 0)` | `var(--gc-border-default)` |

- PKC 侧 76 个变量全部存在；无 PKC-only 变量。
- 差异是「语义别名 vs 原始值」的表示层差异，不是数值漂移。

## 结论

- 直接把 WAE 原始值写入 PKC 会破坏 PKC 主题语义层，**不可自动替换**。
- 正确处置：
  1. 登记为**受控例外**（别名层允许），或
  2. PKC 属主将 `--gc-*` 解析值对齐 WAE ui-tokens，再让 verifier 按解析值比较。
- 本轮不改 PKC 代码。

## 非声明

- 不声明差异已消除；不声明 F-034 可关闭。
