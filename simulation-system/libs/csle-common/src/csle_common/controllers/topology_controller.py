import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class TopologyController:
    """
    Class managing topologies in the emulation environments
    """

    @staticmethod
    def create_topology(emulation_env_config: EmulationEnvConfig, physical_server_ip: str) -> None:
        """
        Utility function for connecting to a running emulation and creating the configuration

        :param emulation_env_config: the emulation configuration
        :param physical_server_ip: ip of the physical server
        :return: None
        """
        Logger.__call__().get_logger().info("Creating topology")
        topology_configs = emulation_env_config.topology_config.node_configs
        topology_configs = topology_configs + [emulation_env_config.kafka_config.firewall_config]
        if emulation_env_config.sdn_controller_config is not None:
            topology_configs = topology_configs + [emulation_env_config.sdn_controller_config.firewall_config]
        for node_fw_config in topology_configs:
            if node_fw_config.physical_host_ip != physical_server_ip:
                continue
            ip = node_fw_config.docker_gw_bridge_ip
            Logger.__call__().get_logger().info(f"Connecting to node:{ip}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

            for route in node_fw_config.routes:
                target, gw = route
                cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} {target} gw {gw}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for default_network_fw_config in node_fw_config.ips_gw_default_policy_networks:
                if default_network_fw_config.default_gw is not None:
                    cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} " \
                          f"-net {default_network_fw_config.network.subnet_mask.replace('/24', '')} " \
                          f"{constants.COMMANDS.NETMASK} {default_network_fw_config.network.bitmask} " \
                          f"gw {default_network_fw_config.default_gw}"
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                                  wait_for_completion=True)

            cmd = constants.COMMANDS.CLEAR_IPTABLES
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                          wait_for_completion=True)

            # Setup /etc/hosts
            internal_ip = node_fw_config.get_ips()[0]
            cmd = f"{constants.COMMANDS.ECHO} '" + internal_ip + " " + \
                  node_fw_config.hostname + f"' | {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            cmd = f"{constants.COMMANDS.ECHO} " \
                  f"{constants.ETC_HOSTS.DEFAULT_HOST_LINE_1} | {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_2} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_3} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_4} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_5} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_6} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            for node2 in emulation_env_config.topology_config.node_configs:
                ips2 = node_fw_config.get_ips()
                if ip not in ips2:
                    cmd = f"{constants.COMMANDS.ECHO} '" + ips2[0] + " " + node2.hostname \
                          + f"' | {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            # Setup iptables and arptables
            for output_node in node_fw_config.output_accept:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for input_node in node_fw_config.input_accept:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for forward_node in node_fw_config.forward_accept:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d {forward_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for output_node in node_fw_config.output_drop:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for input_node in node_fw_config.input_drop:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for forward_node in node_fw_config.forward_drop:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d {forward_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            for default_network_fw_config in node_fw_config.ips_gw_default_policy_networks:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_output}"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                                        wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_output}"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                                        wait_for_completion=True)

                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_FORWARD} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip),
                                              wait_for_completion=True)

            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)
