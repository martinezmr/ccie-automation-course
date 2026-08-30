terraform {
    required_providers {
        iosxe = {
            source  = "CiscoDevNet/iosxe"
            version = "0.8.1"
        }
    }
}

variable "username" {}
variable "password" {}
variable "url" {}

provider "iosxe" {
    username = var.username
    password = var.password
    url     = var.url
}
