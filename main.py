from pathlib import Path
import argparse

import cmds

app = argparse.ArgumentParser(description="Rover Command Line Interface")
sync_app = app.add_subparsers(dest="command")

def sync(args):
    cmds.sync(
        args.src_root,
        args.dst_root,
        remote_host=args.remote_host,
        build=not args.no_build,
        packages=args.packages,
    )

sync_parser = sync_app.add_parser("sync")
sync_parser.add_argument("--src-root", help="Sync source (Roverflake root)", required=True)
sync_parser.add_argument("--dst-root", default="/home/rv/Roverflake2/", help="Sync remote destination (Roverflake root)")
sync_parser.add_argument("--remote-host", default="rv@192.168.1.4", help="Remote host for syncing")
sync_parser.add_argument(
    "--no-build",
    action="store_true",
    help="Disable building the project before syncing",
)
sync_parser.add_argument("--packages", default=None, help="Space-separated list of packages to transfer and build (e.g., 'arm_control drive_control')")
sync_parser.set_defaults(func=sync)

if __name__ == "__main__":
    args = app.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        app.print_help()