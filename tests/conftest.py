"""pytest 会话级防护：不让 pre-commit hook 的 git 环境漏进测试。

背景（2026-10-27 P0）
---------------------
``.githooks/pre-commit.local`` 末尾会跑 ``python3 -m pytest tests/ -q``。
作为 git hook 被执行时，git 会向进程导出 ``GIT_DIR`` / ``GIT_WORK_TREE`` 等变量，
测试里在 ``tempfile`` 中做的 git 操作会因此作用到**真实仓**：真实分支被提交一笔、
``user.*`` 被改成 fixture 身份、``core.worktree`` 被指向临时目录。

两层防护
--------
1. **会话级（本文件）**：导入即从 ``os.environ`` 剥掉所有 ``GIT_*``，
   覆盖"被测代码内部自己跑 git"的情形（如 ``tools/kds-sync/scan_ci_coverage.py``），
   这类子进程无法逐个改 ``env=``。
2. **调用级（tests/git_env.py）**：凡测试里直接 ``subprocess`` 调 git 的地方，
   显式传 ``env=clean_git_env()``，把继承改成显式。

判据（缺一不可）
----------------
* ``GIT_DIR=<仓>/.git GIT_WORK_TREE=<仓> python3 -m pytest tests/ -q`` 全绿；
* 跑完 ``git status --porcelain | wc -l`` 与跑前一致、``git config --get core.worktree`` 仍为空。
"""

from __future__ import annotations

import os

from git_env import clean_git_env  # noqa: F401  re-export：测试可直接 from conftest import clean_git_env

# 会话级剥除：pytest 进程本身以及它后续派生的所有子进程都不再继承 hook 的 git 环境。
for _key in [k for k in os.environ if k.startswith("GIT_")]:
    os.environ.pop(_key, None)
