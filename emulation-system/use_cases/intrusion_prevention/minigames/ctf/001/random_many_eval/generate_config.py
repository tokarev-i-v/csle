from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.container_env_config import ContainerEnvConfig

def generate_envs(num_envs : int, min_num_users : int = 1, max_num_users : int = 5, min_num_flags: int = 1,
                 max_num_flags : int = 5, min_num_nodes : int = 4, max_num_nodes : int = 10,
                 subnet_prefix: str = f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}") -> None:
    """
    Generates the random environment configurations

    :param num_envs: the number of environments to generate
    :param min_num_users: the minimum number of users per environment
    :param max_num_users: the maximum number of users per environment
    :param min_num_flags: the minimum number of flags per environment
    :param max_num_flags: the maximum number of flags per environment
    :param min_num_nodes: the minimum number of nodes per environment
    :param max_num_nodes: the maximum number of nodes per environment
    :param subnet_prefix: the subnet prefix of the environments networks
    :return: None
    """
    EnvConfigGenerator.cleanup_envs(path = util.default_output_dir())

    # container_pool = [(f"{constants.CONTAINER_IMAGES.FTP_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.FTP_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.HONEYPOT_1}", "0.0.1"),
    #                   (f"{constants.CONTAINER_IMAGES.HONEYPOT_2}", "0.0.1"),
    #                   (f"{constants.CONTAINER_IMAGES.SSH_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_2}", "0.0.1"),
    #                   (f"{constants.CONTAINER_IMAGES.SSH_3}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_3}", "0.0.1"),
    #                   (f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}", "0.0.1"),
    #                   (f"{constants.CONTAINER_IMAGES.SAMBA_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}", "0.0.1"),
    #                   (f"{constants.CONTAINER_IMAGES.CVE_2010_0426_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.CVE_2015_5602_1}", "0.0.1")
    #                   ]
    container_pool = [(f"{constants.CONTAINER_IMAGES.FTP_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.FTP_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.HONEYPOT_1}", "0.0.1"),
                      (f"{constants.CONTAINER_IMAGES.HONEYPOT_2}", "0.0.1"),
                      (f"{constants.CONTAINER_IMAGES.SSH_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_2}", "0.0.1"),
                      (f"{constants.CONTAINER_IMAGES.SSH_3}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_3}", "0.0.1"),
                      ]

    # gw_vuln_compatible_containers = [(f"{constants.CONTAINER_IMAGES.SSH_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_3}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_1}", "0.0.1"),
    #                                  (f"{constants.CONTAINER_IMAGES.TELNET_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_3}", "0.0.1"),
    #                                  (f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}", "0.0.1"),
    #                                  (f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}", "0.0.1"),
    #                                  (f"{constants.CONTAINER_IMAGES.SAMBA_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}", "0.0.1"),
    #                                  (f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}", "0.0.1")
    #                                  ]
    gw_vuln_compatible_containers = [(f"{constants.CONTAINER_IMAGES.SSH_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_3}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_1}", "0.0.1"),
                                     (f"{constants.CONTAINER_IMAGES.TELNET_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_3}", "0.0.1")]

    pw_vuln_compatible_containers = [(f"{constants.CONTAINER_IMAGES.SSH_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SSH_3}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_1}", "0.0.1"),
                                     (f"{constants.CONTAINER_IMAGES.TELNET_2}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.TELNET_3}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.FTP_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.FTP_2}", "0.0.1")
                                     ]
    # rce_vuln_compatible_containers = [(f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}", "0.0.1"),
    #                                   (f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}", "0.0.1"),
    #                                   (f"{constants.CONTAINER_IMAGES.SAMBA_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}", "0.0.1"),
    #                                   (f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}", "0.0.1")
    #                                   ]
    rce_vuln_compatible_containers = []
    # sql_injection_vuln_compatible_containers = [(f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}", "0.0.1")]
    sql_injection_vuln_compatible_containers = []
    # priv_esc_vuln_compatible_containers = [(f"{constants.CONTAINER_IMAGES.CVE_2010_0426_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.CVE_2015_5602_1}", "0.0.1")]
    priv_esc_vuln_compatible_containers = []

    agent_containers = [((f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}", "0.0.1"))]
    #router_containers = [(f"{constants.CONTAINER_IMAGES.ROUTER_1}", "0.0.1"), (f"{constants.CONTAINER_IMAGES.ROUTER_2}", "0.0.1")]
    router_containers = [(f"{constants.CONTAINER_IMAGES.ROUTER_2}", "0.0.1")]

    container_env_config = ContainerEnvConfig(
        min_num_users=min_num_users, max_num_users=max_num_users, min_num_flags=min_num_flags,
        max_num_flags=max_num_flags, min_num_nodes=min_num_nodes, max_num_nodes=max_num_nodes,
        container_pool=container_pool, gw_vuln_compatible_containers=gw_vuln_compatible_containers,
        pw_vuln_compatible_containers=pw_vuln_compatible_containers,
        rce_vuln_compatible_containers=rce_vuln_compatible_containers,
        sql_injection_vuln_compatible_containers=sql_injection_vuln_compatible_containers,
        priv_esc_vuln_compatible_containers=priv_esc_vuln_compatible_containers,
        agent_containers=agent_containers, router_containers=router_containers,
        path=util.default_output_dir(), subnet_id_blacklist=set(), subnet_prefix=subnet_prefix
    )

    EnvConfigGenerator.generate_envs(num_envs=num_envs, container_env_config = container_env_config,
                                     cleanup_old_envs=True)

# Creates the random environment configurations
if __name__ == '__main__':
    generate_envs(5, min_num_users=1, max_num_users=3, min_num_flags=1, max_num_flags=4, min_num_nodes=6,
                  max_num_nodes=15, subnet_prefix=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}")
