---
doc_id: GPCF-DOC-F6D2D165A7
title: Headroom LCX Controlled Package Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-controlled-package-20260621.md
source_path: docs/harness/evidence/headroom-lcx-controlled-package-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX Controlled Package Evidence

## Evidence ID

`HEADROOM-LCX-CONTROLLED-PACKAGE-20260621`

## 结论

本 evidence 证明 Headroom LCX 受控能力包已经落地到 `loop/context/headroom/`，覆盖 15 个项目/域，并具备 Proxy、SDK、MCP、Agent Wrap、CCR、Working Memory、Learn preview、Output Shaper profile 的受控配置。

本 evidence 不证明生产代理、真实生产 token 节省、真实 KDS 写入、真实外部 API 写入、accepted、integrated 或 production_ready。

## 覆盖范围

```text
GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS
```

## 关键产物

| 类别 | 路径 |
|---|---|
| 能力包 README | `loop/context/headroom/README.md` |
| Route policy | `loop/context/headroom/policy.yaml` |
| Config schema | `loop/context/headroom/config.schema.yaml` |
| Compression profiles | `loop/context/headroom/compression-profiles.yaml` |
| MCP config | `loop/context/headroom/mcp.json` |
| Proxy env example | `loop/context/headroom/proxy.env.example` |
| Harness evidence schema | `loop/context/headroom/harness/evidence.schema.yaml` |
| Harness metrics schema | `loop/context/headroom/harness/metrics.schema.yaml` |
| WAES policy | `loop/context/headroom/waes/headroom-policy.yaml` |
| CCR retrieve gate | `loop/context/headroom/waes/ccr-retrieve-gate.yaml` |
| KDS component | `loop/context/headroom/kds/context-optimization-component.yaml` |
| Validator | `tools/kds-sync/validate_headroom_lcx_controlled_package.py` |

## 门禁

| 门禁 | 当前状态 |
|---|---|
| project_route_count | 15 |
| all_projects_have_routes | true |
| proxy_configured | true |
| sdk_configured | true |
| mcp_configured | true |
| agent_wrap_configured | true |
| ccr_retrieve_gate_configured | true |
| harness_evidence_schema_configured | true |
| waes_policy_configured | true |
| kds_candidate_component_configured | true |
| telemetry_default_off | true |
| learn_apply_auto | false |
| cross_project_memory_as_fact | false |
| production_admission_gate | false |
| measured_production_tokens | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 检查命令

```bash
python3 tools/kds-sync/validate_headroom_lcx_controlled_package.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 下一轮

`GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001`：在不进入生产、不写真实 TOKEN、不处理未脱敏材料的前提下，对 LCX 受控能力包执行 runtime replay。
