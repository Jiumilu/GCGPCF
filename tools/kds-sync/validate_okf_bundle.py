#!/usr/bin/env python3
"""Validate OKF v0.1 bundle conformance for derived KDS bundles."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUNDLE = ROOT / ".okf/bundles/kds-v0.1"


def fail(reason: str) -> None:
    raise SystemExit(f"okf_bundle_gate=fail reason={reason}")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        fail(f"missing_frontmatter:{rel(path)}")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"invalid_frontmatter:{rel(path)}")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            fail(f"invalid_frontmatter_line:{rel(path)}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def validate_index(path: Path, bundle: Path) -> None:
    text = read_text(path)
    if path == bundle / "index.md" and text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end == -1:
            fail(f"invalid_root_index_frontmatter:{rel(path)}")
        meta_text = text[4:end]
        if 'okf_version: "0.1"' not in meta_text and "okf_version: 0.1" not in meta_text:
            fail(f"missing_okf_version:{rel(path)}")
        body = text[end + 5 :]
    else:
        if text.startswith("---\n"):
            fail(f"frontmatter_not_allowed_in_index:{rel(path)}")
        body = text
    if not body.lstrip().startswith("# "):
        fail(f"invalid_index_structure:{rel(path)}")


def validate_log(path: Path) -> None:
    text = read_text(path)
    if text.startswith("---\n"):
        fail(f"frontmatter_not_allowed_in_log:{rel(path)}")
    if not text.lstrip().startswith("# "):
        fail(f"invalid_log_structure:{rel(path)}")
    for heading in re.findall(r"^##\s+(.+)$", text, flags=re.MULTILINE):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", heading.strip()):
            fail(f"invalid_log_date:{rel(path)}:{heading}")


def validate_concept(path: Path) -> dict[str, str]:
    meta, body = split_frontmatter(path)
    if not meta.get("type"):
        fail(f"missing_type:{rel(path)}")
    if not body.strip():
        fail(f"empty_body:{rel(path)}")
    if meta.get("source_of_record") != "kds":
        fail(f"invalid_source_of_record:{rel(path)}")
    if meta.get("derivation_policy") != "metadata_only_no_body_copy":
        fail(f"invalid_derivation_policy:{rel(path)}")
    source_path = meta.get("source_path", "")
    if not source_path:
        fail(f"missing_source_path:{rel(path)}")
    source = ROOT / source_path
    if not source.exists():
        fail(f"missing_source:{rel(path)}:{source_path}")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if meta.get("source_hash") != source_hash:
        fail(f"stale_source_hash:{rel(path)}:{source_path}")
    if f"`{source_path}`" not in body:
        fail(f"missing_source_path_citation:{rel(path)}")
    return meta


def markdown_links(path: Path) -> set[str]:
    text = read_text(path)
    return set(match.group(1) for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", default=str(DEFAULT_BUNDLE))
    args = parser.parse_args()

    bundle = (ROOT / args.bundle).resolve() if not Path(args.bundle).is_absolute() else Path(args.bundle).resolve()
    if not bundle.exists():
        fail(f"missing_bundle:{rel(bundle)}")

    concept_count = 0
    type_counts: dict[str, int] = {}
    concept_paths: set[str] = set()
    index_links: set[str] = set()
    for path in sorted(bundle.rglob("*.md")):
        if path.name == "index.md":
            validate_index(path, bundle)
            base = path.parent
            for link in markdown_links(path):
                if link.startswith(("http://", "https://", "file://", "/../")):
                    continue
                target = (base / link).resolve()
                try:
                    target.relative_to(bundle.resolve())
                except ValueError:
                    fail(f"index_link_escapes_bundle:{rel(path)}:{link}")
                if not target.exists():
                    fail(f"missing_index_link_target:{rel(path)}:{link}")
                index_links.add(target.relative_to(bundle.resolve()).as_posix())
            continue
        if path.name == "log.md":
            validate_log(path)
            continue
        meta = validate_concept(path)
        concept_count += 1
        concept_paths.add(path.relative_to(bundle).as_posix())
        type_counts[meta["type"]] = type_counts.get(meta["type"], 0) + 1

    if concept_count == 0:
        fail("empty_bundle")
    missing_backlinks = sorted(concept_paths - index_links)
    if missing_backlinks:
        fail(f"concept_not_indexed:{missing_backlinks[0]}")

    type_summary = ",".join(f"{key}:{type_counts[key]}" for key in sorted(type_counts))
    print(
        "okf_bundle_gate=pass "
        f"bundle={rel(bundle)} "
        "okf_version=0.1 "
        f"concepts={concept_count} "
        f"types={type_summary} "
        "reserved_filenames=pass frontmatter=pass source_of_record=kds "
        "derivation_policy=metadata_only_no_body_copy links=pass backlinks=pass stale=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
