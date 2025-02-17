# Copyright (c) 2020-2023 Wind River Systems, Inc.
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
import os

import mock
from six.moves import http_client
import webtest

from dcmanager.api.controllers.v1 import subcloud_deploy
from dcmanager.common import consts
from dcmanager.common import utils as dutils
from dcmanager.tests.unit.api import test_root_controller as testroot
from dcmanager.tests import utils

from tsconfig.tsconfig import SW_VERSION

FAKE_RELEASE = '21.12'
FAKE_TENANT = utils.UUID1
FAKE_ID = '1'
FAKE_URL = '/v1.0/subcloud-deploy'
FAKE_HEADERS = {'X-Tenant-Id': FAKE_TENANT, 'X_ROLE': 'admin,member,reader',
                'X-Identity-Status': 'Confirmed', 'X-Project-Name': 'admin'}

FAKE_DEPLOY_PLAYBOOK_PREFIX = consts.DEPLOY_PLAYBOOK + '_'
FAKE_DEPLOY_OVERRIDES_PREFIX = consts.DEPLOY_OVERRIDES + '_'
FAKE_DEPLOY_CHART_PREFIX = consts.DEPLOY_CHART + '_'
FAKE_DEPLOY_PLAYBOOK_FILE = 'deployment-manager.yaml'
FAKE_DEPLOY_OVERRIDES_FILE = 'deployment-manager-overrides-subcloud.yaml'
FAKE_DEPLOY_CHART_FILE = 'deployment-manager.tgz'
FAKE_DEPLOY_FILES = {
    FAKE_DEPLOY_PLAYBOOK_PREFIX: FAKE_DEPLOY_PLAYBOOK_FILE,
    FAKE_DEPLOY_OVERRIDES_PREFIX: FAKE_DEPLOY_OVERRIDES_FILE,
    FAKE_DEPLOY_CHART_PREFIX: FAKE_DEPLOY_CHART_FILE,
}


