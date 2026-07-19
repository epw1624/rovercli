from pathlib import Path

import typer

import cmds

app = typer.Typer(help="Rover Command Line Interface")

sync_app = typer.Typer()

@sync_app.callback(invoke_without_command=True)
def sync(
    context: typer.Context, 
    src_root: Path = typer.Argument("~/Roverflake2", help="Sync source (Roverflake root)"), 
    dst_root: Path = typer.Argument("~/Roverflake2", help="Sync remote destination (Roverflake root)"),
    remote_host: str = typer.Argument("rv@192.168.1.4", help="Remote host for syncing"), 
    build: bool = typer.Option(True, "--build", "-b", help="Build the project before syncing")
):
    if context.invoked_subcommand is None:
        cmds.sync(src_root, dst_root, remote_host=remote_host, build=build)

app.add_typer(sync_app, name="sync")

if __name__ == "__main__":
    app()