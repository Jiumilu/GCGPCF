---
doc_id: GPCF-DOC-94C5F5E540
title: 现代精工工厂岗位培训资料结构化分析
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/modern-jinggong-training-analysis.md
source_path: 08-evidence-samples/GFIS/modern-jinggong-training-analysis.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 现代精工工厂岗位培训资料结构化分析

## 1. 来源文件

| 项 | 内容 |
|---|---|
| 文件名 | `现代精工工厂岗位培训学习资料_优化版.pdf` |
| 原始位置 | `/Users/lujunxiang/Downloads/现代精工工厂岗位培训学习资料_优化版.pdf` |
| 受控副本 | `08-evidence-samples/GFIS/source-files/现代精工工厂岗位培训学习资料_优化版.pdf` |
| 标题 | 现代精工工厂岗位培训学习资料 |
| 作者 | 葛化项目专班 |
| 生成时间 | 2026-06-10 15:05:31 CST |
| 页数 | 17 |
| 版式 | A4 PDF |
| SHA-256 | `eeff75dd7be9aff05ab2f04f4a86e4dba2d8058a55fef8800358fe6007fe2b62` |

## 2. Loop 定位

该文件应定位为 GFIS 工厂执行系统的首轮业务样本，不应被视为 GFIS 已实现证据。

| Loop 项 | 定位 |
|---|---|
| 项目 | GFIS |
| 首轮 Round ID | `GPCF-GF-LR-001` |
| 输入类型 | source document / field-study preparation evidence |
| 可支撑目标 | 岗位、流程、业务对象、数据项、质量门禁抽取 |
| 不可支撑目标 | 不能单独证明系统实现、现场运行或验收通过 |

## 3. 核心业务内容

PDF 覆盖一条中空板生产交付链：

```text
原材料采购
→ 配方研发
→ 样箱打样
→ 客户确认
→ 安排生产
→ 质检检测 / 产品入库
→ 产品销售
→ 产品出库
→ 客户交付
→ 循环回收
```

该链路可作为 GFIS 最小闭环中“工厂事实主账”的输入，但与 GPC 的客户协同、签收、对账、回款链路存在交叉，需要在后续 Loop 中明确边界。

## 4. 岗位到项目能力映射

| 岗位/模块 | GFIS 能力映射 | 跨项目关系 |
|---|---|---|
| 配混料班组 | 原料批次、配方、投料、留样、灰分/含水率记录 | KDS 沉淀工艺知识 |
| 挤出生产班组 | 工单、产线、设备参数、首件确认、过程巡检 | WAES 约束异常停机和质量门禁 |
| 印刷/覆膜班组 | 工序参数、外观质量、OEM 附加工费数据 | GPC 对接客户定制需求 |
| 模切/成箱班组 | 工序流转、箱型、模具、承重/尺寸检验 | GFIS 形成成品工艺记录 |
| 包装入库班组 | 一物一码、库存、库位、出库复核 | GPC 对接交付和 POD |
| 维修保障班组 | 设备点检、故障、备件、OEE、MTTR | WAES 管控安全和停机事件 |
| 商务销售岗 | 需求、报价、订单、合同、回款、投诉 | 主责应归 GPC，GFIS 接收生产输入 |
| 财务经营分析岗 | 成本、毛利、预算、应收、现金流风险 | GPC/财务域协同，GFIS 提供生产成本事实 |
| 品质管理 | IQC、IPQC、FQC、第三方外检、质量五条铁律 | WAES 形成质量放行门禁 |
| 仓储物流 | 分区、拣货复核、签收单回收、物流异常 | GFIS 管库存，GPC 管客户交付协同 |
| 信息化与数据 | ERP/MES/WMS、全链路追溯、经营看板 | KDS/Brain 用于知识化和展示 |

## 5. GFIS 首轮可抽取对象

| 类型 | 候选对象 |
|---|---|
| 主数据 | 原料、配方、设备、产线、产品、箱型、客户订单、库位 |
| 业务单据 | 来料检验单、配料批次记录、生产日报、首件确认、巡检记录、成品检验、入库单、出库单、设备点检表 |
| 事件 | 异常配料、异常停机、质量不合格、物流异常、客户投诉、逾期回款 |
| 指标 | 单线产能、成品率/合格率、OEE、单位电耗、用工配置、原料损耗率、边角料回收率、成本核算准确率 |
| 门禁 | 未检验不得入库、未确认不得量产、未放行不得发货、未隔离不得返工、未闭环不得销项 |

## 6. 与最小闭环目标的关系

GFIS 最小闭环不应一次覆盖 PDF 全部内容。建议先压缩为：

```text
客户订单/生产需求
→ 工单
→ 配料批次
→ 挤出生产记录
→ 过程巡检
→ 成品检验
→ 入库
→ 出库
→ 交付事实回写
```

其中“客户需求、报价、合同、回款”应进入 GPC 主线；GFIS 只保留生产执行需要的订单约束和交付事实接口。

## 7. 风险与缺口

| 风险/缺口 | 影响 | 下一步 |
|---|---|---|
| PDF 是培训准备材料，不是现场实际记录 | 不能作为验收完成证据 | 现场考察后补真实数据 |
| 部分清单符号在文本抽取中变成控制字符 | KDS 检索质量受影响 | 保留 PDF，同时维护 Markdown 结构化版 |
| 商务/财务内容与 GPC 边界交叉 | 容易把 GFIS 做成全平台 | 在 LR-001 中明确 GFIS/GPC 边界 |
| 信息化系统描述较概括 | 无法直接形成接口契约 | LR-002 补数据字典和接口候选 |
| 设备参数缺少现场确认值 | 不能直接生成产能模型 | 现场采集单线产能、OEE、电耗 |

## 8. 建议 Loop 输出

`GPCF-GF-LR-001` 应输出：

- GFIS 岗位-业务对象映射表
- GFIS 十阶段业务链边界说明
- GFIS 首批数据字典候选
- GFIS 质量门禁候选
- GFIS 与 GPC / WAES / KDS / Brain 的接口候选
- 现场考察数据采集表

## 9. 状态建议

| 项 | 建议 |
|---|---|
| 当前状态 | source_evidence_ready |
| 允许升级 | 不允许直接升级 GFIS 到 `loop_ready` |
| 进入条件 | GFIS 仓库补齐 Manifest、`docs/harness/loop-state.md`、loops/evidence 目录 |
| 下一轮 | `GPCF-GF-LR-001`：岗位、流程、数据、门禁抽取 |
