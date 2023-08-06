import os
import subprocess

from termcolor_util import yellow

from git_monorepo.project_config import read_config


def pull() -> None:
    monorepo = read_config()

    for folder_name, repo_location in monorepo.repos.items():
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
