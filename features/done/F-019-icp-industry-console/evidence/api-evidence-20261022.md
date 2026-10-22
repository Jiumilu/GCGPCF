---
doc_id: GPCF-DOC-CAD81A3AC4
title: F-019 API 证据（2026-10-22 补采）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-019-icp-industry-console/evidence/api-evidence-20261022.md
source_path: features/done/F-019-icp-industry-console/evidence/api-evidence-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-019 API 证据（2026-10-22 补采）

- 采集时间：2026-10-22T07:09:43+08:00
- 采集方式：本地真机 HTTP 探活（自动启动 `gc_icp.api:app`，探测完成后关闭）
- 证据性质：**本地只读候选运行时证据**（`evidence_class: local_read_only_http_probe`），可复算
- 机器可读原文：`evidence/api-evidence-20261022.json`
- 判定：`api: pass`（仅就已采集的本地只读面而言）

## 0. 边界（先读）

- 只访问 `127.0.0.1:8091` 本地候选运行时的**一期只读 GET 面** + CORS/OPTIONS 预检。
- **不做**真实外部 API、真实 KDS API、真实业务源（客户/工厂/平台单据）调用；不写任何业务数据。
- 本次证据**不代表**真实业务接入，**不构成**项目状态提升（`status_ceiling: partial` 不变）。

## 1. 复跑环境

| 项 | 值 |
|---|---|
| 采集机 Python | 3.9.6 |
| fastapi / uvicorn | 0.128.8 / 0.39.0 |
| ICP 仓 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud ICP` |
| ICP HEAD | `80b8aaa`（2026-10-14 09:53:28 +0800） |
| 监听 | `127.0.0.1:8091`（server origin = `started_by_probe`） |
| 启动耗时 | 1.597s |

## 2. 探针结果（本轮真跑：7/7 通过）

| 检查 | URL | HTTP | 结果 | 关键断言（实际值） |
|---|---|---:|---|---|
| GET health（候选态边界） | `http://127.0.0.1:8091/api/v1/health` | 200 | PASS | status_code=200; status=candidate; overallStatus=partial; confirmationStatus=human_required; productionReady=False; noWriteAssertion=True; industryNodeCount=24; poolCount=11; scenarioCount=3 |
| GET industry-model（24 节点） | `http://127.0.0.1:8091/api/v1/industry-model` | 200 | PASS | status_code=200; len(nodes)=24 |
| GET resource-pools（11 池·projectionOnly） | `http://127.0.0.1:8091/api/v1/resource-pools` | 200 | PASS | status_code=200; projectionOnly=True; len(pools)=11 |
| GET scenarios（3 受控场景） | `http://127.0.0.1:8091/api/v1/scenarios` | 200 | PASS | status_code=200; status=candidate; len(scenarios)=3 |
| GET constitution-governance（5 角色·KDS canonical） | `http://127.0.0.1:8091/api/v1/constitution-governance` | 200 | PASS | status_code=200; domainOwner=ICP; canonicalCustodian=KDS; noWriteAssertion=True; len(roles)=5 |
| GET health + Origin（CORS 放行 WAE 宿主） | `http://127.0.0.1:8091/api/v1/health` | 200 | PASS | status_code=200; access-control-allow-origin=http://localhost:4300 |
| OPTIONS health 预检（只读：GET/OPTIONS） | `http://127.0.0.1:8091/api/v1/health` | 200 | PASS | status_code=200; allow-methods 含 GET/OPTIONS=GET, OPTIONS |

## 3. 逐字复跑命令

```bash
# 探针（自启/复用 :8091，只读检查，不落盘）
cd "GlobalCoud GPCF" && python3 features/active/F-019-icp-industry-console/evidence/check_icp_api.py --check-only

# 落盘 JSON 证据
cd "GlobalCoud GPCF" && python3 features/active/F-019-icp-industry-console/evidence/check_icp_api.py \
  --out features/active/F-019-icp-industry-console/evidence/api-evidence-20261022.json
```

## 4. 测试与契约校验（同一轮真跑，逐字输出）

### 4.1 单元测试

```text
test_rejects_missing_node (test_validate_industrial_chain_closure.IndustrialChainClosureValidatorTest) ... ok
test_rejects_missing_required_control_asset (test_validate_industrial_chain_closure.IndustrialChainClosureValidatorTest) ... ok

----------------------------------------------------------------------
Ran 33 tests in 5.005s

OK
```

exit_code = 0

### 4.2 契约门禁 `scripts/validate_gc_icp.py`

```text
gc_icp_contract_gate=pass
industry_nodes=24 pools=11 resource_fact_pools=10 rule_orchestration_pools=1 scenarios=3
status=candidate overall_status=partial confirmation_status=human_required production_ready=false
constitution_domain_owner=ICP canonical_custodian=KDS amendment_status=candidate no_write=true
```

exit_code = 0

### 4.3 产业链闭环校验 `scripts/validate_industrial_chain_closure.py`

```text
OK: GC-ICP industrial-chain controls are consistent (nodes=6, assets=15)
```

exit_code = 0

## 5. 结论

- 5 个只读 GET（health / industry-model / resource-pools / scenarios / constitution-governance）全部 200，断言成立：24 节点、11 资源池（`projectionOnly=true`）、3 受控场景、5 治理角色、`domainOwner=ICP`、`canonicalCustodian=KDS`。
- 候选态边界成立：`status=candidate`、`overallStatus=partial`、`confirmationStatus=human_required`、`productionReady=false`、`noWriteAssertion=true`。
- CORS 边界成立：带 `Origin: http://localhost:4300` 的 GET 返回对应 `access-control-allow-origin`；OPTIONS 预检 200 且 `allow-methods` 仅 `GET, OPTIONS`（一期只读）。
- 单元测试通过；两个契约校验 exit_code 均为 0（见上）。

## 6. 历史治理备注（2026-10-22 复核后不再构成阻塞）

原 `feature.yaml.blockers` 中两条为过程记录，复核后不构成阻塞，已移出 blockers 并保留于此：

1. 「全仓 typecheck 曾现他线红点（后由其修复；我方文件全绿）」——他线已修复，F-019 范围文件无红点。
2. 「queue.json/state.json 经官方函数刷新（enqueue 自动）」——入队机制说明，非阻塞项。

本 Feature 的 `runtime/queue.json` 条目仍为旧状态（`blocked / Evaluator`）：本轮**未**调用官方 dispatch/update 函数刷新，也未做任何状态提升。

## 7. 未采集 / 仍缺的证据（如实记录）

- 真实外部业务源（订单/工厂/监管单据）接入证据：**仍缺**（一期只读，不在本 Feature 范围）。
- 多用户可用性与无障碍门禁：`pending / waived`，未在本次补采。
- 真实 KDS API 同步：未授权，未调用。
