---
doc_id: GPCF-DOC-D914A0DA14
title: GlobalCloud 项目群完成度双账本首版基线 v1.0
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP, PQC, SpaceAI, SpaceAIStudio, World, GCMEM, WAE, Project, PDC, SLC, DRC]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-group-completion-baseline-v1.0.md
source_path: 09-status/globalcloud-project-group-completion-baseline-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群完成度双账本首版基线 v1.0

- 生成时间：2026-10-22T05:36:02+0800
- 任务：**PG-02 完成度双账本**（Wave 0 / P0）
- 口径来源：《GlobalCloud 项目群完成度与综合能力提升 · 任务优先级清单 v1.0》**§1.2 完成度模型**、§2.2 双账本估算、§8 90 天里程碑；纪律来源：《GlobalCloud 项目群实施方案》**§4 实施状态机 / §4.1 开发完成与真实业务验证分离原则**
- 数据源：`runtime/vu-ledger.yaml`（28 项目 / 94 个 VU，generated_at=2026-10-22T05:33:03+08:00）
- 复算器：`tools/kds-sync/render_project_group_completion.py`
- 文档性质：**首版基线（inferred）**。全部 94 个 VU 均标 `inferred: true`，全部 C 值均为**估算**，**不是受控事实**。

---

## 1. 定位与边界

**本文做什么**：把 §1.2 的价值单元（VU）模型落成三件可复算产物 —— 台账（`runtime/vu-ledger.yaml`）、渲染脚本、首版读数；公式、权重与阶段判定依据全部可回放。

**本文不做什么**：

1. 不重写 §1.2 的模型定义，只引用并给出可计算落地（见 §2.3 的系数表，落地选择需人工确认，见 §7）。
2. 不声明任何项目真实业务完成、客户验收、系统集成或生产就绪；不提升任何项目状态。
3. 不把估算写成事实：台账每一条 `inferred: true`，本文不出现"已验证""已验收"类结论。
4. 不替代 PG-01 的口径冻结：本文分母固定 28（`config/project-group-projects.yaml`），但 PG-01 的脏工作树/门禁分母冻结仍未落地。

**与既有产物的关系**：`project-state.md`（2026-10-22 只读盘点）提供 28 项目真实形态与证据缺口；本文在其上定义 VU 并给出开发/真实两套口径的首版读数。

---

## 2. 模型与公式（引用 §1.2，不重写定义）

### 2.1 价值单元（VU）五元组

引用 §1.2：`(业务场景, 权威主体, 单据/资产对象, 事实源, 验收人)`，每项目 3–5 个 VU，全群约 100 个。台账字段 `scene / authority / object / source_of_record / acceptor` 与五元组一一对应。

### 2.2 阶段与权重（§1.2 原表）

| 阶段 | 判据（§1.2 原文） | 权重 w |
|---|---|---:|
| S0 未定义 | 无 VU、无验收人 | 0.00 |
| S1 开发候选 | 代码 / fixture / dry-run 存在 | 0.20 |
| S2 内部验证 | tests / build / validator pass | 0.35 |
| S3 复核就绪 | evidence 包完整 + review 请求 | 0.50 |
| S4 真实业务验证 | 真实 source-of-record 通过 source validation + runtime intake + review queue | 0.70 |
| S5 人工验收 | owner / WAME / 客户确认 | 0.90 |
| S6 闭环归档 | 交付 + 回滚 + 知识化 | 1.00 |

### 2.3 PG-02 的可计算落地（口径系数表）

§1.2 定义：`C_dev` 只计 S0–S3（**把 S3 视为该口径的 1.0**）；`C_real` 只计 S4–S6。为使其可复算，本文将两套口径落成**口径系数**（`vu-ledger.yaml` → `stage_weights.*.dev` / `.real`）：

| 阶段 | §1.2 原权重 w | C_dev 系数 | C_real 系数 |
|---|---:|---:|---:|
| S0 | 0.00 | 0.00 | 0.00 |
| S1 | 0.20 | 0.40 | 0.00 |
| S2 | 0.35 | 0.70 | 0.00 |
| S3 | 0.50 | **1.00** | 0.00 |
| S4 | 0.70 | 1.00（开发已饱和） | 0.70 |
| S5 | 0.90 | 1.00（开发已饱和） | 0.90 |
| S6 | 1.00 | 1.00（开发已饱和） | **1.00** |

