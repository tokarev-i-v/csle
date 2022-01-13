import os
from csle_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from csle_common.dao.container_config.rce_vulnerability_config import RceVulnerabilityConfig
from csle_common.dao.container_config.sql_injection_vulnerability_config import SQLInjectionVulnerabilityConfig
from csle_common.dao.container_config.priv_esc_vulnerability_config import PrivEscVulnerabilityConfig
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
import csle_common.constants.constants as constants


def default_vulns() -> VulnerabilitiesConfig:
    """
    :return: the VulnerabilitiesConfig of the emulation
    """
    vulns = [
        PwVulnerabilityConfig(node_ip="172.18.8.79", vuln_type=VulnType.WEAK_PW, username="l_hopital", pw="l_hopital",
                          root=True),
        PwVulnerabilityConfig(node_ip="172.18.8.79", vuln_type=VulnType.WEAK_PW, username="euler", pw="euler",
                              root=False),
        PwVulnerabilityConfig(node_ip="172.18.8.79", vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.8.2", vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.8.3", vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True),
        RceVulnerabilityConfig(node_ip="172.18.8.19", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.8.31", vuln_type=VulnType.RCE),
        SQLInjectionVulnerabilityConfig(node_ip="172.18.8.42", vuln_type=VulnType.SQL_INJECTION,
                                        username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7", root=True),
        RceVulnerabilityConfig(node_ip="172.18.8.37", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.8.82", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.8.75", vuln_type=VulnType.RCE),
        PwVulnerabilityConfig(node_ip="172.18.8.71", vuln_type=VulnType.WEAK_PW, username="alan", pw="alan", root=False),
        PrivEscVulnerabilityConfig(node_ip="172.18.8.71", vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="alan", pw="alan", root=False, cve="2010-1427"),
        PwVulnerabilityConfig(node_ip="172.18.8.11", vuln_type=VulnType.WEAK_PW, username="donald", pw="donald",
                              root=False),
        PrivEscVulnerabilityConfig(node_ip="172.18.8.11", vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="donald", pw="donald", root=False, cve="2015-5602"),
        PwVulnerabilityConfig(node_ip="172.18.8.51", vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.8.52", vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        RceVulnerabilityConfig(node_ip="172.18.8.54", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.8.55", vuln_type=VulnType.RCE),
        SQLInjectionVulnerabilityConfig(node_ip="172.18.8.56", vuln_type=VulnType.SQL_INJECTION,
                                        username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7", root=True),
        RceVulnerabilityConfig(node_ip="172.18.8.57", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.8.58", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.8.59", vuln_type=VulnType.RCE),
        PwVulnerabilityConfig(node_ip="172.18.8.60", vuln_type=VulnType.WEAK_PW, username="alan", pw="alan",
                              root=False),
        PrivEscVulnerabilityConfig(node_ip="172.18.8.60", vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="alan", pw="alan", root=False, cve="2010-1427"),
        PwVulnerabilityConfig(node_ip="172.18.8.61", vuln_type=VulnType.WEAK_PW, username="donald", pw="donald",
                              root=False),
        PrivEscVulnerabilityConfig(node_ip="172.18.8.61", vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="donald", pw="donald", root=False, cve="2015-5602"),
        PwVulnerabilityConfig(node_ip="172.18.8.62", vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=False)
    ]
    vulns_config = VulnerabilitiesConfig(vulnerabilities=vulns)
    return vulns_config

# Generates the vuln.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_vulnerabilities_path()):
        VulnerabilityGenerator.write_vuln_config(default_vulns())
    vuln_config = util.read_vulns_config(util.default_vulnerabilities_path())
    emulation_config = EmulationConfig(agent_ip="172.18.8.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    VulnerabilityGenerator.create_vulns(vuln_cfg=vuln_config, emulation_config=emulation_config)