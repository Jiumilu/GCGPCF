---
doc_id: GPCF-DOC-BA63F9BF32
title: KDS 开发空间同步台账
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/kds-development-space-sync-register.md
source_path: 09-status/kds-development-space-sync-register.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# KDS 开发空间同步台账

日期：2026-06-12

用途：登记 Git 文档与 KDS `开发` 空间的双向同步映射。当前实现为仓库内 `.kds/development-space/开发` 本地镜像，后续可替换为真实 KDS API。

## 范围说明

当前台账覆盖的是 **GPCF 仓库中已经纳入 KDS `开发` 空间的文档镜像**。其它项目的真实项目仓库文档，只有在后续从对应项目仓导入或同步到本仓/KDS 后，才会出现在本台账中。

其它项目当前在 KDS 中的位置如下：`开发/01-GFIS`、`开发/02-GPC`、`开发/03-PVAOS`、`开发/04-WAES`、`开发/05-KDS`、`开发/06-Brain`、`开发/07-PKC`、`开发/08-XiaoC`、`开发/09-XGD`、`开发/10-XiaoG`、`开发/11-MMC`、`开发/12-GPCF`。跨项目文档主要在 `开发/90-跨项目架构`、`开发/91-治理与验收`、`开发/92-证据与会话归档`。

## 12 项目文档总量统计

| project | kds_project_folder | project 字段文档数 | KDS 项目空间文档数 | 说明 |
| --- | --- | --- | --- | --- |
| GFIS | 01-GFIS | 1 | 1 | 已建空间 |
| GPC | 02-GPC | 27 | 22 | 已建空间 |
| PVAOS | 03-PVAOS | 0 | 0 | 已建空间，暂无直接镜像文档 |
| WAES | 04-WAES | 108 | 8 | 已建空间 |
| KDS | 05-KDS | 39 | 39 | 已建空间 |
| Brain | 06-Brain | 0 | 0 | 已建空间，暂无直接镜像文档 |
| PKC | 07-PKC | 0 | 0 | 已建空间，暂无直接镜像文档 |
| XiaoC | 08-XiaoC | 58 | 58 | 已建空间 |
| XGD | 09-XGD | 0 | 0 | 已建空间，暂无直接镜像文档 |
| XiaoG | 10-XiaoG | 0 | 0 | 已建空间，暂无直接镜像文档 |
| MMC | 11-MMC | 0 | 0 | 已建空间，暂无直接镜像文档 |
| GPCF | 12-GPCF | 81 | 41 | 已建空间 |

## KDS 公共空间文档统计

| kds_public_folder | meaning | document_count |
| --- | --- | --- |
| 00-项目群总控 | 项目群总入口与根 README | 1 |
| 90-跨项目架构 | 跨项目架构、主线、数据/知识跨域文档 | 31 |
| 91-治理与验收 | 治理、验收、状态、台账与门禁文档 | 35 |
| 92-证据与会话归档 | Harness、证据样本、历史会话与归档文档 | 78 |
| 99-过期文档 | deprecated / superseded 文档 | 0 |

## 全量同步清单