- `C_dev` 系数 = `min(w / 0.50, 1.00)`：S3 恰好为 1.00，S4–S6 表示开发口径已饱和（不重复计分）。
- `C_real` 系数：S0–S3 计 0（未进入真实业务验证），S4–S6 取 §1.2 原权重，S6 为唯一 1.00。
- **此落地化是 PG-02 的实施选择，不是 §1.2 的原文**；若老卢裁定改用 §1.2 原权重直接算术平均（C_dev 上限将变为 50%），只需改 `stage_weights` 的 dev 列并重跑脚本，公式与文档口径不变。

### 2.4 公式（§1.2 原文）

```text
C_project = Σ(weight_i × coefficient(stage_i)) / Σ weight_i
C_group   = Σ(PW_j × C_j) / Σ PW_j
```

- `weight_i`：VU 权重（1–5，表示该 VU 在项目内的业务关键度）。
- `PW_j`：项目业务关键度（主链核心 4–5 / 基础与知识 3–4 / 支撑与 external 2–3），落在 `vu-ledger.yaml` → `project_scope[].weight`，合计 101。
- `C_dev` 用 dev 系数列，`C_real` 用 real 系数列，分别计算项目级，再按 `PW_j` 加权得项目群级。

### 2.5 阶段判定纪律（§1.2 + 实施方案 §4.1）

- 无证据 = S0；仅代码 / fixture / dry-run = S1；tests / build / validator pass = S2；evidence 包 + review 请求 = S3。
- 真实 source-of-record 通过 source validation + runtime intake + review queue = S4；人工验收 = S5；闭环归档 = S6。
- **`fixture / dry-run / mock / SIMULATED / PoC governor` 最高 S2，不得进入 S4**（脚本 `--check` 强制校验；本次 94 条中 0 条违规）。
- 无事实依据的条目填 S0/S1 并标 `inferred: true`。
- 与实施方案 §4 状态机的映射：本项目群 `planned/in_progress ≈ S1`、`verified ≈ S2`、`ready_for_review ≈ S3`、`ready_for_uat/customer_review ≈ S4–S5`、`closed ≈ S6`；§4.1 的 `development_lane` 与 `real_business_validation_lane` 正是 C_dev / C_real 两条账本的制度依据。

---

## 3. 首版结果（脚本真实输出）

> 以下为 `python3 tools/kds-sync/render_project_group_completion.py` 的 stdout **原文**，仅将首行标题层级由一级下调为三级以嵌入本节；数值、表行、缺口语均未改动。

### GlobalCloud 项目群完成度双账本（PG-02）

- 台账：`runtime/vu-ledger.yaml`（generated_at=2026-10-22T05:33:03+08:00）
- 公式：`C_project = Σ(weight_i × coefficient(stage_i)) / Σ weight_i`；`C_group = Σ(PW_j × C_j) / Σ PW_j`
- VU 总数：94（inferred=94）；项目数：28；项目权重和：101
- **项目群 C_dev = 35.10%｜C_real = 0.00%**
- 90 天目标口径：C_dev ≥ 55.00%、C_real ≥ 12.00%（目标，非当前事实）
- 全部条目为首版基线估算（inferred），不是受控事实。

