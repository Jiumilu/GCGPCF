# Agent Safety Matrix

## Overview
Four-layer defense for AI agent code modifications: workspace isolation, patch allowlist, static risk scan, human review.

## Requirements
- Agent tasks run in isolated workspace directories
- File type restrictions: .md, .yaml, .json, .html, .css, .js only
- Path restrictions: server/core/auth.py, server/core/db.py, migrations/, scripts/deploy, scripts/backup, .env blocked
- Static scan detects: SQL DROP/DELETE/TRUNCATE, os.system, subprocess, eval, exec, rm -rf
- Risk levels: low (auto-accept), medium (human review + rollback plan), high (mandatory security review), critical (blocked)
- Every patch requires rollback plan for risk >= medium
- 6-state task machine: not_started -> in_progress -> blocked -> ready_for_human_acceptance -> accepted -> applied -> closed

## Acceptance
- [ ] Agent cannot modify auth.py, db.py, or migration files
- [ ] Dangerous SQL/shell patterns detected and flagged
- [ ] High-risk patches require human review
- [ ] Patches without rollback plan rejected at accept step
