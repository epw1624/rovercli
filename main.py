import typer

import cmds

app = typer.Typer(help="Rover Command Line Interface")

sync_app = typer.Typer()

@sync_app.callback(invoke_without_command=True)
def sync(context: typer.Context, dst: str = typer.Argument(..., help="Sync files to the rover/comms base onboard computers")):
    if context.invoked_subcommand is None:
        cmds.sync(dst)

app.add_typer(sync_app, name="sync")

if __name__ == "__main__":
    app()