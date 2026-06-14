import os
import subprocess
import typer

def sync(src: str, dst: str):
    src_dir = src / "src"
    
    if not src_dir.exists():
        typer.echo(f"Source directory not found in Roverflake root: {src}")

    typer.echo("Compiling roverflake project...")

    colcon_cmd = [
        "colcon", "build",
        "--base-paths", str(src_dir),
        "--build-base", str(src / "build"),
        "--install-base", str(src / "install"),
        "--symlink-install"
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
    
    DST_PATH = "/home/roverflake/"
    typer.echo(f"Transferring files to {dst:DST_PATH}")

    rsync_cmd = [
        "rsync", "-azc",
        "--delete",
        "--stats",
        str(src / "install"),
        f"{dst}:{DST_PATH}"
    ]

    rsync_result = subprocess.run(rsync_cmd)
    if rsync_result.returncode != 0:
        typer.echo("Rsync file transfer failed")
        raise typer.Exit(code=1)
    
    typer.echo("File transfer complete!")
