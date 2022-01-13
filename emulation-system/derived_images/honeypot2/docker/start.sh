#!/bin/bash

#./setup_firewall.sh
service csle-firewall start
nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
/usr/sbin/sshd -D &
service snmpd restart
service postfix restart
service postgresql restart
service ntp restart
service rsyslog restart
tail -f /dev/null