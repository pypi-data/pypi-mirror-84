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

"""Scenarios for Gnocchi resource type."""


@validation.add("required_services", services=[consts.Service.GNOCCHI])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(name="GnocchiResourceType.list_resource_type")
class ListResourceType(gnocchiutils.GnocchiBase):

    def run(self):
        """List resource types."""
        self.gnocchi.list_resource_type()


@validation.add("required_services", services=[consts.Service.GNOCCHI])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(
    context={"admin_cleanup@openstack": ["gnocchi.resource_type"]},
    name="GnocchiResourceType.create_resource_type")
class CreateResourceType(gnocchiutils.GnocchiBase):

    def run(self, attributes=None):
        """Create resource type.

        :param attributes: List of attributes
        """
        name = self.generate_random_name()
        self.admin_gnocchi.create_resource_type(name, attributes=attributes)


@validation.add("required_services", services=[consts.Service.GNOCCHI])
@validation.add("required_platform", platform="openstack", admin=True)
@scenario.configure(
    context={"admin_cleanup@openstack": ["gnocchi.resource_type"]},
    name="GnocchiResourceType.create_delete_resource_type")
class CreateDeleteResourceType(gnocchiutils.GnocchiBase):
    def run(self, attributes=None):
        """Create resource type and then delete it.

        :param attributes: List of attributes
        """
        name = self.generate_random_name()
        self.admin_gnocchi.create_resource_type(name, attributes=attributes)
        self.admin_gnocchi.delete_resource_type(name)
