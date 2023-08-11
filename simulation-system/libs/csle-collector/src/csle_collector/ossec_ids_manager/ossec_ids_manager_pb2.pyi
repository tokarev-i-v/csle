"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class GetOSSECIdsAlertsMsg(google.protobuf.message.Message):
    """Message that the client sends to extract the IDS log statistics from a given timestamp"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIMESTAMP_FIELD_NUMBER: builtins.int
    LOG_FILE_PATH_FIELD_NUMBER: builtins.int
    timestamp: builtins.float
    log_file_path: builtins.str
    def __init__(
        self,
        *,
        timestamp: builtins.float = ...,
        log_file_path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["log_file_path", b"log_file_path", "timestamp", b"timestamp"]) -> None: ...

global___GetOSSECIdsAlertsMsg = GetOSSECIdsAlertsMsg

@typing_extensions.final
class StopOSSECIdsMonitorMsg(google.protobuf.message.Message):
    """Message that the client sends to stop the OSSECIdsMonitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StopOSSECIdsMonitorMsg = StopOSSECIdsMonitorMsg

@typing_extensions.final
class StopOSSECIdsMsg(google.protobuf.message.Message):
    """Message that the client sends to stop the OSSECIds"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StopOSSECIdsMsg = StopOSSECIdsMsg

@typing_extensions.final
class StartOSSECIdsMsg(google.protobuf.message.Message):
    """Message that the client sends to start the OSSECIds"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StartOSSECIdsMsg = StartOSSECIdsMsg

@typing_extensions.final
class StartOSSECIdsMonitorMsg(google.protobuf.message.Message):
    """Message that the client sends to start the OSSECIdsMonitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KAFKA_IP_FIELD_NUMBER: builtins.int
    KAFKA_PORT_FIELD_NUMBER: builtins.int
    LOG_FILE_PATH_FIELD_NUMBER: builtins.int
    TIME_STEP_LEN_SECONDS_FIELD_NUMBER: builtins.int
    kafka_ip: builtins.str
    kafka_port: builtins.int
    log_file_path: builtins.str
    time_step_len_seconds: builtins.int
    def __init__(
        self,
        *,
        kafka_ip: builtins.str = ...,
        kafka_port: builtins.int = ...,
        log_file_path: builtins.str = ...,
        time_step_len_seconds: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["kafka_ip", b"kafka_ip", "kafka_port", b"kafka_port", "log_file_path", b"log_file_path", "time_step_len_seconds", b"time_step_len_seconds"]) -> None: ...

global___StartOSSECIdsMonitorMsg = StartOSSECIdsMonitorMsg

@typing_extensions.final
class GetOSSECIdsMonitorStatusMsg(google.protobuf.message.Message):
    """Message that the client sends to get the status of the OSSECIdsMonitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetOSSECIdsMonitorStatusMsg = GetOSSECIdsMonitorStatusMsg

