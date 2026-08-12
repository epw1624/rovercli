from .sync import sync
from .print_ip_table import print_ip_table
from .time_sync import time_sync
from pathlib import Path

def tui():

    #while True:
    print_menu()


def sync_menu():
    print("\n=== Sync Menu ===")
    src_root = input("Enter source root (default: RoverFlake2): ") or "RoverFlake2"
    dst_root = input("Enter destination root (default: RoverFlake2): ") or "RoverFlake2"
    remote_host = input("Enter remote host (default: rv@rover): ") or "rv@rover"
    no_build = input("Disable build after sync? (y/n, default: n): ").lower() == "y"
    external_pkgs = input("Include external packages? (y/n, default: y): ").lower() != "n"
    print("1. Sync all packages")
    print("2. Sync rover packages only")
    print("3. Sync comms pi packages only")
    print("4. Sync jetson packages only")
    print("5. Sync specific packages")

    package_choice = input("Enter your choice (1-5, default: 1): ") or "1"
    packages = None
    package_list = None
    if package_choice == "1":
        packages = None
    elif package_choice == "2":
        package_list = Path("package_lists/rover.json")
    elif package_choice == "3":
        package_list = Path("package_lists/comms_pi.json")
    elif package_choice == "4":
        package_list = Path("package_lists/jetson.json")
    elif package_choice == "5":
        packages = input("Enter specific packages separated by spaces: ").split(" ")

    sync(
        src_root,
        dst_root,
        remote_host=remote_host,
        build=not no_build,
        packages=packages,
        package_list=package_list,
        external_pkgs=external_pkgs,
    )

def time_sync_menu():
    print("\n=== Time Sync Menu ===")
    remote_host = input("Enter remote host (default: rv@rover): ") or "rv@rover"
    time_sync(remote_host=remote_host)

def print_menu():

    
    print("\n=== Rover CLI TUI ===")
    print("1. Sync")
    print("2. Print IP Table")
    print("3. Time Sync")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        sync_menu()
    elif choice == "2":
        print_ip_table()
    elif choice == "3":
        time_sync_menu()
    elif choice == "4":
        print("Exiting TUI.")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
