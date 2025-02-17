# Copyright (c) 2015 Huawei Technologies Co., Ltd.
# Copyright (c) 2017-2022 Wind River Systems, Inc.
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

import pecan
from pecan.configuration import set_config
from pecan.testing import load_test_app

from oslo_config import cfg
from oslo_config import fixture as fixture_config
from oslo_serialization import jsonutils
from oslo_utils import uuidutils

from dcmanager.api import api_config
from dcmanager.common import config
from dcmanager.tests import base

config.register_options()
OPT_GROUP_NAME = 'keystone_authtoken'
cfg.CONF.import_group(OPT_GROUP_NAME, "keystonemiddleware.auth_token")


def fake_delete_response(self, context):
    resp = jsonutils.dumps(context.to_dict())
    return resp


class DCManagerApiTest(base.DCManagerTestCase):

    def setUp(self):
        super(DCManagerApiTest, self).setUp()

        self.addCleanup(set_config, {}, overwrite=True)

        api_config.test_init()

        config = fixture_config.Config()
        self.CONF = self.useFixture(config).conf
        config.set_config_dirs([])

        # self.setup_messaging(self.CONF)
        self.CONF.set_override('auth_strategy', 'noauth')

        self.app = self._make_app()

    def _make_app(self, enable_acl=False):
        self.config = {
            'app': {
                'root': 'dcmanager.api.controllers.root.RootController',
                'modules': ['dcmanager.api'],
                'enable_acl': enable_acl,
                'errors': {
                    400: '/error',
                    '__force_dict__': True
                }
            },
        }

        return load_test_app(self.config)

    def tearDown(self):
        super(DCManagerApiTest, self).tearDown()
        pecan.set_config({}, overwrite=True)


class TestRootController(DCManagerApiTest):
    """Test version listing on root URI."""

    def test_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        json_body = jsonutils.loads(response.body)
        versions = json_body.get('versions')
        self.assertEqual(1, len(versions))

    def _test_method_returns_405(self, method):
        api_method = getattr(self.app, method)
        response = api_method('/', expect_errors=True)
        self.assertEqual(response.status_int, 405)

    def test_post(self):
        self._test_method_returns_405('post')

    def test_put(self):
        self._test_method_returns_405('put')

    def test_patch(self):
        self._test_method_returns_405('patch')

    def test_delete(self):
        self._test_method_returns_405('delete')

    def test_head(self):
        self._test_method_returns_405('head')


class TestErrors(DCManagerApiTest):

    def setUp(self):
        super(TestErrors, self).setUp()
        cfg.CONF.set_override('admin_tenant', 'fake_tenant_id',
                              group='cache')

    def test_404(self):
        response = self.app.get('/assert_called_once', expect_errors=True)
        self.assertEqual(response.status_int, 404)

    def test_bad_method(self):
        fake_tenant = uuidutils.generate_uuid()
        fake_url = '/v1.0/%s/bad_method' % fake_tenant
        response = self.app.patch(fake_url,
                                  expect_errors=True)
        self.assertEqual(response.status_int, 404)


class TestRequestID(DCManagerApiTest):

    def test_request_id(self):
        response = self.app.get('/')
        self.assertIn('x-openstack-request-id', response.headers)
        self.assertTrue(
            response.headers['x-openstack-request-id'].startswith('req-'))
        id_part = response.headers['x-openstack-request-id'].split('req-')[1]
        self.assertTrue(uuidutils.is_uuid_like(id_part))


class TestKeystoneAuth(DCManagerApiTest):

    def setUp(self):
        super(TestKeystoneAuth, self).setUp()

        self.addCleanup(set_config, {}, overwrite=True)

        api_config.test_init()

        self.CONF = self.useFixture(fixture_config.Config()).conf

        cfg.CONF.set_override('auth_strategy', 'keystone')

        self.app = self._make_app()

    def test_auth_not_enforced_for_root(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
