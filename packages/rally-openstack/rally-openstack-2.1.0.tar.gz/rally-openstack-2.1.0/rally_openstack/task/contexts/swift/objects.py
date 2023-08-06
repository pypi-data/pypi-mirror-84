# Copyright 2015: Cisco Systems, Inc.
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

from rally.common import logging
from rally.common import validation
from rally import exceptions

from rally_openstack.common import consts
from rally_openstack.task import context
from rally_openstack.task.contexts.swift import utils as swift_utils

LOG = logging.getLogger(__name__)


@validation.add("required_platform", platform="openstack", users=True)
@context.configure(name="swift_objects", platform="openstack", order=360)
class SwiftObjectGenerator(swift_utils.SwiftObjectMixin,
                           context.OpenStackContext):
    """Create containers and objects in each tenant."""
    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "containers_per_tenant": {
                "type": "integer",
                "minimum": 1
            },
            "objects_per_container": {
                "type": "integer",
                "minimum": 1
            },
            "object_size": {
                "type": "integer",
                "minimum": 1
            },
            "resource_management_workers": {
                "type": "integer",
                "minimum": 1
            }
        },
        "additionalProperties": False
    }

    DEFAULT_CONFIG = {
        "containers_per_tenant": 1,
        "objects_per_container": 1,
        "object_size": 1024,
        "resource_management_workers": 30
    }

    def setup(self):
        """Create containers and objects, using the broker pattern."""
        threads = self.config["resource_management_workers"]

        containers_per_tenant = self.config["containers_per_tenant"]
        containers_num = len(self.context["tenants"]) * containers_per_tenant
        LOG.debug("Creating %d containers using %d threads."
                  % (containers_num, threads))
        containers_count = len(self._create_containers(containers_per_tenant,
                                                       threads))
        if containers_count != containers_num:
            raise exceptions.ContextSetupFailure(
                ctx_name=self.get_name(),
                msg="Failed to create the requested number of containers, "
                    "expected %(expected)s but got %(actual)s."
                    % {"expected": containers_num, "actual": containers_count})

        objects_per_container = self.config["objects_per_container"]
        objects_num = containers_num * objects_per_container
        LOG.debug("Creating %d objects using %d threads."
                  % (objects_num, threads))
        objects_count = len(self._create_objects(objects_per_container,
                                                 self.config["object_size"],
                                                 threads))
        if objects_count != objects_num:
            raise exceptions.ContextSetupFailure(
                ctx_name=self.get_name(),
                msg="Failed to create the requested number of objects, "
                    "expected %(expected)s but got %(actual)s."
                    % {"expected": objects_num, "actual": objects_count})

    def cleanup(self):
        """Delete containers and objects, using the broker pattern."""
        threads = self.config["resource_management_workers"]

        self._delete_objects(threads)
        self._delete_containers(threads)
