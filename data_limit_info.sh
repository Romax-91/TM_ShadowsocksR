#!/bin/bash
#Отправка данных по сетвому трафику сервера
server="[AWS $(sudo curl ifconfig.me)] "
telegram-send "$server- Статистика сервера по трафику: $(sudo iptables -nvL -t filter --line-numbers)" >> /home/ubuntu/cron_info.log 2>&1