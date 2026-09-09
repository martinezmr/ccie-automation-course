from netmiko import ConnectHandler
import csv
from pprint import pprint as pp

switches = []

with open("data/devices.csv") as csv_file:
    inventory = csv.DictReader(csv_file)

    for row in inventory:
        if "rtr" not in row["hostname"]:
            router = ConnectHandler(
                host=row["ip_address"],
                device_type=row["device_type"],
                username="admin",
                password="admin",
                ssh_config_file="~/.ssh/config",
            )
            switches.append(router)

for switch in switches:
    switch.enable()

    vlans = {"50": "Video", "100": "WAP"}

    for vlan_id, vlan_name in vlans.items():
        config_commands = [f"vlan {vlan_id}", f"name {vlan_name}"]
        switch.send_config_set(config_commands)

    output = switch.send_command("show vlan brief", use_textfsm=True)

    pp(output)
