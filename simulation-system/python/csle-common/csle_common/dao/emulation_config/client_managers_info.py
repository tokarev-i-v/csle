from typing import List, Dict, Any
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.client_manager_util as client_manager_util


class ClientManagersInfo:
    """
    DTO containing the status of the Client managers for a given emulation execution
    """

    def __init__(self, running: bool, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 client_managers_statuses: List[csle_collector.client_manager.client_manager_pb2.ClientsDTO]):
        """
        Initializes the DTO

        :param running: boolean that indicates whether the at least one Client manager is running or not
        :param ips: the list of IPs of the running Client managers
        :param ports: the list of ports of the running Client managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param client_managers_statuses: a list of statuses of the Client managers
        """
        self.running = running
        self.ips = ips
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.client_managers_statuses = client_managers_statuses
        self.ports = ports

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"running: {self.running}, ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"client_managers_statuses: {list(map(lambda x: str(x), self.client_managers_statuses))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["running"] = self.running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["client_managers_statuses"] = list(map(
            lambda x: client_manager_util.ClientManagerUtil.client_dto_to_dict(x),
            self.client_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ClientManagersInfo(running=d["running"], ips=d["ips"], ports=d["ports"],
                                 emulation_name=d["emulation_name"],
                                 execution_id=d["execution_id"], client_managers_statuses=list(map(
                lambda x: client_manager_util.ClientManagerUtil.clients_dto_from_dict(x),
                d["client_managers_statuses"])))
        return dto