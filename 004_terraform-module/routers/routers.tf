resource "iosxe_ospf" "ospf1" {
    process_id = 1
    networks = [
        {
            ip = "192.168.2.0"
            wildcard = "0.0.0.255"
            area = 0
        },
    ]
}