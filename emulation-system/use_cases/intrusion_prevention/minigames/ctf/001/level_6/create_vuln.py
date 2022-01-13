import os
from csle_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
import csle_common.constants.constants as constants


def default_vulns() -> VulnerabilitiesConfig:
    """
    :return: the VulnerabilitiesConfig of the emulation
    """
    vulns = [
        PwVulnerabilityConfig(node_ip="172.18.6.79", vuln_type=VulnType.WEAK_PW, username="l_hopital", pw="l_hopital",
                          root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.79", vuln_type=VulnType.WEAK_PW, username="euler", pw="euler",
                              root=False),
        PwVulnerabilityConfig(node_ip="172.18.6.79", vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.2", vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.3", vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.54", vuln_type=VulnType.WEAK_PW, username="vagrant", pw="vagrant",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.74", vuln_type=VulnType.WEAK_PW, username="administrator", pw="administrator",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.61", vuln_type=VulnType.WEAK_PW, username="adm",
                              pw="adm", root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.62", vuln_type=VulnType.WEAK_PW, username="guest", pw="guest", root=True),
        PwVulnerabilityConfig(node_ip="172.18.6.7", vuln_type=VulnType.WEAK_PW, username="ec2-user", pw="ec2-user",
                              root=True)
    ]
    vulns_config = VulnerabilitiesConfig(vulnerabilities=vulns)
    return vulns_config

# Generates the vuln.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_vulnerabilities_path()):
        VulnerabilityGenerator.write_vuln_config(default_vulns())
    vuln_config = util.read_vulns_config(util.default_vulnerabilities_path())
    emulation_config = EmulationConfig(agent_ip="172.18.6.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    VulnerabilityGenerator.create_vulns(vuln_cfg=vuln_config, emulation_config=emulation_config)