| 项目 | PW | VU 数 | C_dev | C_real | 阶段分布 | 主要缺口 |
|---|---:|---:|---:|---:|---|---|
| AAAS | 4 | 3 | 42.50% | 0.00% | S0×1 S1×1 S2×1 | 无项目级状态与证据；ServiceRuntime/WAME binding 仅本地预检，无真实服务包运行 |
| Brain | 4 | 3 | 26.67% | 0.00% | S0×1 S1×2 | 无项目级 STATUS 实质内容；Brain↔KDS 写回契约未落地；lint/format 未清 |
| WAS | 5 | 4 | 40.00% | 0.00% | S0×1 S1×2 S2×1 | F-022 tests/build/summary 全 pending；真实 P4 source-of-record 连续 16 轮为 0 |
| XiaoC | 4 | 4 | 56.88% | 0.00% | S1×2 S2×2 | F-033 summary 未收口；WAME 侧为 PoC governor；消费方未联调 |
| WAME | 5 | 4 | 44.12% | 0.00% | S0×1 S1×1 S2×2 | 引擎面 not_implemented；lint 两处报错；正式治理裁定/发布未发生 |
| GPC | 4 | 3 | 15.38% | 0.00% | S0×2 S1×1 | 外部/运行证据缺；SCaaS 链路未复核；无项目级状态 |
| Studio | 4 | 3 | 62.50% | 0.00% | S1×1 S2×2 | F-011 缺专属验收命令与可用性/无障碍门禁；F-015 主动冻结 |
| GPCF | 5 | 5 | 48.33% | 0.00% | S1×4 S2×1 | 9 个历史 done 不符现行关闭规则；双方案未全核验；授权链已建但未开闸 |
| XWAIL | 4 | 3 | 42.50% | 0.00% | S0×1 S1×1 S2×1 | 无 Feature 载体；Validator/Profile 不完整；XAP 仅由 F-033 PoC 间接覆盖 |
| GFIS | 5 | 4 | 30.00% | 0.00% | S0×2 S1×1 S2×1 | F-005 为 dry-run 样本；真实工厂系统写入与运行层证据缺；停滞 98 天 |
| MMC | 3 | 3 | 28.00% | 0.00% | S0×1 S1×2 | 无项目级状态；委派/人工确认契约仍挂在 F-013 blockers |
| KDS | 5 | 4 | 43.89% | 0.00% | S0×1 S1×1 S2×2 | F-017 归属与证据位置错位（证据在 SpaceAI 仓）；GPU/数据场地未排期；真实 API 同步未授权 |
| XiaoG | 3 | 3 | 26.67% | 0.00% | S0×1 S1×2 | 全栈暂停；live API/设备验证未做；BFF 契约未验证 |
| PVAOS | 4 | 4 | 10.00% | 0.00% | S0×3 S1×1 | 架构承接分支未检出；跨项目接口 implementation_pending |
| SOP | 4 | 3 | 10.00% | 0.00% | S0×2 S1×1 | F-012 零证据、停滞 98 天；owner review 未裁定 |
| PKC | 3 | 3 | 40.00% | 0.00% | S1×3 | 无项目级状态；KDS/Brain 依赖仅 dry-run |
| XGD | 3 | 3 | 39.23% | 0.00% | S0×1 S1×1 S2×1 | F-031 screenshots/api/summary 三项 fail；D10/D11/72h/语音未收口 |
| ICP | 4 | 3 | 39.23% | 0.00% | S0×1 S1×1 S2×1 | F-019 api/summary fail；真实业务源未连接 |
| PQC | 3 | 3 | 25.45% | 0.00% | S0×1 S1×2 | F-032 仅 plan；真实业务与权限验收未执行；项目总体方案 missing |
| SpaceAI | 3 | 4 | 39.38% | 0.00% | S0×2 S2×2 | 数据为 SIMULATED 合成库；真实设备未接入；queue 状态落后 |
| SpaceAIStudio | 2 | 3 | 50.00% | 0.00% | S1×2 S2×1 | Windows/Linux 产物与 GUI 启动运行证据缺；不能独立构建 |
| World | 3 | 3 | 28.00% | 0.00% | S0×1 S1×2 | Ontology 版本冲突；中央门禁 rework_required（6 项 missing_metadata） |
| GCMEM | 3 | 4 | 50.00% | 0.00% | S0×1 S1×1 S2×2 | F-026 Evidence Gate 不可关闭；三夜挖掘 1/3；容器迁移未验证 |
| WAE | 3 | 3 | 14.55% | 0.00% | S0×2 S1×1 | P0 四项未开始；唯一方案未确认；首批界面未纳入 |
| Project | 3 | 3 | 40.00% | 0.00% | S0×1 S1×1 S2×1 | Plane UI 未验证；实例停机；共享/生产实例写入未授权 |
| PDC | 3 | 3 | 40.00% | 0.00% | S1×3 | F-030 tests/summary 双 fail；浏览器关键任务与方案继承未核验 |
| SLC | 2 | 3 | 14.55% | 0.00% | S0×2 S1×1 | 无 Feature；测试/构建/关键任务未重跑；跨仓门禁 20/20 未通过 |
| DRC | 3 | 3 | 16.00% | 0.00% | S0×2 S1×1 | 数据库连接/资源目录/权限模型未实现；门禁 rework_required |

