---
doc_id: GPCF-DOC-18A2F48E80
title: Session Authentication
project: GPCF
related_projects: [GPCF]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/kds-production-hardening/specs/session-auth/spec.md
source_path: openspec/changes/kds-production-hardening/specs/session-auth/spec.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Session Authentication

## Overview
Replace BasicAuth with server-side session authentication and CSRF protection for admin routes.

## Requirements
- Admin login via POST /api/v1/admin/login with username/password form data
- Server-side session creation with itsdangerous signed cookies
- CSRF token generation bound to session via HMAC-SHA256
- Cookies set with HttpOnly, SameSite=Lax, Secure (production only)
- Session expiry: configurable (default 24 hours)
- All admin routes require valid session or return 401
- Logout clears session cookie

## Acceptance
- [ ] Admin login returns session cookie
- [ ] Admin routes return 401 without valid session
- [ ] CSRF tokens validate against correct session
- [ ] Expired sessions rejected
- [ ] Cookie attributes correct (HttpOnly, SameSite, Secure in production)
