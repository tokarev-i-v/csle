from enum import Enum

class ActionId(Enum):
    """
    Enum representing the different attacks
    """
    TCP_SYN_STEALTH_SCAN_HOST = 0
    PING_SCAN_HOST = 1
    UDP_PORT_SCAN_HOST = 2
    TCP_CON_NON_STEALTH_SCAN_HOST = 3
    TCP_FIN_SCAN_HOST = 4
    TCP_NULL_SCAN_HOST = 5
    TCP_XMAS_TREE_SCAN_HOST = 6
    OS_DETECTION_SCAN_HOST = 7
    VULSCAN_HOST = 8
    NMAP_VULNERS_HOST=9
    TELNET_SAME_USER_PASS_DICTIONARY_HOST=10
    SSH_SAME_USER_PASS_DICTIONARY_HOST=11
    FTP_SAME_USER_PASS_DICTIONARY_HOST=12
    CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST=13
    IRC_SAME_USER_PASS_DICTIONARY_HOST=14
    MONGO_SAME_USER_PASS_DICTIONARY_HOST=15
    MYSQL_SAME_USER_PASS_DICTIONARY_HOST=16
    SMTP_SAME_USER_PASS_DICTIONARY_HOST=17
    POSTGRES_SAME_USER_PASS_DICTIONARY_HOST=18

    TCP_SYN_STEALTH_SCAN_SUBNET = 19
    PING_SCAN_SUBNET = 20
    UDP_PORT_SCAN_SUBNET = 21
    TCP_CON_NON_STEALTH_SCAN_SUBNET = 22
    TCP_FIN_SCAN_SUBNET = 23
    TCP_NULL_SCAN_SUBNET = 24
    TCP_XMAS_TREE_SCAN_SUBNET = 25
    OS_DETECTION_SCAN_SUBNET = 26
    VULSCAN_SUBNET = 27
    NMAP_VULNERS_SUBNET = 28
    TELNET_SAME_USER_PASS_DICTIONARY_SUBNET=29
    SSH_SAME_USER_PASS_DICTIONARY_SUBNET=30
    FTP_SAME_USER_PASS_DICTIONARY_SUBNET=31
    CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET=32
    IRC_SAME_USER_PASS_DICTIONARY_SUBNET=33
    MONGO_SAME_USER_PASS_DICTIONARY_SUBNET=34
    MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET=35
    SMTP_SAME_USER_PASS_DICTIONARY_SUBNET=36
    POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET=37

    NETWORK_SERVICE_LOGIN=38
    FIND_FLAG = 39

    NIKTO_WEB_HOST_SCAN = 40
    MASSCAN_HOST_SCAN = 41
    MASSCAN_SUBNET_SCAN = 42
    FIREWALK_HOST = 43
    FIREWALK_SUBNET = 44
    HTTP_ENUM_HOST = 45
    HTTP_ENUM_SUBNET = 46
    HTTP_GREP_HOST = 47
    HTTP_GREP_SUBNET = 48