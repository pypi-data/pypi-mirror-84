# Copyright 2020 John Reese
# Licensed under the MIT license

import logging
import sys
from pathlib import Path
from typing import Optional

import click
import tomlkit

from attribution import __author__, __version__
from .generate import Changelog, VersionFile
from .helpers import sh
from .project import Project
from .tag import Tag
from .types import Version

LOG = logging.getLogger(__name__)


@click.group()
@click.version_option(__version__, "-V", "--version", prog_name="attribution")
@click.option("-d", "--debug", is_flag=True, help="Enable debug logging")
def main(debug: bool = False) -> None:
    """Generate changelogs from tags and shortlog"""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING, stream=sys.stderr
    )


@main.command("init")
def init() -> None:
    project = Project.load()
    name = click.prompt("Project name", default=project.name)
    package = click.prompt("Package namespace", default=project.package)
    version_file = click.confirm(
        "Use __version__.py file", default=project.config["version_file"]
    )

    if project.pyproject_path().is_file():
        pyproject = tomlkit.loads(project.pyproject_path().read_text())
    else:
        pyproject = tomlkit.document()

    if "tool" not in pyproject:
        pyproject.add(tomlkit.nl())
        pyproject["tool"] = tomlkit.table()

    if "attribution" not in pyproject["tool"]:
        pyproject["tool"].add(tomlkit.nl())
        pyproject["tool"]["attribution"] = tomlkit.table()

    pyproject["tool"]["attribution"]["name"] = name
    pyproject["tool"]["attribution"]["package"] = package
    pyproject["tool"]["attribution"]["version_file"] = version_file

    project.pyproject_path().write_text(tomlkit.dumps(pyproject))

    # pick up any changes
    project = Project.load()
    if version_file:
        VersionFile(project).write()


@main.command("generate")
def generate() -> None:
    """Regenerate changelog from existing tags"""
    project = Project.load()
    LOG.debug(f"project: {project}")
    click.echo(Changelog(project).generate())


@main.command("tag")
@click.option(
    "-m",
    "--message",
    type=str,
    default=None,
    help="Use the given message instead of prompting",
)
@click.argument("version", type=Version)
def tag_release(version: Version, message: Optional[str]) -> None:
    """Create new tagged release with changelog"""
    project = Project.load()
    LOG.debug(f"project: {project}")

    if message is None:
        tpl = (
            f"\n# Write a changelog for version {version}\n#\n"
            "# Lines starting with '#' will be ignored\n"
        )

        if project.tags:
            tag = project.tags[0]
            git_log = sh(f"git log --reverse {tag.name}..")
            tpl += f"#\n# Changes since {tag.name}:\n#\n"
            tpl += "".join(f"# {line}\n" for line in git_log.splitlines(keepends=False))

        message = click.edit(tpl)
        if message is None:
            click.echo("No message given, aborting")
            return

        message = "".join(
            line
            for line in message.splitlines(keepends=True)
            if not line.startswith("#")
        )

    try:
        # XXX: This is a really hacky wall of commands
        project = Project.load()
        LOG.debug(f"project: {project}")

        # create empty commit and tag with new version
        sh(f"git commit -m 'Version bump v{version}' --allow-empty")
        tag = Tag.create(version, message=message)

        # update changelog and version file
        changelog = Changelog(project).write()
        sh(f"git add {changelog}")
        if project.config.get("version_file"):
            path = VersionFile(project).write()
            sh(f"git add {path}")

        # update commit and tag
        sh("git commit --amend --no-edit")
        tag.update(message=message, signed=True)

    except Exception:
        mfile = Path(f".attribution-{version}.txt").resolve()
        mfile.write_text(message)
        click.secho(
            f"Bump failed, version message in {mfile}, "
            r"repo state unknown ¯\_(ツ)_/¯",
            fg="yellow",
            bold=True,
        )
        raise


if __name__ == "__main__":
    main(prog_name="attribution")  # pylint: disable=unexpected-keyword-arg
