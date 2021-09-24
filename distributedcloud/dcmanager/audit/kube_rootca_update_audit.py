#
# Copyright (c) 2021 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
from keystoneauth1 import exceptions as keystone_exceptions
from oslo_config import cfg
from oslo_log import log as logging

from fm_api.constants import FM_ALARM_ID_CERT_EXPIRED
from fm_api.constants import FM_ALARM_ID_CERT_EXPIRING_SOON

from dccommon.drivers.openstack.fm import FmClient
from dccommon.drivers.openstack.sdk_platform import OpenStackDriver
from dcorch.common import consts as dcorch_consts

from dcmanager.audit.auditor import Auditor

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


KUBE_ROOTCA_ALARM_LIST = [FM_ALARM_ID_CERT_EXPIRED,
                          FM_ALARM_ID_CERT_EXPIRING_SOON]


class KubeRootcaUpdateAudit(Auditor):
    """Manages tasks related to kube rootca update audits."""

    def __init__(self, context, dcmanager_rpc_client):
        super(KubeRootcaUpdateAudit, self).__init__(
            context,
            dcmanager_rpc_client,
            dcorch_consts.ENDPOINT_TYPE_KUBE_ROOTCA
        )
        self.audit_type = "kube rootca update"
        LOG.debug("%s audit initialized" % self.audit_type)

    def get_regionone_audit_data(self):
        """Query RegionOne to determine kube rootca update information.

        Kubernetes Root CA updates are considered out of sync based on
        alarms in the subcloud, and not based on region one data.

        :return: An empty list
        """
        return []

    def subcloud_audit(self, subcloud_name, region_one_audit_data):
        """Perform an audit of kube root CA update info in a subcloud.

        :param subcloud_name: the name of the subcloud
        :param region_one_audit_data: ignored. Always an empty list
        """
        LOG.info("Triggered %s audit for subcloud:%s" % (self.audit_type,
                                                         subcloud_name))
        # check for a particular alarm in the subcloud
        try:
            sc_os_client = OpenStackDriver(region_name=subcloud_name,
                                           region_clients=None)
            session = sc_os_client.keystone_client.session
            fm_client = FmClient(subcloud_name, session)
        except (keystone_exceptions.EndpointNotFound,
                keystone_exceptions.ConnectFailure,
                keystone_exceptions.ConnectTimeout,
                IndexError):
            LOG.exception("Endpoint for online subcloud:(%s) not found, skip "
                          "%s audit." % (subcloud_name, self.audit_type))
            return
        detected_alarms = fm_client.get_alarms_by_ids(KUBE_ROOTCA_ALARM_LIST)
        if detected_alarms:
            # todo(abailey): determine if the same alarm id is being shared
            # for other certificates, and examine the list for the appropriate
            # alarm if necessary
            self.set_subcloud_endpoint_out_of_sync(subcloud_name)
        else:
            self.set_subcloud_endpoint_in_sync(subcloud_name)
        LOG.info("%s audit completed for:(%s)" % (self.audit_type,
                                                  subcloud_name))