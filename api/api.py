from typing import Optional
from fastapi import FastAPI
import json
import subprocess
import configparser

app = FastAPI()

# load default config
config = configparser.ConfigParser()
config.read('init.ini')

interface = config['SETTINGS']['interface']
print("interface ", interface)

port = config['SETTINGS']['port']
print("PORT ", port)

#
# config.set("SETTINGS", "port", port)
# config.set("SETTINGS", "interface", interface)
# cfg_file = open("sample.ini", 'w')
# config.write(cfg_file)
# cfg_file.close()

# -d: Daily statistics for the last 30 days.
# -m: Monthly statistics for the past 12 months.
# -w: Statistics for the last 7 days, and the current and previous week.
# -h: Hourly statistics for the last 24 hours.


@app.get("/")
def main():
    data = ""
    try:
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
    config = configparser.ConfigParser()
    config.read('init.ini')

    interface = config['SETTINGS']['interface']

    try:
        return {"interface", interface}

    except Exception as e:
        return {"error": str(e)}


@app.get("/set-interface/{i}")
def set_interface(i):
    global interface
    try:
        interface = i
        config = configparser.ConfigParser()
        config.read('init.ini')
        config.set("SETTINGS", "interface", interface)
        cfg_file = open("init.ini", 'w')

        config.write(cfg_file)
        cfg_file.close()
        return {interface}

    except Exception as e:
        return {"error": str(e)}


@app.get("/port")
def port():
    config = configparser.ConfigParser()
    config.read('init.ini')

    port = config['SETTINGS']['port']
    print("PORT ", port)

    try:
        return {str(port)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/set-port/{p}")
def set_port(p):
    global port
    port = p

    try:
        config = configparser.ConfigParser()
        config.read('init.ini')
        config.set("SETTINGS", "port", port)
        cfg_file = open("init.ini", 'w')

        config.write(cfg_file)
        cfg_file.close()

        return {port}

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
    try:
        output = subprocess.getoutput("vnstat --json")
        data = json.loads(output)
        print(interface)
        for i in data['interfaces']:
            if i['name'] == interface:
                print(i)
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


@app.get("/block")
def block():
    try:
        subprocess.getoutput("iptables -t filter -A INPUT -p tcp --dport {} -j DROP".format(port))
        return {"msg": "BLOCKING PORT {} on {}".format(port, interface)}

    except Exception as e:
        return {"error": str(e)}


@app.get("/unblock")
def unblock():
    try:
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



