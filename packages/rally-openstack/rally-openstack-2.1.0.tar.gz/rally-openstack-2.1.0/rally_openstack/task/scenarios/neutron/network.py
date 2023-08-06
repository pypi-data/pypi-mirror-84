# Copyright 2014: Intel Inc.
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

from rally.common import cfg
from rally.common import logging
from rally.task import validation

from rally_openstack.common import consts
from rally_openstack.task import scenario
from rally_openstack.task.scenarios.neutron import utils


LOG = logging.getLogger(__name__)


"""Scenarios for Neutron."""


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_list_networks",
                    platform="openstack")
class CreateAndListNetworks(utils.NeutronBaseScenario):

    def run(self, network_create_args=None):
        """Create a network and then list all networks.

        Measure the "neutron net-list" command performance.

        If you have only 1 user in your context, you will
        add 1 network on every iteration. So you will have more
        and more networks and will be able to measure the
        performance of the "neutron net-list" command depending on
        the number of networks owned by users.

        :param network_create_args: dict, POST /v2.0/networks request options
        """
        self.neutron.create_network(**(network_create_args or {}))
        self.neutron.list_networks()


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_show_network",
                    platform="openstack")
class CreateAndShowNetwork(utils.NeutronBaseScenario):

    def run(self, network_create_args=None):
        """Create a network and show network details.

        Measure the "neutron net-show" command performance.

        :param network_create_args: dict, POST /v2.0/networks request options
        """
        network = self.neutron.create_network(**(network_create_args or {}))
        self.neutron.get_network(network["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_update_args")
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_update_networks",
                    platform="openstack")
class CreateAndUpdateNetworks(utils.NeutronBaseScenario):

    def run(self, network_update_args, network_create_args=None):
        """Create and update a network.

        Measure the "neutron net-create and net-update" command performance.

        :param network_update_args: dict, PUT /v2.0/networks update request
        :param network_create_args: dict, POST /v2.0/networks request options
        """
        network = self.neutron.create_network(**(network_create_args or {}))
        self.neutron.update_network(network["id"], **network_update_args)


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_delete_networks",
                    platform="openstack")
class CreateAndDeleteNetworks(utils.NeutronBaseScenario):

    def run(self, network_create_args=None):
        """Create and delete a network.

        Measure the "neutron net-create" and "net-delete" command performance.

        :param network_create_args: dict, POST /v2.0/networks request options
        """
        network = self.neutron.create_network(**(network_create_args or {}))
        self.neutron.delete_network(network["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_list_subnets",
                    platform="openstack")
class CreateAndListSubnets(utils.NeutronBaseScenario):

    def run(self, network_create_args=None, subnet_create_args=None,
            subnet_cidr_start=None, subnets_per_network=1):
        """Create and a given number of subnets and list all subnets.

        The scenario creates a network, a given number of subnets and then
        lists subnets.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        """
        network = self.neutron.create_network(**(network_create_args or {}))
        for _ in range(subnets_per_network):
            self.neutron.create_subnet(network["id"],
                                       start_cidr=subnet_cidr_start,
                                       **(subnet_create_args or {}))
        self.neutron.list_subnets()


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_update_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_update_subnets",
                    platform="openstack")
class CreateAndUpdateSubnets(utils.NeutronBaseScenario):

    def run(self, subnet_update_args, network_create_args=None,
            subnet_create_args=None, subnet_cidr_start=None,
            subnets_per_network=1):
        """Create and update a subnet.

        The scenario creates a network, a given number of subnets
        and then updates the subnet. This scenario measures the
        "neutron subnet-update" command performance.

        :param subnet_update_args: dict, PUT /v2.0/subnets update options
        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        """
        network = self.neutron.create_network(**(network_create_args or {}))
        subnets = []
        for _ in range(subnets_per_network):
            subnets.append(
                self.neutron.create_subnet(
                    network["id"], start_cidr=subnet_cidr_start,
                    **(subnet_create_args or {}))
            )
        for subnet in subnets:
            self.neutron.update_subnet(subnet["id"], **subnet_update_args)


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_show_subnets",
                    platform="openstack")
