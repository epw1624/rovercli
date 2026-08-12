#!/usr/bin/env python3

import argparse
import cmds

def main():
    app = argparse.ArgumentParser(description="Rover Command Line Interface")
    subparsers = app.add_subparsers(dest="command")

    setup_sync(subparsers)
    setup_print_ip_table(subparsers)
    setup_time_sync(subparsers)
    setup_tui(subparsers)
    args = app.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        app.print_help()

def setup_sync(subparsers):
    def sync(args):
        cmds.sync(
            args.src_root,
            args.dst_root,
            remote_host=args.remote_host,
            build=not args.no_build,
            packages=args.packages,
            external_pkgs=not args.no_external_pkgs,
            package_list=args.package_list,
        )

    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--src-root", default="RoverFlake2", help="Sync source from home directory")
    sync_parser.add_argument("--dst-root", default="RoverFlake2", help="Sync remote destination from home directory")
    sync_parser.add_argument("--remote-host", default="rv@192.168.1.4", help="Remote host for syncing")
    sync_parser.add_argument(
        "--no-build",
        action="store_true",
        help="Disable building the project after syncing",
    )
    sync_parser.add_argument("--packages", nargs = "+", default=None, help="Space-separated list of packages to transfer and build (e.g., 'arm_control drive_control')")
    sync_parser.add_argument("--package-list", type=str, help="Path to a JSON file containing a list of packages to transfer and build")
    sync_parser.add_argument("--no-external-pkgs", action="store_true", help="Do not include external packages in the sync process")
    sync_parser.set_defaults(func=sync)

def setup_print_ip_table(subparsers):
    def print_ip_table(args):
        cmds.print_ip_table()

    print_ip_table_parser = subparsers.add_parser("print-ip-table")
    print_ip_table_parser.set_defaults(func=print_ip_table)

def setup_time_sync(subparsers):
    def time_sync(args):
        cmds.time_sync()

    time_sync_parser = subparsers.add_parser("time-sync")
    time_sync_parser.add_argument("--remote-host", default="rover", help="Remote host for time synchronization")
    time_sync_parser.set_defaults(func=time_sync)

def setup_tui(subparsers):
    def tui(args):
        cmds.tui()

    tui_parser = subparsers.add_parser("tui")
    tui_parser.set_defaults(func=tui)

if __name__ == "__main__":
    main()