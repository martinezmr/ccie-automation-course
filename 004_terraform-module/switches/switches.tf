resource "iosxe_vlan" "data" {
    vlan_id = 100
    name = "Data_VLAN"
}

resource "iosxe_vlan" "voice" {
    vlan_id = 200
    name = "Voice_VLAN"
}

resource "iosxe_vlan" "printer" {
    vlan_id = 300
    name = "Printer_VLAN"
}