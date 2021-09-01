from typing import Optional
from fastapi import FastAPI
import json
import subprocess
import configparser

app = FastAPI()


def current_interface():
    config = configparser.ConfigParser()
    config.read('init.ini')
    return config['SETTINGS']['interface']


def current_port():
    config = configparser.ConfigParser()
    config.read('init.ini')
    return config['SETTINGS']['port']


# -d: Daily statistics for the last 30 days.
# -m: Monthly statistics for the past 12 months.
# -w: Statistics for the last 7 days, and the current and previous week.
# -h: Hourly statistics for the last 24 hours.

@app.get("/")
def main():
    data = ""
    try:
        interface = current_interface()
        output = subprocess.getoutput("vnstat --json")
        data = json.loads(output)
        for i in data['interfaces']:
            if i['name'] == interface:
                data = i['traffic']
                return data

    except Exception as e:
        return {"error": "PATH=/ {}".format(e)}


@app.get("/init-vnstat")
def init_vnstat():
    try:
        subprocess.getoutput("apt-get install vnstat")
        subprocess.getoutput("systemctl restart vnstat")
        return {"ok": "install vnstat"}
    except Exception as e:
        return {"error": "install vnstat - {}".format(e)}


@app.get("/interfaces")
def interfaces():
    data = ""
    try:
        output = subprocess.getoutput("ip link show")
        return output

    except Exception as e:
        return {"error": str(e)}


@app.get("/interface")
def interface():
    try:
        interface = current_interface()
        return {"interface", interface}

    except Exception as e:
        return {"error": str(e)}


@app.get("/set-interface/{i}")
def set_interface(i):
    try:
        config = configparser.ConfigParser()
        config.read('init.ini')
        config.set("SETTINGS", "interface", i)
        cfg_file = open("init.ini", 'w')

        config.write(cfg_file)
        cfg_file.close()
        return {i}

    except Exception as e:
        return {"error": str(e)}


@app.get("/port")
def port():
    try:
        port = current_port()
        return {str(port)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/set-port/{p}")
def set_port(p):
    try:
        config = configparser.ConfigParser()
        config.read('init.ini')
        config.set("SETTINGS", "port", p)
        cfg_file = open("init.ini", 'w')

        config.write(cfg_file)
        cfg_file.close()

        return {p}

    except Exception as e:
        return {"error": str(e)}


@app.get("/limit")
def limit():
    config = configparser.ConfigParser()
    config.read('init.ini')

    l = config['SETTINGS']['limit']
    try:
        return {str(l)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/set-limit/{l}")
def set_limit(l):

    try:
        config = configparser.ConfigParser()
        config.read('init.ini')
        config.set("SETTINGS", "limit", l)
        cfg_file = open("init.ini", 'w')

        config.write(cfg_file)
        cfg_file.close()

        return {l}

    except Exception as e:
        return {"error": str(e)}


@app.get("/h")
def hour():
    data = ""
    interface = current_interface()
    try:
        output = subprocess.getoutput("vnstat --json")
        data = json.loads(output)
        for i in data['interfaces']:
            if i['name'] == interface:
                data = i['traffic']['hour']
                return data

    except Exception as e:
        return {"error": str(e)}


@app.get("/d")
def day():
    data = ""
    interface = current_interface()
    try:
        output = subprocess.getoutput("vnstat --json")
        data = json.loads(output)
        for i in data['interfaces']:
            if i['name'] == interface:
                data = i['traffic']['day']
                return data

    except Exception as e:
        return {"error": str(e)}


@app.get("/m")
def month():
    data = ""
    interface = current_interface()
    try:
        output = subprocess.getoutput("vnstat --json")
        data = json.loads(output)
        for i in data['interfaces']:
            if i['name'] == interface:
                data = i['traffic']['month']
                return data

    except Exception as e:
        return {"error": str(e)}


@app.get("/all")
def all_stat():
    data = ""
    try:
        output = subprocess.getoutput("vnstat --json")
        data = json.loads(output)
        return data

    except Exception as e:
        return {"error": str(e)}


@app.get("/iptables")
def ip_tables():
    try:
        port = current_port()
        output = subprocess.getoutput("iptables -L -n | grep -i {} ".format(port))
        return {"iptables": str(output)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/block")
def block():
    try:
        interface = current_interface()
        port = current_port()

        subprocess.getoutput("iptables -t filter -A INPUT -p tcp --dport {} -j DROP".format(port))
        return {"msg": "BLOCKING PORT {} on {}".format(port, interface)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/unblock")
def unblock():
    try:
        interface = current_interface()
        port = current_port()

        subprocess.getoutput("iptables -F")
        return {"msg": "UNBLOCKING PORT {} on {}".format(port, interface)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/cmd/{c}")
async def cmd(c):
    try:
        output = subprocess.getoutput(str(c))
        return {"cmd": str(c),
                "out": str(output)}

    except Exception as e:
        return {"error": str(e)}
