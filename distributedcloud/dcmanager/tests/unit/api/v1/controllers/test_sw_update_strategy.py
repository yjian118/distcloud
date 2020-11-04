# Copyright (c) 2017 Ericsson AB
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Copyright (c) 2017 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

import copy
import mock
import six
import webtest

from dcmanager.common import consts
from dcmanager.orchestrator import rpcapi as rpc_client

from dcmanager.tests.unit.api import test_root_controller as testroot
from dcmanager.tests.unit.common import fake_strategy
from dcmanager.tests.unit.common import fake_subcloud
from dcmanager.tests import utils

FAKE_TENANT = utils.UUID1
FAKE_ID = '1'
FAKE_URL = '/v1.0/sw-update-strategy'
FAKE_HEADERS = {'X-Tenant-Id': FAKE_TENANT, 'X_ROLE': 'admin',
                'X-Identity-Status': 'Confirmed'}

FAKE_SW_UPDATE_DATA = {
    "type": consts.SW_UPDATE_TYPE_PATCH,
    "subcloud-apply-type": consts.SUBCLOUD_APPLY_TYPE_PARALLEL,
    "max-parallel-subclouds": "10",
    "stop-on-failure": "true"
}
FAKE_SW_UPDATE_APPLY_DATA = {
    "action": consts.SW_UPDATE_ACTION_APPLY
}

FAKE_SW_UPDATE_ABORT_DATA = {
    "action": consts.SW_UPDATE_ACTION_ABORT
}