> 由 `tools/kds-sync/render_project_group_completion.py` 生成；数值全部来自 `runtime/vu-ledger.yaml` 复算，无手工填写。

**项目群读数**：`C_dev = 35.10%`、`C_real = 0.00%`（项目权重和 101，28 项目全覆盖）。

---

## 4. 抽样复核（XiaoC / GFIS / KDS）

复核方法：逐 VU 重读五元组与 `stage_evidence`，按 §2.3 系数用同一公式手算，与脚本输出比对。

### XiaoC（PW=4，VU=4，形态=有实质进展）

| VU | weight | stage | data_class | C_dev 项 | 阶段判定依据 | 备注 |
|---|---:|---|---|---:|---|---|
| XiaoC-VU-01 | 5 | S2 | poc | 5×0.70 | F-033 tests/build pass；XAP 信封与 WAME 台账/回执联调（PoC）；summary pending | PoC 联调，summary 未收口 |
| XiaoC-VU-02 | 4 | S2 | poc | 4×0.70 | req-b1579fe37e4e 已裁定/发布（PoC scope）；WAME 侧为 PoC governor | PoC governor 上限 S2 |
| XiaoC-VU-03 | 4 | S1 | fixture | 4×0.40 | 消费方任务包齐备但实际联调未做 | 任务包 ≠ 联调 |
| XiaoC-VU-04 | 3 | S1 | dry_run | 3×0.40 | 需专项授权；无部署证据 | 环境边界阻塞 |

- C_dev 算式：(5×0.70 + 4×0.70 + 4×0.40 + 3×0.40) / 16 = 0.5688 → **56.88%**（脚本值 56.88%）
- C_real 算式：(5×0.00 + 4×0.00 + 4×0.00 + 3×0.00) / 16 = 0.0000 → **0.00%**（脚本值 0.00%）
- 结论：手算与脚本一致；该项目 main_gap = F-033 summary 未收口；WAME 侧为 PoC governor；消费方未联调

### GFIS（PW=5，VU=4，形态=有实质进展）

| VU | weight | stage | data_class | C_dev 项 | 阶段判定依据 | 备注 |
|---|---:|---|---|---:|---|---|
| GFIS-VU-01 | 5 | S2 | dry_run | 5×0.70 | F-005 tests/build/summary pass，系 dry-run 样本；STATUS 明示「不代表真实工厂系统写入」 | dry-run 上限 S2 |
| GFIS-VU-02 | 5 | S0 | none | 5×0.00 | real_source_records=0；pending_business_verification 未建立；无运行层主键 | 真实 SOR 缺席，约束 C-D |
| GFIS-VU-03 | 4 | S1 | dry_run | 4×0.40 | 仅在 dry-run 内生成主键与队列条目，无 runtime intake 真实记录 | 开发闭环候选，未进入真实运行 |
| GFIS-VU-04 | 3 | S0 | none | 3×0.00 | 无客户确认记录、无业务验证回执 | 验收人明确但从未触发 |

- C_dev 算式：(5×0.70 + 5×0.00 + 4×0.40 + 3×0.00) / 17 = 0.3000 → **30.00%**（脚本值 30.00%）
- C_real 算式：(5×0.00 + 5×0.00 + 4×0.00 + 3×0.00) / 17 = 0.0000 → **0.00%**（脚本值 0.00%）
- 结论：手算与脚本一致；该项目 main_gap = F-005 为 dry-run 样本；真实工厂系统写入与运行层证据缺；停滞 98 天

### KDS（PW=5，VU=4，形态=有实质进展）

