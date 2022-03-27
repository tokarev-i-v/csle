import csle_common.constants.constants as constants
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerNIKTOActions:
    """
    Class implementing NIKTO scan actions for the attacker
    """

    @staticmethod
    def NIKTO_WEB_HOST_SCAN(index: int, ip: str = "") -> AttackerAction:
        """
        Action for running a nikto web scan on a given host

        :param index: index of the machine to apply the action to
        :param ip: ip of the machine to apply the action to
        :return: the action
        """
        cost_noise_multiplier = 1
        id = AttackerActionId.NIKTO_WEB_HOST_SCAN
        file_name = str(id.value) + "_" + ip + ".xml "
        cmd = ["no | sudo nikto " + constants.NIKTO.BASE_ARGS]
        return AttackerAction(id=id, name="Nikto Web Scan", cmd=cmd,
                              type=AttackerActionType.RECON,
                              descr="Nikto Web Scan",
                              cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                              ips=ip, subnet=False, index=index,
                              action_outcome=AttackerActionOutcome.INFORMATION_GATHERING)
