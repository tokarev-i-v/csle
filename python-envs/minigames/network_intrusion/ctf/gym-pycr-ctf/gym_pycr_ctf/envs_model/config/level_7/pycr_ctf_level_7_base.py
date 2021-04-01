from typing import List
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.node import Node
from gym_pycr_ctf.dao.network.flag import Flag
from gym_pycr_ctf.dao.network.node_type import NodeType
from gym_pycr_ctf.dao.network.network_config import NetworkConfig
from gym_pycr_ctf.dao.render.render_config import RenderConfig
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_pycr_ctf.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from gym_pycr_ctf.dao.action.attacker.attacker_nikto_actions import AttackerNIKTOActions
from gym_pycr_ctf.dao.action.attacker.attacker_masscan_actions import AttackerMasscanActions
from gym_pycr_ctf.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from gym_pycr_ctf.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.network.network_service import NetworkService
from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability
from gym_pycr_ctf.dao.network.credential import Credential
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.state_representation.state_type import StateType
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.action.defender.defender_action_config import DefenderActionConfig
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_pycr_ctf.dao.action.defender.defender_stopping_actions import DefenderStoppingActions

class PyCrCTFLevel7Base:
    """
    Base configuration of level 1 of the PyCrCTF environment. (Mainly used when running in simulation mode
    and all the config of the environment have to be hardcoded)
    """
    @staticmethod
    def nodes() -> List[Node]:
        """
        Returns the configuration of all nodes in the environment

        :return: list of node configs
        """
        nodes = [Node(ip="172.18.7.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                      os="linux", vulnerabilities=[], credentials=[
                Credential(username="admin", pw="admin"),
                Credential(username="jessica", pw="water")
            ], reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79",
                                      "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42",
                                      "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      root_usernames=["admin"]),
                 Node(ip="172.18.7.2", ip_id=2, id=2, type=NodeType.SERVER, reachable_nodes =
                 set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191", "172.18.7.10",
                      "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                      "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      flags=[Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="test32121"),
                          Credential(username="puppet", pw="puppet"),
                          Credential(username="user1", pw="123123")
                      ],
                      root_usernames=["admin", "user1"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh",
                                         credentials=[
                                             Credential(username="admin", pw="test32121", port=22,
                                                        protocol = TransportProtocol.TCP, service = "ssh"),
                                             Credential(username="puppet", pw="puppet",
                                                        protocol = TransportProtocol.TCP, service = "ssh"),
                                             Credential(username="user1", pw="123123",
                                                        protocol = TransportProtocol.TCP, service = "ssh")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=53, name="domain", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9042, name="cassandra", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9160, name="cassandra", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=53, name="domain", credentials=[]),
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        service=constants.SSH.SERVICE_NAME,
                                        credentials=[
                                            Credential(username="puppet", pw="puppet",
                                                       protocol=TransportProtocol.TCP, service=constants.SSH.SERVICE_NAME)
                                        ],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8620", cve="CVE-2020-8620", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8617", cve="CVE-2020-8617", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8616", cve="CVE-2020-8616", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2019-6470", cve="CVE-2019-6470", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8623", cve="CVE-2020-8623", cvss=4.3, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8621", cve="CVE-2020-8621", cvss=4.3, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8624", cve="CVE-2020-8624", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8622", cve="CVE-2020-8622", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8619", cve="CVE-2020-8619", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8618", cve="CVE-2020-8618", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP)
                      ]
                      ),
                 Node(ip="172.18.7.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                      reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                         "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                             "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      flags=[Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)], level=3,
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="john", pw="doe"),
                          Credential(username="vagrant", pw="test_pw1")
                      ],
                      root_usernames=["admin", "john"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet",
                                         credentials=[
                                             Credential(username="admin", pw="admin",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet"),
                                             Credential(username="john", pw="doe",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet"),
                                             Credential(username="vagrant", pw="test_pw1",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[])
                      ], vulnerabilities=[
                         Vulnerability(name="CVE-2020-15523", cve="CVE-2020-15523", cvss=6.9, credentials=[], port=80,
                                       protocol=TransportProtocol.TCP),
                         Vulnerability(name="CVE-2020-14422", cve="CVE-2020-14422", cvss=4.3, credentials=[], port=80,
                                       protocol=TransportProtocol.TCP),
                         Vulnerability(name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
                                       cve=None, cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                             Credential(username="admin", pw="admin", service=constants.TELNET.SERVICE_NAME)
                         ],
                                       port=23, protocol=TransportProtocol.TCP, service=constants.TELNET.SERVICE_NAME)
                     ]
                      ),
                 Node(ip="172.18.7.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="test", pw="qwerty"),
                          Credential(username="oracle", pw="abc123")
                      ],
                      root_usernames=["admin", "test"],
                      reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                             "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19",
                                             "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75",
                                             "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=25, name="smtp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=2181, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=5432, name="postgresql", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=6667, name="irc", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9092, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=38969, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=42843, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[]),
                 Node(ip="172.18.7.79", ip_id=79, id=5, type=NodeType.SERVER,
                      reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                         "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                             "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      flags=[Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)], level=3,
                      os="linux",
                      credentials=[
                          Credential(username="l_hopital", pw="l_hopital"),
                          Credential(username="euler", pw="euler"),
                          Credential(username="pi", pw="pi")
                      ],
                      root_usernames=["l_hopital", "pi"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp",
                                         credentials=[
                                             Credential(username="l_hopital", pw="l_hopital",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp"),
                                             Credential(username="euler", pw="euler",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp"),
                                             Credential(username="pi", pw="pi",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=79, name="finger", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=8009, name="ajp13", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=8080, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=10011, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=10022, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=30033, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=27017, name="mongod", credentials=[]),
                      ],
                      vulnerabilities=[
                          Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                                        port=22,
                                        protocol=TransportProtocol.TCP),
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                              Credential(username="pi", pw="pi", service=constants.FTP.SERVICE_NAME)
                          ],
                                        port=21, protocol=TransportProtocol.TCP, service=constants.FTP.SERVICE_NAME)
                      ]
                      ),
                 Node(ip="172.18.7.19", ip_id=19, id=6, type=NodeType.SERVER,
                      flags=[Flag(name="flag4", path="/tmp", id=4, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="karl", pw="gustaf"),
                          Credential(username="steven", pw="carragher")
                      ],
                      root_usernames=["karl"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                           "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=139, name="netbios-ssn", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=445, name="microsoft-ds", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SAMBACRY_EXPLOIT,
                                        cve=constants.EXPLOIT_VULNERABILITES.SAMBACRY_EXPLOIT, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.SAMBA.USER, pw=constants.SAMBA.PW,
                                                       service=constants.SAMBA.SERVICE_NAME)
                                        ],
                                        port=constants.SAMBA.PORT,
                                        protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.31", ip_id=31, id=7, type=NodeType.SERVER,
                      flags=[Flag(name="flag5", path="/tmp", id=5, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="stefan", pw="zweig")
                      ],
                      root_usernames=["stefan"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                           "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SHELLSHOCK_EXPLOIT,
                                        cve=constants.EXPLOIT_VULNERABILITES.SHELLSHOCK_EXPLOIT, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.SHELLSHOCK.BACKDOOR_USER,
                                                       pw=constants.SHELLSHOCK.BACKDOOR_PW,
                                                       service=constants.SHELLSHOCK.SERVICE_NAME)
                                        ],
                                        port=constants.SHELLSHOCK.PORT,
                                        protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.42", ip_id=42, id=8, type=NodeType.SERVER,
                      flags=[Flag(name="flag6", path="/tmp", id=6, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="roy", pw="neruda"),
                          Credential(username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7")
                      ],
                      root_usernames=["pablo"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                           "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION,
                                        cve=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION, cvss=9.5,
                                        credentials=[
                                            Credential(username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7",
                                                       service="http")
                                        ],
                                        port=80, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.37", ip_id=37, id=9, type=NodeType.SERVER,
                      flags=[Flag(name="flag7", path="/tmp", id=7, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="john", pw="conway"),
                      ],
                      root_usernames=["john"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                           "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.CVE_2015_3306.BACKDOOR_USER,
                                                       pw=constants.CVE_2015_3306.BACKDOOR_PW,
                                                       service=constants.CVE_2015_3306.SERVICE_NAME)
                                        ],
                                        port=21, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.82", ip_id=82, id=10, type=NodeType.SERVER,
                      flags=[Flag(name="flag8", path="/tmp", id=8, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="john", pw="nash"),
                      ],
                      root_usernames=["john"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                           "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=9300, name="vrace", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9200, name="wap-wsp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.CVE_2015_3306.BACKDOOR_USER,
                                                       pw=constants.CVE_2015_3306.BACKDOOR_PW,
                                                       service=constants.CVE_2015_3306.SERVICE_NAME)
                                        ],
                                        port=21, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.75", ip_id=75, id=11, type=NodeType.SERVER,
                      flags=[Flag(name="flag9", path="/tmp", id=9, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="larry", pw="samuelson"),
                      ],
                      root_usernames=["larry"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75",
                                           "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http"),
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2016_10033,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2016_10033, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.CVE_2016_10033.BACKDOOR_USER,
                                                       pw=constants.CVE_2016_10033.BACKDOOR_PW,
                                                       service=constants.CVE_2016_10033.SERVICE_NAME)
                                        ],
                                        port=constants.CVE_2016_10033.PORT, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.71", ip_id=71, id=11, type=NodeType.SERVER,
                      flags=[Flag(name="flag10", path="/root", id=10, requires_root=True, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="robbins", pw="monro"),
                      ],
                      root_usernames=["robbins"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75",
                                           "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http"),
                          NetworkService(protocol=TransportProtocol.TCP, port=10011, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=10022, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=30033, name="teamspeak", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        service=constants.SSH.SERVICE_NAME,
                                        credentials=[
                                            Credential(username="alan", pw="alan",
                                                       protocol=TransportProtocol.TCP,
                                                       service=constants.SSH.SERVICE_NAME)
                                        ],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2010_0426,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2010_0426, cvss=6,
                                        credentials=[
                                            Credential(username="alan", pw="alan", service=None)
                                        ], port=None, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.11", ip_id=11, id=12, type=NodeType.SERVER,
                      flags=[Flag(name="flag11", path="/root", id=11, requires_root=True, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="rich", pw="sutton"),
                      ],
                      root_usernames=["rich"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75",
                                           "172.18.7.71", "172.18.7.11"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http"),
                          NetworkService(protocol=TransportProtocol.TCP, port=9042, name="cassandra", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9160, name="cassandra", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        service=constants.SSH.SERVICE_NAME,
                                        credentials=[
                                            Credential(username="donald", pw="donald",
                                                       protocol=TransportProtocol.TCP,
                                                       service=constants.SSH.SERVICE_NAME)
                                        ],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2015_5602,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2015_5602, cvss=6,
                                        credentials=[
                                            Credential(username="donald", pw="donald", service=None)
                                        ], port=None, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.191", ip_id=191, id=13, type=NodeType.HACKER, flags=[], level=1, services=[],
                      os="linux", vulnerabilities=[],
                      reachable_nodes =set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                            "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                            "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                      credentials=[
                          Credential(username="agent", pw="agent")
                      ],
                      root_usernames=["agent"])]
        return nodes

    @staticmethod
    def adj_matrix() -> List:
        """
        Returns the adjacency matrix that defines the topology

        :return: adjacency matrix
        """
        adj_matrix = [
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        return adj_matrix

    @staticmethod
    def subnet_mask() -> str:
        """
        :return: the subnet mask
        """
        subnet_mask = "172.18.7.0/24"
        return subnet_mask

    @staticmethod
    def num_nodes() -> int:
        """
        :return: num nodes
        """
        return 13

    @staticmethod
    def hacker_ip() -> str:
        """
        :return: the agent's ip
        """
        hacker_ip = "172.18.7.191"
        return hacker_ip

    @staticmethod
    def router_ip() -> str:
        """
        :return: the agent's default gw
        """
        router_ip = "172.18.7.10"
        return router_ip

    @staticmethod
    def flags_lookup() -> str:
        """
        :return: dict with the flags
        """
        flags_lookup = {}
        flags_lookup[("172.18.7.2", "/tmp/flag2")] = Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)
        flags_lookup[("172.18.7.3", "/root/flag1")] = Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)
        flags_lookup[("172.18.7.79", "/tmp/flag3")] = Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)
        flags_lookup[("172.18.7.19", "/tmp/flag4")] = Flag(name="flag4", path="/tmp", id=4, requires_root=False, score=1)
        flags_lookup[("172.18.7.31", "/tmp/flag5")] = Flag(name="flag5", path="/tmp", id=5, requires_root=False, score=1)
        flags_lookup[("172.18.7.42", "/tmp/flag6")] = Flag(name="flag6", path="/tmp", id=6, requires_root=False, score=1)
        flags_lookup[("172.18.7.37", "/tmp/flag7")] = Flag(name="flag7", path="/tmp", id=7, requires_root=False, score=1)
        flags_lookup[("172.18.7.82", "/tmp/flag8")] = Flag(name="flag8", path="/tmp", id=8, requires_root=False, score=1)
        flags_lookup[("172.18.7.75", "/tmp/flag9")] = Flag(name="flag9", path="/tmp", id=9, requires_root=False, score=1)
        flags_lookup[("172.18.7.71", "/root/flag10")] = Flag(name="flag10", path="/root", id=10, requires_root=True, score=1)
        flags_lookup[("172.18.7.11", "/root/flag11")] = Flag(name="flag11", path="/root", id=11, requires_root=True, score=1)
        return flags_lookup

    @staticmethod
    def network_conf(generate: bool = False) -> NetworkConfig:
        """
        :return: The network configuration
        """
        nodes = []
        adj_matrix = []
        reachable = set()
        if not generate:
            nodes = PyCrCTFLevel7Base.nodes()
            adj_matrix = PyCrCTFLevel7Base.adj_matrix()
            reachable = PyCrCTFLevel7Base.agent_reachable()
        network_conf = NetworkConfig(subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                     nodes=nodes,
                                     adj_matrix=adj_matrix,
                                     flags_lookup = PyCrCTFLevel7Base.flags_lookup(),
                                     agent_reachable=reachable,
                                     vulnerable_nodes = set(["172.18.7.3", "172.18.7.79", "172.18.7.2", "172.18.7.19",
                                                             "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                                             "172.18.7.82", "172.18.7.75"]))
        return network_conf

    @staticmethod
    def agent_reachable() -> set():
        reachable = set(["172.18.7.10", "172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79","172.18.7.19",
                         "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75"])
        return reachable

    @staticmethod
    def emulation_config() -> EmulationConfig:
        """
        :return: the default emulation config
        """
        emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.7.191",
                                         agent_username="agent", agent_pw="agent", server_connection=True,
                                         server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                         server_username="kim")
        return emulation_config

    @staticmethod
    def attacker_all_actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        attack_actions = []

        # Host actions
        for idx in range(num_nodes):
            attack_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.PING_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            attack_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip = hacker_ip))
            attack_actions.append(AttackerNMAPActions.FIREWALK(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.HTTP_ENUM(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.HTTP_GREP(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.VULSCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.FINGER(index=idx, subnet=False))
            attack_actions.append(AttackerShellActions.SAMBACRY_EXPLOIT(index=idx))
            attack_actions.append(AttackerShellActions.SHELLSHOCK_EXPLOIT(index=idx))
            attack_actions.append(AttackerShellActions.DVWA_SQL_INJECTION(index=idx))
            attack_actions.append(AttackerShellActions.CVE_2015_3306_EXPLOIT(index=idx))
            attack_actions.append(AttackerShellActions.CVE_2015_1427_EXPLOIT(index=idx))
            attack_actions.append(AttackerShellActions.CVE_2016_10033_EXPLOIT(index=idx))
            attack_actions.append(AttackerShellActions.CVE_2010_0426_PRIV_ESC(index=idx))
            attack_actions.append(AttackerShellActions.CVE_2015_5602_PRIV_ESC(index=idx))

        # Subnet Nmap actions
        attack_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.PING_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.FIREWALK(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.HTTP_ENUM(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.HTTP_GREP(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.VULSCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.FINGER(num_nodes + 1, ip=subnet_mask, subnet=True))

        # Nmap actions ALL
        attack_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.PING_SCAN(index=-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.NMAP_VULNERS(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.FIREWALK(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.HTTP_ENUM(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.HTTP_GREP(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.VULSCAN(-1, ip=subnet_mask, subnet=False))
        attack_actions.append(AttackerNMAPActions.FINGER(-1, ip=subnet_mask, subnet=False))

        # Masscan subnet
        attack_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=num_nodes + 1, subnet=True,
                                                                host_ip=hacker_ip, ip=subnet_mask))

        # Shell actions All
        attack_actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        attack_actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))

        attack_actions = sorted(attack_actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST, AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET, AttackerActionId.TCP_SYN_STEALTH_SCAN_ALL,
            AttackerActionId.PING_SCAN_HOST, AttackerActionId.PING_SCAN_SUBNET, AttackerActionId.PING_SCAN_ALL,
            AttackerActionId.UDP_PORT_SCAN_HOST, AttackerActionId.UDP_PORT_SCAN_SUBNET, AttackerActionId.UDP_PORT_SCAN_ALL,
            AttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST, AttackerActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET, AttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL,
            AttackerActionId.TCP_FIN_SCAN_HOST, AttackerActionId.TCP_FIN_SCAN_SUBNET, AttackerActionId.TCP_FIN_SCAN_ALL,
            AttackerActionId.TCP_NULL_SCAN_HOST, AttackerActionId.TCP_NULL_SCAN_SUBNET, AttackerActionId.TCP_NULL_SCAN_ALL,
            AttackerActionId.TCP_XMAS_TREE_SCAN_HOST, AttackerActionId.TCP_XMAS_TREE_SCAN_SUBNET, AttackerActionId.TCP_XMAS_TREE_SCAN_ALL,
            AttackerActionId.OS_DETECTION_SCAN_HOST, AttackerActionId.OS_DETECTION_SCAN_SUBNET, AttackerActionId.OS_DETECTION_SCAN_ALL,
            AttackerActionId.NMAP_VULNERS_HOST, AttackerActionId.NMAP_VULNERS_SUBNET, AttackerActionId.NMAP_VULNERS_ALL,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET, AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL,
            AttackerActionId.FIREWALK_HOST, AttackerActionId.FIREWALK_SUBNET, AttackerActionId.FIREWALK_ALL,
            AttackerActionId.HTTP_ENUM_HOST, AttackerActionId.HTTP_ENUM_SUBNET, AttackerActionId.HTTP_ENUM_ALL,
            AttackerActionId.HTTP_GREP_HOST, AttackerActionId.HTTP_GREP_SUBNET, AttackerActionId.HTTP_GREP_ALL,
            AttackerActionId.VULSCAN_HOST, AttackerActionId.VULSCAN_SUBNET, AttackerActionId.VULSCAN_ALL,
            AttackerActionId.FINGER_HOST, AttackerActionId.FINGER_SUBNET, AttackerActionId.FINGER_ALL
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG, AttackerActionId.SAMBACRY_EXPLOIT, AttackerActionId.SHELLSHOCK_EXPLOIT,
                            AttackerActionId.DVWA_SQL_INJECTION, AttackerActionId.CVE_2015_3306_EXPLOIT, AttackerActionId.CVE_2015_1427_EXPLOIT,
                            AttackerActionId.CVE_2016_10033_EXPLOIT, AttackerActionId.CVE_2010_0426_PRIV_ESC,
                            AttackerActionId.CVE_2015_5602_PRIV_ESC]
        nikto_action_ids = [AttackerActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [AttackerActionId.MASSCAN_HOST_SCAN, AttackerActionId.MASSCAN_SUBNET_SCAN]
        attacker_action_config = AttackerActionConfig(num_indices=num_nodes + 1, actions=attack_actions, nmap_action_ids=nmap_action_ids,
                                             network_service_action_ids=network_service_action_ids,
                                             shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                             masscan_action_ids=masscan_action_ids)
        return attacker_action_config

    @staticmethod
    def defender_all_actions_conf(num_nodes: int, subnet_mask: str) -> DefenderActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :return: the action config
        """
        defender_actions = []

        # Host actions
        for idx in range(num_nodes):
            # actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            pass

        # Subnet actions
        defender_actions.append(DefenderStoppingActions.STOP(index=num_nodes + 1))
        defender_actions.append(DefenderStoppingActions.CONTINUE(index=num_nodes + 1))

        defender_actions = sorted(defender_actions, key=lambda x: (x.id.value, x.index))
        stopping_action_ids = [
            DefenderActionId.STOP, DefenderActionId.CONTINUE
        ]
        defender_action_config = DefenderActionConfig(
            num_indices=num_nodes + 1, actions=defender_actions, stopping_action_ids=stopping_action_ids)
        return defender_action_config

    @staticmethod
    def render_conf() -> RenderConfig:
        """
        :return: the render config
        """
        render_config = RenderConfig(num_levels = 3, num_nodes_per_level = 12, render_adj_matrix=True)
        return render_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, attacker_action_conf: AttackerActionConfig,
                   defender_action_conf: DefenderActionConfig,
                   emulation_config: EmulationConfig,
                   render_conf: RenderConfig) -> EnvConfig:
        """
        :param network_conf: the network config
        :param attacker_action_conf: the attacker's action config
        :param defender_action_conf: the defender's action config
        :param emulation_config: the emulation config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = EnvConfig(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                               attacker_num_ports_obs=10, attacker_num_vuln_obs=10,
                               num_nodes = PyCrCTFLevel7Base.num_nodes(), attacker_num_sh_obs=3,
                               render_config=render_conf, env_mode=EnvMode.SIMULATION,
                               emulation_config=emulation_config,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=PyCrCTFLevel7Base.hacker_ip(), state_type=StateType.BASE,
                               router_ip=PyCrCTFLevel7Base.router_ip())
        env_config.ping_scan_miss_p = 0.0
        env_config.udp_port_scan_miss_p = 0.0
        env_config.syn_stealth_scan_miss_p = 0.0
        env_config.os_scan_miss_p = 0.0
        env_config.vulners_miss_p = 0.0
        env_config.num_flags = 11
        env_config.blacklist_ips = ["172.18.7.1", "172.18.7.254"]
        env_config.ids_router = True
        return env_config