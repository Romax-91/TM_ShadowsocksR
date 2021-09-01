#!/bin/bash
echo '*-*-------Kila All Gunicorn Process-----*-*'
killall gunicorn
echo '------Strat Gunicorn------'
gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 api:app