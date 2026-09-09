from netmiko import ConnectHandler

router = ConnectHandler(
    host="172.17.0.4",
    username="admin",
    password="admin",
    device_type="arista_eos",
    ssh_config_file="~/.ssh/config",
)

router.enable()
router.send_config_from_file("data/bos-rtr-01.cfg")
