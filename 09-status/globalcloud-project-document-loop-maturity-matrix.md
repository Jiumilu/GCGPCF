---
doc_id: GPCF-DOC-C10C271958
title: GlobalCloud 项目文档完整度与 Loop 成熟度量化矩阵
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-document-loop-maturity-matrix.md
source_path: 09-status/globalcloud-project-document-loop-maturity-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 项目文档完整度与 Loop 成熟度量化矩阵

日期：2026-06-13

用途：将 12 个项目的基本文档体系、Loop 覆盖情况和量化成熟度收口到同一张表，作为下一轮 Loop 初始化和补债顺序依据。

## 评分规则

| 指标 | 说明 | 分值 |
|---|---|---:|
| Manifest | 项目 Manifest 已建立或已有基础 | 14 |
| loop-state | `docs/harness/loop-state.md` 或等价状态记录已建立 | 14 |
| 项目主线/架构边界 | 有项目级主线、架构或边界文档 | 14 |
| evidence/证据目录 | 有项目级 evidence 或样本输入 | 14 |
| 验收/状态审计 | 有验收、状态审计或 Harness 证据 | 14 |
| 项目文档数量 | 直接归属文档数，最多 10 分 | 10 |
| KDS 空间落位 | KDS 项目空间已有镜像文档 | 10 |

成熟度：L0 未进入 Loop；L1 有基础但未 loop_ready；L2 已进入微循环；L3 证据接近可审计；L4 已进入审计/验收；L5 已通过验收或集成。

## 12 项目量化矩阵

| 项目 | 代号 | 文档数 | KDS文档 | Manifest | loop-state | 架构边界 | evidence | 验收审计 | 完整度分 | Loop成熟度 | 当前状态 | 主要缺口 | 下一步 |
|---|---|---:|---:|---|---|---|---|---|---:|---|---|---|---|
| GFIS | GF | 14 | 14 | 是 | 是 | 是 | 是 | 否 | 76 | L3：证据接近可审计 | partial | 验收/状态审计；现场真实样本尚未提交；业务 UAT 尚未由工厂/生产/质量/仓储/GPC/WAES 角色签收；生产环境确认和外部联调仍缺；`127.0.0.1:8080` 被本机 Python/uvicorn 占用；迁移窗口未授权；所有 received/signed/confirmed 均为 false | 建立签收证据接收后的审计准备规则；仍不执行 `bench migrate`、schema sync、写 API 或外部联调 |
| GPC | GP | 31 | 25 | 待人工蓝图确认 | 是 | 是 | 是 | 是 | 76 | L2：已进入微循环 | partial | Manifest 与一期蓝图需人工确认；目标平台骨架尚未形成可验收实现；`GPCF-GP-LR-002` 已完成蓝图授权边界核对 | 授权后补齐 Manifest、一期蓝图和真实项目仓验证 |
| PVAOS | PV | 4 | 3 | 是 | 是 | 否 | 是 | 否 | 46 | L2：已进入微循环 | partial | 真实 PVAOS 项目仓未确认；门户底座；平台运营对象；租户/伙伴/组织能力验证；`GPCF-PV-LR-002` 已完成清单 | 授权后进入真实 PVAOS 项目仓或运行态验证 |
| WAES | WA | 121 | 11 | 是 | 是 | 是 | 是 | 是 | 78 | L2：已进入微循环 | partial | WAES 真实项目仓未确认；门禁语义确认；验收审计；AI 越权控制和状态裁决验证；`GPCF-WA-LR-002` 已完成清单 | 授权后进入 WAES 门禁语义和真实裁决链路验证 |
| KDS | KD | 45 | 39 | 是 | 是 | 是 | 是 | 否 | 80 | L2：已进入微循环 | partial | 真实 KDS 项目仓已落地最小 Loop harness 和 validator；知识对象映射、运行态索引健康、KDS API contract、Brain/PKC 依赖验证、验收/状态审计仍未完成 | 授权后推进 KDS runtime index read-only check、API contract dry-run 或 Git 提交推送 |
| Brain | BR | 9 | 3 | 是 | 是 | 否 | 是 | 否 | 52 | L2：已进入微循环 | partial | 真实 Brain 项目仓已落地 `.env` 敏感文件门禁、最小 Loop harness、validator 和 ESLint 9 flat config；`pnpm lint` 通过但有 16 个 warning，`pnpm format:check` 有 68 个既有格式缺口；缺 test script；知识编制对象、知识 UI 边界、模型路由、KDS 依赖和验收/状态审计仍未完成 | 授权后推进 Brain format/test script/lint warning 专项，或建立知识编制对象、知识 UI 边界、模型路由与 KDS 依赖映射清单 |
| PKC | PK | 9 | 3 | 是 | 是 | 是 | 是 | 否 | 62 | L2：已进入微循环 | partial | 真实 PKC 项目仓已落地最小 Loop harness、validator、测试与 typecheck 修复；个人知识对象、端到端用户闭环、KDS/Brain 依赖和体验验证仍未完成；验收/状态审计未完成 | 授权后推进 PKC workflow dry-run、KDS/Brain dependency dry-run 或 Git 提交推送 |
| XiaoC | XC | 67 | 61 | 是 | 是 | 是 | 是 | 是 | 92 | L2：已进入微循环 | partial | 真实 XiaoC 项目仓已落地最小 Loop harness 和 validator；UI 测试、Wrangler、模型路由、真实部署证据仍未闭合 | 授权后推进 XiaoC 模型路由、AI 能力生产、编排链路、UI 超时测试或 Wrangler/部署验证 |
| XGD | XD | 9 | 3 | 是 | 是 | 是 | 是 | 否 | 62 | L2：已进入微循环 | partial | 真实 XGD 项目仓已落地最小 Loop harness 和 validator；长程 Agent、重分析、多端交互、Brain UI/ACUI、外部渠道和验收/状态审计仍未完成 | 授权后推进 XGD TICK loop dry-run、Brain UI/ACUI smoke 或 Git 提交推送 |
| XiaoG | XG | 4 | 3 | 是 | 是 | 否 | 是 | 否 | 46 | L2：已进入微循环 | partial | 真实 XiaoG 项目仓未确认；设备/语音接入；GFIS/WAES 触发链路；真实设备验证；`GPCF-XG-LR-002` 已完成清单 | 授权后进入真实设备/语音触发链路验证 |
| MMC | MM | 5 | 4 | 是 | 是 | 否 | 是 | 否 | 48 | L2：已进入微循环 | partial | 真实 MMC 项目仓未确认；治理模板字段字典；模板复用验证清单未进入真实仓；验收/状态审计 | 授权后进入真实 MMC 项目仓或新一轮 L3/L4 |
| GPCF | CF | 136 | 93 | 是 | 是 | 是 | 是 | 是 | 94 | L3：证据接近可审计 | partial | KDS Token 已 pass；Git dirty；本轮仅完成 Brain ESLint 9 flat config 1 个实质轮次；GPC 一期蓝图、WAES 门禁语义、accepted/integrated、Git push/PR merge 均未授权 | 需用户授权继续 Brain format/test script/lint warning 专项、XiaoC 模型路由/UI/Wrangler 专项、Git commit/push 或更高自治模式 |

