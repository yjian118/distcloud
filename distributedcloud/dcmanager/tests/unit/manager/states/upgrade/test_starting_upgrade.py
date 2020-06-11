#
# Copyright (c) 2020 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
import mock

from dcmanager.common import consts

from dcmanager.tests.unit.manager.states.upgrade.test_base import FakeUpgrade
from dcmanager.tests.unit.manager.states.upgrade.test_base \
    import TestSwUpgradeState

UPGRADE_ABORTING = [FakeUpgrade(state='aborting'), ]
UPGRADE_STARTED = [FakeUpgrade(state='started'), ]
SUCCESS_UPGRADE_START = 'I do not know what this looks like yet'


class TestSwUpgradeStartingUpgradeStage(TestSwUpgradeState):

    def setUp(self):
        super(TestSwUpgradeStartingUpgradeStage, self).setUp()

        # next state after 'starting upgrade' is 'migrating data'
        self.on_success_state = consts.STRATEGY_STATE_LOCKING_CONTROLLER

        # Add the strategy_step state being processed by this unit test
        self.strategy_step = \
            self.setup_strategy_step(consts.STRATEGY_STATE_STARTING_UPGRADE)

        # Add mock API endpoints for sysinv client calls invcked by this state
        self.sysinv_client.upgrade_start = mock.MagicMock()
        self.sysinv_client.get_upgrades = mock.MagicMock()

    def test_upgrade_subcloud_upgrade_start_failure(self):
        """Test the upgrade_start where the API call fails.

        The upgrade_start call fails due to a validation check such as from
        the health-query check.
        """

        # No upgrades should yet exist in the DB / API
        self.sysinv_client.get_upgrades.return_value = []

        # Simulate an upgrade_start failure on the subcloud.
        # The API throws an exception rather than returning an error response
        self.sysinv_client.upgrade_start.side_effect = \
            Exception("HTTPBadRequest: upgrade-start rejected: "
                      "System is not in a valid state for upgrades. "
                      "Run system health-query-upgrade for more details.")

        # invoke the strategy state operation on the orch thread
        self.worker.perform_state_action(self.strategy_step)

        # verify the API call that failed was invoked
        self.sysinv_client.upgrade_start.assert_called()

        # Verify the API failure leads to a state failure
        self.assert_step_updated(self.strategy_step.subcloud_id,
                                 consts.STRATEGY_STATE_FAILED)

    def test_upgrade_subcloud_upgrade_start_success(self):
        """Test upgrade_start where the API call succeeds.

        This will result in an upgrade being created with the appropriate
        state.
        """

        # No upgrades should yet exist in the DB / API
        self.sysinv_client.get_upgrades.return_value = []

        # Simulate an upgrade_start succeeds on the subcloud
        self.sysinv_client.upgrade_start.return_value = SUCCESS_UPGRADE_START

        # invoke the strategy state operation on the orch thread
        self.worker.perform_state_action(self.strategy_step)

        # verify the API call that succeeded was actually invoked
        self.sysinv_client.upgrade_start.assert_called()

        # On success, the state should transition to the next state
        self.assert_step_updated(self.strategy_step.subcloud_id,
                                 self.on_success_state)

    def test_upgrade_subcloud_upgrade_start_skip_already_started(self):
        """Test upgrade_start where the upgrade is already started."""

        # An already started upgrade exists in the DB"""
        self.sysinv_client.get_upgrades.return_value = [UPGRADE_STARTED, ]

        # upgrade_start should not be invoked, so can be mocked as 'failed'
        # by raising an exception
        self.sysinv_client.upgrade_start.side_effect = \
            Exception("HTTPBadRequest: this is a fake exception")

        # invoke the strategy state operation on the orch thread
        self.worker.perform_state_action(self.strategy_step)

        # upgrade_start API call should not have been attempted due to the
        # existing upgrade already in started state.
        self.sysinv_client.upgrade_start.assert_not_called()

        # On success, the state should transition to the next state
        self.assert_step_updated(self.strategy_step.subcloud_id,
                                 self.on_success_state)

    def test_upgrade_subcloud_upgrade_start_fails_bad_existing_upgrade(self):
        """Test the upgrade_start fails due to a bad existing upgrade."""

        # An already started upgrade exists in the DB but is in bad shape."""
        self.sysinv_client.get_upgrades.return_value = [UPGRADE_ABORTING, ]

        # upgrade_start will NOT be invoked. No need to mock it.

        # invoke the strategy state operation on the orch thread
        self.worker.perform_state_action(self.strategy_step)

        # upgrade_start API call should not have been attempted due to the
        # invalid existing upgrade that needs to be cleaned up.
        self.sysinv_client.upgrade_start.assert_not_called()

        # Verify it failed and moves to the next step
        self.assert_step_updated(self.strategy_step.subcloud_id,
                                 self.on_success_state)