| VU | weight | stage | data_class | C_dev 项 | 阶段判定依据 | 备注 |
|---|---:|---|---|---:|---|---|
| KDS-VU-01 | 5 | S2 | dry_run | 5×0.70 | RAG 导出、API smoke、GBrain search/query、wiki trust audit 在 local dev 通过（B 级）；tests pass | 本地 dev 通过，非真实 KDS API 同步 |
| KDS-VU-02 | 4 | S2 | fixture | 4×0.70 | F-017 tests/build pass；但登记在 kds 名下、证据在 SpaceAI 仓，账实不符；GPU/数据场地未排期 | 阶段计 S2，归属与证据位置待纠正 |
| KDS-VU-03 | 4 | S1 | dry_run | 4×0.40 | API contract dry-run 未落地；runtime index read-only check 未执行 | 契约未冻结 |
| KDS-VU-04 | 5 | S0 | none | 5×0.00 | 真实 KDS API 同步未授权；资金报告、sync-run 接收/归档仍待 owner 确认 | 授权未开，真实同步 0 批 |

- C_dev 算式：(5×0.70 + 4×0.70 + 4×0.40 + 5×0.00) / 18 = 0.4389 → **43.89%**（脚本值 43.89%）
- C_real 算式：(5×0.00 + 4×0.00 + 4×0.00 + 5×0.00) / 18 = 0.0000 → **0.00%**（脚本值 0.00%）
- 结论：手算与脚本一致；该项目 main_gap = F-017 归属与证据位置错位（证据在 SpaceAI 仓）；GPU/数据场地未排期；真实 API 同步未授权

### 4.4 抽样结论

- 三个项目的 C_dev / C_real 手算值与脚本值**逐位一致**（差异仅来自四舍五入）。
- 三个项目的 C_real 均为 0：XiaoC 全部证据为 PoC、GFIS 为 dry-run、KDS 为本地 dev/fixture，按 §2.5 纪律均不能计入真实口径。
- 阶段判定中最容易被高估的两处已收紧：XiaoC 的 WAME 侧裁定/发布虽然是"已裁定/发布"，但 governor 为 PoC → 保持 S2；KDS 的 F-017 虽 tests/build pass，但证据在 `GlobalCloud SpaceAI` 仓、归属登记为 kds（账实不符）→ 仍计 S2 并在 `notes` 记录归属待纠正。

---

## 5. 读数解读（对照 §2.2 估算与 90 天目标）

| 口径 | 首版（本台账，脚本） | 清单 §2.2 估算 | 90 天目标 | 差异说明 |
|---|---:|---:|---:|---|
| `C_dev` 开发口径 | **35.10%** | 31% | **55%** | +4.10pp：模板桩项目仍有 S1（系数 0.40）可计，6 个阻塞项目中多个有 tests/build pass（S2，系数 0.70），估算时按 ≈0.3 记偏低 |
| `C_real` 真实口径 | **0.00%** | 4% | **12%** | −4.00pp：§2.2 的 4% 来自 F-033 跨项目 PoC 运行证据；按 §1.2 纪律 PoC governor 最高 S2、不得进入 S4，收紧后真实口径归零，与"真实 source-of-record=0、客户验收=0"的事实一致 |

### 5.1 90 天口径（必须按此解读目标）

- **`C_dev` 目标 55%、`C_real` 目标 12%**，来源为《任务优先级清单》§2.2 与 §8 的 M6（Day 90）。当前首版为 `C_dev 35.10%`、`C_real 0.00%`。
- 距目标：`C_dev` 需 **+19.90pp**；`C_real` 需 **+12.00pp**，且必须至少 1 个项目进入 S4（§8 M6 原文）。
- **`C_real` 的任何提升只能来自真实 SOR**：按 §3 约束 C-D，真实客户/监管/交易单据不在项目群可控域内；工程侧能做的上限是"把项目推成 `development_ready_for_real_business_validation`（≈S3）"，不能自行制造 S4。
- 分母风险：PG-01 未落地前，dirty 仓数与项目群数仍存在多套口径；本文固定分母 28，若 PG-01 改变分母，本账本须整体重算。

### 5.2 结构性读数（与 `project-state.md` 一致）

