from pathlib import Path
import argparse
from typing import Optional

import cmds

app = argparse.ArgumentParser(description="Rover Command Line Interface")
sync_app = app.add_subparsers(dest="command")

def sync(args):
    cmds.sync(
        Path(args.src_root),
        Path(args.dst_root),
        remote_host=args.remote_host,
        build=args.build,
        packages=args.packages,
    )

sync_parser = sync_app.add_parser("sync")
sync_parser.add_argument("--src_root", default="~/Roverflake2", help="Sync source (Roverflake root)")
sync_parser.add_argument("--dst_root", default="~/Roverflake2", help="Sync remote destination (Roverflake root)")
sync_parser.add_argument("--remote_host", default="rv@192.168.1.4", help="Remote host for syncing")
sync_parser.add_argument("--build", type=bool, default=True, help="Build the project before syncing")
sync_parser.add_argument("--packages", default=None, help="Space-separated list of packages to transfer and build (e.g., 'arm_control drive_control')")
sync_parser.set_defaults(func=sync)

if __name__ == "__main__":
    args = app.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        app.print_help()