class TestSubcloudDeploy(testroot.DCManagerApiTest):
    def setUp(self):
        super(TestSubcloudDeploy, self).setUp()
        self.ctx = utils.dummy_context()

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy(self, mock_upload_files):
        params = [('release_version', FAKE_RELEASE)]
        fields = list()
        for opt in consts.DEPLOY_COMMON_FILE_OPTIONS:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, webtest.Upload(fake_name, fake_content)))
        mock_upload_files.return_value = True
        params += fields
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 params=params)
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(FAKE_RELEASE, response.json['release_version'])

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_without_release(self, mock_upload_files):
        fields = list()
        for opt in consts.DEPLOY_COMMON_FILE_OPTIONS:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields)
        self.assertEqual(response.status_code, http_client.OK)
        # Verify the active release will be returned if release doesn't present
        self.assertEqual(SW_VERSION, response.json['release_version'])

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_missing_chart(self, mock_upload_files):
        opts = [consts.DEPLOY_PLAYBOOK, consts.DEPLOY_OVERRIDES, consts.DEPLOY_PRESTAGE]
        fields = list()
        for opt in opts:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields,
                                 expect_errors=True)
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_missing_chart_prestages(self, mock_upload_files):
        opts = [consts.DEPLOY_PLAYBOOK, consts.DEPLOY_OVERRIDES]
        fields = list()
        for opt in opts:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields,
                                 expect_errors=True)
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_missing_playbook_overrides(self, mock_upload_files):
        opts = [consts.DEPLOY_CHART, consts.DEPLOY_PRESTAGE]
        fields = list()
        for opt in opts:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields,
                                 expect_errors=True)
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_missing_prestage(self, mock_upload_files):
        opts = [consts.DEPLOY_PLAYBOOK, consts.DEPLOY_OVERRIDES, consts.DEPLOY_CHART]
        fields = list()
        for opt in opts:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields)
        self.assertEqual(response.status_code, http_client.OK)

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_all_input(self, mock_upload_files):
        opts = [consts.DEPLOY_PLAYBOOK, consts.DEPLOY_OVERRIDES,
                consts.DEPLOY_CHART, consts.DEPLOY_PRESTAGE]
        fields = list()
        for opt in opts:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields)
        self.assertEqual(response.status_code, http_client.OK)

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_prestage(self, mock_upload_files):
        opts = [consts.DEPLOY_PRESTAGE]
        fields = list()
        for opt in opts:
            fake_name = opt + "_fake"
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, fake_name, fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields)
        self.assertEqual(response.status_code, http_client.OK)

    @mock.patch.object(subcloud_deploy.SubcloudDeployController,
                       '_upload_files')
    def test_post_subcloud_deploy_missing_file_name(self, mock_upload_files):
        fields = list()
        for opt in consts.DEPLOY_COMMON_FILE_OPTIONS:
            fake_content = "fake content".encode('utf-8')
            fields.append((opt, "", fake_content))
        mock_upload_files.return_value = True
        response = self.app.post(FAKE_URL,
                                 headers=FAKE_HEADERS,
                                 upload_files=fields,
                                 expect_errors=True)
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)

    @mock.patch.object(dutils, 'get_filename_by_prefix')
    def test_get_subcloud_deploy_with_release(self, mock_get_filename_by_prefix):

        def get_filename_by_prefix_side_effect(dir_path, prefix):
            filename = FAKE_DEPLOY_FILES.get(prefix)
            if filename:
                return prefix + FAKE_DEPLOY_FILES.get(prefix)
            else:
                return None

        os.path.isdir = mock.Mock(return_value=True)
        mock_get_filename_by_prefix.side_effect = \
            get_filename_by_prefix_side_effect
        url = FAKE_URL + '/' + FAKE_RELEASE
        response = self.app.get(url, headers=FAKE_HEADERS)
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(FAKE_RELEASE,
                         response.json['subcloud_deploy']['release_version'])
        self.assertEqual(FAKE_DEPLOY_PLAYBOOK_FILE,
                         response.json['subcloud_deploy'][consts.DEPLOY_PLAYBOOK])
        self.assertEqual(FAKE_DEPLOY_OVERRIDES_FILE,
                         response.json['subcloud_deploy'][consts.DEPLOY_OVERRIDES])
        self.assertEqual(FAKE_DEPLOY_CHART_FILE,
                         response.json['subcloud_deploy'][consts.DEPLOY_CHART])
        self.assertEqual(None,
                         response.json['subcloud_deploy'][consts.DEPLOY_PRESTAGE])

    @mock.patch.object(dutils, 'get_filename_by_prefix')
    def test_get_subcloud_deploy_without_release(self, mock_get_filename_by_prefix):

        def get_filename_by_prefix_side_effect(dir_path, prefix):
            filename = FAKE_DEPLOY_FILES.get(prefix)
            if filename:
                return prefix + FAKE_DEPLOY_FILES.get(prefix)
            else:
                return None

        os.path.isdir = mock.Mock(return_value=True)
        mock_get_filename_by_prefix.side_effect = \
            get_filename_by_prefix_side_effect
        response = self.app.get(FAKE_URL, headers=FAKE_HEADERS)
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(SW_VERSION,
                         response.json['subcloud_deploy']['release_version'])
        self.assertEqual(FAKE_DEPLOY_PLAYBOOK_FILE,
                         response.json['subcloud_deploy'][consts.DEPLOY_PLAYBOOK])
        self.assertEqual(FAKE_DEPLOY_OVERRIDES_FILE,
                         response.json['subcloud_deploy'][consts.DEPLOY_OVERRIDES])
        self.assertEqual(FAKE_DEPLOY_CHART_FILE,
                         response.json['subcloud_deploy'][consts.DEPLOY_CHART])
        self.assertEqual(None,
                         response.json['subcloud_deploy'][consts.DEPLOY_PRESTAGE])
