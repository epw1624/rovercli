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
    
    if build:
        typer.echo("Compiling roverflake project...")

        colcon_cmd = [
            "colcon", "build",
            "--base-paths", str(src_dir),
            "--build-base", str(src / "build"),
            "--install-base", str(src / "install"),
        ]

        # My laptop can't handle colcon builds with all cores and it only has 5
        # So this is to limit the number of cores
        # Should maybe remove when building on a better machine
        env_vars = os.environ.copy()
        env_vars["MAKEFLAGS"] = "-j3"

        build_result = subprocess.run(colcon_cmd, env=env_vars)
        if build_result.returncode != 0:
            typer.echo("Compilation failed. File transfer aborted")
            raise typer.Exit(code=1)
    
    typer.echo(f"Transferring files to {remote_host}:{dst}")

    rsync_cmd = [
        "rsync", "-azc",
        "--stats",
        str(src / "install"),
        f"{remote_host}:{str(dst)}"
    ]

    rsync_result = subprocess.run(rsync_cmd)
    if rsync_result.returncode != 0:
        typer.echo("Rsync install transfer failed")
        raise typer.Exit(code=1)

    rsync_cmd = [
        "rsync", "-azc",
        "--stats",
        str(src / "build"),
        f"{remote_host}:{str(dst)}"
    ]
    rsync_result = subprocess.run(rsync_cmd)
    if rsync_result.returncode != 0:
        typer.echo("Rsync build transfer failed")
        raise typer.Exit(code=1)
    
    typer.echo("File transfer complete!")

    # now, run source install/setup.bash locally
    setup_script = src / "install" / "setup.bash"
    if setup_script.exists():
        setup_script_quoted = shlex.quote(str(setup_script))
        subprocess.run(["bash", "-lc", f"source {setup_script_quoted}"], check=True)
    else:
        typer.echo(f"Setup script not found: {setup_script}")

    # now, run source install/setup.bash remotely
    remote_setup_script = dst / "install" / "setup.bash"
    remote_setup_script_quoted = shlex.quote(str(remote_setup_script))
    remote_cmd = (
        f"if [ -f {remote_setup_script_quoted} ]; then "
        f"bash -lc 'source {remote_setup_script_quoted}'; "
        f"else echo Remote setup script not found: {remote_setup_script_quoted}; exit 1; fi"
    )
    subprocess.run(["ssh", remote_host, remote_cmd], check=True)
