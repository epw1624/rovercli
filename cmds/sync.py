import os
from pathlib import Path
import subprocess
from typing import Optional

def sync(src: str, dst: str, remote_host: str, packages: Optional[list[str]], build: bool = True):

    src_path = Path.home() / src
    if packages:
        dst_path = Path("~") / dst / "src"
    else:
        dst_path = Path("~") / dst

    print(f"Syncing from {src_path} to {remote_host}:{dst_path} with build={build} and packages={packages}")

    src_dir = src_path / "src"
    
    if not src_dir.exists():
        raise ValueError(f"Source directory '{src_dir}' does not exist.")
    
    print(f"Transferring source files to {remote_host}:{dst_path}...")

    rsync_cmd = ["rsync", "-azc", "--stats"]

    if packages:
        external_packages = src_dir / "external_pkgs"
        if external_packages.exists():
            rsync_cmd.append(str(external_packages))
        for package in packages:
            package_path = src_dir / package
            if not package_path.exists():
                print(f"Error: Package directory '{package}' does not exist.")
                raise ValueError(f"Package directory '{package}' does not exist.")
            rsync_cmd.append(str(package_path))

        remote_target = f"{remote_host}:{dst_path}"
    else:
        rsync_cmd.append("--delete")
        rsync_cmd.append(str(src_dir))
        remote_target = f"{remote_host}:{dst_path}"

    rsync_cmd.append(remote_target)

    print(f"Running rsync command: {' '.join(rsync_cmd)}")
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
            f"cd {str(dst_path)}; "
            + "source /opt/ros/humble/setup.bash && "
            + "colcon build "
            + f"--base-paths {str(dst_path / 'src')} "
            + f"--build-base {str(dst_path / 'build')} "
            + f"--install-base {str(dst_path / 'install')} "
            + f"--symlink-install "
        )

        if packages:
            print(f"Building only selected packages: {packages}")
            remote_colcon_cmd += f" --packages-select {' '.join(packages)}"

        remote_build_result = subprocess.run(["ssh", remote_host, remote_colcon_cmd])
        if remote_build_result.returncode != 0:
            print("Remote build failed")
            raise RuntimeError("Remote build failed")