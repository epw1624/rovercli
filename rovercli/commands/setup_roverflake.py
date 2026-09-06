from pathlib import Path
import subprocess, os
import yaml
from string import Template

ROVERFLAKE_GIT = "https://github.com/UBC-Snowbots/RoverFlake2.git"

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
APT_PKG_LISTS_DIR = PACKAGE_ROOT / "apt_pkg_lists"
SETUP_SCRIPTS_DIR = PACKAGE_ROOT / "setup_scripts"
ROVER_ENV_DIR = SETUP_SCRIPTS_DIR / "rover_env"

class ShellTemplate(Template):
    delimiter = "@@"  # unlikely to collide with bash's own $VAR / ${VAR} syntax

def setup_roverflake(dst: Path, pkg_list_files: list[Path], setup_scripts: list[Path], distro: str):
    """
    Sets up the Roverflake environment.
    """

    install_apt_pkgs(pkg_list_files)

    dst.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(["git", "clone", ROVERFLAKE_GIT, str(dst)], check=True)
    check_result(result, "Failed to clone RoverFlake repository.")

    os.environ["ROVERFLAKE_ROOT"] = str(dst)
    os.environ["ROS_DISTRO"] = distro

    for script in setup_scripts:
        result = subprocess.run(["bash", str(script)], check=True)
        check_result(result, f"Failed to run setup script: {script}")


    render_roverrc(dst, distro, ROVER_ENV_DIR / ".roverrc.template", Path.home() / ".roverrc")

def install_apt_pkgs(pkg_list_files: list[Path]):
    all_pkgs = []
    for file in pkg_list_files:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            all_pkgs.extend(data.get("pkgs", []))

    if all_pkgs:
        result = subprocess.run(["sudo", "-v"], check=True)
        check_result(result, "Failed to obtain sudo privileges.")
        result = subprocess.run(["sudo", "apt", "update"], check=True)
        check_result(result, "Failed to update APT package list.")

        result = subprocess.run(["sudo", "apt", "install", "-y", *all_pkgs], check=True)
        check_result(result, "Failed to install APT packages.")

def check_result(result: subprocess.CompletedProcess, error_message: str):
    if result.returncode != 0:
        raise RuntimeError(error_message)

def render_roverrc(dst_root: Path, ros_distro: str, template_path: Path, out_path: Path):
    text = template_path.read_text()
    rendered = ShellTemplate(text).substitute(ROVERFLAKE_ROOT=str(dst_root), ROS_DISTRO=ros_distro)
    out_path.write_text(rendered)
    out_path.chmod(0o644)
