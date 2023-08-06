import os
import shutil
import subprocess
import sys

from termcolor_util import red, yellow, cyan

from git_monorepo.project_config import (
    read_config,
    MONOREPO_CONFIG_FILE,
    write_synchronized_commits,
    GitMonorepoConfig,
)


def move(old_path: str, new_path: str) -> None:
    """
    git mv old/path new/path
    git subtree split --rejoin --prefix=new/path HEAD
    git subtree pull --squash --prefix=new/path giturl branch
    """
    monorepo = read_config()

    old_path = _resolve_in_repo(monorepo, old_path)
    new_path = _resolve_in_repo(monorepo, new_path)

    if old_path not in monorepo.repos:
        print(
            red(old_path, bold=True),
            red("not defined in"),
            red(MONOREPO_CONFIG_FILE, bold=True),
        )
        sys.exit(1)

    giturl = monorepo.repos[old_path]

    print(
        cyan("moving"), cyan(old_path, bold=True), cyan("->"), cyan(new_path, bold=True)
    )

    # we ensure the path exists
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    subprocess.check_call(
        ["git", "mv", old_path, new_path], cwd=monorepo.project_folder
    )
    subprocess.check_call(
        ["git", "commit", "-m", f"git-monorepo: move {old_path} -> {new_path}"],
        cwd=monorepo.project_folder,
    )
    subprocess.check_call(
        ["git", "subtree", "split", "--rejoin", f"--prefix={new_path}", "HEAD"],
        cwd=monorepo.project_folder,
    )
    subprocess.check_call(
        [
            "git",
            "subtree",
            "pull",
            "--squash",
            f"--prefix={new_path}",
            giturl,
            monorepo.current_branch,
        ],
        cwd=monorepo.project_folder,
    )

    monorepo.repos[new_path] = monorepo.repos[old_path]
    del monorepo.repos[old_path]

    write_synchronized_commits(monorepo)

    print(
        "⚠️ ⚠️ ⚠️ ",
        yellow("WARNING", bold=True),
        "⚠️ ⚠️ ⚠️ ",
        yellow("don't forget to patch"),
        yellow(MONOREPO_CONFIG_FILE, bold=True),
        yellow("with the new location, and remove the old entry"),
    )


def _resolve_in_repo(monorepo: GitMonorepoConfig, path: str) -> str:
    """
    Resolves a path inside the monorepo, to allow working inside folders
    """
    absolute_path = os.path.abspath(path)

    if not absolute_path.startswith(monorepo.project_folder):
        print(
            red(path, bold=True),
            red("resolved to"),
            red(absolute_path, bold=True),
            red("was not in the project folder:"),
            red(monorepo.project_folder, bold=True),
        )
        sys.exit(1)

    return os.path.relpath(absolute_path, monorepo.project_folder)
