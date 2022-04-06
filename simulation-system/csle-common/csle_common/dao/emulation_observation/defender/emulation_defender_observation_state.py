from typing import List, Dict, Any
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state \
    import EmulationDefenderMachineObservationState
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig
from csle_common.consumer_threads.docker_stats_consumer_thread import DockerStatsConsumerThread
from csle_common.consumer_threads.ids_log_consumer_thread import IdsLogConsumerThread
from csle_common.consumer_threads.client_population_consumer_thread import ClientPopulationConsumerThread
from csle_common.consumer_threads.attacker_actions_consumer_thread import AttackerActionsConsumerThread
from csle_common.consumer_threads.defender_actions_consumer_thread import DefenderActionsConsumerThread
from csle_common.consumer_threads.aggregated_host_metrics_thread import AggregatedHostMetricsThread
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_collector.ids_manager.alert_counters import AlertCounters
from csle_collector.host_manager.host_metrics import HostMetrics


class EmulationDefenderObservationState:
    """
    Represents the defender's agent's current belief state of the emulation
    """

    def __init__(self, log_sink_config : LogSinkConfig,
                 client_population_metrics : ClientPopulationMetrics = None, docker_stats: DockerStats = None,
                 ids_alert_counters : AlertCounters = None, aggregated_host_metrics: HostMetrics= None,
                 defender_actions : List[EmulationDefenderAction] = None,
                 attacker_actions: List[EmulationAttackerAction] = None):
        """
        Initializes the DTO

        :param log_sink_config: the log sink config
        :param client_population_metrics: the client population metrics
        :param docker_stats: the docker stats
        :param ids_alert_counters: the ids alert counters
        :param defender_actions: the list of defender actions
        :param attacker_actions: the list of attacker actions
        :param aggregated_host_metrics: the aggregated host metrics
        """
        self.log_sink_config = log_sink_config
        self.machines : List[EmulationDefenderMachineObservationState] = []
        self.actions_tried = set()
        self.client_population_metrics = client_population_metrics
        if self.client_population_metrics is None:
            self.client_population_metrics = ClientPopulationMetrics()
        self.docker_stats = docker_stats
        if self.docker_stats is None:
            self.docker_stats = DockerStats()
        self.ids_alert_counters = ids_alert_counters
        if self.ids_alert_counters is None:
            self.ids_alert_counters = AlertCounters()
        self.attacker_actions = attacker_actions
        if self.attacker_actions is None:
            self.attacker_actions = []
        self.defender_actions = defender_actions
        if self.defender_actions is None:
            self.defender_actions = []
        self.aggregated_host_metrics = aggregated_host_metrics
        if aggregated_host_metrics is None:
            self.aggregated_host_metrics = HostMetrics()
        self.docker_stats_consumer_thread = None
        self.client_population_consumer_thread = None
        self.ids_log_consumer_thread = None
        self.attacker_actions_consumer_thread = None
        self.defender_actions_consumer_thread = None
        self.aggregated_host_metrics_thread = None

    def start_monitoring_threads(self) -> None:
        """
        Starts the avg host metrics thread

        :return: None
        """
        self.aggregated_host_metrics_thread = AggregatedHostMetricsThread(
            host_metrics=self.aggregated_host_metrics,
            sleep_time=self.log_sink_config.time_step_len_seconds,
            machines=self.machines
        )
        self.docker_stats_consumer_thread = DockerStatsConsumerThread(
            kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port,
            docker_stats=self.docker_stats)
        self.client_population_consumer_thread = ClientPopulationConsumerThread(
            kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port,
            client_population_metrics=self.client_population_metrics
        )
        self.ids_log_consumer_thread = IdsLogConsumerThread(
            kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port,
            ids_alert_counters=self.ids_alert_counters
        )
        self.attacker_actions_consumer_thread = AttackerActionsConsumerThread(
            kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port,
            attacker_actions=self.attacker_actions
        )
        self.defender_actions_consumer_thread = DefenderActionsConsumerThread(
            kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port,
            defender_actions=self.defender_actions
        )
        self.aggregated_host_metrics_thread.start()
        self.docker_stats_consumer_thread.start()
        self.client_population_consumer_thread.start()
        self.ids_log_consumer_thread.start()
        self.attacker_actions_consumer_thread.start()
        self.defender_actions_consumer_thread.start()
        for m in self.machines:
            m.start_monitor_threads()

    @staticmethod
    def from_dict(d: Dict[str, Any])-> "EmulationDefenderObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationDefenderObservationState(log_sink_config=d["log_sink_config"])
        obj.machines = list(map(lambda x: EmulationDefenderMachineObservationState.from_dict(d=x), d["machines"]))
        obj.actions_tried = set(list(map(lambda x: tuple(x), d["actions_tried"])))
        obj.client_population_metrics = ClientPopulationMetrics.from_dict(d["client_population_metrics"])
        obj.docker_stats = DockerStats.from_dict(d["docker_stats"])
        obj.ids_alert_counters = AlertCounters.from_dict(d["ids_alert_counters"])
        obj.aggregated_host_metrics = HostMetrics.from_dict(d["aggregated_host_metrics"])
        obj.attacker_actions = list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_actions"]))
        obj.defender_actions = list(map(lambda x: EmulationDefenderAction.from_dict(x), d["defender_actions"]))
        obj.log_sink_config = LogSinkConfig.from_dict(d["log_sink_config"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["machines"] = list(map(lambda x: x.to_dict(), self.machines))
        d["actions_tried"] = list(self.actions_tried)
        d["client_population_metrics"] = self.client_population_metrics.to_dict()
        d["docker_stats"] = self.docker_stats.to_dict()
        d["ids_alert_counters"] = self.ids_alert_counters.to_dict()
        d["log_sink_config"] = self.log_sink_config.to_dict()
        d["attacker_actions"] = list(map(lambda x: x.to_dict(), self.attacker_actions))
        d["defender_actions"] = list(map(lambda x: x.to_dict(), self.defender_actions))
        d["aggregated_host_metrics"] = self.aggregated_host_metrics.to_dict()
        return d

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ips[0].rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        if self.docker_stats_consumer_thread is not None:
            self.docker_stats_consumer_thread.running = False
            self.docker_stats_consumer_thread.consumer.close()
        if self.client_population_consumer_thread is not None:
            self.client_population_consumer_thread.running = False
            self.client_population_consumer_thread.consumer.close()
        if self.ids_log_consumer_thread is not None:
            self.ids_log_consumer_thread.running = False
            self.ids_log_consumer_thread.consumer.close()
        if self.attacker_actions_consumer_thread is not None:
            self.attacker_actions_consumer_thread.running = False
            self.attacker_actions_consumer_thread.consumer.close()
        if self.defender_actions_consumer_thread is not None:
            self.defender_actions_consumer_thread.running = False
            self.defender_actions_consumer_thread.consumer.close()
        if self.aggregated_host_metrics_thread is not None:
            self.aggregated_host_metrics_thread.running = False
        for m in self.machines:
            m.cleanup()

    def get_action_ips(self, a : EmulationDefenderAction, emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Gets the ips of the node that a defender action is targeted for

        :param a: the action
        :param emulation_env_config: the emulation env config
        :return: the ip of the target node
        """
        if a.index == -1:
            return emulation_env_config.topology_config.subnetwork_masks
        if a.index < len(self.machines):
            return self.machines[a.index].ips
        return a.ips

    def copy(self) -> "EmulationDefenderObservationState":
        """
        :return: a copy of the object
        """
        c = EmulationDefenderObservationState(
            log_sink_config=self.log_sink_config,
            client_population_metrics=self.client_population_metrics.copy(), docker_stats=self.docker_stats.copy(),
            ids_alert_counters=self.ids_alert_counters.copy(), attacker_actions=self.attacker_actions.copy(),
            defender_actions=self.defender_actions.copy(), aggregated_host_metrics=self.aggregated_host_metrics.copy())
        c.actions_tried = self.actions_tried.copy()

        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"client_population_metrics: {self.client_population_metrics}," \
               f"docker_stats: {self.docker_stats}," \
               f"ids_alert_counters: {self.ids_alert_counters}," \
               f"aggregated_host_metrics: {self.aggregated_host_metrics}" \
               f"attacker_actions: {list(map(lambda x: str(x), self.attacker_actions))}," \
               f"defender_actions: {list(map(lambda x: str(x), self.defender_actions))}\n" \
               + "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
