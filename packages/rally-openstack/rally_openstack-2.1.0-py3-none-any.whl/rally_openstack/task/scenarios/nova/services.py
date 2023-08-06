# Copyright 2016 IBM Corp.
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

from rally.task import validation

from rally_openstack.common import consts
from rally_openstack.task import scenario
from rally_openstack.task.scenarios.nova import utils


"""Scenarios for Nova agents."""


@validation.add("required_services", services=[consts.Service.NOVA])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(name="NovaServices.list_services", platform="openstack")
class ListServices(utils.NovaScenario):

    def run(self, host=None, binary=None):
        """List all nova services.

        Measure the "nova service-list" command performance.

        :param host: List nova services on host
        :param binary: List nova services matching given binary
        """
        self._list_services(host, binary)
