#!/usr/bin/env python3
"""Compile repository Python sources using short temporary bytecode names."""

from __future__ import annotations

import argparse
import os
import py_compile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".kds", ".pytest_cache", ".venv", "__pycache__", "node_modules", "tmp"}


def python_sources(root: Path) -> list[Path]:
    sources = []
    for directory, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        sources.extend(Path(directory) / name for name in files if name.endswith(".py"))
    return sorted(sources)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    failures = []
    sources = python_sources(root)
    with tempfile.TemporaryDirectory(prefix="gpcf-pycompile-") as directory:
        for index, source in enumerate(sources):
            try:
                py_compile.compile(str(source), cfile=str(Path(directory) / f"{index}.pyc"), doraise=True)
            except (OSError, py_compile.PyCompileError) as error:
                failures.append(f"{source.relative_to(root)}: {error}")
    for failure in failures:
        print(failure)
    print(f"python_bytecode={'fail' if failures else 'pass'} files={len(sources)} failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
