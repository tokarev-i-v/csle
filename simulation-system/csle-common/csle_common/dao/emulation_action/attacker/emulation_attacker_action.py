from typing import List, Tuple
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome


class EmulationAttackerAction:
    """
    Class representing an action of the attacker in the emulation
    """
    def __init__(self, id : EmulationAttackerActionId, name :str, cmds : List[str],
                 type: EmulationAttackerActionType, descr: str,
                 ips :List[str], index: int, subnet : bool = False,
                 action_outcome: EmulationAttackerActionOutcome = EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                 vulnerability: str = None, alt_cmds : List[str] = None, backdoor: bool = False):
        """
        Class constructor

        :param id: id of the action
        :param name: name of the action
        :param cmds: command-line commands to apply the action on the emulation
        :param type: type of the action
        :param descr: description of the action (documentation)
        :param ips: ips of the machines to apply the action to
        :param index: index of the machien to apply the action to
        :param subnet: if True, apply action to entire subnet
        :param action_outcome: type of the outcome of the action
        :param vulnerability: type of vulnerability that the action exploits (in case an exploit)
        :param alt_cmds: alternative command if the first command does not work
        :param backdoor: if the action also installs a backdoor (some exploits does this)
        """
        self.type = type
        self.id = id
        self.name = name
        self.cmds = cmds
        self.descr = descr
        self.index = index
        self.subnet = subnet
        self.ips = ips
        self.vulnerability = vulnerability
        self.action_outcome = action_outcome
        self.backdoor = backdoor
        self.alt_cmds = alt_cmds
        self.index = index
        self.backdoor = backdoor

    def nmap_cmds(self, machine_ips: List[str] = None) -> Tuple[List[str], List[str]]:
        """
        Augments the original command of the action with extra flags for NMAP

        :param machine_ips: list of ips
        :return: the new command
        """
        commands = []
        file_names = []
        for ip in self.ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip.replace("/", "_")
            file_name = file_name + ".xml "
            commands.append(self.cmds[0] + constants.NMAP.FILE_ARGS + " " + file_name + ip)
            file_names.append(file_name)
        if machine_ips is None:
            machine_ips = []
        for ip in machine_ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip.replace("/", "_")
            file_name = file_name + ".xml "
            commands.append(self.cmds[0] + constants.NMAP.FILE_ARGS + " " + file_name + ip)
            file_names.append(file_name)
        return commands, file_names

    def nikto_cmds(self) -> Tuple[List[str], List[str]]:
        """
        Augments the original command of the action with extra flags for Nikto

        :return: the new command
        """
        file_names = []
        commands = []
        for ip in self.ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip + ".xml "
            commands.append(self.cmds[0] + constants.NIKTO.HOST_ARG + ip + " " + constants.NIKTO.OUTPUT_ARG + file_name)
            file_names.append(file_name)
        return commands, file_names

    def masscan_cmds(self) -> Tuple[List[str], List[str]]:
        """
        Augments the original command of the action with extra flags for massscan

        :return: the new command
        """
        commands = []
        file_names = []
        for ip in self.ips:
            file_name = str(self.id.value) + "_" + str(self.index) + "_" + ip + ".xml "
            if self.subnet:
                file_name = str(self.id.value) + "_" + str(self.index) + ".xml "
            commands.append(self.cmds[0] + constants.MASSCAN.OUTPUT_ARG + " " + file_name + ip)
            file_names.append(file_name)
        return commands, file_names

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return "id:{},name:{},ips:{},subnet:{},index:{}".format(self.id, self.name, self.ips, self.subnet, self.index)

    @staticmethod
    def from_dict(d: dict) -> "EmulationAttackerAction":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationAttackerAction(
            type = d["type"], id=d["id"], name=d["name"], cmds=d["cmds"], descr=d["descr"], index=d["index"],
            subnet=d["subnet"], ips=d["ips"], vulnerability=d["vulnerability"], action_outcome=d["action_outcome"],
            backdoor=d["backdoor"], alt_cmds=d["alt_cmds"]
        )
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["cmds"] = self.cmds
        d["type"] = self.type
        d["descr"] = self.descr
        d["ips"] = self.ips
        d["index"] = self.index
        d["subnet"] = self.subnet
        d["action_outcome"] = self.action_outcome
        d["vulnerability"] = self.vulnerability
        d["alt_cmds"] = self.alt_cmds
        d["backdoor"] = self.backdoor
        return d

    def ips_match(self, ips: List[str]) -> bool:
        """
        Checks if a list of ips overlap with the ips of this host

        :param ips: the list of ips to check
        :return:  True if they match, False otherwise
        """
        for ip in self.ips:
            if ip in ips:
                return True
        return False

