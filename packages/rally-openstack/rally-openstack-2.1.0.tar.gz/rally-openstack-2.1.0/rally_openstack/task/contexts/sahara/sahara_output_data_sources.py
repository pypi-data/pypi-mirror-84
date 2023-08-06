# Copyright 2015: Mirantis Inc.
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
from rally_openstack.task.cleanup import manager as resource_manager
from rally_openstack.task import context
from rally_openstack.task.scenarios.sahara import utils
from rally_openstack.task.scenarios.swift import utils as swift_utils


@validation.add("required_platform", platform="openstack", users=True)
@context.configure(name="sahara_output_data_sources", platform="openstack",
                   order=444)
class SaharaOutputDataSources(context.OpenStackContext):
    """Context class for setting up Output Data Sources for an EDP job."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "output_type": {
                "enum": ["swift", "hdfs"],
            },
            "output_url_prefix": {
                "type": "string",
            }
        },
        "additionalProperties": False,
        "required": ["output_type", "output_url_prefix"]
    }

    def setup(self):
        utils.init_sahara_context(self)
        for user, tenant_id in self._iterate_per_tenants():

            clients = osclients.Clients(user["credential"])
            sahara = clients.sahara()

            if self.config["output_type"] == "swift":
                swift = swift_utils.SwiftScenario(clients=clients,
                                                  context=self.context)
                container_name = self.generate_random_name()
                self.context["tenants"][tenant_id]["sahara"]["container"] = {
                    "name": swift._create_container(
                        container_name=container_name),
                    "output_swift_objects": []
                }
                self.setup_outputs_swift(swift, sahara, tenant_id,
                                         container_name,
                                         user["credential"].username,
                                         user["credential"].password)
            else:
                self.setup_outputs_hdfs(sahara, tenant_id,
                                        self.config["output_url_prefix"])

    def setup_outputs_hdfs(self, sahara, tenant_id, output_url):
        output_ds = sahara.data_sources.create(
            name=self.generate_random_name(),
            description="",
            data_source_type="hdfs",
            url=output_url)

        self.context["tenants"][tenant_id]["sahara"]["output"] = output_ds.id

    def setup_outputs_swift(self, swift, sahara, tenant_id, container_name,
                            username, password):
        output_ds_swift = sahara.data_sources.create(
            name=self.generate_random_name(),
            description="",
            data_source_type="swift",
            url="swift://" + container_name + ".sahara/",
            credential_user=username,
            credential_pass=password)

        self.context["tenants"][tenant_id]["sahara"]["output"] = (
            output_ds_swift.id
        )

    def cleanup(self):
        resource_manager.cleanup(
            names=["swift.object", "swift.container"],
            users=self.context.get("users", []),
            superclass=self.__class__,
            task_id=self.get_owner_id())
        resource_manager.cleanup(
            names=["sahara.data_sources"],
            users=self.context.get("users", []),
            superclass=self.__class__,
            task_id=self.get_owner_id())
