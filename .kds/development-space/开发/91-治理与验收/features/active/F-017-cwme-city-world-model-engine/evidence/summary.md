---
doc_id: GPCF-DOC-F017-CWME-EVIDENCE-20261011
title: F-017 证据摘要（B4 首月件 B4-1—B4-5 验收）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-017-cwme-city-world-model-engine/evidence/summary.md
source_path: features/active/F-017-cwme-city-world-model-engine/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# F-017 证据摘要（B4 首月件 B4-1—B4-5 验收）

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于条目验收判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass（ci-gate 5/5；GPCF validator 轻检 + `--deep`；2026-10-11）
- build: pass（生成器/加载器/门禁实跑；KDS `0fbf5290` / GPCF `bb6591bb2` 已提交并推送）
- screenshots: waived（本体/生成物/图库，无 UI 变更）
- api: waived（本地只读文件 + 本机容器）
- lint: 脚本纯标准库 + rdflib/pyshacl；产物经 `tsc --noEmit` 与 SQLite 执行验证
- risk: 未授权项列明——无生产承诺、无 WAES 发布、无跨项目写账、无对外发送
<!-- GPCF_EVIDENCE_GATE_END -->

## 一、B4 首月件验收矩阵
| 任务 | 交付物（KDS `世界资产/世界模型引擎/ontology/`） | 验收证据（实跑） | 状态 |
|---|---|---|---|
| B4-1 映射表 | `cwme-mapping-v1.yaml`（spaceai.db 40 表全量处置＋关系数据线索） | 只读盘点：176 元素/168 设备/200 报警/40 相机/45 点位 | ✅ |
| B4-2 扩展本体 | `cwme-ext.ttl`（199 triples/33 类/22 对象属性）＋`cwme-shapes-min.ttl` | rdflib 7.6.0 + pyshacl 0.40.1：正例通过、负例 5 项全检出 | ✅ |
| B4-3 生成器 | `cwme_gen.py`＋`generated/`（TS/SQL/Cypher/vocab＋manifest） | 双跑逐字节一致；`tsc --noEmit` OK；SQLite 33 表执行；改字段全链同步演示 | ✅ |
| B4-4 Neo4j 落地 | `neo4j/`（sync_sample.py＋加载脚本＋验证查询）＋容器 `cwme-neo4j` | **888 节点/914 关系/36 约束/0 错误**；7 项场景查询真实返回 | ✅ |
| B4-5 CI 门禁 | `ci-gate.sh`＋GPCF `validate_cwme_ontology_chain.py`＋`ontology/.venv` | **5/5 PASS**；反例实证双层拦截（source drift＋防漂移步） | ✅ |
| 前置登记 | 申请一（域包登记） | `docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.*`，附件 3/3 验证 | ✅ 已提交（decision 待治理方） |

## 二、一键复核（复核操作）
```bash
cd "…/GlobalCloud KDS/世界资产/世界模型引擎/ontology"
./ci-gate.sh                     # 五步门禁 → 期望 PASS=5 SKIP=0 FAIL=0
cd "…/GlobalCoud GPCF"
python3 tools/kds-sync/validate_cwme_ontology_chain.py --deep    # → pass（deep=pass）
```

## 三、关键数字
- 本体：**199 triples / 33 类 / 22 对象属性 / 1 枚举**（`DeviceHasStatus`，由 SHACL `sh:in` 派生）
- 生成物：4 产物 ＋ `GEN_MANIFEST.json`（sha256 全对、无时间戳=确定性）
- 图：**888 节点 / 914 关系 / 36 约束 / 0 错误**（生成↔落库差异 10 条均为语义正确：8 无效引用＋2 去重）
- 门禁：五步全绿；**反例双层拦截**（改本体不重生成 → validator `source drift` FAIL；ci-gate 防漂移步 FAIL）

## 四、未覆盖（如实保留）
- **B4 深化项**：40 表全量同步、增量机制、列级映射补全（未开始）
- **B5**（Studio/MMC 接入）未启动；人员时间与逐对象授权属业务侧
- D1 命名「万象引擎」、D6 首个演示对象待确认（不阻塞）
- 申请一 `current_decision=pending_governance_review`（decision 属治理方）

## 五、登记与提交
- KDS 提交链（本阶段）：`2c666f8d` → `dd331492` → `def5a4a6` → `0fbf5290`
- GPCF 提交链（本阶段）：`8e890ec35` → `62074e546` → `4f729b39a` → `bb6591bb2`
- journal：`features/active/F-017-cwme-city-world-model-engine/journal.md`（B4 四节记录）
- 边界：以上为**本地可回放证据**；不构成治理结论或状态提升。

## 六、B4 深化追加（2026-10-11）
- `sync_graph.py`：31 张受管表全量 + 行级哈希增量 + check；`full-load.cypher` + `sync-state.json`。
- 全量：**1503 节点 / 1960 关系 / 0 错误**；增量实证（副本、零删除）：改/增/幻影删三类漂移全检出 → 增量脚本 4 语句 → 复查 in_sync。
- ci-gate 升级 **6 步**（+full 防漂移、+源-基线一致性）→ 6/6 PASS。
- 复核命令更新：
```bash
./ci-gate.sh                     # 六步门禁 → 期望 PASS=6 SKIP=0 FAIL=0
python3 tools/kds-sync/validate_cwme_ontology_chain.py --deep    # → pass
```
