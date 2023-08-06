import os
import subprocess
import sys
from typing import List

from termcolor_util import yellow, red

from git_monorepo.project_config import (
    read_config,
    get_current_commit,
    write_synchronized_commits,
    is_synchronized_commits_file_existing,
)


def pull(folders: List[str]) -> None:
    monorepo = read_config()

    pull_folders = set(folders)
    pull_folders.difference_update(monorepo.repos)

    if pull_folders:
        print(
            red("Error:"),
            red(", ".join(pull_folders), bold=True),
            red("not found in monorepo projects."),
        )
        sys.exit(1)

    initial_commit = get_current_commit(project_folder=monorepo.project_folder)

    for folder_name, repo_location in monorepo.repos.items():
        if folders and not folder_name in folders:
            continue

        print(
            yellow(repo_location, bold=True),
            yellow("->"),
            yellow(folder_name, bold=True),
        )

        if not os.path.isdir(folder_name):
            subprocess.check_call(
                [
                    "git",
                    "subtree",
                    "add",
                    "-P",
                    folder_name,
                    repo_location,
                    monorepo.current_branch,
                ],
                cwd=monorepo.project_folder,
            )

            continue

        subprocess.check_call(
            [
                "git",
                "subtree",
                "pull",
                "-P",
                folder_name,
                repo_location,
                monorepo.current_branch,
            ],
            cwd=monorepo.project_folder,
        )

    current_commit = get_current_commit(project_folder=monorepo.project_folder)

    if current_commit == initial_commit and is_synchronized_commits_file_existing(
        monorepo
    ):
        return

    write_synchronized_commits(monorepo)
