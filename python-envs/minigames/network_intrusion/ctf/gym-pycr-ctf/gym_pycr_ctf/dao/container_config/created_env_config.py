from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_ctf.dao.container_config.users_config import UsersConfig
from gym_pycr_ctf.dao.container_config.traffic_config import TrafficConfig


class CreatedEnvConfig:
    """
    A DTO representing the configuration of a created emulation environment
    """

    def __init__(self, containers_config: ContainersConfig, traffic_config: TrafficConfig, flags_config: FlagsConfig,
                 vuln_config: VulnerabilitiesConfig, topology: Topology, users_config: UsersConfig
                 ):
        self.containers_config = containers_config
        self.traffic_config = traffic_config
        self.flags_config = flags_config
        self.vuln_config = vuln_config
        self.topology = topology
        self.users_config = users_config

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "containers_config:{}, traffic_config:{}, flags_config:{}, vuln_config:{}, topology:{}, " \
               "users_config:{}".format(
            self.containers_config, self.traffic_config, self.flags_config, self.vuln_config,
            self.topology, self.users_config)