"""
Constants for csle-rest-api
"""


class MGMT_WEBAPP:
    """
    Constants related to the management webapp
    """

    ACCESS_CONTROL_ALLOW_ORIGIN_HEADER = "Access-Control-Allow-Origin"
    IDS_QUERY_PARAM = "ids"
    DOWNLOAD_QUERY_PARAM = "download"
    TOKEN_QUERY_PARAM = "token"
    STOP_QUERY_PARAM = "stop"
    EMULATION_QUERY_PARAM = "emulation"
    EXECUTION_ID_QUERY_PARAM = "executionid"
    IP_QUERY_PARAM = "ip"
    CONTAINER_NAME_PROPERTY = "container_name"
    STATIC_RESOURCE_INDEX = "index.html"
    HTTP_REST_GET = "GET"
    HTTP_REST_POST = "POST"
    HTTP_REST_DELETE = "DELETE"
    HTTP_REST_PUT = "PUT"
    STATIC = "static"
    ABOUT_PAGE_RESOURCE = "about-page"
    LOGIN_PAGE_RESOURCE = "login-page"
    REGISTER_PAGE_RESOURCE = "register-page"
    EMULATION_STATISTICS_PAGE_RESOURCE = "emulation-statistics-page"
    EMULATIONS_PAGE_RESOURCE = "emulations-page"
    IMAGES_PAGE_RESOURCE = "images-page"
    DOWNLOADS_PAGE_RESOURCE = "downloads-page"
    SERVER_CLUSTER_PAGE_RESOURCE = "server-cluster-page"
    JOBS_PAGE_RESOURCE = "jobs-page"
    MONITORING_PAGE_RESOURCE = "monitoring-page"
    POLICIES_PAGE_RESOURCE = "policies-page"
    POLICY_EXAMINATION_PAGE_RESOURCE = "policy-examination-page"
    SDN_CONTROLLERS_PAGE_RESOURCE = "sdn-controllers-page"
    CONTROL_PLANE_PAGE_RESOURCE = "control-plane-page"
    USER_ADMIN_PAGE_RESOURCE = "user-admin-page"
    CONTAINER_TERMINAL_PAGE_RESOURCE = "container-terminal-page"
    SYSTEM_ADMIN_PAGE_RESOURCE = "system-admin-page"
    LOGS_ADMIN_PAGE_RESOURCE = "logs-admin-page"
    SIMULATIONS_PAGE_RESOURCE = "simulations-page"
    SYSTEM_MODELS_PAGE_RESOURCE = "system-models-page"
    TRACES_PAGE_RESOURCE = "traces-page"
    TRAINING_PAGE_RESOURCE = "training-page"
    CADVISOR_RESOURCE = "cadvisor"
    PGADMIN_RESOURCE = "pgadmin"
    GRAFANA_RESOURCE = "grafana"
    PARAM_RESOURCE = "param"
    PARAMETERS_PROPERTY = "parameters"
    CLUSTER_CONFIG_PROPERTY = "cluster_config"
    CLUSTER_STATUS_RESOURCE = "clusterstatus"
    NGINX_RESOURCE = "nginx"
    POSTGRESQL_RESOURCE = "postgresql"
    DOCKER_RESOURCE = "docker"
    FLASK_RESOURCE = "flask"
    CLUSTERMANAGER_RESOURCE = "clustermanager"
    NODE_EXPORTER_RESOURCE = "node-exporter"
    PROMETHEUS_RESOURCE = "prometheus"
    EMULATIONS_RESOURCE = "emulations"
    EXECUTIONS_SUBRESOURCE = "executions"
    INFO_SUBRESOURCE = "info"
    CLIENT_MANAGER_SUBRESOURCE = "client-manager"
    CLIENT_POPULATION_SUBRESOURCE = "client-population"
    CLIENT_PRODUCER_SUBRESOURCE = "client-producer"
    KAFKA_MANAGER_SUBRESOURCE = "kafka-manager"
    KAFKA_SUBRESOURCE = "kafka"
    ELK_MANAGER_SUBRESOURCE = "elk-manager"
    RYU_MANAGER_SUBRESOURCE = "ryu-manager"
    RYU_CONTROLLER_SUBRESOURCE = "ryu-controller"
    RYU_MONITOR_SUBRESOURCE = "ryu-monitor"
    ELK_STACK_SUBRESOURCE = "elk-stack"
    ELASTIC_SUBRESOURCE = "elastic"
    KIBANA_SUBRESOURCE = "kibana"
    LOGSTASH_SUBRESOURCE = "logstash"
    OSSEC_IDS_MANAGER_SUBRESOURCE = "ossec-ids-manager"
    OSSEC_IDS_SUBRESOURCE = "ossec-ids"
    OSSEC_IDS_MONITOR_SUBRESOURCE = "ossec-ids-monitor"
    SNORT_IDS_MANAGER_SUBRESOURCE = "snort-ids-manager"
    SNORT_IDS_SUBRESOURCE = "snort-ids"
    SNORT_IDS_MONITOR_SUBRESOURCE = "snort-ids-monitor"
    HOST_MANAGER_SUBRESOURCE = "host-manager"
    HOST_MONITOR_SUBRESOURCE = "host-monitor"
    TRAFFIC_MANAGER_SUBRESOURCE = "traffic-manager"
    TRAFFIC_GENERATOR_SUBRESOURCE = "traffic-generator"
    FILEBEAT_SUBRESOURCE = "filebeat"
    PACKETBEAT_SUBRESOURCE = "packetbeat"
    METRICBEAT_SUBRESOURCE = "metricbeat"
    HEARTBEAT_SUBRESOURCE = "heartbeat"
    DOCKER_STATS_MANAGER_SUBRESOURCE = "docker-stats-manager"
    DOCKER_STATS_MONITOR_SUBRESOURCE = "docker-stats-monitor"
    CREATE_SUBRESOURCE = "create"
    REGISTRATION_ALLOWED_SUBRESOURCE = "registration-allowed"
    CONTAINER_SUBRESOURCE = "container"
    SWITCHES_SUBRESOURCE = "switches"
    SDN_CONTROLLER_LOCAL_PORT = "sdn-controller-local-port"
    MONITOR_SUBRESOURCE = "monitor"
    EMULATION_EXECUTIONS_RESOURCE = "emulation-executions"
    EMULATION_TRACES_RESOURCE = "emulation-traces"
    EMULATION_SIMULATION_TRACES_RESOURCE = "emulation-simulation-traces"
    SIMULATION_TRACES_RESOURCE = "simulation-traces"
    TRACES_DATASETS_RESOURCE = "traces-datasets"
    STATISTICS_DATASETS_RESOURCE = "statistics-datasets"
    SIMULATIONS_RESOURCE = "simulations"
    EMULATION_STATISTICS_RESOURCE = "emulation-statistics"
    IMAGES_RESOURCE = "images"
    FILE_RESOURCE = "file"
    LOGIN_RESOURCE = "login"
    JOBS_RESOURCE = "jobs"
    MONITORING_RESOURCE = "monitoring"
    POLICIES_RESOURCE = "policies"
    SDN_CONTROLLERS_RESOURCE = "sdn-controllers"
    SYSTEM_MODELS_RESOURCE = "system-models"
    GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE = "gaussian-mixture-system-models"
    EMPIRICAL_SYSTEM_MODELS_RESOURCE = "empirical-system-models"
    GP_SYSTEM_MODELS_RESOURCE = "gp-system-models"
    EXPERIMENTS_RESOURCE = "experiments"
    MULTI_THRESHOLD_POLICIES_RESOURCE = "multi-threshold-policies"
    LINEAR_THRESHOLD_POLICIES_RESOURCE = "linear-threshold-policies"
    PPO_POLICIES_RESOURCE = "ppo-policies"
    ALPHA_VEC_POLICIES_RESOURCE = "alpha-vec-policies"
    VALUE_RESOURCE = "value"
    VECTOR_POLICIES_RESOURCE = "vector-policies"
    TABULAR_POLICIES_RESOURCE = "tabular-policies"
    USERS_RESOURCE = "users"
    LOGS_RESOURCE = "logs"
    CONFIG_RESOURCE = "config"
    SERVER_CLUSTER_RESOURCE = "server-cluster"
    VERSION_RESOURCE = "version"
    DQN_POLICIES_RESOURCE = "dqn-policies"
    FNN_W_SOFTMAX_POLICIES_RESOURCE = "fnn-w-softmax-policies"
    TRACES_RESOURCE = "traces"
    TRAINING_RESOURCE = "training"
    RUNNING_PROPERTY = "running"
    CADVISOR_RUNNING_PROPERTY = "cAdvisorRunning"
    GRAFANA_RUNNING_PROPERTY = "grafanaRunning"
    POSTGRESQL_RUNNING_PROPERTY = "postgresqlRunning"
    NODE_EXPORTER_RUNNING_PROPERTY = "nodeExporterRunning"
    DOCKER_ENGINE_RUNNING_PROPERTY = "dockerEngineRunning"
    NGINX_RUNNING_PROPERTY = "nginxRunning"
    FLASK_RUNNING_PROPERTY = "flaskRunning"
    PROMETHEUS_RUNNING_PROPERTY = "prometheusRunning"
    PGADMIN_RUNNING_PROPERTY = "pgAdminRunning"
    CADVISOR_URL_PROPERTY = "cAdvisorUrl"
    GRAFANA_URL_PROPERTY = "grafanaUrl"
    NODE_EXPORTER_URL_PROPERTY = "nodeExporterUrl"
    FLASK_URL_PROPERTY = "flaskUrl"
    PROMETHEUS_URL_PROPERTY = "prometheusUrl"
    PGADMIN_URL_PROPERTY = "pgAdminUrl"
    CADVISOR_PORT_PROPERTY = "cAdvisorPort"
    GRAFANA_PORT_PROPERTY = "grafanaPort"
    NODE_EXPORTER_PORT_PROPERTY = "nodeExporterPort"
    FLASK_PORT_PROPERTY = "flaskPort"
    PROMETHEUS_PORT_PROPERTY = "prometheusPort"
    PGADMIN_PORT_PROPERTY = "pgAdminPort"
    REGISTRATION_ALLOWED_PROPERTY = "registration_allowed"
    VERSION_PROPERTY = "version"
    OUTPUT_PROPERTY = "output"
    SALT_PROPOERTY = "salt"
    INPUT_PROPERTY = "input"
    ROWS_PROPERTY = "rows"
    COLS_PROPERTY = "cols"
    WS_CONNECT_MSG = "connect"
    WS_RESIZE_MSG = "resize"
    WS_CONTAINER_TERMINAL_OUTPUT_MSG = "container-terminal-output"
    WS_CONTAINER_TERMINAL_INPUT_MSG = "container-terminal-input"
    IP_PROPERTY = "ip"
    CPUS_PROPERTY = "cpus"
    GPUS_PROPERTY = "gpus"
    LEADER_PROPERTY = "leader"
    RAM_PROPERTY = "RAM"
    EXEC_ID_PROPERTY = "exec_id"
    EMULATION_PROPERTY = "emulation"
    STATISTIC_ID_PROPERTY = "statistic_id"
    SYSTEM_MODEL_TYPE = "system_model_type"
    SIMULATION_PROPERTY = "simulation"
    TRACES_DATASET_PROPERTY = "traces_dataset"
    STATISTICS_DATASET_PROPERTY = "statistics_dataset"
    ID_PROPERTY = "id"
    NAME_PROPERTY = "name"
    SIZE_PROPERTY = "size"
    TRAINING_JOBS_RESOURCE = "training-jobs"
    DATA_COLLECTION_JOBS_RESOURCE = "data-collection-jobs"
    SYSTEM_IDENTIFICATION_JOBS_RESOUCE = "system-identification-jobs"
    LOGS_PROPERTY = "logs"
    PATH_PROPERTY = "path"
    USER_PROPERTY = "user"
    PORT_PROPERTY = "port"
    THREAD_PROPERTY = "thread"
    START_PROPERTY = "start"
    CONFIG_PROPERTY = "config"
    STOP_PROPERTY = "stop"
    STOP_ALL_PROPERTY = "stop-all"
    START_ALL_PROPERTY = "start-all"
    USERNAME_PROPERTY = "username"
    PASSWORD_PROPERTY = "password"
    FIRST_NAME_PROPERTY = "first_name"
    LAST_NAME_PROPERTY = "last_name"
    EMAIL_PROPERTY = "email"
    ORGANIZATION_PROPERTY = "organization"
    TOKEN_PROPERTY = "token"
    ADMIN_PROPERTY = "admin"
    DPID_PROPERTY = "dpid"
    DESC_PROPERTY = "desc"
    FLOWS_PROPERTY = "flows"
    AGG_FLOWS_PROPERTY = "aggflows"
    TABLES_PROPERTY = "tables"
    TABLE_FEATURES_PROPERTY = "tablefeatures"
    PORT_STATS_PROPERTY = "portstats"
    PORT_DESCS_PROPERTY = "portdescs"
    QUEUES_PROPERTY = "queues"
    QUEUE_CONFIGS_PROPERTY = "queueconfigs"
    GROUPS_PROPERTY = "groups"
    GROUP_DESCS_PROPERTY = "groupdescs"
    GROUP_FEATURES_PROPERTY = "groupfeatures"
    METERS_PROPERTY = "meters"
    METER_CONFIGS_PROPERTY = "meter_configs"
    METER_FEATURES_PROPERTY = "meter_features"
    ROLES_PROPERTY = "roles"
    ACTIVE_COUNT_PROPERTY = "active_count"
    TABLE_ID_PROPERTY = "table_id"
    URL_PROPERTY = "url"
    TRAJECTORIES_PROPERTY = "trajectories"
    CONTENT_TYPE_HEADER = "Content-type"
    ACCEPT_HEADER = "Accept"
    APPLICATION_JSON_DATA_TYPE = "application/json"
    GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE = "gaussian_mixture"
    EMPIRICAL_SYSTEM_MODEL_TYPE = "empirical"
    GP_SYSTEM_MODEL_TYPE = "gp"
    WS_CONTAINER_TERMINAL_NAMESPACE = "container-terminal"
    CONTAINER_TERMINAL_SSH_SHELL = "container-terminal-ssh-shell"
    CONTAINER_TERMINAL_SSH_CONNECTION = "container-terminal-ssh-connection"


class SESSION_TOKENS:
    """
    Constants related to session tokens
    """

    EXPIRE_TIME_HOURS = 48
