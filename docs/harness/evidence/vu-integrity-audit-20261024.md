---
doc_id: GPCF-DOC-VU-INTEGRITY-20261024
title: VU 台账完整性审计（2026-10-24）
project: GPCF
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# VU 台账完整性审计

## 结构

- VU 数量：**97**
- VU 权重合计：**380**
- project_scope 项目：**29**
- project_scope 权重合计：**105**
- 缺失项目：0
- 非法权重（≤0/非整数）：0

## 阶段分布

| 阶段 | 数量 |
|---|---:|
| S0 | 29 |
| S1 | 39 |
| S2 | 20 |
| S3 | 9 |
| S4–S6 | 0 |

## C_dev 独立复算

- 公式：项目内 VU 加权 → 项目权重归一 → 项目群平均
- 独立复算：**41.53%**
- 与 renderer 输出一致

## 说明

- C_real=0（无 S4+）。
- 本审计不改变阶段或分数。