| doc_id | git_source | kds_path | sync_direction | kds_api_status |
| --- | --- | --- | --- | --- |
| GPCF-DOC-56E7A7A3B5 | .codex/README.md | 开发/12-GPCF/.codex/README.md | register_and_mirror | pending_api |
| GPCF-DOC-424C591653 | .codex/skills/README.md | 开发/12-GPCF/.codex/skills/README.md | register_and_mirror | pending_api |
| GPCF-DOC-B053B83539 | .codex/skills/globalcloud-document-governance/README.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/README.md | register_and_mirror | pending_api |
| GPCF-DOC-346B3F6F08 | .codex/skills/globalcloud-document-governance/SKILL.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/SKILL.md | register_and_mirror | pending_api |
| GPCF-DOC-6261F5EFD4 | .codex/skills/globalcloud-document-governance/references/README.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/README.md | register_and_mirror | pending_api |
| GPCF-DOC-D02AC375B5 | .codex/skills/globalcloud-document-governance/references/anti-pollution-rules.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/anti-pollution-rules.md | register_and_mirror | pending_api |
| GPCF-DOC-03FB1D644C | .codex/skills/globalcloud-document-governance/references/document-control-policy.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/document-control-policy.md | register_and_mirror | pending_api |
| GPCF-DOC-AAE22480F8 | .codex/skills/globalcloud-document-governance/references/kds-security-policy.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/kds-security-policy.md | register_and_mirror | pending_api |
| GPCF-DOC-DB96D52951 | .codex/skills/globalcloud-document-governance/references/loop-integration-policy.md | 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/loop-integration-policy.md | register_and_mirror | pending_api |
| GPCF-DOC-268058F0F6 | .codex/skills/ui-ux-pro-max/README.md | 开发/12-GPCF/.codex/skills/ui-ux-pro-max/README.md | register_and_mirror | pending_api |
| GPCF-DOC-8025BD5C10 | .codex/skills/ui-ux-pro-max/SKILL.md | 开发/12-GPCF/.codex/skills/ui-ux-pro-max/SKILL.md | register_and_mirror | pending_api |
| GPCF-DOC-D1E79591EA | .harness/README.md | 开发/92-证据与会话归档/.harness/README.md | bidirectional | pending_api |
| GPCF-DOC-32ED2727B9 | .harness/runs/README.md | 开发/92-证据与会话归档/.harness/runs/README.md | bidirectional | pending_api |
| GPCF-DOC-C311AFC61A | .harness/runs/gbrain-admin-console-v1-20260610-201442/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-admin-console-v1-20260610-201442/README.md | bidirectional | pending_api |
| GPCF-DOC-9AF8C291EB | .harness/runs/gbrain-admin-console-v1-20260610-201442/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-admin-console-v1-20260610-201442/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-4609775857 | .harness/runs/gbrain-admin-console-v1-20260610-201442/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-admin-console-v1-20260610-201442/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-6A1A3247B5 | .harness/runs/gbrain-admin-console-v2-20260610-205407/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-admin-console-v2-20260610-205407/README.md | bidirectional | pending_api |
| GPCF-DOC-44D60534C4 | .harness/runs/gbrain-admin-console-v2-20260610-205407/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-admin-console-v2-20260610-205407/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-2C07E0A2D0 | .harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/README.md | bidirectional | pending_api |
| GPCF-DOC-210BFA30D4 | .harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-8352F39CCF | .harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-83A23A2605 | .harness/runs/gbrain-portal-v1-20260610-200455/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-portal-v1-20260610-200455/README.md | bidirectional | pending_api |
| GPCF-DOC-DBC5316C7C | .harness/runs/gbrain-portal-v1-20260610-200455/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-portal-v1-20260610-200455/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-EA8925961C | .harness/runs/gbrain-portal-v1-20260610-200455/proposal.md | 开发/92-证据与会话归档/.harness/runs/gbrain-portal-v1-20260610-200455/proposal.md | bidirectional | pending_api |
| GPCF-DOC-AD7D575AD9 | .harness/runs/gbrain-portal-v1-20260610-200455/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-portal-v1-20260610-200455/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-4B629FE0E5 | .harness/runs/gbrain-portal-v2-frontend-20260610-204915/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-portal-v2-frontend-20260610-204915/README.md | bidirectional | pending_api |
| GPCF-DOC-8898209B8E | .harness/runs/gbrain-portal-v2-frontend-20260610-204915/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-portal-v2-frontend-20260610-204915/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-530B2BF79A | .harness/runs/gbrain-v2-sprint1-20260610-212531/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2-sprint1-20260610-212531/README.md | bidirectional | pending_api |
| GPCF-DOC-0AC4F38B1A | .harness/runs/gbrain-v2.1-sprint1-20260610-214441/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint1-20260610-214441/README.md | bidirectional | pending_api |
| GPCF-DOC-54C43FAC33 | .harness/runs/gbrain-v2.1-sprint1-20260610-214441/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint1-20260610-214441/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-BFEB10D711 | .harness/runs/gbrain-v2.1-sprint2-20260610-214842/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint2-20260610-214842/README.md | bidirectional | pending_api |
| GPCF-DOC-D03E6BE997 | .harness/runs/gbrain-v2.1-sprint2-20260610-214842/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint2-20260610-214842/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-520E6A10FE | .harness/runs/gbrain-v2.1-sprint3-20260610-215034/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint3-20260610-215034/README.md | bidirectional | pending_api |
| GPCF-DOC-2AEC389E51 | .harness/runs/gbrain-v2.1-sprint3-20260610-215034/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint3-20260610-215034/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-B0E20E2E16 | .harness/runs/gbrain-v2.1-sprint4-20260610-215232/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.1-sprint4-20260610-215232/README.md | bidirectional | pending_api |
| GPCF-DOC-F78110A3B6 | .harness/runs/gbrain-v2.2-20260610-215935/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.2-20260610-215935/README.md | bidirectional | pending_api |
| GPCF-DOC-DF73213193 | .harness/runs/gbrain-v2.2-20260610-215935/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.2-20260610-215935/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-4879E0F6B6 | .harness/runs/gbrain-v2.3-20260610-220227/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v2.3-20260610-220227/README.md | bidirectional | pending_api |
| GPCF-DOC-5786630B8F | .harness/runs/gbrain-v3.0-20260610-220702/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.0-20260610-220702/README.md | bidirectional | pending_api |
| GPCF-DOC-F6876D638F | .harness/runs/gbrain-v3.1-hardening-20260610-222505/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260610-222505/README.md | bidirectional | pending_api |
| GPCF-DOC-B96A928F89 | .harness/runs/gbrain-v3.1-hardening-20260610-222505/patches/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260610-222505/patches/README.md | bidirectional | pending_api |
| GPCF-DOC-ED2B81A98D | .harness/runs/gbrain-v3.1-hardening-20260610-222505/workspaces/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260610-222505/workspaces/README.md | bidirectional | pending_api |
| GPCF-DOC-EA97040BE1 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/README.md | bidirectional | pending_api |
| GPCF-DOC-9C70414B66 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-5C8B07F574 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/design.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/design.md | bidirectional | pending_api |
| GPCF-DOC-8A206BCB11 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-17799BC191 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/patches/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/patches/README.md | bidirectional | pending_api |
| GPCF-DOC-F7F2EF5A5D | .harness/runs/gbrain-v3.1-hardening-20260611-002252/proposal.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/proposal.md | bidirectional | pending_api |
| GPCF-DOC-72B2E0EF61 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-65DA9DDC44 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/tasks.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/tasks.md | bidirectional | pending_api |
| GPCF-DOC-5A3C833C90 | .harness/runs/gbrain-v3.1-hardening-20260611-002252/workspaces/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/workspaces/README.md | bidirectional | pending_api |
| GPCF-DOC-60D38E1B72 | .harness/runs/gbrain-v3.2-design-20260611-003001/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-design-20260611-003001/README.md | bidirectional | pending_api |
| GPCF-DOC-253B627E40 | .harness/runs/gbrain-v3.2-design-20260611-003001/proposal.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-design-20260611-003001/proposal.md | bidirectional | pending_api |
| GPCF-DOC-AAE51A57F5 | .harness/runs/gbrain-v3.2-e2e-test-20260611-010548/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-e2e-test-20260611-010548/README.md | bidirectional | pending_api |
| GPCF-DOC-CAC95B5694 | .harness/runs/gbrain-v3.2-e2e-test-20260611-010548/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-e2e-test-20260611-010548/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-CDEF748B2E | .harness/runs/gbrain-v3.2-e2e-test-20260611-010548/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-e2e-test-20260611-010548/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-A31BE9423A | .harness/runs/gbrain-v3.2-e2e-test-20260611-010548/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-e2e-test-20260611-010548/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-FD9FD5FE29 | .harness/runs/gbrain-v3.2-e2e-test-20260611-010548/test-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-e2e-test-20260611-010548/test-matrix.md | bidirectional | pending_api |
| GPCF-DOC-5E9504BBF3 | .harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/README.md | bidirectional | pending_api |
| GPCF-DOC-D750F507B6 | .harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-449C9F0E56 | .harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-CAB96FCBB3 | .harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-fix-tabs-20260611-010336/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-369A9AB18D | .harness/runs/gbrain-v3.2-graph-ux-20260611-010847/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-graph-ux-20260611-010847/README.md | bidirectional | pending_api |
| GPCF-DOC-9DCD03E299 | .harness/runs/gbrain-v3.2-graph-ux-20260611-010847/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-graph-ux-20260611-010847/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-11D2ABC390 | .harness/runs/gbrain-v3.2-sprint1-20260611-003247/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint1-20260611-003247/README.md | bidirectional | pending_api |
| GPCF-DOC-AF04B46319 | .harness/runs/gbrain-v3.2-sprint1-20260611-003247/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint1-20260611-003247/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-4086BF725A | .harness/runs/gbrain-v3.2-sprint1-20260611-003247/patches/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint1-20260611-003247/patches/README.md | bidirectional | pending_api |
| GPCF-DOC-1912183C8E | .harness/runs/gbrain-v3.2-sprint1-20260611-003247/workspaces/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint1-20260611-003247/workspaces/README.md | bidirectional | pending_api |
| GPCF-DOC-CFE38BC1C5 | .harness/runs/gbrain-v3.2-sprint2-20260611-004233/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint2-20260611-004233/README.md | bidirectional | pending_api |
| GPCF-DOC-310C96221E | .harness/runs/gbrain-v3.2-sprint2-20260611-004233/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint2-20260611-004233/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-78696D07CE | .harness/runs/gbrain-v3.2-sprint3-20260611-005031/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint3-20260611-005031/README.md | bidirectional | pending_api |
| GPCF-DOC-9F40EBBE0A | .harness/runs/gbrain-v3.2-sprint3-20260611-005031/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint3-20260611-005031/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-631FAA49D7 | .harness/runs/gbrain-v3.2-sprint4-20260611-005427/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/README.md | bidirectional | pending_api |
| GPCF-DOC-D928C393A1 | .harness/runs/gbrain-v3.2-sprint4-20260611-005427/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-05F302F1E3 | .harness/runs/gbrain-v3.2-sprint4-20260611-005427/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-46C72A325B | .harness/runs/gbrain-v3.2-sprint4-20260611-005427/proposal.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/proposal.md | bidirectional | pending_api |
| GPCF-DOC-FC4108C8F1 | .harness/runs/gbrain-v3.2-sprint4-20260611-005427/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-3C4E0A2FB6 | .harness/runs/gbrain-v3.2-sprint4-20260611-005427/tasks.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/tasks.md | bidirectional | pending_api |
| GPCF-DOC-BE82E88CD0 | .harness/runs/gbrain-v3.2-zh-final-20260611-012235/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-zh-final-20260611-012235/README.md | bidirectional | pending_api |
| GPCF-DOC-0323BC65B4 | .harness/runs/gbrain-v3.2-zh-final-20260611-012235/acceptance-matrix.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-zh-final-20260611-012235/acceptance-matrix.md | bidirectional | pending_api |
| GPCF-DOC-5A27A20A77 | .harness/runs/gbrain-v3.2-zh-final-20260611-012235/evidence/README.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-zh-final-20260611-012235/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-6CED60E9F1 | .harness/runs/gbrain-v3.2-zh-final-20260611-012235/status-audit.md | 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-zh-final-20260611-012235/status-audit.md | bidirectional | pending_api |
| GPCF-DOC-D1608C81FA | 00-index/README.md | 开发/12-GPCF/00-index/README.md | bidirectional | pending_api |
| GPCF-DOC-09655E45C0 | 01-architecture/ADR-GPC从Odoo二开调整为原生公共服务平台.md | 开发/90-跨项目架构/01-architecture/ADR-GPC从Odoo二开调整为原生公共服务平台.md | bidirectional | pending_api |
| GPCF-DOC-7FAF5AD2FB | 01-architecture/AI驱动GFIS三阶段演进构想.md | 开发/90-跨项目架构/01-architecture/AI驱动GFIS三阶段演进构想.md | bidirectional | pending_api |
| GPCF-DOC-16D9DC63AA | 01-architecture/AI驱动GFIS与GlobalCloud体系结合分析.md | 开发/90-跨项目架构/01-architecture/AI驱动GFIS与GlobalCloud体系结合分析.md | bidirectional | pending_api |
| GPCF-DOC-3F9E7988C6 | 01-architecture/AI驱动工厂信息化系统完整方案V3.1.md | 开发/90-跨项目架构/01-architecture/AI驱动工厂信息化系统完整方案V3.1.md | bidirectional | pending_api |
| GPCF-DOC-D54AF3DD5D | 01-architecture/GPC方向全面分析报告.md | 开发/90-跨项目架构/01-architecture/GPC方向全面分析报告.md | bidirectional | pending_api |
| GPCF-DOC-0C519C97BD | 01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md | 开发/90-跨项目架构/01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md | bidirectional | pending_api |
| GPCF-DOC-3DBC8DC5C3 | 01-architecture/GlobalCloud智慧工厂专项架构图集.md | 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂专项架构图集.md | bidirectional | pending_api |
| GPCF-DOC-1DCB795545 | 01-architecture/GlobalCloud智慧工厂进一步梳理与提示词库.md | 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂进一步梳理与提示词库.md | bidirectional | pending_api |
| GPCF-DOC-B2A5E41836 | 01-architecture/GlobalCloud智慧工厂项目群控制表.md | 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂项目群控制表.md | bidirectional | pending_api |
| GPCF-DOC-475051A08A | 01-architecture/GlobalCloud智慧工厂项目群架构图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂项目群架构图.md | bidirectional | pending_api |
| GPCF-DOC-18B774FB34 | 01-architecture/GlobalCloud绿色供应链体系-WIKI宪法体系与葛化项目映射分析.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系-WIKI宪法体系与葛化项目映射分析.md | bidirectional | pending_api |
| GPCF-DOC-0CCC5F2950 | 01-architecture/GlobalCloud绿色供应链体系WAES控制塔与治理门禁图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系WAES控制塔与治理门禁图.md | bidirectional | pending_api |
| GPCF-DOC-31CB143A7C | 01-architecture/GlobalCloud绿色供应链体系WAES控制塔治理架构图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系WAES控制塔治理架构图.md | bidirectional | pending_api |
| GPCF-DOC-2425FD0964 | 01-architecture/GlobalCloud绿色供应链体系全链路事件与证据闭环图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系全链路事件与证据闭环图.md | bidirectional | pending_api |
| GPCF-DOC-069589E530 | 01-architecture/GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系四流综合架构分析与优化方案.md | bidirectional | pending_api |
| GPCF-DOC-B7351DDCF8 | 01-architecture/GlobalCloud绿色供应链体系多厂协同模型.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系多厂协同模型.md | bidirectional | pending_api |
| GPCF-DOC-F6C8634052 | 01-architecture/GlobalCloud绿色供应链体系多智能体实施团队与协同方案.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系多智能体实施团队与协同方案.md | bidirectional | pending_api |
| GPCF-DOC-424D73E236 | 01-architecture/GlobalCloud绿色供应链体系层次化结构与优化提示词.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系层次化结构与优化提示词.md | bidirectional | pending_api |
| GPCF-DOC-2656290CFC | 01-architecture/GlobalCloud绿色供应链体系总体实施路线与交付保障方案.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系总体实施路线与交付保障方案.md | bidirectional | pending_api |
| GPCF-DOC-6ADEF5F42F | 01-architecture/GlobalCloud绿色供应链体系总架构.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系总架构.md | bidirectional | pending_api |
| GPCF-DOC-6B386000D3 | 01-architecture/GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md | bidirectional | pending_api |
| GPCF-DOC-4DF13CF33D | 01-architecture/GlobalCloud绿色供应链体系最新架构图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系最新架构图.md | bidirectional | pending_api |
| GPCF-DOC-5BF9469733 | 01-architecture/GlobalCloud绿色供应链体系真实层次架构图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系真实层次架构图.md | bidirectional | pending_api |
| GPCF-DOC-3DB47E5509 | 01-architecture/GlobalCloud绿色供应链平台业务流架构图.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链平台业务流架构图.md | bidirectional | pending_api |
| GPCF-DOC-AA2468EDC8 | 01-architecture/GlobalCloud绿色供应链平台主架构与宪法约束融合建议.md | 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链平台主架构与宪法约束融合建议.md | bidirectional | pending_api |
| GPCF-DOC-535BF5C0CA | 01-architecture/GlobalCloud项目群交叉分析报告.md | 开发/90-跨项目架构/01-architecture/GlobalCloud项目群交叉分析报告.md | bidirectional | pending_api |
| GPCF-DOC-75A25DFFB1 | 01-architecture/README.md | 开发/90-跨项目架构/01-architecture/README.md | bidirectional | pending_api |
| GPCF-DOC-1D47877518 | 01-architecture/基于GlobalCloud项目群的智慧工厂架构设计方案.md | 开发/90-跨项目架构/01-architecture/基于GlobalCloud项目群的智慧工厂架构设计方案.md | bidirectional | pending_api |
| GPCF-DOC-78AE1A47AE | 02-governance/GlobalCloud智能体团队Codex工具与技能使用治理规范.md | 开发/91-治理与验收/02-governance/GlobalCloud智能体团队Codex工具与技能使用治理规范.md | bidirectional | pending_api |
| GPCF-DOC-39A8CE7FE1 | 02-governance/GlobalCloud智能体团队工作区与项目仓库操作规范.md | 开发/91-治理与验收/02-governance/GlobalCloud智能体团队工作区与项目仓库操作规范.md | bidirectional | pending_api |
| GPCF-DOC-7F63F2D675 | 02-governance/GlobalCloud智能体团队总体运行机制.md | 开发/91-治理与验收/02-governance/GlobalCloud智能体团队总体运行机制.md | bidirectional | pending_api |
| GPCF-DOC-A437BDA6F5 | 02-governance/GlobalCloud智能体团队模型使用治理与成本控制机制.md | 开发/91-治理与验收/02-governance/GlobalCloud智能体团队模型使用治理与成本控制机制.md | bidirectional | pending_api |
| GPCF-DOC-2469340C52 | 02-governance/GlobalCloud智能体团队软件全过程实施与交付控制规范.md | 开发/91-治理与验收/02-governance/GlobalCloud智能体团队软件全过程实施与交付控制规范.md | bidirectional | pending_api |
| GPCF-DOC-39CC074588 | 02-governance/GlobalCloud智能体团队运行与实施环境总体规范.md | 开发/91-治理与验收/02-governance/GlobalCloud智能体团队运行与实施环境总体规范.md | bidirectional | pending_api |
| GPCF-DOC-16A6E29BA0 | 02-governance/GlobalCloud绿色供应链体系交付物完成判定规范.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系交付物完成判定规范.md | bidirectional | pending_api |
| GPCF-DOC-12F3EAB4C6 | 02-governance/GlobalCloud绿色供应链体系动运转达标标准与质量门禁.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系动运转达标标准与质量门禁.md | bidirectional | pending_api |
| GPCF-DOC-1139BD0025 | 02-governance/GlobalCloud绿色供应链体系实施过程控制规范清单.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系实施过程控制规范清单.md | bidirectional | pending_api |
| GPCF-DOC-22B59B08B7 | 02-governance/GlobalCloud绿色供应链体系实施项目控制与量化机制.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系实施项目控制与量化机制.md | bidirectional | pending_api |
| GPCF-DOC-4300D04C44 | 02-governance/GlobalCloud绿色供应链体系模块实施分级判定表.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系模块实施分级判定表.md | bidirectional | pending_api |
| GPCF-DOC-670FDF1C79 | 02-governance/GlobalCloud绿色供应链体系测试与验证规范.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系测试与验证规范.md | bidirectional | pending_api |
| GPCF-DOC-5D55FFB7D9 | 02-governance/GlobalCloud绿色供应链体系状态升级与验收放行规范.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系状态升级与验收放行规范.md | bidirectional | pending_api |
| GPCF-DOC-FD6BA2EC78 | 02-governance/GlobalCloud绿色供应链体系设计-实现追踪矩阵规范.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系设计-实现追踪矩阵规范.md | bidirectional | pending_api |
| GPCF-DOC-94AA31880F | 02-governance/GlobalCloud绿色供应链体系项目仓库实施准入规范.md | 开发/91-治理与验收/02-governance/GlobalCloud绿色供应链体系项目仓库实施准入规范.md | bidirectional | pending_api |
| GPCF-DOC-AC66DE8415 | 02-governance/GlobalCloud项目群KDS开发空间安全规范.md | 开发/91-治理与验收/02-governance/GlobalCloud项目群KDS开发空间安全规范.md | bidirectional | pending_api |
| GPCF-DOC-D2373AEE37 | 02-governance/GlobalCloud项目群在Codex中的模型分工与成本控制方案.md | 开发/91-治理与验收/02-governance/GlobalCloud项目群在Codex中的模型分工与成本控制方案.md | bidirectional | pending_api |
| GPCF-DOC-B8ADFA9E30 | 02-governance/GlobalCloud项目群文档综合治理规范.md | 开发/91-治理与验收/02-governance/GlobalCloud项目群文档综合治理规范.md | bidirectional | pending_api |
| GPCF-DOC-87DD7D79CD | 02-governance/GlobalCloud项目群文档防污染规则.md | 开发/91-治理与验收/02-governance/GlobalCloud项目群文档防污染规则.md | bidirectional | pending_api |
| GPCF-DOC-F949595C37 | 02-governance/README.md | 开发/91-治理与验收/02-governance/README.md | bidirectional | pending_api |
| GPCF-DOC-F3EADEE56A | 02-governance/gpcf-agent-architecture-six-elements.md | 开发/91-治理与验收/02-governance/gpcf-agent-architecture-six-elements.md | bidirectional | pending_api |
| GPCF-DOC-F113DF5034 | 02-governance/gpcf-evidence-taxonomy.md | 开发/91-治理与验收/02-governance/gpcf-evidence-taxonomy.md | bidirectional | pending_api |
| GPCF-DOC-20CE547AAF | 02-governance/gpcf-loop-engineering-spec-v1.md | 开发/91-治理与验收/02-governance/gpcf-loop-engineering-spec-v1.md | bidirectional | pending_api |
| GPCF-DOC-D67341FE2B | 02-governance/gpcf-role-boundary.md | 开发/91-治理与验收/02-governance/gpcf-role-boundary.md | bidirectional | pending_api |
| GPCF-DOC-A33E51C815 | 02-governance/gpcf-status-machine.md | 开发/91-治理与验收/02-governance/gpcf-status-machine.md | bidirectional | pending_api |
| GPCF-DOC-E4579BFF7E | 03-data-ai-knowledge/GPC 绿色供应链公共服务平台总体方案.md | 开发/05-KDS/03-data-ai-knowledge/GPC 绿色供应链公共服务平台总体方案.md | bidirectional | pending_api |
| GPCF-DOC-1F12054E1C | 03-data-ai-knowledge/GlobalCloud企业级知识系统冲突点与收口方案.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud企业级知识系统冲突点与收口方案.md | bidirectional | pending_api |
| GPCF-DOC-F5B3269058 | 03-data-ai-knowledge/GlobalCloud企业级知识系统总目标与执行分解表.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud企业级知识系统总目标与执行分解表.md | bidirectional | pending_api |
| GPCF-DOC-A3B30485E9 | 03-data-ai-knowledge/GlobalCloud全局模型目录与能力标签标准.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud全局模型目录与能力标签标准.md | bidirectional | pending_api |
| GPCF-DOC-0A5E8FD5E6 | 03-data-ai-knowledge/GlobalCloud智能体团队-企业级知识系统实施任务书.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud智能体团队-企业级知识系统实施任务书.md | bidirectional | pending_api |
| GPCF-DOC-1212817FF5 | 03-data-ai-knowledge/GlobalCloud模型授权审计计量与分期结算规划.md | 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud模型授权审计计量与分期结算规划.md | bidirectional | pending_api |
| GPCF-DOC-69CFFD4C82 | 03-data-ai-knowledge/GlobalCloud统一模型配置体系方案.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud统一模型配置体系方案.md | bidirectional | pending_api |
| GPCF-DOC-05774FB8AD | 03-data-ai-knowledge/GlobalCloud绿色供应链体系AI服务模型.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系AI服务模型.md | bidirectional | pending_api |
| GPCF-DOC-CA83191660 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系Edge接入与安全模型.md | 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud绿色供应链体系Edge接入与安全模型.md | bidirectional | pending_api |
| GPCF-DOC-52B18BDBE9 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系LLM Wiki与Brain测试评估矩阵.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系LLM Wiki与Brain测试评估矩阵.md | bidirectional | pending_api |
| GPCF-DOC-664403C419 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系SOP模板库.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系SOP模板库.md | bidirectional | pending_api |
| GPCF-DOC-9B55FCEA8F | 03-data-ai-knowledge/GlobalCloud绿色供应链体系事件合同.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系事件合同.md | bidirectional | pending_api |
| GPCF-DOC-BA68A130D5 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库主存层与LLM Wiki-Brain升级图.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库主存层与LLM Wiki-Brain升级图.md | bidirectional | pending_api |
| GPCF-DOC-D48C6EB801 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库方案.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库方案.md | bidirectional | pending_api |
| GPCF-DOC-1362AFC964 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系全局初始化SOP方案.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系全局初始化SOP方案.md | bidirectional | pending_api |
| GPCF-DOC-1A3581D521 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系对象目录.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系对象目录.md | bidirectional | pending_api |
| GPCF-DOC-0962BEDB78 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系数据治理模型.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系数据治理模型.md | bidirectional | pending_api |
| GPCF-DOC-04D6680E14 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md | bidirectional | pending_api |
| GPCF-DOC-FCCA958E2C | 03-data-ai-knowledge/GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md | bidirectional | pending_api |
| GPCF-DOC-062D4DA687 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系系统-数据库边界总表.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系系统-数据库边界总表.md | bidirectional | pending_api |
| GPCF-DOC-E2FDF91E39 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md | bidirectional | pending_api |
| GPCF-DOC-E4DDF33CF8 | 03-data-ai-knowledge/GlobalCloud绿色供应链体系连接器合同.md | 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系连接器合同.md | bidirectional | pending_api |
| GPCF-DOC-09065C5D7F | 03-data-ai-knowledge/GlobalCloud项目模型引用与用户模型偏好方案.md | 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud项目模型引用与用户模型偏好方案.md | bidirectional | pending_api |
| GPCF-DOC-A7C38B4EA7 | 03-data-ai-knowledge/README.md | 开发/05-KDS/03-data-ai-knowledge/README.md | bidirectional | pending_api |
| GPCF-DOC-56BC03A70C | 04-ui-delivery/GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系P0最小闭环界面实施清单.md | bidirectional | pending_api |
| GPCF-DOC-BD1C1FE02E | 04-ui-delivery/GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系P0最小闭环界面验收矩阵.md | bidirectional | pending_api |
| GPCF-DOC-5D5E27312C | 04-ui-delivery/GlobalCloud绿色供应链体系对话模式与操作模式规范.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系对话模式与操作模式规范.md | bidirectional | pending_api |
| GPCF-DOC-E12B78B67D | 04-ui-delivery/GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系平台订单-签收-异常界面收口专项方案.md | bidirectional | pending_api |
| GPCF-DOC-16087A96BC | 04-ui-delivery/GlobalCloud绿色供应链体系最终交付界面规范与样式规范.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系最终交付界面规范与样式规范.md | bidirectional | pending_api |
| GPCF-DOC-C884E15D19 | 04-ui-delivery/GlobalCloud绿色供应链体系样板页实施计划.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系样板页实施计划.md | bidirectional | pending_api |
| GPCF-DOC-D068AE0B5B | 04-ui-delivery/GlobalCloud绿色供应链体系界面分阶段治理规则.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系界面分阶段治理规则.md | bidirectional | pending_api |
| GPCF-DOC-2BC3BD8BEA | 04-ui-delivery/GlobalCloud绿色供应链体系界面实施差距清单.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系界面实施差距清单.md | bidirectional | pending_api |
| GPCF-DOC-6CA9039C10 | 04-ui-delivery/GlobalCloud绿色供应链体系界面实施排期表.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系界面实施排期表.md | bidirectional | pending_api |
| GPCF-DOC-42C17163FA | 04-ui-delivery/GlobalCloud绿色供应链体系界面实施责任分配表.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系界面实施责任分配表.md | bidirectional | pending_api |
| GPCF-DOC-2D7F908C5F | 04-ui-delivery/GlobalCloud绿色供应链体系统一体验骨架规范.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系统一体验骨架规范.md | bidirectional | pending_api |
| GPCF-DOC-BA482BB4F5 | 04-ui-delivery/GlobalCloud绿色供应链体系统一组件与设计令牌规范.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系统一组件与设计令牌规范.md | bidirectional | pending_api |
| GPCF-DOC-0384F73471 | 04-ui-delivery/GlobalCloud绿色供应链体系统一组件库建设计划.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系统一组件库建设计划.md | bidirectional | pending_api |
| GPCF-DOC-8F1279E706 | 04-ui-delivery/GlobalCloud绿色供应链体系首批组件接入实施计划.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系首批组件接入实施计划.md | bidirectional | pending_api |
| GPCF-DOC-5371CCBDCB | 04-ui-delivery/GlobalCloud绿色供应链体系首批统一组件接入样板清单.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系首批统一组件接入样板清单.md | bidirectional | pending_api |
| GPCF-DOC-0C4A339FD2 | 04-ui-delivery/GlobalCloud绿色供应链体系首批统一组件清单.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系首批统一组件清单.md | bidirectional | pending_api |
| GPCF-DOC-DFFAFE5D69 | 04-ui-delivery/GlobalCloud绿色供应链体系首批统一组件验收标准.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系首批统一组件验收标准.md | bidirectional | pending_api |
| GPCF-DOC-3D439D777F | 04-ui-delivery/GlobalCloud绿色供应链体系高风险模块样板页清单.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系高风险模块样板页清单.md | bidirectional | pending_api |
| GPCF-DOC-6008375BA7 | 04-ui-delivery/GlobalCloud绿色供应链体系高风险模块界面收口任务分解表.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系高风险模块界面收口任务分解表.md | bidirectional | pending_api |
| GPCF-DOC-505DFF5C49 | 04-ui-delivery/GlobalCloud绿色供应链体系高风险模块界面收口计划.md | 开发/02-GPC/04-ui-delivery/GlobalCloud绿色供应链体系高风险模块界面收口计划.md | bidirectional | pending_api |
| GPCF-DOC-C4D724E837 | 04-ui-delivery/README.md | 开发/02-GPC/04-ui-delivery/README.md | bidirectional | pending_api |
| GPCF-DOC-AEEFA55699 | 05-agent-team/GlobalCloud智能体团队12个交付包责任分解表.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队12个交付包责任分解表.md | bidirectional | pending_api |
| GPCF-DOC-B66EC338E9 | 05-agent-team/GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队6个专项首轮实施前验证包执行矩阵.md | bidirectional | pending_api |
| GPCF-DOC-E164F62976 | 05-agent-team/GlobalCloud智能体团队6个专项首轮实施前验证执行台账.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队6个专项首轮实施前验证执行台账.md | bidirectional | pending_api |
| GPCF-DOC-D06020C9DC | 05-agent-team/GlobalCloud智能体团队Loop Engineering全面改进方案.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队Loop Engineering全面改进方案.md | bidirectional | pending_api |
| GPCF-DOC-3874DD0406 | 05-agent-team/GlobalCloud智能体团队PMBOK项目管理台账.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队PMBOK项目管理台账.md | bidirectional | pending_api |
| GPCF-DOC-8CDB82A404 | 05-agent-team/GlobalCloud智能体团队下一步执行清单.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队下一步执行清单.md | bidirectional | pending_api |
| GPCF-DOC-6C1B946AA5 | 05-agent-team/GlobalCloud智能体团队专项回报汇总台账.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队专项回报汇总台账.md | bidirectional | pending_api |
| GPCF-DOC-7249EEECFE | 05-agent-team/GlobalCloud智能体团队专项执行版包模板.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队专项执行版包模板.md | bidirectional | pending_api |
| GPCF-DOC-582A23D485 | 05-agent-team/GlobalCloud智能体团队侧边聊天10条主线-团队责任分配总表.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队侧边聊天10条主线-团队责任分配总表.md | bidirectional | pending_api |
| GPCF-DOC-5D6CD718DA | 05-agent-team/GlobalCloud智能体团队侧边聊天10条主线-当前实施准备完成度总表.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队侧边聊天10条主线-当前实施准备完成度总表.md | bidirectional | pending_api |
| GPCF-DOC-61BD531C70 | 05-agent-team/GlobalCloud智能体团队侧边聊天完整归纳总览.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队侧边聊天完整归纳总览.md | bidirectional | pending_api |
| GPCF-DOC-2F22FF007C | 05-agent-team/GlobalCloud智能体团队实施前准备完成结论.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队实施前准备完成结论.md | bidirectional | pending_api |
| GPCF-DOC-62063BBDE9 | 05-agent-team/GlobalCloud智能体团队实施前准备差距清单.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队实施前准备差距清单.md | bidirectional | pending_api |
| GPCF-DOC-3D6A5A4056 | 05-agent-team/GlobalCloud智能体团队实施前准备目标模式要求.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队实施前准备目标模式要求.md | bidirectional | pending_api |
| GPCF-DOC-D899DB2508 | 05-agent-team/GlobalCloud智能体团队实施前证据与阻塞总表.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队实施前证据与阻塞总表.md | bidirectional | pending_api |
| GPCF-DOC-8A91086A7D | 05-agent-team/GlobalCloud智能体团队当前总目标.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队当前总目标.md | bidirectional | pending_api |
| GPCF-DOC-FE641179EC | 05-agent-team/GlobalCloud智能体团队总体规划与行动计划.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队总体规划与行动计划.md | bidirectional | pending_api |
| GPCF-DOC-B2499B523C | 05-agent-team/GlobalCloud智能体团队控制塔与周报机制.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队控制塔与周报机制.md | bidirectional | pending_api |
| GPCF-DOC-FF53116C54 | 05-agent-team/GlobalCloud智能体团队文档全量盘点与分类总表.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队文档全量盘点与分类总表.md | bidirectional | pending_api |
| GPCF-DOC-A080E39115 | 05-agent-team/GlobalCloud智能体团队文档清理与补充完善建议.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队文档清理与补充完善建议.md | bidirectional | pending_api |
| GPCF-DOC-A45C28115C | 05-agent-team/GlobalCloud智能体团队文档理解与纳入审计.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队文档理解与纳入审计.md | bidirectional | pending_api |
| GPCF-DOC-6F5B2A27CF | 05-agent-team/GlobalCloud智能体团队显性智能体名录与可见机制.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队显性智能体名录与可见机制.md | bidirectional | pending_api |
| GPCF-DOC-C892CAB85A | 05-agent-team/GlobalCloud智能体团队本阶段首轮实施前验证目标.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队本阶段首轮实施前验证目标.md | bidirectional | pending_api |
| GPCF-DOC-92F9FE9764 | 05-agent-team/GlobalCloud智能体团队正式实施开发前准备100分量化评分提示词.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队正式实施开发前准备100分量化评分提示词.md | bidirectional | pending_api |
| GPCF-DOC-C0F82AE843 | 05-agent-team/GlobalCloud智能体团队正式实施开发前准备评分文档纳入覆盖矩阵.md | 开发/12-GPCF/05-agent-team/GlobalCloud智能体团队正式实施开发前准备评分文档纳入覆盖矩阵.md | bidirectional | pending_api |
| GPCF-DOC-338F660061 | 05-agent-team/GlobalCloud智能体团队正式实施开发前缺口关闭清单.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队正式实施开发前缺口关闭清单.md | bidirectional | pending_api |
| GPCF-DOC-D83CE73173 | 05-agent-team/GlobalCloud智能体团队真实项目仓库映射与只读预检计划.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队真实项目仓库映射与只读预检计划.md | bidirectional | pending_api |
| GPCF-DOC-7C5F2C8F94 | 05-agent-team/GlobalCloud智能体团队阶段-工作-工具-技能-方法-效率-成本执行矩阵.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队阶段-工作-工具-技能-方法-效率-成本执行矩阵.md | bidirectional | pending_api |
| GPCF-DOC-A8F6B69EE5 | 05-agent-team/GlobalCloud智能体团队阶段行动计划.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队阶段行动计划.md | bidirectional | pending_api |
| GPCF-DOC-114BC60C1B | 05-agent-team/GlobalCloud智能体团队首版周报.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队首版周报.md | bidirectional | pending_api |
| GPCF-DOC-AF862B0D78 | 05-agent-team/GlobalCloud智能体团队首轮实施前验证入口判断.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队首轮实施前验证入口判断.md | bidirectional | pending_api |
| GPCF-DOC-2EF7BA3A76 | 05-agent-team/GlobalCloud智能体团队首轮实施前验证包总表.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队首轮实施前验证包总表.md | bidirectional | pending_api |
| GPCF-DOC-0D3224DFB9 | 05-agent-team/GlobalCloud智能体实施团队准备度评估.md | 开发/08-XiaoC/05-agent-team/GlobalCloud智能体实施团队准备度评估.md | bidirectional | pending_api |
| GPCF-DOC-E50AD58A99 | 05-agent-team/README.md | 开发/08-XiaoC/05-agent-team/README.md | bidirectional | pending_api |
| GPCF-DOC-43EEEC8238 | 06-workstreams/README.md | 开发/08-XiaoC/06-workstreams/README.md | bidirectional | pending_api |
| GPCF-DOC-9F1BE7A287 | 06-workstreams/仓图专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/仓图专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-93BFB00E2A | 06-workstreams/厂行专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/厂行专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-8DA7A7CF1B | 06-workstreams/厂行专项会话状态报告模板.md | 开发/08-XiaoC/06-workstreams/厂行专项会话状态报告模板.md | bidirectional | pending_api |
| GPCF-DOC-6C34A5454F | 06-workstreams/厂行专项正式只读预检结论.md | 开发/12-GPCF/06-workstreams/厂行专项正式只读预检结论.md | bidirectional | pending_api |
| GPCF-DOC-C3F58B5314 | 06-workstreams/厂行专项首轮实施前验证包.md | 开发/12-GPCF/06-workstreams/厂行专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-9A0B1FF39A | 06-workstreams/厂行专项首轮实施前验证执行记录.md | 开发/12-GPCF/06-workstreams/厂行专项首轮实施前验证执行记录.md | bidirectional | pending_api |
| GPCF-DOC-D30AC30535 | 06-workstreams/宪衡专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/宪衡专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-6FE56B8FED | 06-workstreams/宪衡专项可执行验证入口清单.md | 开发/12-GPCF/06-workstreams/宪衡专项可执行验证入口清单.md | bidirectional | pending_api |
| GPCF-DOC-CE9D5E1820 | 06-workstreams/宪衡专项执行版包-侧线程草案.md | 开发/08-XiaoC/06-workstreams/宪衡专项执行版包-侧线程草案.md | bidirectional | pending_api |
| GPCF-DOC-0FD20721A6 | 06-workstreams/宪衡专项正式只读预检结论.md | 开发/12-GPCF/06-workstreams/宪衡专项正式只读预检结论.md | bidirectional | pending_api |
| GPCF-DOC-24A095DD7D | 06-workstreams/宪衡专项首轮实施前验证包.md | 开发/12-GPCF/06-workstreams/宪衡专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-FFC2BDFA8A | 06-workstreams/宪衡专项首轮实施前验证执行记录.md | 开发/12-GPCF/06-workstreams/宪衡专项首轮实施前验证执行记录.md | bidirectional | pending_api |
| GPCF-DOC-1272F28543 | 06-workstreams/接稳专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/接稳专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-02C8CD9284 | 06-workstreams/数枢专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/数枢专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-510FE064B3 | 06-workstreams/数枢专项正式只读预检结论.md | 开发/12-GPCF/06-workstreams/数枢专项正式只读预检结论.md | bidirectional | pending_api |
| GPCF-DOC-BBAA73EE39 | 06-workstreams/数枢专项首轮实施前验证包.md | 开发/12-GPCF/06-workstreams/数枢专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-656600984E | 06-workstreams/数枢专项首轮实施前验证执行记录.md | 开发/12-GPCF/06-workstreams/数枢专项首轮实施前验证执行记录.md | bidirectional | pending_api |
| GPCF-DOC-7C2F7BF7AC | 06-workstreams/灵策与评证专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/灵策与评证专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-C70B35BC1B | 06-workstreams/灵策与评证专项正式只读预检结论.md | 开发/08-XiaoC/06-workstreams/灵策与评证专项正式只读预检结论.md | bidirectional | pending_api |
| GPCF-DOC-5BEBE02506 | 06-workstreams/灵策与评证专项首轮实施前验证包.md | 开发/08-XiaoC/06-workstreams/灵策与评证专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-452FC27F7F | 06-workstreams/灵策与评证专项首轮实施前验证执行记录.md | 开发/08-XiaoC/06-workstreams/灵策与评证专项首轮实施前验证执行记录.md | bidirectional | pending_api |
| GPCF-DOC-440EE5CBC1 | 06-workstreams/灵策专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/灵策专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-20B2BF28FB | 06-workstreams/灵策专项首轮实施前执行记录.md | 开发/08-XiaoC/06-workstreams/灵策专项首轮实施前执行记录.md | bidirectional | pending_api |
| GPCF-DOC-12DC8FDEE2 | 06-workstreams/灵策专项首轮实施前验证包.md | 开发/08-XiaoC/06-workstreams/灵策专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-A6A151135B | 06-workstreams/知源专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/知源专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-FC88DC4E48 | 06-workstreams/知源专项会话状态报告模板.md | 开发/08-XiaoC/06-workstreams/知源专项会话状态报告模板.md | bidirectional | pending_api |
| GPCF-DOC-4822B637C3 | 06-workstreams/知源专项正式只读预检结论.md | 开发/12-GPCF/06-workstreams/知源专项正式只读预检结论.md | bidirectional | pending_api |
| GPCF-DOC-29B08242D5 | 06-workstreams/知源专项首轮实施前验证包.md | 开发/12-GPCF/06-workstreams/知源专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-2661964453 | 06-workstreams/知源专项首轮实施前验证执行记录.md | 开发/12-GPCF/06-workstreams/知源专项首轮实施前验证执行记录.md | bidirectional | pending_api |
| GPCF-DOC-E526B6F91A | 06-workstreams/证验专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/证验专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-16A50D01FF | 06-workstreams/证验专项首轮实施前执行记录.md | 开发/08-XiaoC/06-workstreams/证验专项首轮实施前执行记录.md | bidirectional | pending_api |
| GPCF-DOC-0298890196 | 06-workstreams/证验专项首轮实施前验证包.md | 开发/08-XiaoC/06-workstreams/证验专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-AE0D14D96A | 06-workstreams/评衡专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/评衡专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-7EC6E52722 | 06-workstreams/评衡专项首轮实施前执行记录.md | 开发/08-XiaoC/06-workstreams/评衡专项首轮实施前执行记录.md | bidirectional | pending_api |
| GPCF-DOC-C54314A529 | 06-workstreams/评衡专项首轮实施前验证包.md | 开发/12-GPCF/06-workstreams/评衡专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-6C0659CB2B | 06-workstreams/链同专项会话状态报告.md | 开发/08-XiaoC/06-workstreams/链同专项会话状态报告.md | bidirectional | pending_api |
| GPCF-DOC-5E93C8BFBC | 06-workstreams/链同专项会话状态报告模板.md | 开发/08-XiaoC/06-workstreams/链同专项会话状态报告模板.md | bidirectional | pending_api |
| GPCF-DOC-E4854CDAC8 | 06-workstreams/链同专项执行版包-侧线程草案.md | 开发/08-XiaoC/06-workstreams/链同专项执行版包-侧线程草案.md | bidirectional | pending_api |
| GPCF-DOC-9757FCD093 | 06-workstreams/链同专项正式只读预检结论.md | 开发/12-GPCF/06-workstreams/链同专项正式只读预检结论.md | bidirectional | pending_api |
| GPCF-DOC-56B87AF669 | 06-workstreams/链同专项首轮实施前验证包.md | 开发/12-GPCF/06-workstreams/链同专项首轮实施前验证包.md | bidirectional | pending_api |
| GPCF-DOC-F204B84F5B | 06-workstreams/链同专项首轮实施前验证执行记录.md | 开发/12-GPCF/06-workstreams/链同专项首轮实施前验证执行记录.md | bidirectional | pending_api |
| GPCF-DOC-EB678B0E98 | 07-acceptance/GlobalCloud绿色供应链体系一期验收矩阵.md | 开发/91-治理与验收/07-acceptance/GlobalCloud绿色供应链体系一期验收矩阵.md | bidirectional | pending_api |
| GPCF-DOC-652F1E79A2 | 07-acceptance/README.md | 开发/91-治理与验收/07-acceptance/README.md | bidirectional | pending_api |
| GPCF-DOC-E37161A1FB | 08-evidence-samples/A23 模型使用计量与统计回指样本.md | 开发/04-WAES/08-evidence-samples/A23 模型使用计量与统计回指样本.md | bidirectional | pending_api |
| GPCF-DOC-9DAA6C3FEC | 08-evidence-samples/README.md | 开发/04-WAES/08-evidence-samples/README.md | bidirectional | pending_api |
| GPCF-DOC-71BD3638A9 | 08-evidence-samples/session-archives/README.md | 开发/92-证据与会话归档/08-evidence-samples/session-archives/README.md | bidirectional | pending_api |
| GPCF-DOC-6ACBFCD6E4 | 08-evidence-samples/session-archives/session-019eafc0-ee61-7900-b137-5cf2252bd82f.md | 开发/92-证据与会话归档/08-evidence-samples/session-archives/session-019eafc0-ee61-7900-b137-5cf2252bd82f.md | bidirectional | pending_api |
| GPCF-DOC-32B2E77806 | 08-evidence-samples/宪衡专项审批阻断与证据写入链样本.md | 开发/04-WAES/08-evidence-samples/宪衡专项审批阻断与证据写入链样本.md | bidirectional | pending_api |
| GPCF-DOC-DDC8DCF7FC | 08-evidence-samples/宪衡专项证据与审批持久化样本结构.md | 开发/04-WAES/08-evidence-samples/宪衡专项证据与审批持久化样本结构.md | bidirectional | pending_api |
| GPCF-DOC-C434D4038A | 08-evidence-samples/宪衡专项运行前样本收集记录.md | 开发/04-WAES/08-evidence-samples/宪衡专项运行前样本收集记录.md | bidirectional | pending_api |
| GPCF-DOC-DB81495EC4 | 08-evidence-samples/宪衡专项连接器阻断与状态链样本.md | 开发/04-WAES/08-evidence-samples/宪衡专项连接器阻断与状态链样本.md | bidirectional | pending_api |
| GPCF-DOC-7ACBAC23C6 | 08-evidence-samples/数枢专项运行前样本收集记录.md | 开发/04-WAES/08-evidence-samples/数枢专项运行前样本收集记录.md | bidirectional | pending_api |
| GPCF-DOC-B2E453D9F1 | 08-evidence-samples/知源专项运行前样本收集记录.md | 开发/04-WAES/08-evidence-samples/知源专项运行前样本收集记录.md | bidirectional | pending_api |
| GPCF-DOC-D77EFFB8F7 | 09-status/README.md | 开发/91-治理与验收/09-status/README.md | bidirectional | pending_api |
| GPCF-DOC-0295C05F40 | 09-status/document-deprecation-register.md | 开发/91-治理与验收/09-status/document-deprecation-register.md | bidirectional | pending_api |
| GPCF-DOC-5EF9F8EE5D | 09-status/globalcloud-document-control-register.md | 开发/91-治理与验收/09-status/globalcloud-document-control-register.md | bidirectional | pending_api |
| GPCF-DOC-71779DF3C3 | 09-status/globalcloud-document-governance-loop-gate.md | 开发/91-治理与验收/09-status/globalcloud-document-governance-loop-gate.md | bidirectional | pending_api |
| GPCF-DOC-C436DDB0F6 | 09-status/globalcloud-document-health-report.md | 开发/91-治理与验收/09-status/globalcloud-document-health-report.md | bidirectional | pending_api |
| GPCF-DOC-6CE17269E9 | 09-status/globalcloud-project-mainline-alignment-matrix.md | 开发/91-治理与验收/09-status/globalcloud-project-mainline-alignment-matrix.md | bidirectional | pending_api |
| GPCF-DOC-C586488E67 | 09-status/gpcf-project-status-matrix.md | 开发/91-治理与验收/09-status/gpcf-project-status-matrix.md | bidirectional | pending_api |
| GPCF-DOC-BA63F9BF32 | 09-status/kds-development-space-sync-register.md | 开发/91-治理与验收/09-status/kds-development-space-sync-register.md | bidirectional | pending_api |
| GPCF-DOC-A55E6422C8 | 10-archive/README.md | 开发/92-证据与会话归档/10-archive/README.md | bidirectional | pending_api |
| GPCF-DOC-5112E5A758 | 10-archive/deprecated/README.md | 开发/92-证据与会话归档/10-archive/deprecated/README.md | bidirectional | pending_api |
| GPCF-DOC-2F9D256EEE | 10-archive/historical-sessions/README.md | 开发/92-证据与会话归档/10-archive/historical-sessions/README.md | bidirectional | pending_api |
| GPCF-DOC-73C77D0200 | 10-archive/imported-legacy/README.md | 开发/92-证据与会话归档/10-archive/imported-legacy/README.md | bidirectional | pending_api |
| GPCF-DOC-36F8C5657B | 10-archive/superseded/README.md | 开发/92-证据与会话归档/10-archive/superseded/README.md | bidirectional | pending_api |
| GPCF-DOC-37DD68363F | AGENTS.md | 开发/02-GPC/AGENTS.md | bidirectional | pending_api |
| GPCF-DOC-16DD6DC90F | PROJECT_HARNESS_MANIFEST.md | 开发/01-GFIS/PROJECT_HARNESS_MANIFEST.md | bidirectional | pending_api |
| GPCF-DOC-8EC9A00BFD | README.md | 开发/00-项目群总控/README.md | bidirectional | pending_api |
| GPCF-DOC-A2F5EC5E20 | docs/GCBrain-Development-Manual.md | 开发/05-KDS/docs/GCBrain-Development-Manual.md | bidirectional | pending_api |
| GPCF-DOC-9F7CBCE127 | docs/README.md | 开发/05-KDS/docs/README.md | bidirectional | pending_api |
| GPCF-DOC-F99E5285C9 | docs/harness/README.md | 开发/05-KDS/docs/harness/README.md | bidirectional | pending_api |
| GPCF-DOC-975562EE9E | docs/harness/acceptance.md | 开发/12-GPCF/docs/harness/acceptance.md | bidirectional | pending_api |
| GPCF-DOC-D190529EF4 | docs/harness/evidence/README.md | 开发/05-KDS/docs/harness/evidence/README.md | bidirectional | pending_api |
| GPCF-DOC-27101F3BEB | docs/harness/multi-tenant-permission-design.md | 开发/05-KDS/docs/harness/multi-tenant-permission-design.md | bidirectional | pending_api |
| GPCF-DOC-40F0A4CB83 | docs/harness/status-audit-2026-06-10.md | 开发/12-GPCF/docs/harness/status-audit-2026-06-10.md | bidirectional | pending_api |
| GPCF-DOC-4F39AFF310 | openspec/README.md | 开发/05-KDS/openspec/README.md | bidirectional | pending_api |
| GPCF-DOC-855B715B04 | openspec/changes/README.md | 开发/05-KDS/openspec/changes/README.md | bidirectional | pending_api |
| GPCF-DOC-D84C374BDC | openspec/changes/archive/README.md | 开发/05-KDS/openspec/changes/archive/README.md | bidirectional | pending_api |
| GPCF-DOC-87769A72B8 | openspec/changes/kds-production-hardening/README.md | 开发/05-KDS/openspec/changes/kds-production-hardening/README.md | bidirectional | pending_api |
| GPCF-DOC-FFFA25C3EF | openspec/changes/kds-production-hardening/design.md | 开发/05-KDS/openspec/changes/kds-production-hardening/design.md | bidirectional | pending_api |
| GPCF-DOC-9630ED7C78 | openspec/changes/kds-production-hardening/proposal.md | 开发/05-KDS/openspec/changes/kds-production-hardening/proposal.md | bidirectional | pending_api |
| GPCF-DOC-D17599C829 | openspec/changes/kds-production-hardening/specs/README.md | 开发/05-KDS/openspec/changes/kds-production-hardening/specs/README.md | bidirectional | pending_api |
| GPCF-DOC-23E999A394 | openspec/changes/kds-production-hardening/specs/agent-safety-matrix/README.md | 开发/05-KDS/openspec/changes/kds-production-hardening/specs/agent-safety-matrix/README.md | bidirectional | pending_api |
| GPCF-DOC-8ECD9BA263 | openspec/changes/kds-production-hardening/specs/agent-safety-matrix/spec.md | 开发/12-GPCF/openspec/changes/kds-production-hardening/specs/agent-safety-matrix/spec.md | bidirectional | pending_api |
| GPCF-DOC-9E32DA48ED | openspec/changes/kds-production-hardening/specs/session-auth/README.md | 开发/05-KDS/openspec/changes/kds-production-hardening/specs/session-auth/README.md | bidirectional | pending_api |
| GPCF-DOC-18A2F48E80 | openspec/changes/kds-production-hardening/specs/session-auth/spec.md | 开发/12-GPCF/openspec/changes/kds-production-hardening/specs/session-auth/spec.md | bidirectional | pending_api |
| GPCF-DOC-D0174E85D8 | openspec/changes/kds-production-hardening/specs/unified-permission-middleware/README.md | 开发/05-KDS/openspec/changes/kds-production-hardening/specs/unified-permission-middleware/README.md | bidirectional | pending_api |
| GPCF-DOC-D067D700F1 | openspec/changes/kds-production-hardening/specs/unified-permission-middleware/spec.md | 开发/05-KDS/openspec/changes/kds-production-hardening/specs/unified-permission-middleware/spec.md | bidirectional | pending_api |
| GPCF-DOC-B1187FF6E1 | openspec/changes/kds-production-hardening/tasks.md | 开发/05-KDS/openspec/changes/kds-production-hardening/tasks.md | bidirectional | pending_api |
| GPCF-DOC-89FBFF25D3 | openspec/specs/README.md | 开发/05-KDS/openspec/specs/README.md | bidirectional | pending_api |
| GPCF-DOC-48D043BA78 | templates/README.md | 开发/12-GPCF/templates/README.md | bidirectional | pending_api |
| GPCF-DOC-33F4C1195D | templates/evidence-index-template.md | 开发/12-GPCF/templates/evidence-index-template.md | bidirectional | pending_api |
| GPCF-DOC-8C2AA8996B | templates/loop-audit-template.md | 开发/12-GPCF/templates/loop-audit-template.md | bidirectional | pending_api |
| GPCF-DOC-1D2FA3DB71 | templates/loop-round-template.md | 开发/12-GPCF/templates/loop-round-template.md | bidirectional | pending_api |
| GPCF-DOC-DDBD7C90C2 | templates/loop-state-template.md | 开发/12-GPCF/templates/loop-state-template.md | bidirectional | pending_api |
| GPCF-DOC-016DDA517E | tools/README.md | 开发/12-GPCF/tools/README.md | bidirectional | pending_api |
| GPCF-DOC-C039431381 | tools/kds-sync/README.md | 开发/12-GPCF/tools/kds-sync/README.md | bidirectional | pending_api |
