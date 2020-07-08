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
# Copyright (c) 2017-2020 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#
import copy
import mock

from oslo_config import cfg

from dcmanager.common import consts
from dcmanager.common import context
from dcmanager.manager import fw_update_orch_thread
from dcmanager.manager import patch_orch_thread
from dcmanager.manager.states.base import BaseState
from dcmanager.manager import sw_update_manager
from dcmanager.manager import sw_upgrade_orch_thread

from dcmanager.tests import base
from dcmanager.tests.unit.manager.states.fakes import FakeKeystoneClient
from dcmanager.tests.unit.manager.states.fakes import FakeSysinvClient
from dcmanager.tests.unit.manager.states.fakes import FakeVimClient
from dcmanager.tests.unit.manager.test_sw_update_manager import FakeOrchThread
from dcmanager.tests.unit.manager.test_sw_update_manager \
    import StrategyStep
from dcmanager.tests.unit.manager.test_sw_update_manager \
    import Subcloud
from dcmanager.tests import utils

CONF = cfg.CONF

FAKE_STRATEGY_STEP_DATA = {
    "id": 1,
    "subcloud_id": 1,
    "stage": 1,
    "state": consts.STRATEGY_STATE_INITIAL,
    "details": '',
    "subcloud": None
}


class TestSwUpdate(base.DCManagerTestCase):

    DEFAULT_STRATEGY_TYPE = consts.SW_UPDATE_TYPE_UPGRADE

    def setUp(self):
        super(TestSwUpdate, self).setUp()

        # construct an upgrade orch thread
        self.worker = self.setup_orch_worker(self.DEFAULT_STRATEGY_TYPE)

        # Mock the context
        self.ctxt = utils.dummy_context()
        p = mock.patch.object(context, 'get_admin_context')
        self.mock_get_admin_context = p.start()
        self.mock_get_admin_context.return_value = self.ctx
        self.addCleanup(p.stop)

        # Mock the keystone client defined in the base state class
        self.keystone_client = FakeKeystoneClient()
        p = mock.patch.object(BaseState, 'get_keystone_client')
        self.mock_keystone_client = p.start()
        self.mock_keystone_client.return_value = self.keystone_client
        self.addCleanup(p.stop)

        # Mock the sysinv client defined in the base state class
        self.sysinv_client = FakeSysinvClient()
        p = mock.patch.object(BaseState, 'get_sysinv_client')
        self.mock_sysinv_client = p.start()
        self.mock_sysinv_client.return_value = self.sysinv_client
        self.addCleanup(p.stop)

        # Mock the vim client defined in the base state class
        self.vim_client = FakeVimClient()
        p = mock.patch.object(BaseState, 'get_vim_client')
        self.mock_vim_client = p.start()
        self.mock_vim_client.return_value = self.vim_client
        self.addCleanup(p.stop)

    def setup_orch_worker(self, strategy_type):
        worker = None
        mock_strategy_lock = mock.Mock()
        mock_dcmanager_audit_api = mock.Mock()
        # There are 3 orch threads. Only one needs to be setup based on type
        if strategy_type == consts.SW_UPDATE_TYPE_UPGRADE:
            sw_update_manager.SwUpgradeOrchThread.stopped = lambda x: False
            worker = \
                sw_update_manager.SwUpgradeOrchThread(mock_strategy_lock,
                                                      mock_dcmanager_audit_api)
            # Mock db_api
            p = mock.patch.object(sw_upgrade_orch_thread, 'db_api')
            self.mock_db_api = p.start()
            self.addCleanup(p.stop)
        else:
            # mock the upgrade orch thread
            self.fake_sw_upgrade_orch_thread = FakeOrchThread()
            p = mock.patch.object(sw_update_manager, 'SwUpgradeOrchThread')
            self.mock_sw_upgrade_orch_thread = p.start()
            self.mock_sw_upgrade_orch_thread.return_value = \
                self.fake_sw_upgrade_orch_thread
            self.addCleanup(p.stop)

        if strategy_type == consts.SW_UPDATE_TYPE_PATCH:
            sw_update_manager.PatchOrchThread.stopped = lambda x: False
            worker = \
                sw_update_manager.PatchOrchThread(mock_strategy_lock,
                                                  mock_dcmanager_audit_api)
            # Mock db_api
            p = mock.patch.object(patch_orch_thread, 'db_api')
            self.mock_db_api = p.start()
            self.addCleanup(p.stop)
        else:
            # mock the patch orch thread
            self.fake_sw_patch_orch_thread = FakeOrchThread()
            p = mock.patch.object(sw_update_manager, 'PatchOrchThread')
            self.mock_sw_patch_orch_thread = p.start()
            self.mock_sw_patch_orch_thread.return_value = \
                self.fake_sw_patch_orch_thread
            self.addCleanup(p.stop)

        if strategy_type == consts.SW_UPDATE_TYPE_FIRMWARE:
            sw_update_manager.FwUpdateOrchThread.stopped = lambda x: False
            worker = \
                sw_update_manager.FwUpdateOrchThread(mock_strategy_lock,
                                                     mock_dcmanager_audit_api)
            # Mock db_api
            p = mock.patch.object(fw_update_orch_thread, 'db_api')
            self.mock_db_api = p.start()
            self.addCleanup(p.stop)
        else:
            # mock the patch orch thread
            self.fake_fw_update_orch_thread = FakeOrchThread()
            p = mock.patch.object(sw_update_manager, 'FwUpdateOrchThread')
            self.mock_fw_update_orch_thread = p.start()
            self.mock_fw_update_orch_thread.return_value = \
                self.fake_fw_update_orch_thread
            self.addCleanup(p.stop)

        return worker

    def setup_strategy_step(self, strategy_state):
        data = copy.copy(FAKE_STRATEGY_STEP_DATA)
        data['state'] = strategy_state
        data['subcloud'] = Subcloud(1,
                                    'subcloud1', 1,
                                    is_managed=True,
                                    is_online=True)
        fake_strategy_step = StrategyStep(**data)
        return fake_strategy_step

    def assert_step_updated(self, subcloud_id, update_state):
        self.mock_db_api.strategy_step_update.assert_called_with(
            mock.ANY,
            subcloud_id,
            state=update_state,
            details=mock.ANY,
            started_at=mock.ANY,
            finished_at=mock.ANY,
        )
