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
from rally_openstack.task.scenarios.ceilometer import utils as ceiloutils


"""Scenarios for Ceilometer Samples API."""


@validation.add("required_services",
                services=[consts.Service.CEILOMETER])
@validation.add("required_contexts", contexts=("ceilometer"))
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(name="CeilometerSamples.list_matched_samples",
                    platform="openstack")
class ListMatchedSamples(ceiloutils.CeilometerScenario):

    def run(self, filter_by_resource_id=False, filter_by_project_id=False,
            filter_by_user_id=False, metadata_query=None, limit=None):
        """Get list of samples that matched fields from context and args.

        :param filter_by_user_id: flag for query by user_id
        :param filter_by_project_id: flag for query by project_id
        :param filter_by_resource_id: flag for query by resource_id
        :param metadata_query: dict with metadata fields and values for query
        :param limit: count of samples in response
        """
        query = self._make_general_query(filter_by_project_id,
                                         filter_by_user_id,
                                         filter_by_resource_id,
                                         metadata_query)
        self._list_samples(query, limit)


@validation.add("required_services",
                services=[consts.Service.CEILOMETER])
@validation.add("required_contexts", contexts=("ceilometer"))
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(name="CeilometerSamples.list_samples",
                    platform="openstack")
class ListSamples(ceiloutils.CeilometerScenario):

    def run(self, metadata_query=None, limit=None):
        """Fetch all available queries for list sample request.

        :param metadata_query: dict with metadata fields and values for query
        :param limit: count of samples in response
        """

        scenario = ListMatchedSamples(self.context)
        scenario.run(filter_by_project_id=True)
        scenario.run(filter_by_user_id=True)
        scenario.run(filter_by_resource_id=True)
        if metadata_query:
            scenario.run(metadata_query=metadata_query)
        if limit:
            scenario.run(limit=limit)
