import os
import subprocess
import typer
import shlex
from pathlib import Path

def sync(src: Path, dst: Path, remote_host: str, build: bool = True):
    src_dir = src / "src"
    
    if not src_dir.exists():
        typer.echo(f"Source directory not found in Roverflake root: {src}")
        raise typer.Exit(code=1)
    
    typer.echo(f"Transferring source files to {remote_host}:{dst}")

    rsync_cmd = [
        "rsync", "-azc",
        "--ignore-times",
        "--stats",
        str(src_dir),
        f"{remote_host}:{str(dst)}"
    ]

    rsync_result = subprocess.run(rsync_cmd)
    if rsync_result.returncode != 0:
        typer.echo("Rsync src transfer failed")
        raise typer.Exit(code=1)
    
    typer.echo("Source transfer complete!")

    if build:
        # Limit local parallelism for lower-core development machines.
        env_vars = os.environ.copy()
        env_vars["MAKEFLAGS"] = "-j3"

        typer.echo("Building roverflake remotely...")
        remote_colcon_cmd = (
            "source /opt/ros/humble/setup.bash && "
            + "bash -lc "
            + shlex.quote(
                "colcon build "
                f"--base-paths {shlex.quote(str(dst / 'src'))} "
                f"--build-base {shlex.quote(str(dst / 'build'))} "
                f"--install-base {shlex.quote(str(dst / 'install'))}"
            )
        )
        remote_build_result = subprocess.run(["ssh", remote_host, remote_colcon_cmd])
        if remote_build_result.returncode != 0:
            typer.echo("Remote build failed")
            raise typer.Exit(code=1)