from typing import List, Dict, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.credential import Credential
from csle_base.json_serializable import JSONSerializable


class NetworkService(JSONSerializable):
    """
    DTO Class representing a service in the network
    """

    def __init__(self, protocol: TransportProtocol, port: int, name: str, credentials: List[Credential] = None):
        """
        Initializes the DTO

        :param protocol: the protocol of the service
        :param port: the port of the service
        :param name: the name of the service
        :param credentials: the list of credentials of the service
        """
        self.protocol = protocol
        self.port = port
        self.name = name
        self.credentials = credentials

    def __str__(self) -> str:
        """
        :return: a string representation of the service
        """
        cr = []
        if self.credentials is not None:
            cr = list(map(lambda x: str(x), self.credentials))
        return "protocol:{}, port:{}, name:{}, credentials: {}".format(self.protocol, self.port, self.name,
                                                                       cr)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["protocol"] = self.protocol
        d["port"] = self.port
        d["name"] = self.name
        d["credentials"] = list(map(lambda x: x.to_dict(), self.credentials))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NetworkService":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = NetworkService(name=d["name"], port=d["port"], protocol=d["protocol"],
                             credentials=list(map(lambda x: Credential.from_dict(x), d["credentials"])))
        return dto

    def copy(self) -> "NetworkService":
        """
        :return: a copy of the DTO
        """
        return NetworkService(
            protocol=self.protocol, port=self.port, name=self.name, credentials=self.credentials
        )

    @staticmethod
    def pw_vuln_services():
        """
        :return: a list of all vulnerabilities that involve weak passwords
        """
        ssh_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh", credentials=[]),
                            constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS)
        ftp_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp", credentials=[]),
                            constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS)
        telnet_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet", credentials=[]),
                               constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS)
        return [ssh_vuln_service, ftp_vuln_service, telnet_vuln_service], [ssh_vuln_service, telnet_vuln_service]

    def __eq__(self, other) -> bool:
        """
        Tests equality with another service

        :param other: the service to compare with
        :return: True if equal otherwise False
        """
        if not isinstance(other, NetworkService):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name and self.protocol == other.protocol and self.port == other.port

    @staticmethod
    def from_credential(credential: Credential) -> "NetworkService":
        """
        Converts the object into a network service representation

        :return: the network service representation
        """
        service = NetworkService(protocol=credential.protocol, port=credential.port,
                                 name=credential.service,
                                 credentials=[credential])
        return service

    @staticmethod
    def from_json_file(json_file_path: str) -> "NetworkService":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NetworkService.from_dict(json.loads(json_str))
