#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GlobalCloud 统一规范检查器（唯一执行源：_governance/rules/standards.yaml）。

用法示例：
    python3 _governance/tools/gc_standard.py check
    python3 _governance/tools/gc_standard.py check --repo "GlobalCloud KDS"
    python3 _governance/tools/gc_standard.py check --json
    python3 _governance/tools/gc_standard.py check --severity error --fail-on error
    python3 _governance/tools/gc_standard.py report --out _governance/reports/gc-standard-2026-10-22.md
    python3 _governance/tools/gc_standard.py explain R12
    python3 _governance/tools/gc_standard.py validate
    python3 _governance/tools/gc_standard.py rules
    python3 _governance/tools/gc_standard.py repos

设计约束：
    - 纯 Python3 标准库；不遍历整棵树（git 命令 + maxdepth 限流）。
    - 同一仓内 ls-files / ls-tree / status / for-each-ref / worktree / log 各只调用一次。
    - 规则 ID、级别、阈值、白名单全部来自 standards.yaml；本文件只实现判定逻辑。
    - 默认 --fail-on none（本地不阻断）；CI/钩子显式 --fail-on error。
"""

import argparse
import datetime
import fnmatch
import json
import os
import re
import subprocess
import sys

TOOL_VERSION = "1.0.0"

SCRIPT_PATH = os.path.abspath(__file__)
DEFAULT_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_PATH)))
# 默认从脚本位置推导项目群根：<WS>/_governance/tools/gc_standard.py

SEVERITY_RANK = {"error": 0, "warn": 1, "info": 2}
SEVERITY_ORDER = ["error", "warn", "info"]

# 规则 ID 固定顺序；validate 会校验实现与 standards.yaml 完全一致。
REQUIRED_RULE_IDS = [
    "R01-repo-name",
    "R02-registered",
    "R03-worktree-location",
    "R04-required-files",
    "R05-gitignore-coverage",
    "R06-root-md-limit",
    "R07-readme-sections",
    "R08-agents-sections",
    "R09-manifest-sections",
    "R10-docs-layout",
    "R11-stray-files",
    "R12-tracked-artifacts",
    "R13-large-tracked-files",
    "R14-dirty-worktree",
    "R15-branch-sprawl",
    "R16-doc-staleness",
    "R17-nested-repos",
    "R18-package-lock",
    "R19-venv-in-repo",
    "R20-clean-commands",
]

# 元检查（不是 20 条业务规则，只用于豁免台账自身的健康度）
META_RULE_INVALID = "EXC-invalid"
META_RULE_EXPIRED = "EXC-expired"

MAX_EVIDENCE = 600
MAX_ITEMS = 10

# R11 / R17 扫描时的剪枝目录：构建产物与依赖目录不进入遍历（避免全树扫描）
PRUNE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".venv",
    "venv",
    "coverage",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".turbo",
    "target",
    "obj",
    "bin",
    ".idea",
    ".vscode",
}
STRAY_NAME_PATTERNS = [".DS_Store", "*.tmp", "*~", "*.orig"]


# ---------------------------------------------------------------------------
# 极简 YAML 子集解析器
# 支持：映射、列表、标量、行内 [a, b] / {k: v}、整行与行尾注释（引号内除外）。
# 不支持：锚点、别名、多行块标量（| / >）、tab 缩进、复杂嵌套序列。规则文件保持简单。
# ---------------------------------------------------------------------------


class YAMLParseError(Exception):
    pass


def _strip_comment(line):
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i].rstrip()
    return line.rstrip()


def _looks_kv(text):
    if not text or text[0] in "\"'[{":
        return False
    return bool(re.match(r"^[A-Za-z0-9_][A-Za-z0-9_.\-]*\s*:", text))


def _split_flow(text):
    parts, buf, depth, quote = [], [], 0, None
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            buf.append(ch)
        elif ch in "[{(":
            depth += 1
            buf.append(ch)
        elif ch in "]})":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def _scalar(value):
    value = value.strip()
    if not value:
        return None
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        try:
            return json.loads(value)
        except ValueError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_scalar(part) for part in _split_flow(inner)]
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        result = {}
        if inner:
            for part in _split_flow(inner):
                if ":" not in part:
                    continue
                key, _, raw = part.partition(":")
                result[key.strip().strip("\"'")] = _scalar(raw)
        return result
    low = value.lower()
    if low in ("null", "~"):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def _preprocess(text):
    """展开 `- key: value`，使解析器只需处理映射/列表两种块。"""
    result = []
    for raw in text.splitlines():
        stripped = raw.rstrip()
        if not stripped.strip():
            continue
        if stripped.lstrip().startswith("#"):
            continue
        if "\t" in stripped[: len(stripped) - len(stripped.lstrip())]:
            raise YAMLParseError("不支持 tab 缩进")
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = _strip_comment(stripped.lstrip())
        if not content:
            continue
        if content.startswith("- ") and _looks_kv(content[2:]):
            result.append((indent, "-"))
            result.append((indent + 2, content[2:].strip()))
        else:
            result.append((indent, content))
    return result


def _parse_list(lines, idx, indent):
    items = []
    while idx < len(lines):
        ind, content = lines[idx]
        if ind < indent:
            break
        if ind != indent or not (content == "-" or content.startswith("- ")):
            break
        rest = content[1:].strip()
        if rest:
            items.append(_scalar(rest))
            idx += 1
            continue
        idx += 1
        if idx < len(lines) and lines[idx][0] > indent:
            value, idx = _parse_node(lines, idx)
            items.append(value)
        else:
            items.append(None)
    return items, idx


def _parse_map(lines, idx, indent):
    result = {}
    while idx < len(lines):
        ind, content = lines[idx]
        if ind < indent:
            break
        if ind > indent:
            # 缩进异常：跳过该行，保证不崩
            idx += 1
            continue
        if content == "-" or content.startswith("- "):
            break
        if ":" not in content:
            idx += 1
            continue
        key, _, raw = content.partition(":")
        key = key.strip().strip("\"'")
        raw = raw.strip()
        if raw:
            result[key] = _scalar(raw)
            idx += 1
        else:
            if idx + 1 < len(lines) and lines[idx + 1][0] > indent:
                value, idx = _parse_node(lines, idx + 1)
                result[key] = value
            else:
                result[key] = None
                idx += 1
    return result, idx


def _parse_node(lines, idx):
    ind = lines[idx][0]
    content = lines[idx][1]
    if content == "-" or content.startswith("- "):
        return _parse_list(lines, idx, ind)
    return _parse_map(lines, idx, ind)


def parse_yaml(text):
    lines = _preprocess(text)
    if not lines:
        return None
    value, idx = _parse_node(lines, 0)
    if idx != len(lines):
        raise YAMLParseError("无法解析第 %d 个有效行：%r" % (idx + 1, lines[idx][1]))
    return value


# ---------------------------------------------------------------------------
# 配置加载与校验
# ---------------------------------------------------------------------------


class ConfigError(Exception):
    pass


class UsageError(Exception):
    pass


def _read_file(path, limit=None, errors="replace"):
    try:
        with open(path, "r", encoding="utf-8", errors=errors) as handle:
            return handle.read() if limit is None else handle.read(limit)
    except OSError:
        return ""


def load_yaml(path):
    text = _read_file(path)
    if not text:
        raise ConfigError("文件不存在或为空：%s" % path)
    try:
        return parse_yaml(text)
    except YAMLParseError as exc:
        raise ConfigError("YAML 解析失败 %s：%s" % (path, exc))


def load_standards(ws):
    path = os.path.join(ws, "_governance", "rules", "standards.yaml")
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ConfigError("standards.yaml 顶层必须是映射")
    for section in ("workspace", "gitignore", "root_md", "thresholds", "rules"):
        if section not in data:
            raise ConfigError("standards.yaml 缺少段：%s" % section)

    rules = data["rules"]
    if not isinstance(rules, list):
        raise ConfigError("standards.yaml rules 必须是列表")
    ids = [rule.get("id") for rule in rules if isinstance(rule, dict)]
    missing = [rid for rid in REQUIRED_RULE_IDS if rid not in ids]
    if missing:
        raise ConfigError("standards.yaml 缺少规则：%s" % ", ".join(missing))
    extra = [rid for rid in ids if rid not in REQUIRED_RULE_IDS]
    if extra:
        raise ConfigError("standards.yaml 存在未实现规则：%s" % ", ".join(extra))
    if len(ids) != len(set(ids)):
        raise ConfigError("standards.yaml 规则 ID 重复")
    for rule in rules:
        rid = rule.get("id")
        if not rid:
            raise ConfigError("规则缺少 id")
        if rule.get("severity") not in SEVERITY_RANK:
            raise ConfigError("规则 %s 的 severity 非法：%r" % (rid, rule.get("severity")))
        for field in ("title", "description", "fix_hint"):
            if not str(rule.get(field) or "").strip():
                raise ConfigError("规则 %s 缺少 %s" % (rid, field))

    thresholds = data["thresholds"]
    for key in (
        "dirty_warn",
        "dirty_error",
        "branch_warn",
        "branch_error",
        "branch_stale_days",
        "doc_stale_days",
        "large_file_mb",
        "scan_maxdepth",
        "nested_repo_maxdepth",
    ):
        if not isinstance(thresholds.get(key), int) or thresholds[key] < 0:
            raise ConfigError("thresholds.%s 必须是非负整数" % key)
    if thresholds["dirty_warn"] > thresholds["dirty_error"]:
        raise ConfigError("thresholds.dirty_warn 不得大于 dirty_error")
    if thresholds["branch_warn"] > thresholds["branch_error"]:
        raise ConfigError("thresholds.branch_warn 不得大于 branch_error")

    for item in data["gitignore"]["required"]:
        if not item.get("key") or not item.get("patterns"):
            raise ConfigError("gitignore.required 条目缺少 key/patterns")
    data["_path"] = path
    data["_rules_by_id"] = {rule["id"]: rule for rule in rules}
    return data


def load_registry(ws, cfg):
    rel = cfg.get("sources", {}).get("registry") or ""
    path = os.path.join(ws, rel)
    data = load_yaml(path)
    projects = data.get("projects") if isinstance(data, dict) else None
    if not isinstance(projects, list) or not projects:
        raise ConfigError("注册表 %s 缺少 projects 列表" % path)
    normalized = []
    for item in projects:
        if not isinstance(item, dict) or not item.get("repo"):
            raise ConfigError("注册表条目非法：%r" % (item,))
        normalized.append(item)
    data["_path"] = path
    data["_projects"] = normalized
    return data


def load_exceptions(ws, cfg):
    """返回 (有效豁免, 台账问题列表)。有效豁免字段：repo/rule/reason/until/approved_by。"""
    rel = cfg.get("exceptions", {}).get("file") or "_governance/rules/exceptions.yaml"
    path = os.path.join(ws, rel)
    if not os.path.exists(path):
        return [], [], path
    data = load_yaml(path)
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        entries = data.get("exceptions") or []
    else:
        raise ConfigError("exceptions.yaml 顶层必须是列表或含 exceptions 的映射")
    required = cfg.get("exceptions", {}).get("required_fields") or [
        "repo",
        "rule",
        "reason",
        "until",
    ]
    valid, problems = [], []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            problems.append({"index": index, "repo": "*", "message": "第 %d 条豁免不是映射" % index})
            continue
        missing = [field for field in required if not str(entry.get(field) or "").strip()]
        if missing:
            problems.append(
                {
                    "index": index,
                    "repo": str(entry.get("repo") or "*"),
                    "message": "第 %d 条豁免缺少必填字段：%s" % (index, "/".join(missing)),
                }
            )
            continue
        until_raw = str(entry["until"]).strip()
        try:
            until = datetime.date.fromisoformat(until_raw)
        except ValueError:
            problems.append(
                {
                    "index": index,
                    "repo": str(entry["repo"]),
                    "message": "第 %d 条豁免 until 不是 YYYY-MM-DD：%r" % (index, until_raw),
                }
            )
            continue
        valid.append(
            {
                "index": index,
                "repo": str(entry["repo"]).strip(),
                "rule": str(entry["rule"]).strip(),
                "reason": str(entry["reason"]).strip(),
                "until": until,
                "approved_by": str(entry.get("approved_by") or "").strip(),
                "path": os.path.relpath(path, ws).replace(os.sep, "/"),
            }
        )
    return valid, problems, path


# ---------------------------------------------------------------------------
# git 辅助
# ---------------------------------------------------------------------------


class GitError(Exception):
    pass


def git_run(repo_path, args, timeout=120, stdin_text=None):
    command = ["git", "--no-optional-locks", "-C", repo_path, "-c", "core.quotepath=false"] + args
    try:
        proc = subprocess.run(
            command,
            input=stdin_text,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitError(str(exc))
    if proc.returncode != 0:
        raise GitError((proc.stderr or "").strip().splitlines()[-1] if proc.stderr else "git 返回 %d" % proc.returncode)
    return proc.stdout


def is_git_dir(path):
    return os.path.isdir(os.path.join(path, ".git")) or os.path.isfile(os.path.join(path, ".git"))


def _real(path):
    try:
        return os.path.realpath(path)
    except OSError:
        return os.path.abspath(path)


def _inside(path, root):
    try:
        return os.path.commonpath([_real(path), _real(root)]) == _real(root)
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# 仓库目标与数据采集
# ---------------------------------------------------------------------------


class RepoEntry:
    __slots__ = ("name", "path", "is_git", "registered", "missing", "is_symlink", "project")

    def __init__(self, name, path, is_git, registered, missing, is_symlink, project=None):
        self.name = name
        self.path = path
        self.is_git = is_git
        self.registered = registered
        self.missing = missing
        self.is_symlink = is_symlink
        self.project = project or {}


def discover_targets(ws, cfg, reg_by_repo):
    workspace_cfg = cfg["workspace"]
    exempt = set(workspace_cfg.get("exempt_top_dirs") or [])
    prefixes = tuple(workspace_cfg.get("exempt_name_prefixes") or [])
    targets = []
    seen = set()
    try:
        names = sorted(os.listdir(ws))
    except OSError as exc:
        raise ConfigError("无法读取工作区 %s：%s" % (ws, exc))
    for name in names:
        path = os.path.join(ws, name)
        if name.startswith(".") or name.startswith(prefixes):
            continue
        if name in exempt:
            continue
        if not os.path.isdir(path):
            continue
        git_repo = is_git_dir(path)
        project = reg_by_repo.get(name)
        if not git_repo and project is None:
            continue
        targets.append(
            RepoEntry(
                name=name,
                path=path,
                is_git=git_repo,
                registered=project is not None,
                missing=False,
                is_symlink=os.path.islink(path),
                project=project,
            )
        )
        seen.add(name)
    # 注册了但目录不存在
    for repo_name, project in reg_by_repo.items():
        if repo_name in seen:
            continue
        targets.append(
            RepoEntry(
                name=repo_name,
                path=os.path.join(ws, repo_name),
                is_git=False,
                registered=True,
                missing=True,
                is_symlink=False,
                project=project,
            )
        )
    return targets


def select_targets(targets, spec):
    spec_l = spec.strip().lower()
    exact = [item for item in targets if item.name.lower() == spec_l]
    if exact:
        return exact
    by_project = [
        item
        for item in targets
        if item.project
        and spec_l
        in (
            str(item.project.get("id", "")).lower(),
            str(item.project.get("slug", "")).lower(),
        )
    ]
    if by_project:
        return by_project
    return [item for item in targets if spec_l in item.name.lower()]


def scan_tree(root, maxdepth, max_entries=20000):
    """限流扫描：返回散落物、嵌套 .git、venv 目录。只做目录枚举，不读文件内容。"""
    stray, nested, venv_dirs = [], [], []
    state = {"count": 0, "truncated": False}

    def walk(dirpath, depth):
        if state["truncated"]:
            return
        try:
            entries = list(os.scandir(dirpath))
        except OSError:
            return
        for entry in entries:
            state["count"] += 1
            if state["count"] > max_entries:
                state["truncated"] = True
                return
            name = entry.name
            try:
                rel = os.path.relpath(entry.path, root).replace(os.sep, "/")
            except ValueError:
                continue
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
                is_file = entry.is_file(follow_symlinks=False)
            except OSError:
                continue
            if name == ".git":
                if depth > 0:
                    nested.append(rel)
                continue
            if is_dir:
                if name in (".venv", "venv"):
                    venv_dirs.append(rel)
                if name in PRUNE_DIRS:
                    continue
                if depth < maxdepth:
                    walk(entry.path, depth + 1)
            elif is_file:
                if name == ".env" or any(fnmatch.fnmatchcase(name, pat) for pat in STRAY_NAME_PATTERNS):
                    stray.append(rel)

    walk(root, 0)
    return {
        "stray": stray,
        "nested": nested,
        "venv": venv_dirs,
        "truncated": state["truncated"],
    }


class RepoData:
    def __init__(self, entry, ws, cfg, staged_only):
        self.entry = entry
        self.name = entry.name
        self.path = entry.path
        self.ws = ws
        self.cfg = cfg
        self.staged_only = staged_only
        self.exists = os.path.isdir(self.path)
        self.is_git = bool(entry.is_git and self.exists)
        self.registered = entry.registered
        self.missing = entry.missing
        self.is_symlink = entry.is_symlink
        self.project = entry.project
        self.ls_files = []
        self.tree = []
        self.status_lines = []
        self.branches = []
        self.worktrees = []
        self.last_commit_ts = None
        self.staged_files = []
        self.root_entries = []
        self.scan = {"stray": [], "nested": [], "venv": [], "truncated": False}
        self.git_errors = []
        self.gitignore_lines = []

    # -- 基础读取 ---------------------------------------------------------
    def root_file(self, name):
        return os.path.isfile(os.path.join(self.path, name))

    def read_root(self, name, limit=300000):
        return _read_file(os.path.join(self.path, name), limit=limit)

    def rel(self, path):
        return path.replace(os.sep, "/")

    def git_lines(self, args):
        if not self.is_git:
            return []
        try:
            return [line for line in git_run(self.path, args).splitlines() if line.strip()]
        except GitError as exc:
            self.git_errors.append("%s: %s" % (" ".join(args), exc))
            return []

    # -- 一次性采集 -------------------------------------------------------
    def collect(self):
        if not self.exists:
            return
        try:
            self.root_entries = sorted(os.listdir(self.path))
        except OSError:
            self.root_entries = []
        scan_depth = min(
            self.cfg["thresholds"]["scan_maxdepth"],
            self.cfg["thresholds"]["nested_repo_maxdepth"],
        )
        self.scan = scan_tree(self.path, scan_depth)
        self.gitignore_lines = _read_file(os.path.join(self.path, ".gitignore")).splitlines()
        if not self.is_git:
            return
        self.ls_files = self.git_lines(["ls-files"])
        self.tree = self._collect_tree()
        self.status_lines = self.git_lines(["status", "--porcelain", "-uall"])
        self._collect_branches()
        self._collect_worktrees()
        self._collect_last_commit()
        if self.staged_only:
            self.staged_files = self.git_lines(
                ["diff", "--cached", "--name-only", "--diff-filter=ACMR"]
            )

    def _collect_tree(self):
        """git ls-tree -r -l HEAD → [(size, path)]；无 HEAD 时返回空。"""
        if not self.is_git:
            return []
        try:
            output = git_run(self.path, ["ls-tree", "-r", "-l", "HEAD"])
        except GitError as exc:
            # 空仓（无 HEAD）视为正常
            message = str(exc)
            if "unknown revision" not in message and "bad revision" not in message:
                self.git_errors.append("ls-tree: %s" % message)
            return []
        files = []
        for line in output.splitlines():
            if "\t" not in line:
                continue
            meta, path = line.split("\t", 1)
            parts = meta.split()
            if len(parts) < 4 or not parts[3].isdigit():
                continue
            files.append((int(parts[3]), path))
        return files

    def _collect_branches(self):
        lines = self.git_lines(
            ["for-each-ref", "--format=%(refname:short)%09%(committerdate:unix)", "refs/heads"]
        )
        branches = []
        for line in lines:
            if "\t" not in line:
                continue
            name, _, ts = line.partition("\t")
            try:
                branches.append((name.strip(), int(ts.strip())))
            except ValueError:
                continue
        self.branches = branches

    def _collect_worktrees(self):
        lines = self.git_lines(["worktree", "list", "--porcelain"])
        blocks, current = [], {}
        for line in lines:
            if line.startswith("worktree "):
                if current:
                    blocks.append(current)
                current = {"path": line[len("worktree ") :].strip()}
            elif line.startswith("branch "):
                current["branch"] = line[len("branch ") :].strip()
            elif line.startswith("HEAD "):
                current["head"] = line[len("HEAD ") :].strip()
            elif line == "detached":
                current["detached"] = True
            elif line.startswith("prunable"):
                current["prunable"] = True
        if current:
            blocks.append(current)
        self.worktrees = blocks

    def _collect_last_commit(self):
        lines = self.git_lines(["log", "-1", "--format=%ct"])
        if lines:
            try:
                self.last_commit_ts = int(lines[0].strip())
            except ValueError:
                self.last_commit_ts = None


# ---------------------------------------------------------------------------
# 通用启发式
# ---------------------------------------------------------------------------


def _gitignore_tokens(lines):
    tokens = set()
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            line = line[1:]
        line = line.replace("**/", "").strip().strip("/")
        for token in line.split("/"):
            token = token.strip().lower()
            if token and token not in ("*", "**"):
                tokens.add(token)
    return tokens


def _covers(tokens, patterns):
    for pattern in patterns:
        pat = str(pattern).lower().replace("**/", "").strip().strip("/")
        if not pat:
            continue
        for token in tokens:
            if token == pat:
                return pattern
            if fnmatch.fnmatchcase(token, pat) or fnmatch.fnmatchcase(pat, token):
                return pattern
    return None


def _missing_sections(text, specs):
    headings = [
        re.sub(r"^#{1,6}\s*", "", line).strip().lower()
        for line in text.splitlines()
        if re.match(r"^#{1,6}\s", line)
    ]
    body = text[:12000].lower()
    missing = []
    for spec in specs:
        patterns = [str(pat).lower() for pat in spec.get("patterns", [])]
        hit = None
        for heading in headings:
            for pattern in patterns:
                if pattern in heading:
                    hit = pattern
                    break
            if hit:
                break
        if not hit:
            for pattern in patterns:
                if pattern in body:
                    hit = pattern
                    break
        if not hit:
            missing.append(spec.get("key", "?"))
    return missing


def _has_test_entry(repo):
    readme = repo.read_root("README.md")
    readme_patterns = re.compile(
        r"(make\s+test|pytest|npm\s+(run\s+)?test|pnpm\s+(run\s+)?test|yarn\s+(run\s+)?test|"
        r"go\s+test|cargo\s+test|mvn\s+test|gradle\s+test|dotnet\s+test|python3?\s+-m\s+pytest)",
        re.IGNORECASE,
    )
    if readme_patterns.search(readme):
        return True
    for name in ("Makefile", "makefile", "GNUmakefile"):
        text = repo.read_root(name)
        if not text:
            continue
        # 只把“有真实命令”的 test/check 目标算作入口；纯 @echo 占位不算（避免 Makefile 骨架虚增通过）
        current = None
        has_real = {}
        for line in text.splitlines():
            if not line.startswith(("\t", " ")) and re.match(r"^[A-Za-z0-9_.-]+\s*:", line):
                current = line.split(":", 1)[0].strip()
                has_real.setdefault(current, False)
                continue
            if current and line.startswith("\t"):
                command = line.strip()
                if command and not command.startswith("#") and not re.match(r"@?echo\b", command):
                    has_real[current] = True
        if any(has_real.get(target) for target in ("test", "tests", "check", "verify")):
            return True
    package_json = repo.read_root("package.json")
    if package_json:
        try:
            data = json.loads(package_json)
        except ValueError:
            data = {}
        scripts = data.get("scripts") if isinstance(data, dict) else None
        if isinstance(scripts, dict):
            for key, value in scripts.items():
                if "test" in str(key).lower() or "test" in str(value).lower():
                    return True
    pyproject = repo.read_root("pyproject.toml")
    if pyproject and ("pytest" in pyproject or "[tool.pytest" in pyproject):
        return True
    return False


def _fmt_size(num):
    return "%.1fMB" % (num / 1048576.0)


def _sample(items, limit=MAX_ITEMS):
    items = list(items)
    shown = items[:limit]
    text = "、".join(shown)
    if len(items) > limit:
        text += " …（共 %d 条）" % len(items)
    return text


# ---------------------------------------------------------------------------
# 结果容器与上下文
# ---------------------------------------------------------------------------


class CheckContext:
    def __init__(self, ws, cfg, staged_only):
        self.ws = ws
        self.cfg = cfg
        self.staged_only = staged_only
        self.violations = []
        self.git_notes = []
        # R03 去重：同一物理 worktree 只报一次（避免主仓与链表互相重复报）
        self.reported_worktrees = set()

    def add(self, repo, rule_id, message, severity=None, path="", evidence="", fix_hint=None):
        meta = self.cfg["_rules_by_id"].get(rule_id) or {}
        self.violations.append(
            {
                "rule": rule_id,
                "severity": severity or meta.get("severity", "warn"),
                "repo": repo.name if hasattr(repo, "name") else str(repo),
                "path": path or ".",
                "message": message,
                "evidence": str(evidence)[:MAX_EVIDENCE],
                "fix_hint": fix_hint or meta.get("fix_hint", ""),
            }
        )


# ---------------------------------------------------------------------------
# 20 条规则
# ---------------------------------------------------------------------------


def check_R01(ctx, repo):
    """仓库目录名：拼写错误 / worktree 后缀 / 软链 / 待改名 / 正则。"""
    name = repo.name
    workspace_cfg = ctx.cfg["workspace"]
    typos = set(workspace_cfg.get("known_name_typos") or [])
    pending = set(workspace_cfg.get("pending_rename_dirs") or [])
    suffixes = workspace_cfg.get("worktree_bad_suffixes") or []
    pattern = workspace_cfg.get("project_name_regex") or r"^GlobalCloud [A-Za-z0-9. -]+$"

    if repo.missing:
        return
    if repo.is_symlink:
        ctx.add(
            repo,
            "R01-repo-name",
            "仓库目录是软链，注册表与实际目录名不一致",
            path=name,
            evidence="%s -> %s" % (name, _real(repo.path)),
            fix_hint="删除软链，统一物理目录名并同步注册表 repo 字段。",
        )
        return
    if name in typos:
        ctx.add(
            repo,
            "R01-repo-name",
            "仓库目录名拼写错误（少字母）",
            path=name,
            evidence="目录名：%s；正确写法应为 GlobalCloud GPCF" % name,
            fix_hint="改名并同步注册表与所有引用（需老卢授权 G5）。",
        )
        return
    bad_suffix = next((suffix for suffix in suffixes if name.endswith(suffix)), None)
    if bad_suffix:
        ctx.add(
            repo,
            "R01-repo-name",
            "仓库目录名带 worktree 后缀 %s" % bad_suffix,
            path=name,
            evidence="目录名：%s" % name,
            fix_hint="worktree 移到 ~/Projects/_wt/<repo>--<branch>/，根目录只留主仓。",
        )
        return
    if name in pending:
        ctx.add(
            repo,
            "R01-repo-name",
            "目录名为待改名中文名，需按注册表迁移",
            severity="warn",
            path=name,
            evidence="目录名：%s；规则允许临时存在，但须登记豁免并限期改名" % name,
        )
        return
    if not re.match(pattern, name):
        ctx.add(
            repo,
            "R01-repo-name",
            "仓库目录名不符合命名规范",
            path=name,
            evidence="目录名：%s；要求匹配 %s" % (name, pattern),
        )


def check_R02(ctx, repo):
    """注册表登记：注册但缺失 / 未注册独立 git 仓。"""
    if repo.missing:
        registry = ctx.cfg.get("sources", {}).get("registry", "注册表")
        ctx.add(
            repo,
            "R02-registered",
            "注册表登记了该仓，但工作区目录不存在",
            path=".",
            evidence="registry=%s；missing dir=%s" % (registry, repo.name),
            fix_hint="恢复项目目录，或走退役流程从注册表移除。",
        )
        return
    if repo.registered:
        return
    if repo.is_git:
        ctx.add(
            repo,
            "R02-registered",
            "未注册的独立 git 仓",
            path=".",
            evidence="顶层 git 仓 %s 不在 project-group-projects.yaml 的 repo 字段" % repo.name,
            fix_hint="在注册表登记（新项目准入）或归档到 _archive/ 后移除工作区顶层目录。",
        )


def check_R03(ctx, repo):
    """worktree 位置：项目群根内的 worktree。

    `git worktree list` 第一块是主 worktree（项目仓自身或主仓路径），不是“新增 worktree”，跳过；
    其余链表条目若位于 WS 根内则报 info；同一物理路径全群只报一次（避免主仓/链表互报）。
    """
    if not repo.is_git:
        return
    ws_real = _real(ctx.ws)
    for index, worktree in enumerate(repo.worktrees):
        if index == 0:
            continue
        path = worktree.get("path") or ""
        if not path:
            continue
        key = _real(path)
        if key == _real(repo.path):
            continue
        if not _inside(path, ws_real):
            continue
        if key in ctx.reported_worktrees:
            continue
        ctx.reported_worktrees.add(key)
        branch = worktree.get("branch") or ("detached" if worktree.get("detached") else "(unknown)")
        flag = "prunable" if worktree.get("prunable") else "live"
        ctx.add(
            repo,
            "R03-worktree-location",
            "项目群根目录内存在 worktree（%s）" % flag,
            path=os.path.relpath(path, ctx.ws).replace(os.sep, "/"),
            evidence="worktree=%s branch=%s state=%s" % (path, branch, flag),
            fix_hint="把 worktree 移到 ~/Projects/_wt/<repo>--<branch>/；prunable 的先 git worktree prune。",
        )


def check_R04(ctx, repo):
    """四件套齐全：缺一报一条。"""
    if repo.missing or not repo.exists:
        return
    for filename in ctx.cfg["workspace"].get("required_files") or []:
        if not repo.root_file(filename):
            ctx.add(
                repo,
                "R04-required-files",
                "缺少必需文件 %s" % filename,
                path=filename,
                evidence="%s 不存在" % os.path.join(repo.name, filename),
                fix_hint="从 _governance/templates/ 复制统一模板补齐。",
            )


def check_R05(ctx, repo):
    """gitignore 覆盖 12 类；至少 8/12。"""
    if repo.missing or not repo.exists:
        return
    tokens = _gitignore_tokens(repo.gitignore_lines)
    required = ctx.cfg["gitignore"]["required"]
    min_coverage = int(ctx.cfg["gitignore"].get("min_coverage") or 8)
    hits, missing = [], []
    for item in required:
        matched = _covers(tokens, item.get("patterns") or [])
        if matched:
            hits.append(item["key"])
        else:
            missing.append(item["key"])
    if len(hits) >= min_coverage:
        return
    ctx.add(
        repo,
        "R05-gitignore-coverage",
        "忽略规则覆盖不足：命中 %d/%d，低于阈值 %d" % (len(hits), len(required), min_coverage),
        path=".gitignore",
        evidence="缺失项：%s；命中项：%s" % (", ".join(missing), ", ".join(hits) or "无"),
        fix_hint="以 _governance/templates/gitignore.template 为基础合并缺失项。",
    )


def check_R06(ctx, repo):
    """根目录一级 .md 数量 ≤ limit。"""
    if repo.missing or not repo.exists:
        return
    root_cfg = ctx.cfg["root_md"]
    limit = int(root_cfg.get("limit") or 6)
    allow_names = {str(name).lower() for name in (root_cfg.get("allow_names") or [])}
    allow_globs = root_cfg.get("allow_globs") or []
    counted = []
    for name in repo.root_entries:
        if not name.lower().endswith(".md"):
            continue
        if name.lower() in allow_names:
            continue
        if any(fnmatch.fnmatchcase(name, pat) for pat in allow_globs):
            continue
        if repo.root_file(name):
            counted.append(name)
    if len(counted) > limit:
        ctx.add(
            repo,
            "R06-root-md-limit",
            "根目录 .md 数量 %d 超过上限 %d" % (len(counted), limit),
            path=".",
            evidence=_sample(sorted(counted), limit=20),
            fix_hint="过程性文档归位 docs/changelog、docs/reports、docs/archive。",
        )


def _section_rule(ctx, repo, rule_id, filename, section_key):
    if repo.missing or not repo.exists:
        return
    text = repo.read_root(filename)
    if not text:
        return
    missing = _missing_sections(text, ctx.cfg.get(section_key) or [])
    if missing:
        ctx.add(
            repo,
            rule_id,
            "%s 缺少段落：%s" % (filename, "、".join(missing)),
            path=filename,
            evidence="缺失段落：%s" % "、".join(missing),
            fix_hint="按 _governance/templates/ 对应模板重排章节，保留原内容。",
        )


def check_R07(ctx, repo):
    _section_rule(ctx, repo, "R07-readme-sections", "README.md", "readme_sections")


def check_R08(ctx, repo):
    _section_rule(ctx, repo, "R08-agents-sections", "AGENTS.md", "agents_sections")


def check_R09(ctx, repo):
    _section_rule(ctx, repo, "R09-manifest-sections", "PROJECT_HARNESS_MANIFEST.md", "manifest_sections")


def check_R10(ctx, repo):
    """根目录源码文件与过程性散落物。"""
    if repo.missing or not repo.exists:
        return
    layout = ctx.cfg["docs_layout"]
    extensions = [str(ext).lower() for ext in (layout.get("source_extensions") or [])]
    allow_root_globs = list(layout.get("allow_root_globs") or [])
    allow_root_globs += list((layout.get("root_source_allowlist") or {}).get(repo.name) or [])
    scattered = layout.get("scattered") or []
    for name in repo.root_entries:
        if not repo.root_file(name):
            continue
        lower = name.lower()
        if any(lower.endswith(ext) for ext in extensions):
            if any(fnmatch.fnmatchcase(name, pat) for pat in allow_root_globs):
                continue
            ctx.add(
                repo,
                "R10-docs-layout",
                "根目录直接放置源码文件 %s" % name,
                path=name,
                evidence="根目录源码文件：%s" % name,
                fix_hint="源码移入 src/（或项目既有源码目录）。",
            )
            continue
        for item in scattered:
            glob = item.get("glob") or ""
            if glob and fnmatch.fnmatchcase(name, glob):
                ctx.add(
                    repo,
                    "R10-docs-layout",
                    "根目录存在过程性散落文件 %s" % name,
                    path=name,
                    evidence="匹配 %s；建议归位 %s" % (glob, item.get("suggestion") or "docs/"),
                    fix_hint="移动到 %s。" % (item.get("suggestion") or "docs/"),
                )
                break


def check_R11(ctx, repo):
    """散落垃圾文件：.DS_Store / *.tmp / *~ / *.orig / .env。

    staged-only（pre-commit）模式只看暂存区，避免把本地历史垃圾算到本次提交头上。
    """
    if repo.missing or not repo.exists:
        return
    if ctx.staged_only:
        stray = [
            path
            for path in repo.staged_files
            if os.path.basename(path) == ".env"
            or any(fnmatch.fnmatchcase(os.path.basename(path), pat) for pat in STRAY_NAME_PATTERNS)
        ]
        scan_hint = "暂存区"
    else:
        tracked = set(repo.ls_files) if repo.is_git else set()
        stray = [
            p
            for p in (repo.scan.get("stray") or [])
            if os.path.basename(p) != ".env" or p in tracked
        ]
        scan_hint = "限 maxdepth %d" % ctx.cfg["stray"].get("maxdepth", 3)
        if repo.scan.get("truncated"):
            ctx.git_notes.append("%s: 目录扫描达到上限，R11/R17 结果可能不完整" % repo.name)
    if stray:
        ctx.add(
            repo,
            "R11-stray-files",
            "发现 %d 个散落垃圾文件（%s）" % (len(stray), scan_hint),
            path=".",
            evidence="、".join(stray[:MAX_ITEMS])
            + (" …（共 %d 条）" % len(stray) if len(stray) > MAX_ITEMS else ""),
            fix_hint="删除本地垃圾文件；.env 用 .env.example 代替并写入 .gitignore。",
        )


def _artifact_hits(paths, limit=MAX_ITEMS):
    pattern = re.compile(
        r"(^|/)(node_modules|dist|build|\.next|\.venv|venv|coverage|__pycache__)(/|$)"
    )
    hits = [path for path in paths if pattern.search(path)]
    return hits


def check_R12(ctx, repo):
    if not repo.is_git:
        return
    source = repo.staged_files if ctx.staged_only else repo.ls_files
    if ctx.staged_only and not source:
        return
    hits = _artifact_hits(source)
    if not hits:
        return
    ctx.add(
        repo,
        "R12-tracked-artifacts",
        "检测到 %d 个构建产物/依赖路径被 git 跟踪" % len(hits),
        path=hits[0],
        evidence="前 %d 条：%s" % (min(len(hits), MAX_ITEMS), _sample(hits)),
        fix_hint="git rm -r --cached <path>，把规则写入 .gitignore 后重新提交。",
    )


def _large_whitelist(cfg, repo_name):
    for item in cfg["thresholds"].get("large_file_whitelist") or []:
        if item.get("repo") == repo_name:
            return {str(ext).lower() for ext in (item.get("extensions") or [])}
    return set()


def check_R13(ctx, repo):
    if not repo.is_git:
        return
    threshold = int(ctx.cfg["thresholds"]["large_file_mb"]) * 1024 * 1024
    allowed_ext = _large_whitelist(ctx.cfg, repo.name)
    big = []
    if ctx.staged_only:
        for path in repo.staged_files:
            full = os.path.join(repo.path, path)
            try:
                size = os.path.getsize(full)
            except OSError:
                continue
            if size <= threshold:
                continue
            if os.path.splitext(path)[1].lower() in allowed_ext:
                continue
            big.append((size, path))
    else:
        for size, path in repo.tree:
            if size <= threshold:
                continue
            if os.path.splitext(path)[1].lower() in allowed_ext:
                continue
            big.append((size, path))
    if not big:
        return
    big.sort(reverse=True)
    evidence = "、".join("%s (%s)" % (path, _fmt_size(size)) for size, path in big[:MAX_ITEMS])
    if len(big) > MAX_ITEMS:
        evidence += " …（共 %d 个）" % len(big)
    ctx.add(
        repo,
        "R13-large-tracked-files",
        "存在 %d 个 >%dMB 的跟踪文件" % (len(big), int(ctx.cfg["thresholds"]["large_file_mb"])),
        path=big[0][1],
        evidence=evidence,
        fix_hint="大文件移出仓库（对象存储/归档）；媒体资产走白名单，非媒体不得入库。",
    )


def _status_path(line):
    """从 porcelain 行提取路径（处理 git 的 C 风格引号/八进制转义）。"""
    p = line[3:] if len(line) > 3 else ""
    if p.startswith('"') and p.endswith('"'):
        raw = p[1:-1]
        try:
            import codecs

            p = codecs.escape_decode(raw.encode("utf-8"))[0].decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            p = raw
    return p


def check_R14(ctx, repo):
    if not repo.is_git or ctx.staged_only:
        return
    zones = (ctx.cfg.get("dirty_zones") or {}).get("repos", {}).get(repo.name, [])
    if zones:
        exempt = sum(1 for ln in repo.status_lines if any(_status_path(ln).startswith(z) for z in zones))
        counted_lines = [ln for ln in repo.status_lines if not any(_status_path(ln).startswith(z) for z in zones)]
    else:
        exempt, counted_lines = 0, list(repo.status_lines)
    count = len(counted_lines or [])
    if count == 0 and exempt == 0:
        return
    thresholds = ctx.cfg["thresholds"]
    if count > thresholds["dirty_error"]:
        severity = "error"
    elif count > thresholds["dirty_warn"]:
        severity = "warn"
    else:
        severity = "info"
    sample = "；".join(line[:100] for line in (counted_lines or repo.status_lines)[:5])
    zone_note = "；其中 %d 条在已声明的治理可脏区内（04 §4）" % exempt if exempt else ""
    ctx.add(
        repo,
        "R14-dirty-worktree",
        "可脏区之外有 %d 条未提交变更（阈值 warn %d / error %d）%s"
        % (count, thresholds["dirty_warn"], thresholds["dirty_error"], zone_note),
        severity=severity,
        path=".",
        evidence="样例：%s" % sample,
        fix_hint="治理产物与产品代码分开提交；收工前在交接中登记脏条目清单。",
    )


def check_R15(ctx, repo):
    if not repo.is_git or ctx.staged_only:
        return
    thresholds = ctx.cfg["thresholds"]
    now = int(datetime.datetime.now().timestamp())
    stale_seconds = thresholds["branch_stale_days"] * 86400
    branch_count = len(repo.branches)
    stale = [name for name, ts in repo.branches if ts and ts < now - stale_seconds]
    if branch_count > thresholds["branch_error"]:
        severity = "error"
    elif branch_count > thresholds["branch_warn"]:
        severity = "warn"
    elif stale:
        severity = "info"
    else:
        return
    ctx.add(
        repo,
        "R15-branch-sprawl",
        "本地分支 %d 个（阈值 warn %d / error %d），其中 %d 个分支 %d 天未提交"
        % (
            branch_count,
            thresholds["branch_warn"],
            thresholds["branch_error"],
            len(stale),
            thresholds["branch_stale_days"],
        ),
        severity=severity,
        path=".",
        evidence="陈旧分支：%s" % (_sample(sorted(stale)) if stale else "无"),
        fix_hint="合并/删除已完成分支；长期分支转 worktree 或归档，保留 main + 活跃分支。",
    )


def check_R16(ctx, repo):
    if ctx.staged_only:
        return
    if not repo.registered or repo.missing or not repo.is_git or repo.last_commit_ts is None:
        return
    threshold = ctx.cfg["thresholds"]["doc_stale_days"]
    now = int(datetime.datetime.now().timestamp())
    age_days = (now - repo.last_commit_ts) // 86400
    if age_days <= threshold:
        return
    last_date = datetime.datetime.fromtimestamp(repo.last_commit_ts).strftime("%Y-%m-%d")
    ctx.add(
        repo,
        "R16-doc-staleness",
        "注册项目最后 commit 距今 %d 天（>%d）" % (age_days, threshold),
        path=".",
        evidence="最后提交：%s" % last_date,
        fix_hint="确认项目是否活跃：活跃则补最近进展；停滞则走归档/退役流程。",
    )


def check_R17(ctx, repo):
    if repo.missing or not repo.exists:
        return
    nested = repo.scan.get("nested") or []
    if not nested:
        return
    ctx.add(
        repo,
        "R17-nested-repos",
        "仓内存在 %d 个嵌套 .git（maxdepth %d）"
        % (len(nested), ctx.cfg["thresholds"]["nested_repo_maxdepth"]),
        path=nested[0],
        evidence=_sample(nested),
        fix_hint="嵌套仓迁出为独立注册项目，或删除其 .git 并作为普通目录纳入父仓。",
    )


def check_R18(ctx, repo):
    if repo.missing or not repo.exists:
        return
    if not repo.root_file("package.json"):
        return
    locks = [
        name
        for name in ("pnpm-lock.yaml", "yarn.lock", "package-lock.json", "npm-shrinkwrap.json")
        if repo.root_file(name)
    ]
    if locks:
        return
    ctx.add(
        repo,
        "R18-package-lock",
        "存在 package.json 但没有锁文件",
        path="package.json",
        evidence="未找到 pnpm-lock.yaml / yarn.lock / package-lock.json",
        fix_hint="选定包管理器并提交锁文件；CI 使用 frozen-lockfile。",
    )


def check_R19(ctx, repo):
    """仓内 .venv/venv 存在且被跟踪或未被忽略。"""
    if repo.missing or not repo.exists:
        return
    venv_paths = list(repo.scan.get("venv") or [])
    for name in (".venv", "venv"):
        if name not in venv_paths and os.path.isdir(os.path.join(repo.path, name)):
            venv_paths.append(name)
    if not venv_paths:
        return
    tracked_prefixes = {path + "/" for path in venv_paths}
    tracked = []
    for tracked_path in repo.ls_files:
        if any(tracked_path.startswith(prefix) for prefix in tracked_prefixes):
            tracked.append(tracked_path)
    tokens = _gitignore_tokens(repo.gitignore_lines)
    ignored = _covers(tokens, [".venv/", "venv/", ".venv", "venv"])
    if tracked:
        ctx.add(
            repo,
            "R19-venv-in-repo",
            "虚拟环境被 git 跟踪（%d 个文件）" % len(tracked),
            path=venv_paths[0],
            evidence="跟踪文件样例：%s" % _sample(tracked),
            fix_hint="git rm -r --cached <venv>，重建本地环境并写入 .gitignore。",
        )
    elif not ignored:
        ctx.add(
            repo,
            "R19-venv-in-repo",
            "仓内存在虚拟环境目录但未被 .gitignore 忽略",
            path=venv_paths[0],
            evidence="目录：%s；.gitignore 未覆盖 .venv/ 或 venv/" % ", ".join(venv_paths[:5]),
            fix_hint="把 .venv/、venv/ 写入 .gitignore。",
        )


def check_R20(ctx, repo):
    if repo.missing or not repo.exists:
        return
    if _has_test_entry(repo):
        return
    ctx.add(
        repo,
        "R20-clean-commands",
        "README/Makefile/package.json/pyproject 中未找到 test 命令入口",
        path=".",
        evidence="已检查 README.md、Makefile、package.json、pyproject.toml",
        fix_hint="提供 make test 或等价命令，并在 README 快速开始段写明。",
    )


RULE_CHECKS = [
    ("R01-repo-name", check_R01),
    ("R02-registered", check_R02),
    ("R03-worktree-location", check_R03),
    ("R04-required-files", check_R04),
    ("R05-gitignore-coverage", check_R05),
    ("R06-root-md-limit", check_R06),
    ("R07-readme-sections", check_R07),
    ("R08-agents-sections", check_R08),
    ("R09-manifest-sections", check_R09),
    ("R10-docs-layout", check_R10),
    ("R11-stray-files", check_R11),
    ("R12-tracked-artifacts", check_R12),
    ("R13-large-tracked-files", check_R13),
    ("R14-dirty-worktree", check_R14),
    ("R15-branch-sprawl", check_R15),
    ("R16-doc-staleness", check_R16),
    ("R17-nested-repos", check_R17),
    ("R18-package-lock", check_R18),
    ("R19-venv-in-repo", check_R19),
    ("R20-clean-commands", check_R20),
]


# ---------------------------------------------------------------------------
# 豁免应用
# ---------------------------------------------------------------------------


def _rule_matches(exception_rule, violation_rule):
    if exception_rule == violation_rule:
        return True
    if exception_rule.endswith("*") and fnmatch.fnmatchcase(violation_rule, exception_rule):
        return True
    # 允许只写 "R12" 前缀
    return bool(re.match(r"^R\d+$", exception_rule)) and violation_rule.startswith(exception_rule + "-")


def apply_exceptions(ctx, exceptions, problems, today):
    applied, kept = [], []
    expired_entries = []
    active = []
    for entry in exceptions:
        if entry["until"] < today:
            expired_entries.append(entry)
            continue
        max_window = today + datetime.timedelta(days=90)
        if entry["until"] > max_window:
            problems.append(
                {
                    "index": entry["index"],
                    "repo": entry["repo"],
                    "message": "第 %d 条豁免 until 超过 90 天上限（%s）"
                    % (entry["index"], entry["until"].isoformat()),
                }
            )
        active.append(entry)
    for violation in ctx.violations:
        matched = None
        for entry in active:
            if entry["repo"] not in ("*", violation["repo"]):
                continue
            if _rule_matches(entry["rule"], violation["rule"]):
                matched = entry
                break
        if matched:
            applied.append(
                {
                    "repo": violation["repo"],
                    "rule": violation["rule"],
                    "reason": matched["reason"],
                    "until": matched["until"].isoformat(),
                    "approved_by": matched["approved_by"],
                    "message": violation["message"],
                }
            )
        else:
            kept.append(violation)
    for entry in expired_entries:
        kept.append(
            {
                "rule": META_RULE_EXPIRED,
                "severity": ctx.cfg["exceptions"].get("expired_severity", "warn"),
                "repo": entry["repo"],
                "path": entry["path"],
                "message": "豁免已过期，自动失效：%s" % entry["rule"],
                "evidence": "repo=%s rule=%s until=%s reason=%s"
                % (entry["repo"], entry["rule"], entry["until"].isoformat(), entry["reason"]),
                "fix_hint": "重新评估：整改后删除豁免，或走 G5 决策重新申请（不得自动续期）。",
            }
        )
    for problem in problems:
        kept.append(
            {
                "rule": META_RULE_INVALID,
                "severity": "warn",
                "repo": problem["repo"],
                "path": "_governance/rules/exceptions.yaml",
                "message": problem["message"],
                "evidence": "exceptions.yaml 第 %s 条" % problem["index"],
                "fix_hint": "补齐必填字段（repo/rule/reason/until），until 使用 YYYY-MM-DD。",
            }
        )
    return kept, applied, expired_entries


# ---------------------------------------------------------------------------
# 运行与结果
# ---------------------------------------------------------------------------


def run_checks(ws, cfg, repo_filter=None, staged_only=False, ignore_exceptions=False):
    registry = load_registry(ws, cfg)
    reg_by_repo = {project["repo"]: project for project in registry["_projects"]}
    targets = discover_targets(ws, cfg, reg_by_repo)

    selected = targets
    if repo_filter:
        selected = select_targets(targets, repo_filter)
        if not selected:
            known = "、".join(item.name for item in targets[:12])
            raise UsageError("未找到匹配的仓库：%r。可选（前 12 个）：%s …" % (repo_filter, known))

    exceptions, problems, _ = load_exceptions(ws, cfg) if not ignore_exceptions else ([], [], "")
    ctx = CheckContext(ws, cfg, staged_only)

    repos = []
    for entry in selected:
        data = RepoData(entry, ws, cfg, staged_only)
        data.collect()
        repos.append(data)
        if data.git_errors:
            ctx.git_notes.append("%s: git 命令异常 %d 条（已降级处理）" % (data.name, len(data.git_errors)))

    for data in repos:
        for _rule_id, func in RULE_CHECKS:
            try:
                func(ctx, data)
            except Exception as exc:  # 单条规则异常不影响全量检查
                ctx.git_notes.append("%s/%s 规则执行异常：%s" % (data.name, _rule_id, exc))

    today = datetime.date.today()
    kept, applied, expired = apply_exceptions(ctx, exceptions, problems, today)

    counts = {"error": 0, "warn": 0, "info": 0}
    for violation in kept:
        counts[violation["severity"]] += 1

    repo_counts = {}
    for data in repos:
        repo_counts[data.name] = {"error": 0, "warn": 0, "info": 0}
    known_repo_names = set(repo_counts)
    for violation in kept:
        if violation["repo"] in repo_counts:
            repo_counts[violation["repo"]][violation["severity"]] += 1

    exemption_counts = {}
    for item in applied:
        exemption_counts[item["rule"]] = exemption_counts.get(item["rule"], 0) + 1

    rule_stats = []
    for rule in cfg["rules"]:
        rid = rule["id"]
        stat = {
            "id": rid,
            "severity": rule["severity"],
            "title": rule["title"],
            "error": 0,
            "warn": 0,
            "info": 0,
            "exempted": exemption_counts.get(rid, 0),
        }
        for violation in kept:
            if violation["rule"] == rid:
                stat[violation["severity"]] += 1
        rule_stats.append(stat)
    meta_stats = []
    for meta_rule in (META_RULE_EXPIRED, META_RULE_INVALID):
        hits = [violation for violation in kept if violation["rule"] == meta_rule]
        if hits:
            meta_stats.append(
                {
                    "id": meta_rule,
                    "severity": hits[0]["severity"],
                    "title": "豁免台账健康度",
                    "error": sum(1 for item in hits if item["severity"] == "error"),
                    "warn": sum(1 for item in hits if item["severity"] == "warn"),
                    "info": sum(1 for item in hits if item["severity"] == "info"),
                    "exempted": 0,
                }
            )

    for data in repos:
        if data.missing:
            ctx.git_notes.append("%s: 注册表登记但目录缺失" % data.name)

    return {
        "schema_version": 1,
        "tool": "gc_standard.py",
        "tool_version": TOOL_VERSION,
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "workspace": ws,
        "standards_file": cfg.get("_path"),
        "registry_file": registry.get("_path"),
        "registered_project_count": len(registry["_projects"]),
        "rule_count": len(cfg["rules"]),
        "repos": repos,
        "repo_counts": repo_counts,
        "violations": kept,
        "counts": counts,
        "rule_stats": rule_stats,
        "meta_stats": meta_stats,
        "exemptions": applied,
        "expired_exceptions": expired,
        "git_notes": ctx.git_notes,
        "target_count": len(targets),
        "checked_count": len(repos),
        "repo_filter": repo_filter,
        "staged_only": staged_only,
    }


def _sort_violations(violations):
    return sorted(
        violations,
        key=lambda item: (
            SEVERITY_RANK.get(item["severity"], 9),
            item["repo"].lower(),
            item["rule"],
        ),
    )


def gate_exit_code(counts, fail_on):
    if fail_on == "error":
        return 1 if counts["error"] else 0
    if fail_on == "warn":
        return 1 if counts["error"] or counts["warn"] else 0
    return 0


def _repo_flags(repo):
    flags = []
    if repo.registered:
        flags.append("已注册")
    else:
        flags.append("未注册")
    if repo.missing:
        flags.append("目录缺失")
    if repo.is_symlink:
        flags.append("软链")
    if not repo.is_git:
        flags.append("非 git")
    return "/".join(flags)


def _top_repos(result, limit=10):
    rows = []
    for data in result["repos"]:
        counts = result["repo_counts"][data.name]
        weight = counts["error"] * 1000 + counts["warn"] * 10 + counts["info"]
        rows.append((weight, data, counts))
    rows.sort(key=lambda item: (-item[0], item[1].name.lower()))
    return rows[:limit]


def print_human(result, fail_on):
    counts = result["counts"]
    total = sum(counts.values())
    print("GlobalCloud 统一规范检查 · %s" % result["generated_at"])
    print(
        "工作区：%s\n规则：%d 条（%s） · 检查仓库：%d 个（注册项目 %d 个）%s"
        % (
            result["workspace"],
            result["rule_count"],
            os.path.basename(result["standards_file"]),
            result["checked_count"],
            result["registered_project_count"],
            " · staged-only" if result["staged_only"] else "",
        )
    )
    print(
        "违规：error %d / warn %d / info %d（合计 %d）；豁免生效 %d 条；过期豁免 %d 条"
        % (
            counts["error"],
            counts["warn"],
            counts["info"],
            total,
            len(result["exemptions"]),
            len(result["expired_exceptions"]),
        )
    )
    if result["repo_filter"]:
        print("筛选：%s" % result["repo_filter"])
    passed = counts["error"] == 0
    print("结论：%s（本地默认不阻断；CI 使用 --fail-on error）" % ("PASS" if passed else "FAIL(存在 error)"))

    if total == 0:
        print("\n未发现违规。")
    else:
        print("\n按规则：")
        for stat in result["rule_stats"] + result["meta_stats"]:
            hits = stat["error"] + stat["warn"] + stat["info"]
            if hits or stat["exempted"]:
                print(
                    "  %-24s error %-3d warn %-3d info %-3d 豁免 %-3d %s"
                    % (stat["id"], stat["error"], stat["warn"], stat["info"], stat["exempted"], stat["title"])
                )
        print("\n按仓库（严重度前 %d）：" % min(10, len(result["repos"])))
        for _weight, data, repo_count in _top_repos(result):
            if not (repo_count["error"] or repo_count["warn"] or repo_count["info"]):
                continue
            print(
                "  %-34s error %-3d warn %-3d info %-3d  [%s]"
                % (data.name, repo_count["error"], repo_count["warn"], repo_count["info"], _repo_flags(data))
            )
        print("\n明细（前 20 条）：")
        for violation in _sort_violations(result["violations"])[:20]:
            print(
                "  [%s] %-22s %-30s %s"
                % (violation["severity"], violation["rule"], violation["repo"], violation["message"])
            )
        if result["git_notes"]:
            print("\n提示：")
            for note in result["git_notes"][:10]:
                print("  - %s" % note)
        print(
            "\n生成报告：python3 _governance/tools/gc_standard.py report --out "
            "_governance/reports/gc-standard-%s.md"
            % datetime.date.today().isoformat()
        )
        print("规则解释：python3 _governance/tools/gc_standard.py explain R12")

    if fail_on != "none":
        code = gate_exit_code(counts, fail_on)
        print("\n门禁：--fail-on %s → 退出码 %d" % (fail_on, code))
    else:
        print("\n门禁：未开启（--fail-on none）→ 退出码 0")


def _violation_md(violation, index):
    return (
        "%d. **[%s] %s** · `%s` · %s\n"
        "   - 证据：%s\n"
        "   - 修复：%s"
        % (
            index,
            violation["rule"],
            violation["repo"],
            violation["path"],
            violation["message"],
            violation["evidence"] or "—",
            violation["fix_hint"] or "—",
        )
    )


def _zero_hit_evidence(rule_id, result, cfg):
    """给 0 命中规则补一句可复核证据（用本轮已采集数据，避免“实现失效”误判）。"""
    repos = result["repos"]
    thresholds = (cfg or {}).get("thresholds") or {}
    now = int(datetime.datetime.now().timestamp())
    if rule_id == "R16-doc-staleness":
        ages = [
            (now - data.last_commit_ts) // 86400
            for data in repos
            if data.registered and data.is_git and data.last_commit_ts
        ]
        if not ages:
            return "复核：无可用最后提交时间数据"
        return "复核：注册项目最后 commit 最老 %d 天，阈值 %d 天，全部在期内" % (
            max(ages), thresholds.get("doc_stale_days", 90))
    if rule_id == "R17-nested-repos":
        return "复核：maxdepth %d 扫描（排除 node_modules 等产物目录）未发现嵌套 .git" % (
            thresholds.get("nested_repo_maxdepth", 3))
    if rule_id == "R18-package-lock":
        packages = [data for data in repos if data.exists and data.root_file("package.json")]
        missing = [
            data.name
            for data in packages
            if not any(
                data.root_file(name)
                for name in ("pnpm-lock.yaml", "yarn.lock", "package-lock.json", "npm-shrinkwrap.json")
            )
        ]
        return "复核：%d 个仓有 package.json，缺锁文件 %d 个" % (len(packages), len(missing))
    if rule_id == "R19-venv-in-repo":
        found = [(data.name, path) for data in repos for path in (data.scan.get("venv") or [])]
        return "复核：发现 venv 目录 %d 个，均已被 .gitignore 忽略或未被跟踪（规则不报本地环境）" % len(found)
    return None


def render_report(result, fail_on="none", limit=120, cfg=None):
    counts = result["counts"]
    lines = []
    lines.append("# GlobalCloud 项目群统一规范检查报告")
    lines.append("")
    lines.append("> 生成时间：%s ｜ 工作区：`%s`" % (result["generated_at"], result["workspace"]))
    lines.append("> 规则源：`%s` ｜ 注册表：`%s`" % (
        os.path.relpath(result["standards_file"], result["workspace"]),
        os.path.relpath(result["registry_file"], result["workspace"]),
    ))
    lines.append("> 复现：`python3 _governance/tools/gc_standard.py report`")
    lines.append("")
    lines.append("## 1. 结论")
    lines.append("")
    lines.append("- 规则 %d 条；检查仓库 %d 个（注册项目 %d 个）；豁免生效 %d 条；过期豁免 %d 条。" % (
        result["rule_count"], result["checked_count"], result["registered_project_count"],
        len(result["exemptions"]), len(result["expired_exceptions"])))
    lines.append("- 违规合计 **%d** 条：error **%d** / warn **%d** / info **%d**。" % (
        sum(counts.values()), counts["error"], counts["warn"], counts["info"]))
    if counts["error"]:
        lines.append("- 结论：**存在 error，需按 SLA 24 小时内整改或走豁免。**")
    elif counts["warn"]:
        lines.append("- 结论：**无 error；warn 需在 14 天内整改。**")
    else:
        lines.append("- 结论：**通过（无 error/warn）。**")
    if fail_on != "none":
        lines.append("- 门禁：`--fail-on %s` → 退出码 %d。" % (
            fail_on, gate_exit_code(counts, fail_on)))
    lines.append("")

    lines.append("## 2. 按规则统计")
    lines.append("")
    lines.append("| 规则 | 级别 | error | warn | info | 豁免 | 标题 |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for stat in result["rule_stats"] + result["meta_stats"]:
        lines.append("| `%s` | %s | %d | %d | %d | %d | %s |" % (
            stat["id"], stat["severity"], stat["error"], stat["warn"], stat["info"],
            stat["exempted"], stat["title"]))
    lines.append("")

    lines.append("## 3. 按仓库统计（error 优先）")
    lines.append("")
    lines.append("| 仓库 | 状态 | error | warn | info |")
    lines.append("|---|---|---:|---:|---:|")
    rows = []
    for data in result["repos"]:
        repo_count = result["repo_counts"][data.name]
        weight = repo_count["error"] * 1000 + repo_count["warn"] * 10 + repo_count["info"]
        rows.append((weight, data, repo_count))
    rows.sort(key=lambda item: (-item[0], item[1].name.lower()))
    for _weight, data, repo_count in rows:
        lines.append("| %s | %s | %d | %d | %d |" % (
            data.name, _repo_flags(data), repo_count["error"], repo_count["warn"], repo_count["info"]))
    lines.append("")

    by_severity = {"error": [], "warn": [], "info": []}
    for violation in _sort_violations(result["violations"]):
        by_severity.setdefault(violation["severity"], []).append(violation)
    titles = {"error": "Error 明细", "warn": "Warn 明细", "info": "Info 明细"}
    section = 4
    for severity in ("error", "warn", "info"):
        items = by_severity.get(severity) or []
        lines.append("## %d. %s（%d 条）" % (section, titles[severity], len(items)))
        lines.append("")
        if not items:
            lines.append("无。")
        else:
            for index, violation in enumerate(items[:limit], 1):
                lines.append(_violation_md(violation, index))
                lines.append("")
            if len(items) > limit:
                lines.append("> 仅展示前 %d 条，完整明细见 JSON：`check --json`。" % limit)
        lines.append("")
        section += 1

    lines.append("## %d. 豁免台账" % section)
    lines.append("")
    if result["exemptions"]:
        lines.append("| 仓库 | 规则 | 期限 | 批准 | 原因 |")
        lines.append("|---|---|---|---|---|")
        for item in result["exemptions"]:
            lines.append("| %s | `%s` | %s | %s | %s |" % (
                item["repo"], item["rule"], item["until"], item["approved_by"] or "—", item["reason"]))
    else:
        lines.append("无生效豁免。")
    if result["expired_exceptions"]:
        lines.append("")
        lines.append("过期豁免（已自动失效）：%s" % "、".join(
            "%s/%s" % (item["repo"], item["rule"]) for item in result["expired_exceptions"]))
    lines.append("")

    zero_rules = [stat for stat in result["rule_stats"] if not (stat["error"] or stat["warn"] or stat["info"] or stat["exempted"])]
    lines.append("## %d. 零命中规则与实现校验" % (section + 1))
    lines.append("")
    if zero_rules:
        lines.append("以下规则本轮全群 0 命中（不代表实现失效；`validate` 校验规则已实现，判定逻辑见源码）：")
        lines.append("")
        for stat in zero_rules:
            lines.append("- `%s`（%s）：%s" % (stat["id"], stat["severity"], stat["title"]))
            evidence = _zero_hit_evidence(stat["id"], result, cfg)
            if evidence:
                lines.append("  - %s" % evidence)
        lines.append("")
        lines.append("0 命中的典型原因：检查项已在上游被满足（如锁文件齐全、venv 已忽略），或全群当前无该形态；`validate` 已确认 20 条规则均有实现。")
    else:
        lines.append("20 条规则均有命中或豁免记录。")
    lines.append("")

    lines.append("## %d. 复现与证据" % (section + 2))
    lines.append("")
    lines.append("```bash")
    lines.append("python3 _governance/tools/gc_standard.py check --json")
    lines.append("python3 _governance/tools/gc_standard.py explain <RULE_ID>")
    lines.append("bash _governance/tools/run_audit.sh")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _write_text(path, text):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def _build_check_payload(result, ws, args, counts, fail_on, code, violations):
    return {
        "schema_version": 1,
        "tool": "gc_standard.py",
        "tool_version": TOOL_VERSION,
        "generated_at": result["generated_at"],
        "workspace": ws,
        "standards_file": result["standards_file"],
        "registry_file": result["registry_file"],
        "registered_project_count": result["registered_project_count"],
        "rule_count": result["rule_count"],
        "mode": {
            "repo_filter": args.repo,
            "severity": args.severity or "all",
            "fail_on": fail_on,
            "staged_only": bool(args.staged_only),
            "exceptions": not args.no_exceptions,
        },
        "summary": {
            "target_count": result["target_count"],
            "checked_count": result["checked_count"],
            "violation_count": sum(counts.values()),
            "counts": counts,
            "exemptions_applied": len(result["exemptions"]),
            "exceptions_expired": len(result["expired_exceptions"]),
            "blocked": bool(code),
            "exit_code": code,
        },
        "rule_stats": result["rule_stats"],
        "meta_stats": result["meta_stats"],
        "repos": [
            {
                "name": data.name,
                "path": os.path.relpath(data.path, ws).replace(os.sep, "/"),
                "registered": data.registered,
                "registered_id": (data.project or {}).get("id"),
                "registered_slug": (data.project or {}).get("slug"),
                "is_git": data.is_git,
                "is_symlink": data.is_symlink,
                "missing": data.missing,
                "counts": result["repo_counts"][data.name],
                "exemptions": sum(1 for item in result["exemptions"] if item["repo"] == data.name),
            }
            for data in result["repos"]
        ],
        "violations": violations,
        "exemptions": result["exemptions"],
        "expired_exceptions": [
            {
                "repo": item["repo"],
                "rule": item["rule"],
                "until": item["until"].isoformat(),
                "reason": item["reason"],
            }
            for item in result["expired_exceptions"]
        ],
        "notes": result["git_notes"],
    }


def cmd_check(args, ws, cfg):
    result = run_checks(
        ws,
        cfg,
        repo_filter=args.repo,
        staged_only=args.staged_only,
        ignore_exceptions=args.no_exceptions,
    )
    violations = _sort_violations(result["violations"])
    if args.severity and args.severity != "all":
        cutoff = SEVERITY_RANK[args.severity]
        violations = [item for item in violations if SEVERITY_RANK.get(item["severity"], 9) <= cutoff]
    counts = {"error": 0, "warn": 0, "info": 0}
    for violation in violations:
        counts[violation["severity"]] += 1
    result["violations"] = violations
    result["counts"] = counts
    fail_on = args.fail_on if args.fail_on is not None else cfg["defaults"].get("fail_on", "none")
    code = gate_exit_code(counts, fail_on)

    payload = _build_check_payload(result, ws, args, counts, fail_on, code, violations)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.json:
        print(text)
    else:
        print_human(result, fail_on)
    if args.json_out:
        _write_text(args.json_out, text + "\n")
    return code


def cmd_report(args, ws, cfg):
    fail_on = args.fail_on if args.fail_on is not None else "none"
    result = run_checks(
        ws,
        cfg,
        repo_filter=args.repo,
        staged_only=False,
        ignore_exceptions=args.no_exceptions,
    )
    markdown = render_report(result, fail_on=fail_on, cfg=cfg)
    out = args.out or os.path.join(
        ws, cfg["report"]["dir"], cfg["report"]["filename_pattern"].format(
            date=datetime.date.today().isoformat()
        )
    )
    if not os.path.isabs(out):
        out = os.path.join(ws, out)
    _write_text(out, markdown)
    if args.json_out:
        payload = {
            "schema_version": 1,
            "generated_at": result["generated_at"],
            "workspace": ws,
            "standards_file": result["standards_file"],
            "rule_count": result["rule_count"],
            "summary": {
                "counts": result["counts"],
                "checked_count": result["checked_count"],
                "registered_project_count": result["registered_project_count"],
                "exemptions_applied": len(result["exemptions"]),
                "exceptions_expired": len(result["expired_exceptions"]),
            },
            "rule_stats": result["rule_stats"],
            "repos": [
                {
                    "name": data.name,
                    "registered": data.registered,
                    "missing": data.missing,
                    "is_git": data.is_git,
                    "is_symlink": data.is_symlink,
                    "counts": result["repo_counts"][data.name],
                }
                for data in result["repos"]
            ],
            "violations": result["violations"],
            "exemptions": result["exemptions"],
            "expired_exceptions": [
                {"repo": item["repo"], "rule": item["rule"], "until": item["until"].isoformat()}
                for item in result["expired_exceptions"]
            ],
            "notes": result["git_notes"],
        }
        _write_text(args.json_out, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print("报告已写入：%s" % out)
    print(
        "违规：error %d / warn %d / info %d；豁免生效 %d 条"
        % (
            result["counts"]["error"],
            result["counts"]["warn"],
            result["counts"]["info"],
            len(result["exemptions"]),
        )
    )
    return gate_exit_code(result["counts"], fail_on)


def cmd_explain(args, ws, cfg):
    rules = cfg["rules"]
    spec = args.rule.strip()
    exact = [rule for rule in rules if rule["id"].lower() == spec.lower()]
    if not exact:
        exact = [rule for rule in rules if rule["id"].lower().startswith(spec.lower() + "-")]
    if not exact and re.match(r"^R\d+$", spec, re.IGNORECASE):
        exact = [rule for rule in rules if rule["id"].lower().startswith(spec.lower())]
    if not exact:
        print("未找到规则：%s。可用规则：%s" % (spec, "、".join(rule["id"] for rule in rules)), file=sys.stderr)
        return 2
    if len(exact) > 1:
        print("规则 ID 不唯一，请写完整：%s" % "、".join(rule["id"] for rule in exact), file=sys.stderr)
        return 2
    rule = exact[0]
    print("规则 %s（%s）" % (rule["id"], rule["severity"]))
    print("标题：%s" % rule["title"])
    print("说明：%s" % rule["description"])
    print("修复：%s" % rule["fix_hint"])
    print("规则源：%s" % cfg["_path"])
    print("检查示例：python3 _governance/tools/gc_standard.py check --repo \"GlobalCloud KDS\"")
    print("仅看该规则：python3 _governance/tools/gc_standard.py check --json | python3 -c "
          "\"import json,sys; d=json.load(sys.stdin); print([v for v in d['violations'] if v['rule']=='%s'][:20])\"" % rule["id"])
    return 0


def cmd_rules(ws, cfg):
    print("规则 ID 固定 20 条；级别与阈值来自 %s\n" % os.path.relpath(cfg["_path"], ws))
    for rule in cfg["rules"]:
        print("%-24s %-6s %s" % (rule["id"], rule["severity"], rule["title"]))
    return 0


def cmd_repos(ws, cfg):
    registry = load_registry(ws, cfg)
    reg_by_repo = {project["repo"]: project for project in registry["_projects"]}
    targets = discover_targets(ws, cfg, reg_by_repo)
    for target in targets:
        if target.registered:
            print(target.name)
    return 0


def cmd_validate(ws, cfg):
    registry = load_registry(ws, cfg)
    exceptions, problems, path = load_exceptions(ws, cfg)
    today = datetime.date.today()
    expired = [entry for entry in exceptions if entry["until"] < today]
    rule_ids = [rule["id"] for rule in cfg["rules"]]
    print("standards.yaml：%s" % cfg["_path"])
    print("规则：%d 条（%s）" % (len(rule_ids), "、".join(rule_ids)))
    print("实现校验：%s" % ("通过（20 条规则均有判定函数）" if [rid for rid, _ in RULE_CHECKS] == REQUIRED_RULE_IDS else "失败"))
    print("注册表：%s（%d 个项目）" % (registry["_path"], len(registry["_projects"])))
    print("豁免台账：%s（有效 %d 条，过期 %d 条，问题 %d 条）" % (
        os.path.relpath(path, ws) if os.path.exists(path) else "(不存在)",
        len(exceptions), len(expired), len(problems)))
    for entry in exceptions:
        state = "已过期" if entry["until"] < today else "生效"
        print("  - [%s] %s / %s 至 %s" % (state, entry["repo"], entry["rule"], entry["until"].isoformat()))
    for problem in problems:
        print("  ! %s" % problem["message"])
    ok = (
        [rid for rid, _ in RULE_CHECKS] == REQUIRED_RULE_IDS
        and len(rule_ids) == len(REQUIRED_RULE_IDS)
        and not problems
    )
    print("结论：%s" % ("PASS" if ok else "FAIL（修复后重跑）"))
    return 0 if ok else 2


def build_parser():
    parser = argparse.ArgumentParser(
        prog="gc_standard.py",
        description="GlobalCloud 项目群统一规范检查器（规则唯一源：_governance/rules/standards.yaml）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n"
        "  gc_standard.py check --repo \"GlobalCloud KDS\"\n"
        "  gc_standard.py check --json > /tmp/gc.json\n"
        "  gc_standard.py check --severity error --fail-on error\n"
        "  gc_standard.py explain R12\n"
        "  gc_standard.py report --out _governance/reports/gc-standard-2026-10-22.md\n",
    )
    parser.add_argument("--workspace", "-w", default=os.environ.get("GC_WORKSPACE") or DEFAULT_WORKSPACE,
                        help="项目群根目录（默认从脚本位置推导，或读 GC_WORKSPACE）")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="全群/单仓检查")
    check.add_argument("--repo", help="只检查某个仓（目录名/id/slug/子串）")
    check.add_argument("--json", action="store_true", help="输出 JSON 到 stdout")
    check.add_argument("--json-out", help="同时把 JSON 写入文件")
    check.add_argument("--severity", choices=["all", "error", "warn", "info"], default="all",
                       help="只输出不低于该级别的违规")
    check.add_argument("--fail-on", choices=["none", "error", "warn"], default=None,
                       help="门禁级别；默认读 standards.yaml defaults.fail_on（none）")
    check.add_argument("--staged-only", action="store_true",
                       help="pre-commit 模式：文件类规则只看暂存区，跳过仓库状态类规则（R14/R15/R16）")
    check.add_argument("--no-exceptions", action="store_true", help="忽略豁免台账（审计用）")
    check.set_defaults(func=cmd_check)

    report = sub.add_parser("report", help="生成 Markdown 报告")
    report.add_argument("--out", help="报告路径（默认 _governance/reports/gc-standard-<date>.md）")
    report.add_argument("--json-out", help="同时输出 JSON 证据文件")
    report.add_argument("--repo", help="只报告某个仓")
    report.add_argument("--fail-on", choices=["none", "error", "warn"], default=None)
    report.add_argument("--no-exceptions", action="store_true")
    report.set_defaults(func=cmd_report)

    explain = sub.add_parser("explain", help="解释某条规则与修复指引")
    explain.add_argument("rule")
    explain.set_defaults(func=cmd_explain)

    rules = sub.add_parser("rules", help="列出 20 条规则")
    rules.set_defaults(func=lambda args, ws, cfg: cmd_rules(ws, cfg))

    repos = sub.add_parser("repos", help="列出注册仓名（供脚本调用）")
    repos.set_defaults(func=lambda args, ws, cfg: cmd_repos(ws, cfg))

    validate = sub.add_parser("validate", help="校验规则集/注册表/豁免台账配置")
    validate.set_defaults(func=lambda args, ws, cfg: cmd_validate(ws, cfg))
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    ws = os.path.abspath(args.workspace)
    try:
        if not os.path.isdir(ws):
            raise ConfigError("工作区不存在：%s" % ws)
        cfg = load_standards(ws)
        if args.command in ("check", "report", "rules", "repos", "validate", "explain"):
            # explain/rules 不需要注册表，这里统一加载规则集即可
            pass
        if args.command in ("check", "report") and not os.path.exists(
            os.path.join(ws, cfg.get("sources", {}).get("registry") or "")
        ):
            raise ConfigError("注册表不存在：%s" % cfg.get("sources", {}).get("registry"))
        return args.func(args, ws, cfg)
    except ConfigError as exc:
        print("配置错误：%s" % exc, file=sys.stderr)
        return 2
    except UsageError as exc:
        print("用法错误：%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
