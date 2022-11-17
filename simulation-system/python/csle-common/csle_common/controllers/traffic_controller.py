from typing import List
import time
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
import csle_collector.client_manager.client_manager_util
import csle_collector.traffic_manager.traffic_manager_pb2_grpc
import csle_collector.traffic_manager.traffic_manager_pb2
import csle_collector.traffic_manager.query_traffic_manager
import csle_collector.traffic_manager.traffic_manager_util
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.traffic_managers_info import TrafficManagersInfo
from csle_common.util.emulation_util import EmulationUtil
from csle_common.dao.emulation_config.client_population_process_type import ClientPopulationProcessType
from csle_common.logging.log import Logger


class TrafficController:
    """
    Class managing traffic generators in the emulation environments
    """

    @staticmethod
    def start_traffic_managers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the traffic manager is running and starting it if it is not running
        on every node

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=node_traffic_config.ip)

            # Check if traffic_manager is already running
            cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                  + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                    conn=emulation_env_config.get_connection(ip=node_traffic_config.ip))

            if not constants.COMMANDS.SEARCH_TRAFFIC_MANAGER in str(o):

                Logger.__call__().get_logger().info(f"Starting traffic manager on node {node_traffic_config.ip}")

                # Stop old background job if running
                cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                      constants.COMMANDS.SPACE_DELIM \
                      + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME
                o, e, _ = EmulationUtil.execute_ssh_cmd(
                    cmd=cmd, conn=emulation_env_config.get_connection(ip=node_traffic_config.ip))

                # Start the _manager
                cmd = constants.COMMANDS.START_TRAFFIC_MANAGER.format(node_traffic_config.traffic_manager_port)
                o, e, _ = EmulationUtil.execute_ssh_cmd(
                    cmd=cmd, conn=emulation_env_config.get_connection(ip=node_traffic_config.ip))
                time.sleep(5)

    @staticmethod
    def stop_traffic_managers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for stopping traffic managers

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=node_traffic_config.ip)
            Logger.__call__().get_logger().info(f"Stopping traffic manager on node {node_traffic_config.ip}")

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=node_traffic_config.ip))

    @staticmethod
    def start_client_manager(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method starting the client manager

        :param emulation_env_config: the emulation env config
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.ip)

        # Check if client_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))

        if not constants.COMMANDS.SEARCH_CLIENT_MANAGER in str(o):
            Logger.__call__().get_logger().info(f"Starting client manager on node "
                                                f"{emulation_env_config.traffic_config.client_population_config.ip}")

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                emulation_env_config.traffic_config.client_population_config.client_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
            time.sleep(5)

    @staticmethod
    def stop_client_manager(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method starting the client manager

        :param emulation_env_config: the emulation env config
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.ip)

        Logger.__call__().get_logger().info(f"Stopping client manager on node "
                                            f"{emulation_env_config.traffic_config.client_population_config.ip}")

        # Stop old background job if running
        cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
              constants.COMMANDS.SPACE_DELIM \
              + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
            ip=emulation_env_config.traffic_config.client_population_config.ip))

    @staticmethod
    def stop_client_population(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Function for stopping the client arrival process of an emulation

        :param emulation_env_config: the emulation env config
        :return: None
        """
        Logger.__call__().get_logger().info(f"Stopping client population on container: "
              f"{emulation_env_config.traffic_config.client_population_config.ip}")

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port)

        if client_dto.client_process_active:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                    f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
                stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
                csle_collector.client_manager.query_clients.stop_clients(stub)

    @staticmethod
    def start_client_producer(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Starts the Kafka producer for client metrics

        :param emulation_env_config: the emulation environment configuration
        :return: None
        """
        Logger.__call__().get_logger().info(f"Starting client producer on container:"
                                            f" {emulation_env_config.traffic_config.client_population_config.ip}")

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port
        )
        if not client_dto.producer_active:

            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                    f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
                stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)

                # Start the producer thread
                csle_collector.client_manager.query_clients.start_producer(
                    stub=stub, ip=emulation_env_config.kafka_config.container.get_ips()[0],
                    port=emulation_env_config.kafka_config.kafka_port,
                    time_step_len_seconds=emulation_env_config.kafka_config.time_step_len_seconds)

    @staticmethod
    def stop_client_producer(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stops the Kafka producer for client metrics

        :param emulation_env_config: the emulation environment configuration
        :return: None
        """
        Logger.__call__().get_logger().info(f"Stopping client producer on container:"
                                            f" {emulation_env_config.traffic_config.client_population_config.ip}")

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port
        )

        if client_dto.producer_active:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                    f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
                stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)

                # Stop the producer thread
                csle_collector.client_manager.query_clients.start_producer(
                    stub=stub, ip=emulation_env_config.kafka_config.container.get_ips()[0],
                    port=emulation_env_config.kafka_config.kafka_port,
                    time_step_len_seconds=emulation_env_config.kafka_config.time_step_len_seconds)

    @staticmethod
    def start_client_population(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Starts the arrival process of clients

        :param emulation_env_config: the emulation environment configuration
        :return: None
        """
        Logger.__call__().get_logger().info(f"Starting client population on container:"
              f" {emulation_env_config.traffic_config.client_population_config.ip}")
        commands = []
        reachable_containers = []

        # Collect commands and reachable containers
        for container in emulation_env_config.containers_config.containers:
            match = False
            for ip,net in container.ips_and_networks:
                for net2 in emulation_env_config.traffic_config.client_population_config.networks:
                    if net.name == net2.name:
                        match = True
                        break
            if match:
                for ip2 in container.get_ips():
                    reachable_containers.append(ip2)

        for node_traffic_cfg in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_cfg.ip in reachable_containers:
                for cmd in node_traffic_cfg.commands:
                    commands.append(cmd.format(node_traffic_cfg.ip))

        for net in emulation_env_config.traffic_config.client_population_config.networks:
            for cmd in constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.TRAFFIC_COMMANDS.CLIENT_1_SUBNET]:
                commands.append(cmd.format(net.subnet_mask))

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port
        )

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)

            # Stop the client population if it is already running
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_clients(stub)
                time.sleep(5)

            # Start the client population
            sine_modulated = False
            if (emulation_env_config.traffic_config.client_population_config.client_process_type ==
                    ClientPopulationProcessType.SINE_MODULATED_POISSON):
                sine_modulated = True
            csle_collector.client_manager.query_clients.start_clients(
                stub=stub, mu=emulation_env_config.traffic_config.client_population_config.mu,
                lamb=emulation_env_config.traffic_config.client_population_config.lamb,
                time_step_len_seconds=
                emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds,
                commands=commands,
                num_commands=emulation_env_config.traffic_config.client_population_config.num_commands,
                sine_modulated=sine_modulated,
                time_scaling_factor=emulation_env_config.traffic_config.client_population_config.time_scaling_factor,
                period_scaling_factor=emulation_env_config.traffic_config.client_population_config.period_scaling_factor
            )

            time.sleep(5)

    @staticmethod
    def get_num_active_clients(emulation_env_config : EmulationEnvConfig) \
            -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Gets the number of active clients

        :param emulation_env_config: the emulation configuration
        :return: A ClientDTO which contains the number of active clients
        """

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port)
        return client_dto

    @staticmethod
    def get_clients_dto_by_ip_and_port(ip: str, port: int) -> \
            csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        A method that sends a request to the ClientManager on a specific container
        to get its status

        :param emulation_env_config: the emulation config
        :return: the status of the clientmanager
        """
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:{port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            status = csle_collector.client_manager.query_clients.get_clients(stub=stub)
            return status

    @staticmethod
    def stop_internal_traffic_generators(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility function for stopping internal traffic generators

        :param emulation_env_config: the configuration of the emulation env
        :return: None
        """
        TrafficController.start_traffic_managers(emulation_env_config=emulation_env_config)
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            Logger.__call__().get_logger().info(f"Stopping traffic generator script, "
                                                f"node ip:{node_traffic_config.ip}")

            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{node_traffic_config.ip}:{node_traffic_config.traffic_manager_port}') as channel:
                stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
                csle_collector.traffic_manager.query_traffic_manager.stop_traffic(stub)

    @staticmethod
    def start_internal_traffic_generators(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility function for starting internal traffic generators

        :param emulation_env_config: the configuration of the emulation env
        :return: None
        """
        TrafficController.start_traffic_managers(emulation_env_config=emulation_env_config)
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            Logger.__call__().get_logger().info(f"Starting traffic generator script, "
                                                f"node ip:{node_traffic_config.ip}")

            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{node_traffic_config.ip}:{node_traffic_config.traffic_manager_port}') as channel:
                stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
                csle_collector.traffic_manager.query_traffic_manager.start_traffic(stub)

    @staticmethod
    def create_internal_traffic_generator_scripts(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Installs the traffic generation scripts at each node

        :param emulation_env_config: the emulation env configuration
        :return: None
        """
        sleep_time = emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds
        for node in emulation_env_config.traffic_config.node_traffic_configs:
            container = None
            for c in emulation_env_config.containers_config.containers:
                if node.ip in c.get_ips():
                    container = c
                    break

            commands = []
            subnet_masks = []
            reachable_containers = []
            for ip_net1 in container.ips_and_networks:
                ip,net1 = ip_net1
                subnet_masks.append(net1.subnet_mask)
            for c in emulation_env_config.containers_config.containers:
                for ip_net1 in c.ips_and_networks:
                    ip,net1 = ip_net1
                    if net1.subnet_mask in subnet_masks and ip not in container.get_ips():
                        reachable_containers.append((ip, c.get_ips()))

            for node2 in emulation_env_config.traffic_config.node_traffic_configs:
                for rc in reachable_containers:
                    ip, ips = rc
                    if node2.ip in ips:
                        for cmd in node2.commands:
                            commands.append(cmd.format(ip))

            Logger.__call__().get_logger().info("Creating traffic generator script, node ip:{}".format(node.ip))

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=node.ip)

            # Remove old file if exists
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.RM_F + \
                  constants.COMMANDS.SPACE_DELIM + \
                  constants.COMMANDS.SLASH_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # File contents
            script_file = ""
            script_file = script_file + "#!/bin/bash\n"
            script_file = script_file + "while [ 1 ]\n"
            script_file = script_file + "do\n"
            script_file = script_file + "    sleep {}\n".format(sleep_time)
            for cmd in commands:
                script_file = script_file + "    " + cmd + "\n"
                script_file = script_file + "    sleep {}\n".format(sleep_time)
            script_file = script_file + "done\n"

            # Create file
            sftp_client = emulation_env_config.get_connection(ip=node.ip).open_sftp()
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.TOUCH + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Make executable
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.CHMOD_777 + \
                  constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Write traffic generation script file
            remote_file = sftp_client.open(constants.COMMANDS.SLASH_DELIM
                                           + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME, mode="w")
            try:
                remote_file.write(script_file)
            except Exception as e:
                Logger.__call__().get_logger().warning("exception writing traffic generation file:{}".format(str(e)))
            finally:
                remote_file.close()

            # Disconnect
            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)

    @staticmethod
    def get_client_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the Client managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [emulation_env_config.traffic_config.client_population_config.ip]

    @staticmethod
    def get_client_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Client managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        return [emulation_env_config.traffic_config.client_population_config.client_manager_port]

    @staticmethod
    def get_client_managers_info(emulation_env_config: EmulationEnvConfig) -> ClientManagersInfo:
        """
        Extracts the information of the Client managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: a DTO with the status of the Client managers
        """
        client_managers_ips = TrafficController.get_client_managers_ips(emulation_env_config=emulation_env_config)
        client_managers_ports = TrafficController.get_client_managers_ports(emulation_env_config=emulation_env_config)
        client_statuses = []
        running = False
        status = None
        for ip in client_managers_ips:
            try:
                status = TrafficController.get_clients_dto_by_ip_and_port(
                    ip=ip,
                    port=emulation_env_config.traffic_config.client_population_config.client_manager_port)
                running = True
            except Exception as e:
                Logger.__call__().get_logger().debug(
                    f"Could not fetch client manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                client_statuses.append(status)
            else:
                client_statuses.append(
                    csle_collector.client_manager.client_manager_util.ClientManagerUtil.clients_dto_empty())
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        client_manager_info_dto = ClientManagersInfo(
            running=running, ips=client_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, client_managers_statuses=client_statuses,  ports=client_managers_ports)
        return client_manager_info_dto

    @staticmethod
    def get_traffic_manager_status_by_port_and_ip(ip: str, port: int) -> \
            csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        A method that sends a request to the TrafficManager on a specific container
        to get its status

        :param emulation_env_config: the emulation config
        :return: the status of the traffic manager
        """
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:{port}') as channel:
            stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
            status = csle_collector.traffic_manager.query_traffic_manager.get_traffic_status(stub=stub)
            return status

    @staticmethod
    def get_traffic_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the ips of the traffic managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            try:
                TrafficController.get_traffic_manager_status_by_port_and_ip(
                    port=node_traffic_config.traffic_manager_port, ip = node_traffic_config.ip)
                ips.append(node_traffic_config.ip)
            except Exception as e:
                pass
        return ips

    @staticmethod
    def get_traffic_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Traffic managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            try:
                TrafficController.get_traffic_manager_status_by_port_and_ip(
                    port=node_traffic_config.traffic_manager_port, ip = node_traffic_config.ip)
                ports.append(node_traffic_config.traffic_manager_port)
            except Exception as e:
                pass
        return ports

    @staticmethod
    def get_traffic_managers_info(emulation_env_config: EmulationEnvConfig) -> TrafficManagersInfo:
        """
        Extracts the information of the traffic managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: a DTO with the status of the traffic managers
        """
        traffic_managers_ips = TrafficController.get_traffic_managers_ips(emulation_env_config=emulation_env_config)
        traffic_managers_ports = TrafficController.get_traffic_managers_ports(emulation_env_config=emulation_env_config)
        traffic_managers_statuses = []
        running = False
        status = None
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_config.ip in traffic_managers_ips:
                try:
                    status = TrafficController.get_traffic_manager_status_by_port_and_ip(
                        port=node_traffic_config.traffic_manager_port, ip=node_traffic_config.ip)
                    running = True
                except Exception as e:
                    Logger.__call__().get_logger().debug(
                        f"Could not fetch traffic manager status on IP:{node_traffic_config}, error: {str(e)}, {repr(e)}")
                if status is not None:
                    traffic_managers_statuses.append(status)
                else:
                    traffic_managers_statuses.append(
                        csle_collector.traffic_manager.traffic_manager_util.TrafficManagerUtil.traffic_dto_empty())
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        traffic_manager_info_dto = TrafficManagersInfo(
            running=running, ips=traffic_managers_ips, execution_id=execution_id, emulation_name=emulation_name,
            traffic_managers_statuses=traffic_managers_statuses, ports=traffic_managers_ports)
        return traffic_manager_info_dto