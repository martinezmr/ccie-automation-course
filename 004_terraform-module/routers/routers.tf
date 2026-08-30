resource "iosxe_interface_ethernet" "r1gi2" {
  type              = "GigabitEthernet"
  name              = "2"
  shutdown          = false
  ipv4_address      = "192.168.2.1"
  ipv4_address_mask = "255.255.255.0"
}

resource "iosxe_interface_ethernet" "gi3" {
  type     = "GigabitEthernet"
  name     = "3"
  shutdown = false
}

resource "iosxe_interface_ethernet" "gi4" {
  type     = "GigabitEthernet"
  name     = "4"
  shutdown = false
}

resource "iosxe_ospf" "ospf1" {
  process_id = 1
  networks = [
    {
      ip       = "192.168.2.0"
      wildcard = "0.0.0.255"
      area     = "0"
    }
  ]
}

resource "iosxe_access_list_extended" "my_first_acl" {
    name = "my_first_acl"
    entries = [
        {
            sequence = 10
            remarks = "permit all traffic"
            ace_rule_action = "permit"
            ace_rule_protocol = "ip"
            source_any = true
            destination_any = true
        },
    ]
}