from typing import List, Dict, Any, Tuple
import time
import numpy as np
import csle_collector.constants.constants as constants
from csle_collector.ids_manager.ids_alert import FastLogAlert
import csle_collector.ids_manager.ids_manager_pb2


class AlertCounters:
    """
    DTO containing statistics from the IDS log

    """
    def __init__(self):
        """
        Initializes the DTO
        """
        self.priority_alerts = list(np.zeros(4))
        self.class_alerts = list(np.zeros(len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))))
        self.severe_alerts = 0
        self.warning_alerts = 0
        self.total_alerts = 0
        self.ip = None
        self.ts = None

    def count(self, alerts: List[FastLogAlert]) -> None:
        """
        Counts the list of alerts

        :param alerts: list of alerts from the log
        :return: None
        """
        for a in alerts:
            if a.priority in range(0, len(self.priority_alerts)):
                self.priority_alerts[a.priority] += 1
            if a.class_id in range(0, len(self.class_alerts)):
                self.class_alerts[a.class_id] += 1

        self.total_alerts = len(alerts)
        self.warning_alerts = sum(self.priority_alerts[0:constants.IDS_ROUTER.SEVERE_ALERT_PRIORITY_THRESHOLD])
        self.severe_alerts = sum(self.priority_alerts[constants.IDS_ROUTER.SEVERE_ALERT_PRIORITY_THRESHOLD:])

    @staticmethod
    def from_kafka_record(record: str) -> "AlertCounters":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record to convert
        :return: the DTO
        """
        parts = record.split(",")
        obj = AlertCounters()
        obj.ts = float(parts[0])
        obj.ip = parts[1]
        obj.total_alerts = parts[2]
        obj.warning_alerts = parts[3]
        obj.severe_alerts = parts[4]
        obj.class_alerts = []
        obj.priority_alerts = []
        for i in range(5, len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))+5):
            obj.class_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))+5,
                       len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))+9):
            obj.priority_alerts.append(int(round(float(parts[i]))))
        return obj

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a kafka record

        :param record: the kafka record to use for updating
        :return: None
        """
        parts = record.split(",")
        self.ts = float(parts[0])
        self.ip = parts[1]
        self.total_alerts = parts[2]
        self.warning_alerts = parts[3]
        self.severe_alerts = parts[4]
        self.class_alerts = []
        self.priority_alerts = []
        for i in range(5, len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))+5):
            self.class_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))+5,
                       len(set(constants.IDS_ROUTER.ALERT_IDS_ID.values()))+9):
            self.priority_alerts.append(int(round(float(parts[i]))))


    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record

        :param ip: the ip to add to the record in addition to the IDS statistics
        :return: a comma-separated string representing the kafka record
        """
        ts = time.time()
        total_counters = [ts, ip, self.total_alerts, self.warning_alerts, self.severe_alerts] \
                         + self.class_alerts + self.priority_alerts
        record_str = ",".join(list(map(lambda x: str(x), total_counters)))
        return record_str

    def to_dto(self, ip: str) -> csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO:
        """
        Converts the object into a gRPC DTO for serialization

        :param ip: the ip to add to the DTO in addition to the statistics
        :return: A csle_collector.ids_manager.ids_manager_pb2.IdsLogDTOb
        """
        ts = time.time()
        csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO(
            timestamp=ts,
            ip=ip,
            attempted_admin_alerts=self.class_alerts[33],
            attempted_user_alerts=self.class_alerts[32],
            inappropriate_content_alerts=self.class_alerts[31],
            policy_violation_alerts=self.class_alerts[30],
            shellcode_detect_alerts=self.class_alerts[29],
            successful_admin_alerts=self.class_alerts[28],
            successful_user_alerts=self.class_alerts[27],
            trojan_activity_alerts=self.class_alerts[26],
            unsuccessful_user_alerts=self.class_alerts[25],
            web_application_attack_alerts=self.class_alerts[24],
            attempted_dos_alerts=self.class_alerts[23],
            attempted_recon_alerts=self.class_alerts[22],
            bad_unknown_alerts=self.class_alerts[21],
            default_login_attempt_alerts=self.class_alerts[20],
            denial_of_service_alerts=self.class_alerts[19],
            misc_attack_alerts=self.class_alerts[18],
            non_standard_protocol_alerts=self.class_alerts[17],
            rpc_portman_decode_alerts=self.class_alerts[16],
            successful_dos_alerts=self.class_alerts[15],
            successful_recon_largescale_alerts=self.class_alerts[14],
            successful_recon_limited_alerts=self.class_alerts[13],
            suspicious_filename_detect_alerts=self.class_alerts[12],
            suspicious_login_alerts=self.class_alerts[11],
            system_call_detect_alerts=self.class_alerts[10],
            unusual_client_port_connection_alerts=self.class_alerts[9],
            web_application_activity_alerts=self.class_alerts[8],
            icmp_event_alerts=self.class_alerts[7],
            misc_activity_alerts=self.class_alerts[6],
            network_scan_alerts=self.class_alerts[5],
            not_suspicious_alerts=self.class_alerts[4],
            protocol_command_decode_alerts=self.class_alerts[3],
            string_detect_alerts=self.class_alerts[2],
            unknown_alerts=self.class_alerts[1],
            tcp_connection_alerts=self.class_alerts[0],
            priority_1_alerts=self.priority_alerts[1],
            priority_2_alerts=self.priority_alerts[2],
            priority_3_alerts=self.priority_alerts[3],
            priority_4_alerts=self.priority_alerts[4],
            total_alerts=self.total_alerts,
            warning_alerts=self.warning_alerts,
            severe_alerts=self.severe_alerts
        )

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"total_alerts: {self.total_alerts}, warning_alerts: {self.warning_alerts}, " \
               f"severe_alerts: {self.severe_alerts}, " \
               f"priority_alerts: {self.priority_alerts}, class_alerts: {self.class_alerts}"


    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AlertCounters":
        """
        Converts a dict representaion of the object into an instance

        :param d: the dict to convert
        :return: the DTO
        """
        obj = AlertCounters()
        obj.ip = d["ip"]
        obj.ts = d["ts"]
        obj.total_alerts = d["total_alerts"]
        obj.warning_alerts = d["warning_alerts"]
        obj.severe_alerts = d["severe_alerts"]
        obj.priority_alerts = d["priority_alerts"]
        obj.class_alerts = d["class_alerts"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["class_alerts"] = self.class_alerts
        d["priority_alerts"] = self.priority_alerts
        d["total_alerts"] = self.total_alerts
        d["warning_alerts"] = self.warning_alerts
        d["severe_alerts"] = self.severe_alerts
        return d

    def copy(self) -> "AlertCounters":
        """
        :return: a copy of the object
        """
        c = AlertCounters()
        c.class_alerts = self.class_alerts
        c.priority_alerts = self.priority_alerts
        c.ip = self.ip
        c.ts = self.ts
        c.total_alerts = self.total_alerts
        c.warning_alerts = self.warning_alerts
        c.severe_alerts = self.severe_alerts

    def get_deltas(self, counters_prime: "AlertCounters", max_counter: int) -> Tuple[List[int], List[str]]:
        """
        Get the deltas between two counters objects

        :param counters_prime: the counters object to compare with
        :param max_counter: the maximum counter value
        :return: the deltas and the labels
        """
        deltas_priority = list(np.minimum([max_counter]*len(counters_prime.priority_alerts),
                                     np.maximum([-max_counter]*len(counters_prime.priority_alerts),
                                     np.array(counters_prime.priority_alerts) - np.array(self.priority_alerts))))
        deltas_class = list(np.minimum([max_counter]*len(counters_prime.class_alerts),
                                  np.maximum([-max_counter]*len(counters_prime.class_alerts),
                                  np.array(counters_prime.class_alerts) - np.array(self.class_alerts))))
        deltas = [
                     min(max_counter, max(-max_counter, counters_prime.total_alerts-self.total_alerts)),
                     min(max_counter, max(-max_counter, counters_prime.warning_alerts-self.warning_alerts)),
                     min(max_counter, max(-max_counter, counters_prime.severe_alerts-self.severe_alerts))
                  ] + deltas_priority + deltas_class
        labels = constants.LOG_SINK.IDS_ALERTS_LABELS
        assert len(labels) == len(deltas)
        return list(deltas), labels





