"""Compatibility functions going from Zabbix-CLI v2 to v3.

The functions in this module are intended to ease the transition by
providing fallbacks to deprecated functionality in Zabbix-CLI v2.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING
from typing import List
from typing import Optional

import typer

if TYPE_CHECKING:
    from click.core import CommandCollection
    from click.core import Group


CONFIG_FILENAME = "zabbix-cli.conf"
CONFIG_FIXED_NAME = "zabbix-cli.fixed.conf"

# Config file locations
CONFIG_DEFAULT_DIR = "/usr/share/zabbix-cli"
CONFIG_SYSTEM_DIR = "/etc/zabbix-cli"
CONFIG_USER_DIR = os.path.expanduser("~/.zabbix-cli")

# Any item will overwrite values from the previous (NYI)
CONFIG_PRIORITY = tuple(
    Path(os.path.join(d, f))
    for d, f in (
        (CONFIG_DEFAULT_DIR, CONFIG_FIXED_NAME),
        (CONFIG_SYSTEM_DIR, CONFIG_FIXED_NAME),
        (CONFIG_USER_DIR, CONFIG_FILENAME),
        (CONFIG_SYSTEM_DIR, CONFIG_FILENAME),
        (CONFIG_DEFAULT_DIR, CONFIG_FILENAME),
    )
)


AUTH_FILE = Path.home() / ".zabbix-cli_auth"
AUTH_TOKEN_FILE = Path.home() / ".zabbix-cli_auth_token"


def run_command_from_option(ctx: typer.Context, command: str) -> None:
    """Runs a command via old-style --command/-C option."""
    from zabbix_cli.output.console import error
    from zabbix_cli.output.console import exit_err
    from zabbix_cli.output.console import warning

    warning(
        "The [i]--command/-C[/] option is deprecated and will be removed in a future release. "
        "Invoke command directly instead."
    )
    if not isinstance(ctx.command, (CommandCollection, Group)):
        exit_err(  # TODO: find out if this could ever happen?
            f"Cannot run command {command!r}. Ensure it is a valid command and try again."
        )
    cmd_obj = ctx.command.get_command(ctx, command)
    if not cmd_obj:
        exit_err(
            f"Cannot run command {command!r}. Ensure it is a valid command and try again."
        )
    try:
        ctx.invoke(cmd_obj, *ctx.args)
    except typer.Exit:
        pass
    except Exception as e:
        error(
            f"Command {command!r} failed with error: {e}. Try re-running without --command."
        )


def args_callback(
    ctx: typer.Context, value: Optional[List[str]]
) -> Optional[List[str]]:
    if ctx.resilient_parsing:
        return  # for auto-completion
    if value:
        from zabbix_cli.output.console import warning

        warning(
            f"Detected deprecated positional arguments {value}. Use options instead."
        )
    # NOTE: Must NEVER return None. The "fix" in Typer 0.10.0 for None defaults
    # somehow broke the parsing of callback values, where this None default
    # is passed as-is to the typer command callback, which then fails.
    # Without this callback, an empty list is passed to the internal callback instead.
    # https://github.com/tiangolo/typer/pull/664
    # https://github.com/tiangolo/typer/blob/142422a14ca4c6a8ad579e9bd0fd0728364d86e3/typer/main.py#L639
    return value or []


ARGS_POSITIONAL = typer.Argument(
    None,
    help="DEPRECATED: V2-style positional arguments.",
    show_default=False,
    hidden=True,
    callback=args_callback,
)
