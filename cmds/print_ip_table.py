JETSON = "192.168.1.5"
ONBOARD = "192.168.1.4"
BASE = "192.168.1.50"
COMMS_PI = "192.168.1.51"
RELAY = "192.168.1.22"
ONBOARD_ANTENNA = "192.168.1.21"
DISH = "192.168.1.20"

def print_ip_table():
    print(f"{'Device':<20} {'IP Address':<15}")
    print("-" * 35)
    print(f"{'Jetson':<20} {JETSON:<15}")
    print(f"{'Onboard Computer':<20} {ONBOARD:<15}")
    print(f"{'Base Station':<20} {BASE:<15}")
    print(f"{'Comms Pi':<20} {COMMS_PI:<15}")
    print(f"{'Relay':<20} {RELAY:<15}")
    print(f"{'Onboard Antenna':<20} {ONBOARD_ANTENNA:<15}")
    print(f"{'Dish':<20} {DISH:<15}")
    