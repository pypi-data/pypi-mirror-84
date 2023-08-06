import subprocess

from termcolor_util import yellow, green

from git_monorepo.project_config import (
    read_config,
    GitMonorepoConfig,
    write_synchronized_commits,
)


def push():
    monorepo = read_config()
    something_changed = False

    for folder_name, repo_location in monorepo.repos.items():
        if is_repo_unchanged(monorepo, folder_name):
            print(
                green(repo_location, bold=True),
                green("->"),
                green(folder_name, bold=True),
                green("UNCHANGED", bold=True),
            )
            continue

        something_changed = True

        print(
            yellow(repo_location, bold=True),
            yellow("->"),
            yellow(folder_name, bold=True),
            yellow("PUSH", bold=True),
        )
        subprocess.check_call(
            [
                "git",
                "subtree",
                "push",
                "-P",
                folder_name,
                repo_location,
                monorepo.current_branch,
            ],
            cwd=monorepo.project_folder,
        )

    if not something_changed:
        return

    # we need to update the last commit file with the new value
    monorepo.synchronized_commits = [get_current_commit(monorepo)]
    write_synchronized_commits(monorepo)


def is_repo_unchanged(monorepo: GitMonorepoConfig, folder_name: str) -> bool:
    """
    We check if the sub-repo is changed. This is done via a log that could happen
    against multiple branches if this is a merge.
    :param monorepo:
    :param folder_name:
    :return:
    """
    # if no commits are synchronized, we need to mark this repo as changed
    # first, so the changes are being pushed
    if not monorepo.synchronized_commits:
        return False

    for last_commit in monorepo.synchronized_commits:
        folder_log = (
            subprocess.check_output(
                ["git", "log", f"{last_commit}..HEAD", "--", folder_name],
                cwd=monorepo.project_folder,
            )
            .decode("utf-8")
            .strip()
        )

        if folder_log:
            return False

    return True


def get_current_commit(monorepo: GitMonorepoConfig) -> str:
    return (
        subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=monorepo.project_folder,
        )
        .decode("utf-8")
        .strip()
    )
