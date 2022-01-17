import os
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants


def default_containers_config(network_id: int = 5):
    """
    :param network_id: the network id
    :return: the ContainersConfig of the emulation
    """
    containers = [
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CLIENT_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.FTP_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf", version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.ROUTER_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_1}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.FTP_2}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_2}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_3}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_2}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_3}", network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                            minigame="ctf",
                            version="0.0.1", level="5",
                            ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62")
    ]
    containers_cfg = ContainersConfig(containers=containers,
                                      network=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}_{network_id}",
                                      agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                      router_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                      subnet_mask=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}"
                                                  f"{constants.CSLE.CSLE_SUBNETMASK}",
                                      subnet_prefix=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.",
                                      ids_enabled=True)
    return containers_cfg


# Generates the containers.json configuration file
if __name__ == '__main__':
    network_id = 5
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config(network_id=network_id)
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())