@typing_extensions.final
class OSSECIdsMonitorDTO(google.protobuf.message.Message):
    """Message that the server returns when asked about the status of the OSSEC IDS Monitor thread and OSSEC itself"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MONITOR_RUNNING_FIELD_NUMBER: builtins.int
    OSSEC_IDS_RUNNING_FIELD_NUMBER: builtins.int
    monitor_running: builtins.bool
    ossec_ids_running: builtins.bool
    def __init__(
        self,
        *,
        monitor_running: builtins.bool = ...,
        ossec_ids_running: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["monitor_running", b"monitor_running", "ossec_ids_running", b"ossec_ids_running"]) -> None: ...

global___OSSECIdsMonitorDTO = OSSECIdsMonitorDTO

@typing_extensions.final
class OSSECIdsLogDTO(google.protobuf.message.Message):
    """Message that the server returns when requested by the client, contains info about the OSSEC IDS log"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIMESTAMP_FIELD_NUMBER: builtins.int
    IP_FIELD_NUMBER: builtins.int
    ATTEMPTED_ADMIN_ALERTS_FIELD_NUMBER: builtins.int
    TOTAL_ALERTS_FIELD_NUMBER: builtins.int
    WARNING_ALERTS_FIELD_NUMBER: builtins.int
    SEVERE_ALERTS_FIELD_NUMBER: builtins.int
    ALERTS_WEIGHTED_BY_LEVEL_FIELD_NUMBER: builtins.int
    LEVEL_0_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_1_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_2_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_3_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_4_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_5_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_6_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_7_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_8_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_9_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_10_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_11_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_12_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_13_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_14_ALERTS_FIELD_NUMBER: builtins.int
    LEVEL_15_ALERTS_FIELD_NUMBER: builtins.int
    INVALID_LOGIN_ALERTS_FIELD_NUMBER: builtins.int
    AUTHENTICATION_SUCCESS_ALERTS_FIELD_NUMBER: builtins.int
    AUTHENTICATION_FAILED_ALERTS_FIELD_NUMBER: builtins.int
    CONNECTION_ATTEMPT_ALERTS_FIELD_NUMBER: builtins.int
    ATTACKS_ALERTS_FIELD_NUMBER: builtins.int
    ADDUSER_ALERTS_FIELD_NUMBER: builtins.int
    SSHD_ALERTS_FIELD_NUMBER: builtins.int
    IDS_ALERTS_FIELD_NUMBER: builtins.int
    FIREWALL_ALERTS_FIELD_NUMBER: builtins.int
    SQUID_ALERTS_FIELD_NUMBER: builtins.int
    APACHE_ALERTS_FIELD_NUMBER: builtins.int
    SYSLOG_ALERTS_FIELD_NUMBER: builtins.int
    timestamp: builtins.float
    ip: builtins.str
    attempted_admin_alerts: builtins.int
    total_alerts: builtins.int
    warning_alerts: builtins.int
    severe_alerts: builtins.int
    alerts_weighted_by_level: builtins.int
    level_0_alerts: builtins.int
    level_1_alerts: builtins.int
    level_2_alerts: builtins.int
    level_3_alerts: builtins.int
    level_4_alerts: builtins.int
    level_5_alerts: builtins.int
    level_6_alerts: builtins.int
    level_7_alerts: builtins.int
    level_8_alerts: builtins.int
    level_9_alerts: builtins.int
    level_10_alerts: builtins.int
    level_11_alerts: builtins.int
    level_12_alerts: builtins.int
    level_13_alerts: builtins.int
    level_14_alerts: builtins.int
    level_15_alerts: builtins.int
    invalid_login_alerts: builtins.int
    authentication_success_alerts: builtins.int
    authentication_failed_alerts: builtins.int
    connection_attempt_alerts: builtins.int
    attacks_alerts: builtins.int
    adduser_alerts: builtins.int
    sshd_alerts: builtins.int
    ids_alerts: builtins.int
    firewall_alerts: builtins.int
    squid_alerts: builtins.int
    apache_alerts: builtins.int
    syslog_alerts: builtins.int
    def __init__(
        self,
        *,
        timestamp: builtins.float = ...,
        ip: builtins.str = ...,
        attempted_admin_alerts: builtins.int = ...,
        total_alerts: builtins.int = ...,
        warning_alerts: builtins.int = ...,
        severe_alerts: builtins.int = ...,
        alerts_weighted_by_level: builtins.int = ...,
        level_0_alerts: builtins.int = ...,
        level_1_alerts: builtins.int = ...,
        level_2_alerts: builtins.int = ...,
        level_3_alerts: builtins.int = ...,
        level_4_alerts: builtins.int = ...,
        level_5_alerts: builtins.int = ...,
        level_6_alerts: builtins.int = ...,
        level_7_alerts: builtins.int = ...,
        level_8_alerts: builtins.int = ...,
        level_9_alerts: builtins.int = ...,
        level_10_alerts: builtins.int = ...,
        level_11_alerts: builtins.int = ...,
        level_12_alerts: builtins.int = ...,
        level_13_alerts: builtins.int = ...,
        level_14_alerts: builtins.int = ...,
        level_15_alerts: builtins.int = ...,
        invalid_login_alerts: builtins.int = ...,
        authentication_success_alerts: builtins.int = ...,
        authentication_failed_alerts: builtins.int = ...,
        connection_attempt_alerts: builtins.int = ...,
        attacks_alerts: builtins.int = ...,
        adduser_alerts: builtins.int = ...,
        sshd_alerts: builtins.int = ...,
        ids_alerts: builtins.int = ...,
        firewall_alerts: builtins.int = ...,
        squid_alerts: builtins.int = ...,
        apache_alerts: builtins.int = ...,
        syslog_alerts: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["adduser_alerts", b"adduser_alerts", "alerts_weighted_by_level", b"alerts_weighted_by_level", "apache_alerts", b"apache_alerts", "attacks_alerts", b"attacks_alerts", "attempted_admin_alerts", b"attempted_admin_alerts", "authentication_failed_alerts", b"authentication_failed_alerts", "authentication_success_alerts", b"authentication_success_alerts", "connection_attempt_alerts", b"connection_attempt_alerts", "firewall_alerts", b"firewall_alerts", "ids_alerts", b"ids_alerts", "invalid_login_alerts", b"invalid_login_alerts", "ip", b"ip", "level_0_alerts", b"level_0_alerts", "level_10_alerts", b"level_10_alerts", "level_11_alerts", b"level_11_alerts", "level_12_alerts", b"level_12_alerts", "level_13_alerts", b"level_13_alerts", "level_14_alerts", b"level_14_alerts", "level_15_alerts", b"level_15_alerts", "level_1_alerts", b"level_1_alerts", "level_2_alerts", b"level_2_alerts", "level_3_alerts", b"level_3_alerts", "level_4_alerts", b"level_4_alerts", "level_5_alerts", b"level_5_alerts", "level_6_alerts", b"level_6_alerts", "level_7_alerts", b"level_7_alerts", "level_8_alerts", b"level_8_alerts", "level_9_alerts", b"level_9_alerts", "severe_alerts", b"severe_alerts", "squid_alerts", b"squid_alerts", "sshd_alerts", b"sshd_alerts", "syslog_alerts", b"syslog_alerts", "timestamp", b"timestamp", "total_alerts", b"total_alerts", "warning_alerts", b"warning_alerts"]) -> None: ...

global___OSSECIdsLogDTO = OSSECIdsLogDTO