- 28 项目形态：有实质进展 13 / 仅模板桩 9 / 阻塞 6；`C_dev` 最高的三个是 Studio 62.50%、XiaoC 56.88%、SpaceAIStudio 50.00%，最低的五个是 PVAOS 10.00%、SOP 10.00%、GPC 15.38%、WAE 14.55%、SLC 14.55%（均为模板桩或零证据）。
- 全群 0 条 S3+：最高阶段为 S2。这意味着**没有任何一个 VU 走到"evidence 包完整 + review 请求"**——与"10/23 活跃 Feature blocked、authorization_granted=0"的治理事实互为印证。
- 因此 `C_dev` 的提升瓶颈不在代码，而在**证据收口 + 复核请求**；`C_real` 的瓶颈是真实 SOR。

---

## 6. 复算与校验

```bash
# 1) Markdown 表（本文 §3 的原样来源）
python3 tools/kds-sync/render_project_group_completion.py

# 2) 机器可读 JSON
python3 tools/kds-sync/render_project_group_completion.py --json

# 3) 完整性校验（28 项目覆盖 / VU 数 3–5 / weight / stage / data_class / governor 纪律）
python3 tools/kds-sync/render_project_group_completion.py --check

# 4) 无 PyYAML 环境（内置极简解析器，结果应与 1/2 完全一致）
python3 tools/kds-sync/render_project_group_completion.py --no-pyyaml --json
```

本次校验记录（`--check` 原文）：

```text
summary: projects=28 vu_total=94 inferred=94 C_group_dev=0.3510 C_group_real=0.0000
result: PASS
```

- 校验项 15 项 PASS / 0 项 FAIL；失败时退出码为 1（已用故意破坏的临时台账验证：缺项目、VU 数越界、weight=9、fixture 进 S4 四类违规均被拦截）。
- PyYAML 与内置解析器的 `projects` / `group` 输出逐字段一致（已比对）。

---

## 7. 待人工确认事项

1. **C_dev 归一化口径**：把"S3 视为该口径 1.0"落地为 dev 系数 `min(w/0.50, 1.00)`，是否接受？（若改为按原权重算术平均，`C_dev` 上限为 50%，55% 目标将失去意义。）
2. **C_real 的 S4 计分**：S4 取原权重 0.70（本文选择）还是另行归一化，是否接受？
3. **项目权重 PW 分配**：主链核心 4–5 / 基础与知识 3–4 / 支撑与 external 2–3，合计 101，是否接受？
4. **首版 VU 边界与权重**：94 个 VU 的场景切分与 1–5 权重是否接受为基线？哪些 VU 需要拆分或合并？
5. **是否正式采纳本基线**：本文当前是 PG-02 首版产物，尚未经人工确认采纳；确认后方可作为后续周度复算的基准。

---

## 8. 非声明边界

- 本文与台账中的全部 94 条 VU 均为 `inferred: true` 的**估算**，不是受控事实、不是审计证据。
- 本文**不声明**任何项目的真实业务完成、客户验收、系统集成或生产就绪；不声明任何 VU 达到 S4 及以上（本次最高为 S2）。
- 本文**不构成**项目状态提升依据：`stage` 是台账估算值，不改变 `feature.yaml` / `runtime/queue.json` 的任何状态。
- 本文**不替代** §1.2 的模型定义；若模型变更，以清单为准并重算。
- 数据来源仅限本仓可读输入（`project-state.md`、`features/active/*/feature.yaml`、`config/project-group-projects.yaml`、`09-status/globalcloud-project-implementation-control-register.md`、各项目 `STATUS.md` 与证据目录清单）；未读取任何项目仓的业务数据。

## 2026-10-23 修正记录（append-only）

- 修正：移除 `runtime/vu-ledger.yaml` 中重复的 `KDS-VU-02`（CWME/F-017 证据在 SpaceAI 仓、登记在 KDS 名下；F-017 已归属 `spaceai`）。
- 复算：VU 97（inferred 97）、项目 29、项目权重和 105。
- 新读数：**C_dev = 35.58%｜C_real = 0.00%**（由 `render_project_group_completion.py` 生成，无手工填数）。
- 本文 v1.0 的历史读数（94 VU / 28 项目 / 35.10%）保留为当时事实，不覆盖。
