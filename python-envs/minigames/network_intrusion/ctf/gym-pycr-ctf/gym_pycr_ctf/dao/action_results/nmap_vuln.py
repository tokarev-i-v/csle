from typing import List
from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol
from gym_pycr_ctf.dao.observation.common.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_ctf.dao.network.credential import Credential


class NmapVuln:
    """
    DTO representing a vulnerability found with NMAP
    """

    def __init__(self, name : str, port: int, protocol: TransportProtocol, cvss: float, service: str,
                 credentials : List[Credential] = None):
        """
        Initializes the DTO

        :param name: the name of the vulnerability
        :param port: the port of the vulnerability
        :param protocol: the protocol of the vulnerability
        :param cvss: the cvss of the vulnerability
        :param service: the service of the vulnerability
        :param credentials: the credentials of the vulnerability
        """
        self.name = name
        self.port = port
        self.protocol = protocol
        self.cvss = cvss
        self.service = service
        self.credentials = credentials

    def to_obs(self) -> VulnerabilityObservationState:
        """
        Converts the object into a VulnerabilityObservationState

        :return: the created VulnerabilityObservationState
        """
        vuln = VulnerabilityObservationState(name=self.name, port=self.port, protocol=self.protocol, cvss=self.cvss,
                                             credentials=self.credentials)
        return vuln

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.name) + 31 * hash(self.port)

    def __eq__(self, other):
        """
        Compares equality of the object with another object

        :param other: the object to compare with
        :return: True if equal otherwise False
        """
        return (self.name == other.name and
                self.port == other.port)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "name:{}, port:{}, protocol:{}, cvss:{}, service:{}, credentials:{}".format(
            self.name, self.port, self.protocol, self.cvss, self.service,
            list(map(lambda x: str(x), self.credentials)))