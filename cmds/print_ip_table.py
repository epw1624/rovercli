JETSON = ["Jetson", "192.168.1.5", "jet"]
ONBOARD = ["Rover Onboard Computer", "192.168.1.4", "rover"]
BASE = ["Control Base Station", "192.168.1.50", "cbs"]
COMMS_PI = ["Comms Pi", "192.168.1.51", "comms_pi"]
RELAY = ["Relay", "192.168.1.22", "relay"]
ONBOARD_ANTENNA = ["Onboard Antenna", "192.168.1.21", "rv_bullet"]
DISH = ["Dish", "192.168.1.20", "dish"]
BEN = ["Ben's laptop", "192.168.1.55", "ben"]
ALL_DEVICES = [JETSON, ONBOARD, BASE, COMMS_PI, RELAY, ONBOARD_ANTENNA, DISH, BEN]

def print_ip_table():
    print("To create an alias, run sudo nano /etc/hosts and paste the following lines:")
    for device in ALL_DEVICES:
        name, ip, alias = device
        print(f"{ip}\t{alias}")
    
    print(f"\n\n{'Device':<25} {'IP Address':<15} {'Alias':<10}")
    print("-" * 50)
    for device in ALL_DEVICES:
        name, ip, alias = device
        print(f"{name:<25} {ip:<15} {alias:<10}")