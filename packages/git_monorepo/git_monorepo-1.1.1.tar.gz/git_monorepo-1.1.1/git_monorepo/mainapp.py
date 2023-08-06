#!/usr/bin/env python3
import sys

import click

from git_monorepo.pull_command import pull
from git_monorepo.push_command import push


@click.group()
def main():
    pass


click_pull = click.command("pull")(pull)
click_push = click.command("push")(push)


@click.command("help")
@click.argument("command")
def help(command) -> None:
    with click.Context(main) as ctx:  # type: ignore
        if "pull" == command:
            click.echo(click_pull.get_help(ctx))
        elif "push" == command:
            click.echo(click_push.get_help(ctx))
        else:
            click.echo(f"Unknown command {command}")
            sys.exit(1)


main.add_command(click_pull)
main.add_command(click_push)
main.add_command(help)


if __name__ == "__main__":
    main()
