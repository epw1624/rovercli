import typer

import cmds

app = typer.Typer(help="Rover Command Line Interface")

sync_app = typer.Typer()

@sync_app.callback(invoke_without_command=True)
def sync(context: typer.Context, src: str = typer.Argument(..., help="Sync source (Roverflake root)"), dst: str = typer.Argument(..., help="Sync destination")):
    if context.invoked_subcommand is None:
        cmds.sync(src, dst)

app.add_typer(sync_app, name="sync")

if __name__ == "__main__":
    app()