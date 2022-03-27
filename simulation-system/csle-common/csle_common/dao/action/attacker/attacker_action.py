from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action_outcome import AttackerActionOutcome


class AttackerAction:
    """
    Class representing an action of the attacker in the environment
    """
    def __init__(self, id : AttackerActionId, name :str, cmd : List[str], type: AttackerActionType, descr: str, cost: float,
                 noise : float, ips :List[str], index: int, subnet : bool = False,
                 action_outcome: AttackerActionOutcome = AttackerActionOutcome.INFORMATION_GATHERING,
                 vulnerability: str = None, alt_cmd = List[str], alerts = None, backdoor: bool = False):
        """
        Class constructor

        :param id: id of the action
        :param name: name of the action
        :param cmd: command-line commands to apply the action on the emulation
        :param type: type of the action
        :param descr: description of the action (documentation)
        :param cost: cost of the action
        :param noise: noise-level of the action
        :param ips: ips of the machines to apply the action to
        :param index: index of the machien to apply the action to
        :param subnet: if True, apply action to entire subnet
        :param action_outcome: type of the outcome of the action
        :param vulnerability: type of vulnerability that the action exploits (in case an exploit)
        :param alt_cmd: alternative command if the first command does not work
        :param alerts: the number of IDS alerts triggered by this action
        :param backdoor: if the action also installs a backdoor (some exploits does this)
        """
        self.type = type
        self.id = id
        self.name = name
        self.cmd = cmd
        self.descr = descr
        self.index = index
        self.subnet = subnet
        self.ips = ips
        self.vulnerability = vulnerability
        self.noise = noise
        self.alerts = alerts
        if self.alerts is None:
            self.alerts = (0,0)
        self.action_outcome = action_outcome
        self.backdoor = backdoor
        self.cost = cost
        self.alt_cmd = alt_cmd
        self.index = index
        self.backdoor = backdoor

    def nmap_cmd(self, machine_ip : str = None) -> List[str]:
        """
        Augments the original command of the action with extra flags for NMAP

        :param machine_ip: ip of the machine
        :return: the new command
        """
        commands = []
        for ip in self.ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip
            if self.subnet:
                file_name = str(self.id.value) + "_" + str(self.index)
            if machine_ip is not None:
                file_name = file_name + "_" + machine_ip
            file_name = file_name + ".xml "
            commands.append(self.cmd[0] + constants.NMAP.FILE_ARGS + " " + file_name + ip)
        return commands

    def nikto_cmd(self):
        """
        Augments the original command of the action with extra flags for Nikto

        :return: the new command
        """
        commands = []
        for ip in self.ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip + ".xml "
            commands.append(self.cmd[0] + constants.NIKTO.HOST_ARG + ip + " " + constants.NIKTO.OUTPUT_ARG + file_name)
        return commands

    def masscan_cmd(self):
        """
        Augments the original command of the action with extra flags for massscan

        :return: the new command
        """
        commands = []
        for ip in self.ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip + ".xml "
            if self.subnet:
                file_name = str(self.id.value) + "_" + str(self.index) + ".xml "
            commands.append(self.cmd[0] + constants.MASSCAN.OUTPUT_ARG + " " + file_name + ip)
        return commands


    def __str__(self):
        """
        :return: a string representation of the object
        """
        return "id:{},name:{},ips:{},subnet:{},index:{}".format(self.id, self.name, self.ips, self.subnet, self.index)
