from typing import List
import numpy as np
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction


class DefenderObservationState:
    """
    Represents the defender's agent's current belief state of the environment
    """

    def __init__(self, num_machines : int, ids = False):
        """
        Initializes the DTO

        :param num_machines: the numer of machines
        :param ids: whether there is an IDS or not
        """
        self.num_machines = num_machines
        self.ids = ids
        self.machines : List[DefenderMachineObservationState] = []
        self.defense_actions_tried = set()
        self.num_alerts_recent = 0
        self.num_severe_alerts_recent = 0
        self.num_warning_alerts_recent = 0
        self.sum_priority_alerts_recent = 0
        self.num_alerts_total = 0
        self.sum_priority_alerts_total = 0
        self.num_severe_alerts_total = 0
        self.num_warning_alerts_total = 0
        self.caught_attacker = False
        self.stopped = False
        self.adj_matrix = np.array(0)
        self.last_alert_ts = None
        self.step = 1
        self.snort_warning_baseline_reward = 0
        self.snort_severe_baseline_reward = 0
        self.snort_critical_baseline_reward = 0
        self.var_log_baseline_reward = 0
        self.step_baseline_reward = 0
        self.snort_warning_baseline_step = 1
        self.snort_severe_baseline_step = 1
        self.snort_critical_baseline_step = 1
        self.var_log_baseline_step = 1
        self.step_baseline_step = 1

        self.snort_severe_baseline_stopped = False
        self.snort_warning_baseline_stopped = False
        self.snort_critical_baseline_stopped = False
        self.var_log_baseline_stopped = False
        self.step_baseline_stopped = False

        self.snort_severe_baseline_caught_attacker = False
        self.snort_warning_baseline_caught_attacker = False
        self.snort_critical_baseline_caught_attacker = False
        self.var_log_baseline_caught_attacker = False
        self.step_baseline_caught_attacker = False

        self.snort_severe_baseline_early_stopping = False
        self.snort_warning_baseline_early_stopping = False
        self.snort_critical_baseline_early_stopping = False
        self.var_log_baseline_early_stopping = False
        self.step_baseline_early_stopping = False

        self.snort_severe_baseline_uncaught_intrusion_steps = 0
        self.snort_warning_baseline_uncaught_intrusion_steps = 0
        self.snort_critical_baseline_uncaught_intrusion_steps = 0
        self.var_log_baseline_uncaught_intrusion_steps = 0
        self.step_baseline_uncaught_intrusion_steps = 0

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ip(self, a : DefenderAction) -> str:
        """
        Gets the ip of the node that a defender action is targeted for

        :param a: the action
        :return: the ip of the target node
        """
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.ip, self.machines))
            ips_str = "_".join(ips)
            return ips_str
        if a.index < len(self.machines) and a.index < self.num_machines:
            return self.machines[a.index].ip
        return a.ip

    def copy(self) -> "DefenderObservationState":
        """
        :return: a copy of the object
        """
        c = DefenderObservationState(num_machines = self.num_machines, ids=self.ids)
        c.caught_attacker = self.caught_attacker
        c.stopped = self.stopped
        c.defense_actions_tried = self.defense_actions_tried.copy()
        c.num_alerts_recent = self.num_alerts_recent
        c.num_severe_alerts_recent = self.num_severe_alerts_recent
        c.num_warning_alerts_recent = self.num_warning_alerts_recent
        c.sum_priority_alerts_recent = self.sum_priority_alerts_recent
        c.num_alerts_total = self.num_alerts_total
        c.num_severe_alerts_total = self.num_severe_alerts_total
        c.num_warning_alerts_total = self.num_warning_alerts_total
        c.sum_priority_alerts_total = self.sum_priority_alerts_total
        c.adj_matrix = self.adj_matrix
        c.snort_warning_baseline_reward = self.snort_warning_baseline_reward
        c.snort_severe_baseline_reward = self.snort_severe_baseline_reward
        c.snort_warning_baseline_stopped = self.snort_warning_baseline_stopped
        c.snort_warning_baseline_step = self.snort_warning_baseline_step
        c.snort_severe_baseline_stopped = self.snort_severe_baseline_stopped
        c.snort_severe_baseline_step = self.snort_severe_baseline_step
        c.snort_critical_baseline_reward = self.snort_critical_baseline_reward
        c.snort_critical_baseline_stopped = self.snort_critical_baseline_stopped
        c.snort_critical_baseline_step = self.snort_critical_baseline_step
        c.var_log_baseline_reward = self.var_log_baseline_reward
        c.var_log_baseline_stopped = self.var_log_baseline_stopped
        c.var_log_baseline_step = self.var_log_baseline_step

        c.step_baseline_stopped = self.step_baseline_stopped
        c.step_baseline_reward = self.step_baseline_reward
        c.step_baseline_step = self.step_baseline_step
        c.last_alert_ts = self.last_alert_ts
        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def update_info_dict(self, info: dict) -> dict:
        """
        Update the info dict with information from the defender's observation state

        :param info: the info dict
        :return: the updated dict
        """
        info[constants.INFO_DICT.CAUGHT_ATTACKER] = self.caught_attacker
        info[constants.INFO_DICT.EARLY_STOPPED] = self.stopped
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_REWARD] = self.snort_severe_baseline_reward
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_REWARD] = self.snort_warning_baseline_reward
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_REWARD] = self.snort_critical_baseline_reward
        info[constants.INFO_DICT.VAR_LOG_BASELINE_REWARD] = self.var_log_baseline_reward
        info[constants.INFO_DICT.STEP_BASELINE_REWARD] = self.step_baseline_reward
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_STEP] = self.snort_severe_baseline_step
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_STEP] = self.snort_warning_baseline_step
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STEP] = self.snort_critical_baseline_step
        info[constants.INFO_DICT.VAR_LOG_BASELINE_STEP] = self.var_log_baseline_step
        info[constants.INFO_DICT.STEP_BASELINE_STEP] = self.step_baseline_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER] = self.snort_severe_baseline_caught_attacker
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_CAUGHT_ATTACKER] = self.snort_warning_baseline_caught_attacker
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER] = self.snort_critical_baseline_caught_attacker
        info[constants.INFO_DICT.VAR_LOG_BASELINE_CAUGHT_ATTACKER] = self.var_log_baseline_caught_attacker
        info[constants.INFO_DICT.STEP_BASELINE_CAUGHT_ATTACKER] = self.step_baseline_caught_attacker
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_EARLY_STOPPING] = self.snort_severe_baseline_early_stopping
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_EARLY_STOPPING] = self.snort_warning_baseline_early_stopping
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_EARLY_STOPPING] = self.snort_critical_baseline_early_stopping
        info[constants.INFO_DICT.VAR_LOG_BASELINE_EARLY_STOPPING] = self.var_log_baseline_early_stopping
        info[constants.INFO_DICT.STEP_BASELINE_EARLY_STOPPING] = self.step_baseline_early_stopping
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.snort_severe_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.snort_warning_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.snort_critical_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.var_log_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.step_baseline_uncaught_intrusion_steps
        return info

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return  "# alerts recent:{}, # severe alerts recent: {}, # warning alerts recent: {}, " \
                "sum priority recent:{}, # alerts total:{} # severe alerts total: {}, " \
                "# warning alerts total: {}, sum priority total: {}, caught_attacker:{}," \
                "stopped:{}, step:{}, snort_severe_baseline_reward:{}, snort_warning_baseline_reward:{}," \
                "snort_severe_baseline_stopped:{}, snort_warning_baseline_stopped:{}," \
                "snort_critical_baseline_reward:{}, snort_critical_baseline_stopped:{}," \
                "var_log_baseline_reward:{}, var_log_baseline_stopped:{}, last_alert_ts:{}," \
                "snort_severe_baseline_step:{}, snort_warning_baseline_step:{}, snort_critical_baseline_step:{}," \
                "var_log_baseline_step:{}, step_baseline_reward:{}, step_baseline_step:{}, step_baseline_stopped:{}".format(
            self.num_alerts_recent, self.num_severe_alerts_recent, self.num_warning_alerts_recent,
            self.sum_priority_alerts_recent, self.num_alerts_total, self.num_severe_alerts_total,
            self.num_warning_alerts_total, self.sum_priority_alerts_total,
            self.caught_attacker, self.stopped, self.step, self.snort_severe_baseline_reward,
            self.snort_warning_baseline_reward, self.snort_severe_baseline_stopped,
            self.snort_warning_baseline_stopped, self.snort_critical_baseline_reward,
            self.snort_critical_baseline_stopped, self.var_log_baseline_reward, self.var_log_baseline_stopped,
            self.last_alert_ts, self.snort_severe_baseline_step, self.snort_warning_baseline_step,
            self.snort_critical_baseline_step, self.var_log_baseline_step, self.step_baseline_reward,
            self.step_baseline_step, self.step_baseline_stopped) + "\n" + "\n".join([str(i) + ":"
                                                    + str(self.machines[i]) for i in range(len(self.machines))])
