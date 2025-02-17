# Copyright (c) 2020-2022 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

SECONDS_IN_HOUR = 3600

KS_ENDPOINT_ADMIN = "admin"
KS_ENDPOINT_INTERNAL = "internal"
KS_ENDPOINT_DEFAULT = KS_ENDPOINT_ADMIN

ENDPOINT_TYPE_IDENTITY_OS = "identity_openstack"

# openstack endpoint types
ENDPOINT_TYPES_LIST_OS = [ENDPOINT_TYPE_IDENTITY_OS]

# distributed Cloud constants
CLOUD_0 = "RegionOne"
VIRTUAL_MASTER_CLOUD = "SystemController"

SW_UPDATE_DEFAULT_TITLE = "all clouds default"
LOAD_VAULT_DIR = '/opt/dc-vault/loads'
DEPLOY_DIR = '/opt/platform/deploy'

USER_HEADER_VALUE = "distcloud"
USER_HEADER = {'User-Header': USER_HEADER_VALUE}

ADMIN_USER_NAME = "admin"
ADMIN_PROJECT_NAME = "admin"
SYSINV_USER_NAME = "sysinv"
DCMANAGER_USER_NAME = "dcmanager"
SERVICES_USER_NAME = "services"

NOVA_QUOTA_FIELDS = ("metadata_items",
                     "cores",
                     "instances",
                     "ram",
                     "key_pairs",
                     "injected_files",
                     "injected_file_path_bytes",
                     "injected_file_content_bytes",
                     "server_group_members",
                     "server_groups",)

CINDER_QUOTA_FIELDS = ("volumes",
                       "volumes_iscsi",
                       "volumes_ceph",
                       "per_volume_gigabytes",
                       "groups",
                       "snapshots",
                       "snapshots_iscsi",
                       "snapshots_ceph",
                       "gigabytes",
                       "gigabytes_iscsi",
                       "gigabytes_ceph",
                       "backups",
                       "backup_gigabytes")

NEUTRON_QUOTA_FIELDS = ("network",
                        "subnet",
                        "subnetpool",
                        "rbac_policy",
                        "trunk",
                        "port",
                        "router",
                        "floatingip",
                        "security_group",
                        "security_group_rule",
                        )

ENDPOINT_TYPE_PLATFORM = "platform"
ENDPOINT_TYPE_PATCHING = "patching"
ENDPOINT_TYPE_IDENTITY = "identity"
ENDPOINT_TYPE_FM = "faultmanagement"
ENDPOINT_TYPE_NFV = "nfv"
ENDPOINT_TYPE_LOAD = "load"
ENDPOINT_TYPE_DC_CERT = 'dc-cert'
ENDPOINT_TYPE_FIRMWARE = 'firmware'
ENDPOINT_TYPE_KUBERNETES = 'kubernetes'
ENDPOINT_TYPE_KUBE_ROOTCA = 'kube-rootca'

# All endpoint types
ENDPOINT_TYPES_LIST = [ENDPOINT_TYPE_PLATFORM,
                       ENDPOINT_TYPE_PATCHING,
                       ENDPOINT_TYPE_IDENTITY,
                       ENDPOINT_TYPE_LOAD,
                       ENDPOINT_TYPE_DC_CERT,
                       ENDPOINT_TYPE_FIRMWARE,
                       ENDPOINT_TYPE_KUBERNETES,
                       ENDPOINT_TYPE_KUBE_ROOTCA]

# All endpoint audit requests
ENDPOINT_AUDIT_REQUESTS = {
    ENDPOINT_TYPE_FIRMWARE: 'firmware_audit_requested',
    ENDPOINT_TYPE_KUBERNETES: 'kubernetes_audit_requested',
    ENDPOINT_TYPE_KUBE_ROOTCA: 'kube_rootca_update_audit_requested',
    ENDPOINT_TYPE_LOAD: 'load_audit_requested',
    ENDPOINT_TYPE_PATCHING: 'patch_audit_requested',
}

# Well known region names
SYSTEM_CONTROLLER_NAME = "SystemController"
DEFAULT_REGION_NAME = "RegionOne"

# Subcloud management state
MANAGEMENT_UNMANAGED = "unmanaged"
MANAGEMENT_MANAGED = "managed"

# Subcloud availability status
AVAILABILITY_OFFLINE = "offline"
AVAILABILITY_ONLINE = "online"

# Subcloud sync status
SYNC_STATUS_UNKNOWN = "unknown"
SYNC_STATUS_IN_SYNC = "in-sync"
SYNC_STATUS_OUT_OF_SYNC = "out-of-sync"

# OS type
OS_RELEASE_FILE = '/etc/os-release'
OS_CENTOS = 'centos'
OS_DEBIAN = 'debian'
SUPPORTED_OS_TYPES = [OS_CENTOS, OS_DEBIAN]

# SSL cert
CERT_CA_FILE_CENTOS = "ca-cert.pem"
CERT_CA_FILE_DEBIAN = "ca-cert.crt"
SSL_CERT_CA_DIR = "/etc/pki/ca-trust/source/anchors/"
