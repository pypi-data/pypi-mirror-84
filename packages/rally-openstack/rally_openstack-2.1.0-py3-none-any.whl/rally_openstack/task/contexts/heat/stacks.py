# Copyright 2015: Mirantis Inc.
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

from rally.common import validation

from rally_openstack.common import consts
from rally_openstack.task.cleanup import manager as resource_manager
from rally_openstack.task import context
from rally_openstack.task.scenarios.heat import utils as heat_utils


@validation.add("required_platform", platform="openstack", users=True)
@context.configure(name="stacks", platform="openstack", order=435)
class StackGenerator(context.OpenStackContext):
    """Context class for create temporary stacks with resources.

       Stack generator allows to generate arbitrary number of stacks for
       each tenant before test scenarios. In addition, it allows to define
       number of resources (namely OS::Heat::RandomString) that will be created
       inside each stack. After test execution the stacks will be
       automatically removed from heat.
    """

    # The schema of the context configuration format
    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,

        "properties": {
            "stacks_per_tenant": {
                "type": "integer",
                "minimum": 1
            },
            "resources_per_stack": {
                "type": "integer",
                "minimum": 1
            }
        },
        "additionalProperties": False
    }

    DEFAULT_CONFIG = {
        "stacks_per_tenant": 2,
        "resources_per_stack": 10
    }

    @staticmethod
    def _prepare_stack_template(res_num):
        template = {
            "heat_template_version": "2014-10-16",
            "description": "Test template for rally",
            "resources": {}
        }
        rand_string = {"type": "OS::Heat::RandomString"}
        for i in range(res_num):
            template["resources"]["TestResource%d" % i] = rand_string
        return template

    def setup(self):
        template = self._prepare_stack_template(
            self.config["resources_per_stack"])
        for user, tenant_id in self._iterate_per_tenants():
            heat_scenario = heat_utils.HeatScenario(
                {"user": user, "task": self.context["task"],
                 "owner_id": self.context["owner_id"]})
            self.context["tenants"][tenant_id]["stacks"] = []
            for i in range(self.config["stacks_per_tenant"]):
                stack = heat_scenario._create_stack(template)
                self.context["tenants"][tenant_id]["stacks"].append(stack.id)

    def cleanup(self):
        resource_manager.cleanup(names=["heat.stacks"],
                                 users=self.context.get("users", []),
                                 superclass=heat_utils.HeatScenario,
                                 task_id=self.get_owner_id())
