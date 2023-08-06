# Copyright 2017 Red Hat, Inc. <http://www.redhat.com>
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
from rally_openstack.task.scenarios.gnocchi import utils as gnocchiutils


"""Scenarios for Gnocchi status."""


@validation.add("required_services",
                services=[consts.Service.GNOCCHI])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(name="Gnocchi.get_status")
class GetStatus(gnocchiutils.GnocchiBase):

    def run(self, detailed=False):
        """Get the status of measurements processing.

        :param detailed: get detailed output
        """
        self.admin_gnocchi.get_status(detailed)
