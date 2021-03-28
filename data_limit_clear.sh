#!/bin/bash
#Сброс данных по трафику. Обнуление
server="[AWS $(sudo curl ifconfig.me)] "
sudo iptables -Z OUTPUT
telegram-send "$server- Обнуление данных по трафику"
telegram-send "$server- Статистика сервера по трафику: $(sudo iptables -nvL -t filter --line-numbers)" >> /home/ubuntu/cron_info.log 2>&1