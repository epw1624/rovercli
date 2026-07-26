#!/usr/bin/env python3

import argparse
import cmds

def main():
    app = argparse.ArgumentParser(description="Rover Command Line Interface")

    setup_sync(app)
    args = app.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        app.print_help()

def setup_sync(app: argparse.ArgumentParser):
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
    sync_parser.add_argument("--src-root", default="RoverFlake2", help="Sync source from home directory")
    sync_parser.add_argument("--dst-root", default="RoverFlake2", help="Sync remote destination from home directory")
    sync_parser.add_argument("--remote-host", default="rv@192.168.1.4", help="Remote host for syncing")
    sync_parser.add_argument(
        "--no-build",
        action="store_true",
        help="Disable building the project after syncing",
    )
    sync_parser.add_argument("--packages", nargs = "+", default=None, help="Space-separated list of packages to transfer and build (e.g., 'arm_control drive_control')")
    sync_parser.set_defaults(func=sync)

if __name__ == "__main__":
    main()