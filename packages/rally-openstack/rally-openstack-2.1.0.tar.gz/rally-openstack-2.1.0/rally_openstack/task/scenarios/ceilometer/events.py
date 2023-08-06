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

"""
Scenarios for Ceilometer Events API.
"""

from rally.task import validation

from rally_openstack.common import consts
from rally_openstack.task import scenario
from rally_openstack.task.scenarios.ceilometer import utils as cutils
from rally_openstack.task.scenarios.keystone import basic as kbasic


# NOTE(idegtiarov): to work with event we need to create it, there are
# no other way except emit suitable notification from one of services,
# for example create new user in keystone.

@validation.add("required_services", services=[consts.Service.CEILOMETER,
                                               consts.Service.KEYSTONE])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(context={"admin_cleanup@openstack": ["keystone"],
                             "cleanup@openstack": ["ceilometer"]},
                    name="CeilometerEvents.create_user_and_list_events",
                    platform="openstack")
class CeilometerEventsCreateUserAndListEvents(cutils.CeilometerScenario,
                                              kbasic.KeystoneBasic):

    def run(self):
        """Create user and fetch all events.

        This scenario creates user to store new event and
        fetches list of all events using GET /v2/events.
        """
        self.admin_keystone.create_user()
        events = self._list_events()
        msg = ("Events list is empty, but it should include at least one "
               "event about user creation")
        self.assertTrue(events, msg)


@validation.add("required_services", services=[consts.Service.CEILOMETER,
                                               consts.Service.KEYSTONE])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(context={"admin_cleanup@openstack": ["keystone"],
                             "cleanup@openstack": ["ceilometer"]},
                    name="CeilometerEvents.create_user_and_list_event_types",
                    platform="openstack")
class CeilometerEventsCreateUserAndListEventTypes(cutils.CeilometerScenario,
                                                  kbasic.KeystoneBasic):

    def run(self):
        """Create user and fetch all event types.

        This scenario creates user to store new event and
        fetches list of all events types using GET /v2/event_types.
        """
        self.admin_keystone.create_user()
        event_types = self._list_event_types()
        msg = ("Event types list is empty, but it should include at least one"
               " type about user creation")
        self.assertTrue(event_types, msg)


@validation.add("required_services", services=[consts.Service.CEILOMETER,
                                               consts.Service.KEYSTONE])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(context={"admin_cleanup@openstack": ["keystone"],
                             "cleanup@openstack": ["ceilometer"]},
                    name="CeilometerEvents.create_user_and_get_event",
                    platform="openstack")
class CeilometerEventsCreateUserAndGetEvent(cutils.CeilometerScenario,
                                            kbasic.KeystoneBasic):

    def run(self):
        """Create user and gets event.

        This scenario creates user to store new event and
        fetches one event using GET /v2/events/<message_id>.
        """
        self.admin_keystone.create_user()
        events = self._list_events()
        msg = ("Events list is empty, but it should include at least one "
               "event about user creation")
        self.assertTrue(events, msg)
        self._get_event(event_id=events[0].message_id)
