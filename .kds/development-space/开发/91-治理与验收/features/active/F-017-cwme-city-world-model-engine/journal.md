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

## 2026-10-11 · B4-5 CI 门禁（**F-017 首月件收口**）
- `ontology/ci-gate.sh`（五步门禁：本体/SHACL → 防漂移 → 生成物回验 → 加载脚本 → Neo4j 在线）＋`ontology/.venv`（持久化，验证环境脱离临时目录）＋GPCF `tools/kds-sync/validate_cwme_ontology_chain.py`（静态轻检 + `--deep`）。
- 实跑：ci-gate **5/5 PASS**；validator 轻检 + deep **pass**。
- **反例实证**：改本体不重生成 → 双重拦截（validator `source drift` FAIL；ci-gate 防漂移步 FAIL=1→EXIT 2）；恢复后全绿——"改本体→必须重生成→CI 才绿"链路闭环。
- **F-017 首月件 B4-1—B4-5 全部完成**（映射表/扩展本体/SHACL/生成器/Neo4j/CI 门禁）。

## 2026-10-11 · B4 深化（40 表全量 + 增量机制）
- `sync_graph.py`（neo4j/）：**31 张受管表**全量生成 + 行级哈希增量 + check 三模式；`full-load.cypher`（3908 行）+ `sync-state.json` 基线。
- 全量导入：**1503 节点 / 1960 关系 / 0 错误**（较 B4-4 样例 +615 节点 +1046 关系）；字典四套挂钩、模型/视角/用户/地物/GPS 全入图。
- **增量实证**（副本库、零删除）：改 1 + 增 1 + 幻影删 1 → check **三类漂移全检出**（exit 2）→ 增量脚本 4 语句（removed 零删除报告）→ 复查 **in_sync**。
- **ci-gate 升级 6 步**（+full 防漂移、+源-基线一致性）→ **6/6 PASS**。
- 缺陷修复：两段式语句顺序（节点段→关系段）——首轮前向引用致约 500+ 关系落空，修正后全部补齐（1960 与理论值对账一致）。

## 2026-10-11 · D1/D6 确认（按建议）
- D1 命名「万象引擎」、D6 首个演示对象「光谷」——按老卢「按建议执行」确认（启动记录＋feature.yaml 已更新）。
