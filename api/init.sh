#!/bin/bash
apt-get update
apt-get -y install python3-pip
apt-get install vnstat
systemctl restart vnstat
pip3 install fastapi
pip install uvicorn[standard]
pip3 install uvicorn
pip3 install gunicorn
pip install hurry.filesize
pip3 install hurry.filesize

gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 api:app

crontab -l | { cat; echo "0 */6 * * * /home/ubuntu/TM_ShadowsocksR-main/api/python3 parser.py  >> /home/ubuntu/api/parser.log 2>&1"; } | crontab -
crontab -l | { cat; echo "0 */24 * * * /home/ubuntu/TM_ShadowsocksR-main/api/restart_api >> /home/ubuntu/api/api.log 2>&1"; } | crontab -