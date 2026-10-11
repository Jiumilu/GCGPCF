---
doc_id: GPCF-F-017-JOURNAL-CWME-CITY-WORLD-MODEL-ENGINE
title: journal
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-017-cwme-city-world-model-engine/journal.md
source_path: features/active/F-017-cwme-city-world-model-engine/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

## 2026-10-11 · 立项与启动（老卢点名）

- 老卢拍板「启动」（原话："4、启动"）：立项编号 **F-017**；启动时间＝**2026-10-11**（决策清单 D4 执行）。
- 决策清单快照（v2.1 §九）：D1 产品命名「万象引擎」**待确认**；D2 图存储 **Neo4j**（推荐已定）；D3 样板体系（城市级旗舰=光谷真实城市；行业=黄梅/当阳/校园群，按节奏）；D4 启动时间＝**已执行（2026-10-11）**；D5 团队**最小启动**（1 核心＋AI 打底）；D6 首个演示对象**待确认**（内部跑通→对外普适）。
- 协同：本项目 B4-1/B4-2 初版件＝《域包登记申请》申请一（CWME 空间域扩展包登记）前置；与 F-016（WAM）经 `crosswalk-工业绿链×CWME v0.1` 对接（**不交叉写账**）。
- 语义契约：本体工具链与 WAS 侧共用基线（Protégé＋pySHACL，见《WAS×CWME 协同方案》R6/M1）。
- 边界：无生产/发布/接受声明；`accepted=false / integrated=false / production_ready=false`。
- 启动记录（KDS）：`世界资产/世界模型引擎/2026-10-11_CWME项目启动记录.md`

## 2026-10-11 · B4-1/B4-2 初版件产出 + 申请一提交
- B4 初版件（KDS `世界资产/世界模型引擎/ontology/`）：`cwme-ext.ttl`（**199 triples/33 类/22 对象属性**）＋`cwme-mapping-v1.yaml`（spaceai.db **40 表**全量处置＋关系数据线索）＋`cwme-shapes-min.ttl`（4 形状）＋样例×2＋`verify_ontology.py`。
- 验证（rdflib 7.6.0＋pyshacl 0.40.1 实跑）：合规样例 conforms=True；违规样例 **5 项全检出**。
- **申请一（CWME 城市空间域扩展包 → WAS-Ontology 登记）已提交** GPCF（`docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.*`＋loop＋validator；`current_decision=pending`）。
- 至此随老卢"1、提交／4、启动"的三个登记请求（XWAIL Profile／业务域／CWME 域包）**全部入库**。

## 2026-10-11 · B4-3 生成器 PoC（单一事实源链路）
- 产出：`ontology/cwme_gen.py`（本体→4 类产物）＋`verify_generated.py`（CI 门禁雏形）＋`generated/`（ts/sql/cypher/vocab＋manifest）。
- 验收（"改本体一个字段→全仓生成物同步"）：① 确定性双跑**逐字节一致**；② `tsc --noEmit` OK；③ SQLite 执行 **33 表** OK；④ **演示**：副本本体加 `Camera.resolution` → 重生成后 TS/SQL 同步出现该字段（基线 0 处）✓。
- 细节：`DeviceHasStatus` 枚举由 SHACL `sh:in` 派生进 TS 类型；SQL 对设备链自动加 CHECK；锚类通用关系不进表结构（走关系层）。

## 2026-10-11 · B4-4 Neo4j 落地 PoC（端到端）
- 本机容器 `cwme-neo4j`（neo4j:5 / 5.26.31 community；:7474/:7687）。
- 产出：`ontology/neo4j/`——`sync_sample.py`（spaceai.db 只读→加载脚本）＋`sample-load.cypher`＋`verify_queries.cypher`＋`verify-output.txt`＋README。
- **实跑：888 节点 / 914 关系 / 36 约束 / 0 错误**；场景抽检全真实返回（居住区报警链、文波楼 40 设备、5 条巡更线、门禁事件、相机 40）。
- 生成↔落库差异 10 条均为语义正确（8 无效引用＋2 去重）；约束内联本体生成物（设计层→运行层联动）。
