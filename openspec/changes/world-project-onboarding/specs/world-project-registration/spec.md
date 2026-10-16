---
doc_id: GPCF-WORLD-OPENSPEC-CHANGES-WORLD-PROJECT-ONBOARDING-SPECS-WORLD-PROJECT-REGISTRATION-SPEC-MD-20261016
title: spec
project: GPCF
related_projects: [WAME, GPCF]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/world-project-onboarding/specs/world-project-registration/spec.md
source_path: openspec/changes/world-project-onboarding/specs/world-project-registration/spec.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 独立纳管与 Git 基线
系统 SHALL 在项目清单、技能链、OpenSpec 映射和 Feature 白名单登记 world，并建立独立 main 分支与私有远端；如中央门禁失败则保持 partial。

#### Scenario: 用户授权纳管
- **WHEN** 执行 World 纳管
- **THEN** 可回读唯一项目登记与本地远端一致的提交，既有代码和任务归属不变

#### Scenario: 既有门禁未通过
- **WHEN** 文档门禁返回 rework_required
- **THEN** 记录原始证据并保持 partial，不宣称项目群全量通过
