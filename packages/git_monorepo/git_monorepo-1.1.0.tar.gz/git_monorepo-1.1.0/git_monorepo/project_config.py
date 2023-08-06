import os
import subprocess
import sys
from typing import Dict, Any, List

import yaml
from termcolor_util import red, yellow


class GitMonorepoConfig:
    def __init__(
        self,
        *,
        repos: Dict[str, str],
        current_branch: str,
        synchronized_commits: List[str],
        project_folder: str,
    ) -> None:
        # maps local folder to remote git repo location
        self.repos = repos
        self.current_branch = current_branch
        self.synchronized_commits = synchronized_commits
        self.project_folder = project_folder


def read_config() -> GitMonorepoConfig:
    monorepo_config_folder = os.path.abspath(os.curdir)
    while monorepo_config_folder and not os.path.isfile(
        os.path.join(monorepo_config_folder, "monorepo.yml")
    ):
        parent_folder = os.path.dirname(monorepo_config_folder)

        if parent_folder == monorepo_config_folder:
            print(
                red("Unable to find"),
                red("monorepo.yml", bold=True),
                red("in any of the parents from"),
                red(os.path.abspath(os.curdir), bold=True),
            )
            sys.exit(1)

        monorepo_config_folder = parent_folder

    project_folder = monorepo_config_folder

    current_branch = (
        subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=project_folder
        )
        .decode(encoding="utf-8")
        .strip()
    )

    config_file_name = os.path.join(project_folder, "monorepo.yml")
    with open(config_file_name, "rt") as f:
        config_data = yaml.safe_load(f)

    synchronized_commits = _read_synchronized_commits(project_folder)

    repos: Dict[str, str] = dict()
    _merge_repos(path="", repos=repos, data=config_data["mappings"])

    return GitMonorepoConfig(
        repos=repos,
        current_branch=current_branch,
        project_folder=project_folder,
        synchronized_commits=synchronized_commits,
    )


def write_synchronized_commits(monorepo: GitMonorepoConfig):
    sync_file_name = os.path.join(monorepo.project_folder, ".monorepo.sync")

    print(yellow("Updating"), yellow(sync_file_name, bold=True))

    with open(sync_file_name, "wt", encoding="utf-8") as f:
        yaml.safe_dump(monorepo.synchronized_commits, f)

    subprocess.check_call(
        ["git", "add", sync_file_name],
        cwd=monorepo.project_folder,
    )
    subprocess.check_call(
        [
            "git",
            "commit",
            "-m",
            f"git-monorepo: sync commit: {monorepo.synchronized_commits}",
        ],
        cwd=monorepo.project_folder,
    )


def _read_synchronized_commits(project_folder: str) -> List[str]:
    sync_file_name = os.path.join(project_folder, ".monorepo.sync")

    if not os.path.isfile(sync_file_name):
        return []

    with open(sync_file_name, "rt", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _merge_repos(*, repos: Dict[str, str], path: str, data: Dict[str, Any]) -> None:
    for key_name, key_value in data.items():
        relative_path = os.path.join(path, key_name)

        if isinstance(key_value, str):
            repos[relative_path] = key_value
            continue

        _merge_repos(
            repos=repos,
            path=relative_path,
            data=key_value,
        )
