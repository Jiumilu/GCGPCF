#!/usr/bin/env python3
"""Validate GPCF KDS token completion evidence without exposing the token."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/harness/evidence/gpcf_kds_access_completion_lr032.json"
DOC = ROOT / "docs/harness/gpcf-kds-access-completion-lr032.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-CF-LR-032.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def main() -> int:
    require(DATA.exists(), f"missing data: {DATA}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LOOP.exists(), f"missing loop record: {LOOP}")
    data = json.loads(DATA.read_text(encoding="utf-8"))

    code, output = run(["python3", "tools/kds-sync/validate_kds_token.py"])
    require(code == 0, output)
    require("kds_token=pass fingerprint=bfd9553d" in output, "unexpected KDS token fingerprint")

    require(data.get("round_id") == "GPCF-CF-LR-032", "round id mismatch")
    require(data.get("token_fingerprint") == "bfd9553d", "fingerprint mismatch")
    require(data.get("kds_space") == "开发", "KDS space must be 开发")
    require(set(data.get("kds_api_scope", [])) == {"read", "write", "edit"}, "KDS scope mismatch")
    require(data.get("non_development_space_access") == "denied_403", "non-development access must be denied")
    require(data.get("real_kds_sync_ran") is True, "real KDS sync must be recorded")
    require(data.get("git_push_done") is False, "git push must remain false")
    require(data.get("pr_merge_done") is False, "PR merge must remain false")
    require(data.get("accepted_or_integrated_allowed") is False, "accepted/integrated must remain false")

    for flag in [
        "token_plaintext_in_git",
        "token_plaintext_in_docs",
        "token_plaintext_in_evidence",
        "token_plaintext_in_logs",
    ]:
        require(data.get(flag) is False, f"{flag} must be false")

    text = DOC.read_text(encoding="utf-8")
    require("GPCF-CF-LR-032" in text, "doc missing round id")
    require("bfd9553d" in text, "doc missing fingerprint")
    require("Current state remains `partial`" in text, "doc must cap state")
    require("Token 未进入 Git、文档、evidence 或日志" in text, "doc missing non-leak statement")

    print("gpcf KDS access completion validation passed")
    print("kds_token=pass fingerprint=bfd9553d git_push=false pr_merge=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
