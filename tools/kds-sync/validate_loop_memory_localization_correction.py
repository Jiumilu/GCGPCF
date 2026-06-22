#!/usr/bin/env python3
"""Validate LOOP memory localization correction evidence."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs/harness/evidence/loop-five-direction-memory-localization-correction-20260622.md"
MEMORY_NOTE = Path("/Users/lujunxiang/.codex/memories/extensions/ad_hoc/notes/2026-06-22-loop-five-direction-self-evolution.md")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_loop_memory_localization_correction: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    evidence = read(EVIDENCE)
    memory = read(MEMORY_NOTE)

    for phrase in [
        "status: controlled",
        "source_path: docs/harness/evidence/loop-five-direction-memory-localization-correction-20260622.md",
        "sync_direction: bidirectional",
        "长期记忆文件",
        "localization_correction_applied",
        "默认必须使用中文",
        "外部 memory note 不在 `loop_document_gate.py` 的仓库扫描范围内",
    ]:
        require(phrase in evidence, f"evidence missing phrase: {phrase}")

    for phrase in [
        "记忆更新：GPCF LOOP 运行控制闭环自我进化",
        "LOOP 五方向` 是历史别名",
        "后续 GPCF LOOP 工作必须遵守以下规则",
        "本次偏差纠正",
        "默认必须使用中文",
    ]:
        require(phrase in memory, f"memory note missing Chinese correction phrase: {phrase}")

    forbidden = [
        "Memory update:",
        "When working in",
        "Required structure:",
        "Current completion status:",
        "Do not present this as:",
        "Use the following rule",
        "Validated evidence",
    ]
    for phrase in forbidden:
        require(phrase not in memory, f"memory note still contains English heading: {phrase}")

    print(
        "loop_memory_localization_correction=pass "
        "memory_note_language=zh "
        "status=localization_correction_applied "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
