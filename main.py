from pathlib import Path
import typer
from typing import Optional

import cmds

app = typer.Typer(help="Rover Command Line Interface")

sync_app = typer.Typer()

@sync_app.callback()
def sync(
    context: typer.Context, 
    src_root: Path = typer.Argument("~/Roverflake2", help="Sync source (Roverflake root)"), 
    dst_root: Path = typer.Argument("~/Roverflake2", help="Sync remote destination (Roverflake root)"),
    remote_host: str = typer.Argument("rv@192.168.1.4", help="Remote host for syncing"), 
    build: bool = typer.Argument(True, help="Build the project before syncing"),
    packages: Optional[str] = typer.Argument(
        None, 
        help="Space-separated list of packages to transfer and build (e.g., 'arm_control drive_control')"
    )
):
    if context.invoked_subcommand is None:
        cmds.sync(src_root, dst_root, remote_host=remote_host, build=build, packages=packages)

app.add_typer(sync_app, name="sync")

if __name__ == "__main__":
    app()