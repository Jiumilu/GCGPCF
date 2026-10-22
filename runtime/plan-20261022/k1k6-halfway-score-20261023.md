---
doc_id: GPCF-DOC-K1K6-HALFWAY-SCORE-20261023
title: K1–K6 能力半程评分（2026-10-23）
project: GPCF
related_projects: [GPCF, WAE, PKC, WAME, XWAIL, GFIS, GPC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/runtime/plan-20261022/k1k6-halfway-score-20261023.md
source_path: runtime/plan-20261022/k1k6-halfway-score-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# K1–K6 能力半程评分（2026-10-23）

> 性质：**估算评分**，非审计事实；评分依据为当前仓内可回放证据与双账本。
> 公式：`K = (K1×K2×K3×K4×K5×K6)^(1/6)`。

## 1. 评分

| 维度 | 起点（framework v1.0） | 半程 | 依据 |
|---|---:|---:|---|
| K1 感知 | 15 | **15** | 真实 SOR 仍 0；批次 2 0/2；会议→Feature 仍弱 |
| K2 决策 | 20 | **35** | 授权回执 22 granted / 16 executed；StartLux 决策留痕 12 条；问答+概率机制落地 |
| K3 交付 | 45 | **52** | closed 15（F-010/F-034 等）；F-035/F-036 六门 pass；active 22 |
| K4 治理 | 30 | **45** | 契约 8/8 closed；门禁 9/9 pass；CI gates 强化；VU 校验器；pytest 59/59 |
| K5 复用 | 25 | **31** | 资产注册表 25 项；跨仓扫描：活跃复用 1 项（startlux，5 项目）+ 3 项仅归档；validator/模板复用 |
| K6 商业 | 5 | **5** | 无真实订单/回款/客户验收 |

## 2. 计算

```text
K = (15 × 35 × 52 × 45 × 31 × 5)^(1/6)
  = 190,417,500^(1/6)
  ≈ 23.99 / 100
```

起点：约 19/100（framework v1.0 六维几何平均）；半程 **≈ 23.99**，提升约 5.0。

## 3. 解读

- 提升主要来自 K2（授权留痕）与 K4（契约/门禁），K3 小幅提升。
- K1/K6 仍接近零，几何平均被显著拉低；真实业务线（批次 2/3）不启动，K1/K6 不会改善。
- K5 提升有限：跨仓活跃复用仅 1 项（startlux），3 个 skill 仅归档；注册表引用度量已建立但真实复用仍少。

## 4. 下一半建议

1. K1：批次 2 外部输入到位后接入真实 SOR。
2. K6：真实订单/回款/客户验收闭环（依赖业务线）。
3. K3：F-035/F-036 收口，降低 blocked/返工。
4. K5：补资产引用次数与复用项目数度量。

## 5. 非声明

- 评分是估算，不是审计结论；
- 不声明 90 天目标已达成；
- 不声明任何项目状态提升。
