# Copyright 2014: Mirantis Inc.
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

import requests

from rally.common import validation
from rally import exceptions

from rally_openstack.common import consts
from rally_openstack.common import osclients
from rally_openstack.task.cleanup import manager as resource_manager
from rally_openstack.task import context
from rally_openstack.task.scenarios.sahara import utils


@validation.add("required_platform", platform="openstack", users=True)
@context.configure(name="sahara_job_binaries", platform="openstack", order=442)
class SaharaJobBinaries(context.OpenStackContext):
    """Context class for setting up Job Binaries for an EDP job."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "mains": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "download_url": {
                            "type": "string"
                        }
                    },
                    "additionalProperties": False,
                    "required": ["name", "download_url"]
                }
            },
            "libs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "download_url": {
                            "type": "string"
                        }
                    },
                    "additionalProperties": False,
                    "required": ["name", "download_url"]
                }
            }
        },
        "additionalProperties": False
    }

    # This cache will hold the downloaded libs content to prevent repeated
    # downloads for each tenant
    lib_cache = {}

    def setup(self):
        utils.init_sahara_context(self)
        for user, tenant_id in self._iterate_per_tenants():

            clients = osclients.Clients(user["credential"])
            sahara = clients.sahara()

            self.context["tenants"][tenant_id]["sahara"]["mains"] = []
            self.context["tenants"][tenant_id]["sahara"]["libs"] = []

            for main in self.config.get("mains", []):
                self.download_and_save_lib(
                    sahara=sahara,
                    lib_type="mains",
                    name=main["name"],
                    download_url=main["download_url"],
                    tenant_id=tenant_id)

            for lib in self.config.get("libs", []):
                self.download_and_save_lib(
                    sahara=sahara,
                    lib_type="libs",
                    name=lib["name"],
                    download_url=lib["download_url"],
                    tenant_id=tenant_id)

    def setup_inputs(self, sahara, tenant_id, input_type, input_url):
        if input_type == "swift":
            raise exceptions.RallyException(
                "Swift Data Sources are not implemented yet")
        # Todo(nkonovalov): Add swift credentials parameters and data upload
        input_ds = sahara.data_sources.create(
            name=self.generate_random_name(),
            description="",
            data_source_type=input_type,
            url=input_url)

        self.context["tenants"][tenant_id]["sahara"]["input"] = input_ds.id

    def download_and_save_lib(self, sahara, lib_type, name, download_url,
                              tenant_id):
        if download_url not in self.lib_cache:
            lib_data = requests.get(download_url).content
            self.lib_cache[download_url] = lib_data
        else:
            lib_data = self.lib_cache[download_url]

        job_binary_internal = sahara.job_binary_internals.create(
            name=name,
            data=lib_data)

        url = "internal-db://%s" % job_binary_internal.id
        job_binary = sahara.job_binaries.create(name=name,
                                                url=url,
                                                description="",
                                                extra={})

        self.context["tenants"][tenant_id]["sahara"][lib_type].append(
            job_binary.id)

    def cleanup(self):
        resources = ["job_binary_internals", "job_binaries"]

        resource_manager.cleanup(
            names=["sahara.%s" % res for res in resources],
            users=self.context.get("users", []),
            superclass=utils.SaharaScenario,
            task_id=self.context["task"]["uuid"])
