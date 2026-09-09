from netmiko import ConnectHandler
import csv
from pprint import pprint as pp

routers = []

with open("data/devices.csv") as csv_file:
    inventory = csv.DictReader(csv_file)

    for row in inventory:
        if "rtr" in row["hostname"]:
            router = ConnectHandler(
                host=row["ip_address"],
                device_type=row["device_type"],
                username="admin",
                password="admin",
                ssh_config_file="~/.ssh/config",
            )
            routers.append(router)

for router in routers:
    router.enable()
    hostname = router.base_prompt

    ospf_neighbors = router.send_command("show ip ospf neighbor", use_textfsm=True)
    pp(ospf_neighbors)
