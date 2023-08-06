# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from rally.common import validation

from rally_openstack.common import consts
from rally_openstack.common import osclients
from rally_openstack.task import context


@validation.add("required_platform", platform="openstack", users=True)
@context.configure(name="existing_network", platform="openstack", order=349)
class ExistingNetwork(context.OpenStackContext):
    """This context supports using existing networks in Rally.

    This context should be used on a deployment with existing users.
    """

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "additionalProperties": False
    }

    def setup(self):
        for user, tenant_id in self._iterate_per_tenants():
            clients = osclients.Clients(user["credential"])
            self.context["tenants"][tenant_id]["networks"] = (
                clients.neutron().list_networks()["networks"]
            )

            self.context["tenants"][tenant_id]["subnets"] = (
                clients.neutron().list_subnets()["subnets"]
            )

    def cleanup(self):
        """Networks were not created by Rally, so nothing to do."""
