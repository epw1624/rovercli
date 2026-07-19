import os
from pathlib import Path
import shlex
import subprocess
from typing import Optional

def sync(src: Path, dst: Path, remote_host: str, packages: Optional[str], build: bool = True):
    
    src_dir = Path(src) / "src"
    dst = Path(dst)
    
    if not src_dir.exists():
        raise ValueError(f"Source directory '{src_dir}' does not exist.")
    
    print(f"Transferring source files to {remote_host}:{dst}")

    rsync_cmd = ["rsync", "-azc", "--stats"]

    if packages:
        package_list = packages.split()

        for package in package_list:
            package_path = src_dir / package
            if not package_path.exists():
                print(f"Error: Package directory '{package}' does not exist.")
                raise ValueError(f"Package directory '{package}' does not exist.")
            rsync_cmd.append(str(package_path))

        remote_target = f"{remote_host}:{dst}"
    else:
        rsync_cmd.append("--delete")
        rsync_cmd.append(str(src_dir))
        remote_target = f"{remote_host}:{dst}"

    rsync_cmd.append(remote_target)

    rsync_result = subprocess.run(rsync_cmd)
    if rsync_result.returncode != 0:
        print("Rsync src transfer failed")
        raise RuntimeError("Rsync src transfer failed")
    
    print("Source transfer complete!")

    if build:
        # Limit number of cores to not freeze less powerful machines like Raspberry Pi
        env_vars = os.environ.copy()
        env_vars["MAKEFLAGS"] = "-j3"

        print("Building roverflake remotely...")
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

        if packages:
            remote_colcon_cmd += f" --packages-select {packages}"

        remote_build_result = subprocess.run(["ssh", remote_host, remote_colcon_cmd])
        if remote_build_result.returncode != 0:
            print("Remote build failed")
            raise RuntimeError("Remote build failed")