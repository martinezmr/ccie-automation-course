from netmiko import ConnectHandler

router = ConnectHandler(
    host="172.17.0.4",
    username="admin",
    password="admin",
    device_type="arista_eos"
)

router.send_config_from_file("data/bos-rtr-01.txt")

