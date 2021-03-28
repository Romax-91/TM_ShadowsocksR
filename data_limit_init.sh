#!/bin/bash
# init limit data per user/443
server="[AWS $(sudo curl ifconfig.me)] "
sudo iptables -I OUTPUT -p tcp --sport 443 -j DROP
sudo iptables -I OUTPUT -p tcp --sport 443 -m quota --quota 14000000000 -j ACCEPT
telegram-send "$server- Ограничение  трафика на 443 порту (лимит 14Гб) - Установлено"
telegram-send "$server- Статистика сервера по трафику: $(sudo iptables -nvL -t filter --line-numbers)" >> /home/ubuntu/cron_info.log 2>&1