class TestSwUpdateStrategy(testroot.DCManagerApiTest):

    def setUp(self):
        super(TestSwUpdateStrategy, self).setUp()
        self.ctx = utils.dummy_context()

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update(self, mock_rpc_client):
        data = FAKE_SW_UPDATE_DATA
        mock_rpc_client().create_sw_update_strategy.return_value = True
        response = self.app.post_json(FAKE_URL,
                                      headers=FAKE_HEADERS,
                                      params=data)
        mock_rpc_client().create_sw_update_strategy.assert_called_once_with(
            mock.ANY,
            data)
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_with_force_option(self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["force"] = "true"
        data["cloud_name"] = "subcloud1"
        mock_rpc_client().create_sw_update_strategy.return_value = True
        response = self.app.post_json(FAKE_URL,
                                      headers=FAKE_HEADERS,
                                      params=data)
        mock_rpc_client().create_sw_update_strategy.assert_called_once_with(
            mock.ANY,
            data)
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_bad_type(self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["type"] = "bad type"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_bad_apply_type(self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["subcloud-apply-type"] = "bad type"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_bad_max_parallel(
            self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["max-parallel-subclouds"] = "not an integer"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_invalid_stop_on_failure_type(
            self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["stop-on-failure"] = "not an boolean"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_invalid_force_type(
            self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["force"] = "not an boolean"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_valid_force_type_missing_cloud_name(
            self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        data["force"] = "true"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_no_body(self, mock_rpc_client):
        data = {}
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_no_type(self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_DATA)
        del data['type']
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_apply(self, mock_rpc_client):
        data = FAKE_SW_UPDATE_APPLY_DATA
        mock_rpc_client().apply_sw_update_strategy.return_value = True
        response = self.app.post_json(FAKE_URL + '/actions',
                                      headers=FAKE_HEADERS,
                                      params=data)
        mock_rpc_client().apply_sw_update_strategy.assert_called_once()
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_scoped_post_sw_update_apply(self, mock_rpc_client):
        data = FAKE_SW_UPDATE_APPLY_DATA
        mock_rpc_client().apply_sw_update_strategy.return_value = True
        response = self.app.post_json(
            FAKE_URL + '/actions?type=' + consts.SW_UPDATE_TYPE_PATCH,
            headers=FAKE_HEADERS,
            params=data)
        mock_rpc_client().apply_sw_update_strategy.assert_called_once()
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_abort(self, mock_rpc_client):
        mock_rpc_client().abort_sw_update_strategy.return_value = True
        data = FAKE_SW_UPDATE_ABORT_DATA
        response = self.app.post_json(FAKE_URL + '/actions',
                                      headers=FAKE_HEADERS,
                                      params=data)
        mock_rpc_client().abort_sw_update_strategy.assert_called_once()
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_scoped_post_sw_update_abort(self, mock_rpc_client):
        mock_rpc_client().abort_sw_update_strategy.return_value = True
        data = FAKE_SW_UPDATE_ABORT_DATA
        response = self.app.post_json(
            FAKE_URL + '/actions?type=' + consts.SW_UPDATE_TYPE_PATCH,
            headers=FAKE_HEADERS,
            params=data)
        mock_rpc_client().abort_sw_update_strategy.assert_called_once()
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_post_sw_update_bad_action(self, mock_rpc_client):
        data = copy.copy(FAKE_SW_UPDATE_APPLY_DATA)
        data["action"] = "bad action"
        six.assertRaisesRegex(self, webtest.app.AppError, "400 *",
                              self.app.post_json, FAKE_URL,
                              headers=FAKE_HEADERS, params=data)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_delete_sw_update_strategy(self, mock_rpc_client):
        delete_url = FAKE_URL
        mock_rpc_client().delete_sw_update_strategy.return_value = True
        response = self.app.delete_json(delete_url, headers=FAKE_HEADERS)
        mock_rpc_client().delete_sw_update_strategy.assert_called_once_with(
            mock.ANY, update_type=None)
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_scoped_delete_sw_update_strategy(self,
                                              mock_rpc_client):
        delete_url = FAKE_URL + "?type=" + consts.SW_UPDATE_TYPE_PATCH
        mock_rpc_client().delete_sw_update_strategy.return_value = True
        response = self.app.delete_json(delete_url, headers=FAKE_HEADERS)
        mock_rpc_client().delete_sw_update_strategy.assert_called_once_with(
            mock.ANY, update_type=consts.SW_UPDATE_TYPE_PATCH)
        self.assertEqual(response.status_int, 200)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_get_sw_update_strategy(self, mock_rpc_client):
        fake_strategy.create_fake_strategy(self.ctx,
                                           consts.SW_UPDATE_TYPE_PATCH)

        get_url = FAKE_URL
        response = self.app.get(get_url, headers=FAKE_HEADERS)

        self.assertEqual(response.json['type'], consts.SW_UPDATE_TYPE_PATCH)
        self.assertEqual(response.json['state'], consts.SW_UPDATE_STATE_INITIAL)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_scoped_get_sw_update_strategy(self, mock_rpc_client):
        fake_strategy.create_fake_strategy(self.ctx,
                                           consts.SW_UPDATE_TYPE_PATCH)

        get_url = FAKE_URL + '?type=' + consts.SW_UPDATE_TYPE_PATCH
        response = self.app.get(get_url, headers=FAKE_HEADERS)

        self.assertEqual(response.json['type'], consts.SW_UPDATE_TYPE_PATCH)
        self.assertEqual(response.json['state'], consts.SW_UPDATE_STATE_INITIAL)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_get_sw_update_strategy_steps(self, mock_rpc_client):
        fake_subcloud.create_fake_subcloud(self.ctx)
        fake_strategy.create_fake_strategy_step(self.ctx,
                                                consts.STRATEGY_STATE_INITIAL)

        get_url = FAKE_URL + '/steps'
        response = self.app.get(get_url, headers=FAKE_HEADERS)

        self.assertEqual(response.json['strategy-steps'][0]['state'],
                         consts.STRATEGY_STATE_INITIAL)

    @mock.patch.object(rpc_client, 'ManagerOrchestratorClient')
    def test_get_sw_update_strategy_single_step(self, mock_rpc_client):
        fake_subcloud.create_fake_subcloud(self.ctx)
        fake_strategy.create_fake_strategy_step(self.ctx,
                                                consts.STRATEGY_STATE_INITIAL)

        get_url = FAKE_URL + '/steps/subcloud1'
        response = self.app.get(get_url, headers=FAKE_HEADERS)

        self.assertEqual(response.json['state'],
                         consts.STRATEGY_STATE_INITIAL)
