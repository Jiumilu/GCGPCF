#!/usr/bin/env python3
"""Agent-Reach 本地授权边界。

背景：P8/P9 系列门禁建立在「本地授权文件尚未创建」的前置态上；一旦人工审批通过
（例如 GPCF-AGENT-REACH-P8-FULL-LIVE-SEARCH-BATCH-1-20260622-001，授权人 lujunxiang），
该前置态被合法取代，门禁不应再对「文件存在」本身报错。

边界定义：
- 存在且**有效**（authorization_status 以 approved 开头、expires_at 未过期）→ 合规，放行；
- 存在但**无效**（未审批 / 已过期 / 非法 JSON）→ 判失败（这才是真正需要拦的杂散授权文件）；
- 不存在 → 不判失败（前置态由其它断言负责）。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def authorization_is_valid(path: Path) -> bool:
    """本地授权文件存在且构成有效授权。"""
    if not path.is_file():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(payload, dict):
        return False
    status = str(payload.get("authorization_status") or "")
    if not status.startswith("approved"):
        return False
    expires = str(payload.get("expires_at") or "")
    try:
        return datetime.fromisoformat(expires) > datetime.now(timezone.utc)
    except ValueError:
        return False


def stray_local_authorization(path: Path) -> bool:
    """True 表示该文件存在且不构成有效授权 —— 应判失败。"""
    return path.exists() and not authorization_is_valid(path)
