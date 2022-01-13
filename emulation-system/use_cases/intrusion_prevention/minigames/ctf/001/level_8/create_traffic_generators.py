import os
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants


def default_traffic_generators() -> TrafficConfig:
    """
    :return: the TrafficConfig of the emulation
    """
    traffic_generators = [
        NodeTrafficConfig(ip="172.18.8.254",
                          commands=[
                              # "timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n  172.18.8.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5 -n 172.18.8.0/24 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.2 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.3 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.21 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.79 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.10 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.19 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.31 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.42 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.37 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.82 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.75 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.71 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.8.11 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.2 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.3 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.21 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.79 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.10 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.19 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.31 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.42 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.37 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.82 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.75 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.71 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21",
                              "172.18.8.79", "172.18.8.10", "172.18.8.19", "172.18.8.31", "172.18.8.42", "172.18.8.37",
                              "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.191", commands=[],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21",
                              "172.18.8.79", "172.18.8.10", "172.18.8.19",
                              "172.18.8.31", "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75",
                              "172.18.8.71", "172.18.8.11",
                              "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                              "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                              "172.18.8.61", "172.18.8.62"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip="172.18.8.10", commands=[
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
            "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
            "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
            "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
            "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
            "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
            "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
            "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
            "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
            "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
            "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
            "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
            "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
        ], jumphosts=[
            "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
            "172.18.8.191", "172.18.8.19", "172.18.8.31",
            "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
            "172.18.8.11",
            "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
            "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
            "172.18.8.61", "172.18.8.62"
        ], target_hosts=[
            "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
            "172.18.8.19", "172.18.8.31",
            "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
            "172.18.8.11",
            "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
            "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
            "172.18.8.61", "172.18.8.62"]),
        NodeTrafficConfig(ip="172.18.8.2",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.52 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.52:80 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11", "172.18.8.52"
                          ],
                          target_hosts=[
                              "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.19", "172.18.8.31", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11", "172.18.8.52"
                          ]),
        NodeTrafficConfig(ip="172.18.8.3",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              ["172.18.8.2", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                               "172.18.8.10", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                               "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                               "172.18.8.11"]
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.21", "172.18.8.79",
                              "172.18.8.19", "172.18.8.31", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.21",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3",
                              "172.18.8.79",
                              "172.18.8.19", "172.18.8.31", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.79",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.51 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.51:80 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.191",
                              "172.18.8.10", "172.18.8.19", "172.18.8.31",
                              "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11", "172.18.8.51"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21",
                              "172.18.8.19", "172.18.8.31",
                              "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11", "172.18.8.51"
                          ]),
        NodeTrafficConfig(ip="172.18.8.19",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.31",
                              "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.31",
                              "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                              "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.31",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                              "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.42", "172.18.8.37",
                              "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.42",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.37", "172.18.8.82",
                              "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.37", "172.18.8.82",
                              "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.37",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.42", "172.18.8.82",
                              "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.42", "172.18.8.82",
                              "172.18.8.75", "172.18.8.71", "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.82",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.51 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.51:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.53 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.53 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.53 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.53 -p 5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                              "172.18.8.75", "172.18.8.71", "172.18.8.11", "172.18.8.53", "172.18.8.51"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.42",
                              "172.18.8.37", "172.18.8.75", "172.18.8.71", "172.18.8.11", "172.18.8.53",
                              "172.18.8.51"
                          ]),
        NodeTrafficConfig(ip="172.18.8.75",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                              "172.18.8.82", "172.18.8.71", "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.71", "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.71",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                              "172.18.8.82", "172.18.8.75", "172.18.8.11"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.11"
                          ]),
        NodeTrafficConfig(ip="172.18.8.11",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.8.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.21 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.8.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.19 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.19 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.31 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.31 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.42/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.42 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.37 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.37 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.75 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.71 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.71:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                              "172.18.8.10", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                              "172.18.8.82", "172.18.8.75", "172.18.8.71"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                              "172.18.8.79", "172.18.8.42",
                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71"
                          ]),
        NodeTrafficConfig(ip="172.18.8.51",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234",
                              "timeout 5 ftp 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.79", "172.18.8.82"
                          ],
                          target_hosts=[
                              "172.18.8.79", "172.18.8.82"
                          ]),
        NodeTrafficConfig(ip="172.18.8.52",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.54 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.2", "172.18.8.54"
                          ],
                          target_hosts=[
                              "172.18.8.2", "172.18.8.54"
                          ]),
        NodeTrafficConfig(ip="172.18.8.53",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.82 -c csle_ctf1234"
                          ],
                          jumphosts=[
                              "172.18.8.82"
                          ],
                          target_hosts=[
                              "172.18.8.82"
                          ]),
        NodeTrafficConfig(ip="172.18.8.54",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.52 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.52:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.55 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.55 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.55 -c csle_ctf1234 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.52", "172.18.8.55"
                          ],
                          target_hosts=[
                              "172.18.8.52", "172.18.8.55"
                          ]),
        NodeTrafficConfig(ip="172.18.8.55",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.54 > /dev/null 2>&1",
                              "(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L 172.18.8.54 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.56 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.56/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.56 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.54", "172.18.8.56"
                          ],
                          target_hosts=[
                              "172.18.8.54", "172.18.8.56"
                          ]),
        NodeTrafficConfig(ip="172.18.8.56",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.55 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.55 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.8.55 -c csle_ctf1234 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.57 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.57 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.57 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.55", "172.18.8.57"
                          ],
                          target_hosts=[
                              "172.18.8.55", "172.18.8.57"
                          ]),
        NodeTrafficConfig(ip="172.18.8.57",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.56 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.56/login.php > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.8.56 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.58 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.58 -c csle_ctf1234"
                          ],
                          jumphosts=[
                              "172.18.8.56", "172.18.8.58"
                          ],
                          target_hosts=[
                              "172.18.8.56", "172.18.8.58"
                          ]),
        NodeTrafficConfig(ip="172.18.8.58",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.57 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.57 -c csle_ctf1234",
                              "timeout 5 curl 172.18.8.57 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.59 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.59 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.57", "172.18.8.59"
                          ],
                          target_hosts=[
                              "172.18.8.57", "172.18.8.59"
                          ]),
        NodeTrafficConfig(ip="172.18.8.59",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.58 > /dev/null 2>&1",
                              "snmpwalk -v2c 172.18.8.58 -c csle_ctf1234",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.60 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.60:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.58", "172.18.8.60"
                          ],
                          target_hosts=[
                              "172.18.8.58", "172.18.8.60"
                          ]),
        NodeTrafficConfig(ip="172.18.8.60",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.59 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.59 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.59", "172.18.8.61"
                          ],
                          target_hosts=[
                              "172.18.8.59", "172.18.8.61"
                          ]),
        NodeTrafficConfig(ip="172.18.8.61",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.60 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.60:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.62 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.8.62:80 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.60", "172.18.8.62"
                          ],
                          target_hosts=[
                              "172.18.8.60", "172.18.8.62"
                          ]),
        NodeTrafficConfig(ip="172.18.8.62",
                          commands=[
                              "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.8.61"
                          ],
                          target_hosts=[
                              "172.18.8.61"
                          ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf

# Generates the traffic.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators())
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip="172.18.8.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)