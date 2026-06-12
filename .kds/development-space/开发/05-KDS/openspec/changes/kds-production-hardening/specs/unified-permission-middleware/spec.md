---
doc_id: GPCF-DOC-D067D700F1
title: Unified Permission Middleware
project: KDS
related_projects: [KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/kds-production-hardening/specs/unified-permission-middleware/spec.md
source_path: openspec/changes/kds-production-hardening/specs/unified-permission-middleware/spec.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Unified Permission Middleware

## Overview
All API routes (frontend and admin) pass through unified request identification and permission context building.

## Requirements
- Every request gets a UUID request_id
- User identified from session cookie or X-KDS-API-Key header
- Permission context built with tenant_id, role, scopes
- Tenant and sensitivity SQL filters applied at query layer
- Permission decisions return structured explanation (allowed, reason, matched_rule, tenant, role, sensitivity)
- Admin routes require authentication; frontend routes are permission-aware (filter, not block)

## Acceptance
- [ ] All requests have X-Request-ID header
- [ ] Cross-tenant data leak prevented at SQL layer
- [ ] Permission denial returns 403 with structured reason
- [ ] Frontend search returns only tenant-appropriate results
