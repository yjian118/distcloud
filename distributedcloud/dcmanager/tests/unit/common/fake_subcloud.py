#
# Copyright (c) 2020 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

import base64

from dcmanager.common import consts
from dcmanager.tests import utils

FAKE_TENANT = utils.UUID1
FAKE_ID = '1'
FAKE_URL = '/v1.0/subclouds'
WRONG_URL = '/v1.0/wrong'

FAKE_HEADERS = {'X-Tenant-Id': FAKE_TENANT, 'X_ROLE': 'admin',
                'X-Identity-Status': 'Confirmed'}

FAKE_SUBCLOUD_DATA = {"id": FAKE_ID,
                      "name": "subcloud1",
                      "description": "subcloud1 description",
                      "location": "subcloud1 location",
                      "system_mode": "duplex",
                      "management_subnet": "192.168.101.0/24",
                      "management_start_address": "192.168.101.2",
                      "management_end_address": "192.168.101.50",
                      "management_gateway_address": "192.168.101.1",
                      "systemcontroller_gateway_address": "192.168.204.101",
                      "deploy_status": consts.DEPLOY_STATE_DONE,
                      "external_oam_subnet": "10.10.10.0/24",
                      "external_oam_gateway_address": "10.10.10.1",
                      "external_oam_floating_address": "10.10.10.12",
                      "availability-status": "disabled"}

FAKE_BOOTSTRAP_VALUE = {
    'bootstrap-address': '10.10.10.12',
    'sysadmin_password': base64.b64encode('testpass'.encode("utf-8"))
}

FAKE_SUBCLOUD_INSTALL_VALUES = {
    "image": "http://192.168.101.2:8080/iso/bootimage.iso",
    "software_version": "12.34",
    "bootstrap_interface": "eno1",
    "bootstrap_address": "128.224.151.183",
    "bootstrap_address_prefix": 23,
    "bmc_address": "128.224.64.180",
    "bmc_username": "root",
    "nexthop_gateway": "128.224.150.1",
    "network_address": "128.224.144.0",
    "network_mask": "255.255.254.0",
    "install_type": 3,
    "console_type": "tty0",
    "bootstrap_vlan": 128,
    "rootfs_device": "/dev/disk/by-path/pci-0000:5c:00.0-scsi-0:1:0:0",
    "boot_device": "/dev/disk/by-path/pci-0000:5c:00.0-scsi-0:1:0:0",
    "rd.net.timeout.ipv6dad": 300,
}