## 总体判定

- 12 项目平均文档完整度：66.5/100。
- 文档完整度 >=80 的项目数：2/12。
- Loop 成熟度 L0 项目数：0/12。
- Loop 成熟度 L1 项目数：0/12。
- Loop 成熟度 L2 及以上项目数：12/12。

## 执行结论

1. KDS 项目空间已经建立，12 项目均已纳入项目级 Loop 记录入口，但项目级基本文档体系仍未全量完善。
2. Loop 机制已经覆盖 12 个项目；本轮按新真实性规则只完成 Brain ESLint 9 flat config 1 个实质轮次，收口原因为 `authorization_boundary`。
3. 当前量化体系已经具备可计算指标，下一步必须在授权后进入真实项目仓、运行态验证、蓝图确认或 Git 提交推送，而不能继续只做总控文档补债。

## 下一轮补齐顺序

1. GFIS：已完成 `GPCF-GF-LR-030` UAT 问题处置闭环和豁免复核规则，金融事实保持 L4 阻断，下一步建立签收证据接收后的审计准备规则。
2. GPCF：KDS Token 上线同步门禁已完成；本轮按新真实性规则只完成 Brain ESLint 9 flat config 1 个实质轮次；下一步需用户授权继续 Brain format/test script/lint warning 专项、XiaoC 模型路由/UI/Wrangler 专项、Git commit/push 或更高自治模式。
3. MMC：已完成二轮治理模板字段字典与模板复用验证清单，下一轮需授权进入真实 MMC 项目仓或验收审计。
4. KDS：已完成真实项目仓最小 Loop harness 和 validator；下一轮可进入 runtime index read-only check、API contract dry-run 或 Brain/PKC 依赖证据补齐。
5. Brain：真实项目仓已补齐 `.env` 敏感文件门禁、最小 Loop harness 和 ESLint 9 flat config；下一轮优先处理 format check、test script 或 16 个 lint warning，或建立知识编制对象、知识 UI 边界、模型路由与 KDS 依赖映射清单。
6. PKC：已完成真实项目仓最小 Loop harness、项目级 validator、测试和 typecheck 修复；下一轮可进入 workflow dry-run、KDS/Brain dependency dry-run 或体验证据补齐。
7. XiaoC：真实项目仓最小 Loop harness 已落地；下一步补齐测试、部署和模型路由证据，不自动升级 accepted/integrated。
8. GPC、PVAOS、WAES、XGD、XiaoG：GPC/PVAOS/WAES/XiaoG 已完成第二轮清单；XGD 已完成真实仓最小 Loop harness，后续需要运行态 dry-run 与 Brain UI/ACUI evidence；不得越权改蓝图、部署、生产配置或 accepted/integrated。