class CreateAndShowSubnets(utils.NeutronBaseScenario):

    def run(self, network_create_args=None,
            subnet_create_args=None, subnet_cidr_start=None,
            subnets_per_network=1):
        """Create and show a subnet details.

        The scenario creates a network, a given number of subnets
        and show the subnet details. This scenario measures the
        "neutron subnet-show" command performance.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options.
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        """
        network = self._get_or_create_network(**(network_create_args or {}))
        subnets = []
        for _ in range(subnets_per_network):
            subnets.append(
                self.neutron.create_subnet(
                    network["id"], start_cidr=subnet_cidr_start,
                    **(subnet_create_args or {}))
            )
        for subnet in subnets:
            self.neutron.get_subnet(subnet["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_delete_subnets",
                    platform="openstack")
class CreateAndDeleteSubnets(utils.NeutronBaseScenario):

    def run(self, network_create_args=None, subnet_create_args=None,
            subnet_cidr_start=None, subnets_per_network=1):
        """Create and delete a given number of subnets.

        The scenario creates a network, a given number of subnets and then
        deletes subnets.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        """
        network = self._get_or_create_network(**(network_create_args or {}))
        subnets = []
        for _ in range(subnets_per_network):
            subnets.append(
                self.neutron.create_subnet(
                    network["id"], start_cidr=subnet_cidr_start,
                    **(subnet_create_args or {}))
            )
        for subnet in subnets:
            self.neutron.delete_subnet(subnet["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="router_create_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_list_routers",
                    platform="openstack")
class CreateAndListRouters(utils.NeutronBaseScenario):

    def run(self, network_create_args=None, subnet_create_args=None,
            subnet_cidr_start=None, subnets_per_network=1,
            router_create_args=None):
        """Create and a given number of routers and list all routers.

        Create a network, a given number of subnets and routers
        and then list all routers.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        :param router_create_args: dict, POST /v2.0/routers request options
        """
        subnet_create_args = dict(subnet_create_args or {})
        subnet_create_args["start_cidr"] = subnet_cidr_start

        self.neutron.create_network_topology(
            network_create_args=(network_create_args or {}),
            router_create_args=(router_create_args or {}),
            router_per_subnet=True,
            subnet_create_args=subnet_create_args,
            subnets_count=subnets_per_network
        )
        self.neutron.list_routers()


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="router_create_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services", services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_show_routers",
                    platform="openstack")
class CreateAndShowRouters(utils.NeutronBaseScenario):

    def run(self, network_create_args=None, subnet_create_args=None,
            subnet_cidr_start=None, subnets_per_network=1,
            router_create_args=None):
        """Create and show a given number of routers.

        Create a network, a given number of subnets and routers
        and then show all routers.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for each network
        :param router_create_args: dict, POST /v2.0/routers request options
        """
        subnet_create_args = dict(subnet_create_args or {})
        subnet_create_args["start_cidr"] = subnet_cidr_start

        net_topo = self.neutron.create_network_topology(
            network_create_args=(network_create_args or {}),
            router_create_args=(router_create_args or {}),
            router_per_subnet=True,
            subnet_create_args=subnet_create_args,
            subnets_count=subnets_per_network
        )

        for router in net_topo["routers"]:
            self.neutron.get_router(router["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="router_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="router_update_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_update_routers",
                    platform="openstack")
class CreateAndUpdateRouters(utils.NeutronBaseScenario):

    def run(self, router_update_args, network_create_args=None,
            subnet_create_args=None, subnet_cidr_start=None,
            subnets_per_network=1, router_create_args=None):
        """Create and update a given number of routers.

        Create a network, a given number of subnets and routers
        and then updating all routers.

        :param router_update_args: dict, PUT /v2.0/routers update options
        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        :param router_create_args: dict, POST /v2.0/routers request options
        """
        subnet_create_args = dict(subnet_create_args or {})
        subnet_create_args["start_cidr"] = subnet_cidr_start

        net_topo = self.neutron.create_network_topology(
            network_create_args=(network_create_args or {}),
            router_create_args=(router_create_args or {}),
            router_per_subnet=True,
            subnet_create_args=subnet_create_args,
            subnets_count=subnets_per_network
        )

        for router in net_topo["routers"]:
            self.neutron.update_router(router["id"], **router_update_args)


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="subnet_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="router_create_args")
@validation.add("number", param_name="subnets_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_delete_routers",
                    platform="openstack")
class CreateAndDeleteRouters(utils.NeutronBaseScenario):

    def run(self, network_create_args=None, subnet_create_args=None,
            subnet_cidr_start=None, subnets_per_network=1,
            router_create_args=None):
        """Create and delete a given number of routers.

        Create a network, a given number of subnets and routers
        and then delete all routers.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param subnet_create_args: dict, POST /v2.0/subnets request options
        :param subnet_cidr_start: str, start value for subnets CIDR
        :param subnets_per_network: int, number of subnets for one network
        :param router_create_args: dict, POST /v2.0/routers request options
        """
        subnet_create_args = dict(subnet_create_args or {})
        subnet_create_args["start_cidr"] = subnet_cidr_start

        net_topo = self.neutron.create_network_topology(
            network_create_args=(network_create_args or {}),
            router_create_args=(router_create_args or {}),
            router_per_subnet=True,
            subnet_create_args=subnet_create_args,
            subnets_count=subnets_per_network
        )

        for e in range(subnets_per_network):
            router = net_topo["routers"][e]
            subnet = net_topo["subnets"][e]
            self.neutron.remove_interface_from_router(subnet_id=subnet["id"],
                                                      router_id=router["id"])
            self.neutron.delete_router(router["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="router_create_args")
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.set_and_clear_router_gateway",
                    platform="openstack")
class SetAndClearRouterGateway(utils.NeutronBaseScenario):

    def run(self, enable_snat=True, network_create_args=None,
            router_create_args=None):
        """Set and Remove the external network gateway from a router.

        create an external network and a router, set external network
        gateway for the router, remove the external network gateway from
        the router.

        :param enable_snat: True if enable snat
        :param network_create_args: dict, POST /v2.0/networks request
                                    options
        :param router_create_args: dict, POST /v2.0/routers request options
        """
        network_create_args = network_create_args or {}
        router_create_args = router_create_args or {}

        ext_net = self.neutron.create_network(**network_create_args)
        router = self.neutron.create_router(**router_create_args)
        self.neutron.add_gateway_to_router(router_id=router["id"],
                                           network_id=ext_net["id"],
                                           enable_snat=enable_snat)
        self.neutron.remove_gateway_from_router(router["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="port_create_args")
@validation.add("number", param_name="ports_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_list_ports",
                    platform="openstack")
class CreateAndListPorts(utils.NeutronBaseScenario):

    def run(self, network_create_args=None,
            port_create_args=None, ports_per_network=1):
        """Create and a given number of ports and list all ports.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param port_create_args: dict, POST /v2.0/ports request options
        :param ports_per_network: int, number of ports for one network
        """
        network = self._get_or_create_network(**(network_create_args or {}))
        for i in range(ports_per_network):
            self.neutron.create_port(network["id"], **(port_create_args or {}))

        self.neutron.list_ports()


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="port_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="port_update_args")
@validation.add("number", param_name="ports_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_update_ports",
                    platform="openstack")
class CreateAndUpdatePorts(utils.NeutronBaseScenario):

    def run(self, port_update_args, network_create_args=None,
            port_create_args=None, ports_per_network=1):
        """Create and update a given number of ports.

        Measure the "neutron port-create" and "neutron port-update" commands
        performance.

        :param port_update_args: dict, PUT /v2.0/ports update request options
        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param port_create_args: dict, POST /v2.0/ports request options
        :param ports_per_network: int, number of ports for one network
        """
        network = self._get_or_create_network(**(network_create_args or {}))
        for i in range(ports_per_network):
            port = self.neutron.create_port(
                network["id"], **(port_create_args or {}))
            self.neutron.update_port(port["id"], **port_update_args)


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="port_create_args")
@validation.add("number", param_name="ports_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_show_ports",
                    platform="openstack")
class CreateAndShowPorts(utils.NeutronBaseScenario):

    def run(self, network_create_args=None,
            port_create_args=None, ports_per_network=1):
        """Create a given number of ports and show created ports in trun.

        Measure the "neutron port-create" and "neutron port-show" commands
        performance.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options.
        :param port_create_args: dict, POST /v2.0/ports request options
        :param ports_per_network: int, number of ports for one network
        """
        network = self._get_or_create_network(**(network_create_args or {}))
        for i in range(ports_per_network):
            port = self.neutron.create_port(
                network["id"], **(port_create_args or {}))

            self.neutron.get_port(port["id"])


@validation.add("restricted_parameters",
                param_names="name",
                subdict="network_create_args")
@validation.add("restricted_parameters",
                param_names="name",
                subdict="port_create_args")
@validation.add("number", param_name="ports_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_delete_ports",
                    platform="openstack")
class CreateAndDeletePorts(utils.NeutronBaseScenario):

    def run(self, network_create_args=None,
            port_create_args=None, ports_per_network=1):
        """Create and delete a port.

        Measure the "neutron port-create" and "neutron port-delete"
        commands performance.

        :param network_create_args: dict, POST /v2.0/networks request
                                    options. Deprecated.
        :param port_create_args: dict, POST /v2.0/ports request options
        :param ports_per_network: int, number of ports for one network
        """
        network = self._get_or_create_network(**(network_create_args or {}))
        for i in range(ports_per_network):
            port = self.neutron.create_port(
                network["id"], **(port_create_args or {}))

            self.neutron.delete_port(port["id"])


@validation.add("number", param_name="ports_per_network", minval=1,
                integer_only=True)
@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_contexts", contexts=["network", "networking_agents"])
@validation.add("required_platform", platform="openstack",
                users=True, admin=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"],
                             "networking_agents@openstack": {},
                             "network@openstack": {}},
                    name="NeutronNetworks.create_and_bind_ports",
                    platform="openstack")
class CreateAndBindPorts(utils.NeutronBaseScenario):

    def run(self, ports_per_network=1):
        """Bind a given number of ports.

        Measure the performance of port binding and all of its pre-requisites:
        * openstack network create
        * openstack subnet create --ip-version 4
        * openstack subnet create --ip-version 6
        * openstack port create
        * openstack port update (binding)

        :param ports_per_network: int, number of ports for one network
        """

        # NOTE(bence romsics): Find a host where we can expect to bind
        # successfully. Look at agent types used in the gate.
        host_to_bind = None
        for agent in self.context["networking_agents"]:
            if (agent["admin_state_up"]
                    and agent["alive"]
                    and agent["agent_type"] in
                    cfg.CONF.openstack.neutron_bind_l2_agent_types):
                host_to_bind = agent["host"]
        if host_to_bind is None:
            raise Exception(
                "No live agent of type(s) to bind was found: %s" %
                ", ".join(cfg.CONF.openstack.neutron_bind_l2_agent_types))

        tenant_id = self.context["tenant"]["id"]
        for network in self.context["tenants"][tenant_id]["networks"]:
            self.neutron.create_subnet(network_id=network["id"], ip_version=4)
            self.neutron.create_subnet(network_id=network["id"], ip_version=6)

            for i in range(ports_per_network):
                port = self.neutron.create_port(network_id=network["id"])
                # port bind needs admin role
                self.admin_neutron.update_port(
                    port_id=port["id"],
                    device_owner="compute:nova",
                    device_id="ba805478-85ff-11e9-a2e4-2b8dea218fc8",
                    **{"binding:host_id": host_to_bind},
                )


@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("external_network_exists", param_name="floating_network")
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_list_floating_ips",
                    platform="openstack")
class CreateAndListFloatingIps(utils.NeutronBaseScenario):

    def run(self, floating_network=None, floating_ip_args=None):
        """Create and list floating IPs.

        Measure the "neutron floating-ip-create" and "neutron floating-ip-list"
        commands performance.

        :param floating_network: str, external network for floating IP creation
        :param floating_ip_args: dict, POST /floatingips request options
        """
        floating_ip_args = floating_ip_args or {}
        self.neutron.create_floatingip(floating_network=floating_network,
                                       **floating_ip_args)
        self.neutron.list_floatingips()


@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("external_network_exists", param_name="floating_network")
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronNetworks.create_and_delete_floating_ips",
                    platform="openstack")
class CreateAndDeleteFloatingIps(utils.NeutronBaseScenario):

    def run(self, floating_network=None, floating_ip_args=None):
        """Create and delete floating IPs.

        Measure the "neutron floating-ip-create" and "neutron
        floating-ip-delete" commands performance.

        :param floating_network: str, external network for floating IP creation
        :param floating_ip_args: dict, POST /floatingips request options
        """
        floating_ip_args = floating_ip_args or {}
        floatingip = self.neutron.create_floatingip(
            floating_network=floating_network, **floating_ip_args)
        self.neutron.delete_floatingip(floatingip["id"])


@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("external_network_exists", param_name="floating_network")
@scenario.configure(
    context={"cleanup@openstack": ["neutron"]},
    name="NeutronNetworks.associate_and_dissociate_floating_ips",
    platform="openstack")
class AssociateAndDissociateFloatingIps(utils.NeutronBaseScenario):

    def run(self, floating_network=None):
        """Associate and dissociate floating IPs.

        Measure the "openstack floating ip set" and
        "openstack floating ip unset" commands performance.
        Because of the prerequisites for "floating ip set/unset" we also
        measure the performance of the following commands:

          * "openstack network create"
          * "openstack subnet create"
          * "openstack port create"
          * "openstack router create"
          * "openstack router set --external-gateway"
          * "openstack router add subnet"

        :param floating_network: str, external network for floating IP creation
        """
        floating_network = self.neutron.find_network(floating_network,
                                                     external=True)
        floating_ip = self.neutron.create_floatingip(
            floating_network=floating_network)

        private_network = self.neutron.create_network()
        subnet = self.neutron.create_subnet(network_id=private_network["id"])
        port = self.neutron.create_port(network_id=private_network["id"])

        router = self.neutron.create_router()
        self.neutron.add_gateway_to_router(
            router["id"], network_id=floating_network["id"])
        self.neutron.add_interface_to_router(
            subnet_id=subnet["id"], router_id=router["id"])

        self.neutron.associate_floatingip(
            floatingip_id=floating_ip["id"], port_id=port["id"])
        self.neutron.dissociate_floatingip(floatingip_id=floating_ip["id"])


@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(name="NeutronNetworks.list_agents", platform="openstack")
class ListAgents(utils.NeutronBaseScenario):

    def run(self, agent_args=None):
        """List all neutron agents.

        This simple scenario tests the "neutron agent-list" command by
        listing all the neutron agents.

        :param agent_args: dict, POST /v2.0/agents request options
        """
        agent_args = agent_args or {}
        self.neutron.list_agents(**agent_args)


@validation.add("required_services",
                services=[consts.Service.NEUTRON])
@validation.add("required_contexts", contexts=["network"])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["neutron"]},
                    name="NeutronSubnets.delete_subnets",
                    platform="openstack")
class DeleteSubnets(utils.NeutronBaseScenario):

    def run(self):
        """Delete a subnet that belongs to each precreated network.

        Each runner instance picks a specific subnet from the list based on its
        positional location in the list of users. By doing so, we can start
        multiple threads with sufficient number of users created and spread
        delete requests across all of them, so that they hit different subnets
        concurrently.

        Concurrent execution of this scenario should help reveal any race
        conditions and other concurrency issues in Neutron IP allocation layer,
        among other things.
        """
        tenant_id = self.context["tenant"]["id"]
        users = self.context["tenants"][tenant_id]["users"]
        number = users.index(self.context["user"])
        for network in self.context["tenants"][tenant_id]["networks"]:
            # delete one of subnets based on the user sequential number
            subnet_id = network["subnets"][number]
            self.neutron.delete_subnet(subnet_id)
